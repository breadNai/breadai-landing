// 신규 고객사 리스트 요청 접수 — 폼 데이터 수신 후 팀 알림 이메일 발송
import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export const config = {
  maxDuration: 10,
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
  if (entry.count > RATE_LIMIT_MAX) return true;
  return false;
}

// ── 입력값 정리 (XSS 방지) ──
function sanitize(str) {
  if (!str) return str;
  return String(str).replace(/[<>&"']/g, c => ({
    '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;'
  })[c]).trim().slice(0, 500);
}

// ── 허용 도메인 (CORS) ──
const ALLOWED_ORIGINS = ['https://breadai.co.kr', 'https://www.breadai.co.kr', 'http://localhost:3000', 'http://127.0.0.1:5500'];

export default async function handler(req, res) {
  // CORS headers
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

  // Rate limit
  const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.socket?.remoteAddress || 'unknown';
  if (isRateLimited(clientIp)) {
    return res.status(429).json({ error: '요청이 너무 많습니다. 잠시 후 다시 시도해주세요.' });
  }

  // Honeypot
  if (req.body._hp) {
    return res.status(200).json({ success: true });
  }

  const company = sanitize(req.body.company);
  const name = sanitize(req.body.name);
  const url = sanitize(req.body.url);
  const email = sanitize(req.body.email);
  const fileName = sanitize(req.body.fileName);
  const fileKey = req.body.fileKey || ''; // S3에 업로드된 파일의 키

  // 검증
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

  // ── S3 다운로드 URL 생성 (파일이 있는 경우) ──
  let downloadUrl = '';
  if (fileKey && process.env.AWS_ACCESS_KEY_ID && process.env.AWS_SECRET_ACCESS_KEY && process.env.AWS_S3_BUCKET) {
    try {
      const client = new S3Client({
        region: 'ap-northeast-2',
        credentials: {
          accessKeyId: process.env.AWS_ACCESS_KEY_ID,
          secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
        },
      });
      const command = new GetObjectCommand({
        Bucket: process.env.AWS_S3_BUCKET,
        Key: fileKey,
      });
      downloadUrl = await getSignedUrl(client, command, { expiresIn: 7 * 24 * 60 * 60 }); // 7일 유효
    } catch (err) {
      console.error('S3 download URL error:', err);
    }
  }

  // 소개서 링크 HTML
  const attachmentHtml = downloadUrl
    ? `<a href="${downloadUrl}" style="color:#CC7247;text-decoration:underline">${fileName || '소개서 다운로드'}</a> (7일간 유효)`
    : (fileName || '없음');

  try {
    // ── 팀 알림 이메일 발송 (Resend) ──
    const notifyRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread&AI <noreply@breadai.co.kr>',
        to: ['contact@breadai.co.kr', 'wk.bae@breadai.co.kr'],
        subject: `[신규 고객사 리스트 요청] ${company}`,
        html: `
          <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:0 auto;padding:24px">
            <h2 style="color:#3D3530;margin-bottom:20px">신규 고객사 리스트 요청이 접수되었습니다</h2>
            <table style="width:100%;border-collapse:collapse;font-size:15px">
              <tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F;width:120px">회사명</td><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530;font-weight:600">${company}</td></tr>
              <tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F">담당자</td><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530">${name || '-'}</td></tr>
              <tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F">홈페이지</td><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530">${url || '-'}</td></tr>
              <tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F">이메일</td><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530"><a href="mailto:${email}" style="color:#CC7247">${email}</a></td></tr>
              <tr><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#81746F">첨부 소개서</td><td style="padding:10px 12px;border-bottom:1px solid #E8DFD5;color:#3D3530">${attachmentHtml}</td></tr>
              <tr><td style="padding:10px 12px;color:#81746F">접수 시각</td><td style="padding:10px 12px;color:#3D3530">${now}</td></tr>
            </table>
            <div style="margin-top:24px;padding:16px;background:#FDF5ED;border-radius:10px;border:1px solid rgba(204,114,71,0.15)">
              <div style="font-size:13px;font-weight:700;color:#CC7247;margin-bottom:6px">Action Required</div>
              <div style="font-size:14px;color:#3D3530;line-height:1.6">
                1. Bread&AI에서 해당 회사 소개서 기반 고객사 탐색 실행<br>
                2. Top 5 결과 중 3개는 노출, 2개는 블러 처리하여 스크린샷<br>
                3. 영업일 1일 내로 ${email}로 결과 메일 발송
              </div>
            </div>
          </div>
        `,
      }),
    });

    if (!notifyRes.ok) {
      const errBody = await notifyRes.text();
      console.error('Resend error:', errBody);
    }

    // ── 요청자에게 접수 확인 이메일 발송 ──
    await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread&AI <noreply@breadai.co.kr>',
        to: [email],
        subject: `[Bread&AI] 신규 고객사 리스트 요청이 접수되었습니다`,
        html: `
          <div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:600px;margin:0 auto;padding:24px">
            <div style="text-align:center;margin-bottom:32px">
              <div style="font-size:20px;font-weight:800;color:#3D3530">Bread & AI</div>
            </div>
            <h2 style="color:#3D3530;margin-bottom:16px">요청이 접수되었습니다</h2>
            <p style="font-size:15px;color:#3D3530;line-height:1.7">
              안녕하세요, <strong>${company}</strong> ${name ? name + '님' : '담당자님'}!<br><br>
              신규 고객사 리스트 요청이 정상적으로 접수되었습니다.<br>
              AI가 귀사에 맞는 고객사를 탐색 중이며, <strong>영업일 기준 1일 내</strong>로 결과를 보내드리겠습니다.
            </p>
            <div style="margin-top:24px;padding:16px;background:#F5EDE4;border-radius:10px;text-align:center">
              <div style="font-size:13px;color:#81746F;margin-bottom:8px">기다리시는 동안 직접 체험해 보세요</div>
              <a href="https://app.breadai.co.kr/" style="display:inline-block;padding:12px 28px;background:#CC7247;color:white;border-radius:8px;font-size:15px;font-weight:700;text-decoration:none">7일 무료 체험 시작하기 →</a>
            </div>
            <div style="margin-top:32px;padding-top:16px;border-top:1px solid #E8DFD5;font-size:12px;color:#81746F;text-align:center">
              &copy; 2026 Bread & AI. All rights reserved.
            </div>
          </div>
        `,
      }),
    }).catch(err => console.error('Confirmation email failed:', err));

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Prospect request error:', err);
    return res.status(500).json({ error: '서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.' });
  }
}
