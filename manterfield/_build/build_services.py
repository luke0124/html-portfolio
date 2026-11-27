"""Service pages, the Services overview and the 404 page.

Called by build_projects.py (it passes itself in as `bp` for the shared helpers).
Service wording lives in services-source.json: edit it there, then rebuild:

    python3 manterfield/_build/build_projects.py
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

AREA_LINE = "Barnsley, Wakefield, Sheffield, Leeds and across South Yorkshire"

# What each service page targets on Google. `cat` is the matching projects filter.
SEO = {
    "building": dict(cat="building", title="Builders in Barnsley", h1="Builders in Barnsley &amp; South Yorkshire",
                     phrase="Building work, brickwork and structural alterations"),
    "extensions": dict(cat="extensions", title="House Extensions in Barnsley", h1="House Extensions in Barnsley",
                       phrase="Single and double storey house extensions"),
    "roofing": dict(cat="roofing", title="Roofing & Re-roofs in Barnsley", h1="Roofers in Barnsley &amp; South Yorkshire",
                    phrase="Re-roofs, roof repairs, flat roofs and storm damage"),
    "renovations": dict(cat="renovations", title="Home Renovations in Barnsley", h1="Home Renovations in Barnsley",
                        phrase="Home renovations, knock-throughs and garage conversions"),
    "loft-conversions": dict(cat="lofts", title="Loft Conversions in Barnsley", h1="Loft Conversions in Barnsley",
                             phrase="Dormer, hip-to-gable and Velux loft conversions"),
    "commercial": dict(cat="commercial", title="Commercial Builders in Barnsley", h1="Commercial Builders in Barnsley",
                       phrase="Commercial building and roofing work"),
    "landscaping": dict(cat="landscaping", title="Patios, Driveways &amp; Landscaping in Barnsley",
                        h1="Patios, Driveways &amp; Landscaping in Barnsley",
                        phrase="Patios, driveways, walls and landscaping"),
}


def _relink(fragment, root):
    """Make relative links in a copied fragment work from a page in a subfolder."""
    return re.sub(r'href="(?!https?:|tel:|mailto:|#|/|\.\./)([^"]+)"', lambda m: f'href="{root}{m.group(1)}"', fragment)


def _card(bp, p, root, n):
    img = (f'{root}images/thumbs/{os.path.basename(p["card_img"])}' if p.get("card_img")
           else f'{root}images/projects/{p["slug"]}/thumbs/{p["imgs"][-1]}')
    pos = f' style="object-position:{p["card_pos"]}"' if p.get("card_pos") else ""
    where = p["area"] or bp.LABEL[p["cat"]]
    return f'''          <a class="project reveal" href="{root}projects/{p["slug"]}.html">
            <div class="ph"><img src="{img}" alt="{bp.e(p["title"])}" loading="lazy"{pos}></div>
            <div class="project-meta"><span>{n:02d}</span><span>{bp.e(p["title"])}</span><span class="cat">{bp.e(where)}</span></div>
          </a>'''


def build(bp, projects):
    site = bp.SITE
    services = json.load(open(os.path.join(HERE, "services-source.json"), encoding="utf-8"))
    os.makedirs(os.path.join(site, "services"), exist_ok=True)
    arrow = bp.ARROW

    for i, s in enumerate(services):
        seo = SEO[s["id"]]
        root = "../"
        related = [p for p in projects if p["cat"] == seo["cat"]]
        towns = []
        for p in related:
            if p["area"] and p["area"] not in towns:
                towns.append(p["area"])
        town_line = ""
        if towns:
            shown = sorted(towns[:8])
            town_line = (f'<p>Recent {s["name"].lower()} work by our team includes projects in '
                         f'{", ".join(shown[:-1])}{" and " if len(shown) > 1 else ""}{shown[-1]}.</p>')
        cards = "\n".join(_card(bp, p, root, n + 1) for n, p in enumerate(related[:6]))
        others = "".join(f'<a href="{o["id"]}.html">{html.escape(o["name"])}</a>' for o in services if o["id"] != s["id"])
        img_style = f' style="{s["img_style"]}"' if s["img_style"] else ""
        desc = bp.trim(f"{seo['phrase']} in Barnsley, Wakefield and South Yorkshire by Manterfield Building &amp; Roofing. "
                       f"Family firm, FMB members. Free quotes on 01226 781344.".replace("&amp;", "&"))
        lead_text = re.sub(r'^<p class="lead">|</p>$', "", s["lead_html"].strip())
        body = f'''    <section class="page-hero">
      <div class="wrap">
        <span class="crumb reveal"><a href="../services.html">Services</a> / {html.escape(s["name"])}</span>
        <h1 class="reveal">{seo["h1"]}</h1>
        <p class="reveal">{_relink(lead_text, root)}</p>
        <div class="svc-actions reveal"><a class="btn" href="../contact.html">Get a free quote{arrow}</a><a class="btn lime" href="tel:01226781344">01226 781344</a></div>
      </div>
    </section>
    <div class="wrap"><img class="proj-cover reveal-img" src="../{s["img"]}" alt="{html.escape(s["alt"])}" fetchpriority="high"{img_style}></div>
    <section class="wrap proj-about">
      <h2 class="reveal">{html.escape(s["name"])} by Manterfield</h2>
      <div class="txt svc-body reveal">
{_relink(s["body_html"], root)}
          <p>We work across {AREA_LINE}.</p>
          {town_line}
      </div>
    </section>
'''
        if related:
            body += f'''    <section class="pad" style="padding-top:0">
      <div class="wrap">
        <div class="sec-head reveal"><h2>Recent {html.escape(s["name"].lower())} projects</h2><a href="../projects.html#{seo["cat"]}">See all {len(related)}</a></div>
        <div class="grid">
{cards}
        </div>
      </div>
    </section>
'''
        body += f'''    <section class="pad" style="padding-top:0">
      <div class="wrap">
        <div class="sec-head reveal"><h2>Other services</h2></div>
        <nav class="chips reveal" aria-label="Other services">{others}</nav>
      </div>
    </section>
    <section class="dark pad cta">
      <div class="wrap">
        <h2 class="reveal">Call for a FREE home consultation &amp; quotation.</h2>
        <div class="actions reveal">
          <a class="btn lime" href="tel:01226781344">01226 781344</a>
          <a class="btn" href="../contact.html" style="background:var(--dark-2)">Send an enquiry{arrow}</a>
        </div>
      </div>
    </section>
'''
        with open(os.path.join(site, "services", s["id"] + ".html"), "w", encoding="utf-8") as f:
            f.write(bp.head(html.unescape(seo["title"]), desc, root, "services") + body + bp.tail(root))

    # ---- Services overview: short summary of each service linking to its own page
    arts = []
    for s in services:
        img_style = f' style="{s["img_style"]}"' if s["img_style"] else ""
        arts.append(f'''      <article class="svc" id="{s["id"]}">
        <div class="svc-head reveal"><span class="num">{s["num"]}</span><h2><a href="services/{s["id"]}.html">{html.escape(s["name"])}</a></h2><img src="{s["img"]}" alt="{html.escape(s["alt"])}" loading="lazy"{img_style}></div>
        <div class="svc-body reveal">
          {s["lead_html"]}
          <a class="link-row" href="services/{s["id"]}.html">More about {html.escape(s["name"].lower())} in Barnsley{arrow}</a>
        </div>
      </article>''')
    path = os.path.join(site, "services.html")
    page = open(path, encoding="utf-8").read()
    page, n = re.subn(r"<!-- services:start -->.*?<!-- services:end -->",
                      lambda m: "<!-- services:start -->\n    <div class=\"wrap\">\n" + "\n\n".join(arts) + "\n    </div>\n    <!-- services:end -->",
                      page, flags=re.S)
    assert n == 1, "services markers missing in services.html"
    chips = "".join(f'<a href="services/{s["id"]}.html">{html.escape(s["name"])}</a>' for s in services)
    page = re.sub(r'(<nav class="chips reveal" aria-label="Services">\s*).*?(\s*</nav>)', lambda m: m.group(1) + chips + m.group(2), page, count=1, flags=re.S)
    open(path, "w", encoding="utf-8").write(page)

    # ---- 404 page (absolute paths: it can be shown at any address)
    links = "".join(f'<a href="/services/{s["id"]}.html">{html.escape(s["name"])}</a>' for s in services)
    body404 = f'''    <section class="page-hero">
      <div class="wrap">
        <span class="crumb reveal">Page not found</span>
        <h1 class="reveal">Sorry, we can&rsquo;t find that page.</h1>
        <p class="reveal">It may have moved when we updated our website. Try one of these, or call us on <a class="inline-link" href="tel:01226781344">01226 781344</a>.</p>
        <div class="svc-actions reveal"><a class="btn" href="/index.html">Home page{arrow}</a><a class="btn lime" href="/projects.html">Our projects</a></div>
        <nav class="chips reveal" aria-label="Services" style="margin-top:32px">{links}<a href="/contact.html">Contact</a></nav>
      </div>
    </section>
'''
    head404 = bp.head("Page not found", "The page you were looking for could not be found.", "/", "notfound")
    head404 = head404.replace('<meta name="theme-color"', '<meta name="robots" content="noindex">\n  <meta name="theme-color"', 1)
    with open(os.path.join(site, "404.html"), "w", encoding="utf-8") as f:
        f.write(head404 + body404 + bp.tail("/"))
    print("services: 7 service pages, overview and 404 page written")
