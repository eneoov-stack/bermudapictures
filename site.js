// 버뮤다픽쳐스 홈페이지 — 작업 영상 라이트박스, 분류 칩, 움직임 줄이기
(function () {
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hv = document.querySelector(".hero-video");
  if (hv && reduce) { hv.removeAttribute("autoplay"); hv.pause(); }

  // 작업 카드를 누르면 유튜브 영상을 페이지 안에서 연다
  var lb = document.querySelector(".lightbox");
  var frame = lb && lb.querySelector(".lb-frame");
  var last = null;
  function open(vid) {
    frame.innerHTML = '<iframe src="https://www.youtube-nocookie.com/embed/' + vid + '?autoplay=1&rel=0" title="영상" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
    lb.hidden = false; document.body.style.overflow = "hidden";
    lb.querySelector(".lb-close").focus();
  }
  function close() {
    lb.hidden = true; frame.innerHTML = ""; document.body.style.overflow = "";
    if (last) last.focus();
  }
  document.addEventListener("click", function (e) {
    var w = e.target.closest(".work");
    if (w) { last = w; open(w.dataset.vid); return; }
    if (lb && !lb.hidden && (e.target === lb || e.target.closest(".lb-close"))) close();
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && lb && !lb.hidden) close(); });

  // 작업 페이지 분류 칩
  var chips = document.querySelectorAll(".chip");
  if (!chips.length) return;
  function filter(name) {
    chips.forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.filter === name)); });
    document.querySelectorAll(".cat").forEach(function (s) { s.hidden = !(name === "all" || s.dataset.cat === name); });
  }
  chips.forEach(function (c) { c.addEventListener("click", function () { filter(c.dataset.filter); }); });
  var m = location.hash.match(/^#cat-(\d+)$/);
  if (m) { var c = document.getElementById("cat-" + m[1]); if (c) filter(c.dataset.filter); }
})();
