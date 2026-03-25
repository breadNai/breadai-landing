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
  const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const BROCHURE_URL = process.env.BROCHURE_PDF_URL || 'https://breadai.co.kr/BreadAI_%EC%86%8C%EA%B0%9C%EC%84%9C.pdf';
  const now = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });

  // 직함/부서 조합으로 인사말 구성
  const positionText = position ? ` ${position}님` : '님';
  const deptText = department ? `${department} ` : '';

  try {
    // ── 1) PDF 첨부 준비 (base64) ──
    let attachments = [];
    try {
      const pdfRes = await fetch(BROCHURE_URL);
      if (pdfRes.ok) {
        const pdfBuffer = await pdfRes.arrayBuffer();
        const pdfBase64 = Buffer.from(pdfBuffer).toString('base64');
        attachments = [{
          filename: 'Bread_AI_제품소개서.pdf',
          content: pdfBase64,
        }];
      }
    } catch (pdfErr) {
      console.error('PDF fetch failed, sending without attachment:', pdfErr);
    }

    // ── 2) AI 맞춤 메시지 생성 (Claude API) ──
    let personalizedSection = '';
    if (ANTHROPIC_API_KEY) {
      try {
        const aiMessage = await generatePersonalizedMessage({
          apiKey: ANTHROPIC_API_KEY,
          company,
          department: department || '',
          position: position || '',
          email,
        });
        if (aiMessage) {
          personalizedSection = aiMessage;
        }
      } catch (aiErr) {
        console.error('AI personalization failed, using default:', aiErr);
      }
    }

    // AI 실패 시 기본 메시지
    if (!personalizedSection) {
      personalizedSection = `${company}에서 B2B 영업을 진행하시면서, 타겟 기업마다 제안서와 콜드 이메일을 일일이 작성하는 데 많은 시간을 쏟고 계시지 않으신가요?<br><br>Bread & AI는 영업할 기업을 AI가 자동으로 리서치하고, 그 기업에 <strong>왜 우리 제품이 필요한지</strong>를 논리적으로 설명하는 맞춤 제안서와 콜드 이메일을 자동 생성합니다.<br><br>100통의 똑같은 콜드메일 대신, <strong>상대방이 읽고 싶어지는 1통의 맞춤 제안</strong>. 맞춤 제안은 미팅이 되고, 미팅은 매출이 됩니다.`;
    }

    // ── 3) 방문자에게 소개서 메일 발송 ──
    const visitorRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread & AI <contact@breadai.co.kr>',
        reply_to: 'contact@breadai.co.kr',
        to: email,
        subject: `[Bread & AI] ${name}${positionText}, 요청하신 제품 소개서를 보내드립니다`,
        attachments,
        html: buildVisitorEmail({ company, deptText, name, positionText, personalizedSection }),
      }),
    });

    if (!visitorRes.ok) {
      const err = await visitorRes.json();
      console.error('Visitor email failed:', err);
      return res.status(500).json({ error: '이메일 발송에 실패했습니다.' });
    }

    // ── 4) 승욱님에게 알림 메일 (리드 정보 + AI 메시지) ──
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
            ${personalizedSection ? `
            <div style="margin-top:20px;padding:16px;background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px">
              <p style="font-size:13px;font-weight:600;color:#92400E;margin:0 0 8px">AI가 생성한 맞춤 메시지:</p>
              <p style="font-size:13px;color:#374151;line-height:1.6;margin:0">${personalizedSection}</p>
            </div>` : ''}
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


// ── AI 맞춤 메시지 생성 함수 (2-Branch) ──
async function generatePersonalizedMessage({ apiKey, company, department, position, email }) {
  const emailDomain = email.split('@')[1] || '';

  // 개인 이메일 도메인 → 회사 특정 불가 판단 기준
  const personalDomains = [
    'gmail.com', 'naver.com', 'daum.net', 'hanmail.net', 'kakao.com',
    'nate.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
    'me.com', 'live.com', 'msn.com', 'protonmail.com', 'mail.com',
  ];
  const isPersonalEmail = personalDomains.includes(emailDomain.toLowerCase());

  // ── Branch 판단: 회사를 특정할 수 있는가? ──
  // 조건: 회사명이 구체적 + (기업 이메일 도메인 OR 잘 알려진 회사명)
  // "개인", "테스트", "없음" 같은 더미 회사명 제외
  const dummyCompanyNames = ['개인', '없음', '테스트', 'test', 'none', 'n/a', '-', '없어요'];
  const isDummyCompany = dummyCompanyNames.some(d => company.trim().toLowerCase() === d);
  const canIdentify = !isDummyCompany && company.trim().length >= 2;

  let prompt;

  if (canIdentify) {
    // ═══ Branch A: 회사 특정 가능 → 맞춤 영업 메시지 ═══
    prompt = `당신은 Bread & AI의 영업 담당자입니다. 소개서를 요청한 잠재 고객에게 보낼 이메일의 핵심 본문을 작성하세요.

## Bread & AI 제품 정보
- B2B 영업의 성공률을 높이는 AI 맞춤 제안 솔루션
- 영업할 기업을 AI가 자동으로 리서치하고, "왜 우리 제품이 필요한지"를 설명하는 맞춤 제안서 + 콜드 이메일을 자동 생성
- 핵심 기능 3가지:
  · 탐색: AI가 가망 영역을 분석하고, Fit Score와 함께 최적의 타겟 기업 추천
  · 리서치: 타겟 기업을 실시간 웹 리서치 → 맞춤 제안 논리 자동 생성
  · 제작: 기업별 맞춤 콜드 이메일 + 제안서를 자동 생성, 바로 발송
- 가치: 100통의 똑같은 콜드메일 대신, 상대방이 읽고 싶어지는 1통의 맞춤 제안

## 소개서 요청자 정보
- 회사명: ${company}
- 부서: ${department || '(미입력)'}
- 직함: ${position || '(미입력)'}
- 이메일 도메인: ${emailDomain}

## 당신의 임무
이 회사가 **정확히 어떤 회사인지** 파악하세요 (회사명 + 이메일 도메인으로 추론).
그리고 이 회사의 사업 특성과${department ? ` ${department}의 업무 맥락을 고려하여` : ''} 아래 구조로 작성하세요:

### 작성 구조 (7-8줄)
1. (1-2줄) ${company}의 사업 특성을 구체적으로 언급하면서, 이 회사가 B2B 영업에서 겪을 만한 어려움을 짚어주세요.
   - 이 회사가 뭘 파는 회사인지, 어떤 고객에게 파는지 보여줘야 "아 이 사람이 우리를 알고 연락했구나" 느낌을 줌.
${department ? `   - ${department}에서 특히 겪을 영업 관련 pain point를 짚으면 더 효과적.` : ''}
2. (2-3줄) Bread & AI가 그 어려움을 어떻게 해결할 수 있는지 구체적으로 연결.
   - "${company}의 [구체적 상황]에서 Bread & AI를 활용하면 [구체적 효과]" 형태.
   - 기능을 나열하지 말고, 이 회사의 맥락에 맞춰서 가치를 설명.
3. (2-3줄) 미팅 유도: 첨부 소개서 확인 요청 + "귀사의 영업 프로세스에 맞춰 구체적인 활용 방안을 15-20분 정도 시연해 드리겠습니다" 느낌의 미팅 제안. 부담 없는 톤으로.

### 작성 규칙
- 과장 금지. 자연스럽고 단정한 비즈니스 톤.
- HTML 태그: <br> (줄바꿈), <strong> (강조) 정도만 사용.
- 절대 인사말(안녕하세요 등)이나 서명을 쓰지 마세요 — 별도로 추가됩니다.
- 순수 본문 텍스트만 출력. JSON이나 마크다운으로 감싸지 마세요.
- 만약 회사를 정확히 특정할 수 없다면, 회사명을 그대로 사용하되 무리하게 추측하지 마세요.`;

  } else {
    // ═══ Branch B: 회사 특정 불가 → 일반 강점 어필 메시지 ═══
    prompt = `당신은 Bread & AI의 영업 담당자입니다. 소개서를 요청한 잠재 고객에게 보낼 이메일의 핵심 본문을 작성하세요.

## Bread & AI 제품 정보
- B2B 영업의 성공률을 높이는 AI 맞춤 제안 솔루션
- 영업할 기업을 AI가 자동으로 리서치하고, "왜 우리 제품이 필요한지"를 설명하는 맞춤 제안서 + 콜드 이메일을 자동 생성
- 핵심 기능: 타겟 탐색 (Fit Score 추천), 기업 리서치 + 맞춤 제안 논리 생성, 콜드 이메일/제안서 자동 제작
- 가치: 100통의 똑같은 콜드메일 대신, 상대방이 읽고 싶어지는 1통의 맞춤 제안

## 상황
소개서를 요청한 분의 구체적인 회사 정보를 알 수 없습니다.
B2B 영업을 하는 일반적인 기업 담당자를 대상으로 작성하세요.

### 작성 구조 (7-8줄)
1. (1-2줄) B2B 영업 현장의 공통적인 어려움을 짚어주세요.
   - 콜드 이메일 응답률이 낮은 문제, 기업별 맞춤 제안에 시간이 너무 많이 드는 문제 등.
2. (2-3줄) Bread & AI의 핵심 차별점을 명확하게 어필.
   - "AI가 타겟 기업을 자동 리서치해서 맞춤 제안 논리를 만들어준다"는 핵심 가치.
   - 구체적인 기능 시나리오 1-2개로 체감되게.
3. (2-3줄) 미팅 유도: 첨부 소개서 확인 요청 + "귀사의 영업 프로세스에 맞춰 구체적인 활용 방안을 15-20분 정도 시연해 드리겠습니다" 느낌의 미팅 제안.

### 작성 규칙
- 과장 금지. 자연스럽고 단정한 비즈니스 톤.
- HTML 태그: <br> (줄바꿈), <strong> (강조) 정도만 사용.
- 절대 인사말(안녕하세요 등)이나 서명을 쓰지 마세요 — 별도로 추가됩니다.
- 순수 본문 텍스트만 출력. JSON이나 마크다운으로 감싸지 마세요.`;
  }

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 800,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  if (!response.ok) {
    const err = await response.text();
    console.error('Anthropic API error:', err);
    return null;
  }

  const data = await response.json();
  const text = data.content?.[0]?.text?.trim();
  return text || null;
}


// ── 이메일 HTML 템플릿 ──
function buildVisitorEmail({ company, deptText, name, positionText, personalizedSection }) {
  return `
<div style="font-family:-apple-system,'Pretendard Variable','Malgun Gothic',sans-serif;max-width:600px;margin:0 auto;padding:0;background:#ffffff">
  <!-- Header: 로고 아이콘 + 텍스트 -->
  <div style="padding:32px 32px 24px;border-bottom:1px solid #F1F5F9">
    <table cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td style="vertical-align:middle;padding-right:10px">
          <img src="https://breadai.co.kr/logo_email.png" alt="" style="height:32px;width:auto;display:block" />
        </td>
        <td style="vertical-align:middle">
          <span style="font-size:18px;font-weight:700;color:#1B2A4A;letter-spacing:-0.3px">Bread & AI</span>
        </td>
      </tr>
    </table>
  </div>

  <!-- Body -->
  <div style="padding:32px">
    <!-- 인사말 -->
    <p style="font-size:16px;color:#1B2A4A;font-weight:700;margin:0 0 8px;line-height:1.6">
      안녕하세요, ${company} ${deptText}${name}${positionText}.
    </p>
    <p style="font-size:15px;color:#374151;line-height:1.8;margin:0 0 24px">
      Bread & AI 대표 이승욱입니다.<br>
      제품 소개서를 신청해주셔서 감사합니다.
    </p>

    <!-- AI 맞춤 영업 메시지 -->
    <div style="background:#F8FAFC;border-left:4px solid #D97706;padding:20px 24px;margin:0 0 24px;border-radius:0 8px 8px 0">
      <p style="font-size:14px;color:#374151;line-height:1.85;margin:0">
        ${personalizedSection}
      </p>
    </div>

    <!-- 주요 기능 요약 -->
    <p style="font-size:14px;font-weight:700;color:#1B2A4A;margin:0 0 12px">Bread & AI 주요 기능</p>
    <table style="font-size:14px;color:#374151;line-height:1.7;border-collapse:collapse;width:100%;margin-bottom:24px">
      <tr>
        <td style="padding:10px 12px 10px 0;vertical-align:top;white-space:nowrap;color:#D97706;font-weight:700">탐색</td>
        <td style="padding:10px 0">AI가 가망 영역을 분석하고, Fit Score와 함께 최적의 타겟 기업을 추천</td>
      </tr>
      <tr style="border-top:1px solid #F1F5F9">
        <td style="padding:10px 12px 10px 0;vertical-align:top;white-space:nowrap;color:#D97706;font-weight:700">리서치</td>
        <td style="padding:10px 0">타겟 기업을 실시간으로 리서치하여, "왜 필요한지"를 설명하는 맞춤 제안 논리 생성</td>
      </tr>
      <tr style="border-top:1px solid #F1F5F9">
        <td style="padding:10px 12px 10px 0;vertical-align:top;white-space:nowrap;color:#D97706;font-weight:700">제작</td>
        <td style="padding:10px 0">기업별 맞춤 콜드 이메일 + 제안서를 자동 생성, 바로 발송 가능</td>
      </tr>
    </table>

    <!-- 소개서 안내 -->
    <p style="font-size:15px;color:#374151;line-height:1.8;margin:0 0 24px">
      첨부드린 소개서에서 더 자세한 내용을 확인하실 수 있습니다.<br>
      궁금하신 점이 있으시면 본 메일로 편하게 회신 부탁드립니다.
    </p>

    <!-- CTA 버튼 -->
    <a href="https://app.breadai.co.kr" style="display:inline-block;padding:14px 32px;background:#D97706;color:#ffffff;border-radius:10px;font-size:15px;font-weight:700;text-decoration:none;margin-bottom:8px">
      무료로 시작하기
    </a>
    <p style="font-size:12px;color:#94A3B8;margin:8px 0 0">계정 생성 후 바로 사용해보실 수 있습니다.</p>
  </div>

  <!-- Footer / 서명 -->
  <div style="padding:24px 32px;background:#F8FAFC;border-top:1px solid #F1F5F9">
    <p style="font-size:13px;color:#1B2A4A;font-weight:600;margin:0 0 4px">이승욱 대표</p>
    <p style="font-size:12px;color:#64748B;margin:0;line-height:1.6">
      Bread & AI — AI 맞춤 제안 솔루션<br>
      <a href="mailto:contact@breadai.co.kr" style="color:#D97706;text-decoration:none">contact@breadai.co.kr</a> ·
      <a href="https://breadai.co.kr" style="color:#D97706;text-decoration:none">breadai.co.kr</a>
    </p>
  </div>
</div>`;
}
