#!/usr/bin/env python3
"""Write the header, menu and footer into every page's HTML.

They used to be added by JavaScript, which search engines that don't run scripts
(and link previews) never saw. Now they are plain HTML in each page, between
<!-- site-header:start/end --> and <!-- site-footer:start/end --> markers.

Edit the links or contact details here, then run:
    python3 manterfield/_build/chrome.py
(The page generators run it automatically.)
"""
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

ARROW = ('<svg viewBox="0 0 34 14" fill="none" aria-hidden="true">'
         '<path d="M0 7h32M26 1l6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>')

NAV = [("index.html", "Home", "home"), ("about.html", "About", "about"), ("services.html", "Services", "services"),
       ("projects.html", "Projects", "projects"), ("testimonials.html", "Testimonials", "testimonials"),
       ("contact.html", "Contact", "contact")]
SERVICES = [("building", "Building"), ("extensions", "Extensions"), ("roofing", "Roofing"),
            ("renovations", "Renovations"), ("loft-conversions", "Loft Conversions"), ("commercial", "Commercial"),
            ("landscaping", "Landscaping")]
SOCIAL = [("https://www.instagram.com/manterfield.building", "Instagram"),
          ("https://www.facebook.com/profile.php?id=61560415476579", "Facebook"),
          ("https://www.google.com/maps?cid=11234015266589093734", "Google Reviews"),
          ("https://www.fmb.org.uk/builder/manterfield-building-roofing-limited.html", "Federation of Master Builders")]

BLOCK = re.compile(r"[ \t]*<!-- site-(header|footer):start -->.*?<!-- site-\1:end -->\n?", re.S)
SKIP = re.compile(r'[ \t]*<a class="skip" href="#main">Skip to content</a>\n?')


def pages():
    out = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    for sub in ("projects", "services"):
        d = os.path.join(SITE, sub)
        if os.path.isdir(d):
            out += [f"{sub}/{f}" for f in sorted(os.listdir(d)) if f.endswith(".html")]
    return out


def header(root, page):
    logo = (f'<img src="{root}images/logo-round.webp" alt="Manterfield Building &amp; Roofing" width="640" height="640">')
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{root}{h}"{cur if k == page else ""}><span>0{i + 1}</span>{t}</a>'
                  for i, (h, t, k) in enumerate(NAV))
    return f'''  <!-- site-header:start -->
  <header class="site-header">
    <a class="skip" href="#main">Skip to content</a>
    <a class="brand" href="{root}index.html" aria-label="Manterfield Building &amp; Roofing — home">{logo}</a>
    <div class="header-actions">
      <a class="header-call" href="tel:01226781344">01226 781344</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
    </div>
  </header>
  <div class="menu" id="menu" aria-hidden="true">
    <div class="menu-top">
      <a class="brand" href="{root}index.html" aria-label="Home">{logo}</a>
      <button class="menu-btn" type="button" data-close>Close</button>
    </div>
    <nav aria-label="Main">{nav}</nav>
    <div class="menu-foot">
      <span>Call for a FREE home consultation &amp; quotation</span>
      <a href="tel:01226781344">01226 781344</a>
      <a href="mailto:manterfield1@btinternet.com">manterfield1@btinternet.com</a>
    </div>
  </div>
  <!-- site-header:end -->
'''


def footer(root):
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in SOCIAL)
    nav = "".join(f'<li><a href="{root}{h}">{t}</a></li>' for h, t, _ in NAV)
    svc = "".join(f'<li><a href="{root}services/{s}.html">{t}</a></li>' for s, t in SERVICES)
    year = datetime.date.today().year
    return f'''  <!-- site-footer:start -->
  <footer class="site-footer">
    <div class="wrap">
      <div class="wordmark" aria-hidden="true">Manterfield</div>
      <div class="foot-cta">
        <h2>Tell us about your project</h2>
        <a class="link-row" href="{root}contact.html">Call for a FREE home consultation &amp; quotation{ARROW}</a>
      </div>
      <div class="foot-grid">
        <div><a href="tel:01226781344">01226 781344</a><br><a href="tel:07841204807">07841 204807</a><br><a href="mailto:manterfield1@btinternet.com">manterfield1@btinternet.com</a></div>
        <div class="r"><ul>{social}</ul></div>
        <div><ul>{nav}</ul></div>
        <div><ul>{svc}</ul></div>
        <div class="r end"><address>Manterfield Building &amp; Roofing Ltd<br>259a Pontefract Road<br>Cudworth<br>Barnsley, South Yorkshire<br>S72 8AQ</address></div>
      </div>
      <div class="foot-base">
        <span>&copy; <span data-year>{year}</span> Manterfield Building &amp; Roofing Ltd.</span>
        <span>Company Reg. 08779779 &middot; VAT 184 2696 75</span>
        <span><a href="{root}terms-conditions.html">Terms &amp; Conditions</a> &middot; <a href="{root}privacy-policy.html">Privacy Policy</a></span>
        <span class="foot-fmb"><img src="{root}images/fmb-logo.png" alt="Federation of Master Builders member" width="800" height="312" loading="lazy">Chas &middot; Velux &middot; EBC</span>
      </div>
    </div>
  </footer>
  <!-- site-footer:end -->
'''


def apply():
    for rel in pages():
        path = os.path.join(SITE, rel)
        s = open(path, encoding="utf-8").read()
        body = re.search(r"<body[^>]*>", s)
        if not body:
            continue
        page = (re.search(r'data-page="([^"]*)"', body.group(0)) or [None, ""])[1]
        root = (re.search(r'data-root="([^"]*)"', body.group(0)) or [None, ""])[1]
        s = BLOCK.sub("", s)
        s = SKIP.sub("", s)
        body = re.search(r"<body[^>]*>\n?", s)
        s = s[:body.end()] + header(root, page) + s[body.end():]
        script = re.search(r'[ \t]*<script src="[^"]*js/main\.js', s)
        s = s[:script.start()] + footer(root) + s[script.start():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
    print(f"chrome: header, menu and footer written into {len(pages())} pages")


if __name__ == "__main__":
    apply()
