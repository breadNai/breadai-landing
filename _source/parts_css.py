# -*- coding: utf-8 -*-
"""공통 CSS. A/B 차이는 build.py 에서 주입."""

CSS = r"""
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
:root{
  --paper:#FAF8F3; --paper2:#F3EFE6; --paper3:#EAE4D7; --surf:#FFFFFF;
  --ink:#1A1714; --ink2:#5A554B; --ink3:#8B857A; --ink4:#AFA99C;
  --line:#E7E1D4; --line2:#F0EBE0;
  --pet:#0E5766; --pet2:#0A414D; --petw:#E4EEF0; --petw2:#CFE2E6;
  --pos:#2C6B4F; --posw:#E7F0EA;
  --terra:#CC7247; --terraw:#F7EAE1;
  --f:'Pretendard Variable',Pretendard,'Noto Sans CJK KR',-apple-system,BlinkMacSystemFont,sans-serif;
  --fq:'Noto Sans','Noto Sans KR',Georgia,serif;
  --max:1200px; --e:cubic-bezier(.22,.68,.32,1);
  --s1:0 1px 2px rgba(26,23,20,.04),0 0 0 1px rgba(26,23,20,.05);
  --s2:0 2px 5px rgba(26,23,20,.03),0 12px 26px -12px rgba(26,23,20,.16),0 0 0 1px rgba(26,23,20,.05);
  --s3:0 5px 10px rgba(26,23,20,.04),0 30px 60px -22px rgba(26,23,20,.24),0 0 0 1px rgba(26,23,20,.06);
  --s4:0 10px 20px rgba(26,23,20,.05),0 56px 100px -30px rgba(26,23,20,.32),0 0 0 1px rgba(26,23,20,.07);
  --dot:radial-gradient(circle at 1px 1px, rgba(26,23,20,.30) 1px, transparent 0);
}
/* 안드로이드 Chrome 은 좁은 화면에서 작은 글자를 임의로 키운다(text autosizing).
   씬 목업의 5~9px 글자가 부풀어 표·본문이 겹치므로 반드시 꺼둔다. */
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{font-family:var(--f);background:var(--paper);color:var(--ink);line-height:1.65;letter-spacing:-.012em;
  word-break:keep-all;-webkit-font-smoothing:antialiased;overflow-x:clip}
::selection{background:var(--petw2);color:var(--pet2)}
a{color:inherit;text-decoration:none}
button{font-family:inherit;cursor:pointer;border:none;background:none;color:inherit}
img,video{display:block;max-width:100%}
.wrap{max-width:var(--max);margin:0 auto;padding:0 40px}
.wrapw{max-width:1360px;margin:0 auto;padding:0 40px}
h1,h2,h3{text-wrap:balance}
.rv{opacity:0;transform:translateY(22px);transition:opacity .85s var(--e),transform .85s var(--e)}
.rv.on{opacity:1;transform:none}
.d1{transition-delay:.09s}.d2{transition-delay:.18s}.d3{transition-delay:.27s}.d4{transition-delay:.36s}
.prog{position:fixed;top:0;left:0;height:2px;background:var(--pet);z-index:130;width:0}
.mob-only{display:none}
.dotbg{position:relative}
.dotbg::before{content:'';position:absolute;inset:0;background-image:var(--dot);background-size:22px 22px;
  opacity:1;pointer-events:none;
  -webkit-mask-image:radial-gradient(ellipse 78% 72% at 50% 46%,#000 18%,transparent 76%);
  mask-image:radial-gradient(ellipse 78% 72% at 50% 46%,#000 18%,transparent 76%)}
.dotbg > *{position:relative;z-index:1}

/* ══ NAV — Lassie식 필 메뉴 ══ */
nav{position:fixed;top:0;left:0;right:0;z-index:110;transition:background .35s var(--e),border-color .35s var(--e)}
nav .in{max-width:1360px;margin:0 auto;padding:0 32px;height:80px;display:grid;
  grid-template-columns:1fr auto 1fr;align-items:center;gap:18px}
nav .in > .pills:last-of-type{justify-self:end}
nav .in > .burger{justify-self:end}
nav.solid{background:rgba(250,248,243,.82);backdrop-filter:blur(18px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;flex:none}
.brand .wm{height:41px;width:auto;display:block;filter:drop-shadow(0 2px 12px rgba(0,0,0,.45))}
.brand .dk{display:none;height:41px;width:auto}
nav.solid .brand .wm{display:none}
nav.solid .brand .dk{display:block}
.pills{display:flex;gap:6px;align-items:center}
.pills a{background:rgba(255,255,255,.95);color:var(--ink);padding:10px 17px;border-radius:12px;
  font-size:14.5px;font-weight:600;letter-spacing:-.02em;white-space:nowrap;
  box-shadow:0 2px 10px rgba(20,16,12,.10);transition:.2s var(--e)}
.pills a:hover{background:#fff;transform:translateY(-1px)}
.pills a.mut{background:rgba(255,255,255,.40);color:#fff;backdrop-filter:blur(10px);box-shadow:none}
nav.solid .pills a.mut{background:rgba(26,23,20,.07);color:var(--ink2);backdrop-filter:none}
.pills a.cta{background:var(--ink);color:#fff}
.pills a.cta:hover{background:#332D25}
nav.solid .pills a{box-shadow:0 1px 3px rgba(20,16,12,.07),inset 0 0 0 1px var(--line)}
nav.solid .pills a.cta{box-shadow:none}
nav.dark .pills a.cta{background:#fff;color:var(--ink)}
nav.dark .pills a.mut{background:rgba(255,255,255,.16);color:#fff}
.burger{display:none;flex-direction:column;gap:5px;padding:10px;border-radius:11px;background:rgba(255,255,255,.95);box-shadow:0 2px 10px rgba(20,16,12,.10)}
.burger i{width:18px;height:1.7px;background:var(--ink);display:block;border-radius:2px}

/* ══ HERO ══ */
.heroWrap{position:relative;height:calc(100svh + 86vh);background:var(--paper)}
.hero{position:sticky;top:0;height:100svh;display:flex;flex-direction:column;align-items:center;
  justify-content:center;text-align:center;overflow:hidden;color:#fff;padding:300px 0 40px}
.film{position:absolute;inset:var(--fi,0px);overflow:hidden;background:#141210;border-radius:var(--fr,0px)}
/* 카피 가독성을 위해 영상은 충분히 어둡게 — 비즈니스 미팅의 '분위기'만 남긴다 */
.film video,.film .still{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  filter:brightness(.40) saturate(.72) contrast(1.08)}
@media (max-width:760px){.film video{object-position:64% 50%}}
.scrim{position:absolute;inset:0;background:
  linear-gradient(180deg,rgba(10,8,6,.5) 0%,rgba(10,8,6,.2) 24%,rgba(10,8,6,.08) 45%),
  linear-gradient(0deg,rgba(10,8,6,.68) 0%,rgba(10,8,6,.4) 28%,rgba(10,8,6,.16) 58%),
  linear-gradient(90deg,rgba(10,8,6,.44) 0%,rgba(10,8,6,.12) 46%,transparent 70%)}
.halo{position:absolute;left:50%;top:62%;transform:translate(-50%,-50%);width:min(1180px,94vw);height:min(560px,64vh);
  background:radial-gradient(ellipse at center,rgba(10,8,6,.50) 0%,rgba(10,8,6,.28) 48%,transparent 76%);
  filter:blur(2px);pointer-events:none}
.hero-in{position:relative;z-index:3;max-width:var(--max);margin:0 auto;padding:0 40px;width:100%;
  opacity:var(--ho,1);transform:translateY(calc(var(--hy,0) * -1px))}
.hero h1{font-size:clamp(33px,4.35vw,61px);font-weight:800;letter-spacing:-.055em;line-height:1.14;max-width:26ch;margin:0 auto;
  text-shadow:0 1px 2px rgba(0,0,0,.5),0 3px 22px rgba(0,0,0,.55),0 0 72px rgba(0,0,0,.4)}
.hero h1 .ln{display:block;overflow:hidden}
.hero h1 .ln b{display:block;font-weight:inherit;transform:translateY(112%);opacity:0;
  animation:h1Up 1.05s cubic-bezier(.16,.9,.24,1) forwards}
.hero h1 .l1 b{animation-delay:.25s}
.hero h1 .l2 b{animation-delay:.46s}
@keyframes h1Up{to{transform:none;opacity:1}}
.hero h1 .l{font-weight:450;letter-spacing:-.04em;color:#fff;margin-top:8px;
  text-shadow:0 1px 2px rgba(0,0,0,.55),0 3px 24px rgba(0,0,0,.6),0 0 80px rgba(0,0,0,.45)}
.hero .roll,.hero .hero-cta,.hero .hero-note{opacity:0;animation:h1Fade .9s var(--e) .95s forwards}
@keyframes h1Fade{to{opacity:1}}
/* 고정줄 + 롤링줄 */
.roll{margin-top:144px;display:flex;flex-direction:column;align-items:center;gap:8px}
.roll-f{font-size:15px;font-weight:600;color:rgba(255,255,255,.88);letter-spacing:-.02em;
  text-shadow:0 2px 14px rgba(0,0,0,.55)}
.roll-t{position:relative;height:32px;width:100%}
.rk{position:absolute;left:50%;top:0;transform:translateX(-50%) translateY(14px);opacity:0;
  display:flex;align-items:center;gap:10px;font-size:clamp(16px,1.68vw,19.5px);font-weight:700;letter-spacing:-.038em;
  color:#fff;white-space:nowrap;transition:opacity .6s var(--e),transform .6s var(--e);
  text-shadow:0 2px 16px rgba(0,0,0,.6)}
.rk.on{opacity:1;transform:translateX(-50%) translateY(0)}
.rk .pic{width:26px;height:26px;border-radius:8px;background:rgba(255,255,255,.20);border:1px solid rgba(255,255,255,.3);
  backdrop-filter:blur(8px);display:flex;align-items:center;justify-content:center;flex:none}
.rk .pic svg{width:14px;height:14px;stroke:#fff}
.hero-note{display:inline-flex;align-items:center;gap:8px;margin-top:26px;font-size:13.5px;font-weight:600;
  color:rgba(255,255,255,.86);text-shadow:0 2px 12px rgba(0,0,0,.6);
  border-bottom:1px solid rgba(255,255,255,.32);padding-bottom:3px;transition:.2s var(--e)}
.hero-note:hover{color:#fff;border-bottom-color:#fff}
.hero-note svg{width:16px;height:16px;flex:none}
.hero-cta{display:flex;gap:12px;margin-top:36px;flex-wrap:wrap;justify-content:center;align-items:center}
.tip{position:relative;display:inline-flex}
.tip::after{content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 12px);
  transform:translateX(-50%) translateY(5px);white-space:nowrap;
  background:var(--pet);color:#fff;font-size:13px;font-weight:700;letter-spacing:-.02em;
  padding:9px 15px;border-radius:10px;box-shadow:0 12px 28px -8px rgba(14,87,102,.65);
  opacity:0;pointer-events:none;transition:opacity .22s var(--e),transform .22s var(--e);z-index:20}
.tip::before{content:'';position:absolute;left:50%;bottom:calc(100% + 7px);
  transform:translateX(-50%) translateY(5px) rotate(45deg);width:10px;height:10px;background:var(--pet);
  border-radius:2px;opacity:0;pointer-events:none;transition:opacity .22s var(--e),transform .22s var(--e);z-index:20}
.tip:hover::after,.tip:hover::before{opacity:1;transform:translateX(-50%) translateY(0)}
.tip:hover::before{transform:translateX(-50%) translateY(0) rotate(45deg)}
/* 엔딩 CTA 툴팁은 위 문구를 가리지 않도록 버튼 아래로.
   컬러는 히어로와 같은 페트롤 — 테라코타는 실제 CTA에만 쓴다.
   테라코타로 바꾸려면 아래 두 줄의 var(--pet)을 var(--terra)로. */
.end .tip::after{top:calc(100% + 12px);bottom:auto;transform:translateX(-50%) translateY(-5px);
  background:var(--pet);box-shadow:0 12px 28px -8px rgba(14,87,102,.6)}
.end .tip::before{top:calc(100% + 7px);bottom:auto;
  transform:translateX(-50%) translateY(-5px) rotate(45deg);background:var(--pet)}
.end .tip:hover::after{transform:translateX(-50%) translateY(0)}
.end .tip:hover::before{transform:translateX(-50%) translateY(0) rotate(45deg)}
.hero-cta .btn{padding:17px 34px;font-size:16.5px;border-radius:13px;font-weight:700;min-width:206px}
.btn{font-size:15px;font-weight:700;padding:11px 20px;border-radius:9px;transition:.2s var(--e);
  display:inline-block;text-align:center;letter-spacing:-.018em;white-space:nowrap}
.btn-d{background:var(--ink);color:var(--paper)}.btn-d:hover{background:#332D25}
.btn-p{background:var(--pet);color:#fff}.btn-p:hover{background:var(--pet2)}
.btn-o{background:var(--surf);color:var(--ink);box-shadow:inset 0 0 0 1px var(--paper3),0 1px 2px rgba(26,23,20,.04)}
.btn-o:hover{box-shadow:inset 0 0 0 1px var(--ink3)}
.btn-w{background:#fff;color:var(--ink);box-shadow:0 8px 26px -10px rgba(0,0,0,.5)}
.btn-w:hover{background:#F2EDE3}
.btn-glass{color:#fff;background:rgba(255,255,255,.16);backdrop-filter:blur(12px);
  box-shadow:inset 0 0 0 1.4px rgba(255,255,255,.55)}
.btn-glass:hover{background:rgba(255,255,255,.28)}

/* ══ 로고월 (Ramp식 셀) ══ */
.lwall{padding:96px 0 0;background:var(--paper)}
.lgrid{display:grid;border-top:1px solid var(--line);border-left:1px solid var(--line)}
.lgrid.a{grid-template-columns:repeat(6,minmax(0,1fr));border-bottom:1px solid var(--line)}
.lgrid.b{grid-template-columns:repeat(3,minmax(0,1fr)) minmax(0,1.25fr);border-bottom:1px solid var(--line)}
.lcell{border-right:1px solid var(--line);border-bottom:1px solid var(--line);min-height:132px;
  display:flex;align-items:center;justify-content:center;position:relative;transition:background .25s var(--e);cursor:default}
.lgrid.a .lcell{border-bottom:none}
.lcell:hover{background:var(--surf)}
.lcell .lg{width:auto;opacity:.38;filter:grayscale(1) contrast(.9);transition:opacity .25s var(--e),filter .25s var(--e)}
.lcell:hover .lg{opacity:.85;filter:grayscale(1) contrast(1)}
.lcell .arw{position:absolute;top:12px;right:14px;font-size:12px;color:var(--ink4);opacity:0;transition:opacity .25s var(--e)}
.lcell:hover .arw{opacity:1}
.lcell::after{content:'';position:absolute;right:-3.5px;bottom:-3.5px;width:6px;height:6px;transform:rotate(45deg);
  background:var(--paper);border:1px solid var(--line);z-index:2}
.lgrid.b .lfeat{grid-column:4;grid-row:1/span 2}
.lfeat{border-right:1px solid var(--line);border-bottom:1px solid var(--line);position:relative;
  overflow:hidden;min-height:264px;display:flex;flex-direction:column;justify-content:flex-end;padding:26px;color:#fff}
.lfeat .bg{position:absolute;inset:0;background:linear-gradient(150deg,#5C7364,#2F4A46 48%,#1E2C2B);transition:opacity .4s var(--e)}
.lfeat .bg::after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(10,14,13,.72),transparent 62%)}
.lfeat .in{position:relative;z-index:2}
.lfeat .who{font-size:12.5px;font-weight:700;opacity:.82;letter-spacing:-.01em}
.lfeat .num{font-size:clamp(38px,4vw,54px);font-weight:800;letter-spacing:-.06em;line-height:1;margin-top:10px}
.lfeat .cap{font-size:14px;opacity:.76;margin-top:8px}
.lfeat .arw2{position:absolute;top:20px;right:22px;z-index:2;width:28px;height:28px;border-radius:50%;
  background:rgba(255,255,255,.9);color:var(--ink);display:flex;align-items:center;justify-content:center;font-size:13px}
.lfeat .fimg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:48% 16%;z-index:1}
.lfeat .fimg + .ph{display:none}
.lfeat .ph{position:absolute;inset:0;display:flex;align-items:flex-start;justify-content:center;
  padding-top:64px;font-size:12px;color:rgba(255,255,255,.45);z-index:1}
.lfeat .bg{z-index:0}
.lfeat::after{content:'';position:absolute;inset:0;z-index:1;
  background:linear-gradient(0deg,rgba(10,14,13,.82),rgba(10,14,13,.15) 52%,transparent 78%)}

/* ══ 카운터 띠 배너 ══ */
.band{border-top:1px solid var(--line);border-bottom:1px solid var(--line);background:var(--paper);overflow:hidden}
.band-in{max-width:1360px;margin:0 auto;padding:0 40px;height:62px;display:flex;align-items:center;gap:30px;
  justify-content:center;overflow-x:auto;scrollbar-width:none;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 40px,#000 calc(100% - 40px),transparent);
  mask-image:linear-gradient(90deg,transparent,#000 40px,#000 calc(100% - 40px),transparent)}
.band-in::-webkit-scrollbar{display:none}
.band-l{display:flex;align-items:center;gap:9px;font-size:12px;font-weight:800;letter-spacing:.04em;
  color:var(--ink);white-space:nowrap;flex:none}
.band-l i{width:7px;height:7px;border-radius:50%;background:var(--pos);flex:none;animation:pulse 2.2s infinite}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.45;transform:scale(.8)}}
.bs{display:flex;align-items:center;gap:10px;font-size:12px;font-weight:700;color:var(--ink3);
  letter-spacing:.02em;white-space:nowrap;flex:none}
.bs em{font-style:normal;font-size:13.5px;font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums;
  background:var(--paper2);border:1px solid var(--line);border-radius:7px;padding:3px 9px;min-width:64px;text-align:right}
.band-d{font-size:11.5px;font-weight:600;color:var(--ink4);white-space:nowrap;flex:none;letter-spacing:0}

/* ══ 공통 섹션 ══ */
section.s{padding:150px 0}
.head{max-width:720px;margin:0 auto 64px;text-align:center}
.head h2{font-size:clamp(29px,3.5vw,45px);font-weight:800;letter-spacing:-.05em;line-height:1.24}
.head h2 .q{color:var(--pet)}
.head p{font-size:18px;color:var(--ink2);line-height:1.74;margin-top:20px}
.head p b{font-weight:800;color:var(--ink)}

/* ══ WHY — 핀 + 카드 스택 ══ */
.why{position:relative;background:var(--paper2);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.why-st{position:sticky;top:0;height:100svh;display:flex;flex-direction:column;justify-content:center;overflow:hidden;padding:96px 0 40px}
.why-h{max-width:var(--max);margin:0 auto 36px;padding:0 40px;text-align:center;width:100%}
.why-h h2{font-size:clamp(26px,3.2vw,42px);font-weight:800;letter-spacing:-.05em;line-height:1.26}
.why-h h2 .q{color:var(--pet)}
.why-h p{font-size:16.5px;color:var(--ink2);margin-top:14px}
.lg.up{position:relative;top:-5px}
.why-stage{position:relative;max-width:1040px;width:100%;margin:0 auto;padding:0 40px;height:min(390px,45vh)}
.wc{position:absolute;left:40px;right:40px;top:0;height:100%;background:var(--surf);border-radius:24px;
  box-shadow:var(--s3);overflow:hidden;display:grid;grid-template-columns:minmax(0,1.24fr) minmax(0,.76fr);
  transform:translateY(100%);opacity:0;transition:transform .7s var(--e),opacity .7s var(--e);will-change:transform}
.wc-l{padding:36px 40px;display:flex;flex-direction:column;justify-content:center;
  align-items:center;text-align:center;position:relative}
.wcb{position:relative;width:100%}
/* 1번 카드 — 헤드라인 문장의 좌상/우하에 모퉁이 꺽쇠 (문장과 넉넉히 띄운다) */
.wcb.brk h3{position:relative;padding:6px 0}
.wcb.brk h3::before,.wcb.brk h3::after{content:'';position:absolute;width:26px;height:26px;
  border-color:rgba(26,23,20,.2);border-style:solid}
.wcb.brk h3::before{left:-18px;top:-8px;border-width:2.5px 0 0 2.5px}
.wcb.brk h3::after{right:-18px;bottom:-8px;border-width:0 2.5px 2.5px 0}
.wc .no{font-size:15.5px;font-weight:800;color:var(--terra);letter-spacing:.01em;margin-bottom:14px}
.wc h3{font-size:clamp(25px,3.05vw,38px);font-weight:800;letter-spacing:-.052em;line-height:1.3;margin-bottom:16px}
/* 따옴표만 Noto Sans — 글자는 기존 폰트 그대로 */
.wc h3 .qo,.wc h3 .qc{font-family:var(--fq);font-style:normal;font-weight:700;
  color:var(--ink4);line-height:0;position:relative;top:.12em}
.wc h3 .qo{margin-right:.2em}
.wc h3 .qc{margin-left:.2em}
.wc h3 .qm{color:var(--terra)}
.wc[data-i="0"] h3 .qm{color:#3F6150}
.wc[data-i="1"] h3 .qm{color:#96742F}
.wc[data-i="2"] h3 .qm{color:#3D6673}
.wc[data-i="3"] h3 .qm{color:#8A6247}
.wc[data-i="4"] h3 .qm{color:var(--pet)}
.wc p{font-size:16.5px;color:#4A4640;line-height:1.76}
.wc-r{position:relative;overflow:hidden}
.wc-r .gfx{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.wc-r .gfx svg{opacity:0;transform:scale(.9) translateY(10px);
  transition:opacity .75s var(--e) .12s,transform .75s var(--e) .12s}
.wc.cur .wc-r .gfx svg{opacity:1;transform:none;animation:gfxfloat 6s ease-in-out 1s infinite}
@keyframes gfxfloat{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-9px) rotate(-.5deg)}}
.wc-r .gfx svg{width:72%;height:72%}
.wc-r.ph img{width:100%;height:100%;object-fit:cover;display:block}
.g0{background:linear-gradient(140deg,#D3DCD2,#93A697 44%,#55705F)}
.g1{background:linear-gradient(140deg,#E7D9BE,#C6B491 46%,#9E8E72)}
.g2{background:linear-gradient(140deg,#CFDCDF,#8FB0B8 44%,#4E7480)}
.g3{background:linear-gradient(140deg,#E9DED2,#CDB9A8 46%,#A78A73)}
.g4{background:linear-gradient(140deg,#2A5C68,#0E5766 46%,#08333D)}
.wc.need .wc-l{background:linear-gradient(152deg,#F2F6F1,#DFE8DE)}
.wc.need .no{color:#3F6150}
.wc[data-i="1"] .no{color:#96742F}
.wc[data-i="2"] .no{color:#3D6673}
.wc[data-i="3"] .no{color:#8A6247}
.wc[data-i="4"] .no{color:var(--pet)}
/* 마지막 요약 카드의 도입부는 결론 문장이므로 조금 크게 */
.wc.ans .no{font-size:19px;margin-bottom:16px}
/* WHY 도형 애니메이션 (활성 카드에서만) */
.gx{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.gx svg{width:72%;height:72%}
/* 0) 일반 메일은 가라앉고, custom 제안 메일은 올라가 계속 떠 있는다 */
.gx0{gap:9%;align-items:center}
.gx0 .env{width:37%;position:relative}
.wc-r .gfx .gx0 .ev{width:100%;height:auto}
.wc.cur .wc-r .gfx .gx0 .ev{animation:none;transform:none}
.gx0 .ev{width:100%;height:auto;display:block}
.gx0 .bdg{position:absolute;top:-16px;left:50%;transform:translateX(-50%);white-space:nowrap;
  font-size:11px;font-weight:800;letter-spacing:.02em;padding:4px 11px;border-radius:7px;
  background:#fff;color:#2F5544}
.wc.cur .gx0 .a{animation:mSink 1.1s var(--e) .3s forwards}
.wc.cur .gx0 .b{animation:mRise 1.1s var(--e) .3s forwards,mFloat 3.6s ease-in-out 1.4s infinite}
@keyframes mSink{to{transform:translateY(26px);opacity:.38}}
@keyframes mRise{to{transform:translateY(-30px)}}
@keyframes mFloat{0%,100%{transform:translateY(-30px)}50%{transform:translateY(-39px)}}
/* 1) 시계 */
.gx1 .hnd{transform-origin:100px 100px}
.wc.cur .gx1 .hnd.m{animation:spin 5s linear infinite}
.wc.cur .gx1 .hnd.h{animation:spin 60s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
/* 2) 여러 공이 몰려오지만 한둘만 통과 */
.gx2 .bl{position:absolute;width:15px;height:15px;border-radius:50%;background:rgba(255,255,255,.75);
  top:14%;opacity:0}
.wc.cur .gx2 .bl{animation:crowd 4s ease-in-out infinite}
.gx2 .q1{left:24%}.gx2 .q2{left:33%}.gx2 .q3{left:42%}.gx2 .q4{left:50%}
.gx2 .q5{left:58%}.gx2 .q6{left:67%}.gx2 .q7{left:76%}
.wc.cur .gx2 .q2{animation-delay:.12s}.wc.cur .gx2 .q3{animation-delay:.24s}
.wc.cur .gx2 .q4{animation-delay:.36s}.wc.cur .gx2 .q5{animation-delay:.48s}
.wc.cur .gx2 .q6{animation-delay:.6s}.wc.cur .gx2 .q7{animation-delay:.72s}
@keyframes crowd{0%{opacity:0;top:8%}12%{opacity:1}
 42%{opacity:1;top:40%;left:50%}55%{opacity:.25;top:44%;left:50%}
 70%,100%{opacity:0;top:44%;left:50%}}
.gx2 .pass{position:absolute;left:50%;top:44%;width:24px;height:24px;border-radius:50%;
  background:#fff;transform:translateX(-50%);opacity:0}
.wc.cur .gx2 .pass{animation:through 4s ease-in-out infinite}
.wc.cur .gx2 .p2{animation-delay:2s}
@keyframes through{0%,30%{opacity:0;top:44%}45%{opacity:1;top:52%}
 75%{opacity:1;top:84%;transform:translateX(-50%) scale(.85)}100%{opacity:0;top:90%}}
/* 3) 같은 소개서가 하나씩 붙는다 */
.gx3{align-items:center;justify-content:center}
.gx3 .pg{position:absolute;width:30%;aspect-ratio:3/4;border-radius:9px;
  border:2px solid rgba(255,255,255,.5);background:rgba(255,255,255,.10)}
.gx3 .pg em{position:absolute;left:9%;top:7%;font-style:normal;font-size:10px;font-weight:800;
  letter-spacing:-.01em;color:rgba(255,255,255,.88);white-space:nowrap}
.gx3 .p1{transform:translate(-48px,-18px)}
.gx3 .p2{transform:translate(-16px,-6px);opacity:0}
.gx3 .p3{transform:translate(16px,6px);opacity:0}
.gx3 .p4{transform:translate(48px,18px);opacity:0}
.wc.cur .gx3 .p2{animation:attach 4.5s ease-out infinite}
.wc.cur .gx3 .p3{animation:attach2 4.5s ease-out infinite}
.wc.cur .gx3 .p4{animation:attach3 4.5s ease-out infinite}
@keyframes attach{0%,10%{opacity:0;transform:translate(80px,60px)}
 24%,100%{opacity:1;transform:translate(-16px,-6px)}}
@keyframes attach2{0%,26%{opacity:0;transform:translate(96px,72px)}
 42%,100%{opacity:1;transform:translate(16px,6px)}}
@keyframes attach3{0%,44%{opacity:0;transform:translate(112px,84px)}
 60%,100%{opacity:1;transform:translate(48px,18px)}}
/* 4) 하나의 제안이 여러 기업으로 */
.gx4 .ray{stroke-dasharray:170;stroke-dashoffset:170}
.cur .gx4 .ray{animation:draw 1s ease-out forwards}
.cur .gx4 .r1{animation-delay:.3s}
.cur .gx4 .r2{animation-delay:.5s}
.cur .gx4 .r3{animation-delay:.7s}
.gx4 .tgt{opacity:0}
.cur .gx4 .tgt{animation:popIn .5s ease-out forwards}
.cur .gx4 .t1{animation-delay:1.2s}
.cur .gx4 .t2{animation-delay:1.4s}
.cur .gx4 .t3{animation-delay:1.6s}
@keyframes popIn{to{opacity:1}}

/* ══ 시나리오 2카드 ══ */
.sgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.scard{text-align:left;border-radius:26px;padding:0;position:relative;overflow:hidden;
  display:flex;flex-direction:column;transition:.35s var(--e);box-shadow:var(--s2)}
.sph{display:block;position:relative;aspect-ratio:1000/560;overflow:hidden;flex:none}
.sph img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--e)}
.scard:hover .sph img{transform:scale(1.035)}
.sph::after{content:'';position:absolute;inset:0}
.scard.sa .sph::after{background:linear-gradient(180deg,rgba(253,244,235,0) 55%,rgba(253,244,235,.9))}
.scard.sb .sph::after{background:linear-gradient(180deg,rgba(18,38,44,.1) 45%,rgba(31,69,80,.94))}
.sbody{padding:28px 36px 34px;display:flex;flex-direction:column;flex:1}
.scard:hover{transform:translateY(-5px);box-shadow:var(--s3)}
.scard.sa{background:linear-gradient(178deg,#FDF4EB,#F3DFCC)}
.scard.sb{background:linear-gradient(155deg,#1F4550,#12262C);color:#fff}
.scard .tag{display:inline-flex;align-items:center;gap:7px;font-size:12.5px;font-weight:800;letter-spacing:.02em;
  padding:6px 12px;border-radius:8px;background:rgba(204,114,71,.14);color:#A9552C;width:max-content;margin-bottom:18px}
.scard.sb .tag{background:rgba(127,196,210,.16);color:#9FD8E4}
.scard h3{font-size:clamp(23px,2.6vw,32px);font-weight:800;letter-spacing:-.05em;line-height:1.3;margin-bottom:16px}
.scard p{font-size:15.5px;line-height:1.8;color:var(--ink2)}
.scard.sb p{color:rgba(255,255,255,.72)}
.scard .pick{margin-top:auto;padding-top:24px;display:flex;align-items:center;gap:8px;
  font-size:15px;font-weight:800;color:#A9552C}
.scard.sb .pick{color:#9FD8E4}
.scard .pick svg{width:16px;height:16px;transition:transform .3s var(--e)}
.scard:hover .pick svg{transform:translateX(4px)}
/* 카드 내부 미니 UI 애니메이션 */
.mini{margin:22px 0 4px;border-radius:14px;padding:13px;background:rgba(255,255,255,.8);
  box-shadow:inset 0 0 0 1px rgba(26,23,20,.07);display:flex;flex-direction:column;gap:7px}
.mhd{font-size:11.5px;font-weight:800;letter-spacing:.03em;color:var(--ink3);padding:1px 2px 3px}
.scard.sb .mhd{color:rgba(255,255,255,.5)}
.scard.sb .mini{background:rgba(255,255,255,.07);box-shadow:inset 0 0 0 1px rgba(255,255,255,.12)}
.mrow{display:flex;align-items:center;gap:10px;font-size:13px;color:var(--ink2);
  background:#fff;border-radius:9px;padding:9px 11px;box-shadow:0 1px 2px rgba(26,23,20,.05);
  opacity:0;transform:translateY(7px)}
.scard.sb .mrow{background:rgba(255,255,255,.09);color:rgba(255,255,255,.86);box-shadow:none}
.in-view .mrow{animation:pop .6s var(--e) forwards}
.in-view .mrow:nth-child(1){animation-delay:.15s}
.in-view .mrow:nth-child(2){animation-delay:.75s}
.in-view .mrow:nth-child(3){animation-delay:1.35s}
.in-view .mrow:nth-child(4){animation-delay:1.95s}
.in-view .mrow:nth-child(5){animation-delay:2.55s}
@keyframes pop{to{opacity:1;transform:none}}
.mrow b{margin-left:auto;font-variant-numeric:tabular-nums;font-weight:800;color:#A9552C;font-size:12.5px}
.scard.sb .mrow b{color:#9FD8E4}
.mrow .dt{width:7px;height:7px;border-radius:50%;background:var(--terra);flex:none;opacity:.7}
.scard.sb .mrow .dt{background:#9FD8E4}
.typ{font-size:13px;color:var(--ink3);display:flex;align-items:center;gap:8px}
.scard.sb .typ{color:rgba(255,255,255,.6)}
.typ .cur{display:inline-block;width:1.5px;height:14px;background:currentColor;animation:blink 1s steps(2) infinite}
@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}

/* ══ 프로세스 — 핀 + 스크롤로 단계 이동 · 3D 개념 애니메이션 ══ */
/* 레퍼런스: Runway(양끝 탭 + 큰 사이드바) / Ramp(입체 산개 카드) / Attio(멀티 윈도우) */
.proc{position:relative;background:var(--paper2);border-top:1px solid var(--line)}
.proc-st{position:sticky;top:0;height:100svh;display:flex;flex-direction:column;
  justify-content:center;overflow:hidden;padding:130px 0 120px}
.proc-h{max-width:var(--max);margin:0 auto;padding:0 40px;width:100%;text-align:center}
.proc-h h2{font-size:clamp(28px,3.9vw,50px);font-weight:800;letter-spacing:-.05em;line-height:1.2}
.proc-h h2 .q{color:var(--pet)}
.why-h h2 .q{color:var(--pet)}

/* ── 시나리오 탭 : 중앙 정렬 세그먼트 필 — 두 트랙을 한눈에, 색으로 구분 ── */
.trk{width:fit-content;margin:36px auto 0;display:flex;gap:4px;background:var(--surf);
  border-radius:999px;padding:5px;box-shadow:inset 0 0 0 1px var(--line)}
.trk button{font-size:clamp(14px,1.15vw,16.5px);font-weight:800;letter-spacing:-.03em;
  color:var(--ink3);cursor:pointer;transition:background .35s var(--e),color .35s var(--e);
  white-space:nowrap;flex:none;border-radius:999px;padding:12px 24px}
.trk button:nth-child(1).on{background:var(--terra);color:#fff}
.trk button:nth-child(2).on{background:var(--pet);color:#fff}
/* 비활성 탭도 누를 수 있다는 것을 알아채도록 은은한 넛지 애니메이션 */
.trk button:not(.on){animation:tabNudge 2.6s ease-in-out infinite}
.trk button:not(.on):hover,.trk button:not(.on):focus-visible{
  color:var(--ink2);animation-play-state:paused}
@keyframes tabNudge{0%,44%,100%{transform:translateX(0)}22%{transform:translateX(4px)}}

/* ── 좌우가 바뀌는 레이아웃 (Case 1: 사이드바 좌 / Case 2: 사이드바 우) ── */
.proc-b{max-width:var(--max);margin:34px auto 0;padding:0 40px;width:100%;
  display:grid;grid-template-columns:minmax(0,374px) minmax(0,1fr);gap:40px;align-items:center;
  transform:translateX(var(--sx,0));opacity:1}
.proc-b.sw-out{transform:translateX(var(--sx,0));opacity:0;
  transition:transform .3s cubic-bezier(.5,0,.9,.4),opacity .28s linear}
.proc-b.sw-in{transition:transform .6s cubic-bezier(.16,.86,.28,1),opacity .42s var(--e)}
.proc[data-track="1"] .proc-b{grid-template-columns:minmax(0,1fr) minmax(0,374px)}
.fnav{position:relative;text-align:left;order:1}
.fstage{order:2}
.proc[data-track="1"] .fnav{order:2}
.proc[data-track="1"] .fstage{order:1}

.fnavt{display:none;flex-direction:column;gap:16px}
.fnavt.on{display:flex}
/* 가치 약속 문장만 — 한 줄에 들어가도록 자간·크기 조절. 설명은 화면 하단 자막으로 */
.fb{cursor:pointer;font-size:clamp(17.6px,1.7vw,23px);font-weight:800;letter-spacing:-.052em;
  line-height:1.68;color:#C6BFB4;transition:color .45s var(--e);white-space:nowrap}
.fb .t{transition:color .45s var(--e)}
.fb.on{color:var(--ink)}
/* 단계가 활성화되면 핵심 워딩에 형광펜이 그어진다 — 트랙1 주황, 트랙2 틸 블루.
   background-size 로 그리므로 z-index 스택 문제 없이 PC·모바일 모두 동일하게 동작한다. */
.fb .t em{font-style:normal;background-repeat:no-repeat;background-position:0 86%;
  background-size:0% 40%;transition:background-size .72s cubic-bezier(.5,.05,.3,1) .18s}
.fb.on .t em{background-size:100% 40%}
.fnavt[data-t="0"] .fb .t em,.mtrk[data-t="0"] .fb .t em{
  background-image:linear-gradient(rgba(204,114,71,.38),rgba(204,114,71,.38))}
.fnavt[data-t="1"] .fb .t em,.mtrk[data-t="1"] .fb .t em{
  background-image:linear-gradient(rgba(31,116,133,.32),rgba(31,116,133,.32))}
.proc[data-track="1"] .fnav{text-align:right}

/* ── 스테이지 : 바탕은 흰색. 대비는 카드 쪽에 컬러를 줘서 만든다 ── */
.fstage{position:relative;aspect-ratio:16/9;border-radius:20px;overflow:hidden;
  box-shadow:var(--s3);background:linear-gradient(160deg,#FFFFFF,#FCFAF6 62%,#F7F2EA);
  border:1px solid var(--line)}
.ftrack{position:absolute;inset:0;opacity:0;pointer-events:none;transition:opacity .3s var(--e)}
.ftrack.on{opacity:1;pointer-events:auto}
.fpane{position:absolute;inset:0;opacity:0;transform:scale(1.02);
  transition:opacity .5s var(--e),transform .6s var(--e)}
.fpane.on{opacity:1;transform:none}
.sc{position:absolute;inset:0}
.fpane.on .sc{animation:scZoom 5.4s var(--e) forwards}
@keyframes scZoom{from{transform:scale(1)}to{transform:scale(1.035)}}
.stg3{position:absolute;inset:0;perspective:1000px;transform-style:preserve-3d}
/* 화면 내 하단 자막 */
.sub{position:absolute;left:6%;right:6%;bottom:5%;text-align:center;font-size:13.5px;
  color:var(--ink2);letter-spacing:-.02em;line-height:1.5;opacity:0;z-index:6}
.sub b{font-weight:800;color:var(--ink)}
.fpane.on .sub{animation:fadeUp .7s var(--e) 1.2s forwards}
@keyframes fadeUp{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:none}}
@keyframes pop2{from{opacity:0;transform:translateY(12px) scale(.94)}to{opacity:1;transform:none}}
@keyframes typeIn{from{max-width:0}to{max-width:100%}}
@keyframes wIn{to{opacity:1}}

/* ── 회사 소개서 표지 (샘플) — 16:9 PPT 비율, 틸블루 ── */
.cov{position:relative;width:100%;height:100%;border-radius:8px;overflow:hidden;
  background:linear-gradient(126deg,#1B6E7E,#2F7F8C 46%,#4E93A0)}
.cov .cbg{position:absolute;right:-14%;top:-40%;width:40%;aspect-ratio:1;border-radius:50%;
  border:8px solid rgba(255,255,255,.16)}
.cov .cdiag{position:absolute;right:-12%;top:-30%;width:26%;height:180%;background:#F2F4F3;
  transform:rotate(20deg)}
.cov .cmark{position:absolute;right:6.5%;top:9%;font-size:9px;font-weight:800;
  color:rgba(255,255,255,.85);letter-spacing:.06em}
.cov .cbadge{position:absolute;left:8%;top:26%;background:#0E4650;color:#fff;font-size:8.5px;
  font-weight:800;letter-spacing:.06em;padding:3px 8px;border-radius:2px}
.cov .ctit{position:absolute;left:8%;top:41%;font-size:clamp(14px,1.9vw,25px);font-weight:800;
  color:#fff;letter-spacing:-.03em;line-height:1}
.cov .csub{position:absolute;left:8.5%;top:62%;font-size:7.5px;font-weight:600;
  color:rgba(255,255,255,.8);letter-spacing:.14em}
.cov .cdots{position:absolute;left:8%;bottom:12%;display:flex;gap:7px}
.cov .cdots i{width:11px;height:11px;border-radius:50%;border:1.2px solid rgba(255,255,255,.55)}

/* ── 기업 카드 — 1-2의 수렴 카드와 1-3의 리스트 행이 같은 모양을 공유한다 ── */
.ecard{display:grid;grid-template-columns:26px minmax(0,1.55fr) minmax(0,.95fr) 46px 66px;
  align-items:center;gap:12px;border-radius:11px;padding:10px 15px;
  background:#F7F3EC;border:1px solid rgba(26,23,20,.09);
  box-shadow:0 10px 22px -16px rgba(26,23,20,.3)}
.ecard.hi{background:#FFF3E9;border-color:rgba(204,114,71,.32);
  box-shadow:0 14px 28px -16px rgba(204,114,71,.4)}
.ecard .eini{width:26px;height:26px;border-radius:8px;background:var(--pet);color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800}
.ecard.hi .eini{background:var(--terra)}
.ecard .enm{font-size:13.5px;font-weight:800;letter-spacing:-.03em;color:var(--ink);
  display:grid;grid-template-columns:auto auto;gap:2px 7px;align-items:center;min-width:0;
  grid-template-areas:'a b' 'c c';justify-content:start}
.ecard .enm em{grid-area:b;font-style:normal;font-size:9px;font-weight:800;color:var(--ink3);
  letter-spacing:-.01em;background:rgba(26,23,20,.06);padding:2px 6px;border-radius:4px}
.ecard .enm small{grid-area:c;font-size:10px;font-weight:600;color:var(--ink2);letter-spacing:-.02em}
.ecard .ectc{font-size:10.5px;font-weight:700;color:var(--ink3);letter-spacing:-.02em;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ecard .esc{font-size:18px;font-weight:800;letter-spacing:-.04em;color:var(--pet);text-align:right}
.ecard.hi .esc{color:var(--terra)}
.ecard .ego{font-size:10px;font-weight:800;color:var(--ink3);text-align:right;white-space:nowrap}

/* ── 1-1) 소개서 분석 : 표지에서 실선이 뻗어 분석 카드로 연결된다 ── */
.sc.up .wires{position:absolute;inset:0;width:100%;height:100%;overflow:visible;z-index:1}
.sc.up .wr{fill:none;stroke:var(--terra);stroke-width:.55;opacity:.9;
  stroke-dasharray:1;stroke-dashoffset:1;vector-effect:non-scaling-stroke}
.fpane.on .up .wr{animation:draw .7s var(--e) forwards}
.fpane.on .up .w1{animation-delay:.85s}
.fpane.on .up .w2{animation-delay:1.25s}
.fpane.on .up .w3{animation-delay:1.65s}
.fpane.on .up .w4{animation-delay:2.05s}
@keyframes draw{to{stroke-dashoffset:0}}
.sc.up .docw{position:absolute;left:50%;top:47%;width:31%;aspect-ratio:16/9;z-index:2;
  transform:translate(-50%,-50%) rotateY(-11deg) rotateX(4deg);transform-style:preserve-3d;
  box-shadow:0 26px 50px -20px rgba(26,23,20,.45);border-radius:8px}
.sc.up .scan{position:absolute;left:0;right:0;height:40%;opacity:0;border-radius:8px;
  background:linear-gradient(180deg,transparent,rgba(255,255,255,.45),transparent)}
.fpane.on .up .scan{animation:scan 2.1s var(--e) .2s 2}
@keyframes scan{0%{opacity:0;transform:translateY(-40%)}12%{opacity:1}88%{opacity:1}
  100%{opacity:0;transform:translateY(280%)}}
.sc.up .chip{position:absolute;background:#fff;border-radius:11px;padding:11px 15px;
  box-shadow:0 18px 34px -16px rgba(26,23,20,.32);display:flex;flex-direction:column;gap:3px;
  width:24%;opacity:0;z-index:3;border:1px solid rgba(26,23,20,.08)}
.sc.up .ck{font-size:9.5px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:var(--terra)}
.sc.up .cv{font-size:12px;font-weight:700;letter-spacing:-.025em;color:var(--ink);line-height:1.4}
.sc.up .c1{left:8%;top:12%}
.sc.up .c2{right:7%;top:15%}
.sc.up .c3{left:8%;bottom:22%}
.sc.up .c4{right:7%;bottom:19%}
.fpane.on .up .chip{animation:chipIn .6s var(--e) forwards}
.fpane.on .up .c1{animation-delay:1.35s}
.fpane.on .up .c2{animation-delay:1.75s}
.fpane.on .up .c3{animation-delay:2.15s}
.fpane.on .up .c4{animation-delay:2.55s}
@keyframes chipIn{from{opacity:0;transform:translateZ(-120px) scale(.88)}to{opacity:1;transform:none}}

/* ── 1-2) 기업 선별 : 실제 서비스 화면을 훑어 기업 카드 한 장으로 모인다 ── */
.sc.flt .win{position:absolute;background:#fff;border-radius:10px;overflow:hidden;opacity:0;
  box-shadow:0 24px 44px -18px rgba(26,23,20,.36);border:1px solid rgba(26,23,20,.09)}
.fpane.on .flt .win{animation:winIn .6s var(--e) forwards,winGather .8s var(--e) 3s forwards}
.sc.flt .wv{left:4%;top:8%;width:40%;z-index:1}
.fpane.on .flt .wv{animation-delay:.25s,3s}
.sc.flt .wn{right:3%;top:19%;width:47%;z-index:2}
.fpane.on .flt .wn{animation-delay:.7s,3.1s}
.sc.flt .wj{left:26%;bottom:13%;width:44%;z-index:3}
.fpane.on .flt .wj{animation-delay:1.15s,3.2s}
@keyframes winIn{from{opacity:0;transform:translateY(20px) scale(.94)}to{opacity:1;transform:none}}
/* 창들이 화면 중앙의 카드 자리로 빨려 들어간다 */
@keyframes winGather{to{opacity:0;transform:translate(var(--gx,0),var(--gy,0)) scale(.34)}}
.sc.flt .wv{--gx:32%;--gy:150%}
.sc.flt .wn{--gx:-24%;--gy:88%}
.sc.flt .wj{--gx:6%;--gy:-72%}
.sc.flt .vth{position:relative;aspect-ratio:16/9;
  background:linear-gradient(150deg,#2B4A57,#16303A 55%,#0D2029)}
.sc.flt .vplay{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:34px;height:24px;border-radius:6px;background:rgba(255,0,0,.88);display:block}
.sc.flt .vplay::after{content:'';position:absolute;left:52%;top:50%;transform:translate(-50%,-50%);
  border-left:8px solid #fff;border-top:5px solid transparent;border-bottom:5px solid transparent}
.sc.flt .vdur{position:absolute;right:5px;bottom:5px;background:rgba(0,0,0,.78);color:#fff;
  font-size:8px;font-weight:700;padding:1px 4px;border-radius:3px}
.sc.flt .vmeta{display:flex;gap:8px;padding:9px 10px 11px}
.sc.flt .vav{width:22px;height:22px;border-radius:50%;background:#2C7D91;color:#fff;flex:none;
  display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800}
.sc.flt .vtx{display:flex;flex-direction:column;gap:2px;min-width:0}
.sc.flt .vtx b{font-size:10.5px;font-weight:800;letter-spacing:-.03em;color:var(--ink);line-height:1.35}
.sc.flt .vtx u{text-decoration:none;font-size:8.5px;color:var(--ink4)}
.sc.flt .nhd{display:flex;align-items:center;gap:7px;padding:8px 12px;
  border-bottom:1px solid var(--line)}
.sc.flt .nlogo{font-size:9px;font-weight:800;color:#fff;background:#1F3D6B;padding:2px 7px;border-radius:3px}
.sc.flt .ncat{font-size:8.5px;font-weight:700;color:var(--ink3)}
.sc.flt .ndate{font-size:8.5px;color:var(--ink4);margin-left:auto}
.sc.flt .nbody{padding:10px 12px 11px;display:flex;flex-direction:column;gap:5px}
.sc.flt .nti{font-size:12px;font-weight:800;letter-spacing:-.035em;color:var(--ink);line-height:1.35}
.sc.flt .nld{font-size:9px;color:var(--ink3);line-height:1.6;letter-spacing:-.02em}
.sc.flt .nfoot{font-size:8.5px;font-weight:800;color:#1F3D6B;margin-top:1px}
.sc.flt .jhd{display:flex;align-items:center;gap:7px;padding:8px 12px;background:#F6F8FA;
  border-bottom:1px solid var(--line)}
.sc.flt .jlogo{width:18px;height:18px;border-radius:4px;background:#2C7D91;color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:800}
.sc.flt .jco{font-size:9.5px;font-weight:800;color:var(--ink2)}
.sc.flt .jnew{margin-left:auto;font-size:8.5px;font-weight:800;color:#fff;background:#E0533C;
  padding:2px 7px;border-radius:3px}
.sc.flt .jbody{padding:10px 12px 11px;display:flex;flex-direction:column;gap:6px}
.sc.flt .jti{font-size:11.5px;font-weight:800;letter-spacing:-.035em;color:var(--ink)}
.sc.flt .jtags{display:flex;gap:4px;flex-wrap:wrap}
.sc.flt .jtags i{font-style:normal;font-size:8px;font-weight:700;color:var(--ink3);
  background:#EEF1F4;padding:2px 7px;border-radius:3px}
.sc.flt .jfoot{font-size:8.5px;font-weight:800;color:#2C7D91}
/* 수렴한 결과 — 다음 장면의 리스트 행과 똑같은 카드 */
.sc.flt .onecard{position:absolute;left:11%;right:11%;top:47%;transform:translateY(-50%);
  z-index:4;opacity:0}
.fpane.on .flt .onecard{animation:cardLand .7s var(--e) 3.5s forwards}
@keyframes cardLand{from{opacity:0;transform:translateY(-50%) scale(.86)}
  to{opacity:1;transform:translateY(-50%) scale(1)}}
.fpane.on .flt .sub{animation-delay:4.2s}

/* ── 1-3) 우선순위 : 카드가 위에서 아래로 흐르다 Fit Score 순으로 멈춘다 ── */
.sc.scr{display:flex;flex-direction:column;justify-content:center;padding:3.5% 6% 12%}
.scr .swin{position:relative;overflow:hidden;height:86%;
  -webkit-mask-image:linear-gradient(180deg,transparent,#000 12%,#000 82%,transparent);
  mask-image:linear-gradient(180deg,transparent,#000 12%,#000 82%,transparent)}
.scr .srail{display:flex;flex-direction:column;gap:6px;position:absolute;left:0;right:0;top:0}
/* 리스트 행은 조금 더 촘촘하게 — 한 화면에 5~6개가 보이도록 */
.scr .ecard{padding:8px 14px;gap:11px}
.scr .ecard .eini{width:23px;height:23px;border-radius:7px;font-size:11px}
.scr .ecard{grid-template-columns:23px minmax(0,1.55fr) minmax(0,.95fr) 44px 62px}
.scr .ecard .enm{font-size:12.5px}
.scr .ecard .enm small{font-size:9.5px}
.scr .ecard .esc{font-size:16.5px}
.fpane.on .scr .srail{animation:reel 3.9s cubic-bezier(.16,.72,.2,1) forwards}
@keyframes reel{0%{transform:translateY(-62%)}100%{transform:translateY(0)}}
.fpane.on .scr .swin{animation:listZoom 1.4s var(--e) 4s forwards}
@keyframes listZoom{to{transform:scale(1.04)}}
.fpane.on .scr .sub{animation-delay:4s}

/* ── 1-4) 심층 리서치 : 실시간 모니터링 대시보드 ── */
.sc.res{padding:3.5% 4.5% 11.5%;display:flex}
.res .dash{flex:1;background:#fff;border-radius:14px;padding:13px 15px 14px;
  display:flex;flex-direction:column;gap:8px;border:1px solid rgba(26,23,20,.09);
  box-shadow:0 22px 44px -24px rgba(26,23,20,.4);overflow:hidden}
.res .dtop{display:flex;align-items:center;gap:9px;opacity:0}
.fpane.on .res .dtop{animation:pop2 .5s var(--e) .12s forwards}
.res .fi{width:26px;height:26px;border-radius:8px;background:var(--pet);color:#fff;
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex:none}
.res .dnm{display:flex;flex-direction:column;gap:1px;min-width:0}
.res .dnm b{font-size:13.5px;font-weight:800;letter-spacing:-.03em}
.res .dnm small{font-size:9.5px;color:var(--ink4)}
.res .live{margin-left:auto;display:flex;align-items:center;gap:5px;font-size:9.5px;font-weight:800;
  color:#2C7D91;background:#E6F0F2;padding:4px 9px;border-radius:20px;flex:none}
.res .live i{width:5px;height:5px;border-radius:50%;background:#2C7D91}
.fpane.on .res .live i{animation:blink 1.4s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.2}}
.res .dtab{display:flex;gap:2px;border-bottom:1px solid var(--line);opacity:0;flex:none}
.fpane.on .res .dtab{animation:pop2 .45s var(--e) .3s forwards}
.res .dtab span{font-size:9.5px;font-weight:700;color:var(--ink4);padding:5px 9px;
  border-bottom:2px solid transparent;margin-bottom:-1px}
.res .dtab span.on{color:var(--pet);border-bottom-color:var(--pet)}
.res .kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;flex:none}
.res .kpi{background:#F8F6F1;border-radius:9px;padding:7px 10px;display:flex;
  flex-direction:column;gap:2px;opacity:0;border:1px solid rgba(26,23,20,.05);min-width:0}
.fpane.on .res .kpi{animation:pop2 .5s var(--e) forwards}
.fpane.on .res .kpi:nth-child(1){animation-delay:.5s}
.fpane.on .res .kpi:nth-child(2){animation-delay:.7s}
.fpane.on .res .kpi:nth-child(3){animation-delay:.9s}
.fpane.on .res .kpi:nth-child(4){animation-delay:1.1s}
.res .kk{font-size:9px;font-weight:700;color:var(--ink3)}
.res .krow{display:flex;align-items:flex-end;gap:7px;min-width:0}
.res .kpi b{font-size:17px;font-weight:800;letter-spacing:-.05em;color:var(--ink);
  display:flex;align-items:baseline;gap:2px;white-space:nowrap}
.res .kpi b u{text-decoration:none;font-size:.48em;color:var(--ink3);font-weight:700}
.res .spk{width:44px;height:16px;flex:none;margin-bottom:2px;overflow:visible}
.res .spk path{fill:none;stroke:var(--pet);stroke-width:1.6;stroke-linecap:round;
  stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;vector-effect:non-scaling-stroke}
.fpane.on .res .spk path{animation:draw .9s var(--e) 1.3s forwards}
.res .kd{font-size:8.5px;font-weight:800;color:var(--ink4);display:flex;align-items:baseline;gap:5px}
.res .kd.up{color:#2F7D5B}
.res .kd em{font-style:normal;font-weight:600;color:var(--ink4);font-size:7.5px;
  margin-left:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.res .dgrid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:7px;
  flex:1;min-height:124px}
.res .pnl{background:#F8F6F1;border-radius:9px;padding:9px 11px;display:flex;
  flex-direction:column;gap:6px;opacity:0;border:1px solid rgba(26,23,20,.05);min-height:0}
.fpane.on .res .pnl{animation:pop2 .5s var(--e) forwards}
.fpane.on .res .chart{animation-delay:1.35s}
.fpane.on .res .insight{animation-delay:1.6s}
.res .pnt{font-size:9px;font-weight:800;color:var(--ink3);display:flex;align-items:baseline;gap:6px}
.res .pnt.hi{color:var(--terra)}
.res .pnt em{font-style:normal;font-weight:600;color:var(--ink4);font-size:7.5px;margin-left:auto}
.res .chart .pnt{gap:9px}
.res .bars{flex:1;display:flex;align-items:flex-end;gap:8px;min-height:52px;padding-bottom:12px;
  position:relative}
.res .bars i{flex:1;display:flex;align-items:flex-end;justify-content:center;gap:2px;height:100%;
  position:relative}
.res .bars u{width:42%;border-radius:2px 2px 0 0;height:0;text-decoration:none}
.res .bars .b1{background:var(--pet)}
.res .bars .b2{background:#D7A98C}
.res .bars s{position:absolute;left:0;right:0;bottom:-12px;text-align:center;text-decoration:none;
  font-size:6.5px;color:var(--ink4)}
.fpane.on .res .bars u{animation:bar .8s var(--e) 1.7s forwards}
@keyframes bar{to{height:var(--h)}}
.res .lgd{display:flex;gap:9px;flex:none;margin-top:-2px}
.res .lgd em{font-style:normal;font-size:7.5px;font-weight:700;color:var(--ink3);
  display:flex;align-items:center;gap:4px}
.res .lgd em::before{content:'';width:7px;height:7px;border-radius:2px}
.res .lgd .e1::before{background:var(--pet)}
.res .lgd .e2::before{background:#D7A98C}
.res .insight{background:#FDF3EC;border-color:rgba(204,114,71,.2)}
.res .iv{font-size:10px;font-weight:700;color:var(--ink2);letter-spacing:-.025em;line-height:1.45;
  white-space:nowrap;overflow:hidden;max-width:0;flex:none}
.res .iv.hit{font-weight:800;color:var(--terra);font-size:10.5px;margin-top:auto}
.res .iv b{font-weight:800;font-size:1.2em}
.fpane.on .res .iv{animation:typeIn .75s steps(30) forwards}
.fpane.on .res .insight .l1{animation-delay:1.95s}
.fpane.on .res .insight .l2{animation-delay:2.65s}
.fpane.on .res .insight .l3{animation-delay:3.35s}
.fpane.on .res .sub{animation-delay:4.1s}

/* ── 2-1) 제안 논리 : 회사 옆에 공개 데이터 창이 뜨고 논리가 정리된다 ── */
.sc.lgc .bldg{position:absolute;left:23%;top:44%;width:19%;
  transform:translate(-50%,-50%);
  display:flex;flex-direction:column;align-items:center;gap:5px;opacity:0}
.fpane.on .lgc .bldg{animation:bldgIn .7s var(--e) .15s forwards}
@keyframes bldgIn{from{opacity:0;transform:translate(-50%,-50%) scale(.86)}
  to{opacity:1;transform:translate(-50%,-50%) scale(1)}}
.sc.lgc .bldg svg{width:100%;height:auto;display:block}
.sc.lgc .bldg rect{fill:#D9E4E6;stroke:#2C7D91;stroke-width:2.4}
.sc.lgc .bldg .grd{fill:#2C7D91;stroke:none}
.sc.lgc .bldg .wdw{stroke:#2C7D91;stroke-width:2.6;stroke-linecap:round;opacity:.5}
.sc.lgc .bldg b{font-size:12px;font-weight:800;letter-spacing:-.03em;color:var(--ink);margin-top:3px}
.sc.lgc .bldg u{text-decoration:none;font-size:9.5px;font-weight:600;color:var(--ink3);
  text-align:center;line-height:1.35}
.sc.lgc .lwin{position:absolute;background:#fff;border-radius:10px;padding:9px 12px;
  display:flex;flex-direction:column;gap:2px;width:41%;opacity:0;
  border:1px solid rgba(26,23,20,.09);box-shadow:0 18px 34px -16px rgba(26,23,20,.32)}
.sc.lgc .lk{font-size:8.5px;font-weight:800;letter-spacing:.04em;color:var(--pet)}
.sc.lgc .lv{font-size:11px;font-weight:700;letter-spacing:-.03em;color:var(--ink);line-height:1.4}
.sc.lgc .lm{font-size:8.5px;font-weight:600;color:var(--ink4)}
.sc.lgc .lw1{right:5%;top:8%}
.sc.lgc .lw2{right:12%;top:31%}
.sc.lgc .lw3{right:4%;top:54%}
.sc.lgc .lw4{right:14%;bottom:9%}
.fpane.on .lgc .lwin{animation:lwIn .55s var(--e) forwards,lwOut .6s var(--e) 3.4s forwards}
.fpane.on .lgc .lw1{animation-delay:.7s,3.4s}
.fpane.on .lgc .lw2{animation-delay:1.1s,3.5s}
.fpane.on .lgc .lw3{animation-delay:1.5s,3.6s}
.fpane.on .lgc .lw4{animation-delay:1.9s,3.7s}
@keyframes lwIn{from{opacity:0;transform:translateX(24px) scale(.94)}to{opacity:1;transform:none}}
@keyframes lwOut{to{opacity:0;transform:translateX(18px) scale(.9)}}
.fpane.on .lgc .bldg{animation:bldgIn .7s var(--e) .15s forwards,lwOut .6s var(--e) 3.5s forwards}
/* 제안 논리 — 이메일로 이어질 문장이라 테라코타 박스로 표시한다 */
.sc.lgc .lout{position:absolute;left:9%;right:9%;top:50%;transform:translateY(-50%);
  background:#fff;border-radius:14px;padding:20px 24px;display:flex;flex-direction:column;gap:9px;
  opacity:0;z-index:4;border:1px solid rgba(26,23,20,.1);
  box-shadow:0 28px 52px -22px rgba(26,23,20,.4)}
.sc.lgc .lt{font-size:9.5px;font-weight:800;letter-spacing:.08em;color:var(--terra)}
.sc.lgc .ln{font-size:14px;font-weight:700;letter-spacing:-.035em;color:var(--ink);
  line-height:1.5;background:var(--terraw);padding:7px 12px;border-radius:7px;
  align-self:flex-start;opacity:0}
.fpane.on .lgc .lout{animation:loutIn .7s var(--e) 3.9s forwards}
@keyframes loutIn{from{opacity:0;transform:translateY(-50%) scale(.94)}
  to{opacity:1;transform:translateY(-50%) scale(1)}}
.fpane.on .lgc .ln{animation:fadeUp .5s var(--e) forwards}
.fpane.on .lgc .l1{animation-delay:4.25s}
.fpane.on .lgc .l2{animation-delay:4.65s}
.fpane.on .lgc .l3{animation-delay:5.05s}
.fpane.on .lgc .sub{animation-delay:5.5s}

/* ── 2-2) 이메일 생성 : 제안 논리 문장이 그대로 본문에 붙는다 ── */
.sc.mal{padding:4.5% 5% 12%;display:flex}
.mal .mwin{flex:1;background:#fff;border-radius:14px;padding:16px 22px 18px;display:flex;
  flex-direction:column;justify-content:center;gap:8px;border:1px solid rgba(26,23,20,.09);
  box-shadow:0 22px 44px -24px rgba(26,23,20,.4)}
.mal .mlang{display:inline-flex;align-self:flex-start;gap:2px;background:#F1EEE8;border-radius:7px;
  padding:2px;opacity:0}
.fpane.on .mal .mlang{animation:pop2 .45s var(--e) .1s forwards}
.mal .mlang span{font-size:9.5px;font-weight:800;color:var(--ink3);padding:4px 11px;border-radius:5px}
.mal .mlang .on{background:var(--ink);color:#fff}
.mal .mh{display:flex;align-items:baseline;gap:14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.mal .mf{font-size:10px;font-weight:700;color:var(--ink3);width:56px;flex:none}
.mal .mv{font-size:13px;font-weight:700;letter-spacing:-.03em;color:var(--ink)}
.mal .mb{display:flex;flex-direction:column;gap:7px;margin-top:6px}
.mal .mb .bl{font-size:12px;color:var(--ink2);letter-spacing:-.025em;line-height:1.6;opacity:0}
.mal .ty{display:block;overflow:hidden;max-width:0;white-space:nowrap}
.fpane.on .mal .t1{animation:typeIn .8s steps(24) .6s forwards}
.fpane.on .mal .bl{animation:lineIn .5s var(--e) forwards}
@keyframes lineIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.fpane.on .mal .b0{animation-delay:1.5s}
.mal .moved{font-weight:700;color:var(--ink);align-self:flex-start;
  padding:5px 10px;border-radius:6px;margin-left:-10px}
.fpane.on .mal .mv1{animation:movedIn .7s var(--e) 2.1s forwards}
.fpane.on .mal .mv2{animation:movedIn .7s var(--e) 2.85s forwards}
.fpane.on .mal .mv3{animation:movedIn .7s var(--e) 3.6s forwards}
@keyframes movedIn{0%{opacity:0;transform:translateX(-26px);background:var(--terraw)}
  50%{opacity:1;transform:none;background:var(--terraw)}
  100%{opacity:1;transform:none;background:transparent}}
.fpane.on .mal .b4{animation-delay:4.4s}
.fpane.on .mal .sub{animation-delay:5s}

/* ── 2-3) 전송 : 버튼 한 번에 주소와 본문이 통째로 옮겨간다 ── */
.sc.snd .mini{position:absolute;left:5%;top:24%;width:32%;background:#fff;border-radius:11px;
  padding:10px 12px;display:flex;flex-direction:column;gap:4px;opacity:0;
  border:1px solid rgba(26,23,20,.09);box-shadow:0 22px 42px -20px rgba(26,23,20,.42);
  transform:translateY(-50%)}
.fpane.on .snd .mini{animation:pop2 .6s var(--e) .3s forwards}
.sc.snd .mkt{font-size:7.5px;font-weight:800;letter-spacing:.06em;color:var(--ink4);
  padding-bottom:4px;border-bottom:1px solid var(--line)}
.sc.snd .emr{display:flex;align-items:baseline;gap:7px;padding-bottom:3px;
  border-bottom:1px solid var(--line)}
.sc.snd .emk{font-size:7.5px;font-weight:700;color:var(--ink3);width:38px;flex:none}
.sc.snd .emv{font-size:9px;font-weight:700;letter-spacing:-.03em;color:var(--ink);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sc.snd .mbody{display:flex;flex-direction:column;gap:2px;margin-top:1px}
.sc.snd .mbl{font-size:7px;color:var(--ink3);letter-spacing:-.025em;line-height:1.4}
.sc.snd .mbl.hl{color:var(--ink);font-weight:700;background:var(--terraw);
  padding:1.5px 4px;border-radius:3px;align-self:flex-start}
.sc.snd .obtn{align-self:stretch;text-align:center;margin-top:3px;background:var(--terra);color:#fff;
  font-size:9px;font-weight:800;padding:6px 9px;border-radius:6px;
  box-shadow:0 10px 20px -10px rgba(204,114,71,.65)}
.fpane.on .snd .obtn{animation:btnTap .6s var(--e) 2s}
@keyframes btnTap{0%{transform:none}35%{transform:scale(.9);filter:brightness(.86)}100%{transform:none}}
.sc.snd .flyA,.sc.snd .flyB{position:absolute;left:31%;border-radius:6px;background:var(--pet);
  opacity:0;z-index:5}
.sc.snd .flyA{top:40.1%;width:16%;height:9px}
.sc.snd .flyB{top:44.3%;width:16%;height:20px;background:var(--petw2)}
.fpane.on .snd .flyA{animation:flyOverA 1.1s var(--e) 2.4s forwards}
.fpane.on .snd .flyB{animation:flyOverB 1.1s var(--e) 2.75s forwards}
/* 날아가는 막대는 '이동'만 담당하고 중간에 사라진다. 착지 표시는 아웃룩 필드 자체에
   형광펜으로 그리므로(.ov), 기기 비율이 달라져도 엉뚱한 곳에 찍히지 않는다. */
@keyframes flyOverA{0%{opacity:0;transform:translateX(0) scale(.9)}
  18%{opacity:1;transform:translateX(20%) scale(1)}
  70%{opacity:.9;transform:translateX(120%) scale(1)}
  100%{opacity:0;transform:translateX(165%) scale(.94)}}
@keyframes flyOverB{0%{opacity:0;transform:translateX(0) scale(.9)}
  18%{opacity:1;transform:translateX(20%) scale(1)}
  70%{opacity:.9;transform:translateX(120%) scale(1)}
  100%{opacity:0;transform:translateX(165%) scale(.94)}}
.sc.snd .olk{position:absolute;right:4%;top:45%;width:54%;background:#fff;border-radius:11px;
  overflow:hidden;border:1px solid rgba(26,23,20,.09);
  box-shadow:0 26px 50px -22px rgba(26,23,20,.42);
  transform:translateY(-50%) translateX(6%);opacity:0}
.fpane.on .snd .olk{animation:olkIn .8s var(--e) .9s forwards}
@keyframes olkIn{to{opacity:1;transform:translateY(-50%) translateX(0)}}
.sc.snd .obar{display:flex;align-items:center;gap:5px;background:#F3F2F1;padding:7px 11px;
  border-bottom:1px solid #E1DFDD}
.sc.snd .odot{width:7px;height:7px;border-radius:50%}
.sc.snd .odot.r{background:#FF5F57}.sc.snd .odot.y{background:#FEBC2E}.sc.snd .odot.g{background:#28C840}
.sc.snd .ologo{width:14px;height:14px;border-radius:3px;background:#0F6CBD;color:#fff;font-size:9px;
  font-weight:800;display:flex;align-items:center;justify-content:center;margin-left:7px}
.sc.snd .obar b{font-size:9.5px;font-weight:700;color:#323130}
.sc.snd .obody{display:grid;grid-template-columns:27% minmax(0,1fr)}
.sc.snd .oside{background:#FAF9F8;border-right:1px solid #EDEBE9;padding:9px 8px;
  display:flex;flex-direction:column;gap:5px}
.sc.snd .oi{font-size:8.5px;font-weight:600;color:#605E5C;padding:4px 6px;border-radius:4px}
.sc.snd .oi.on{background:#EAEAEA;color:#0F6CBD;font-weight:800}
.sc.snd .omain{padding:10px 13px 12px;display:flex;flex-direction:column;gap:6px}
.sc.snd .ofld{display:flex;align-items:baseline;gap:8px;padding-bottom:5px;border-bottom:1px solid #EDEBE9}
.sc.snd .ok{font-size:8.5px;font-weight:700;color:#8A8886;flex:none;width:46px}
.sc.snd .ov{font-size:10px;font-weight:700;color:#201F1E;letter-spacing:-.02em;
  white-space:nowrap;overflow:hidden;max-width:0;flex:none}
/* 채워지는 두 필드('받는 사람'·'제목')에 형광펜을 깔아두면, typeIn 이 max-width 를 늘리는
   동안 형광펜도 같이 칠해진다 — 좌표를 찍지 않으므로 어떤 기종에서도 정확히 이 두 줄에만 뜬다. */
.sc.snd .ov.land,.sc.snd .ov.land2{
  background-image:linear-gradient(rgba(204,114,71,.34),rgba(204,114,71,.34));
  background-repeat:no-repeat;background-position:0 86%;background-size:100% 46%}
.fpane.on .snd .land{animation:typeIn .6s steps(22) 3.3s forwards}
.fpane.on .snd .land2{animation:typeIn .7s steps(26) 3.9s forwards}
.sc.snd .obd{font-size:9px;color:#605E5C;line-height:1.55;letter-spacing:-.02em;opacity:0}
.fpane.on .snd .land3{animation:lineIn .6s var(--e) 4.5s forwards}
.sc.snd .osend{align-self:flex-start;margin-top:4px;background:#0F6CBD;color:#fff;font-size:9px;
  font-weight:800;padding:5px 12px;border-radius:3px;opacity:0}
.fpane.on .snd .osend{animation:pop2 .5s var(--e) 5.1s forwards}
.fpane.on .snd .sub{animation-delay:5.4s}

/* ── 2-4) 제안서 : 한 장이 조립된 뒤 뒤로 물러나며 전체가 나열된다 ── */
.sc.dck .build{position:absolute;left:50%;top:43%;width:54%;aspect-ratio:16/9;
  transform:translate(-50%,-50%);background:#fff;border-radius:10px;padding:5% 5.5%;
  border:1px solid rgba(26,23,20,.09);
  box-shadow:0 28px 54px -22px rgba(26,23,20,.42);overflow:hidden;z-index:3}
.fpane.on .dck .build{animation:buildBack 1s var(--e) 4.2s forwards}
@keyframes buildBack{to{transform:translate(-50%,-50%) translateY(-26%) scale(.42)}}
.sc.dck .btag{position:absolute;left:5.5%;top:7.5%;font-size:8px;font-weight:800;color:#fff;
  background:#2C7D91;padding:4px 9px;border-radius:20px;opacity:0}
.fpane.on .dck .btag{animation:pop2 .5s var(--e) .6s forwards}
.sc.dck .bt{position:absolute;left:27%;top:6.5%;right:5.5%;font-size:10.5px;font-weight:800;
  letter-spacing:-.035em;line-height:1.4;color:#12495A;opacity:0;
  border-bottom:1.5px solid #12495A;padding-bottom:5px}
.fpane.on .dck .bt{animation:pop2 .5s var(--e) .25s forwards}
.sc.dck .bbody{position:absolute;left:5.5%;top:30%;width:44%;font-size:8.5px;font-weight:600;
  color:var(--ink2);line-height:1.6;letter-spacing:-.02em;opacity:0}
.fpane.on .dck .bbody{animation:pop2 .5s var(--e) 1.05s forwards}
.sc.dck .btbl{position:absolute;left:5.5%;bottom:8%;width:44%;display:flex;flex-direction:column;gap:0}
.sc.dck .btbl i{display:grid;grid-template-columns:minmax(0,1fr) 40px 30px;gap:4px;
  padding:3.5px 4px;border-bottom:1px solid #E3EAEC;opacity:0}
.sc.dck .btbl u{text-decoration:none;font-size:7px;font-weight:700;color:var(--ink2);letter-spacing:-.02em}
.sc.dck .btbl u:not(:first-child){text-align:right;font-variant-numeric:tabular-nums}
.sc.dck .btbl .th{border-bottom:1.5px solid #12495A}
.sc.dck .btbl .th u{color:#12495A;font-weight:800}
.sc.dck .btbl .sum{background:#E9F1F3;border-bottom:none}
.sc.dck .btbl .sum u{color:#12495A;font-weight:800}
.fpane.on .dck .btbl i{animation:tblIn .4s var(--e) forwards}
@keyframes tblIn{from{opacity:0;transform:translateX(-14px)}to{opacity:1;transform:none}}
.fpane.on .dck .btbl i:nth-child(1){animation-delay:1.5s}
.fpane.on .dck .btbl i:nth-child(2){animation-delay:1.65s}
.fpane.on .dck .btbl i:nth-child(3){animation-delay:1.8s}
.fpane.on .dck .btbl i:nth-child(4){animation-delay:1.95s}
.fpane.on .dck .btbl i:nth-child(5){animation-delay:2.1s}
/* 지도 — 실제 장표의 지도 이미지가 그대로 뜬다 */
.sc.dck .bmap{position:absolute;right:2.5%;top:17%;bottom:6%;width:43%;
  display:flex;align-items:center;justify-content:center}
.sc.dck .kmap{max-width:100%;max-height:100%;width:auto;height:auto;display:block;opacity:0}
.fpane.on .dck .kmap{animation:mapIn .7s var(--e) 2.3s forwards}
@keyframes mapIn{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
/* 전체 장표가 나열된다 — 실제 생성된 제안서 장표 */
.sc.dck .pages{position:absolute;left:5%;right:5%;top:58%;
  display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:5px;z-index:2}
.sc.dck .pgz{position:relative;aspect-ratio:16/9;border-radius:3px;overflow:hidden;
  background:#fff;border:1px solid rgba(26,23,20,.14);
  box-shadow:0 7px 14px -9px rgba(26,23,20,.32);opacity:0}
.sc.dck .pgz img{width:100%;height:100%;object-fit:cover;display:block}
.fpane.on .dck .pgz{animation:pgIn .45s var(--e) forwards}
@keyframes pgIn{from{opacity:0;transform:translateY(14px) scale(.86)}to{opacity:1;transform:none}}
.fpane.on .dck .p0{animation-delay:4.75s}
.fpane.on .dck .p1{animation-delay:4.80s}
.fpane.on .dck .p2{animation-delay:4.85s}
.fpane.on .dck .p3{animation-delay:4.90s}
.fpane.on .dck .p4{animation-delay:4.95s}
.fpane.on .dck .p5{animation-delay:5.00s}
.fpane.on .dck .p6{animation-delay:5.05s}
.fpane.on .dck .p7{animation-delay:5.10s}
.fpane.on .dck .p8{animation-delay:5.15s}
.fpane.on .dck .p9{animation-delay:5.20s}
.fpane.on .dck .p10{animation-delay:5.25s}
.fpane.on .dck .p11{animation-delay:5.30s}
.fpane.on .dck .p12{animation-delay:5.35s}
.fpane.on .dck .p13{animation-delay:5.40s}
.fpane.on .dck .p14{animation-delay:5.45s}
.fpane.on .dck .p15{animation-delay:5.50s}
.fpane.on .dck .p16{animation-delay:5.55s}
.fpane.on .dck .p17{animation-delay:5.60s}
.fpane.on .dck .p18{animation-delay:5.65s}
.fpane.on .dck .sub{animation-delay:5.5s}

/* ══ 범용 AI 비교 ══ */
.cmpsec{padding:104px 0 96px}
.cmphead{text-align:center;margin-bottom:52px}
.cmpq{font-size:17.5px;font-weight:700;color:var(--ink2);letter-spacing:-.03em;margin-bottom:16px}
.cmphead h2{font-size:clamp(27px,3.5vw,45px);font-weight:800;letter-spacing:-.05em;line-height:1.28}
.cmphead h2 .ul{color:var(--pet)}

.cmp{position:relative;max-width:1080px;margin:0 auto;background:var(--surf);
  border-radius:20px;box-shadow:var(--s2);overflow:hidden}
.cmpcol{position:absolute;top:0;bottom:0;left:66.6%;right:0;background:var(--pet);
  pointer-events:none}
.cmphd,.cmpr{position:relative;display:grid;
  grid-template-columns:minmax(0,1.15fr) minmax(0,1fr) minmax(0,1fr)}
.cmphd span{font-size:17px;font-weight:800;letter-spacing:-.03em;color:var(--ink2);
  padding:22px 32px 18px;text-align:center}
.cmphd span:first-child{background:var(--paper2)}
.cmphd span.on{color:#fff}
.cmpr{border-top:1px solid var(--line)}
.cmpr>div{padding:26px 32px;display:flex;flex-direction:column;gap:5px;justify-content:center}
.cmpk{background:var(--paper2);font-size:16.5px;font-weight:800;letter-spacing:-.04em;color:var(--terra);
  line-height:1.42}
.cmpa b,.cmpb b{font-size:17px;font-weight:800;letter-spacing:-.04em;line-height:1.4}
.cmpa small,.cmpb small{font-size:13.5px;letter-spacing:-.02em;line-height:1.55}
/* 범용 AI 쪽 답변은 먹색으로 또렷하게 — 질문은 테라코타로 행 라벨 역할을 준다 */
.cmpa b{color:var(--ink)}
.cmpa small{color:var(--ink3)}
.cmpb b{color:#fff}
.cmpb small{color:rgba(255,255,255,.82)}
.cmpend{max-width:960px;margin:44px auto 0;text-align:center}
.cmpend b{display:block;font-weight:800;color:var(--ink);letter-spacing:-.035em}
.cmpend .cmpend1{font-size:clamp(27px,3.5vw,45px);margin-bottom:2px}
.cmpend .cmpend2{display:block;font-weight:800;color:var(--ink2);letter-spacing:-.02em;
  font-size:clamp(15.5px,1.6vw,19px);line-height:1.5;margin-top:8px}

/* ══ 성과 (덮임 전환) ══ */
.overlap{position:relative;z-index:3;margin-top:-52px;border-radius:32px 32px 0 0;overflow:hidden;
  background:var(--ink);color:#fff;padding:132px 0 150px;box-shadow:0 -30px 60px -30px rgba(26,23,20,.5)}
.overlap::before{content:'';position:absolute;top:-160px;left:50%;transform:translateX(-50%);
  width:960px;height:560px;background:radial-gradient(ellipse at center,rgba(20,110,130,.28),transparent 66%)}
.overlap .wrap{position:relative}
.overlap .head h2{color:#fff}
.overlap .head h2 .q{color:#9FDCE9}
.overlap .head p{color:rgba(255,255,255,.66)}
/* 도입 사례 — 레이아웃 고정, hover 시 픽토그램만 강조 */
.tg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;margin-top:56px}
.tc{background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.09);border-radius:22px;
  padding:30px 30px 30px;min-height:340px;position:relative;overflow:hidden;
  display:flex;flex-direction:column;
  transition:background .4s var(--e),border-color .4s var(--e),transform .4s var(--e)}
.tc:hover{background:rgba(255,255,255,.075);border-color:rgba(255,255,255,.22);transform:translateY(-6px)}
.tc .who{font-size:15px;font-weight:800;letter-spacing:-.02em;color:rgba(255,255,255,.42);
  margin-bottom:18px}
/* 코멘트 — 문장은 좌측 정렬, 따옴표만 Noto Sans로 정렬선 바깥에 매달린다 */
.tc blockquote{position:relative;padding-left:19px;margin-bottom:auto;text-align:left}
.tc .qt{display:inline;font-size:17.5px;font-weight:700;letter-spacing:-.038em;line-height:1.66;
  color:rgba(255,255,255,.9)}
.tc .qo,.tc .qc{font-family:var(--fq);font-style:normal;font-weight:700;
  font-size:24px;color:rgba(255,255,255,.28);line-height:0;position:relative;top:.14em}
.tc .qo{position:absolute;left:-2px;top:.42em}
.tc .qc{margin-left:.24em}
/* 숫자 블록 — 우측 정렬로 크게 */
.tc .stat{margin-top:26px;text-align:right}
.tc .bl{font-size:26px;font-weight:800;color:#84C6D4;margin-bottom:6px;
  letter-spacing:-.035em;line-height:1.25}
.tc .big{font-size:clamp(44px,4.9vw,62px);font-weight:800;letter-spacing:-.062em;line-height:1;
  display:flex;align-items:baseline;justify-content:flex-end;gap:5px;color:#84C6D4}
.tc .big .pre{font-size:.32em;font-weight:700;color:rgba(255,255,255,.62);letter-spacing:-.02em}
.tc .big .pre:empty{display:none}
.tc .big .u{font-size:.3em;color:rgba(255,255,255,.62);letter-spacing:-.02em;white-space:nowrap}
/* 세어 올라가는 동안은 흰색, 목표 숫자에 닿으면 하늘색으로 돌아온다 */
.tc .big .nm{transition:color .45s var(--e)}
.tc .big .nm.counting{color:#fff}

/* ══ 가격 ══ */
.pg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;align-items:stretch}
.pc{background:var(--surf);border-radius:22px;padding:38px 34px;display:flex;flex-direction:column;position:relative;box-shadow:var(--s2);transition:.3s var(--e)}
.pc:hover{transform:translateY(-3px);box-shadow:var(--s3)}
.pc.hot{background:linear-gradient(162deg,#12414D,#0B2C36 62%,#071F26);color:#fff;z-index:2;
  box-shadow:0 34px 70px -26px rgba(11,44,54,.6);transform:translateY(-16px)}
.pc.hot:hover{transform:translateY(-22px)}
.pc.hot .pd{color:rgba(255,255,255,.66)}
.pc.hot .pp{color:#fff}
.pc.hot .pt{color:rgba(255,255,255,.55);border-bottom-color:rgba(255,255,255,.16)}
.pc.hot .pin2{border-bottom-color:rgba(255,255,255,.16)}
.pc.hot .pin2 .r{color:rgba(255,255,255,.66)}
.pc.hot .pin2 .r b{color:#fff}
.pc.hot .pin2 .r b.h{color:#84C6D4}
.pc.hot .pfe li{color:rgba(255,255,255,.82)}
.pc.hot .pfe li::before{border-color:#84C6D4}
.pc.hot .btn-p{background:#fff;color:var(--pet2)}
.pc.hot .btn-p:hover{background:#EAF3F4}
.pc .pb{position:absolute;top:22px;right:26px;background:rgba(255,255,255,.16);color:#fff;
  font-size:11.5px;font-weight:800;padding:6px 12px;border-radius:20px;
  border:1px solid rgba(255,255,255,.24)}
.pc h3{font-size:23px;font-weight:800;letter-spacing:-.045em;margin-bottom:12px}
.pd{font-size:14px;color:var(--ink3);line-height:1.72;min-height:66px;margin-bottom:26px}
.pp{font-size:35px;font-weight:800;letter-spacing:-.055em;line-height:1.08;font-variant-numeric:tabular-nums}
.pt{font-size:13.5px;color:var(--ink3);margin-top:10px;padding-bottom:24px;border-bottom:1px solid var(--line)}
.pin2{padding:22px 0;border-bottom:1px solid var(--line);display:flex;flex-direction:column;gap:11px}
.pin2 .r{display:flex;justify-content:space-between;font-size:14px;color:var(--ink2)}
.pin2 .r b{color:var(--ink);font-weight:700}.pin2 .r b.h{color:var(--pet)}
.pfe{list-style:none;padding:24px 0 30px;flex:1;display:flex;flex-direction:column;gap:13px}
.pfe li{font-size:14px;color:var(--ink2);padding-left:25px;position:relative;line-height:1.68}
.pfe li::before{content:'';position:absolute;left:0;top:7px;width:11px;height:6.5px;
  border-left:2px solid var(--pet);border-bottom:2px solid var(--pet);transform:rotate(-45deg)}
.pc .btn{width:100%;padding:14px;font-size:15.5px;border-radius:11px}
.pn{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px;margin-top:44px;padding-top:36px;border-top:1px solid var(--line)}
.pn b{font-size:14px;display:block;margin-bottom:9px}
.pn p{font-size:13.5px;color:var(--ink3);line-height:1.78}

/* ══ FAQ ══ */
.faq{max-width:840px;margin:0 auto;text-align:left}
.fq{border-bottom:1px solid var(--line)}
.fq:first-child{border-top:1px solid var(--line)}
.fq button{width:100%;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:28px 2px;
  text-align:left;font-size:18.5px;font-weight:700;letter-spacing:-.04em}
.fq .pm{width:20px;height:20px;flex:none;position:relative}
.fq .pm::before,.fq .pm::after{content:'';position:absolute;background:var(--ink3);border-radius:2px;transition:.3s var(--e)}
.fq .pm::before{left:1px;top:9px;width:18px;height:2px}
.fq .pm::after{left:9px;top:1px;width:2px;height:18px}
.fq.on .pm::after{transform:rotate(90deg);opacity:0}
.fq .an{max-height:0;overflow:hidden;transition:max-height .4s var(--e)}
.fq.on .an{max-height:400px}
.fq .an p{font-size:16px;color:var(--ink2);line-height:1.85;padding:0 2px 30px;max-width:72ch}

/* ══ ENDING ══ */
.end{position:relative;padding:168px 0;overflow:hidden;text-align:center;isolation:isolate}
.end-bg{position:absolute;inset:0;background-size:cover;background-position:center;transform:scale(1.06)}
.end-bg::after{content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(250,248,243,.86),rgba(250,248,243,.62) 45%,rgba(250,248,243,.9))}
.end .wrap{position:relative;z-index:2}
.end h2{font-size:clamp(30px,4.1vw,52px);font-weight:800;letter-spacing:-.055em;line-height:1.16;max-width:21ch;margin:0 auto;
  text-shadow:0 1px 0 rgba(255,255,255,.6)}
.end p{font-size:17.5px;color:var(--ink2);margin-top:22px;max-width:62ch;margin-left:auto;margin-right:auto;line-height:1.74}
.end p.lead{font-weight:700;color:#3A362F}
.end .hi{color:var(--pet);font-weight:800}
.ul{position:relative;display:inline-block;white-space:nowrap}
/* 손으로 그은 듯한 반투명 하이라이트 마커 — 텍스트 뒤에 깔린다 */
.hlmark::before{content:'';position:absolute;left:-4%;right:-4%;top:6%;bottom:0%;z-index:-1;
  background:rgba(204,114,71,.32);border-radius:3px 9px 6px 8px;
  transform:rotate(-.8deg) scaleX(0);transform-origin:left center;
  transition:transform .85s cubic-bezier(.5,.05,.3,1) .3s}
.end h2.on .hlmark::before{transform:rotate(-.8deg) scaleX(1)}
.end .row{display:flex;gap:12px;margin-top:38px;flex-wrap:wrap;justify-content:center;align-items:center}
.end .btn{padding:16px 34px;font-size:16px;border-radius:12px;min-width:224px}
.btn-ow{background:rgba(255,255,255,.9);color:var(--ink);backdrop-filter:blur(8px);
  box-shadow:inset 0 0 0 1.4px rgba(26,23,20,.16),0 4px 16px -8px rgba(26,23,20,.3)}
.btn-ow:hover{background:#fff}

footer{border-top:1px solid var(--line);padding:64px 0 40px;background:var(--paper)}
.ft{display:flex;justify-content:space-between;gap:56px;margin-bottom:52px;flex-wrap:wrap}
.fb2 .fl{font-size:26px;font-weight:800;letter-spacing:-.05em;color:var(--ink);line-height:1.1}
.fb2 p{font-size:14px;color:var(--ink3);margin-top:14px;line-height:1.78;white-space:nowrap}
.fc{display:flex;gap:64px;flex-wrap:wrap}
.fc h5{font-size:13px;font-weight:700;margin-bottom:18px}
.fc a{display:block;font-size:14.5px;color:var(--ink2);margin-bottom:12px;transition:color .2s}
.fc a:hover{color:var(--ink)}
.fbiz{border-top:1px solid var(--line);padding-top:24px;display:flex;flex-wrap:wrap;gap:6px 22px;
  font-size:13px;color:var(--ink3);line-height:1.7}
.fbiz span{position:relative}
.fbot{padding-top:18px;font-size:13px;color:var(--ink4)}


/* ══ 문의 · 소개서 모달 ══ */
.mdl{position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
  padding:20px}
.mdl[hidden]{display:none}
.mdl-bg{position:absolute;inset:0;background:rgba(20,17,14,.55);backdrop-filter:blur(3px);
  animation:mdlBg .22s var(--e)}
@keyframes mdlBg{from{opacity:0}to{opacity:1}}
.mdl-box{position:relative;width:min(520px,100%);max-height:88vh;overflow-y:auto;
  background:var(--surf);border-radius:20px;box-shadow:0 40px 90px -30px rgba(26,23,20,.5);
  animation:mdlIn .28s var(--e)}
@keyframes mdlIn{from{opacity:0;transform:translateY(14px) scale(.985)}to{opacity:1;transform:none}}
.mdl-hd{position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:24px 26px 16px;background:var(--surf);border-bottom:1px solid var(--line)}
.mdl-hd h3{font-size:21px;font-weight:800;letter-spacing:-.045em}
.mdl-x{width:34px;height:34px;flex:none;border-radius:9px;font-size:22px;line-height:1;
  color:var(--ink3);background:transparent;transition:.2s var(--e)}
.mdl-x:hover{background:var(--paper2);color:var(--ink)}
#mdlF{padding:20px 26px 26px;display:flex;flex-direction:column;gap:14px}
.mdl-plan{background:var(--terraw,#FBF0E9);border:1px solid rgba(204,114,71,.25);
  border-radius:11px;padding:13px 16px;font-size:14px;font-weight:600;color:var(--ink2)}
.mdl-plan b{color:var(--terra);font-weight:800}
.mdl-plan[hidden]{display:none}
.mdl-d{font-size:14.5px;color:var(--ink3);line-height:1.6}
/* block 이어야 라벨 글자와 * 가 같은 줄에 남는다 (flex 로 하면 * 가 다음 줄로 떨어짐) */
#mdlF label.f,.mdl-2 label{display:block;font-size:14px;font-weight:700;color:var(--ink)}
#mdlF label.f>input,#mdlF label.f>textarea,.mdl-2 label>input{margin-top:7px}
#mdlF label.f[hidden]{display:none}
#mdlF label i{color:#C0553B;font-style:normal}
.mdl-2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
#mdlF input[type=text],#mdlF input:not([type]),#mdlF input[type=email],#mdlF textarea{
  width:100%;font:inherit;font-weight:500;font-size:15px;color:var(--ink);
  background:var(--paper2);border:1px solid transparent;border-radius:11px;padding:13px 14px;
  transition:.18s var(--e)}
#mdlF textarea{resize:vertical;min-height:84px;line-height:1.6}
#mdlF input::placeholder,#mdlF textarea::placeholder{color:var(--ink4);font-weight:400}
#mdlF input:focus,#mdlF textarea:focus{outline:none;background:#fff;border-color:var(--pet);
  box-shadow:0 0 0 3px rgba(14,87,102,.12)}
.mdl-chk{display:flex;align-items:center;gap:9px;font-size:13.5px;color:var(--ink3);cursor:pointer}
.mdl-chk input{width:17px;height:17px;flex:none;accent-color:var(--pet)}
.mdl-go{margin-top:4px;width:100%;padding:16px;font-size:16px;border-radius:12px;
  background:var(--terra);color:#fff;font-weight:800}
.mdl-go:hover{background:#B85F38}
.mdl-go:disabled{opacity:.6;cursor:default}
.mdl-msg{font-size:14px;line-height:1.55;text-align:center;padding:2px 4px}
.mdl-msg.ok{color:var(--pet);font-weight:700}
.mdl-msg.err{color:#B4472C;font-weight:700}
.mdl-msg[hidden]{display:none}

@media(max-width:1080px){
  /* PC 전용 / 모바일 전용 전환 — 모바일뷰는 스토리를 다르게 구성한다 */
  .pc-only{display:none!important}
  .mob-only{display:block}


  /* 모달 — 좁은 화면에서는 아래에서 올라오는 시트로 */
  .mdl{padding:0;align-items:flex-end}
  .mdl-box{width:100%;max-height:92vh;border-radius:20px 20px 0 0}
  .mdl-hd{padding:20px 20px 14px}
  .mdl-hd h3{font-size:19px}
  #mdlF{padding:16px 20px 24px;gap:12px}
  .mdl-2{gap:10px}
  #mdlF input,#mdlF textarea{font-size:16px}   /* iOS 자동 확대 방지 */
  .sgrid{grid-template-columns:minmax(0,1fr)}

  /* 중요 섹션은 스크롤이 한 번 멈췄다 넘어가도록 스냅 지점을 준다.
     proximity 라서 나머지 구간(핀 고정된 WHY·프로세스)은 그대로 자유롭게 스크롤된다. */
  html{scroll-snap-type:y proximity;scroll-padding-top:66px}
  .wmsg,#genai,#cases,#pricing,.end{scroll-snap-align:start;scroll-snap-stop:always}

  /* ── 히어로 ── 3줄 카피 · 전체 좌측 정렬 · CTA 한 줄 · 로고 마퀴는 영상 최하단 고정 */
  .heroWrap{height:100svh}
  .film{inset:0;border-radius:0}
  .hero-in{text-align:left}
  /* 한글 2줄은 크되 가볍게(600), 핵심 키워드는 한 줄을 꽉 채우는 볼드(800)로 무게를 준다 */
  .hero .mob-h{text-align:left;margin:0;max-width:none;font-size:clamp(26px,8.1vw,33px);
    font-weight:600;line-height:1.26;letter-spacing:-.05em}
  .hero .mob-h .l1 b,.hero .mob-h .l2 b{font-weight:600}
  /* 슬로건보다 핵심 키워드를 한 단계 크고 굵게 — 위계를 만든다 */
  .hero .mob-h .l3{margin-top:11px;font-size:1.09em;letter-spacing:-.05em}
  .hero .mob-h .l3 b{font-weight:800}
  .roll{align-items:flex-start;margin-top:96px}
  .roll-t{width:auto}
  .rk{left:0;transform:translateX(0) translateY(14px)}
  .rk.on{transform:translateX(0) translateY(0)}
  /* .tip 래퍼가 flex 아이템이므로 버튼이 아니라 래퍼에 균등 분배를 걸어야 두 버튼 폭이 같아진다 */
  .hero-cta{justify-content:flex-start;flex-wrap:nowrap;gap:9px;width:100%;margin-bottom:0}
  .hero-cta>*{flex:1 1 0;min-width:0}
  .hero-cta .tip{display:flex}
  .hero-cta .btn{min-width:0;width:100%;padding:14px 8px;font-size:13.5px;white-space:nowrap;
    justify-content:center}
  .hero-mq{display:block;position:absolute;left:0;right:0;z-index:3;
    bottom:calc(18px + env(safe-area-inset-bottom,0px));overflow:hidden;
    -webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);
    mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
  .hero-mq-track{display:flex;align-items:center;gap:32px;width:max-content;
    animation:mqScroll 22s linear infinite}
  .hero-mq img{width:auto;filter:brightness(0) invert(1);opacity:.8;position:relative}
  @keyframes mqScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}

  /* ── WHY ── PC와 같은 핀 고정 스택. 카드가 위로 날아가며 다음 카드가 드러난다.
     스테이지에 overflow:hidden 을 걸어 지나간 카드가 위 헤드카피를 침범하지 않게 한다. */
  .why-st{padding:82px 0 34px}
  .why-h{margin-bottom:22px}
  .why-stage{padding:0 20px;height:min(400px,54vh);overflow:hidden}
  .wc{left:20px;right:20px;border-radius:20px;
    grid-template-columns:none;grid-template-rows:140px minmax(0,1fr)}
  .wc.ans{display:none}
  .wc-r{order:-1;min-height:0}
  /* 도형마다 그려진 크기가 달라 균일해 보이도록: svg 는 높이 기준, HTML 도형은 개별 축소 */
  .wc-r .gfx{transform:none}
  .wc-r .gx>svg{width:auto;height:88%}
  .wc-r .gx0{transform:scale(.62)}
  .wc-r .gx3{transform:scale(.66)}
  .wc-l{padding:16px 22px 20px;justify-content:center}
  .wc .no{font-size:12.5px;margin-bottom:7px}
  /* 따옴표를 문장 흐름에서 빼내 바깥에 두고, 문장만 가운데 정렬시킨다.
     따옴표가 있는 카드는 폭을 문장에 맞춰 좁혀야 따옴표가 코멘트에 붙어 보인다. */
  .wc h3{font-size:clamp(20px,5.9vw,25px);margin-bottom:9px;position:relative;padding:0 14px}
  .wc[data-i="1"] h3,.wc[data-i="2"] h3,.wc[data-i="3"] h3{
    max-width:11.6em;margin-left:auto;margin-right:auto}
  .wc h3 .qo,.wc h3 .qc{position:absolute;margin:0;top:auto;font-size:22px;line-height:1;
    color:var(--ink4);opacity:.55}
  .wc h3 .qo{left:0;top:1px}
  .wc h3 .qc{right:0;bottom:1px}
  .wc p{font-size:13px;line-height:1.62}
  .wcb.brk h3::before,.wcb.brk h3::after{display:none}
  .why-dots{margin-top:16px}

  /* ── 상품소개 ── 앞뒤 크림색 섹션과 확실히 구분되도록 짙은 틸 블루로 */
  /* isolation 이 있어야 형광펜(::before, z-index:-1)이 섹션 배경 뒤로 숨지 않는다.
     한 화면을 통째로 차지하게 해서 스크롤이 확실히 머물다 넘어가도록 한다. */
  .wmsg{padding:96px 0 100px;text-align:center;isolation:isolate;
    min-height:100svh;display:flex;align-items:center;
    background:linear-gradient(168deg,#2A5C68 0%,#0E5766 46%,#08333D 100%)}
  .wmsg .wrap{width:100%}
  .wmsg h2{font-size:clamp(23px,6.8vw,30px);font-weight:800;letter-spacing:-.045em;
    line-height:1.4;color:#fff}
  .wmsg h2 .q{color:#7FD4CB}
  /* 엔딩과 같은 형광펜 — 어두운 바탕에서는 반투명이 탁해지므로 불투명 마커에 글자를 뒤집는다 */
  .wmsg h2 .hlmark{color:#0B2C35}
  .wmsg h2 .hlmark::before{background:#EBA875}
  .wmsg.cur h2 .hlmark::before{transform:rotate(-.8deg) scaleX(1)}
  .wmsg-gfx{width:min(196px,54%);margin:22px auto 18px;aspect-ratio:1/1;position:relative}
  .wmsg-gfx .gx{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
  .wmsg-gfx svg{width:100%;height:100%}
  .wmsg p{font-size:15px;color:rgba(255,255,255,.76);line-height:1.74}
  .wmsg p b{color:#7FD4CB;font-weight:800}
  /* 제안이 각 기업으로 뻗어나가는 동작을 한 번만 하지 않고 계속 반복한다 */
  .wmsg.cur .gx4 .ray{animation:rayLoop 3.4s ease-in-out infinite}
  .wmsg.cur .gx4 .r1{animation-delay:0s}
  .wmsg.cur .gx4 .r2{animation-delay:.22s}
  .wmsg.cur .gx4 .r3{animation-delay:.44s}
  .wmsg.cur .gx4 .tgt{animation:tgtLoop 3.4s ease-in-out infinite}
  .wmsg.cur .gx4 .t1{animation-delay:.5s}
  .wmsg.cur .gx4 .t2{animation-delay:.72s}
  .wmsg.cur .gx4 .t3{animation-delay:.94s}
  @keyframes rayLoop{0%{stroke-dashoffset:170}28%,74%{stroke-dashoffset:0}100%{stroke-dashoffset:170}}
  @keyframes tgtLoop{0%,12%{opacity:0}30%,74%{opacity:1}100%{opacity:0}}

  /* ── 프로세스 ── 트랙마다 핀 고정, 스크롤 진행도로 4단계를 차례로 넘긴다.
     헤드카피는 두 트랙을 지나는 동안 상단에 붙어 있다가 섹션이 끝나면 함께 사라진다.
     --ph 는 헤드카피 실제 높이로, JS 가 재어 넣는다. */
  /* 상단 고정 네비(66px) 아래에 헤드카피가 붙어야 글자가 가려지지 않는다 */
  .proc-m{position:relative;--navh:66px}
  .proc-m{padding-top:56px}
  .proc-m .proc-h{position:sticky;top:var(--navh);z-index:4;background:var(--paper2);
    padding:18px 20px 14px;text-align:center}
  .proc-m .proc-h h2{font-size:clamp(22px,6.2vw,29px);font-weight:800;
    letter-spacing:-.05em;line-height:1.3}
  .proc-m .proc-h h2 .q{color:var(--pet)}
  .mtrk{position:relative}
  .mtrk-in{position:sticky;top:calc(var(--navh) + var(--ph,0px));
    min-height:calc(100svh - var(--navh) - var(--ph,0px));
    display:flex;flex-direction:column;justify-content:flex-start;padding:18px 20px 28px}
  .mtag{display:flex;justify-content:center;margin-bottom:18px}
  .mtag span{display:inline-block;padding:10px 20px;border-radius:999px;font-size:13.5px;
    font-weight:800;letter-spacing:-.03em;color:#fff}
  .mtrk[data-t="0"] .mtag span{background:var(--terra)}
  .mtrk[data-t="1"] .mtag span{background:var(--pet)}
  .mfnav{display:flex;flex-direction:column;gap:2px;margin-bottom:18px}
  .mfnav .fb{font-size:15px;line-height:1.5;white-space:normal;color:var(--ink4);
    padding:9px 0 9px 14px;border-left:3px solid var(--line);border-top:none;
    transition:.35s var(--e)}
  .mfnav .fb.on{color:var(--ink);font-weight:700}
  .mtrk[data-t="0"] .mfnav .fb.on{border-left-color:var(--terra)}
  .mtrk[data-t="1"] .mfnav .fb.on{border-left-color:var(--pet)}
  .mtrk .fstage{aspect-ratio:4/3;border-radius:14px}

  /* ── 가격 ── 가로 스와이프 캐러셀. Pro가 기본으로 중앙에 오도록 JS가 스크롤 위치를 잡는다 */
  #pricing .pg{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px;
    padding:4px 24px 10px;scrollbar-width:none;grid-template-columns:none;align-items:stretch}
  #pricing .pg::-webkit-scrollbar{display:none}
  /* 카드 하나가 한 화면에 다 들어오도록 줄간격·여백을 전반적으로 줄인다 */
  #pricing .pc{flex:0 0 86%;scroll-snap-align:center;padding:24px 22px}
  #pricing .pc h3{font-size:20px;margin-bottom:8px}
  #pricing .pp{margin-top:2px;font-size:28px}
  #pricing .pt{font-size:12px;margin-top:6px;padding-bottom:15px}
  #pricing .pin2{padding:14px 0;gap:8px}
  #pricing .pin2 .r{font-size:13px}
  #pricing .pfe{padding:15px 0 18px;gap:9px}
  #pricing .pfe li{font-size:13px;line-height:1.5;padding-left:22px}
  #pricing .pfe li::before{top:5px}
  #pricing .pc .btn{padding:13px 16px;font-size:14.5px}
  #pricing .pc .pb{top:18px;right:20px;font-size:11px;padding:5px 10px}
  /* 좌우로 넘길 수 있다는 표시 */
  .pgdots{display:flex;justify-content:center;gap:7px;margin-top:14px}
  .pgdots i{width:6px;height:6px;border-radius:50%;background:var(--line2,rgba(26,23,20,.18));
    transition:.3s var(--e)}
  .pgdots i.on{background:var(--pet);width:18px;border-radius:3px}
  /* 하단 고지 문구는 참고용이므로 작게 */
  .pn{grid-template-columns:minmax(0,1fr);margin-top:28px;padding-top:22px;gap:18px}
  .pn b{font-size:12.5px;margin-bottom:5px}
  .pn p{font-size:11.5px;line-height:1.56}
  .tg,.tw{grid-template-columns:minmax(0,1fr)}
  .tw-c.big{grid-row:auto}

  /* ── 고객사 코멘트 ── 라벨을 숫자 왼쪽에 붙여 카드 높이를 줄인다 */
  .tc .stat{margin-top:18px;display:flex;align-items:baseline;justify-content:space-between;gap:10px}
  .tc .bl{font-size:15px;margin-bottom:0;text-align:left;line-height:1.35}
  .tc .big{font-size:clamp(34px,9.4vw,44px)}

  /* ── 엔딩 ── 실사 블러 대신 딥 틸 블루, 서브카피+CTA 를 한 쌍씩 */
  .end{padding:104px 0 110px;background:linear-gradient(168deg,#0E5766 0%,#08333D 100%)}
  .end h2{font-size:clamp(27px,7.6vw,34px);max-width:none;color:#fff;text-shadow:none;line-height:1.34}
  /* 딥 틸 위에서는 반투명 마커가 회색으로 탁해진다(어두운 바탕과 섞이기 때문).
     그래서 불투명 형광펜으로 바꾸고 글자를 어둡게 뒤집는다. */
  .end .hlmark{color:#0B2C35}
  .end .hlmark::before{background:#EBA875}
  .end-m{margin-top:34px;display:flex;flex-direction:column;gap:26px}
  .end-opt p{font-size:14.5px;color:rgba(255,255,255,.8);line-height:1.6;margin-bottom:12px}
  .end-opt{text-align:center}
  .end-opt p b{color:#fff;font-weight:800}
  /* 두 CTA 폭을 동일하게 — 글자 수가 달라도 min-width 로 맞춘다 */
  .end-opt .btn{display:inline-flex;justify-content:center;width:auto;min-width:236px;
    padding:15px 22px;font-size:15px}
}
@media(max-width:768px){
  .wrap,.wrapw,nav .in,.hero-in,.why-h,.proc-h,.proc-b,.band-in{padding-left:20px;padding-right:20px}
  .pills{display:none}.burger{display:flex}
  /* 브랜드 로고 — 기존 대비 80% 크기로, 좀 더 왼쪽에 붙인다 (컬러 로고로 바꿔도 그대로 유지) */
  nav .in{height:66px;grid-template-columns:1fr auto;padding-left:12px}
  .brand .wm,.brand .dk{height:27px}
  section.s{padding:76px 0}
  .head{margin-bottom:36px}
  .head h2{font-size:clamp(25px,7vw,34px)}
  .head p{font-size:15.5px}
  .hero{padding:92px 0 96px}
  .hero h1{font-size:clamp(27px,7.6vw,34px)}
  .roll-f{font-size:14.5px}
  .rk{font-size:15px;gap:8px}
  .rk .pic{width:22px;height:22px}
  .hero-cta{gap:8px;margin-top:44px}
  .hero-cta .btn{padding:13px 6px;font-size:13px}
  .tip::after,.tip::before{display:none}
  .lgrid.a,.lgrid.b{grid-template-columns:repeat(2,minmax(0,1fr))}
  .lgrid.b .lfeat{grid-column:span 2}
  .lcell{min-height:86px}
  .lcell .lg{max-width:74%}
  .band-in{height:auto;padding-top:12px;padding-bottom:12px;gap:16px;justify-content:flex-start}
  .band-l{font-size:11px}
  .bs{font-size:11px;gap:7px}
  .bs em{font-size:12.5px;min-width:0;padding:3px 7px}
  .band-d{display:none}

  /* WHY */
  .why-st{padding:74px 0 30px}
  .why-h h2{font-size:clamp(23px,6.4vw,30px)}
  .wc{border-radius:18px}
  .gx0{gap:7%}
  .gx0 .env{width:37%}
  .gx0 .bdg{font-size:9.5px;padding:3px 8px;top:-13px}

  /* 시나리오 */
  .sbody{padding:22px 22px 26px}
  .scard h3{font-size:clamp(20px,5.6vw,25px)}
  .scard p{font-size:14.5px}

  /* 프로세스 */
  .proc-st{padding:76px 0 70px}
  .proc-h h2{font-size:clamp(24px,6.6vw,32px)}
  .trk{margin-top:22px;padding:4px;gap:2px}
  .trk button{font-size:12.5px;padding:9px 15px;letter-spacing:-.03em}
  .proc-b{margin-top:20px}
  .fstage{aspect-ratio:4/3;border-radius:14px}
  .fb{font-size:15px}
  .sub{font-size:10.5px;bottom:4%;left:5%;right:5%;line-height:1.45}
  /* 1-1 소개서 분석 */
  .sc.up .docw{width:40%}
  .cov .ctit{font-size:13px}
  .cov .cbadge{font-size:6.5px;padding:2px 5px}
  .cov .csub{font-size:5.5px;letter-spacing:.1em}
  .cov .cmark{font-size:7.5px}
  .cov .cdots i{width:7px;height:7px}
  .sc.up .chip{width:33%;padding:8px 10px;border-radius:9px}
  .sc.up .ck{font-size:7px}
  .sc.up .cv{font-size:9px;line-height:1.35}
  .sc.up .c1{left:3%;top:8%}
  .sc.up .c2{right:3%;top:12%}
  .sc.up .c3{left:3%;bottom:20%}
  .sc.up .c4{right:3%;bottom:15%}
  /* 1-2 실사형 멀티 윈도우 */
  .sc.flt .win{border-radius:8px}
  .sc.flt .wv{left:3%;top:7%;width:50%}
  .sc.flt .wn{right:2%;top:30%;width:56%}
  .sc.flt .wj{left:6%;bottom:15%;width:54%}
  .sc.flt .vplay{width:26px;height:18px}
  .sc.flt .vdur{font-size:6.5px}
  .sc.flt .vmeta{padding:6px 7px 8px;gap:6px}
  .sc.flt .vav{width:16px;height:16px;font-size:8px}
  .sc.flt .vtx b{font-size:8.5px}
  .sc.flt .vtx u{font-size:6.5px}
  .sc.flt .nhd{padding:5px 8px;gap:5px}
  .sc.flt .nlogo{font-size:7px;padding:1px 5px}
  .sc.flt .ncat,.sc.flt .ndate{font-size:6.5px}
  .sc.flt .nbody{padding:7px 8px 8px;gap:3px}
  .sc.flt .nti{font-size:9.5px}
  .sc.flt .nld{font-size:7px;line-height:1.5}
  .sc.flt .nfoot{font-size:6.5px}
  .sc.flt .jhd{padding:5px 8px;gap:5px}
  .sc.flt .jlogo{width:14px;height:14px;font-size:7px}
  .sc.flt .jco{font-size:7.5px}
  .sc.flt .jnew{font-size:6.5px;padding:1px 5px}
  .sc.flt .jbody{padding:7px 8px 8px;gap:4px}
  .sc.flt .jti{font-size:9px}
  .sc.flt .jtags i{font-size:6px;padding:1px 5px}
  .sc.flt .jfoot{font-size:6.5px}
  .sc.flt .onecard{left:5%;right:5%}
  /* 기업 카드 (1-2 · 1-3 공용) */
  .ecard,.scr .ecard{grid-template-columns:20px minmax(0,1fr) 36px;gap:8px;
    padding:7px 10px;border-radius:8px}
  .ecard .ectc,.ecard .ego{display:none}
  .ecard .eini,.scr .ecard .eini{width:20px;height:20px;border-radius:6px;font-size:9.5px}
  .ecard .enm,.scr .ecard .enm{font-size:10.5px}
  .ecard .enm em{font-size:7.5px;padding:1px 5px}
  .ecard .enm small,.scr .ecard .enm small{font-size:8.5px}
  .ecard .esc,.scr .ecard .esc{font-size:13px}
  /* 1-3 우선순위 */
  .sc.scr{padding:4% 5% 13%}
  .scr .swin{height:84%}
  .scr .srail{gap:5px}
  /* 1-4 대시보드 */
  .sc.res{padding:3.5% 4% 13%}
  .res .dash{padding:9px 10px 10px;gap:6px;border-radius:10px}
  .res .fi{width:19px;height:19px;border-radius:6px;font-size:9.5px}
  .res .dnm b{font-size:10.5px}
  .res .dnm small{display:none}
  .res .live{font-size:7px;padding:3px 6px}
  .res .dtab{display:none}
  .res .kpis{grid-template-columns:repeat(4,minmax(0,1fr));gap:4px}
  .res .kpi{padding:5px 6px;border-radius:6px;gap:0}
  .res .kk{font-size:6.5px}
  .res .kpi b{font-size:11.5px}
  .res .spk{display:none}
  .res .kd{font-size:6px}
  .res .kd em{display:none}
  .res .dgrid{grid-template-columns:minmax(0,1fr);gap:5px;min-height:92px}
  .res .chart{display:none}
  .res .pnl{padding:6px 8px;gap:4px;border-radius:6px}
  .res .pnt{font-size:7.5px}
  .res .iv{font-size:7.8px;white-space:normal;line-height:1.35;letter-spacing:-.04em}
  .res .iv.hit{margin-top:4px}
  .res .insight{justify-content:flex-start}
  .res .iv.hit{font-size:9.5px}
  /* 2-1 제안 논리 */
  .sc.lgc .bldg{left:20%;width:26%}
  .sc.lgc .bldg b{font-size:9.5px}
  .sc.lgc .bldg u{font-size:7.5px}
  .sc.lgc .lwin{width:56%;padding:6px 9px;border-radius:8px}
  .sc.lgc .lk{font-size:7px}
  .sc.lgc .lv{font-size:9px;line-height:1.35}
  .sc.lgc .lm{font-size:7px}
  .sc.lgc .lw1{right:3%;top:6%}
  .sc.lgc .lw2{right:8%;top:30%}
  .sc.lgc .lw3{right:2%;top:54%}
  .sc.lgc .lw4{right:9%;bottom:8%}
  .sc.lgc .lout{left:4%;right:4%;padding:13px 14px;border-radius:11px;gap:6px}
  .sc.lgc .lt{font-size:8px}
  .sc.lgc .ln{font-size:10px;padding:5px 9px;border-radius:5px}
  /* 2-2 이메일 */
  /* 메일 폼 — 좁은 화면에서 본문이 자막을 침범하지 않도록 줄간격·여백을 줄인다 */
  .sc.mal{padding:3.5% 4% 15%}
  .mal .mwin{padding:9px 12px 10px;gap:5px;border-radius:10px}
  .mal .mlang span{font-size:8px;padding:3px 8px}
  .mal .mf{font-size:8px;width:42px}
  .mal .mv{font-size:10px}
  .mal .mh{padding-bottom:6px;gap:8px}
  .mal .mb{gap:2px;margin-top:3px}
  .mal .mb .bl{font-size:8.5px;line-height:1.22}
  /* 2-3 전송 */
  .sc.snd .mini{left:3%;top:16%;width:38%;padding:7px 8px;border-radius:9px;gap:3px}
  .sc.snd .mbody .mbl:not(.hl){display:none}
  .sc.snd .mbl{font-size:6px}
  .sc.snd .mbl.hl{padding:1px 3px;white-space:nowrap;overflow:hidden;
    text-overflow:ellipsis;max-width:100%;align-self:stretch}
  .sc.snd .mkt{font-size:6.5px;padding-bottom:3px}
  .sc.snd .obtn{margin-top:2px}
  .sc.snd .mkt{font-size:6.5px}
  .sc.snd .emk{font-size:6.5px;width:30px}
  .sc.snd .emv{font-size:7.5px}
  .sc.snd .mbl{font-size:6.5px;line-height:1.4}
  .sc.snd .obtn{font-size:8px;padding:5px 7px;border-radius:5px}
  .sc.snd .flyA,.sc.snd .flyB{left:36%;width:14%}
  .sc.snd .flyA{height:7px;top:42%}
  .sc.snd .flyB{height:15px;top:47.8%}
  /* 아웃룩 창 — 위로 올려 자막과 간격을 만들고, 본문이 창 밖으로 나가지 않게 줄인다 */
  .sc.snd .olk{right:3%;top:33%;width:54%;border-radius:9px;overflow:hidden}
  .sc.snd .omain{padding:6px 7px 7px;gap:3px}
  .sc.snd .ofld{padding-bottom:3px;gap:5px}
  .sc.snd .ok{font-size:6px;width:28px}
  .sc.snd .ov{font-size:7.5px}
  .sc.snd .obd{font-size:6.5px;line-height:1.4}
  .sc.snd .obar{padding:5px 8px}
  .sc.snd .obar b{font-size:8px}
  .sc.snd .ologo{width:11px;height:11px;font-size:7px}
  .sc.snd .oside{padding:6px 5px;gap:3px}
  .sc.snd .oi{font-size:6.5px;padding:3px 4px}
  .sc.snd .omain{padding:7px 9px 9px;gap:4px}
  .sc.snd .ok{font-size:6.5px;width:34px}
  .sc.snd .ov{font-size:8px}
  .sc.snd .obd{font-size:7px;line-height:1.45}
  .sc.snd .osend{font-size:7.5px;padding:4px 9px}
  /* 2-4 제안서 — 미리보기와 장표 썸네일을 위로 올려 하단 자막과 겹치지 않게.
     폭을 %가 아닌 고정 px로 잡아야 기기 폭이 달라져도 장표 내부가 재배치되며 깨지지 않는다.
     세로는 헤드라인 → 본문 → 표 순으로 구간을 나누고, 지도는 헤드라인 아래에서 시작한다. */
  .sc.dck .build{width:252px;top:34%}
  .sc.dck .btag{font-size:6px;padding:3px 6px}
  .sc.dck .bt{font-size:7.5px;left:30%}
  .sc.dck .bbody{font-size:5.5px;top:30%;width:46%;line-height:1.4}
  .sc.dck .btbl{bottom:5%;top:auto}
  .sc.dck .btbl i{grid-template-columns:minmax(0,1fr) 26px 20px;padding:1.8px 3px}
  .sc.dck .btbl u{font-size:5px}
  .sc.dck .bmap{right:2%;width:42%;top:31%;bottom:5%}
  .sc.dck .pages{grid-template-columns:repeat(7,minmax(0,1fr));gap:2.5px;top:55%;left:4%;right:4%}
  .sc.dck .pgz{border-radius:3px}

  /* 범용 AI 비교 */
  .cmpsec{padding:76px 0 70px}
  .cmphead{margin-bottom:28px}
  .cmpq{font-size:16.5px;margin-bottom:9px}
  .cmphead h2{font-size:clamp(23px,6.3vw,30px)}
  /* 표를 하나의 큰 박스로 두면 전체 폭 질문 행이 틸 컬럼을 가로질러 '잘린' 것처럼 보인다.
     그래서 질문은 배경 위로 빼고, 답변 한 쌍만 카드로 묶어 질문별 카드 목록으로 만든다. */
  /* 질문과 답변이 따로 떠 보이던 문제 — 표 전체를 한 톤 낮은 레이어로 감싸 묶어준다 */
  .cmp{background:var(--paper2);box-shadow:none;border:1px solid var(--line);
    border-radius:18px;padding:20px 16px;overflow:visible}
  .cmpcol{display:none}
  .cmphd{grid-template-columns:minmax(0,1fr) minmax(0,1fr);padding-left:0;
    background:none;margin-bottom:14px}
  /* 두 진영 사이가 비어 보이지 않도록 가운데 vs 표시 */
  .cmphd::after{content:'vs';position:absolute;left:50%;top:50%;
    transform:translate(-50%,-50%);font-size:12.5px;font-weight:800;
    color:var(--ink4);letter-spacing:0}
  .cmphd span:first-child{display:none}
  .cmphd span{font-size:16.5px;font-weight:800;padding:0;text-align:center;
    background:none;color:var(--ink);border:0}
  .cmphd span.on{color:var(--pet);background:none}
  .cmpr{grid-template-columns:minmax(0,1fr) minmax(0,1fr);grid-template-areas:'k k' 'a b';
    border-top:0;margin-bottom:12px;background:none}
  .cmpr:last-child{margin-bottom:0}
  /* .cmpr>div 가 .cmpa/.cmpb 보다 특정도가 높아 여백을 여기서 먼저 0으로 되돌린다 */
  .cmpr>div{padding:0;gap:2px}
  .cmpk{grid-area:k;background:none!important;padding:0 2px 7px!important;text-align:center;
    font-size:14.5px;font-weight:800;letter-spacing:-.035em;color:var(--terra)}
  /* 답변 박스는 min-height 로 높이를 맞춰 4행이 한 눈에 들어오게 한다 */
  .cmpr>.cmpa,.cmpr>.cmpb{min-height:50px;justify-content:center;padding:10px 13px}
  .cmpr>.cmpa{background:#fff;border-color:rgba(26,23,20,.10);
    box-shadow:0 1px 3px rgba(26,23,20,.05)}
  .cmpr>.cmpb{box-shadow:0 1px 3px rgba(14,87,102,.18)}
  .cmpa{grid-area:a;background:var(--surf);border:1px solid var(--line);border-right:0;
    border-radius:13px 0 0 13px}
  .cmpb{grid-area:b;background:var(--pet);border-radius:0 13px 13px 0}
  .cmpa b,.cmpb b{font-size:14px;line-height:1.4}
  .cmpa small,.cmpb small{font-size:10.5px;line-height:1.5}
  .cmpend{margin-top:32px}
  .cmpend .cmpend1{font-size:clamp(23px,6.3vw,30px);margin-bottom:4px}
  .cmpend .cmpend2{font-size:19px;line-height:1.46}

  /* 도입 사례 */
  .overlap{padding:80px 0 84px;border-radius:24px 24px 0 0;margin-top:-32px}
  .tc{padding:24px 22px;min-height:0}
  .tc .qt{font-size:16px}
  .tc .who{font-size:13.5px;margin-bottom:14px}
  .tc .qo,.tc .qc{font-size:21px}
  .tc .stat{margin-top:20px}
  .tc .big{font-size:44px}
  .tc .bl{font-size:20px;margin-bottom:4px}

  .end{padding:88px 0}
  .end h2{font-size:clamp(25px,7.2vw,34px)}
  .end p{font-size:15px}
  .end .row{flex-direction:column;align-items:stretch}
  .end .row .btn{min-width:0;width:100%}
  .fc{gap:32px}
  .fb2 p{white-space:normal}
  .fbiz{flex-direction:column;gap:4px}
}
@media(prefers-reduced-motion:reduce){
  *{transition-duration:.01ms!important;animation-duration:.01ms!important;scroll-behavior:auto!important}
  .rv{opacity:1;transform:none}
  .wc{opacity:1;transform:none}
}
"""
