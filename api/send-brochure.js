// 소개서 요청 접수 — 즉시 응답 후 백그라운드 처리 함수를 별도 호출
export const config = {
  // 발송 완료(PDF 첨부 + AI 문구 생성 + 메일 2건)를 끝까지 기다리므로 여유를 둔다
  maxDuration: 60,
};

// ── Rate Limiter (IP당 분당 20회) ──
const RATE_LIMIT_WINDOW = 60 * 1000; // 1분
const RATE_LIMIT_MAX = 20;
const ipHits = new Map(); // { ip: { count, resetAt } }

function isRateLimited(ip) {
  const now = Date.now();
  const entry = ipHits.get(ip);
  if (!entry || now > entry.resetAt) {
    ipHits.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW });
    return false;
  }
  entry.count++;
  if (entry.count > RATE_LIMIT_MAX) return true;
  return false;
}

// ── 입력값 정리 (XSS 방지) ──
function sanitize(str) {
  if (!str) return str;
  return String(str).replace(/[<>&"']/g, c => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'
  })[c]).trim().slice(0, 200);
}

// ── 허용 도메인 (CORS) ──
const ALLOWED_ORIGINS = ['https://breadai.co.kr', 'https://www.breadai.co.kr', 'http://localhost:3000', 'http://127.0.0.1:5500'];

export default async function handler(req, res) {
  // CORS headers — 허용 도메인만
  const reqOrigin = req.headers.origin || '';
  if (ALLOWED_ORIGINS.includes(reqOrigin)) {
    res.setHeader('Access-Control-Allow-Origin', reqOrigin);
  } else {
    res.setHeader('Access-Control-Allow-Origin', 'https://breadai.co.kr');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // Rate limit 체크
  const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.socket?.remoteAddress || 'unknown';
  if (isRateLimited(clientIp)) {
    return res.status(429).json({ error: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.' });
  }

  // Honeypot 체크 (숨겨진 필드에 값이 있으면 봇)
  if (req.body._hp) {
    return res.status(200).json({ success: true }); // 봇에게는 성공인 척
  }

  const email = sanitize(req.body.email);
  const company = sanitize(req.body.company);
  const name = sanitize(req.body.name);
  const department = sanitize(req.body.department);
  const position = sanitize(req.body.position);
  const phone = sanitize(req.body.phone);

  // 이메일 형식 검증 강화
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!email || !emailRegex.test(email)) {
    return res.status(400).json({ error: '유효한 이메일을 입력해주세요.' });
  }
  if (!company || company.length < 2 || !name || name.length < 2) {
    return res.status(400).json({ error: '필수 정보를 입력해주세요.' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  // ── 발송 처리 함수 호출 ──
  // 이전에는 fire-and-forget(응답을 안 기다림) 방식이었으나, 서버리스에서
  // 응답 반환 직후 함수가 정지되면 이 요청이 중간에 끊겨 메일이 조용히 누락됐다.
  // (화면에는 "발송 완료"가 뜨는데 실제로는 안 나가는 문제)
  // → 완료를 끝까지 기다리고, 실패하면 사용자에게 실패를 알린다.
  const PROCESS_SECRET = process.env.PROCESS_SECRET || 'brochure-internal-key';
  const origin = `https://${req.headers.host || 'www.breadai.co.kr'}`;

  try {
    const procRes = await fetch(`${origin}/api/send-brochure-process`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-internal-secret': PROCESS_SECRET,
      },
      body: JSON.stringify({ email, company, name, department, position, phone, remarks: sanitize(req.body.remarks) || '' }),
    });

    if (!procRes.ok) {
      const detail = await procRes.text().catch(() => '');
      console.error('Brochure send failed:', procRes.status, detail.slice(0, 500));
      return res.status(502).json({
        error: '소개서 발송에 실패했습니다. contact@breadai.co.kr 로 요청해주시면 바로 보내드리겠습니다.',
      });
    }

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Brochure send error:', err);
    return res.status(502).json({
      error: '소개서 발송에 실패했습니다. contact@breadai.co.kr 로 요청해주시면 바로 보내드리겠습니다.',
    });
  }
}
