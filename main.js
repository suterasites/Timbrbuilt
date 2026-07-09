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
