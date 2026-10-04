#!/usr/bin/env python3
"""버뮤다픽쳐스 홈페이지 빌드 (2026-10-04 개편). data/site.json -> site/*.html
브랜드 홍보 사이트다. 유튜브 채널 숫자(구독자·강의 수·재생목록)는 싣지 않는다 (사용자 2026-10-04).
탭 넷이 각각 다른 페이지다: 홈 / 작업 / 교육 / 문의.
usage: python build.py
"""
import html
import json
from datetime import datetime
from pathlib import Path

# 저장소 bermudapictures 안에서 돈다: 사이트 파일은 저장소 뿌리, 원본은 _src/ (2026-10-04, 회사·집 어디서든 고칠 수 있게)
BASE = Path(__file__).resolve().parents[1]          # _src/
SITE = json.loads((BASE / "data" / "site.json").read_text(encoding="utf-8"))
OUT = BASE.parent                                    # 저장소 뿌리 = 게시되는 사이트
E = html.escape
YT = "https://www.youtube.com"
CHANNEL = f"{YT}/@bermudapictures"
TABS = [("index.html", "홈"), ("works.html", "작업"), ("education.html", "교육"), ("contact.html", "문의")]


CAT_OF = {i["id"]: w["name"] for w in SITE["works"] for i in w["items"]}


def thumb(vid):
    # 글자 없는 장면 한 장(tools/pick_frames.py가 만든다). 없으면 유튜브 썸네일로 대신한다
    own = OUT / "assets" / "works" / f"{vid}.webp"
    return f"assets/works/{vid}.webp" if own.exists() else f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"


def work_card(w, cat=""):
    # Artlist 모델 카드처럼: 장면이 카드를 꽉 채우고, 아래쪽 흐림 위에 제목과 한 줄 (사용자 2026-10-04)
    cat = cat or CAT_OF.get(w["id"], "")
    sub = " · ".join(x for x in (cat, w.get("year", "")) if x)
    return (f'<button class="work" type="button" data-vid="{w["id"]}" data-cat="{E(cat)}" aria-label="{E(w["title"])} 재생">'
            f'<img src="{thumb(w["id"])}" alt="" loading="lazy"><span class="shade" aria-hidden="true"></span>'
            f'<span class="meta"><strong>{E(w["title"])}</strong><span class="sub">{E(sub)}</span></span>'
            f'<i class="play" aria-hidden="true"></i></button>')


def asset_ver():
    # 고칠 때마다 CSS·JS 주소가 바뀌게 해서 방문자 브라우저가 옛 파일을 쓰지 않게 한다
    import hashlib
    h = hashlib.sha1()
    for f in ("style.css", "site.js"):
        h.update((OUT / f).read_bytes())
    return h.hexdigest()[:8]


def page(file, title, desc, body, extra_js=""):
    v = asset_ver()
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{f}"{cur if f == file else ""}>{E(n)}</a>' for f, n in TABS)
    c = SITE["contact"]
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="assets/hero-poster.jpg">
<link rel="icon" href="assets/logo.png">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="style.css?v={v}">
</head>
<body>
<header class="top">
 <nav class="tabs" aria-label="주 메뉴">{nav}</nav>
</header>
<main class="{"has-hero" if file == "index.html" else "no-hero"}">
{body}
</main>
<footer>
 <span>&copy; {datetime.now().year} BermudaPictures</span>
 <span class="links"><a href="mailto:{c["email"]}">{E(c["email"])}</a><a href="{CHANNEL}" target="_blank" rel="noopener">YouTube</a><a href="{c["instagram"]}" target="_blank" rel="noopener">Instagram</a></span>
</footer>
<div class="lightbox" hidden><div class="lb-in"><button class="lb-close" type="button" aria-label="닫기"></button><div class="lb-frame"></div></div></div>
<script src="site.js?v={v}"></script>{extra_js}
</body>
</html>
'''


works = SITE["works"]
featured = [works[2]["items"][0], works[2]["items"][1], works[0]["items"][1], works[1]["items"][0]]
c = SITE["contact"]
m = SITE["membership"]

# ---------------------------------------------------------------- 홈
home = f'''
<section class="hero">
 <video class="hero-video" autoplay muted loop playsinline preload="metadata" poster="assets/hero-poster.jpg" aria-hidden="true">
  <source src="assets/hero.webm" type="video/webm"><source src="assets/hero.mp4" type="video/mp4">
 </video>
 <div class="hero-in">
  <p class="eyebrow">Bermuda Pictures</p>
  <h1>영상을 만들고<br><span>만드는 법</span>을 나눕니다</h1>
  <p class="lead">홍보영상과 스팟, AI 영상을 직접 만들고, 그 과정을 강의로 나누는 영상 제작 브랜드예요.</p>
  <div class="actions">
   <a class="button primary" href="works.html">작업 보기</a>
   <a class="button ghost" href="contact.html">제작 문의</a>
  </div>
 </div>
</section>

<section class="section">
 <p class="eyebrow">What we do</p>
 <h2>버뮤다픽쳐스가 하는 일</h2>
 <div class="pillars">
  <a class="pillar" href="works.html#cat-0"><span class="num">01</span><h3>영상 제작</h3><p>공공기관과 기업의 홍보영상, 스팟, 행사 중계를 기획부터 마감까지 만들어요.</p></a>
  <a class="pillar" href="works.html#cat-2"><span class="num">02</span><h3>AI 영상</h3><p>캐릭터 시트, 프리비즈, 생성, 마감까지 AI로 만드는 영상 제작 흐름을 실제 납품에 써요.</p></a>
  <a class="pillar" href="education.html"><span class="num">03</span><h3>교육</h3><p>학원과 대학에서 영상 제작을 가르치고, 유튜브에서 강의를 이어 가요.</p></a>
 </div>
</section>

<section class="section">
 <div class="head-row"><div><p class="eyebrow">Portfolio</p><h2>포트폴리오</h2></div><a class="more" href="works.html">전체 보기</a></div>
 <div class="grid four">{"".join(work_card(w) for w in featured)}</div>
</section>

<section class="section cta">
 <h2>만들고 싶은 영상이 있으세요?</h2>
 <p class="lead">홍보영상, 스팟, AI 영상, 강의 문의를 받아요.</p>
 <div class="actions"><a class="button primary" href="contact.html">문의하기</a></div>
</section>
'''

# ---------------------------------------------------------------- 작업
chips = "".join(f'<button class="chip" type="button" data-filter="{E(w["name"])}" id="cat-{i}">{E(w["name"])}</button>' for i, w in enumerate(works))
works_body = f'''
<section class="section page-head">
 <p class="eyebrow">Works</p>
 <h1 class="page-title">작업</h1>
 <p class="lead">공공기관·기업 홍보영상부터 AI 영상, 모션 그래픽까지 직접 만든 작업이에요.</p>
 <div class="chips" role="group" aria-label="분류"><button class="chip" type="button" data-filter="all" aria-pressed="true">전체</button>{chips}</div>
</section>
''' + "".join(
    f'<section class="section cat" data-cat="{E(w["name"])}"><h2>{E(w["name"])}</h2><div class="grid three">{"".join(work_card(it, w["name"]) for it in w["items"])}</div></section>'
    for w in works)

# ---------------------------------------------------------------- 교육
teach = "".join(f'<li><strong>{E(t["where"])}</strong><span>{E(t["what"])}</span></li>' for t in SITE["teaching"])
series = "".join(f'<li><h3>{E(s["name"])}</h3><p>{E(s["blurb"])}</p></li>' for s in SITE["series"])
member = "" if not m.get("show") else f'''
<section class="section">
 <div class="member-box">
  <div>
   <p class="eyebrow">Membership</p>
   <h2>AI 영상, 프롬프트까지</h2>
   <p class="lead">AI 제작과정 영상에 실제로 넣은 프롬프트 원문을 유튜브 멤버십 회원에게 드려요.</p>
   <ul>{"".join(f"<li>{E(p)}</li>" for p in m["perks"])}</ul>
  </div>
  <div class="price">
   <span class="tier">{E(m["tier"])}</span>
   <strong>{E(m["price"])}</strong>
   <a class="button primary" href="{m["join"]}" target="_blank" rel="noopener">멤버십 가입하기</a>
   <small>결제와 해지는 유튜브 채널 멤버십으로 해요.</small>
  </div>
 </div>
</section>'''
edu_body = f'''
<section class="section page-head">
 <p class="eyebrow">Education</p>
 <h1 class="page-title">교육</h1>
 <p class="lead">현장에서 쓰는 방식 그대로 가르쳐요. 툴 사용법보다 영상을 끝까지 만드는 흐름을 먼저 잡아요.</p>
</section>
<section class="section">
 <h2>출강</h2>
 <ul class="teach">{teach}</ul>
</section>
<section class="section">
 <div class="head-row"><div><h2>온라인 강의</h2></div><a class="more" href="{CHANNEL}" target="_blank" rel="noopener">유튜브에서 보기</a></div>
 <ul class="series">{series}</ul>
</section>
{member}
'''

# ---------------------------------------------------------------- 문의
contact_body = f'''
<section class="section page-head contact">
 <p class="eyebrow">Contact</p>
 <h1 class="page-title">문의</h1>
 <p class="lead">영상 제작, AI 영상, 출강과 협업 문의는 메일로 받아요. 만들고 싶은 영상의 용도와 길이, 일정을 적어 주시면 빠르게 답할게요.</p>
 <div class="contact-cards">
  <a class="ccard" href="mailto:{c["email"]}"><span>메일</span><strong>{E(c["email"])}</strong></a>
  <a class="ccard" href="{c["instagram"]}" target="_blank" rel="noopener"><span>인스타그램</span><strong>@Bermuda._.Pictures</strong></a>
  <a class="ccard" href="{CHANNEL}" target="_blank" rel="noopener"><span>유튜브</span><strong>@bermudapictures</strong></a>
 </div>
</section>
'''

DESC = "영상을 만들고 만드는 법을 나누는 영상 제작 브랜드 버뮤다픽쳐스. 홍보영상, 스팟, AI 영상, 영상 교육."
pages = {
    "index.html": ("버뮤다픽쳐스 BermudaPictures | 영상 제작·AI 영상·영상 교육", DESC, home),
    "works.html": ("작업 | 버뮤다픽쳐스", "홍보영상, 스팟, AI 영상, 행사 중계, 모션 그래픽 작업.", works_body),
    "education.html": ("교육 | 버뮤다픽쳐스", "출강과 온라인 강의, AI 영상 멤버십.", edu_body),
    "contact.html": ("문의 | 버뮤다픽쳐스", "영상 제작·출강·협업 문의.", contact_body),
}
for f, (t, d, b) in pages.items():
    (OUT / f).write_text(page(f, t, d, b), encoding="utf-8")
print("ok", ", ".join(pages))
