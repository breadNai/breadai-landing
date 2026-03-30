// 소개서 요청 접수 — 즉시 응답 후 백그라운드 처리 함수를 별도 호출
export const config = {
  maxDuration: 10,
};

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
