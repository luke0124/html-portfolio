#!/usr/bin/env python3
"""Generate projects.html and one page per project in projects/.

Source data: projects-source.json (scraped from the original Manterfield site:
title, text and gallery image URLs for each project, in the original order).
Photos are expected at images/projects/<slug>/<NNN>.jpg (001 = first photo).

Run from anywhere:  python3 manterfield/_build/build_projects.py
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

SKIP = {"manterfield-builders-supporting-england-world-cup-2018"}  # news post, not a project
COMMERCIAL = {"linac-services-ltd", "k-m-travel", "bransley-bowl-guttering"}
LANDSCAPE_WORDS = ("patio", "garden", "steps", "decking", "drive", "cobbled")

FILTERS = [
    ("extensions", "Extensions", "Extension"),
    ("roofing", "Roofing", "Roofing"),
    ("building", "Building", "Building"),
    ("renovations", "Renovations", "Renovation"),
    ("lofts", "Loft Conversions", "Loft Conversion"),
    ("landscaping", "Landscaping", "Landscaping"),
    ("commercial", "Commercial", "Commercial"),
]
LABEL = {k: single for k, _, single in FILTERS}

ARROW = ('<svg viewBox="0 0 34 14" fill="none" aria-hidden="true">'
         '<path d="M0 7h32M26 1l6 6-6 6" stroke="currentColor" stroke-width="1.5"/></svg>')


def e(s):
    return html.escape(s, quote=True)


def category(p):
    slug, cats, title = p["slug"], p["cats"], p["title"].lower()
    if slug in COMMERCIAL:
        return "commercial"
    if "loft-conversions" in cats:
        return "lofts"
    if any(w in title for w in LANDSCAPE_WORDS) and "extensions" not in cats:
        return "landscaping"
    if "extensions" in cats:
        return "extensions"
    if "roofing" in cats or "roof" in title:
        return "roofing"
    if "renovations" in cats:
        return "renovations"
    if "building" in cats:
        return "building"
    if "orangery" in p["text"].lower():
        return "extensions"
    return "renovations" if "burner" in title else "building"


def paragraphs(p):
    paras = [re.sub(r"\s+", " ", x.replace("\xa0", " ")).strip() for x in p["text"].split("\n\n")]
    paras = [x for x in paras if x]
    if paras and paras[0].lower().rstrip(".") == p["title"].lower().strip():
        paras = paras[1:]
    return paras


def photos(slug, n):
    folder = os.path.join(SITE, "images", "projects", slug)
    return [f"{i:03d}.jpg" for i in range(1, n + 1) if os.path.exists(os.path.join(folder, f"{i:03d}.jpg"))]


def head(title, desc, root, page):
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} | Manterfield Building &amp; Roofing</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#221c29">
  <link rel="icon" href="{root}images/favicon-round.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/styles.css?v=14">
</head>
<body data-page="{page}" data-root="{root}">
  <a class="skip" href="#main">Skip to content</a>
  <main id="main">
'''


def tail(root):
    return f'''  </main>
  <script src="{root}js/main.js?v=9"></script>
</body>
</html>
'''


def main():
    src = json.load(open(os.path.join(HERE, "projects-source.json")))
    projects = []
    for p in src:
        if p["slug"] in SKIP:
            continue
        imgs = photos(p["slug"], len(p["imgs"]))
        if not imgs:
            print("no photos yet, skipping:", p["slug"])
            continue
        projects.append(dict(slug=p["slug"], title=p["title"].strip(), cat=category(p),
                             paras=paragraphs(p), imgs=imgs))

    os.makedirs(os.path.join(SITE, "projects"), exist_ok=True)
    n = len(projects)
    for i, p in enumerate(projects):
        prev_p, next_p = projects[i - 1], projects[(i + 1) % n]
        base = f"../images/projects/{p['slug']}/"
        desc = (p["paras"][0][:150] if p["paras"] else f"{p['title']}: {LABEL[p['cat']].lower()} project by Manterfield Building & Roofing, Barnsley.")
        about = ""
        if p["paras"]:
            about = ('<section class="wrap proj-about">\n      <h2 class="reveal">About the project</h2>\n'
                     '      <div class="txt reveal">' + "".join(f"<p>{e(x)}</p>" for x in p["paras"]) + "</div>\n    </section>")
        gallery = "\n".join(
            f'        <a href="{base}{f}" data-lightbox><img src="{base}{f}" alt="{e(p["title"])}, photo {j + 1}" loading="lazy"></a>'
            for j, f in enumerate(p["imgs"]))
        body = f'''    <section class="wrap proj-hero">
      <span class="crumb reveal"><a href="../projects.html">Projects</a> / {e(LABEL[p["cat"]])}</span>
      <h1 class="reveal">{e(p["title"])}</h1>
      <div class="proj-facts reveal">
        <div><span>Type</span>{e(LABEL[p["cat"]])}</div>
        <div><span>Photos</span>{len(p["imgs"])}</div>
        <div><span>Area</span>Barnsley &amp; South Yorkshire</div>
      </div>
    </section>
    <div class="wrap"><img class="proj-cover reveal-img" src="{base}{p["imgs"][-1]}" alt="{e(p["title"])}, finished" fetchpriority="high"></div>
    {about}
    <section class="wrap" style="{'' if about else 'padding-top:clamp(40px,5vw,72px)'}">
      <div class="sec-head reveal"><h2>Gallery</h2><span class="muted">Tap a photo to enlarge</span></div>
      <div class="gallery">
{gallery}
      </div>
      <nav class="proj-pager" aria-label="More projects">
        <a class="prev" href="{prev_p["slug"]}.html"><small>&larr; Previous project</small>{e(prev_p["title"])}</a>
        <a class="next" href="{next_p["slug"]}.html"><small>Next project &rarr;</small>{e(next_p["title"])}</a>
      </nav>
    </section>
    <section class="pad">
      <div class="wrap">
        <a class="link-row" href="../contact.html">Planning something similar? Call for a FREE home consultation &amp; quotation{ARROW}</a>
      </div>
    </section>
'''
        with open(os.path.join(SITE, "projects", p["slug"] + ".html"), "w") as f:
            f.write(head(p["title"], desc, "../", "projects") + body + tail("../"))

    # Remove pages for projects that no longer exist
    keep = {p["slug"] + ".html" for p in projects}
    for f in os.listdir(os.path.join(SITE, "projects")):
        if f.endswith(".html") and f not in keep:
            os.remove(os.path.join(SITE, "projects", f))

    counts = {k: sum(1 for p in projects if p["cat"] == k) for k, _, _ in FILTERS}
    buttons = "\n".join(
        [f'          <button type="button" class="is-active" aria-pressed="true" data-f="all">All <span class="muted">{n}</span></button>'] +
        [f'          <button type="button" aria-pressed="false" data-f="{k}">{plural} <span class="muted">{counts[k]}</span></button>'
         for k, plural, _ in FILTERS if counts[k]])
    cards = "\n".join(
        f'''          <a class="project reveal" data-cat="{p["cat"]}" href="projects/{p["slug"]}.html">
            <div class="ph"><img src="images/projects/{p["slug"]}/{p["imgs"][-1]}" alt="{e(p["title"])}" loading="lazy"></div>
            <div class="project-meta"><span>{i + 1:02d}</span><span>{e(p["title"])}</span><span class="cat">{e(LABEL[p["cat"]])}</span></div>
          </a>''' for i, p in enumerate(projects))
    listing = f'''    <section class="page-hero">
      <div class="wrap">
        <span class="crumb reveal">Project Gallery</span>
        <h1 class="reveal">All Projects</h1>
        <p class="reveal">From minor roof repairs to major structural renovations, across Barnsley and surrounding areas.</p>
      </div>
    </section>
    <section class="pad" style="padding-top:0">
      <div class="wrap">
        <div class="filter reveal" data-filter role="group" aria-label="Filter projects">
{buttons}
        </div>
        <div class="grid">
{cards}
        </div>
      </div>
    </section>
    <section class="dark pad cta">
      <div class="wrap">
        <h2 class="reveal">Make us top of your contractor list.</h2>
        <div class="actions reveal">
          <a class="btn lime" href="tel:01226781344">01226 781344</a>
          <a class="btn" href="contact.html" style="background:var(--dark-2)">Free, no obligation quotation{ARROW}</a>
        </div>
      </div>
    </section>
'''
    with open(os.path.join(SITE, "projects.html"), "w") as f:
        f.write(head("Projects", "Extensions, re-roofs, renovations and loft conversions across Barnsley, Wakefield and South Yorkshire.", "", "projects")
                + listing + tail(""))
    print(f"{n} project pages written;", counts)


if __name__ == "__main__":
    main()
