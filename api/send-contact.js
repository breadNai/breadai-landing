// 도입 문의 접수 — 팀 알림 + 문의자 접수 확인 메일 발송 (Resend)
// 이전에는 외부 서비스(Web3Forms)를 거쳤으나 수신이 누락되어 자체 발송으로 전환.
export const config = {
  maxDuration: 30,
};

// ── Rate Limiter (IP당 분당 10회) ──
const RATE_LIMIT_WINDOW = 60 * 1000;
const RATE_LIMIT_MAX = 10;
const ipHits = new Map();

function isRateLimited(ip) {
  const now = Date.now();
  const entry = ipHits.get(ip);
  if (!entry || now > entry.resetAt) {
    ipHits.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW });
    return false;
  }
  entry.count++;
  return entry.count > RATE_LIMIT_MAX;
}

// ── 입력값 정리 (XSS 방지) ──
function sanitize(str, max = 500) {
  if (!str) return '';
  return String(str).replace(/[<>&"']/g, c => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'
  })[c]).trim().slice(0, max);
}

const ALLOWED_ORIGINS = [
  'https://breadai.co.kr', 'https://www.breadai.co.kr',
  'http://localhost:3000', 'http://127.0.0.1:5500',
];

export default async function handler(req, res) {
  const reqOrigin = req.headers.origin || '';
  res.setHeader('Access-Control-Allow-Origin',
    ALLOWED_ORIGINS.includes(reqOrigin) ? reqOrigin : 'https://breadai.co.kr');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim()
    || req.socket?.remoteAddress || 'unknown';
  if (isRateLimited(clientIp)) {
    return res.status(429).json({ error: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.' });
  }

  // Honeypot (봇이면 조용히 성공 응답)
  if (req.body._hp) {
    console.log('Honeypot triggered (contact):', { company: req.body.company });
    return res.status(200).json({ success: true });
  }

  const company    = sanitize(req.body.company, 100);
  const name       = sanitize(req.body.name, 50);
  const email      = sanitize(req.body.email, 100);
  const phone      = sanitize(req.body.phone, 30);
  const department = sanitize(req.body.department, 50);
  const position   = sanitize(req.body.position, 50);
  const plan       = sanitize(req.body.plan, 50);
  const message    = sanitize(req.body.message, 2000);

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!email || !emailRegex.test(email)) {
    return res.status(400).json({ error: '유효한 이메일을 입력해주세요.' });
  }
  if (!company || company.length < 2) {
    return res.status(400).json({ error: '회사명을 입력해주세요.' });
  }
  if (!name || name.length < 2) {
    return res.status(400).json({ error: '담당자 성함을 입력해주세요.' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const now = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
  const row = (label, value) =>
    `<tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F;width:110px;white-space:nowrap">${label}</td>` +
    `<td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530">${value || '-'}</td></tr>`;

  try {
    // ── 1) 팀 알림 메일 ──
    const notifyRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread & AI <contact@breadai.co.kr>',
        to: 'contact@breadai.co.kr',
        reply_to: email,
        subject: plan
          ? `[도입 문의 · ${plan}] ${company} ${name}`
          : `[도입 문의] ${company} ${name}`,
        html: `
          <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:620px;margin:0 auto;padding:24px">
            <h2 style="color:#3D3530;margin-bottom:20px">도입 문의가 접수되었습니다</h2>
            <table style="width:100%;border-collapse:collapse;font-size:15px">
              ${row('회사명', `<strong>${company}</strong>`)}
              ${row('담당자', name)}
              ${row('부서', department)}
              ${row('직함', position)}
              ${row('이메일', `<a href="mailto:${email}" style="color:#CC7247">${email}</a>`)}
              ${row('연락처', phone)}
              ${row('관심 플랜', plan || '일반 문의')}
              ${row('접수 시각', now)}
            </table>
            ${message ? `
            <div style="margin-top:20px;padding:16px;background:#FDF5ED;border-radius:10px;border:1px solid rgba(204,114,71,0.15)">
              <div style="font-size:13px;font-weight:700;color:#CC7247;margin-bottom:8px">문의 내용</div>
              <div style="font-size:14px;color:#3D3530;line-height:1.7;white-space:pre-wrap">${message}</div>
            </div>` : ''}
            <p style="margin-top:22px;font-size:13px;color:#81746F">
              이 메일에 그대로 회신하면 ${name}님에게 전송됩니다.
            </p>
          </div>
        `,
      }),
    });

    if (!notifyRes.ok) {
      const errBody = await notifyRes.text().catch(() => '');
      console.error('Resend contact notify error:', notifyRes.status, errBody.slice(0, 500));
      return res.status(502).json({
        error: '문의 전송에 실패했습니다. contact@breadai.co.kr 로 보내주시면 바로 확인하겠습니다.',
      });
    }

    // ── 2) 문의자 접수 확인 메일 (실패해도 전체 성공은 유지) ──
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread & AI <contact@breadai.co.kr>',
        reply_to: 'contact@breadai.co.kr',
        to: [email],
        subject: '[Bread & AI] 도입 문의가 접수되었습니다',
        html: `
          <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:0 auto;padding:24px">
            <div style="text-align:center;margin-bottom:28px">
              <div style="font-size:20px;font-weight:800;color:#3D3530">Bread &amp; AI</div>
            </div>
            <h2 style="color:#3D3530;margin-bottom:16px">문의가 접수되었습니다</h2>
            <p style="font-size:15px;color:#3D3530;line-height:1.7">
              안녕하세요, <strong>${company}</strong> ${name}님.<br><br>
              도입 문의를 남겨주셔서 감사합니다.<br>
              담당자가 확인 후 <strong>영업일 기준 1일 내</strong>로 연락드리겠습니다.
            </p>
            <div style="margin-top:24px;padding:16px;background:#F5EDE4;border-radius:10px;text-align:center">
              <div style="font-size:13px;color:#81746F;margin-bottom:10px">기다리시는 동안 직접 체험해 보세요</div>
              <a href="https://app.breadai.co.kr/" style="display:inline-block;padding:12px 28px;background:#CC7247;color:#fff;border-radius:8px;font-size:15px;font-weight:700;text-decoration:none">무료로 시작하기 →</a>
            </div>
            <div style="margin-top:30px;padding-top:16px;border-top:1px solid #E8DFD5;font-size:12px;color:#81746F;text-align:center">
              &copy; 2026 Bread &amp; AI. All rights reserved.
            </div>
          </div>
        `,
      }),
    }).catch(err => console.error('Contact confirmation email failed:', err));

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Contact request error:', err);
    return res.status(500).json({ error: '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.' });
  }
}
