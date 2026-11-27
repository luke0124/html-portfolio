(function () {
  'use strict';
  window.__mfReady = true;  // tells the page's safety check that the script is running

  var ARROW = '<svg viewBox="0 0 34 14" fill="none" aria-hidden="true"><path d="M0 7h32M26 1l6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>';
  /* ---------- Header + menu (written into each page's HTML by _build/chrome.py) ---------- */
  var header = document.querySelector('.site-header');
  var menu = document.getElementById('menu');
  if (header && menu) {
    var openBtn = header.querySelector('.menu-btn');
    var closeBtn = menu.querySelector('[data-close]');
    var setMenu = function (open) {
      menu.classList.toggle('is-open', open);
      menu.setAttribute('aria-hidden', String(!open));
      openBtn.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('menu-open', open);
      if (open) closeBtn.focus(); else openBtn.focus();
    };
    openBtn.addEventListener('click', function () { setMenu(true); });
    closeBtn.addEventListener('click', function () { setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false);
    });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---------- Arrow placeholders ---------- */
  document.querySelectorAll('[data-arrow]').forEach(function (el) { el.insertAdjacentHTML('beforeend', ARROW); });

  /* ---------- Hero video ---------- */
  var heroVideo = document.querySelector('video.hero-media');
  if (heroVideo) {
    var toggle = document.querySelector('.hero-toggle');
    // Phones and narrow screens get the portrait (9:16) video and its portrait still photo
    var isPhone = window.matchMedia('(max-width: 899px)').matches;
    if (isPhone) heroVideo.poster = heroVideo.getAttribute('data-poster-phone');
    var conn = navigator.connection || {};
    var dataSaver = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');
    function setLabel() {
      var paused = heroVideo.paused;
      toggle.textContent = paused ? 'Play' : 'Pause';
      toggle.setAttribute('aria-label', (paused ? 'Play' : 'Pause') + ' background video');
    }
    function tryPlay() {
      var pr = heroVideo.play();
      if (pr && pr.catch) pr.catch(function () { setLabel(); });
    }
    if (dataSaver) {
      // Visitor asked to save data: keep the still photo, download no video.
      toggle.hidden = true;
    } else {
      // Choose ONE file up front (1080p for large screens, 720p otherwise) so only one is downloaded.
      var big = window.innerWidth >= 900 && window.innerWidth * (window.devicePixelRatio || 1) > 1280;
      heroVideo.src = heroVideo.getAttribute(isPhone ? 'data-src-phone' : (big ? 'data-src-large' : 'data-src-small'));
      heroVideo.addEventListener('play', setLabel);
      heroVideo.addEventListener('pause', setLabel);
      toggle.addEventListener('click', function () { if (heroVideo.paused) tryPlay(); else heroVideo.pause(); });
      tryPlay();
    }
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

  /* ---------- Project filter + "Show more" (24 at a time) ---------- */
  var filter = document.querySelector('[data-filter]');
  var grid = document.querySelector('.grid');
  if (filter && grid) {
    var PAGE = 24, limit = PAGE, current = 'all';
    var items = Array.prototype.slice.call(grid.querySelectorAll('.project'));
    var moreWrap = document.createElement('div');
    moreWrap.className = 'more-wrap';
    moreWrap.innerHTML = '<button type="button" class="btn more-btn"></button>';
    grid.parentNode.insertBefore(moreWrap, grid.nextSibling);
    var moreBtn = moreWrap.querySelector('button');
    var render = function () {
      var total = 0;
      items.forEach(function (it) {
        var match = current === 'all' || it.getAttribute('data-cat') === current;
        it.classList.toggle('is-hidden', !match);
        if (match) total++;
        it.classList.toggle('is-more', match && total > limit);
      });
      var left = total - Math.min(total, limit);
      moreWrap.hidden = left <= 0;
      moreBtn.textContent = 'Show more projects (' + left + ' more)';
    };
    moreBtn.addEventListener('click', function () {
      var firstNew = items.filter(function (it) { return it.classList.contains('is-more'); })[0];
      limit += PAGE;
      render();
      if (firstNew) firstNew.focus({ preventScroll: true });
    });
    filter.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      filter.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-active', x === b); x.setAttribute('aria-pressed', String(x === b)); });
      current = b.getAttribute('data-f');
      limit = PAGE;
      render();
    });
    render();
    var fromHash = location.hash.replace('#', '');
    if (fromHash) {
      var hb = filter.querySelector('button[data-f="' + fromHash + '"]');
      if (hb) hb.click();
    }
  }

  /* ---------- Enquiry form: sends straight to the office; falls back to the visitor's email app ---------- */
  var form = document.querySelector('form.enquiry');
  if (form) {
    var shownAt = Date.now();
    var okBox = form.querySelector('.form-ok');
    var errBox = form.querySelector('.form-err');
    var sendBtn = form.querySelector('button[type="submit"]');
    var btnLabel = sendBtn.firstChild ? sendBtn.firstChild.textContent : 'Send enquiry';

    function openEmailApp(d) {
      var subject = d.get('subject') || ('Project enquiry \u2014 ' + (d.get('service') || 'General'));
      var body = 'Name: ' + d.get('name') + '\nEmail: ' + d.get('email') + '\nPhone: ' + (d.get('phone') || '') +
        '\nService: ' + (d.get('service') || '') + '\n\n' + d.get('message');
      window.location.href = 'mailto:manterfield1@btinternet.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      okBox.classList.remove('show');
      errBox.classList.remove('show');
      if (!form.reportValidity()) return;
      var d = new FormData(form);
      d.append('elapsed', String(Date.now() - shownAt));
      sendBtn.disabled = true;
      sendBtn.firstChild.textContent = 'Sending\u2026';
      fetch(form.getAttribute('action'), { method: 'POST', body: d, headers: { 'Accept': 'application/json' } })
        .then(function (r) {
          return r.json().then(function (j) { return { status: r.status, body: j }; });
        })
        .then(function (res) {
          if (res.body && res.body.ok) {
            form.reset();
            okBox.classList.add('show');
            okBox.focus && okBox.setAttribute('tabindex', '-1');
            okBox.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
          } else {
            errBox.textContent = (res.body && res.body.error) || 'Sorry, your message could not be sent. Please call us on 01226 781344.';
            errBox.classList.add('show');
          }
        })
        .catch(function () {
          // The sending script isn't available here (for example a preview site): use the visitor's email app instead.
          openEmailApp(d);
          okBox.textContent = 'Your email app should now be open with your message ready to send.';
          okBox.classList.add('show');
        })
        .then(function () {
          sendBtn.disabled = false;
          sendBtn.firstChild.textContent = btnLabel;
        });
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
