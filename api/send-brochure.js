export default async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { email, company, name, department, position, phone } = req.body;
  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: '유효한 이메일을 입력해주세요.' });
  }
  if (!company || !name) {
    return res.status(400).json({ error: '필수 정보를 입력해주세요.' });
  }

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const BROCHURE_URL = process.env.BROCHURE_PDF_URL || 'https://breadai.co.kr/BreadAI_소개서.pdf';
  const now = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });

  try {
    // 1) 방문자에게 소개서 메일 발송
    const visitorRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread & AI <contact@breadai.co.kr>',
        to: email,
        subject: '[Bread & AI] 요청하신 소개서를 보내드립니다',
        html: `
          <div style="font-family:'Pretendard Variable',sans-serif;max-width:560px;margin:0 auto;padding:40px 24px">
            <img src="https://breadai.co.kr/Bread%26AI_%EB%A1%9C%EA%B3%A0_%EB%B0%B0%EA%B2%BD%EC%A0%9C%EA%B1%B0.png" alt="Bread & AI" style="height:32px;margin-bottom:32px">
            <h2 style="font-size:22px;color:#1B2A4A;margin-bottom:12px">${name}님, 소개서를 보내드립니다</h2>
            <p style="font-size:15px;color:#4A5568;line-height:1.7;margin-bottom:24px">
              안녕하세요, Bread & AI입니다.<br>
              요청하신 제품 소개서를 아래 버튼을 눌러 다운로드하실 수 있습니다.<br>
              궁금하신 점이 있으시면 편하게 문의해 주세요.
            </p>
            <a href="${BROCHURE_URL}" style="display:inline-block;padding:14px 28px;background:#D97706;color:#fff;border-radius:10px;font-size:15px;font-weight:700;text-decoration:none">
              소개서 다운로드
            </a>
            <hr style="border:none;border-top:1px solid #E2E8F0;margin:32px 0 16px">
            <p style="font-size:12px;color:#94A3B8">
              Bread & AI — AI 맞춤 제안 솔루션<br>
              <a href="https://breadai.co.kr" style="color:#D97706">breadai.co.kr</a> ·
              <a href="mailto:contact@breadai.co.kr" style="color:#D97706">contact@breadai.co.kr</a>
            </p>
          </div>
        `,
      }),
    });

    if (!visitorRes.ok) {
      const err = await visitorRes.json();
      console.error('Visitor email failed:', err);
      return res.status(500).json({ error: '이메일 발송에 실패했습니다.' });
    }

    // 2) 승욱님에게 알림 메일 (리드 정보 포함)
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread & AI <contact@breadai.co.kr>',
        to: 'contact@breadai.co.kr',
        subject: `[소개서 요청] ${company} ${name}`,
        html: `
          <div style="font-family:sans-serif;padding:20px">
            <h3 style="color:#1B2A4A;margin-bottom:16px">새로운 소개서 요청</h3>
            <table style="font-size:14px;color:#333;border-collapse:collapse;width:100%">
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">회사명</td><td style="padding:8px 0;border-bottom:1px solid #eee">${company}</td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">이름</td><td style="padding:8px 0;border-bottom:1px solid #eee">${name}</td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">부서</td><td style="padding:8px 0;border-bottom:1px solid #eee">${department || '-'}</td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">직함</td><td style="padding:8px 0;border-bottom:1px solid #eee">${position || '-'}</td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">이메일</td><td style="padding:8px 0;border-bottom:1px solid #eee"><a href="mailto:${email}">${email}</a></td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap;border-bottom:1px solid #eee">연락처</td><td style="padding:8px 0;border-bottom:1px solid #eee">${phone || '-'}</td></tr>
              <tr><td style="padding:8px 16px 8px 0;font-weight:600;white-space:nowrap">요청 시각</td><td style="padding:8px 0">${now}</td></tr>
            </table>
          </div>
        `,
      }),
    });

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Send brochure error:', error);
    return res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
}
