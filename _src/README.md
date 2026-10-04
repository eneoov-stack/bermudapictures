# 버뮤다픽쳐스 홈페이지

**고치는 법 (어느 컴퓨터에서든)**: 이 저장소를 받고 `_src/data/site.json`(문구·작업·연락처)이나 `style.css`·`site.js`를 고친 뒤 `python _src/tools/build.py` → 커밋 → push. 1분 안팎으로 https://bermudapictures.kr 에 반영된다. 작업 카드 장면은 `assets/works/<영상id>.webp`.

2026-10-04 착수. 옛 시안 `K:\버뮤다픽쳐스 웹사이트`(2026-04-28)의 톤(검정 + 주황)과 히어로 이미지·로고를 가져와 새로 지었다.

사용자 결정 (2026-10-04)
- 첫 판은 결제 없이. 강의 소개, 멤버십 가입 링크, 작업·출강, 문의.
- 무료 주소로 먼저, 도메인은 나중에.
- 살린 섹션: 강의·채널 소개, 포트폴리오·출강 이력. 무료 자료실과 AI Radar는 뺐다.

구조
- `data/site.json` — 사람이 고치는 값(시리즈, 재생목록 순서, 멤버십, 작업, 출강, 연락처).
- `data/channel.json` — `tools/fetch_channel.py`가 유튜브 API에서 읽기 전용으로 가져온다. 공개 영상만.
- `tools/build.py` — 둘을 합쳐 `site/index.html`을 만든다. `site/style.css`는 손으로 고친다.
- 갱신: `python tools/fetch_channel.py && python tools/build.py`
- 미리보기: `.claude/launch.json`의 `bermuda-website` (포트 8790).

글꼴: Pretendard(OFL, jsDelivr). 옛 시안의 210 수명조·NEXON 글꼴 파일은 웹 배포 라이선스를 확인하지 않아 가져오지 않았다.

## 개편 2026-10-04 (사용자 지시)

- 유튜브 채널이 아니라 브랜드 「버뮤다픽쳐스」를 알리는 사이트다. 구독자·강의 수·재생목록은 싣지 않는다.
- 한 장 스크롤에서 탭 넷(홈 `index.html`, 작업 `works.html`, 교육 `education.html`, 문의 `contact.html`)으로 나눴다.
- 작업은 에어메이드 포트폴리오(`https://airmade.netlify.app` 의 `data/portfolio_items.json`, 사본 `data/airmade_portfolio_items.json`)를 바탕으로: 홍보영상 그대로, 스팟에서 아르테미스 베개 뺌, AI에 2026 청남대 가을축제·격이 다른 진천 추가, 행사 중계 그대로, 프로그램 대신 모션 그래픽(저탄소 벼, 고향사랑기부제, 충청북도의회 CF 인포그래픽).
- 작업 영상은 일부 공개 유튜브를 페이지 안 라이트박스(youtube-nocookie)로 연다.
- 공개: 저장소 eneoov-stack/bermudapictures, GitHub Pages main → https://bermudapictures.kr (가비아 2026-10-04~2028-10-04, DNS A 넷 + www CNAME, site/CNAME 파일)
- 갱신: `data/site.json` 고친 뒤 `python tools/build.py`, `site/` 에서 커밋·push. `fetch_channel.py`는 이제 빌드에 쓰지 않는다.
- 작업 카드 (2026-10-04): Artlist 모델 카드 형식. 장면 22장은 `site/assets/works/<영상id>.webp` (글자 없는 장면, `tools/pick_frames.py`로 뽑음). 영상은 720p 화면만 받아 장면을 고른 뒤 휴지통으로 보냈다. 중계 영상은 앞 10분만 받았다(사용자 지시). 장면 파일이 없는 영상은 유튜브 썸네일로 대신 뜬다.
