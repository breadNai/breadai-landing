// 소개서 요청 접수 — 즉시 응답 후 백그라운드 처리 함수를 별도 호출
export const config = {
  maxDuration: 10,
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
  const origin = req.headers.origin || '';
  if (ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
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

  // ── 백그라운드 처리 함수 호출 (fire-and-forget) ──
  const PROCESS_SECRET = process.env.PROCESS_SECRET || 'brochure-internal-key';
  const origin = `https://${req.headers.host || 'www.breadai.co.kr'}`;

  // fetch를 먼저 시작하고, 요청이 Vercel 네트워크에 도달할 시간을 확보
  fetch(`${origin}/api/send-brochure-process`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-internal-secret': PROCESS_SECRET,
    },
    body: JSON.stringify({ email, company, name, department, position, phone }),
  }).catch(err => console.error('Background trigger failed:', err));

  // Vercel이 함수 종료하기 전에 HTTP 요청이 나갈 시간 확보 (1.5초)
  await new Promise(resolve => setTimeout(resolve, 1500));

  // ── 응답 (유저 체감 ~2초) ──
  return res.status(200).json({ success: true });
}
