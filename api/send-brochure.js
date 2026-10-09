// 소개서 요청 접수: 방문자에게는 바로 접수 완료를 응답하고, 발송은 백그라운드에서 끝까지 진행
import { waitUntil } from '@vercel/functions';

export const config = {
  // 응답 후 백그라운드 발송(PDF 첨부 + AI 문구 생성 최대 90초 + 메일 2건)이 끝날 때까지 함수가 살아 있도록 여유를 둔다
  maxDuration: 120,
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

  // ── 발송 처리: 응답은 바로, 발송은 백그라운드로 ──
  // 8월 이전에는 처리 함수를 호출만 해두고 바로 응답했는데(fire-and-forget), 서버리스는 응답 직후
  // 함수를 멈출 수 있어 처리 요청이 중간에 끊기고 메일이 조용히 누락됐다. 그래서 한동안은 발송이
  // 끝날 때까지 방문자를 기다리게 했다. 지금은 waitUntil로 응답 이후에도 발송 작업이 끝날 때까지
  // 함수를 살려 두므로, 방문자는 바로 화면을 떠나도 되고 메일 누락도 없다.
  // 발송이 실패하면 방문자는 알 수 없으므로, 대신 contact@로 수동 발송 요청 알림을 보낸다.
  const PROCESS_SECRET = process.env.PROCESS_SECRET || 'brochure-internal-key';
  const origin = `https://${req.headers.host || 'www.breadai.co.kr'}`;
  const lead = { email, company, name, department, position, phone, remarks: sanitize(req.body.remarks) || '' };

  const job = (async () => {
    try {
      const procRes = await fetch(`${origin}/api/send-brochure-process`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-internal-secret': PROCESS_SECRET,
        },
        body: JSON.stringify(lead),
      });
      if (!procRes.ok) {
        const detail = await procRes.text().catch(() => '');
        console.error('Brochure send failed:', procRes.status, detail.slice(0, 500));
        await notifyFailure(RESEND_API_KEY, lead, `처리 함수 응답 ${procRes.status}`);
      }
    } catch (err) {
      console.error('Brochure send error:', err);
      await notifyFailure(RESEND_API_KEY, lead, String(err?.message || err));
    }
  })();

  waitUntil(job);
  return res.status(200).json({ success: true });
}

// ── 자동 발송 실패 시 담당자에게 수동 발송 요청 ──
async function notifyFailure(apiKey, lead, reason) {
  try {
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${apiKey}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: 'Bread&AI <contact@breadai.co.kr>',
        to: 'contact@breadai.co.kr',
        subject: `[확인 필요] 소개서 자동 발송 실패: ${lead.company} ${lead.name}`,
        html: `<div style="font-family:sans-serif;padding:20px;font-size:14px;color:#333;line-height:1.7">
          <p style="color:#B4472C;font-weight:700">소개서 자동 발송이 실패했습니다. 아래 분께 소개서를 직접 보내주세요.</p>
          <p>회사명: ${lead.company}<br>이름: ${lead.name}<br>부서: ${lead.department || '-'}<br>직함: ${lead.position || '-'}<br>
          이메일: <a href="mailto:${lead.email}">${lead.email}</a><br>연락처: ${lead.phone || '-'}</p>
          <p style="color:#888;font-size:12px">실패 사유: ${String(reason).slice(0, 300)}</p></div>`,
      }),
    });
  } catch (e) {
    console.error('Failure notice also failed:', e);
  }
}
