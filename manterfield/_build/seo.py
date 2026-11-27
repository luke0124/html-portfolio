#!/usr/bin/env python3
"""Add SEO tags to every page and write robots.txt + sitemap.xml.

Adds (between <!-- seo:start --> and <!-- seo:end --> in each <head>):
  - canonical link
  - Open Graph / Twitter tags (so shared links show a title, text and photo)
  - LocalBusiness structured data on the home and contact pages

Safe to re-run any time; the generators (build_projects.py, build_legal.py)
call it automatically. Run on its own after hand-editing a page:

    python3 manterfield/_build/seo.py
"""
import datetime
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DOMAIN = "https://www.manterfieldbuilders.co.uk"
DEFAULT_IMAGE = "videos/hero2-poster.jpg"  # 1920x1080, used for link previews

BLOCK_RE = re.compile(r"\n?[ \t]*<!-- seo:start -->.*?<!-- seo:end -->", re.S)

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": ["GeneralContractor", "RoofingContractor"],
    "@id": DOMAIN + "/#business",
    "name": "Manterfield Building & Roofing Ltd",
    "url": DOMAIN + "/",
    "logo": DOMAIN + "/images/logo-round.webp",
    "image": DOMAIN + "/" + DEFAULT_IMAGE,
    "description": "Family run builders and roofers in Barnsley, South Yorkshire: building, extensions, roofing, renovations and loft conversions.",
    "telephone": "+441226781344",
    "email": "manterfield1@btinternet.com",
    "vatID": "GB184269675",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "259a Pontefract Road",
        "addressLocality": "Cudworth",
        "addressRegion": "South Yorkshire",
        "postalCode": "S72 8AQ",
        "addressCountry": "GB",
    },
    "areaServed": ["Barnsley", "Wakefield", "Sheffield", "Leeds", "South Yorkshire"],
    "hasMap": "https://www.google.com/maps?cid=11234015266589093734",
    # Opening hours: Monday to Friday, 8am to 5pm (also shown on the Contact page and in the footer)
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:00",
        "closes": "17:00",
    }],
    "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Building and roofing services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "url": DOMAIN + "/services/" + sid + ".html"}}
            for sid, n in [("building", "Building work"), ("extensions", "House extensions"), ("roofing", "Roofing and re-roofs"),
                           ("renovations", "Home renovations"), ("loft-conversions", "Loft conversions"),
                           ("commercial", "Commercial building"), ("landscaping", "Patios, driveways and landscaping")]
        ],
    },
    "sameAs": [
        "https://www.facebook.com/profile.php?id=61560415476579",
        "https://www.instagram.com/manterfield.building",
        "https://www.fmb.org.uk/builder/manterfield-building-roofing-limited.html",
    ],
}


def e(s):
    return html.escape(s, quote=True)


def pages():
    out = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    for sub in ("services", "projects"):
        d = os.path.join(SITE, sub)
        if os.path.isdir(d):
            out += [sub + "/" + f for f in sorted(os.listdir(d)) if f.endswith(".html")]
    return [p for p in out if p != "404.html"]


def url_for(rel):
    return DOMAIN + "/" if rel == "index.html" else DOMAIN + "/" + rel


def apply():
    today = datetime.date.today().isoformat()
    for rel in pages():
        path = os.path.join(SITE, rel)
        s = open(path, encoding="utf-8").read()
        s = BLOCK_RE.sub("", s)
        title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip())
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        desc = html.unescape(m.group(1)) if m else ""
        img = DOMAIN + "/" + DEFAULT_IMAGE
        cover = re.search(r'class="proj-cover[^"]*" src="\.\./([^"]+)"', s)
        if cover:
            img = DOMAIN + "/" + cover.group(1)
        url = url_for(rel)
        lines = [
            '  <!-- seo:start -->',
            f'  <link rel="canonical" href="{url}">',
            '  <meta property="og:type" content="website">',
            '  <meta property="og:site_name" content="Manterfield Building &amp; Roofing">',
            '  <meta property="og:locale" content="en_GB">',
            f'  <meta property="og:title" content="{e(title)}">',
            f'  <meta property="og:description" content="{e(desc)}">',
            f'  <meta property="og:url" content="{url}">',
            f'  <meta property="og:image" content="{img}">',
            '  <meta name="twitter:card" content="summary_large_image">',
        ]
        if rel in ("index.html", "contact.html"):
            lines.append('  <script type="application/ld+json">' + json.dumps(LOCAL_BUSINESS, ensure_ascii=False) + "</script>")
        # Breadcrumbs (Home > Services/Projects > page) and a Service entry for service pages
        if rel.startswith(("projects/", "services/")):
            section, section_url = (("Projects", DOMAIN + "/projects.html") if rel.startswith("projects/")
                                    else ("Services", DOMAIN + "/services.html"))
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
            name = html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else title
            crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                {"@type": "ListItem", "position": 2, "name": section, "item": section_url},
                {"@type": "ListItem", "position": 3, "name": name, "item": url}]}
            lines.append('  <script type="application/ld+json">' + json.dumps(crumbs, ensure_ascii=False) + "</script>")
            if rel.startswith("services/"):
                svc = {"@context": "https://schema.org", "@type": "Service", "name": name, "url": url,
                       "description": desc, "provider": {"@id": DOMAIN + "/#business"},
                       "areaServed": LOCAL_BUSINESS["areaServed"]}
                lines.append('  <script type="application/ld+json">' + json.dumps(svc, ensure_ascii=False) + "</script>")
        lines.append("  <!-- seo:end -->")
        s = s.replace("</head>", "\n".join(lines) + "\n</head>", 1)
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)

    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for rel in pages():
            pr = "1.0" if rel == "index.html" else ("0.9" if rel.startswith("services/") else ("0.8" if "/" not in rel else "0.5"))
            f.write(f"  <url><loc>{url_for(rel)}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    print(f"seo: tags added to {len(pages())} pages; sitemap.xml and robots.txt written")


if __name__ == "__main__":
    apply()
