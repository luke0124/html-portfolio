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
import sys
from multiprocessing import Pool

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
THUMB_SIZE = 720          # long side in px, for the projects grid and gallery tiles
TITLE_LIMIT = 60          # Google cuts page titles off at roughly this many characters

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

# Projects shown as the four featured cards on the home page (by slug, in order)
HOME_FEATURED = ["two-storey-structural-transformation", "stone-barn-renovation", "kitchen-extension", "new-roof"]
HOME_CARD_SIZE = 1000

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


# Places named in project titles/text (the area we show for each project).
TOWNS = ["High Hoyland", "Little Houghton", "Monk Bretton", "Ward Green", "Hood Green", "Low Valley", "Blacker Hill",
         "Cundy Cross", "Hoylandswaine", "Stainborough", "Grimethorpe", "Hemingfield", "Mapplewell", "Thurgoland",
         "Staincross", "Stairfoot", "Silkstone", "Birdwell", "Brampton", "Cudworth", "Darfield", "Royston", "Wombwell",
         "Shafton", "Darton", "Woolley", "Higham", "Swinton", "Rothwell", "Wakefield", "Sheffield", "Rotherham", "Wath",
         "Barnsley"]
TOWN_ALIASES = {"Worsborough": "Worsbrough", "Worsbrough": "Worsbrough"}
_STREET = re.compile(r"\b[A-Za-z\u2019']+(?: [A-Za-z\u2019']+)? (?:Road|Rd|Drive|Street|St|Lane|Close|Crescent|Avenue|Place|Estate)\b", re.I)


def find_area(p):
    """Town named in the project's own title, else its text. Street names are ignored
    ("Wakefield Road" is not Wakefield). Returns "" when no place is stated."""
    for source in (p["title"], p.get("text", "")):
        s = _STREET.sub(" ", source)
        for alias, town in TOWN_ALIASES.items():
            if re.search(r"\b" + alias + r"\b", s, re.I):
                return town
        for town in TOWNS:
            if re.search(r"\b" + re.escape(town) + r"\b", s, re.I):
                return town
    return ""


def area_id(town):
    return "area-" + re.sub(r"[^a-z]+", "-", town.lower()).strip("-")


def trim(text, limit=155):
    """Cut text to at most `limit` characters at a word boundary (meta descriptions)."""
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-\u2013") + "\u2026"


def page_title(t):
    """'<name> | Manterfield Building & Roofing', shortened so Google doesn't cut it off."""
    full = f"{t} | Manterfield Building & Roofing"
    if len(full) <= TITLE_LIMIT:
        return full
    short = f"{t} | Manterfield"
    if len(short) <= TITLE_LIMIT:
        return short
    room = TITLE_LIMIT - len(" | Manterfield") - 1
    return t[:room].rsplit(" ", 1)[0].rstrip(" ,;:-\u2013&") + "\u2026 | Manterfield"


COVER_WIDTH = 960          # width of the phone-sized project cover photo


def _thumb_job(job):
    src, dst, mode = job
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with Image.open(src) as im:
        im = im.convert("RGB")
        if mode == "cover":
            if im.width > COVER_WIDTH:
                im = im.resize((COVER_WIDTH, round(im.height * COVER_WIDTH / im.width)), Image.LANCZOS)
            im.save(dst, "JPEG", quality=70, optimize=True, progressive=True)
        else:
            im.thumbnail((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
            im.save(dst, "JPEG", quality=66, optimize=True, progressive=True)


def make_thumbs(projects):
    """Small copies of every project photo (images/projects/<slug>/thumbs/NNN.jpg).
    Only (re)built when missing or older than the full-size photo."""
    jobs = []
    for p in projects:
        folder = os.path.join(SITE, "images", "projects", p["slug"])
        for f in p["imgs"]:
            src, dst = os.path.join(folder, f), os.path.join(folder, "thumbs", f)
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
                jobs.append((src, dst, "thumb"))
        csrc = os.path.join(folder, p["imgs"][-1])
        cdst = os.path.join(folder, "thumbs", "cover-%d.jpg" % COVER_WIDTH)
        if not os.path.exists(cdst) or os.path.getmtime(cdst) < os.path.getmtime(csrc):
            jobs.append((csrc, cdst, "cover"))
        if p.get("card_img"):
            src = os.path.join(SITE, p["card_img"])
            dst = os.path.join(SITE, "images", "thumbs", os.path.basename(p["card_img"]))
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
                jobs.append((src, dst, "thumb"))
    if jobs:
        with Pool(min(8, os.cpu_count() or 2)) as pool:
            pool.map(_thumb_job, jobs, chunksize=8)
    print(f"thumbnails: {len(jobs)} made")


def update_home(projects):
    """Rebuild the featured cards on index.html (between the featured markers) from
    each project's cover photo, so they can never point at the wrong picture."""
    by = {p["slug"]: p for p in projects}
    out_dir = os.path.join(SITE, "images", "home-cards")
    os.makedirs(out_dir, exist_ok=True)
    cards = []
    for i, slug in enumerate(HOME_FEATURED, 1):
        p = by[slug]
        src = os.path.join(SITE, p["card_img"]) if p.get("card_img") else os.path.join(SITE, "images", "projects", slug, p["imgs"][-1])
        dst = os.path.join(out_dir, slug + ".jpg")
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            with Image.open(src) as im:
                im = im.convert("RGB")
                im.thumbnail((HOME_CARD_SIZE, HOME_CARD_SIZE), Image.LANCZOS)
                im.save(dst, "JPEG", quality=72, optimize=True, progressive=True)
        pos = p.get("card_pos") or p.get("cover_pos")
        style = f' style="object-position:{pos}"' if pos else ""
        cards.append(f'''          <a class="project reveal" href="projects/{slug}.html">
            <div class="ph"><img src="images/home-cards/{slug}.jpg" alt="{e(p["title"])}" loading="lazy"{style}></div>
            <div class="project-meta"><span>{i:02d}</span><span>{e(p["title"])}</span><span class="cat">{e(LABEL[p["cat"]])}</span></div>
          </a>''')
    path = os.path.join(SITE, "index.html")
    html_ = open(path, encoding="utf-8").read()
    new, n = re.subn(r"<!-- featured:start -->.*?<!-- featured:end -->", lambda m: "<!-- featured:start -->\n" + "\n".join(cards) + "\n          <!-- featured:end -->", html_, flags=re.S)
    assert n == 1, "featured markers missing in index.html"
    open(path, "w", encoding="utf-8").write(new)


def full_w(p):
    """Pixel width of a project's full-size cover photo (for the srcset)."""
    with Image.open(os.path.join(SITE, "images", "projects", p["slug"], p["imgs"][-1])) as im:
        return max(im.width, COVER_WIDTH + 1)


def photos(slug, n):
    folder = os.path.join(SITE, "images", "projects", slug)
    return [f"{i:03d}.jpg" for i in range(1, n + 1) if os.path.exists(os.path.join(folder, f"{i:03d}.jpg"))]


def head(title, desc, root, page):
    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(page_title(title))}</title>
  <meta name="description" content="{e(desc)}">
  <meta name="theme-color" content="#221c29">
  <link rel="icon" href="{root}images/favicon-round.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{root}css/styles.css?v=33">
</head>
<body data-page="{page}" data-root="{root}">
  <a class="skip" href="#main">Skip to content</a>
  <main id="main">
'''


def tail(root):
    return f'''  </main>
  <script src="{root}js/main.js?v=18"></script>
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
        projects.append(dict(slug=p["slug"], title=p["title"].strip(), cat=p.get("cat") or category(p),
                             paras=paragraphs(p), imgs=imgs, cover_pos=p.get("cover_pos"), card_img=p.get("card_img"), card_pos=p.get("card_pos"),
                             seo_title=p.get("seo_title"), area=p.get("area") or find_area(p)))
    make_thumbs(projects)

    os.makedirs(os.path.join(SITE, "projects"), exist_ok=True)
    n = len(projects)
    for i, p in enumerate(projects):
        prev_p, next_p = projects[i - 1], projects[(i + 1) % n]
        base = f"../images/projects/{p['slug']}/"
        where = f" in {p['area']}" if p["area"] and p["area"].lower() not in p["title"].lower() else ""
        desc = trim(p["paras"][0] if p["paras"] else f"{p['title']}: a {LABEL[p['cat']].lower()} project{where} by Manterfield Building & Roofing, Barnsley. See the photos and get a free quote.")
        kind = LABEL[p["cat"]].lower()
        about = ""
        if p["paras"]:
            about = ('<section class="wrap proj-about">\n      <h2 class="reveal">About the project</h2>\n'
                     '      <div class="txt reveal">' + "".join(f"<p>{e(x)}</p>" for x in p["paras"]) + "</div>\n    </section>")
        gallery = "\n".join(
            f'        <a href="{base}{f}" data-lightbox><img src="{base}thumbs/{f}" alt="{e(p["title"])} \u2013 {"finished " if j == len(p["imgs"]) - 1 else ""}{kind} project{e(where)}, photo {j + 1} of {len(p["imgs"])}" loading="lazy"></a>'
            for j, f in enumerate(p["imgs"]))
        body = f'''    <section class="wrap proj-hero">
      <span class="crumb reveal"><a href="../projects.html">Projects</a> / {e(LABEL[p["cat"]])}</span>
      <h1 class="reveal">{e(p["title"])}</h1>
      <div class="proj-facts reveal">
        <div><span>Type</span>{e(LABEL[p["cat"]])}</div>
        <div><span>Photos</span>{len(p["imgs"])}</div>
        <div><span>Area</span>{(f'<a href="../projects.html#{area_id(p["area"])}">{e(p["area"])}</a>') if p["area"] else "Barnsley &amp; South Yorkshire"}</div>
      </div>
    </section>
    <div class="wrap"><img class="proj-cover reveal-img" src="{base}{p["imgs"][-1]}" srcset="{base}thumbs/cover-{COVER_WIDTH}.jpg {COVER_WIDTH}w, {base}{p["imgs"][-1]} {full_w(p)}w" sizes="(max-width: 900px) calc(100vw - 32px), 1280px" alt="{e(p["title"])}, finished" fetchpriority="high"{(" style=\"object-position:" + p["cover_pos"] + "\"") if p.get("cover_pos") else ""}></div>
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
            f.write(head(p["seo_title"] or p["title"], desc, "../", "projects") + body + tail("../"))

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
            <div class="ph"><img src="{("images/thumbs/" + os.path.basename(p["card_img"])) if p["card_img"] else ("images/projects/" + p["slug"] + "/thumbs/" + p["imgs"][-1])}" alt="{e(p["title"])}" loading="lazy"{(" style=\"object-position:" + p["card_pos"] + "\"") if p.get("card_pos") else ""}></div>
            <div class="project-meta"><span>{i + 1:02d}</span><span>{e(p["title"])}</span><span class="cat">{e(LABEL[p["cat"]])}</span></div>
          </a>''' for i, p in enumerate(projects))
    by_town = {}
    for p in projects:
        if p["area"]:
            by_town.setdefault(p["area"], []).append(p)
    blocks = "\n".join(
        f'          <div class="area reveal" id="{area_id(t)}"><h3>{e(t)}</h3><ul>' +
        "".join(f'<li><a href="projects/{p["slug"]}.html">{e(p["seo_title"] or p["title"])}</a></li>' for p in ps) + "</ul></div>"
        for t, ps in sorted(by_town.items()))
    areas_html = f'''    <section class="pad" style="padding-top:0">
      <div class="wrap">
        <div class="sec-head reveal"><h2>Areas we cover</h2><span class="muted">Barnsley, Wakefield and across South Yorkshire</span></div>
        <div class="areas">
{blocks}
        </div>
      </div>
    </section>'''
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
{areas_html}
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
        f.write(head("Building & Roofing Projects in Barnsley", "Photos of over 100 building and roofing projects across Barnsley, Wakefield and South Yorkshire: extensions, re-roofs, loft conversions and renovations.", "", "projects")
                + listing + tail(""))
    update_home(projects)
    print(f"{n} project pages written;", counts)
    import build_services, chrome, seo
    build_services.build(sys.modules[__name__], projects)
    chrome.apply()
    seo.apply()


if __name__ == "__main__":
    main()
