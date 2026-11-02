/* Timbr Built - shared site scripts */
(function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav__toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
      var open = document.body.classList.contains('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('nav-open'); });
    });
  }

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

/* Cinematic navbar: full-screen menu overlay */
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
})();

/* Home top bar: solid once the hero tab strip scrolls up under it */
(function () {
  var bar = document.querySelector('[data-topbar]');
  var tabs = document.querySelector('[data-hero-tabs]');
  if (!bar || !tabs || !('IntersectionObserver' in window)) return;
  new IntersectionObserver(function (entries) {
    bar.classList.toggle('is-solid', entries[0].intersectionRatio < 1);
  }, { rootMargin: '-' + (bar.offsetHeight - 4) + 'px 0px 0px 0px', threshold: 1 }).observe(tabs);
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

