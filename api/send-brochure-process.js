// 소개서 발송 백그라운드 처리 — PDF + AI 맞춤 메시지 + 이메일 발송
export const config = {
  // AI 맞춤 문구(Opus, 웹 검색 포함)에 최대 90초를 주고, PDF 첨부와 메일 2건 발송까지 여유를 둔다
  maxDuration: 120,
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
          filename: 'BreadAI_상품소개서.pdf',
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
      personalizedSection = `B2B 영업에서 맞춤 제안이 효과가 좋다는 건 대부분 알고 계실 겁니다. 다만 한 곳을 제대로 준비하는 데 2~3시간씩 걸리다 보니, 실제로는 몇 곳만 맞춤으로 준비하고 나머지에는 같은 소개서를 보내게 되는 경우가 많습니다.<br><br>Bread&AI는 이 준비 과정을 AI로 대신합니다. 상품 소개서를 올리면 사업 확장, 신규 조직, 채용처럼 최근 영업 기회가 생긴 기업을 먼저 찾아드리고, 그 기업의 상황에 맞춰 <strong>왜 지금 만나야 하는지</strong>를 담은 제안 논리와 이메일, 제안서까지 만들어 드립니다. 기업 한 곳당 몇 분이면 맞춤 제안 준비가 끝납니다.`;
    }

    // ── 3) 방문자에게 소개서 메일 발송 ──
    const visitorRes = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Bread&AI <contact@breadai.co.kr>',
        reply_to: 'contact@breadai.co.kr',
        to: email,
        subject: `[Bread&AI] ${name}${positionText}, 요청하신 상품 소개서를 보내드립니다`,
        attachments,
        html: buildVisitorEmail({ company, deptText, name, positionText, personalizedSection }),
      }),
    });

    const visitorFailed = !visitorRes.ok;
    if (visitorFailed) {
      const err = await visitorRes.json().catch(() => ({}));
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
        from: 'Bread&AI <contact@breadai.co.kr>',
        to: 'contact@breadai.co.kr',
        subject: `${visitorFailed ? '[확인 필요: 고객 메일 발송 실패] ' : ''}[소개서 요청] ${company} ${name}`,
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

    // ── 5) Google Sheets 리드 기록 ──
    const SHEETS_WEBHOOK = process.env.GOOGLE_SHEETS_WEBHOOK;
    if (SHEETS_WEBHOOK) {
      try {
        await fetch(SHEETS_WEBHOOK, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            timestamp: now,
            company,
            name,
            department: department || '',
            position: position || '',
            email,
            phone: phone || '',
            isDummy: isDummyCompanyCheck(company),
            remarks: req.body.remarks || '',
          }),
        });
      } catch (sheetErr) {
        console.error('Google Sheets webhook failed:', sheetErr);
      }
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Send brochure process error:', error);
    return res.status(500).json({ error: '서버 오류가 발생했습니다.' });
  }
}


// ── 더미 회사명 체크 함수 ──
function isDummyCompanyCheck(company) {
  const dummyExact = ['개인', '없음', 'test', 'none', 'n/a', '-', '없어요', 'asdf', 'aaa', 'ㅇㅇ', 'ㅇㅇㅇ', 'ㄱㄱ'];
  const dummyContains = ['테스트', 'test', 'sample', '더미', 'dummy', '임시'];
  const companyLower = company.trim().toLowerCase();
  return dummyExact.some(d => companyLower === d) || dummyContains.some(d => companyLower.includes(d));
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

  const PRODUCT = `## Bread&AI 제품 정보 (이 안의 내용과 수치만 사용)
- 한 줄 소개: 세일즈 시그널로 지금 영업하기 좋은 고객사를 찾고, 기업별 맞춤 제안서까지 만드는 B2B 영업 AI
- 고객의 문제: 맞춤 제안이 효과적이라는 건 알지만 한 곳 준비에 2~3시간이 걸려, 소수에게만 맞춤 제안을 하고 나머지에는 같은 소개서를 보내게 됨. 또 어느 회사부터 영업해야 할지 정하기 어려움
- 1단계 세일즈 시그널 탐색: 상품 소개서를 올리면 AI가 우리 상품에 맞는 시그널(사업 확장, 신규 조직, 채용, 인력 증감, 신공장, 신제품 등)을 추천하고, 최근 시그널이 포착된 기업을 20곳 이상 찾아 우선순위대로 보여줌
- 2단계 심층 리서치: 기업 현황, 재무, 조직, 채용, 뉴스를 출처와 함께 정리하고, 그 회사가 왜 지금 우리 상품을 써야 하는지 제안 논리를 세움
- 3단계 맞춤 이메일과 제안서: 리서치한 논리로 첫 연락용 이메일과 콜 스크립트를 쓰고, 미팅에 가져갈 15~20장 제안서(PPT)를 약 5분 만에 만듦
- 쓸 수 있는 수치: 일반 콜드메일 회신율 2~3% 대비 상대 회사 맥락을 담은 맞춤 메일 회신율 8~9%, 맞춤 제안 1건 준비 시간 2~3시간에서 몇 분으로 단축
- 이 밖의 수치(미팅율, 매출 증가율, ROI 등)는 절대 만들지 마세요.`;

  const STYLE = `### 문체 규칙
- 대표가 직접 쓰는 메일입니다. 동료에게 설명하듯 담백하고 구체적인 한국어로 쓰세요.
- 과장 표현 금지: "혁신적인", "획기적인", "극대화", "폭발적" 같은 말을 쓰지 마세요.
- 줄표(—)와 가운데점(·)을 쓰지 마세요. 나열은 쉼표로 하세요.
- 마크다운 금지. HTML은 <br>(줄바꿈)과 <strong>(강조, 본문 전체에서 한 번만)만 사용.
- 인사말, 자기소개, 감사 인사, 첨부 안내, 무료 체험 안내, 서명은 쓰지 마세요. 메일 템플릿에 이미 들어 있습니다.
- 첫 글자부터 바로 본문을 시작하고, 순수 본문(HTML)만 출력하세요. JSON이나 코드블록으로 감싸지 마세요.`;

  let prompt;
  let useWebSearch = false;

  if (canIdentify) {
    useWebSearch = true;
    prompt = `당신은 Bread&AI 대표 이승욱입니다. 홈페이지에서 상품 소개서를 요청한 잠재 고객에게 보낼 메일의 핵심 본문 두 단락을 쓰세요.

## 최우선 규칙: 회사 정보는 웹 검색으로 확인된 사실만
- 반드시 web_search 도구로 "${company}"가 어떤 회사인지 먼저 확인하세요.
- 확인된 사실만 쓰세요. 업종이나 사업 내용을 추측해서 쓰는 것은 치명적입니다. 확신이 없으면 회사 이야기를 빼고 일반적인 B2B 영업 이야기로 쓰세요.
- "검색", "확인", "조사", "리서치 결과" 같은 말로 검색 과정을 드러내지 마세요. 회사를 못 찾았다는 사실도 언급하지 마세요.

${PRODUCT}

## 소개서 요청자 정보
- 회사명: ${company}
- 부서: ${department || '(미입력)'}
- 직함: ${position || '(미입력)'}
- 이메일 도메인: ${emailDomain}

## 본문 구성 (딱 두 단락, 단락 사이는 <br><br>)
1단락 (2~3문장): ${company}가 하는 일을 한 문장으로 짧게 짚고, 이 회사가 신규 고객사를 찾고 제안할 때 겪을 만한 어려움을 이야기하세요.${department ? ` ${department} 입장에서 겪을 어려움이면 더 좋습니다.` : ''} 회사 설명을 길게 늘어놓지 마세요.
2단락 (2~3문장): Bread&AI가 ${company}의 영업에 어떻게 쓰일 수 있는지 구체적인 장면으로 보여주세요. 예를 들어 이 회사 고객사에게 생길 만한 세일즈 시그널이 무엇인지 한두 개 예시를 들고, 그런 기업을 찾아 맞춤 제안까지 이어지는 흐름을 설명하세요. 기능을 나열하지 마세요.

${STYLE}`;

  } else {
    prompt = `당신은 Bread&AI 대표 이승욱입니다. 홈페이지에서 상품 소개서를 요청한 잠재 고객에게 보낼 메일의 핵심 본문 두 단락을 쓰세요.
요청자의 회사 정보는 알 수 없으니, B2B 신규 영업을 하는 일반적인 기업 담당자를 떠올리며 쓰세요.

${PRODUCT}

## 본문 구성 (딱 두 단락, 단락 사이는 <br><br>)
1단락 (2~3문장): 맞춤 제안이 효과적인 줄 알면서도 준비 시간 때문에 결국 같은 소개서를 돌리게 되는 현실, 어느 회사부터 영업해야 할지 막막한 상황에 공감하세요.
2단락 (2~3문장): Bread&AI가 세일즈 시그널로 지금 영업하기 좋은 기업을 찾고, 그 회사 상황에 맞춘 제안까지 만들어 주는 흐름을 구체적으로 설명하세요.

${STYLE}`;
  }

  const requestBody = {
    model: 'claude-opus-5-5',
    max_tokens: 2000,
    system: '당신은 이메일 본문 작성기입니다. 출력은 실제 고객에게 발송되는 이메일입니다. 절대로 사고 과정, 메타 설명, 검색 과정, "~로 확인되었으나", "~작성하겠습니다" 같은 문장을 출력하지 마세요. 첫 글자부터 곧바로 이메일 본문만 출력하세요.',
    messages: [{ role: 'user', content: prompt }],
  };

  if (useWebSearch) {
    requestBody.tools = [{
      type: 'web_search_20250305',
      name: 'web_search',
      max_uses: 2,
    }];
  }

  // 함수 실행 한도(120초) 안에 메일 발송까지 끝나도록, AI 생성은 90초를 넘기면 기본 문구로 대체한다.
  // 웹 검색(서버 도구)을 쓰면 응답이 stop_reason "pause_turn"으로 중간에 끊겨 올 수 있다.
  // 그때는 받은 내용을 assistant 턴으로 붙여 다시 요청해 이어서 쓰게 한다(최대 3회).
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 90000);
  const startedAt = Date.now();
  const allContent = [];
  let data;
  try {
    for (let turn = 0; turn < 3; turn++) {
      let response;
      try {
        response = await fetch('https://api.anthropic.com/v1/messages', {
          method: 'POST',
          signal: controller.signal,
          headers: {
            'x-api-key': apiKey,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });
      } catch (e) {
        console.error('Anthropic API timeout or network error:', e?.name || e, `${Date.now() - startedAt}ms`);
        return null;
      }

      if (!response.ok) {
        const err = await response.text();
        console.error('Anthropic API error:', response.status, err.slice(0, 500));
        return null;
      }

      data = await response.json();
      allContent.push(...(data.content || []));
      if (data.stop_reason !== 'pause_turn') break;
      requestBody.messages = [
        ...requestBody.messages.filter(m => m.role === 'user').slice(0, 1),
        { role: 'assistant', content: allContent },
      ];
    }
  } finally {
    clearTimeout(timer);
  }

  const textBlocks = allContent.filter(b => b.type === 'text');
  const rawText = textBlocks.map(b => b.text).join('').trim();
  const text = sanitizeAIOutput(rawText);

  const diag = {
    ms: Date.now() - startedAt,
    stop: data?.stop_reason,
    blocks: allContent.map(b => b.type).join(','),
    usage: data?.usage ? `${data.usage.input_tokens}/${data.usage.output_tokens}` : '',
    rawLen: rawText.length,
    finalLen: (text || '').length,
  };
  if (!text) {
    console.error('AI personalization empty, using default:', JSON.stringify(diag), rawText.slice(0, 300));
    return null;
  }
  console.log('AI personalization ok:', JSON.stringify(diag));
  return text;
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
  // 상품 소개서와 동일한 톤: 딥 틸(#0E5766) · 테라코타(#CC7247) · 아이보리 페이퍼(#FAF8F3)
  // 메일 클라이언트 호환을 위해 table 레이아웃 + 인라인 스타일만 사용한다.
  const F = "-apple-system,BlinkMacSystemFont,'Pretendard Variable',Pretendard,'Malgun Gothic','Apple SD Gothic Neo',sans-serif";

  // 숫자는 카드 안쪽에 크고 흐리게 깔아 장식처럼 쓰고, 옆에 제목·설명을 세운다.
  const step = (no, title, desc) => `
              <tr>
                <td style="padding:0 0 10px">
                  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#ffffff;border-radius:14px;border-collapse:separate">
                    <tr>
                      <td width="64" valign="middle" align="center" style="padding:16px 0 16px 6px">
                        <div style="font:800 40px/1 ${F};color:#EDE0D5;letter-spacing:-0.05em">${no}</div>
                      </td>
                      <td valign="middle" style="padding:16px 18px 16px 4px">
                        <div style="font:800 15px/1.45 ${F};color:#0E5766;letter-spacing:-0.025em">${title}</div>
                        <div style="font:400 13.5px/1.65 ${F};color:#5A554B;margin-top:4px">${desc}</div>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>`;

  return `
<div style="background:#F3EFE6;padding:28px 12px;font-family:${F};-webkit-text-size-adjust:100%">
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:600px;margin:0 auto;background:#FAF8F3;border-radius:18px;overflow:hidden;border-collapse:separate">

    <!-- 헤더 : 소개서 표지와 같은 다크 잉크 -->
    <tr>
      <td style="background:#1A1714;padding:26px 32px">
        <table cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="vertical-align:middle;padding-right:9px">
              <img src="https://breadai.co.kr/logo_email.png" alt="" width="26" style="height:26px;width:auto;display:block;border:0" />
            </td>
            <td style="vertical-align:middle">
              <span style="font:800 17px/1 ${F};color:#ffffff;letter-spacing:-0.02em">Bread&amp;AI</span>
            </td>
          </tr>
        </table>
        <div style="font:700 13px/1.5 ${F};color:#7FB4BF;margin-top:16px;letter-spacing:-0.01em">AI Sales Intelligence</div>
        <div style="font:800 21px/1.4 ${F};color:#ffffff;margin-top:5px;letter-spacing:-0.03em">요청하신 상품 소개서를 보내드립니다</div>
      </td>
    </tr>

    <!-- 본문 -->
    <tr>
      <td style="padding:32px 32px 8px">
        <div style="font:700 16.5px/1.6 ${F};color:#1A1714;letter-spacing:-0.02em;margin-bottom:14px">
          안녕하세요, ${company} ${deptText}${name}${positionText}.
        </div>
        <div style="font:400 15px/1.85 ${F};color:#3F3A33;margin-bottom:22px">
          Bread&amp;AI 대표 이승욱입니다.<br>
          상품 소개서를 요청해 주셔서 감사합니다.
        </div>
        <div style="font:400 15px/1.9 ${F};color:#3F3A33">
          ${personalizedSection}
        </div>
      </td>
    </tr>

    <!-- 첨부 안내 -->
    <tr>
      <td style="padding:24px 32px 0">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#E4EEF0;border-radius:12px;border-collapse:separate">
          <tr>
            <td style="padding:15px 18px">
              <div style="font:700 13.5px/1.5 ${F};color:#0A414D;letter-spacing:-0.01em">📎 상품 소개서가 이 메일에 첨부되어 있습니다</div>
              <div style="font:400 12.5px/1.6 ${F};color:#0E5766;margin-top:3px">BreadAI_상품소개서.pdf</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- 3단계 -->
    <tr>
      <td style="padding:26px 32px 0">
        <table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#EAE4D7;border-radius:14px;border-collapse:separate">
          <tr>
            <td style="padding:20px 16px 10px">
              <div style="font:800 14.5px/1.5 ${F};color:#1A1714;letter-spacing:-0.02em;padding:0 0 14px 4px">
                Bread&amp;AI로 영업 준비가 이렇게 바뀝니다
              </div>
              <table cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:separate">
${step('1', '세일즈 시그널로 영업 대상 찾기', '사업 확장, 신규 조직, 채용처럼 최근 영업 기회가 생긴 기업을 찾아 우선순위대로 보여드립니다')}
${step('2', '심층 리서치와 제안 논리', '기업 현황, 재무, 채용, 뉴스를 출처와 함께 정리하고 왜 지금 우리 상품이 필요한지 논리를 세웁니다')}
${step('3', '맞춤 이메일과 제안서', '첫 연락용 이메일과 콜 스크립트, 미팅에 가져갈 15~20장 제안서를 약 5분 만에 만듭니다')}
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- CTA -->
    <tr>
      <td style="padding:28px 32px 0">
        <div style="font:400 15px/1.85 ${F};color:#3F3A33;margin-bottom:20px">
          자세한 내용은 첨부한 소개서에 담았습니다.<br>
          1주일 동안 무료로 써보실 수 있으니 부담 없이 먼저 사용해 보시고,<br>
          궁금한 점은 이 메일로 편하게 회신해 주세요.
        </div>
        <table cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td style="background:#CC7247;border-radius:11px">
              <a href="https://app.breadai.co.kr" style="display:inline-block;padding:14px 32px;font:700 15px/1 ${F};color:#ffffff;text-decoration:none;letter-spacing:-0.02em">1주일 무료 체험하기 →</a>
            </td>
          </tr>
        </table>
        <div style="font:600 12px/1.6 ${F};color:#8B857A;margin-top:10px">결제 정보 없이 바로 시작할 수 있습니다</div>
      </td>
    </tr>

    <!-- 서명 -->
    <tr>
      <td style="padding:28px 32px 30px">
        <div style="border-top:1px solid #E7E1D4;padding-top:20px">
          <div style="font:700 13.5px/1.5 ${F};color:#1A1714">이승욱 대표</div>
          <div style="font:400 12.5px/1.75 ${F};color:#8B857A;margin-top:3px">
            Bread&amp;AI | AI Sales Intelligence<br>
            <a href="mailto:contact@breadai.co.kr" style="color:#0E5766;text-decoration:none;font-weight:600">contact@breadai.co.kr</a>
            &nbsp;|&nbsp;
            <a href="https://breadai.co.kr" style="color:#0E5766;text-decoration:none;font-weight:600">breadai.co.kr</a>
          </div>
        </div>
      </td>
    </tr>
  </table>
</div>`;
}
