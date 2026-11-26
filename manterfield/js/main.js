(function () {
  'use strict';

  var ARROW = '<svg viewBox="0 0 34 14" fill="none" aria-hidden="true"><path d="M0 7h32M26 1l6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>';
  var page = document.body.getAttribute('data-page') || '';
  var ROOT = document.body.getAttribute('data-root') || '';

  var links = [
    ['index.html', 'Home', 'home'],
    ['about.html', 'About', 'about'],
    ['services.html', 'Services', 'services'],
    ['projects.html', 'Projects', 'projects'],
    ['testimonials.html', 'Testimonials', 'testimonials'],
    ['contact.html', 'Contact', 'contact']
  ];

  function navLinks() {
    return links.map(function (l, i) {
      var cur = l[2] === page ? ' aria-current="page"' : '';
      return '<a href="' + ROOT + l[0] + '"' + cur + '><span>0' + (i + 1) + '</span>' + l[1] + '</a>';
    }).join('');
  }

  /* ---------- Header + menu ---------- */
  var header = document.createElement('header');
  header.className = 'site-header';
  header.innerHTML =
    '<a class="brand" href="' + ROOT + 'index.html" aria-label="Manterfield Building &amp; Roofing — home">' +
      '<img src="' + ROOT + 'images/logo-round.webp" alt="Manterfield Building &amp; Roofing" width="640" height="640"></a>' +
    '<div class="header-actions">' +
      '<a class="header-call" href="tel:01226781344">01226 781344</a>' +
      '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>' +
    '</div>';

  var menu = document.createElement('div');
  menu.className = 'menu';
  menu.id = 'menu';
  menu.setAttribute('aria-hidden', 'true');
  menu.innerHTML =
    '<div class="menu-top">' +
      '<a class="brand" href="' + ROOT + 'index.html" aria-label="Home"><img src="' + ROOT + 'images/logo-round.webp" alt="Manterfield Building &amp; Roofing" width="640" height="640"></a>' +
      '<button class="menu-btn" type="button" data-close>Close</button>' +
    '</div>' +
    '<nav aria-label="Main">' + navLinks() + '</nav>' +
    '<div class="menu-foot">' +
      '<span>Call for a FREE home consultation &amp; quotation</span>' +
      '<a href="tel:01226781344">01226 781344</a>' +
      '<a href="mailto:manterfield1@btinternet.com">manterfield1@btinternet.com</a>' +
    '</div>';

  document.body.insertBefore(menu, document.body.firstChild);
  document.body.insertBefore(header, document.body.firstChild);

  var openBtn = header.querySelector('.menu-btn');
  var closeBtn = menu.querySelector('[data-close]');
  function setMenu(open) {
    menu.classList.toggle('is-open', open);
    menu.setAttribute('aria-hidden', String(!open));
    openBtn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('menu-open', open);
    if (open) closeBtn.focus(); else openBtn.focus();
  }
  openBtn.addEventListener('click', function () { setMenu(true); });
  closeBtn.addEventListener('click', function () { setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false);
  });

  /* ---------- Footer ---------- */
  var footer = document.createElement('footer');
  footer.className = 'site-footer';
  footer.innerHTML =
    '<div class="wrap">' +
      '<div class="wordmark" aria-hidden="true">Manterfield</div>' +
      '<div class="foot-cta">' +
        '<h2>Tell us about your project</h2>' +
        '<a class="link-row" href="' + ROOT + 'contact.html">Call for a FREE home consultation &amp; quotation' + ARROW + '</a>' +
      '</div>' +
      '<div class="foot-grid">' +
        '<div><a href="tel:01226781344">01226 781344</a><br><a href="tel:07841204807">07841 204807</a><br>' +
          '<a href="mailto:manterfield1@btinternet.com">manterfield1@btinternet.com</a></div>' +
        '<div class="r"><ul>' +
          '<li><a href="https://www.instagram.com/manterfield.building" target="_blank" rel="noopener">Instagram</a></li>' +
          '<li><a href="https://www.facebook.com/profile.php?id=61560415476579" target="_blank" rel="noopener">Facebook</a></li>' +
          '<li><a href="https://www.google.com/maps?cid=11234015266589093734" target="_blank" rel="noopener">Google Reviews</a></li>' +
          '<li><a href="https://www.fmb.org.uk/builder/manterfield-building-roofing-limited.html" target="_blank" rel="noopener">Federation of Master Builders</a></li>' +
        '</ul></div>' +
        '<div><ul>' + links.map(function (l) { return '<li><a href="' + ROOT + l[0] + '">' + l[1] + '</a></li>'; }).join('') + '</ul></div>' +
        '<div class="r end">259a Pontefract Road<br>Cudworth<br>Barnsley, South Yorkshire<br>S72 8AQ</div>' +
      '</div>' +
      '<div class="foot-base">' +
        '<span>&copy; ' + new Date().getFullYear() + ' Manterfield Building &amp; Roofing Ltd.</span>' +
        '<span>Company Reg. 08779779 &middot; VAT 184 2696 75</span>' +
        '<span><a href="' + ROOT + 'terms-conditions.html">Terms &amp; Conditions</a> &middot; <a href="' + ROOT + 'privacy-policy.html">Privacy Policy</a></span>' +
        '<span class="foot-fmb"><img src="' + ROOT + 'images/fmb-logo.png" alt="Federation of Master Builders member" width="800" height="312">Chas &middot; Velux &middot; EBC</span>' +
      '</div>' +
    '</div>';
  document.body.appendChild(footer);

  /* ---------- Arrow placeholders ---------- */
  document.querySelectorAll('[data-arrow]').forEach(function (el) { el.insertAdjacentHTML('beforeend', ARROW); });

  /* ---------- Hero video ---------- */
  var heroVideo = document.querySelector('video.hero-media');
  if (heroVideo) {
    // Larger screens get the 1080p file; phones keep the 720p <source> from the HTML.
    var big = window.innerWidth >= 900 && window.innerWidth * (window.devicePixelRatio || 1) > 1280;
    if (big) {
      var t = heroVideo.currentTime;
      heroVideo.querySelector('source').src = heroVideo.getAttribute('data-src-large');
      heroVideo.load();
      if (t) heroVideo.currentTime = t;
    }
    var toggle = document.querySelector('.hero-toggle');
    function setLabel() {
      var paused = heroVideo.paused;
      toggle.textContent = paused ? 'Play' : 'Pause';
      toggle.setAttribute('aria-label', (paused ? 'Play' : 'Pause') + ' background video');
    }
    function tryPlay() {
      var pr = heroVideo.play();
      if (pr && pr.catch) pr.catch(function () { setLabel(); });
    }
    heroVideo.addEventListener('play', setLabel);
    heroVideo.addEventListener('pause', setLabel);
    toggle.addEventListener('click', function () { if (heroVideo.paused) tryPlay(); else heroVideo.pause(); });
    tryPlay();
  }

  /* ---------- Header state on scroll ---------- */
  var hasHero = !!document.querySelector('.hero');
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    var threshold = hasHero ? window.innerHeight * 0.85 : 10;
    header.classList.toggle('is-solid', y > threshold || !hasHero);
    header.classList.toggle('is-hidden', y > lastY && y > 400 && !document.body.classList.contains('menu-open'));
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Reveal ---------- */
  var revealEls = document.querySelectorAll('.reveal, .reveal-img');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- Testimonial slider ---------- */
  document.querySelectorAll('[data-slider]').forEach(function (root) {
    var track = root.querySelector('.quotes-track');
    var slides = track.children.length;
    var idx = 0;
    var cur = root.querySelector('[data-cur]');
    var total = root.querySelector('[data-total]');
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    total.textContent = pad(slides);
    function go(i) {
      idx = (i + slides) % slides;
      track.style.transform = 'translateX(' + (-100 * idx) + '%)';
      cur.textContent = pad(idx + 1);
      Array.prototype.forEach.call(track.children, function (s, j) { s.setAttribute('aria-hidden', String(j !== idx)); });
    }
    root.querySelector('[data-prev]').addEventListener('click', function () { go(idx - 1); });
    root.querySelector('[data-next]').addEventListener('click', function () { go(idx + 1); });
    var sx = null;
    track.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 40) go(idx + (dx < 0 ? 1 : -1));
      sx = null;
    });
    go(0);
  });

  /* ---------- Project filter ---------- */
  var filter = document.querySelector('[data-filter]');
  if (filter) {
    var items = document.querySelectorAll('.grid .project');
    filter.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      filter.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', String(x === b)); });
      var f = b.getAttribute('data-f');
      items.forEach(function (it) {
        it.classList.toggle('is-hidden', f !== 'all' && it.getAttribute('data-cat') !== f);
      });
    });
  }

  /* ---------- Enquiry form (opens the visitor's email app) ---------- */
  var form = document.querySelector('form.enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      var subject = d.get('subject') || ('Project enquiry — ' + (d.get('service') || 'General'));
      var body = 'Name: ' + d.get('name') + '\nEmail: ' + d.get('email') + '\nPhone: ' + (d.get('phone') || '') +
        '\nService: ' + (d.get('service') || '') + '\n\n' + d.get('message');
      window.location.href = 'mailto:manterfield1@btinternet.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
      form.querySelector('.form-ok').classList.add('show');
    });
  }

  /* ---------- Gallery lightbox ---------- */
  var gallery = document.querySelectorAll('[data-lightbox]');
  if (gallery.length) {
    var items = Array.prototype.map.call(gallery, function (a) { return { src: a.getAttribute('href'), alt: (a.querySelector('img') || {}).alt || '' }; });
    var box = document.createElement('div');
    box.className = 'lightbox';
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Photo viewer');
    box.innerHTML =
      '<div class="lb-top"><span class="lb-count"></span><button type="button" class="lb-close">Close</button></div>' +
      '<figure class="lb-stage"><img alt=""></figure>' +
      '<div class="lb-nav"><button type="button" class="lb-prev">Prev</button><button type="button" class="lb-next">Next</button></div>';
    document.body.appendChild(box);
    var lbImg = box.querySelector('img'), lbCount = box.querySelector('.lb-count');
    var cur = 0, lastFocus = null;
    function pad2(n) { return (n < 10 ? '0' : '') + n; }
    function show(i) {
      cur = (i + items.length) % items.length;
      lbImg.src = items[cur].src;
      lbImg.alt = items[cur].alt;
      lbCount.innerHTML = pad2(cur + 1) + ' <span>/ ' + pad2(items.length) + '</span>';
      [cur - 1, cur + 1].forEach(function (j) { var im = new Image(); im.src = items[(j + items.length) % items.length].src; });
    }
    function open(i) { lastFocus = document.activeElement; show(i); box.classList.add('is-open'); document.body.classList.add('menu-open'); box.querySelector('.lb-close').focus(); }
    function close() { box.classList.remove('is-open'); document.body.classList.remove('menu-open'); if (lastFocus) lastFocus.focus(); }
    Array.prototype.forEach.call(gallery, function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
    box.querySelector('.lb-close').addEventListener('click', close);
    box.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
    box.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
    box.addEventListener('click', function (e) { if (e.target === box || e.target.classList.contains('lb-stage')) close(); });
    document.addEventListener('keydown', function (e) {
      if (!box.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowLeft') show(cur - 1);
      else if (e.key === 'ArrowRight') show(cur + 1);
    });
    var lx = null;
    box.addEventListener('touchstart', function (e) { lx = e.touches[0].clientX; }, { passive: true });
    box.addEventListener('touchend', function (e) {
      if (lx === null) return;
      var dx = e.changedTouches[0].clientX - lx;
      if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
      lx = null;
    });
  }
})();
