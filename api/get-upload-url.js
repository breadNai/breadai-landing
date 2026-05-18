// S3 Presigned URL 발급 — 프론트에서 직접 S3로 파일 업로드할 수 있게
import { S3Client, PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

export const config = { maxDuration: 10 };

const ALLOWED_ORIGINS = ['https://breadai.co.kr', 'https://www.breadai.co.kr', 'http://localhost:3000', 'http://127.0.0.1:5500'];

export default async function handler(req, res) {
  // CORS
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

  const { fileName, contentType } = req.body;
  if (!fileName) return res.status(400).json({ error: 'fileName is required' });

  const bucket = process.env.AWS_S3_BUCKET;
  if (!bucket || !process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  // 파일명에 타임스탬프 + 랜덤 추가 (중복 방지)
  const timestamp = Date.now();
  const rand = Math.random().toString(36).slice(2, 8);
  const safeName = fileName.replace(/[^a-zA-Z0-9가-힣._-]/g, '_');
  const key = `prospects/${timestamp}-${rand}/${safeName}`;

  const client = new S3Client({
    region: 'ap-northeast-2',
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
    // 브라우저에서 직접 업로드 시 체크섬 헤더 문제 방지
    requestChecksumCalculation: 'WHEN_REQUIRED',
    responseChecksumValidation: 'WHEN_REQUIRED',
  });

  try {
    const command = new PutObjectCommand({
      Bucket: bucket,
      Key: key,
      ContentType: contentType || 'application/pdf',
    });

    const uploadUrl = await getSignedUrl(client, command, {
      expiresIn: 600, // 10분 유효
      // 브라우저 PUT 요청에서 체크섬 헤더를 빼야 CORS 문제 없음
      unhoistableHeaders: new Set(['x-amz-checksum-crc32']),
    });

    return res.status(200).json({ uploadUrl, key });
  } catch (err) {
    console.error('Presigned URL error:', err);
    return res.status(500).json({ error: '업로드 URL 생성 실패' });
  }
}
