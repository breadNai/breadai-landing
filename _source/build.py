# -*- coding: utf-8 -*-
"""
Bread&AI 홈페이지 빌드 스크립트
  python3 build.py           →  index.html (A안) + index-v2.html (B안) 생성

A안 / B안 차이는 이 파일 안에서만 관리한다.
직접 index.html 을 수정하지 말 것 — 다음 빌드에서 덮어써진다.
"""
import io, os
from parts_css import CSS

OUT = os.path.dirname(os.path.abspath(__file__))

# ── 아이콘 ────────────────────────────────────────────────────────────
def ic(path, w=2.2):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (w, path))

I_ARROW = ic('<path d="M5 12h13M12 5l7 7-7 7"/>', 2.4)
I_TARGET = ic('<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.2"/><path d="M12 1v3M12 20v3M1 12h3M20 12h3"/>')
I_MAIL = ic('<rect x="3" y="5" width="18" height="14" rx="2.4"/><path d="M3.5 7l8.5 6 8.5-6"/>')
I_DECK = ic('<rect x="3" y="4" width="18" height="12.5" rx="2"/><path d="M12 16.5v3.5M8.5 20h7M7 8.5h6M7 12h4"/>')
I_PLAY = ic('<circle cx="12" cy="12" r="9.4"/><path d="M10 8.6l6 3.4-6 3.4z" fill="currentColor" stroke-width="1"/>', 1.8)
BRANDMARK = ('<svg viewBox="0 0 24 24" fill="none"><path d="M3 12h13M11 6l6 6-6 6" stroke="%s" '
             'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
             '<circle cx="20.5" cy="12" r="1.8" fill="%s"/></svg>')

# ── 고객사 로고 ───────────────────────────────────────────────────────
# (파일, alt, 표시높이px, 표시명, 수치, 캡션)  ※ 수치·캡션은 B안 인터뷰 패널용 임시값
# 표시 높이는 로고 원본 비율(모두 120px 높이 기준)로 '면적'을 맞춘 값.
# 단순히 높이를 통일하면 가로로 긴 워드마크가 훨씬 커 보인다.
LOGOS = [
    ("logo-skrent.png",    "SK렌터카", 44, "SK렌터카", "18장",   "기업별 맞춤 제안서", ""),
    ("logo-remember.png",  "리멤버",   21, "리멤버",   "3.2배",  "콜드메일 회신율", "interview-remember.jpg"),
    ("logo-cashwalk.png",  "캐시워크", 25, "캐시워크", "2배",    "주간 제안 발송량", ""),
    ("logo-momsitter.png", "맘시터",   27, "맘시터",   "40시간", "월 절감 시간", ""),
    ("logo-miridih.png",   "미리디",   23, "미리디",   "3배",    "미팅 전환율", ""),
    ("logo-eleven.png",    "열한시",   28, "열한시",   "2.4배",  "첫 회신까지 속도", ""),
]

# ── 고객사 사용 현황 띠 ───────────────────────────────────────────────
# SK렌터카 운영 모니터링(2026-05-01~08-31) + 맘시터 사용 통계 합산.
#   탐색 실행   1,150 + 90  = 1,240
#   심층 리서치 5,895 + 375 = 6,270
#   맞춤 제안서 4,723 + 131 = 4,854
# ⚠️ '발굴 타겟 기업 23,684' 은 SK렌터카 단독 수치. 맘시터 값이 없어 합산되지 않았다.
#    맘시터 발굴 회사 수를 받으면 합산하고, 그때까지는 각주가 필요하다.
BAND_UPDATED = "2026.08 기준"
BAND = [("신규 발굴한 타겟 기업", 23684), ("기업 심층 리서치 수행", 6270),
        ("맞춤 제안서 생성", 4854)]

# ── WHY 카드 그래픽 ───────────────────────────────────────────────────
# 각 도형은 카드가 활성화(.wc.cur)될 때 CSS 키프레임으로 움직인다.
GFX = {}
# 0) 일반 메일은 가라앉고, 맞춤(custom) 제안 메일은 올라가 계속 떠 있는다
_ENV = ('<svg class="ev" viewBox="0 0 128 92" fill="none">'
        '<rect x="3.5" y="3.5" width="121" height="85" rx="12" fill="%s" stroke="%s" stroke-width="3"/>'
        '<path d="M10 15l54 39 54-39" stroke="%s" stroke-width="3" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
GFX[0] = ('<div class="gx gx0">'
          '<div class="env a">'
          + _ENV % ('rgba(255,255,255,.07)', 'rgba(255,255,255,.40)', 'rgba(255,255,255,.40)')
          + '</div>'
          '<div class="env b"><span class="bdg">custom</span>'
          + _ENV % ('rgba(255,255,255,.22)', '#fff', '#fff')
          + '</div></div>')
# 1) 시계 — 분침이 돈다
GFX[1] = ('<div class="gx gx1"><svg viewBox="0 0 200 200" fill="none">'
          '<circle cx="100" cy="100" r="74" stroke="rgba(255,255,255,.3)" stroke-width="2"/>'
          '<circle cx="100" cy="100" r="54" stroke="rgba(255,255,255,.16)" stroke-width="2"/>'
          '<g class="hnd h"><path d="M100 100V56" stroke="rgba(255,255,255,.9)" stroke-width="5" '
          'stroke-linecap="round"/></g>'
          '<g class="hnd m"><path d="M100 100V38" stroke="#fff" stroke-width="3.4" stroke-linecap="round"/></g>'
          '<circle cx="100" cy="100" r="5.5" fill="#fff"/></svg></div>')
# 2) 깔때기 — 공이 하나씩 통과
GFX[2] = ('<div class="gx gx2"><svg viewBox="0 0 200 200" fill="none" '
          'stroke="rgba(255,255,255,.85)" stroke-width="2.6" stroke-linejoin="round">'
          '<path d="M30 52h140L120 116v42l-40 22v-64z"/></svg>'
          '<span class="bl q1"></span><span class="bl q2"></span><span class="bl q3"></span>'
          '<span class="bl q4"></span><span class="bl q5"></span><span class="bl q6"></span>'
          '<span class="bl q7"></span>'
          '<span class="pass p1"></span><span class="pass p2"></span></div>')
# 3) 같은 소개서가 계속 쌓인다
GFX[3] = ('<div class="gx gx3">'
          '<div class="pg p1"><em>Proposal</em></div><div class="pg p2"><em>Proposal</em></div>'
          '<div class="pg p3"><em>Proposal</em></div>'
          '<div class="pg p4"><em>Proposal</em></div></div>')
# 4) 하나의 제안이 여러 기업으로 뻗어나간다
GFX[4] = ('<div class="gx gx4"><svg viewBox="0 0 200 200" fill="none">'
          '<rect x="10" y="78" width="46" height="46" rx="8" fill="rgba(255,255,255,.16)" '
          'stroke="rgba(255,255,255,.9)" stroke-width="2"/>'
          '<path d="M22 94h22M22 106h14" stroke="rgba(255,255,255,.9)" stroke-width="2.4" stroke-linecap="round"/>'
          '<path class="ray r1" d="M60 101H92c14 0 14-48 28-48h8" stroke="rgba(255,255,255,.55)" '
          'stroke-width="2.4" stroke-linecap="round"/>'
          '<path class="ray r2" d="M60 101h68" stroke="rgba(255,255,255,.55)" stroke-width="2.4" '
          'stroke-linecap="round"/>'
          '<path class="ray r3" d="M60 101H92c14 0 14 48 28 48h8" stroke="rgba(255,255,255,.55)" '
          'stroke-width="2.4" stroke-linecap="round"/>'
          '<g class="tgt t1"><rect x="130" y="34" width="52" height="38" rx="7" fill="rgba(255,255,255,.18)"/>'
          '<path d="M143 53l7 7 13-14" stroke="#fff" stroke-width="3.2" stroke-linecap="round" '
          'stroke-linejoin="round"/></g>'
          '<g class="tgt t2"><rect x="130" y="82" width="52" height="38" rx="7" fill="rgba(255,255,255,.18)"/>'
          '<path d="M143 101l7 7 13-14" stroke="#fff" stroke-width="3.2" stroke-linecap="round" '
          'stroke-linejoin="round"/></g>'
          '<g class="tgt t3"><rect x="130" y="130" width="52" height="38" rx="7" fill="rgba(255,255,255,.18)"/>'
          '<path d="M143 149l7 7 13-14" stroke="#fff" stroke-width="3.2" stroke-linecap="round" '
          'stroke-linejoin="round"/></g></svg></div>')

# WHY 카드 — 문구는 넛지헬스케어 온보딩 자료(2026-08-21) 01섹션 원문 그대로
# (태그, 헤드라인, PC 본문, 모바일 본문, 그래픽 배경, GFX 번호)
# 모바일은 카드 폭이 좁아 PC 본문이 어색하게 잘리므로 줄바꿈까지 지정한 축약 문구를 따로 쓴다.
WHY_CARDS = [
    ("검증된 사실",
     "아웃바운드 영업에서 맞춤 제안의<br><span class=\"qm\">회신율은 3배</span>나 높습니다",
     "자사 홍보 위주의 일반적인 콜드메일 회신율이 <b>2~3%</b>인데 비해,<br>"
     "상대 회사 맥락을 담은 맞춤 제안 메일은 회신율 <b>8~9%</b>까지 증가합니다",
     "일반적인 콜드메일 회신율 <b>2~3%</b><br>vs<br>"
     "상대 회사 맥락 담은 맞춤 메일 회신율 <b>8~9%</b>", "g0", 0),
    ("영업 현장의 한계 1",
     "<i class=\"qo\">“</i>하지만, 맞춤 제안 1건에<br>최소 <span class=\"qm\">2~3시간</span> 걸려요<i class=\"qc\">”</i>",
     "타겟 기업 리서치, 뉴스 분석, Pain Point 파악, 제안 논리 구성…<br>"
     "1건 준비하는 데만 너무 많은 시간이 듭니다.",
     "타겟 기업 리서치, 뉴스 분석,<br>Pain Point 파악, 제안 논리 구성…<br>"
     "1건 준비하는 데만 너무 많은 시간 소요", "g1", 1),
    ("영업 현장의 한계 2",
     "<i class=\"qo\">“</i>확률 높은 곳에만<br><span class=\"qm\">준비할 수밖에</span> 없어요<i class=\"qc\">”</i>",
     "물리적으로 하루 최대 2건이 한계다 보니,<br>"
     "단가 높고 확률 높은 고가치 고객만 선별해서 준비하게 됩니다.",
     "물리적으로 하루 최대 2건이 한계다 보니<br>"
     "단가 높고 확률 높은 일부 고객에만 맞춤 제안", "g2", 2),
    ("영업 현장의 한계 3",
     "<i class=\"qo\">“</i>결국 매번<br><span class=\"qm\">같은 논리</span>로 제안하죠<i class=\"qc\">”</i>",
     "맞춤 준비를 한 소수의 기업 외에는,<br>"
     "결국 같은 소개서를 복사·붙여넣기 해서 제안할 수밖에 없습니다.",
     "맞춤 준비를 한 소수의 기업 외에는<br>"
     "결국 같은 소개서를 복붙해서 제안할 수 밖에 없음", "g3", 3),
]

# ── 프로세스 섹션 ─────────────────────────────────────────────────────
# 스크린샷 없음. 시나리오별 가치를 개념 애니메이션으로.
# 핀 스크롤을 걷어내고 뷰포트에 들어오면 자동으로 단계가 넘어간다.

# AI가 훑어온 순서(정렬 전) → 점수가 매겨지고 → Fit Score 순으로 재정렬된다.
# (이름, 근거, 점수, 정렬 후 최종 순위)
# ── 회사 소개서 표지 (샘플) — 16:9 PPT 비율, 틸블루 톤 ────────────────
COVER = ('<div class="cov">'
         '<span class="cbg"></span><span class="cdiag"></span>'
         '<span class="cmark">2026</span>'
         '<span class="cbadge">OUR</span>'
         '<b class="ctit">PROPOSAL</b>'
         '<span class="csub">COMPANY INTRODUCTION</span>'
         '<span class="cdots"><i></i><i></i><i></i></span>'
         '</div>')

# ── 프로세스에 등장하는 기업은 전부 가상입니다 ─────────────────────────
# (이름, 이니셜, 태그, 근거, 연락처, 점수)  ※ 점수 내림차순이 최종 정렬 결과
_SROWS = [("플랜존클라우드", "P", "중견 · 클라우드 MSP", "AI 인프라 전담 조직 신설", "sales@planzone.***", 97),
          ("LN전자", "L", "대기업 · 전자", "신사업 조직 신설", "02-6363-****", 96),
          ("SL모빌리티", "S", "대기업 · 모빌리티", "B2B 채널 강화", "02-2008-****", 93),
          ("빌더스엔터테인먼트", "B", "중견 · 콘텐츠", "글로벌 진출 가속", "biz@buildus.***", 91),
          ("코어테크놀로지", "C", "중견 · SI", "공공 부문 확대", "1544-****", 89),
          ("한빛소프트웨어", "H", "중견 · ERP", "AI 제품 출시", "partner@hanbit.***", 87),
          ("대원인더스트리", "D", "중견 · 제조", "스마트팩토리 전환", "02-777-****", 85),
          ("유니콘페이먼츠", "U", "스타트업 · 핀테크", "시리즈C 유치", "hello@unicornpay.***", 83),
          ("세종바이오랩", "S", "중견 · 바이오", "생산 라인 증설", "02-451-****", 81),
          ("아이엠로지스", "I", "중견 · 물류", "풀필먼트 확대", "sales@iamlogis.***", 79),
          ("그린에너지솔루션", "G", "중견 · 에너지", "ESS 사업 진출", "02-889-****", 77),
          ("퍼스트커머스", "F", "중견 · 커머스", "B2B 채널 신설", "biz@firstcm.***", 75)]


def _card(nm, ini, tg, rs, ct, sc, cls=""):
    """기업 카드 — 장면 1-2의 수렴 카드와 1-3의 리스트 행이 같은 모양을 쓴다."""
    return ('<div class="ecard%s"><span class="eini">%s</span>'
            '<span class="enm">%s<em>%s</em><small>%s</small></span>'
            '<span class="ectc">%s</span>'
            '<b class="esc">%d</b>'
            '<span class="ego">리서치 시작 ›</span></div>'
            % (cls, ini, nm, tg, rs, ct, sc))


def _score_rows():
    return "".join(_card(nm, ini, tg, rs, ct, sc, " r%d" % i + (" hi" if i == 0 else ""))
                   for i, (nm, ini, tg, rs, ct, sc) in enumerate(_SROWS))


# ── 기업을 둘러싼 공개 데이터 창 (2-1에서 회사 옆에 뜬다) ──────────────
_WINS = [("보도자료", "전국 48개 사업장 통합 안전보건 체계 구축", "2026.07 · 3건"),
         ("지속가능경영보고서", "임직원 케어 프로그램 확대 명시", "p.42"),
         ("채용공고", "인사총무본부 HR운영 담당", "진행 중 2건"),
         ("조직 개편", "인사총무본부 신설 · 복리후생 예산 +18%", "2026.06")]

def _lwins():
    return "".join('<div class="lwin lw%d"><span class="lk">%s</span>'
                   '<span class="lv">%s</span><span class="lm">%s</span></div>'
                   % (i + 1, k, v, m) for i, (k, v, m) in enumerate(_WINS))


# 제안 논리 3문장 — 이 문장이 다음 컷의 이메일 본문으로 그대로 이어진다
LOGIC = ["귀사는 전국 48개 사업장에 인력이 분산되어 있습니다",
         "지사별로 케어 수준이 달라지면 제도 자체가 흔들립니다",
         "저희는 전사 커버리지를 인당 월 정액으로 운영합니다"]

# 대한민국 지도 (단순화한 실루엣) — 제안서 장표에 그려진다
KMAP = ('<img class="kmap" src="assets/img/deck-map.jpg" alt="" '
        'loading="lazy" decoding="async">')


# ── 제안서 장표 썸네일 ────────────────────────────────────────────────
# assets/img/deck/p01~p19.jpg — 실제 생성된 제안서 장표(브랜딩 제거본)
DECK_N = 19


def _pages():
    return "".join('<span class="pgz p%d">'
                   '<img src="assets/img/deck/p%02d.jpg" alt="" loading="lazy" decoding="async">'
                   '</span>' % (k, k + 1) for k in range(DECK_N))


SCENE_1 = [
    # 1) 소개서 분석 — 표지에서 실선이 뻗어 분석 카드로 연결된다
    ('<div class="sc up"><div class="stg3">'
     '<svg class="wires" viewBox="0 0 100 100" preserveAspectRatio="none">'
     '<path class="wr w1" pathLength="1" d="M38 42 L28 24"/>'
     '<path class="wr w2" pathLength="1" d="M62 41 L74 27"/>'
     '<path class="wr w3" pathLength="1" d="M38 58 L28 74"/>'
     '<path class="wr w4" pathLength="1" d="M62 59 L74 77"/></svg>'
     '<div class="docw">' + COVER + '<div class="scan"></div></div>'
     '<div class="chip c1"><span class="ck">핵심 강점</span>'
     '<span class="cv">전사 커버리지 · 월 정액 운영</span></div>'
     '<div class="chip c2"><span class="ck">타겟 업종</span>'
     '<span class="cv">제조 · 유통 · 금융</span></div>'
     '<div class="chip c3"><span class="ck">가격 구조</span>'
     '<span class="cv">인당 월 정액 / 연 단위 계약</span></div>'
     '<div class="chip c4"><span class="ck">레퍼런스</span>'
     '<span class="cv">대기업 12개사</span></div>'
     '</div><div class="sub">색상·폰트·페이지 구조까지 읽어 '
     '<b>우리가 무엇을 파는지</b> 이해합니다</div></div>'),
    # 2) 기업 선별 — 실제 서비스 화면을 훑어 기업 카드 한 장으로 모인다
    ('<div class="sc flt"><div class="stg3">'
     '<div class="win wv"><div class="vth"><span class="vplay"></span>'
     '<span class="vdur">12:04</span></div>'
     '<div class="vmeta"><span class="vav">P</span>'
     '<span class="vtx"><b>플랜존클라우드 2026 사업 전략 발표</b>'
     '<u>플랜존클라우드 공식 · 조회수 3.2만회 · 2주 전</u></span></div></div>'
     '<div class="win wn"><div class="nhd"><span class="nlogo">뉴스</span>'
     '<span class="ncat">IT · 산업</span><span class="ndate">2026.08.14</span></div>'
     '<div class="nbody"><b class="nti">플랜존클라우드, AI 인프라 전담 조직 신설</b>'
     '<span class="nld">클라우드 MSP 기업 플랜존클라우드가 AI 인프라 사업을 전담하는 '
     '조직을 신설하고 관련 투자를 확대한다고 14일 밝혔다.</span>'
     '<span class="nfoot">관련 보도 3건</span></div></div>'
     '<div class="win wj"><div class="jhd"><span class="jlogo">P</span>'
     '<span class="jco">플랜존클라우드</span><span class="jnew">D-14</span></div>'
     '<div class="jbody"><b class="jti">클라우드 아키텍트 (경력 5년 이상)</b>'
     '<span class="jtags"><i>경력 5~10년</i><i>정규직</i><i>서울 강남</i></span>'
     '<span class="jfoot">진행 중인 공고 17건</span></div></div>'
     '<div class="onecard">'
     + _card(*_SROWS[0], cls=" hi") +
     '</div></div>'
     '<div class="sub">사업 현황, 최근 뉴스, 채용 공고 등을 검색하여<br>'
     '<b>적합한 기업들을 리스팅</b>합니다</div></div>'),
    # 3) 우선순위 — 카드가 위에서 아래로 흐르다 멈추고 Fit Score 순으로 정렬
    ('<div class="sc scr"><div class="swin"><div class="srail">' + _score_rows() + '</div></div>'
     '<div class="sub">Fit Score와 <b>공개 연락처</b>까지 '
     '<b>20~30개 기업</b>이 함께 나옵니다</div></div>'),
    # 4) 심층 리서치 — 실시간 모니터링 대시보드
    ('<div class="sc res"><div class="dash">'
     '<div class="dtop"><span class="fi">P</span>'
     '<span class="dnm"><b>플랜존클라우드</b>'
     '<small>클라우드 MSP · 코스닥 상장 · planzone.co.kr</small></span>'
     '<span class="live"><i></i>실시간 수집</span></div>'
     '<div class="dtab"><span class="on">기업 개요</span><span>재무</span>'
     '<span>조직 · 채용</span><span>뉴스</span><span>영업 인사이트</span></div>'
     '<div class="kpis">'
     '<div class="kpi"><span class="kk">연매출</span>'
     '<span class="krow"><b><span class="cnt" data-c="1854">0</span><u>억원</u></b>'
     '<svg class="spk" viewBox="0 0 60 20" preserveAspectRatio="none">'
     '<path pathLength="1" d="M0 17L15 14L30 11L45 7L60 2"/></svg></span>'
     '<span class="kd up">▲ 28.4%<em>NICE평가정보</em></span></div>'
     '<div class="kpi"><span class="kk">영업이익</span>'
     '<span class="krow"><b><span class="cnt" data-c="212">0</span><u>억원</u></b>'
     '<svg class="spk" viewBox="0 0 60 20" preserveAspectRatio="none">'
     '<path pathLength="1" d="M0 16L15 17L30 12L45 8L60 3"/></svg></span>'
     '<span class="kd up">▲ 47.2%<em>전자공시</em></span></div>'
     '<div class="kpi"><span class="kk">임직원수</span>'
     '<span class="krow"><b><span class="cnt" data-c="1240">0</span><u>명</u></b>'
     '<svg class="spk" viewBox="0 0 60 20" preserveAspectRatio="none">'
     '<path pathLength="1" d="M0 15L15 13L30 12L45 8L60 4"/></svg></span>'
     '<span class="kd up">▲ 112명<em>국민연금</em></span></div>'
     '<div class="kpi"><span class="kk">채용 공고</span>'
     '<span class="krow"><b><span class="cnt" data-c="17">0</span><u>건</u></b>'
     '<svg class="spk" viewBox="0 0 60 20" preserveAspectRatio="none">'
     '<path pathLength="1" d="M0 14L15 15L30 9L45 10L60 3"/></svg></span>'
     '<span class="kd">진행 중<em>사람인·잡코리아</em></span></div>'
     '</div>'
     '<div class="dgrid">'
     '<div class="pnl chart"><span class="pnt">매출 · 영업이익 추이<em>단위 억원</em></span>'
     '<span class="bars">'
     '<i><u class="b1" style="--h:60%"></u><u class="b2" style="--h:14%"></u><s>2022</s></i>'
     '<i><u class="b1" style="--h:68%"></u><u class="b2" style="--h:19%"></u><s>2023</s></i>'
     '<i><u class="b1" style="--h:74%"></u><u class="b2" style="--h:26%"></u><s>2024</s></i>'
     '<i><u class="b1" style="--h:84%"></u><u class="b2" style="--h:38%"></u><s>2025</s></i>'
     '<i><u class="b1" style="--h:100%"></u><u class="b2" style="--h:52%"></u><s>2026E</s></i>'
     '</span>'
     '<span class="lgd"><em class="e1">매출</em><em class="e2">영업이익</em></span></div>'
     '<div class="pnl insight"><span class="pnt hi">영업 논리</span>'
     '<span class="iv l1">인력은 3개월 연속 늘리는데 제안 준비 인력은 그대로</span>'
     '<span class="iv l2">신설 조직은 첫해 레퍼런스 확보가 급한 상황</span>'
     '<span class="iv l3 hit">→ 준비 시간을 줄여 제안 건수를 늘리는 우리 제품이 정확히 맞는 시점</span></div>'
     '</div></div>'
     '<div class="sub">매출·이익·조직 규모와 Pain Point를 <b>근거 출처와 함께</b> 정리합니다</div></div>'),
]

SCENE_2 = [
    # 1) 제안 논리 — 회사 옆에 공개 데이터 창이 뜨고, 논리 3문장이 정리된다
    ('<div class="sc lgc"><div class="stg3">'
     '<div class="bldg"><svg viewBox="0 0 120 130" fill="none">'
     '<rect x="14" y="34" width="40" height="90" rx="3"/>'
     '<rect x="60" y="12" width="46" height="112" rx="3"/>'
     '<path class="wdw" d="M22 46h10M40 46h6M22 60h10M40 60h6M22 74h10M40 74h6'
     'M22 88h10M40 88h6M22 102h10M40 102h6"/>'
     '<path class="wdw" d="M68 26h12M88 26h10M68 42h12M88 42h10M68 58h12M88 58h10'
     'M68 74h12M88 74h10M68 90h12M88 90h10M68 106h12M88 106h10"/>'
     '<rect x="0" y="124" width="120" height="4" rx="2" class="grd"/></svg>'
     '<b>대형 제조 A사</b><u>임직원 4,800명<br>48개 사업장</u></div>'
     + _lwins() +
     '<div class="lout"><span class="lt">제안 논리</span>'
     + "".join('<span class="ln l%d">%s</span>' % (k + 1, t) for k, t in enumerate(LOGIC)) +
     '</div></div>'
     '<div class="sub">상대 회사의 이슈와 우리 강점을 연결해 <b>제안 논리</b>를 세웁니다</div></div>'),
    # 2) 이메일 생성 — 앞에서 만든 제안 논리가 그대로 본문에 붙는다
    ('<div class="sc mal"><div class="mwin">'
     '<div class="mlang"><span class="on">한국어</span><span>English</span></div>'
     '<div class="mh"><span class="mf">받는사람</span>'
     '<span class="mv">인사총무본부 담당 임원</span></div>'
     '<div class="mh"><span class="mf">제목</span>'
     '<span class="mv ty t1">전국 48개 사업장 임직원 케어 관련</span></div>'
     '<div class="mb">'
     '<span class="bl b0">담당자님, 안녕하세요. BR케어의 김지수입니다.</span>'
     + "".join('<span class="bl mv%d moved">%s.</span>' % (k + 1, t) for k, t in enumerate(LOGIC)) +
     '<span class="bl b4">유사 규모 제조사 3곳의 운영 사례를 15분만 공유드려도 될까요?</span>'
     '</div></div>'
     '<div class="sub">한글과 영문으로 <b>맞춤 콜드메일</b>이 자동 생성됩니다</div></div>'),
    # 3) 전송 — 버튼 한 번에 주소와 본문이 통째로 아웃룩으로 옮겨간다
    ('<div class="sc snd"><div class="stg3">'
     '<div class="mini"><span class="mkt">이메일 초안</span>'
     '<div class="emr"><span class="emk">받는사람</span>'
     '<span class="emv">인사총무본부 담당 임원</span></div>'
     '<div class="emr"><span class="emk">제목</span>'
     '<span class="emv st">전국 48개 사업장 임직원 케어 관련</span></div>'
     '<div class="mbody">'
     '<span class="mbl">담당자님, 안녕하세요. BR케어의 김지수입니다.</span>'
     + "".join('<span class="mbl hl">%s.</span>' % t for t in LOGIC) +
     '</div>'
     '<span class="obtn">아웃룩으로 보내기</span></div>'
     '<div class="flyA"></div><div class="flyB"></div>'
     '<div class="olk">'
     '<div class="obar"><span class="odot r"></span><span class="odot y"></span>'
     '<span class="odot g"></span><span class="ologo">O</span><b>Outlook</b></div>'
     '<div class="obody"><div class="oside">'
     '<span class="oi">받은 편지함</span><span class="oi">보낸 편지함</span>'
     '<span class="oi on">임시 보관함</span></div>'
     '<div class="omain">'
     '<div class="ofld"><span class="ok">받는 사람</span>'
     '<span class="ov land">jh.kim@ln-elec.co.kr</span></div>'
     '<div class="ofld"><span class="ok">제목</span>'
     '<span class="ov land2">전국 48개 사업장 임직원 케어 관련</span></div>'
     '<span class="obd land3">담당자님, 안녕하세요. 귀사는 전국 48개 사업장에 '
     '인력이 분산되어 있습니다…</span>'
     '<span class="osend">보내기</span></div></div></div>'
     '</div>'
     '<div class="sub">버튼 한 번으로 <b>주소와 제목이 그대로</b> 아웃룩에 채워집니다</div></div>'),
    # 4) 제안서 — 한 장이 조립된 뒤 뒤로 물러나며 전체 장표가 나열된다
    ('<div class="sc dck"><div class="stg3">'
     '<div class="build">'
     '<span class="btag">서비스 커버리지</span>'
     '<span class="bt">전국 최대 규모의 전문 네트워크로<br>안정적인 서비스를 제공합니다</span>'
     '<span class="bbody">전국 949개 서비스 네트워크 · 160개 지점으로<br>'
     '어디서나 동일한 품질로 운영합니다.</span>'
     '<span class="btbl"><i class="th"><u>구분</u><u>네트워크</u><u>지점</u></i>'
     '<i><u>수도권</u><u>365</u><u>83</u></i><i><u>충청</u><u>127</u><u>22</u></i>'
     '<i><u>영남</u><u>293</u><u>23</u></i><i class="sum"><u>합계</u><u>949</u><u>160</u></i></span>'
     '<span class="bmap">' + KMAP + '</span>'
     '</div>'
     '<div class="pages">' + _pages() + '</div>'
     '</div>'
     '<div class="sub"><b>15~20장</b>의 영업 초도 제안서가 <b>5분 내</b>에 생성됩니다</div></div>'),
]

# 단계 문구의 <em>…</em> 는 단계가 활성화될 때 형광펜이 칠해지는 구간이다.
# (트랙1은 주황 terra, 트랙2는 틸 블루 — CSS 에서 트랙별로 색을 준다)
TRACKS = [
    ("타겟 기업을 새로 찾을 때", [
        ("AI가 <em>소개서</em>를 분석하고", "색상·폰트·페이지 구조까지 읽어 우리가 무엇을 파는지 이해합니다"),
        ("<em>지금 영업할 기회</em>가 있는 기업을 골라서",
         "사업 현황, 최근 뉴스, 채용 공고 등을 검색하여<br>적합한 기업들을 리스팅합니다"),
        ("영업할 우선순위를 <em>한눈에 보고</em>", "왜 이 기업인지 근거와 공개 연락처까지 함께 나옵니다"),
        ("선택한 기업을 <em>심층 리서치</em>합니다", "매출·이익·조직 규모와 Pain Point를 근거 출처와 함께 정리합니다"),
    ]),
    ("타겟 기업이 이미 정해져 있을 때", [
        ("<em>왜 우리를 선택해야 하는지</em> 논리를 만들고", "상대 회사의 이슈와 우리 강점을 연결해 제안 논리를 세웁니다"),
        ("그 회사만을 위한 <em>이메일</em>이 작성되고", "상대 회사 맥락에서 시작하는 첫 문단이 그대로 완성됩니다"),
        ("원클릭으로 바로 <em>아웃룩에</em> 보낼 수 있고", "제목과 본문이 아웃룩으로 그대로 넘어갑니다"),
        ("<em>제안서</em>까지 AI가 한 번에 완성합니다", "자사 특화 템플릿에 그 회사만을 위한 내용이 채워집니다"),
    ]),
]


def features():
    tabs = "".join('<button type="button" data-t="%d"%s><span>%s</span></button>'
                   % (i, ' class="on"' if i == 0 else '', t[0]) for i, t in enumerate(TRACKS))
    navs, stages, mtrks = [], [], []
    for ti, (tname, steps) in enumerate(TRACKS):
        fbs = "".join('<div class="fb%s" data-f="%d"><div class="t">%s</div></div>'
                      % (' on' if i == 0 else '', i, t) for i, (t, d) in enumerate(steps))
        navs.append('<div class="fnavt%s" data-t="%d">%s</div>' % (' on' if ti == 0 else '', ti, fbs))
        sc = SCENE_1 if ti == 0 else SCENE_2
        panes = "".join('<div class="fpane%s">%s</div>' % (' on' if i == 0 else '', h)
                        for i, h in enumerate(sc))
        stages.append('<div class="ftrack%s" data-t="%d">%s</div>' % (' on' if ti == 0 else '', ti, panes))
        # 모바일: 사이드바로 트랙을 고르게 하지 않고, 두 트랙을 각각 핀 고정 블록으로 순서대로 노출한다.
        # .mtrk 높이를 JS가 늘려두고 .mtrk-in 이 sticky 로 붙어, 스크롤 진행도가 4단계를 차례로 넘긴다.
        mtrks.append('<div class="mtrk" data-t="%d"><div class="mtrk-in">'
                     '<div class="mtag"><span>%s</span></div>'
                     '<div class="mfnav">%s</div><div class="fstage">%s</div>'
                     '</div></div>' % (ti, tname, fbs, panes))
    return ('<section class="proc" id="features" data-track="0">'
            '<div class="proc-st pc-only"><div class="proc-h">'
            '<h2>미팅 전환율을 높이는 <span class="q">AI 영업 프로세스</span></h2></div>'
            '<div class="trk" id="trk">' + tabs + '</div>'
            '<div class="proc-b"><div class="fnav" id="fnav">' + "".join(navs) + '</div>'
            '<div class="fstage" id="fstage">' + "".join(stages) + '</div></div>'
            '</div>'
            '<div class="proc-m mob-only"><div class="proc-h">'
            '<h2>Bread&AI를 쓰시면<br>영업 방식이 <span class="q">이렇게 바뀝니다</span></h2></div>'
            + "".join(mtrks) +
            '</div></section>')


# ── 범용 AI 비교 ──────────────────────────────────────────────────────
# 모바일은 설명(작은 글자)을 없애고 큰 글자만 남기므로, 일부 항목은 모바일 전용 축약 문구를 따로 둔다.
# (질문, av, ad, bv, bd, av_모바일, bv_모바일) — 모바일 문구가 None이면 av/bv 그대로 쓴다.
CMP_ROWS = [
    ("제안 1건당 준비 시간은?",
     "30분 ~ 1시간", "같은 퀄리티를 얻으려면 대화를 반복",
     "3 ~ 5분", "최대 12배 단축", None, None),
    ("어제 한 작업은 남아있는가?",
     "대화창이 바뀌면 사라짐", "상품·타겟·톤을 매번 다시 설명",
     "팀 계정에 축적", "일관된 관점으로 영업 지속 및 팀 자산화", None, None),
    ("할루시네이션 문제는 없는가?",
     "매번 재확인 필요", "출처·수치 검증에 시간이 또 듦",
     "검증된 파이프라인의 일관된 산출물", "근거 출처가 함께 나옴",
     "매번 재검증 필요", "근거 출처를 명시"),
    ("우리 회사에 맞는 시스템 구축이 가능한가?",
     "소개서만 조금 바뀌어도 처음부터 다시 시작", "프롬프트·자료를 직접 재구성",
     "우리 회사 및 업종에 특화된 기능 고도화",
     "예) 렌터카는 고객사 차량 대수, 광고플랫폼은 매체비 사용 데이터",
     "소개서만 바뀌어도 처음부터", "우리 회사·업종 특화 기능 고도화"),
]


def _cmp_big(full, mobile):
    """PC 전체 문구와 모바일 축약 문구가 다르면 두 버전을 함께 심어 CSS로 전환한다."""
    if not mobile or mobile == full:
        return '<b>%s</b>' % full
    return '<b class="pc-only">%s</b><b class="mob-only">%s</b>' % (full, mobile)


def genai():
    rows = "".join(
        '<div class="cmpr">'
        '<div class="cmpk">%s</div>'
        '<div class="cmpa">%s<small class="pc-only">%s</small></div>'
        '<div class="cmpb">%s<small class="pc-only">%s</small></div>'
        '</div>' % (k, _cmp_big(av, avm), ad, _cmp_big(bv, bvm), bd)
        for k, av, ad, bv, bd, avm, bvm in CMP_ROWS)
    return ('<section class="s dotbg cmpsec" id="genai"><div class="wrap">'
            '<div class="cmphead rv">'
            '<p class="cmpq">챗GPT, 제미나이로도 충분하지 않냐구요?</p>'
            '<h2 class="pc-only">실질적인 매출 증가를 위해서는<br>'
            '<span class="ul">우리 회사에 맞는 영업 특화 AI</span>가 필요합니다</h2>'
            '<h2 class="mob-only"><span class="ul">우리 회사에 맞는 영업 특화 AI</span>만이<br>'
            '매출을 빠르게 증가시킵니다</h2>'
            '</div>'
            '<div class="cmp rv"><span class="cmpcol"></span>'
            '<div class="cmphd"><span></span><span>범용 AI</span>'
            '<span class="on">Bread&AI</span></div>'
            + rows +
            '</div>'
            '<p class="cmpend rv pc-only"><b class="cmpend1">영업은 효율이 생명입니다</b>'
            '<span class="cmpend2">범용 AI 쓰느라 제안·미팅 속도가 떨어지면<br>'
            '매출 파이프라인이 점점 줄어듭니다</span></p>'
            '</div></section>')


def nav_links(ab):
    ls = ['<a href="#features">주요 기능</a>', '<a href="#cases">도입 사례</a>',
          '<a href="#pricing">가격</a>']
    if ab == "B":
        # TODO: 리소스 페이지(resources.html) 별도 제작 필요
        ls.append('<a href="resources.html">리소스</a>')
    return "".join(ls)


# 모바일 히어로 마퀴에서 각 로고가 시각적으로 같은 무게로 보이도록 (높이, 세로 보정)을 개별 지정한다.
# (로고마다 원본 여백·자간이 달라 균일 높이로는 리멤버·미리디가 과하게 커 보인다.
#  SK렌터카는 글자 아래 여백이 있어 살짝 키우고 위로 올려야 다른 로고와 하단이 맞는다)
MQ_H = {"logo-skrent.png": (27, -3), "logo-remember.png": (15, 0), "logo-cashwalk.png": (17, 0),
        "logo-momsitter.png": (19, 0), "logo-miridih.png": (15, 0), "logo-eleven.png": (18, 0)}


def hero(ab, hv="hero"):
    note = ('<a class="hero-note" href="#cases">%s도입 기업 영상 인터뷰</a>' % I_PLAY) if ab == "B" else ""
    mq_imgs = "".join('<img src="assets/img/%s" alt="" style="height:%dpx;top:%dpx" decoding="async">'
                      % ((f,) + MQ_H.get(f, (18, 0))) for f, *_ in LOGOS) * 2
    return ('<div class="heroWrap" id="top"><header class="hero">'
            # 히어로 영상은 PC(가로 16:9) · 모바일(세로 9:16) 컷이 따로다.
            # src 를 비워두고 바로 아래 인라인 스크립트가 화면 크기에 맞는 것 하나만 받게 한다.
            '<div class="film"><video id="heroV" autoplay muted loop playsinline preload="auto"'
            ' data-pc="assets/video/hero-pc.mp4" data-mob="assets/video/hero-mob.mp4"'
            ' data-pcp="assets/img/hero-pc-poster.jpg" data-mobp="assets/img/hero-mob-poster.jpg">'
            '</video>'
            # 재생속도를 여기서 바로 걸어야 한다. 본 스크립트는 body 끝에서 실행되므로
            # 그 사이에 영상이 1배속으로 잠깐 재생돼 첫 화면이 튀어 보였다.
            '<script>(function(){var v=document.getElementById("heroV"),'
            'm=matchMedia("(max-width:1080px)").matches,R=0.7;'
            'v.poster=m?v.dataset.mobp:v.dataset.pcp;'
            'v.src=m?v.dataset.mob:v.dataset.pc;'
            'var fix=function(){if(v.playbackRate!==R)v.playbackRate=R};'
            '["loadedmetadata","loadeddata","canplay","play","playing"]'
            '.forEach(function(e){v.addEventListener(e,fix)});'
            'v.load();fix();})();</script>'
            '<div class="scrim"></div><div class="halo"></div></div>'
            '<div class="hero-in">'
            '<h1 class="pc-only"><span class="ln l1"><b>B2B 영업의 맞춤 제안이 가능해지는</b></span>'
            '<span class="ln l2 l"><b>AI Sales Intelligence</b></span></h1>'
            '<h1 class="mob-only mob-h">'
            '<span class="ln l1"><b>B2B 영업,</b></span>'
            '<span class="ln l2"><b>이제 맞춤 제안으로</b></span>'
            '<span class="ln l3 l"><b>AI 세일즈 인텔리전스</b></span></h1>'
            '<div class="roll"><div class="roll-f">상품 소개서만 업로드하면</div>'
            '<div class="roll-t" id="roll">'
            '<div class="rk on"><span class="pic">' + I_TARGET + '</span>타겟 기업 리스트 30개</div>'
            '<div class="rk"><span class="pic">' + I_MAIL + '</span>회사별 맞춤 이메일과 콜 스크립트</div>'
            '<div class="rk"><span class="pic">' + I_DECK + '</span>5분 만에 영업 제안서 PPT</div>'
            '</div></div>'
            '<div class="hero-cta">'
            '<span class="tip" data-tip="1주일간 모든 기능 체험 가능"><a class="btn btn-w" href="' + APP + '" target="_blank" rel="noopener">무료로 시작하기</a></span>'
            '<a class="btn btn-glass" href="#" data-modal="deck">소개서 받기</a></div>' + note +
            '</div>'
            # 로고 마퀴는 hero-in 바깥에 두어, 본문 길이와 무관하게 영상 최하단에 고정한다.
            '<div class="hero-mq mob-only"><div class="hero-mq-track">' + mq_imgs + '</div></div>'
            '</header></div>')


def logo_wall(ab):
    cells = []
    for i, (f, alt, h, name, num, cap, ph) in enumerate(LOGOS):
        cells.append(
            '<div class="lcell" data-i="%d"><span class="arw">↗</span>'
            '<img class="lg%s" style="height:%dpx" src="assets/img/%s" alt="%s" decoding="async"></div>'
            % (i, ' up' if f == 'logo-skrent.png' else '', h, f, alt))
    if ab == "A":
        return ('<section class="lwall pc-only"><div class="wrapw">'
                '<div class="lgrid a">' + "".join(cells) + '</div></div></section>')
    feat = ('<a class="lfeat" id="lfeat" href="#"><div class="bg" id="lfeatbg"></div>'
            '<img class="fimg" id="lfimg" src="assets/img/%s" alt="" decoding="async">'
            '<div class="ph" id="lfph">인터뷰 썸네일 준비 중</div><span class="arw2">↗</span>'
            '<div class="in"><div class="who" id="lfw">%s</div>'
            '<div class="num" id="lfn">%s</div><div class="cap" id="lfc">%s</div></div></a>'
            % (LOGOS[0][6], LOGOS[0][3], LOGOS[0][4], LOGOS[0][5]))
    return ('<section class="lwall pc-only"><div class="wrapw">'
            '<div class="lgrid b">' + "".join(cells) + feat + '</div></div></section>')


def band():
    items = "".join('<span class="bs">%s<em data-n="%d" data-k="%s">0</em></span>'
                    % (n, v, n) for n, v in BAND)
    return ('<div class="band pc-only"><div class="band-in">'
            '<span class="band-l"><i></i>고객사 사용 현황</span>' + items +
            '<span class="band-d">' + BAND_UPDATED + '</span></div></div>')


def why():
    cards = []
    for i, (tag, h3, p, pm, g, no) in enumerate(WHY_CARDS):
        body = ('<span class="pc-only">%s</span><span class="mob-only">%s</span>' % (p, pm)) if pm else p
        cards.append(
            '<article class="wc%s" data-i="%d" style="z-index:%d">'
            '<div class="wc-l"><div class="wcb%s"><div class="no">%s</div>'
            '<h3>%s</h3><p>%s</p></div></div>'
            '<div class="wc-r %s"><div class="gfx">%s</div></div></article>'
            % (' need' if i == 0 else '', i, i + 1,
               ' brk' if i == 0 else '', tag, h3, body, g, GFX[no]))
    cards.append(
        '<article class="wc ans" data-i="%d" style="z-index:%d">' % (len(WHY_CARDS), len(WHY_CARDS) + 1) +
        '<div class="wc-l"><div class="wcb">'
        '<div class="no">이제 AI 세일즈 인텔리전스 Bread&AI가 있으면</div>'
        '<h3>모든 타겟 기업들에게<br>'
        '<span class="qm">각각 맞춤 제안</span>을 보낼 수 있습니다</h3>'
        '<p>영업 준비를 AI가 하면, 더 많은 기업에게 더 정교한 맞춤 제안이 가능합니다.<br>'
        '제안 파이프라인이 많아지면, 자연히 미팅이 늘어나고 매출이 상승합니다.</p></div></div>'
        '<div class="wc-r g4"><div class="gfx">%s</div></div></article>' % GFX[4])
    dots = "".join('<i%s></i>' % (' class="on"' if i == 0 else '') for i in range(len(WHY_CARDS) + 1))
    return ('<section class="why dotbg" id="why"><div class="why-st">'
            '<div class="why-h"><h2>맞춤 제안 좋은 건 다들 아시면서<br>'
            '<span class="q">그 동안은 왜 못했을까요?</span></h2></div>'
            '<div class="why-stage">' + "".join(cards) + '</div>'
            '<div class="why-dots">' + dots + '</div></div></section>')


def why_mobile_msg():
    """WHY 카드 스택 다음에 오는 모바일 전용 상품소개 섹션.

    앞뒤가 모두 크림색 섹션이므로 짙은 틸 블루를 깔아 확실히 구분한다.
    도형은 PC 'ans' 카드에 쓰던 GFX[4](하나의 제안이 여러 기업으로 뻗어나가는 픽토그램)를 재사용한다.
    """
    return ('<section class="wmsg mob-only" data-nav="dark"><div class="wrap">'
            '<h2>이제 영업 전문 <span class="q">Bread&AI</span>로<br>'
            '모든 타겟 기업들에게<br>'
            '<span class="ul hlmark">맞춤 제안</span>을 보내세요</h2>'
            '<div class="wmsg-gfx">' + GFX[4] + '</div>'
            '<p><b>고객사 서칭, 맞춤 논리 수립, 이메일·제안서 작성</b><br>'
            '준비는 AI에게 다 맡기고<br>사람은 늘어나는 미팅에만 집중하세요</p>'
            '</div></section>')


def scenarios():
    left = ('<button class="scard sa" data-track="0" type="button">'
            '<span class="sph"><img src="assets/img/scen-1.jpg" alt="" decoding="async"></span>'
            '<span class="sbody">'
            '<span class="tag">Case 1</span>'
            '<h3>어느 곳부터 영업해야 할지<br>막막하신가요?</h3>'
            '<p>공략할 타겟 기업이 정해지지 않았을 때 소개서만 올리면<br>'
            'AI가 지금 영업할 기업 리스트를 생성하고 심층 리서치합니다.</p>'
            '<span class="pick">Bread&AI로 지금 영업할 기업 찾기 %s</span></span></button>' % I_ARROW)
    right = ('<button class="scard sb" data-track="1" type="button">'
             '<span class="sph"><img src="assets/img/scen-2.jpg" alt="" decoding="async"></span>'
             '<span class="sbody">'
             '<span class="tag">Case 2</span>'
             '<h3>타겟은 정해져 있지만,<br>어떻게 제안할지 고민되세요?</h3>'
             '<p>타겟 기업 리서치 기반으로 ‘왜 우리를 선택해야 하는지’ 맞춤 논리를 도출하고<br>'
             '이를 담은 이메일과 콜 스크립트, 제안서를 AI가 생성합니다.</p>'
             '<span class="pick">Bread&AI로 맞춤 이메일과 제안서 만들기 %s</span></span></button>' % I_ARROW)
    return ('<section class="s dotbg pc-only" id="start"><div class="wrap">'
            '<div class="head"><h2>귀사의 영업 팀은<br><span class="q">어떤 상황</span>에 '
            '놓여져 있나요?</h2>'
            '<p><b>타겟 기업을 새로 찾아야 하거나, 이미 정해져 있거나</b></p></div>'
            '<div class="sgrid rv">' + left + right + '</div></div></section>')


# ── 도입 사례 ─────────────────────────────────────────────────────────
# 실제 고객사 코멘트. 회사명은 업종 + 이니셜로 익명 표기.
CASES = [
    ("60명 영업팀이 함께 쓰면서,<br>영업 파이프라인 규모가 이전과 완전히 달라졌습니다",
     "대기업 모빌리티 S사", "월", "1,000", "개사", "제안 기업 수", 1000),
    ("고객사의 이야기로 시작하니,<br>콜드메일 응답률이 3배 이상 올라갔습니다",
     "O2O플랫폼 E사", "", "8", "%", "콜드메일·콜드콜 회신율", 8),
    ("광고 사업을 시작한 지 얼마 안 됐는데도,<br>아웃바운드 영업의 루틴이 잡혔습니다",
     "광고플랫폼 M사", "주", "3", "건 이상", "영업 미팅 수", 3),
]


def impact(ab):
    out = []
    for i, (q, who, pre, v, u, lab, n) in enumerate(CASES):
        out.append('<article class="tc rv d%d" data-i="%d">'
                   '<div class="who">%s</div>'
                   '<blockquote><i class="qo">“</i><span class="qt">%s</span>'
                   '<i class="qc">”</i></blockquote>'
                   '<div class="stat"><div class="bl">%s</div>'
                   '<div class="big"><span class="pre">%s</span>'
                   '<span class="nm" data-c="%s">%s</span>'
                   '<span class="u">%s</span></div></div>'
                   '</article>'
                   % (i + 1, i, who, q, lab, pre, n, v, u))
    return ('<section class="overlap" id="cases" data-nav="dark"><div class="wrap">'
            '<div class="head rv"><h2>Bread&AI를 쓰는 영업팀들은<br>'
            '<span class="q">달라진 영업 성과</span>를 얘기합니다</h2></div>'
            '<div class="tg">' + "".join(out) + '</div></div></section>'
            )


def _li(full, short):
    """가격 카드 체크 항목. 모바일에서는 한 줄에 들어오는 축약 문구로 바꿔 카드 길이를 줄인다."""
    if short == full:
        return '<li>%s</li>' % full
    return '<li><span class="pc-only">%s</span><span class="mob-only">%s</span></li>' % (full, short)


PRICING = ('<section class="s dotbg" id="pricing"><div class="wrap">'
           '<div class="head"><h2>맞춤 제안에 투자하면<br><span class="q">매출 상승</span>으로 돌아옵니다</h2></div>'
           '<div class="pg rv">'
           '<div class="pc"><h3>Basic</h3>'
           '<p class="pd pc-only">미팅 전환율을 높여 영업 성과를 만들어야 하는 성장형 B2B 팀</p>'
           '<div class="pp">월 100만원</div><div class="pt">3개월 단위 결제 · 총 300만원 · 5인 기본</div>'
           '<div class="pin2"><div class="r"><span>기본 제공 계정</span><b>5인</b></div>'
           '<div class="r"><span>맞춤 제안서 생성</span><b>무제한*</b></div>'
           '<div class="r"><span>제안서 템플릿</span><b>범용 템플릿</b></div></div>'
           '<ul class="pfe">'
           + _li('타겟 기업 심층 분석 및 페인포인트 도출', '타겟 기업 심층 분석')
           + _li('기업별 맞춤형 아웃바운드 이메일 작성', '기업별 맞춤 이메일 작성')
           + _li('첫 미팅 성사를 위한 검증된 기본 제안 템플릿', '검증된 기본 제안 템플릿') +
           '</ul>'
           '<a class="btn btn-o" href="#" data-modal="contact" data-plan="Basic">도입 문의하기</a></div>'
           '<div class="pc hot"><span class="pb">가장 많이 선택</span><h3>Pro</h3>'
           '<p class="pd pc-only">자사 브랜딩 제안서로 전환율을 극대화하고 파이프라인을 키우려는 영업 조직</p>'
           '<div class="pp">월 200만원</div><div class="pt">3개월 단위 결제 · 총 600만원 · 10인 기본</div>'
           '<div class="pin2"><div class="r"><span>기본 제공 계정</span><b>10인</b></div>'
           '<div class="r"><span>맞춤 제안서 생성</span><b>무제한*</b></div>'
           '<div class="r"><span>제안서 템플릿</span><b class="h">자사 특화 세팅</b></div></div>'
           '<ul class="pfe">'
           + _li('Basic 플랜의 모든 기능 포함', 'Basic 플랜 전체 기능 포함')
           + _li('고객사 전용 디자인·로고 템플릿 세팅', '자사 전용 디자인 템플릿')
           + _li('초기 온보딩 세션 지원', '초기 온보딩 세션 지원') +
           '</ul><a class="btn btn-p" href="#" data-modal="contact" data-plan="Pro">도입 문의하기</a></div>'
           '<div class="pc"><h3>Enterprise</h3>'
           '<p class="pd pc-only">다수 계정과 유연한 맞춤 관리가 필요한 대규모 영업 조직</p>'
           '<div class="pp">Custom</div><div class="pt">연간 계약 · 요구사항에 따른 협의</div>'
           '<div class="pin2"><div class="r"><span>기본 제공 계정</span><b>무제한 (협의)</b></div>'
           '<div class="r"><span>맞춤 제안서 생성</span><b>무제한*</b></div>'
           '<div class="r"><span>제안서 템플릿</span><b>다중 브랜드 커스텀</b></div></div>'
           '<ul class="pfe">'
           + _li('Pro 플랜의 모든 기능 포함', 'Pro 플랜 전체 기능 포함')
           + _li('기업 맞춤 온보딩 및 교육', '기업 맞춤 온보딩 및 교육')
           + _li('특화 기능 지원', '특화 기능 지원') +
           '</ul>'
           '<a class="btn btn-o" href="#" data-modal="contact" data-plan="Enterprise">견적 상담하기</a></div></div>'
           # 모바일 캐러셀에 좌우로 넘길 수 있다는 표시
           '<div class="pgdots mob-only"><i></i><i class="on"></i><i></i></div>'
           '<div class="pn rv"><div><b>계정 추가 옵션</b>'
           '<p>기본 제공 계정 초과 시 Basic / Pro 계정당 월 20만원/인이 추가됩니다. (3개월 단위 결제)</p></div>'
           '<div><b>* 공정 사용 정책</b>'
           '<p>제안서 무제한 생성을 원칙으로 하되, 비정상적인 과다 호출 감지 시 이용 속도가 제한될 수 있습니다.</p></div>'
           '</div></div></section>')

FAQ_ITEMS = [
    ("Bread &amp; AI는 어떤 솔루션인가요?",
     "B2B 영업의 Pre-sales 전체를 AI로 자동화하는 세일즈 인텔리전스 솔루션입니다. "
     "AI가 타겟 기업의 상황을 분석하고, 그에 맞는 제안서와 이메일을 자동 생성하여 미팅 전환율을 높입니다."),
    ("처음 쓰는데 어떻게 시작하나요?",
     "회사 소개서 PDF 한 장만 업로드하시면 됩니다. 제품 강점을 자동으로 추출한 뒤 가망 기업 리스트를 만들어드립니다."),
    ("기존 영업 방식과 무엇이 다른가요?",
     "기존에는 한 기업에 맞춤 제안을 준비하는 데 2–3시간이 걸려 대부분 같은 내용의 메일을 복사해 보냈습니다. "
     "Bread &amp; AI는 타겟 기업의 현황, Pain Point, 최근 이슈를 자동 분석하고 기업 상황에 맞는 제안서와 이메일을 생성합니다."),
    ("업로드한 소개서와 고객 정보는 안전한가요?",
     "업로드된 자료는 모델 학습에 사용되지 않으며 고객사 워크스페이스 단위로 격리 저장됩니다. "
     "전송 구간은 TLS 1.3, 저장 구간은 AES-256으로 암호화하며, 요청 시 전량 영구 삭제 후 결과를 문서로 회신드립니다."),
    ("가격은 얼마인가요?",
     "Basic 플랜 월 100만원(3개월 단위 결제, 5인 기본), Pro 플랜 월 200만원(3개월 단위 결제, 10인 기본)부터 시작합니다. "
     "Enterprise는 맞춤 견적을 제공합니다."),
    ("제안서는 어떤 형식으로 나오나요?",
     "15–20장 분량의 PPT(PPTX) 파일로 생성되며, 원본 회사 소개서의 브랜드 컬러가 반영됩니다. "
     "Pro 플랜부터는 자사 전용 디자인·로고 템플릿을 세팅해 드립니다."),
]


def faq():
    its = []
    for i, (q, a) in enumerate(FAQ_ITEMS):
        its.append('<div class="fq%s"><button type="button"><span>%s</span><span class="pm"></span></button>'
                   '<div class="an"><p>%s</p></div></div>' % (' on' if i == 0 else '', q, a))
    return ('<section class="s" id="faq" style="background:var(--paper);border-top:1px solid var(--line)">'
            '<div class="wrap"><div class="head"><h2>자주 묻는 질문</h2></div>'
            '<div class="faq">' + "".join(its) + '</div></div></section>')


SURVEY = "https://breadaisurvey.vercel.app/survey"
APP = "https://app.breadai.co.kr/"        # 무료 체험·로그인 진입
CONTACT_MAIL = "contact@breadai.co.kr"    # 모달 폼 제출 수신처


# ── 문의 모달 ─────────────────────────────────────────────────────────
# 기존 홈페이지 모달과 같은 항목 구성. '소개서 받기'(deck)와 '도입 문의'(contact)가
# 같은 폼을 쓰고 제목·안내문·버튼·문의내용 노출 여부만 바뀐다.
# 수신처는 JS 상단 FORM_ENDPOINT 한 줄로 결정된다(비어 있으면 메일 클라이언트로 대체).
MODAL = ('<div class="mdl" id="mdl" hidden>'
         '<div class="mdl-bg" data-close></div>'
         '<div class="mdl-box" role="dialog" aria-modal="true" aria-labelledby="mdlT">'
         '<div class="mdl-hd"><h3 id="mdlT">도입 문의하기</h3>'
         '<button class="mdl-x" type="button" aria-label="닫기" data-close>&times;</button></div>'
         '<form id="mdlF" novalidate>'
         '<div class="mdl-plan" id="mdlPlan" hidden>관심 플랜: <b></b></div>'
         '<p class="mdl-d" id="mdlD">아래 정보를 남겨주시면 담당자가 빠르게 연락드립니다.</p>'
         '<label class="f">회사명 <i>*</i><input name="회사명" required placeholder="예: 삼성전자" autocomplete="organization"></label>'
         '<div class="mdl-2"><label>부서<input name="부서" placeholder="예: 영업팀"></label>'
         '<label>직함<input name="직함" placeholder="예: 팀장"></label></div>'
         '<label class="f">이름 <i>*</i><input name="이름" required placeholder="홍길동" autocomplete="name"></label>'
         '<label class="f">이메일 <i>*</i><input name="이메일" type="email" required '
         'placeholder="name@company.com" autocomplete="email"></label>'
         '<label class="f">연락처<input name="연락처" placeholder="01012345678" autocomplete="tel"></label>'
         '<label class="f" id="mdlMemo">문의 내용'
         '<textarea name="문의내용" rows="3" placeholder="궁금하신 점이나 요청사항을 자유롭게 적어주세요."></textarea></label>'
         '<label class="mdl-chk"><input type="checkbox" name="동의" required>'
         '<span>개인정보 수집·이용에 동의합니다</span></label>'
         '<button class="btn mdl-go" type="submit">문의 보내기</button>'
         '<p class="mdl-msg" id="mdlMsg" hidden></p>'
         '</form></div></div>')

ENDING = ('<section class="end">'
          '<div class="end-bg pc-only" style="background-image:url(assets/img/end-bg.jpg)"></div>'
          '<div class="wrap">'
          '<h2 class="rv pc-only">영업은 결국,<br>상대를 '
          '<span class="ul hlmark">얼마나 아느냐</span>의 싸움입니다</h2>'
          '<h2 class="rv mob-only">부담없이<br><span class="ul hlmark">무료 체험</span>부터 해보세요</h2>'
          '<p class="lead pc-only">Bread&amp;AI를 <b class="hi">1주일 무료 체험</b>하면서 타겟 기업을 리서치하세요<br>'
          '먼저 <b class="hi">우리 팀 역량을 진단</b>하기 위해 테스트부터 하셔도 좋습니다</p>'
          '<div class="row pc-only">'
          '<span class="tip" data-tip="1주일간 모든 기능 체험 가능"><a class="btn btn-d" href="' + APP + '" target="_blank" rel="noopener">무료 체험 시작</a></span>'
          '<span class="tip" data-tip="20문항으로 우리 팀 역량 평가">'
          '<a class="btn btn-ow" href="' + SURVEY + '" target="_blank" rel="noopener">우리 영업팀 자가 진단</a></span>'
          '</div>'
          # 모바일: 서브카피 → CTA 를 한 쌍으로 묶어 두 갈래를 순서대로 보여준다.
          '<div class="end-m mob-only">'
          '<div class="end-opt"><p>Bread&amp;AI의 <b>모든 기능을 직접</b> 써 보시려면</p>'
          '<a class="btn btn-d" href="' + APP + '" target="_blank" rel="noopener">1주일 무료 체험 시작</a></div>'
          '<div class="end-opt"><p>우리 팀 역량 진단을 위해 <b>테스트</b>부터 하시려면</p>'
          '<a class="btn btn-ow" href="' + SURVEY + '" target="_blank" rel="noopener">영업팀 자가 진단</a></div>'
          '</div>'
          '</div></section>')



def footer(ab):
    res = ('<div><h5>리소스</h5><a href="resources.html">도입 사례</a><a href="resources.html">블로그</a>'
           '<a href="resources.html">리포트</a></div>') if ab == "B" else ""
    return ('<footer><div class="wrap"><div class="ft"><div class="fb2">'
            '<div class="fl">Bread&amp;AI</div>'
            '<p>맞춤 제안을 가능하게 하는 AI Sales Intelligence</p></div>'
            '<div class="fc">'
            '<div><h5>제품</h5><a href="#start">시작 방식</a><a href="#features">주요 기능</a>'
            '<a href="#pricing">가격</a></div>' + res +
            '<div><h5>리소스</h5>'
            '<a href="' + SURVEY + '" target="_blank" rel="noopener">영업팀 자가 진단</a></div>'
            '</div></div>'
            '<div class="fbiz">'
            '<span>(주)브레드앤에이아이</span><span>대표자 이승욱</span>'
            '<span>사업자등록번호 874-33-01581</span>'
            '<span>서울특별시 송파구 가락로 244, 3층 305-S28호(방이동, 동원빌딩)</span>'
            '</div>'
            '<div class="fbot">© 2026 Bread &amp; AI. All rights reserved.</div></div></footer>')



JS = r"""
(function(){
  var nav=document.getElementById('nav'), prog=document.getElementById('prog');
  var hw=document.getElementById('top');
  var darks=[].slice.call(document.querySelectorAll('[data-nav="dark"]'));
  var mob=matchMedia('(max-width:1080px)').matches;
  var cl=function(v,a,b){return v<a?a:v>b?b:v};

  /* ── 히어로: 스크롤 시 영상이 프레임 안으로 축소 ── */
  var hero=document.querySelector('.hero');
  var hv=document.querySelector('.film video');
  if(hv){hv.playbackRate=0.7;hv.addEventListener('loadedmetadata',function(){hv.playbackRate=0.7})}
  function heroFrame(){
    if(!hw||!hero) return;
    var q=cl(scrollY/(innerHeight*0.72),0,1);
    var eased=q*q*(3-2*q);
    /* 모바일에서는 영상 축소(프레임 인) 없이 전체 화면을 유지한다 — 아래 베이지 리빌 문구를 없앴기 때문. */
    if(!mob){
      hero.style.setProperty('--fi',(eased*58).toFixed(1)+'px');
      hero.style.setProperty('--fr',(eased*34).toFixed(1)+'px');
    }
    var f=cl((q-0.18)/0.42,0,1);
    hero.style.setProperty('--ho',(1-f).toFixed(3));
    hero.style.setProperty('--hy',(f*46).toFixed(1));
  }

  function frame(){
    var y=scrollY, vh=innerHeight, max=document.body.scrollHeight-vh;
    prog.style.width=(max>0?cl(y/max,0,1)*100:0)+'%';
    var onDark=false;
    for(var i=0;i<darks.length;i++){
      var b=darks[i].getBoundingClientRect();
      if(b.top<=76&&b.bottom>=76){onDark=true;break}
    }
    var overHero = hw && hw.getBoundingClientRect().bottom>76;
    nav.classList.toggle('dark',onDark);
    nav.classList.toggle('solid',!(overHero||onDark));
    heroFrame(); whyFrame(); procFrame(); procMobFrame();
  }
  var t=false;
  addEventListener('scroll',function(){if(!t){t=true;requestAnimationFrame(function(){frame();t=false})}},{passive:true});
  addEventListener('resize',function(){mob=matchMedia('(max-width:1080px)').matches;
    setWhyHeight();setProcHeight();setMtrkHeight();frame()});

  /* ── 등장 ── */
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}})},{threshold:.08,rootMargin:'0px 0px -50px'});
  document.querySelectorAll('.rv').forEach(function(el){io.observe(el)});

  var vo=new IntersectionObserver(function(es){es.forEach(function(e){
    e.target.classList.toggle('in-view',e.isIntersecting)})},{threshold:.3});
  document.querySelectorAll('.scard').forEach(function(el){vo.observe(el)});

  /* ── 히어로 롤링 문구 ── */
  var rks=document.querySelectorAll('#roll .rk');
  if(rks.length){var k=0;setInterval(function(){
    rks.forEach(function(x){x.classList.remove('on')});k=(k+1)%rks.length;rks[k].classList.add('on');},2600)}

  /* ── 로고월 → 인터뷰 패널 (B안) ── */
  var LF=window.__LF||[];
  var lfw=document.getElementById('lfw'),lfn=document.getElementById('lfn'),
      lfc=document.getElementById('lfc'),lfbg=document.getElementById('lfeatbg');
  if(lfw){
    var BGS=['linear-gradient(150deg,#5C7364,#2F4A46 48%,#1E2C2B)',
             'linear-gradient(150deg,#6B6A52,#3F4436 48%,#232620)',
             'linear-gradient(150deg,#6E5D52,#443831 48%,#26201C)',
             'linear-gradient(150deg,#4F6570,#2C4450 48%,#1A2830)',
             'linear-gradient(150deg,#5A5F6E,#343A46 48%,#1F2229)',
             'linear-gradient(150deg,#6A5566,#413143 48%,#241B26)'];
    document.querySelectorAll('.lcell').forEach(function(c){
      c.addEventListener('mouseenter',function(){
        var i=+c.dataset.i, d=LF[i]; if(!d)return;
        lfw.textContent=d[0]; lfn.textContent=d[1]; lfc.textContent=d[2];
        lfbg.style.background=BGS[i%BGS.length];
        var im=document.getElementById('lfimg'), ph=document.getElementById('lfph');
        if(d[3]){im.src='assets/img/'+d[3];im.style.display='block';ph.style.display='none'}
        else{im.style.display='none';ph.style.display='flex'}
      });
    });
  }

  /* ── 고객사 사용 현황 띠: 카운트업 후 라이브 틱 ──
     ※ 현재 값은 임시 플레이스홀더. 운영 API 연결 시 fetch 로 교체할 것. */
  var fmt=function(n){return Math.round(n).toLocaleString('ko-KR')};
  /* assets/usage.json 이 있으면 그 값으로 덮어쓴다. 없으면 내장값 사용.
     → 숫자만 갱신할 때 재빌드·재배포 없이 JSON 한 줄만 고치면 된다. */
  function loadUsage(done){
    try{
      fetch('assets/usage.json',{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){
        if(d&&d.items) document.querySelectorAll('[data-n]').forEach(function(el){
          var v=d.items[el.dataset.k]; if(v!=null) el.dataset.n=v;});
      }).catch(function(){}).then(done,done);
    }catch(err){done()}
  }
  var bo=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;
    var el=e.target, tv=+el.dataset.n;
    var c=Math.round(tv*0.82), d=(tv-c)/72;
    var iv=setInterval(function(){c+=d;if(c>=tv){c=tv;clearInterval(iv)}
      el.textContent=fmt(c)},16);
    bo.unobserve(el)})},{threshold:.4});
  loadUsage(function(){document.querySelectorAll('[data-n]').forEach(function(el){bo.observe(el)})});

  /* 천단위 구분 — 로케일/정규식에 의존하지 않는 수동 포맷 */
  function fmtN(n){var s=String(n),o='',k=0;
    for(var i=s.length-1;i>=0;i--){o=s.charAt(i)+o;if(++k%3===0&&i>0)o=','+o}
    return o}

  /* ── 숫자 카운트업 ── (성과 카드의 .nm 은 자체 핸들러가 있으므로 제외) */
  var co=new IntersectionObserver(function(es){es.forEach(function(e){
    if(!e.isIntersecting)return;
    var el=e.target, tv=parseFloat(el.dataset.c), dec=+(el.dataset.dec||0), c=0, st=tv/54;
    var iv=setInterval(function(){c+=st;if(c>=tv){c=tv;clearInterval(iv)}
      el.textContent=dec?c.toFixed(1):fmtN(Math.round(c))},16);
    co.unobserve(el)})},{threshold:.5});
  document.querySelectorAll('[data-c]:not(.nm)').forEach(function(el){co.observe(el)});

  /* ── WHY 카드 스택 ── */
  var why=document.querySelector('.why'), wcAll=document.querySelectorAll('.wc'),
      wdots=document.querySelectorAll('.why-dots i'), wcur=-1, wmob=null;
  /* 모바일은 마지막 요약 카드(.ans)를 감추고 별도 섹션(.wmsg)으로 대체하므로 스택에서 제외한다. */
  function wlist(){
    if(!mob) return wcAll;
    if(!wmob) wmob=[].filter.call(wcAll,function(c){return !c.classList.contains('ans')});
    return wmob;
  }
  function setWhyHeight(){
    if(!why) return;
    var n=wlist().length;
    /* 모바일은 카드당 스크롤 여유를 조금 더 줘서 한 장씩 넘어가는 느낌이 나게 한다. */
    why.style.height=((n+1)*(mob?58:50))+'vh';
  }
  setWhyHeight();
  function whyFrame(){
    if(!why) return;
    var list=wlist(), n=list.length;
    var total=why.offsetHeight-innerHeight; if(total<=0) return;
    var p=cl(-why.getBoundingClientRect().top/total,0,1);
    var idx=cl(Math.floor(p*n*1.04),0,n-1);
    if(idx!==wcur){
      wcur=idx;
      [].forEach.call(list,function(c,i){
        var d=i-idx;
        if(d>0){c.style.transform='translateY(100%)';c.style.opacity='0'}
        else if(d===0){c.style.transform='none';c.style.opacity='1'}
        else{var a=Math.min(-d,3);
          /* 지나간 카드는 위로 날아가며 작아진다 */
          c.style.transform='translateY('+(mob?-40*a:-24*a)+'px) scale('+(1-0.045*a)+')';
          c.style.opacity=String(Math.max(0,1-(mob?0.55:0.42)*a))}
      });
      [].forEach.call(list,function(c,i){c.classList.toggle('cur',i===idx)});
      wdots.forEach(function(x,i){x.classList.toggle('on',i===idx)});
    }
  }

  /* ── 프로세스: 핀 + 스크롤로 단계 이동(PC) / 자동 진행(모바일) ── */
  var proc=document.querySelector('.proc'),
      pStep=0, pTimer=null, pIn=false, pCur=-1;
  function panes(){var t=document.querySelector('.ftrack.on');return t?t.querySelectorAll('.fpane'):[]}
  function fbsOf(){var n=document.querySelector('.fnavt.on');return n?n.querySelectorAll('.fb'):[]}
  function setProcHeight(){if(proc) proc.style.height=mob?'':((panes().length+1)*55)+'vh'}
  setProcHeight();
  function procFrame(){
    if(!proc||mob) return;
    var n=panes().length; if(!n) return;
    var total=proc.offsetHeight-innerHeight; if(total<=0) return;
    var p=cl(-proc.getBoundingClientRect().top/total,0,1);
    var idx=cl(Math.floor(p*n*1.04),0,n-1);
    if(idx!==pCur) showStep(idx,false);
  }
  function countUp(pane){
    if(!pane) return;
    pane.querySelectorAll('.cnt').forEach(function(el){
      var tv=parseFloat(el.dataset.c),c=0,st=tv/42;
      clearInterval(el._iv);
      el._iv=setInterval(function(){c+=st;if(c>=tv){c=tv;clearInterval(el._iv)}
        el.textContent=fmtN(Math.round(c))},20);
    });
  }
  function showStep(i,restart){
    var fps=panes(), fbs=fbsOf();
    if(!fps.length) return;
    pStep=i; pCur=i;
    fbs.forEach(function(x,k){x.classList.toggle('on',k===i)});
    fps.forEach(function(x,k){
      if(k===i){x.classList.remove('on');void x.offsetWidth;x.classList.add('on')}
      else x.classList.remove('on');
    });
    countUp(fps[i]);
    if(restart) arm();
  }
  function arm(){clearTimeout(pTimer);if(!pIn||!mob)return;
    /* Case 2는 읽을 문장이 많아 더 오래 머문다 */
    var ms=(proc&&+proc.dataset.track===1)?6900:5400;
    pTimer=setTimeout(function(){showStep((pStep+1)%panes().length,true)},ms)}
  var swTimer=null;
  function switchTrack(ti){
    if(!proc) return;
    if(+proc.dataset.track===ti && proc.dataset.ready==='1'){showStep(0,true);return}
    var pb=document.querySelector('.proc-b'), dir=(ti===1?-1:1);
    document.querySelectorAll('#trk button').forEach(function(b,i){b.classList.toggle('on',i===ti)});
    clearTimeout(swTimer);
    if(pb){
      /* 1) 진행 방향으로 밀려 나가고 */
      pb.style.setProperty('--sx',(dir*7)+'%');
      pb.classList.add('sw-out');
    }
    swTimer=setTimeout(function(){
      document.querySelectorAll('.ftrack').forEach(function(x){x.classList.toggle('on',+x.dataset.t===ti)});
      document.querySelectorAll('.fnavt').forEach(function(x){x.classList.toggle('on',+x.dataset.t===ti)});
      proc.setAttribute('data-track',ti);
      proc.dataset.ready='1';
      if(pb){
        /* 2) 반대편에서 밀려 들어온다 — 끊김 없이 이어지도록 */
        pb.style.setProperty('--sx',(-dir*7)+'%');
        pb.classList.remove('sw-out');void pb.offsetWidth;
        pb.classList.add('sw-in');
        setTimeout(function(){pb.style.setProperty('--sx','0%')},20);
        setTimeout(function(){pb.classList.remove('sw-in')},640);
      }
      showStep(0,true);
    },300);
  }
  if(proc){
    new IntersectionObserver(function(es){es.forEach(function(e){
      pIn=e.isIntersecting;
      if(pIn){showStep(pStep,true)}else{clearTimeout(pTimer)}
    })},{threshold:.35}).observe(proc);
  }
  /* ── 프로세스(모바일): 트랙마다 핀 고정 + 스크롤 진행도로 4단계를 차례로 넘긴다 ──
     타이머로 자동 재생하면 너무 빨리 지나가 읽히지 않으므로, 체류 시간을 스크롤이 결정하게 한다. */
  var mtrks=[].slice.call(document.querySelectorAll('.mtrk'));
  mtrks.forEach(function(trk){
    trk._fbs=trk.querySelectorAll('.mfnav .fb');
    trk._panes=trk.querySelectorAll('.fpane');
    trk._cur=-1;
    trk._show=function(idx){
      if(idx===trk._cur) return;
      trk._cur=idx;
      [].forEach.call(trk._fbs,function(x,k){x.classList.toggle('on',k===idx)});
      [].forEach.call(trk._panes,function(x,k){
        if(k===idx){x.classList.remove('on');void x.offsetWidth;x.classList.add('on');countUp(x)}
        else x.classList.remove('on');
      });
    };
    [].forEach.call(trk._fbs,function(b,k){
      b.addEventListener('click',function(){trk._show(k)});
    });
  });
  function setMtrkHeight(){
    if(!mtrks) return;
    /* 헤드카피가 sticky 로 상단에 붙으므로, 그 높이만큼 트랙을 아래로 내려 붙인다 */
    var pm=document.querySelector('.proc-m'), ph=document.querySelector('.proc-m .proc-h');
    if(pm&&ph) pm.style.setProperty('--ph',(mob?ph.offsetHeight:0)+'px');
    mtrks.forEach(function(trk){
      /* 단계당 약 58vh 의 스크롤 여유 — 각 단계가 충분히 머물다 넘어가도록 */
      trk.style.height=mob?((trk._panes.length+1)*58)+'vh':'';
    });
  }
  setMtrkHeight();
  function procMobFrame(){
    if(!mob||!mtrks) return;
    mtrks.forEach(function(trk){
      var n=trk._panes.length; if(!n) return;
      var r=trk.getBoundingClientRect();
      /* 화면 밖에서는 아무 단계도 켜두지 않는다 — 미리 돌아버리면 진입했을 때 이미 끝나 있다 */
      if(r.top>innerHeight||r.bottom<0){
        if(trk._cur!==-1){
          trk._cur=-1;
          [].forEach.call(trk._panes,function(x){x.classList.remove('on')});
          [].forEach.call(trk._fbs,function(x){x.classList.remove('on')});
        }
        return;
      }
      var total=trk.offsetHeight-innerHeight; if(total<=0) return;
      var p=cl(-r.top/total,0,1);
      /* 4단계를 스크롤 구간에 정확히 균등 분배 (마지막 단계만 길어지지 않도록) */
      trk._show(cl(Math.floor(p*n),0,n-1));
    });
  }
  procMobFrame();
  /* ── 도입 사례: 마우스 오버 시 숫자 카운트업 ── */
  document.querySelectorAll('.tc .nm').forEach(function(el){
    var tv=parseFloat(el.dataset.c), card=el.closest('.tc');
    function run(){
      clearInterval(el._iv);
      /* 작은 수치는 0부터 세어 올린다 (예: 영업 미팅 0 → 3) */
      var c=(tv<20?0:tv*0.42), st=(tv-c)/34;
      el.classList.add('counting');
      el._iv=setInterval(function(){c+=st;
        if(c>=tv){c=tv;clearInterval(el._iv);el.classList.remove('counting')}
        el.textContent=fmtN(Math.round(c))},18);
    }
    card.addEventListener('mouseenter',run);
    card.addEventListener('focusin',run);
    /* 터치 환경에는 hover 가 없으므로 탭하면 다시 센다 */
    card.addEventListener('click',run);
    new IntersectionObserver(function(es,ob){es.forEach(function(en){
      if(!en.isIntersecting) return;
      ob.unobserve(en.target);
      /* .rv 등장 트랜지션이 끝난 뒤 세어야 숫자가 올라가는 게 실제로 보인다 */
      setTimeout(run,520);
    })},{threshold:.35}).observe(card);
  });

  /* 상품소개 섹션(모바일) — 화면에 들어오면 픽토그램 애니메이션을 재생 */
  var wmsg=document.querySelector('.wmsg');
  if(wmsg){
    new IntersectionObserver(function(es){es.forEach(function(e){
      e.target.classList.toggle('cur',e.isIntersecting)})},{threshold:.3}).observe(wmsg);
  }

  document.addEventListener('click',function(ev){
    var b=ev.target.closest('#trk button');
    if(b){switchTrack(+b.dataset.t);return}
    var fb=ev.target.closest('.fnavt.on .fb');
    if(fb){showStep([].indexOf.call(fbsOf(),fb),true)}
  });

  /* ── 시나리오 카드 → 프로세스 해당 시나리오로 이동 ── */
  document.querySelectorAll('.scard').forEach(function(c){
    c.addEventListener('click',function(){
      switchTrack(+c.dataset.track);
      if(proc){
        var y=proc.getBoundingClientRect().top+scrollY-58;
        scrollTo({top:y,behavior:'smooth'});
        setTimeout(function(){pIn=true;showStep(0,true)},700);
      }
    });
  });

  /* ── FAQ ── */
  document.querySelectorAll('.fq button').forEach(function(b){b.onclick=function(){
    var f=b.parentElement, open=f.classList.contains('on');
    document.querySelectorAll('.fq').forEach(function(x){x.classList.remove('on')});
    if(!open)f.classList.add('on');}});

  /* ── 가격(모바일): 캐러셀 초기 위치를 Pro 카드가 중앙에 오도록 ── */
  function centerPricing(){
    if(!mob) return;
    var pg=document.querySelector('#pricing .pg'), hot=document.querySelector('#pricing .pc.hot');
    if(!pg||!hot) return;
    pg.scrollLeft=hot.offsetLeft-(pg.clientWidth-hot.offsetWidth)/2;
  }
  addEventListener('load',centerPricing);
  setTimeout(centerPricing,300);
  /* 섹션에 처음 도달했을 때도 Pro가 먼저 보이도록 — 사용자가 직접 넘기기 전까지만 보정한다 */
  (function(){
    var pgz=document.querySelector('#pricing .pg'), sec=document.querySelector('#pricing');
    if(!pgz||!sec) return;
    var touched=false;
    ['pointerdown','touchstart','wheel','keydown'].forEach(function(ev){
      pgz.addEventListener(ev,function(){touched=true},{passive:true});
    });
    new IntersectionObserver(function(es){es.forEach(function(e){
      if(e.isIntersecting&&!touched) centerPricing();
    })},{threshold:.15}).observe(sec);
  })();
  /* 캐러셀 위치에 맞춰 하단 점 표시를 갱신한다 */
  (function(){
    var pg=document.querySelector('#pricing .pg'),
        dots=document.querySelectorAll('#pricing .pgdots i'),
        cards=document.querySelectorAll('#pricing .pc');
    if(!pg||!dots.length) return;
    function sync(){
      var c=pg.scrollLeft+pg.clientWidth/2, best=0, bd=1e9;
      [].forEach.call(cards,function(x,i){
        var d=Math.abs(x.offsetLeft+x.offsetWidth/2-c);
        if(d<bd){bd=d;best=i}
      });
      dots.forEach(function(x,i){x.classList.toggle('on',i===best)});
    }
    pg.addEventListener('scroll',function(){clearTimeout(pg._st);pg._st=setTimeout(sync,60)},{passive:true});
    addEventListener('load',sync);
    setTimeout(sync,400);
  })();

  /* ── 문의 · 소개서 모달 ────────────────────────────────────────────
     ※ 아래 수신처들은 실제 운영 연동이다. 임의로 비우지 말 것.
        · 도입 문의   → Web3Forms (담당자 메일 수신)
        · 소개서 받기 → /api/send-brochure (소개서 PDF 자동 발송)
        · 공통        → logLead()로 통합 리드 마스터 시트에 기록          */

  /* 통합 리드 마스터(구글시트) 웹훅 — 모든 인바운드 리드를 기록한다 */
  var LEAD_HOOK = 'https://script.google.com/macros/s/AKfycbwLUMOe89imz-B6uqM3YD5Vy_6lSxCbqaDan4fWMvRumFLAYZ7CedzWm_dENKV79lw/exec';
  var LEAD_HOOK_SECRET = '17b997a38d4a5f02fe18fa93ff8edf11';
  function logLead(source, data){
    try{
      fetch(LEAD_HOOK,{
        method:'POST', mode:'no-cors',
        headers:{'Content-Type':'text/plain'},
        body:JSON.stringify(Object.assign({secret:LEAD_HOOK_SECRET, source:source}, data))
      });
    }catch(e){ /* 훅 실패는 무시 — 제출 흐름에 영향 없음 */ }
  }

  /* 도입 문의는 자체 API(/api/send-contact)로 발송한다.
     이전에는 외부 서비스(Web3Forms)를 거쳤으나 수신이 누락되어 전환함. */

  var mdl=document.getElementById('mdl');
  if(mdl){
    var mdlT=document.getElementById('mdlT'), mdlD=document.getElementById('mdlD'),
        mdlF=document.getElementById('mdlF'), mdlMemo=document.getElementById('mdlMemo'),
        mdlPlan=document.getElementById('mdlPlan'), mdlMsg=document.getElementById('mdlMsg'),
        mdlGo=mdl.querySelector('.mdl-go'), lastFocus=null, mdlKind='contact';
    var COPY={
      deck:{t:'소개서 받기', d:'아래 정보를 남겨주시면 소개서를 이메일로 보내드립니다.', go:'소개서 받기', memo:false},
      contact:{t:'도입 문의하기', d:'아래 정보를 남겨주시면 담당자가 빠르게 연락드립니다.', go:'문의 보내기', memo:true}
    };
    function openMdl(kind,plan){
      mdlKind=kind; var c=COPY[kind]||COPY.contact;
      mdlT.textContent=c.t; mdlD.textContent=c.d; mdlGo.textContent=c.go;
      mdlMemo.hidden=!c.memo;
      if(plan){mdlPlan.hidden=false; mdlPlan.querySelector('b').textContent=plan}
      else mdlPlan.hidden=true;
      mdlMsg.hidden=true; mdlF.reset();
      lastFocus=document.activeElement;
      mdl.hidden=false; document.body.style.overflow='hidden';
      setTimeout(function(){var i=mdlF.querySelector('input');if(i)i.focus()},60);
    }
    function closeMdl(){
      mdl.hidden=true; document.body.style.overflow='';
      if(lastFocus&&lastFocus.focus)lastFocus.focus();
    }
    document.addEventListener('click',function(e){
      var t=e.target.closest('[data-modal]');
      if(t){e.preventDefault();openMdl(t.dataset.modal,t.dataset.plan||'');return}
      if(e.target.closest('[data-close]')) closeMdl();
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&!mdl.hidden) closeMdl();
    });
    function say(txt,ok){
      mdlMsg.hidden=false; mdlMsg.textContent=txt;
      mdlMsg.className='mdl-msg'+(ok?' ok':' err');
    }
    mdlF.addEventListener('submit',async function(e){
      e.preventDefault();
      if(!mdlF.checkValidity()){mdlF.reportValidity();return}

      /* 폼 값 수집 (한글 name → 내부 키) */
      var f={};
      new FormData(mdlF).forEach(function(v,k){if(k!=='동의')f[k]=(v||'').trim()});
      var company=f['회사명']||'', name=f['이름']||'', email=f['이메일']||'',
          phone=(f['연락처']||'').replace(/[^0-9]/g,''), department=f['부서']||'',
          position=f['직함']||'', message=f['문의내용']||'',
          plan=(!mdlPlan.hidden ? mdlPlan.querySelector('b').textContent : '');

      mdlGo.disabled=true; mdlGo.textContent='보내는 중…';
      function done(ok,msg){
        mdlGo.disabled=false; mdlGo.textContent=COPY[mdlKind].go;
        if(ok){say(msg||'접수되었습니다. 담당자가 빠르게 연락드리겠습니다.',true);
               mdlF.reset(); setTimeout(closeMdl,2400)}
        else{say(msg||'전송에 실패했습니다. __MAIL__ 로 보내주세요.',false)}
      }

      try{
        if(mdlKind==='deck'){
          /* ── 소개서 받기 → 소개서 PDF 자동 발송 API ── */
          var res=await fetch('/api/send-brochure',{
            method:'POST', headers:{'Content-Type':'application/json'},
            body:JSON.stringify({email:email, company:company, name:name,
              department:department, position:position, phone:phone, remarks:message, _hp:''})
          });
          var r=await res.json();
          if(r.success){
            logLead('소개서요청',{company:company, name:name, email:email, phone:phone,
              department:department, position:position});
            done(true,'소개서를 이메일로 보내드렸습니다. 메일함을 확인해주세요.');
          }else{ done(false, r.error); }
        }else{
          /* ── 도입 문의 → 자체 발송 API ── */
          var res2=await fetch('/api/send-contact',{
            method:'POST', headers:{'Content-Type':'application/json'},
            body:JSON.stringify({
              company:company, name:name, email:email, phone:f['연락처']||'',
              department:department, position:position, plan:plan, message:message, _hp:''
            })
          });
          var r2=await res2.json();
          if(r2.success){
            logLead('도입문의',{company:company, name:name, email:email, phone:phone,
              department:department, position:position, plan:plan, message:message});
            done(true);
          }else{ done(false, r2.error); }
        }
      }catch(err){
        done(false,'네트워크 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
      }
    });
  }

  frame();
})();
"""


# ── 운영 연동 블록 (SEO / 검색엔진 인증 / Schema.org / Favicon / Clarity) ──
#    ※ 실제 서비스 연동이므로 임의로 지우지 말 것.
SEO_HEAD = '<meta name="google-site-verification" content="DzKa9n_gNSL7cgofNCclCsIcJZ9DR7sMfHbndN2PE7I" />\n  <meta name="naver-site-verification" content="86171a58f78e357d53b482a7265c1a09e59316c1" />\n  <meta name="msvalidate.01" content="93A125744D27E4846DE5E2CE0517D791" />\n  <title>Bread&AI - B2B 영업, AI 세일즈 인텔리전스로 맞춤 제안하세요.</title>\n  <meta name="description" content="B2B 영업 준비를 자동화하는 AI 세일즈 인텔리전스, 맞춤 제안으로 더 많은 미팅과 매출 성과를 만듭니다">\n  <meta name="keywords" content="B2B 영업 AI, 맞춤 제안서 자동화, AI 세일즈, 콜드 이메일 AI, 영업 자동화, AI proposal generator, B2B sales automation">\n  <link rel="canonical" href="https://breadai.co.kr/">\n\n  <!-- Favicon (Bread&AI 로고) -->\n  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20width%3D\'160\'%20height%3D\'160\'%20viewBox%3D\'0%200%20160%20160\'%20fill%3D\'none\'%20xmlns%3D\'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg\'%3E%3Cpath%20d%3D\'M57.2554%2046.4758L152.412%207.25773L113.134%20104.577L113.364%2047.6204L55.0928%2047.3283L57.2554%2046.4758Z\'%20fill%3D\'%23CC7247\'%2F%3E%3Crect%20x%3D\'7.25775\'%20y%3D\'55.9175\'%20width%3D\'96.4948\'%20height%3D\'96.4948\'%20fill%3D\'%231A1A1A\'%2F%3E%3C%2Fsvg%3E">\n  <link rel="apple-touch-icon" href="data:image/svg+xml,%3Csvg%20width%3D\'160\'%20height%3D\'160\'%20viewBox%3D\'0%200%20160%20160\'%20fill%3D\'none\'%20xmlns%3D\'http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg\'%3E%3Crect%20width%3D\'160\'%20height%3D\'160\'%20fill%3D\'white\'%2F%3E%3Cpath%20d%3D\'M57.2554%2046.4758L152.412%207.25773L113.134%20104.577L113.364%2047.6204L55.0928%2047.3283L57.2554%2046.4758Z\'%20fill%3D\'%23CC7247\'%2F%3E%3Crect%20x%3D\'7.25775\'%20y%3D\'55.9175\'%20width%3D\'96.4948\'%20height%3D\'96.4948\'%20fill%3D\'%231A1A1A\'%2F%3E%3C%2Fsvg%3E">\n\n  <!-- Open Graph / SNS 공유용 -->\n  <meta property="og:type" content="website">\n  <meta property="og:title" content="B2B 영업 준비를 자동화하는 AI 세일즈 인텔리전스">\n  <meta property="og:description" content="맞춤 제안으로 더 많은 미팅과 매출 성과를 만듭니다">\n  <meta property="og:url" content="https://breadai.co.kr/">\n  <meta property="og:site_name" content="Bread&AI (브레드앤에이아이)">\n  <meta property="og:locale" content="ko_KR">\n  <meta property="og:image" content="https://breadai.co.kr/og-image.png">\n  <meta property="og:image:width" content="1200">\n  <meta property="og:image:height" content="630">\n\n  <!-- Twitter Card -->\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="B2B 영업 준비를 자동화하는 AI 세일즈 인텔리전스">\n  <meta name="twitter:description" content="맞춤 제안으로 더 많은 미팅과 매출 성과를 만듭니다">\n  <meta name="twitter:image" content="https://breadai.co.kr/og-image.png">\n\n  <!-- 구조화 데이터: Organization -->\n  <script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "SoftwareApplication",\n    "name": "Bread&AI (브레드앤에이아이)",\n    "alternateName": "브레드앤에이아이",\n    "url": "https://breadai.co.kr",\n    "applicationCategory": "BusinessApplication",\n    "operatingSystem": "Web",\n    "description": "브레드앤에이아이(Bread&AI)는 AI가 타겟 기업을 리서치하고 기업별 상황에 맞는 제안서와 이메일을 자동 생성하는 B2B 영업 AI 솔루션입니다. 맞춤 제안으로 미팅 전환율 향상.",\n    "offers": {\n      "@type": "Offer",\n      "price": "1000000",\n      "priceCurrency": "KRW",\n      "priceValidUntil": "2026-12-31",\n      "availability": "https://schema.org/InStock"\n    },\n    "provider": {\n      "@type": "Organization",\n      "name": "Bread&AI (브레드앤에이아이)",\n      "alternateName": "브레드앤에이아이",\n      "url": "https://breadai.co.kr",\n      "email": "contact@breadai.co.kr",\n      "foundingDate": "2025",\n      "description": "브레드앤에이아이(Bread&AI) — AI 세일즈 인텔리전스. B2B 영업의 Pre-sales 전체를 AI로 맞춤화하여 미팅 수를 늘리는 솔루션.",\n      "sameAs": []\n    },\n    "featureList": [\n      "타겟 기업 자동 발굴",\n      "AI 기업 리서치 및 Pain Point 분석",\n      "맞춤 콜드 이메일 자동 생성",\n      "기업별 맞춤 제안서 15-20장 자동 생성",\n      "맞춤 제안으로 미팅 전환율 30% 향상"\n    ]\n  }\n  </script>\n\n  <!-- 구조화 데이터: FAQ (검색결과 풍부한 표시용) -->\n  <script type="application/ld+json">\n  {\n    "@context": "https://schema.org",\n    "@type": "FAQPage",\n    "mainEntity": [\n      {\n        "@type": "Question",\n        "name": "Bread & AI는 어떤 솔루션인가요?",\n        "acceptedAnswer": {\n          "@type": "Answer",\n          "text": "Bread & AI는 B2B 영업의 Pre-sales 전체를 AI로 자동화하는 세일즈 인텔리전스 솔루션입니다. AI가 타겟 기업의 상황을 분석하고, 그에 맞는 제안서와 이메일을 자동 생성하여 미팅 전환율을 높입니다."\n        }\n      },\n      {\n        "@type": "Question",\n        "name": "기존 영업 방식과 무엇이 다른가요?",\n        "acceptedAnswer": {\n          "@type": "Answer",\n          "text": "기존에는 한 기업에 맞춤 제안을 준비하는 데 2-3시간이 걸려 대부분 같은 내용의 메일을 복사해 보냈습니다. Bread & AI는 AI가 타겟 기업의 현황, Pain Point, 최근 이슈를 자동 분석하고 기업 상황에 맞는 제안서와 이메일을 생성합니다."\n        }\n      },\n      {\n        "@type": "Question",\n        "name": "가격은 얼마인가요?",\n        "acceptedAnswer": {\n          "@type": "Answer",\n          "text": "Basic 플랜 월 100만원(3개월 단위 결제, 5인 기본), Pro 플랜 월 200만원(3개월 단위 결제, 10인 기본)부터 시작합니다. Enterprise는 맞춤 견적을 제공합니다."\n        }\n      }\n    ]\n  }\n  </script>\n\n  <!-- Microsoft Clarity -->\n  <script type="text/javascript">\n    (function(c,l,a,r,i,t,y){\n      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};\n      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;\n      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);\n    })(window, document, "clarity", "script", "vx5y6icwmu");\n  </script>\n  <link rel="preconnect" href="https://cdn.jsdelivr.net">'

CLARITY = '<script type="text/javascript">\n    (function(c,l,a,r,i,t,y){\n      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};\n      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;\n      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);\n    })(window, document, "clarity", "script", "vx5y6icwmu");\n  </script>'


def build(ab, hv="hero"):
    tracks_js = ""
    lf_js = "window.__LF=" + repr([[l[3], l[4], l[5], l[6]] for l in LOGOS]).replace("'", '"') + ";"

    body = (hero(ab, hv) + logo_wall(ab) + band() + why() + why_mobile_msg() + scenarios() + features()
            + genai()
            + impact(ab) + PRICING + ENDING + footer(ab) + MODAL)

    return ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n'
            '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            + SEO_HEAD + '\n'
            '<!-- 이 파일은 build.py 로 생성됩니다. 직접 수정하지 마세요. -->\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@700&'
            'family=Noto+Serif+KR:wght@600&display=swap" rel="stylesheet">\n'
            '<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/'
            'pretendardvariable-dynamic-subset.min.css" rel="stylesheet">\n'
            '<style>' + CSS + '</style>\n' + CLARITY + '\n</head>\n<body>\n'
            '<div class="prog" id="prog"></div>\n'
            '<nav id="nav"><div class="in">'
            '<a href="#top" class="brand"><img class="wm" src="assets/img/White@2x.png" alt="Bread&AI">'
            '<img class="dk" src="assets/img/logo-dark.png" alt="Bread&AI"></a>'
            '<div class="pills">' + nav_links(ab) + '</div>'
            '<div class="pills"><a class="mut" href="' + APP + '" target="_blank" rel="noopener">로그인</a>'
            '<a class="cta" href="' + APP + '" target="_blank" rel="noopener">무료로 시작하기</a></div>'
            ''
            '</div></nav>\n'
            + body +
            '\n<script>' + tracks_js + lf_js + JS.replace('__MAIL__', CONTACT_MAIL) + '</script>\n</body>\n</html>\n')


# (안, 파일명, 히어로 영상 키)
# 2026-08 기준 index.html 만 쓴다. 대안(a2)·B안(v2)은 필요할 때 ALL_VARIANTS=True 로 되살린다.
ALL_VARIANTS = False
OUTPUTS = [
    ("A", "index.html",     "hero-a1"),  # 채택 — 회의실 원테이크 (Pexels 7643320)
]
if ALL_VARIANTS:
    OUTPUTS += [
        ("A", "index-a2.html",  "hero-a2"),  # 대안 — 사람 없는 원목 데스크 (Pexels 15106918)
        ("B", "index-v2.html",  "hero-a1"),
    ]
for ab, fn, hv in OUTPUTS:
    p = os.path.join(OUT, fn)
    io.open(p, "w", encoding="utf-8", newline="\n").write(build(ab, hv))
    print("%s (%s안 · %s) %d bytes" % (fn, ab, hv, os.path.getsize(p)))
