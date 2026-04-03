// 소개서 발송 백그라운드 처리 — PDF + AI 맞춤 메시지 + 이메일 발송
export const config = {
  maxDuration: 60,
};

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  // 내부 호출만 허용
  const PROCESS_SECRET = process.env.PROCESS_SECRET || 'brochure-internal-key';
  if (req.headers['x-internal-secret'] !== PROCESS_SECRET) {
    return res.status(403).json({ error: 'Forbidden' });
  }

  const { email, company, name, department, position, phone } = req.body;

  const RESEND_API_KEY = process.env.RESEND_API_KEY;
  const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
  if (!RESEND_API_KEY) {
    return res.status(500).json({ error: 'Server configuration error' });
  }

  const BROCHURE_URL = process.env.BROCHURE_PDF_URL || 'https://breadai.co.kr/BreadAI_%EC%86%8C%EA%B0%9C%EC%84%9C.pdf';
  const now = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
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
          filename: 'Bread_AI_AI_Sales_Intelligence_소개서.pdf',
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
      personalizedSection = `고객사를 대상으로 B2B 영업을 하다 보면, 맞춤 제안이 효과적이라는 건 누구나 알지만 한 기업당 제안을 준비하는 데 2~3시간이 걸리다 보니 결국 소수에게만 맞춤 제안을 하고 나머지는 같은 메일을 보내게 되는 현실을 겪고 계실 겁니다.<br><br>Bread & AI는 이 문제를 AI로 해결합니다. 타겟 기업명만 입력하면 AI가 그 기업의 현황과 Pain Point를 자동으로 분석하고, <strong>"왜 만나야 하는지"</strong> 설득하는 맞춤 제안 논리와 이메일, 제안서를 5분 만에 완성합니다. 맞춤 제안 도입 시 미팅율이 평균 30% 개선되고, 기존 2~3시간 걸리던 영업 준비를 5분으로 단축할 수 있습니다.<br><br>첨부드린 소개서에서 구체적인 내용을 확인하실 수 있고, 7일 무료 체험도 가능하니 부담 없이 먼저 사용해보시기 바랍니다. 추가로 궁금하신 점이 있으시면 편하게 말씀해주세요.`;
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
        subject: `[Bread & AI] ${name}${positionText}, 요청하신 AI 세일즈 인텔리전스 소개서입니다`,
        attachments,
        html: buildVisitorEmail({ company, deptText, name, positionText, personalizedSection }),
      }),
    });

    if (!visitorRes.ok) {
      const err = await visitorRes.json();
      console.error('Visitor email failed:', err);
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
    console.error('Send brochure process error:', error);
    return res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
}


// ── AI 맞춤 메시지 생성 함수 (2-Branch + Web Search) ──
async function generatePersonalizedMessage({ apiKey, company, department, position, email }) {
  const emailDomain = email.split('@')[1] || '';

  const personalDomains = [
    'gmail.com', 'naver.com', 'daum.net', 'hanmail.net', 'kakao.com',
    'nate.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
    'me.com', 'live.com', 'msn.com', 'protonmail.com', 'mail.com',
  ];
  const isPersonalEmail = personalDomains.includes(emailDomain.toLowerCase());

  const dummyExact = ['개인', '없음', 'test', 'none', 'n/a', '-', '없어요', 'asdf', 'aaa', 'ㅇㅇ', 'ㅇㅇㅇ', 'ㄱㄱ'];
  const dummyContains = ['테스트', 'test', 'sample', '더미', 'dummy', '임시'];
  const companyLower = company.trim().toLowerCase();
  const isDummyCompany = dummyExact.some(d => companyLower === d)
    || dummyContains.some(d => companyLower.includes(d));
  const canIdentify = !isDummyCompany && company.trim().length >= 2;

  let prompt;
  let useWebSearch = false;

  if (canIdentify) {
    useWebSearch = true;
    prompt = `당신은 Bread & AI의 영업 담당자입니다. 소개서를 요청한 잠재 고객에게 보낼 이메일의 핵심 본문을 작성하세요.

## ⚠️ 최우선 규칙: 반드시 웹 검색으로 확인
- 반드시 web_search 도구를 사용하여 "${company}"가 정확히 어떤 회사인지 검색하세요.
- 검색 결과에서 확인된 사실만 사용하세요. 추측하거나 지어내면 절대 안 됩니다.
- 검색해도 회사 정보를 확신할 수 없으면, 회사 구체 정보를 언급하지 말고 일반적인 B2B 영업 관점으로 작성하세요.
- 잘못된 업종/사업 내용을 쓰는 것은 치명적입니다. 차라리 안 쓰는 게 낫습니다.

## 🚫 절대 금지 (이것만은 반드시 지켜주세요)
- "검색 결과에서 ~를 확인할 수 없습니다", "정확한 정보를 찾을 수 없어", "~가 어떤 회사인지 명확하지 않으므로" 같은 문장은 ⛔️절대 금지⛔️입니다. 이 메일은 실제 고객에게 발송됩니다.
- 회사를 찾을 수 없으면 검색 실패를 언급하지 말고, 자연스럽게 일반 B2B 영업 맥락으로 작성하세요. 고객은 AI가 검색했다는 사실 자체를 몰라야 합니다.
- "검색", "확인", "조사", "리서치 결과" 등 검색 과정을 암시하는 단어를 본문에 절대 쓰지 마세요.

## Bread & AI 제품 정보
- AI 세일즈 인텔리전스: B2B 영업의 Pre-sales 전체를 AI로 맞춤화하여 미팅 수를 늘리는 솔루션
- 핵심 가치: B2C에서 맞춤 추천이 성과를 폭발시켰듯이, B2B 영업에서도 AI로 1:1 맞춤 제안이 가능해짐
- 기존 문제: 한 기업에 맞춤 제안을 준비하는 데 2~3시간 소요 → 소수 고객에게만 맞춤 가능, 나머지는 복붙
- Bread & AI 해결: 5분 만에 타겟 기업 리서치 → 맞춤 제안 논리 → 맞춤 이메일 + 제안서까지 자동 완성
- 3단계 프로세스:
  · STEP 1 탐색: 제품 소개서 업로드 → AI가 맞춤 제안이 먹힐 최적의 타겟 기업 자동 발굴
  · STEP 2 리서치: 타겟 기업 현황, Pain Point, 차별화 포인트 자동 분석 → 맞춤 제안 논리 + 콜드 이메일 생성
  · STEP 3 제안: 기업별 맞춤 15~20장 제안서 자동 생성, 바로 발송
- 성과: 맞춤 제안 도입 시 미팅율 +30% 개선, 영업 준비 시간 대폭 단축

## 소개서 요청자 정보
- 회사명: ${company}
- 부서: ${department || '(미입력)'}
- 직함: ${position || '(미입력)'}
- 이메일 도메인: ${emailDomain}

## 당신의 임무
1단계: web_search로 "${company}"를 검색하여 이 회사의 실제 사업 내용을 확인하세요.
2단계: 검색 결과를 바탕으로 아래 구조의 이메일 본문을 작성하세요.

### 작성 구조 (3단락, 각 단락 2-3줄)
⚠️ 가독성이 매우 중요합니다. 반드시 단락 사이에 <br><br>로 빈 줄을 넣어 단락을 구분하세요.

**1단락: 상대 회사 이해 + pain point (2-3줄)**
- ${company}의 사업을 1줄로 축약하여 언급하세요 ("~에 특화된 [업종]으로 이해하고 있습니다" 정도). 상대방은 자기 회사를 이미 아니까 길게 설명할 필요 없습니다.
- 이어서 이 회사가 B2B 영업에서 겪을 pain point를 짚으세요. 특히 "맞춤 제안을 하고 싶지만 시간이 없어서 결국 같은 자료를 보내는" 현실.
${department ? `- ${department}에서 특히 겪을 영업 관련 pain point를 짚으면 더 효과적.` : ''}
- ⛔ 회사 소개를 3줄 이상 쓰지 마세요. 상대방이 자기 회사 설명을 장황하게 읽는 건 지루합니다.

**2단락: Bread & AI가 해결하는 방식 (2-3줄)**
- "${company}의 [구체적 상황]에서 Bread & AI가 어떻게 도움이 되는지" 연결.
- 기능 나열이 아닌, 이 회사 맥락에서 AI 맞춤 제안이 만들어내는 구체적 임팩트를 보여주세요.
- 맞춤 제안 도입 시 미팅율 평균 30% 개선. 기존 2~3시간 걸리던 영업 준비가 5분으로 단축된다는 점 활용.

**3단락: 부드러운 CTA (2줄)**
- ⛔ "미팅하자", "시연을 보여드리겠다"는 말은 하지 마세요. 처음부터 미팅을 요구하면 부담스럽습니다.
- 대신: 첨부 소개서를 읽어달라고 하고, 7일 무료 체험도 가능하니 부담 없이 사용해보시라고 안내하세요.
- "추가로 궁금하신 점이 있으시면 편하게 말씀해주세요" 정도로 마무리.

### 출력 형식 — 반드시 지킬 것
- ⛔ "검색 결과를 바탕으로~", "~확인되었습니다", "작성해보겠습니다", "검색 결과에서 ~를 확인할 수 없습니다" 같은 메타 설명/사고 과정을 절대 출력하지 마세요. 이건 실제 고객에게 발송되는 이메일입니다.
- ⛔ 회사 정보를 찾지 못했다는 사실 자체를 절대 언급하지 마세요. 찾지 못했으면 일반 B2B 영업 맥락으로 매끄럽게 작성하면 됩니다.
- ⛔ 마크다운 문법(**bold**, *italic*, ## 등) 절대 금지. HTML 태그만 사용: <br> (줄바꿈), <strong> (강조).
- ⛔ 인사말(안녕하세요 등), 서명, "~드립니다" 같은 편지 형식의 시작/끝 금지 — 별도로 추가됩니다.
- 첫 글자부터 바로 본문 내용이 시작되어야 합니다. 어떤 전제 설명도 없이 곧바로 본문으로 시작하세요.
- 과장 금지. 자연스럽고 단정한 비즈니스 톤. 상대방의 사업을 이해하고 있는 영업 담당자의 말투로 쓰세요.
- 검색 결과로 확인되지 않은 회사 정보는 절대 언급하지 마세요.
- 순수 본문 텍스트(HTML)만 출력. JSON이나 코드블록으로 감싸지 마세요.`;

  } else {
    prompt = `당신은 Bread & AI의 영업 담당자입니다. 소개서를 요청한 잠재 고객에게 보낼 이메일의 핵심 본문을 작성하세요.

## Bread & AI 제품 정보
- AI 세일즈 인텔리전스: B2B 영업의 Pre-sales 전체를 AI로 맞춤화하여 미팅 수를 늘리는 솔루션
- 핵심 문제: B2B 맞춤 제안이 효과적이라는 건 누구나 알지만, 1건 준비에 2~3시간이 걸려 실행이 불가능했음
- Bread & AI 해결: 5분 만에 타겟 기업 리서치 → 맞춤 제안 논리 → 맞춤 이메일 + 제안서까지 자동 완성
- 성과: 맞춤 제안 도입 시 미팅율 +30% 개선, 복붙 콜드메일 대비 응답률 6배 이상

## 상황
소개서를 요청한 분의 구체적인 회사 정보를 알 수 없습니다.
B2B 영업을 하는 일반적인 기업 담당자를 대상으로 작성하세요.

### 작성 구조 (3단락, 각 단락 2-3줄)
⚠️ 가독성이 매우 중요합니다. 반드시 단락 사이에 <br><br>로 빈 줄을 넣어 단락을 구분하세요.

**1단락: B2B 영업 pain point 공감 (2-3줄)**
- "맞춤 제안을 하고 싶지만 시간이 없어서 결국 같은 메일을 100곳에 보내는" 현실의 공감.

**2단락: Bread & AI가 해결하는 방식 (2-3줄)**
- AI가 상대를 이해하고 맞춤 제안을 만들어내는 과정을 설명.
- 구체적 시나리오: "타겟 기업명만 입력하면 AI가 최신 현황을 리서치하고, 왜 만나야 하는지 설득하는 제안을 자동 완성"

**3단락: 부드러운 CTA (2줄)**
- ⛔ "미팅하자", "시연을 보여드리겠다"는 말은 하지 마세요. 부담스럽습니다.
- 대신: 첨부 소개서를 읽어달라고 하고, 7일 무료 체험도 가능하니 부담 없이 사용해보시라고 안내하세요.
- "추가로 궁금하신 점이 있으시면 편하게 말씀해주세요" 정도로 마무리.

### 작성 규칙
- 과장 금지. 자연스럽고 단정한 비즈니스 톤.
- HTML 태그: <br> (줄바꿈), <strong> (강조) 정도만 사용. 마크다운(**bold** 등) 절대 금지.
- 절대 인사말(안녕하세요 등)이나 서명을 쓰지 마세요 — 별도로 추가됩니다.
- 첫 글자부터 바로 본문 내용이 시작되어야 합니다.
- 순수 본문 텍스트만 출력. JSON이나 코드블록으로 감싸지 마세요.`;
  }

  const requestBody = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    system: '당신은 이메일 본문 작성기입니다. 출력은 실제 고객에게 발송되는 이메일입니다. 절대로 사고 과정, 메타 설명, 검색 과정, "~로 확인되었으나", "~작성하겠습니다" 같은 문장을 출력하지 마세요. 첫 글자부터 곧바로 이메일 본문만 출력하세요.',
    messages: [{ role: 'user', content: prompt }],
  };

  if (useWebSearch) {
    requestBody.tools = [{
      type: 'web_search_20250305',
      name: 'web_search',
      max_uses: 3,
    }];
  }

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const err = await response.text();
    console.error('Anthropic API error:', err);
    return null;
  }

  const data = await response.json();

  const textBlocks = (data.content || []).filter(b => b.type === 'text');
  let text = textBlocks.map(b => b.text).join('').trim();

  // ── 후처리: AI 메타 설명/사고 과정 제거 ──
  text = sanitizeAIOutput(text);

  return text || null;
}


// ── AI 출력 후처리 필터 ──
function sanitizeAIOutput(text) {
  if (!text) return text;

  // 메타 설명 패턴 (AI가 사고 과정을 노출하는 경우)
  const metaPatterns = [
    /검색\s*결과[에서으로]*\s*.*?확인[되었습니다하겠습니다]/g,
    /.*?[으로]로\s*확인되었으나.*?작성하겠습니다[.。]?\s*/g,
    /.*?명확하지\s*않아\s*일반적인.*?작성하겠습니다[.。]?\s*/g,
    /.*?구체적인\s*영업\s*환경이.*?작성하겠습니다[.。]?\s*/g,
    /일반적인\s*B2B\s*영업\s*맥락으로\s*작성하겠습니다[.。]?\s*/g,
    /작성해\s*보겠습니다[.。]?\s*/g,
    /작성해보겠습니다[.。]?\s*/g,
    /작성하겠습니다[.。]?\s*/g,
    /리서치\s*결과[를에]?\s*/g,
    /검색\s*결과[를에]?\s*바탕으로\s*/g,
    /웹\s*검색[을를]?\s*통해\s*/g,
    /확인[이되]?\s*어렵[습지]\s*/g,
  ];

  for (const pattern of metaPatterns) {
    text = text.replace(pattern, '');
  }

  // 첫 문장이 메타 설명으로 시작하는 경우 해당 문장 전체 제거
  // "~확인되었으나" "~파악되었으나" 등으로 시작하는 첫 문장
  text = text.replace(/^[^.。]*(?:확인되었으나|파악되었으나|확인할 수 없어|찾을 수 없어)[^.。]*[.。]\s*/i, '');

  // 연속 줄바꿈 정리
  text = text.replace(/(<br\s*\/?>){3,}/gi, '<br><br>');
  text = text.replace(/^\s*(<br\s*\/?>)+/i, ''); // 시작 부분 빈 줄바꿈 제거

  return text.trim();
}


// ── 이메일 HTML 템플릿 ──
function buildVisitorEmail({ company, deptText, name, positionText, personalizedSection }) {
  return `
<div style="font-family:-apple-system,'Pretendard Variable','Malgun Gothic',sans-serif;max-width:600px;margin:0 auto;padding:0;background:#ffffff">
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

  <div style="padding:32px">
    <p style="font-size:16px;color:#1B2A4A;font-weight:700;margin:0 0 8px;line-height:1.6">
      안녕하세요, ${company} ${deptText}${name}${positionText}.
    </p>
    <p style="font-size:15px;color:#374151;line-height:1.8;margin:0 0 20px">
      Bread & AI 대표 이승욱입니다.<br>
      제품 소개서를 신청해주셔서 감사합니다.
    </p>

    <div style="font-size:15px;color:#374151;line-height:1.9;margin:0 0 28px">
      ${personalizedSection}
    </div>

    <div style="background:#FFFBEB;border-radius:12px;padding:24px 28px;margin:0 0 28px">
      <p style="font-size:14px;font-weight:700;color:#1B2A4A;margin:0 0 16px">Bread & AI는 이렇게 작동합니다</p>
      <table style="font-size:14px;color:#374151;line-height:1.7;border-collapse:collapse;width:100%">
        <tr>
          <td style="padding:8px 16px 8px 0;vertical-align:top;color:#D97706;font-weight:700;width:24px">①</td>
          <td style="padding:8px 0"><strong>타겟 발굴</strong> — 맞춤 제안이 먹힐 최적의 기업을 AI가 자동으로 찾아줍니다</td>
        </tr>
        <tr>
          <td style="padding:8px 16px 8px 0;vertical-align:top;color:#D97706;font-weight:700;width:24px">②</td>
          <td style="padding:8px 0"><strong>리서치 &amp; 제안 논리</strong> — 상대 기업의 현황과 Pain Point를 분석, 맞춤 이메일 생성</td>
        </tr>
        <tr>
          <td style="padding:8px 16px 8px 0;vertical-align:top;color:#D97706;font-weight:700;width:24px">③</td>
          <td style="padding:8px 0"><strong>맞춤 제안서</strong> — 5분 만에 기업별 맞춤 제안서까지 완성</td>
        </tr>
      </table>
    </div>

    <p style="font-size:15px;color:#374151;line-height:1.8;margin:0 0 24px">
      첨부드린 소개서에서 더 자세한 내용을 확인하실 수 있습니다.<br>
      7일 무료 체험도 가능하니 부담 없이 먼저 사용해보시고,<br>
      추가로 궁금하신 점이 있으시면 편하게 회신 부탁드립니다.
    </p>

    <a href="https://app.breadai.co.kr" style="display:inline-block;padding:14px 32px;background:#D97706;color:#ffffff;border-radius:10px;font-size:15px;font-weight:700;text-decoration:none;margin-bottom:8px">
      7일 무료 체험하기
    </a>
    <p style="font-size:12px;color:#D97706;font-weight:600;margin:8px 0 0">결제 불필요 · 1분 만에 시작</p>
  </div>

  <div style="padding:24px 32px;background:#F8FAFC;border-top:1px solid #F1F5F9">
    <p style="font-size:13px;color:#1B2A4A;font-weight:600;margin:0 0 4px">이승욱 대표</p>
    <p style="font-size:12px;color:#64748B;margin:0;line-height:1.6">
      Bread & AI — AI Sales Intelligence<br>
      <a href="mailto:contact@breadai.co.kr" style="color:#D97706;text-decoration:none">contact@breadai.co.kr</a> ·
      <a href="https://breadai.co.kr" style="color:#D97706;text-decoration:none">breadai.co.kr</a>
    </p>
  </div>
</div>`;
}
