/* Timbr Built - shared site scripts */
(function () {
  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // GCLID capture for offline conversion attribution
  // Priority: ?gclid= URL param -> sessionStorage -> _gcl_aw cookie (set by gtag.js)
  function getParam(name) {
    var m = window.location.search.match(new RegExp('[?&]' + name + '=([^&]+)'));
    return m ? decodeURIComponent(m[1]) : '';
  }
  function getCookieGclid() {
    var m = document.cookie.match(/(?:^|;\s*)_gcl_aw=([^;]+)/);
    if (!m) return '';
    var parts = decodeURIComponent(m[1]).split('.');
    return parts.length >= 3 ? parts.slice(2).join('.') : '';
  }
  var gclid = getParam('gclid');
  if (gclid) { try { sessionStorage.setItem('tb_gclid', gclid); } catch (e) {} }
  else { try { gclid = sessionStorage.getItem('tb_gclid') || ''; } catch (e) {} if (!gclid) gclid = getCookieGclid(); }
  document.querySelectorAll('form[data-track-gclid]').forEach(function (form) {
    var g = form.querySelector('input[name="gclid"]');
    var l = form.querySelector('input[name="landing_url"]');
    var r = form.querySelector('input[name="referrer"]');
    if (g) g.value = gclid;
    if (l) l.value = window.location.href;
    if (r) r.value = document.referrer || '';
  });

  // Deferred Google Ads conversion tracking (loads on first interaction or after 3s to protect LCP)
  // TODO before launch: replace AW-XXXXXXXXXXX + CONVERSION_LABEL with Timbr Built's real IDs.
  var loaded = false;
  function loadTracking() {
    if (loaded) return; loaded = true;
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag('js', new Date());
    gtag('config', 'AW-XXXXXXXXXXX');
    gtag('config', 'AW-XXXXXXXXXXX/CONVERSION_LABEL', { phone_conversion_number: '0484 698 553' });
    var s = document.createElement('script');
    s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXXX';
    document.head.appendChild(s);
  }
  var evts = ['scroll', 'pointerdown', 'keydown', 'touchstart'];
  function trigger() { evts.forEach(function (e) { window.removeEventListener(e, trigger); }); loadTracking(); }
  evts.forEach(function (e) { window.addEventListener(e, trigger, { passive: true }); });
  setTimeout(loadTracking, 3000);
})();

/* Menu panel: opens from the top bar, closes on a link, Escape or the veil */
(function () {
  document.querySelectorAll('[data-menu-toggle]').forEach(function (b) {
    b.addEventListener('click', function () { document.body.classList.toggle('menu-open'); });
  });
  document.querySelectorAll('.menu-overlay__links a').forEach(function (a) {
    a.addEventListener('click', function () { document.body.classList.remove('menu-open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') document.body.classList.remove('menu-open');
  });
  // the dim veil behind the panel is body::after, so a click on it lands on body itself
  document.addEventListener('click', function (e) {
    if (e.target === document.body) document.body.classList.remove('menu-open');
  });
})();

/* Top bar: solid once the page scrolls */
(function () {
  var bar = document.querySelector('[data-topbar]');
  if (!bar) return;
  function update() { bar.classList.toggle('is-solid', window.scrollY > 8); }
  window.addEventListener('scroll', update, { passive: true });
  update();
})();

/* What we do: the two tile rows drift in opposite directions as the section scrolls past */
(function () {
  var wall = document.querySelector('[data-swall]');
  if (!wall || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var rows = wall.querySelectorAll('.swall__row');
  var wide = window.matchMedia('(min-width: 761px)');
  var ticking = false;
  function update() {
    ticking = false;
    if (!wide.matches) { rows.forEach(function (r) { r.style.transform = ''; }); return; }
    var box = wall.getBoundingClientRect(), vh = window.innerHeight;
    if (box.bottom < 0 || box.top > vh) return;
    var x = ((vh - box.top) / (vh + box.height) - 0.5) * 64; // +-32px across the pass
    rows[0].style.transform = 'translateX(' + x.toFixed(1) + 'px)';
    rows[1].style.transform = 'translateX(' + (-x).toFixed(1) + 'px)';
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
