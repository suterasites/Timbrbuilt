#!/usr/bin/env python3
"""seo_100_patch.py - idempotent on-page SEO patcher for the Timbr Built site.

Brings every page to a clean pass on the machine-checkable checks in
Apps/sutera-seo/checklist.py (the audit engine behind SEO HQ). Safe to re-run;
every insertion is guarded by a presence check.

Fixes applied:
  - Twitter Card block (summary_large_image + title/description/image) - all indexable pages
  - JSON-LD @graph: GeneralContractor + BreadcrumbList - the 8 interior pages
    (homepage already carries GeneralContractor; a homepage crumb is pointless UX
    so it is deliberately left off, matching the ANKS house pattern)
  - visible breadcrumb nav below the hero - interior pages only
  - skip-to-content link + <main id="main"> landmark - every page
  - <header> landmark: the persistent navbar div becomes a semantic <header>
  - footer column headings h4 -> h3 (kills the H2->H4 heading-hierarchy skip);
    a .footer__h class preserves the exact look (see styles.css)
  - homepage: a visually-hidden <h2> in the showcase (kills the H1->H3 skip)
  - trimmed 3 over-long meta descriptions into the 150-160 target band
  - explicit width/height on every <img>, read from the real asset (no distortion;
    global `img { height:auto }` makes the attrs a pure CLS/aspect-ratio hint)

privacy.html + thank-you.html are noindex and not in the sitemap (not scored), so
they get only the safe structural fixes (header/main/skip-link/img-dims).
"""

import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://timbrbuilt.com.au"

# indexable pages -> canonical slug ("" == homepage)
CORE = {
    "index.html": "",
    "services.html": "services.html",
    "carpentry.html": "carpentry.html",
    "bathroom-renovations.html": "bathroom-renovations.html",
    "decks-pergolas.html": "decks-pergolas.html",
    "lockups-new-builds.html": "lockups-new-builds.html",
    "contact.html": "contact.html",
    "projects.html": "projects.html",
    "about.html": "about.html",
}
NOINDEX = ["privacy.html", "thank-you.html"]  # structural fixes only

# Visible + schema breadcrumb trail per interior page: [(name, slug_or_None)].
# slug "" -> homepage, None -> current page (no link, aria-current). Homepage omitted.
CRUMBS = {
    "services.html": [("Home", ""), ("Services", None)],
    "carpentry.html": [("Home", ""), ("Services", "services.html"), ("Carpentry", None)],
    "bathroom-renovations.html": [("Home", ""), ("Services", "services.html"), ("Bathroom Renovations", None)],
    "decks-pergolas.html": [("Home", ""), ("Services", "services.html"), ("Decks & Pergolas", None)],
    "lockups-new-builds.html": [("Home", ""), ("Services", "services.html"), ("Lockups & New Builds", None)],
    "contact.html": [("Home", ""), ("Contact", None)],
    "projects.html": [("Home", ""), ("Projects", None)],
    "about.html": [("Home", ""), ("About", None)],
}

# Trimmed meta descriptions (target 150-160 chars, were 187/174/181).
META = {
    "index.html": "Qualified local carpenter in Melbourne's inner west. Carpentry, bathroom renovations, decks, pergolas and new-build lockups. Built right, with fixed quotes.",
    "services.html": "Timbr Built services: carpentry, bathroom renovations, decks and pergolas, and new-build lockups across Melbourne's inner west. One carpenter-led team, fixed quotes.",
    "about.html": "Qualified local carpenter in Melbourne's inner west, taking on carpentry, bathroom renovations, decks and new builds with honest pricing and a quality finish.",
}

# The business entity, mirrored verbatim from index.html so rich-results dedupe
# on the shared @id and stay consistent across every page.
BUSINESS_NODE = {
    "@type": "GeneralContractor",
    "@id": SITE + "/#business",
    "name": "Timbr Built",
    "image": SITE + "/Assets/logo-navy.png",
    "logo": SITE + "/Assets/logo-navy.png",
    "telephone": "+61484698553",
    "email": "timbrbuilt@gmail.com",
    "url": SITE + "/",
    "priceRange": "$$",
    "address": {"@type": "PostalAddress", "addressLocality": "Melbourne",
                "addressRegion": "VIC", "addressCountry": "AU"},
    "areaServed": [
        {"@type": "Place", "name": "Melbourne Inner West"},
        {"@type": "Place", "name": "Hobsons Bay"},
        {"@type": "City", "name": "Williamstown"},
        {"@type": "City", "name": "Yarraville"},
        {"@type": "City", "name": "Altona"},
    ],
    "makesOffer": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Carpentry"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Bathroom Renovations"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Decks and Pergolas"}},
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "New Build Lockups"}},
    ],
}

_DIM_CACHE = {}


def img_dims(src):
    """Return (w, h) for a local asset src, or None. Cached. Remote/data URIs skipped."""
    src = src.split("?")[0].split("#")[0]
    if src.startswith(("http://", "https://", "data:", "//")):
        return None
    if src in _DIM_CACHE:
        return _DIM_CACHE[src]
    path = os.path.normpath(os.path.join(ROOT, src.lstrip("/")))
    if not path.startswith(ROOT) or not os.path.isfile(path):
        _DIM_CACHE[src] = None
        return None
    try:
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                             capture_output=True, text=True, timeout=20).stdout
        w = re.search(r"pixelWidth:\s*(\d+)", out)
        h = re.search(r"pixelHeight:\s*(\d+)", out)
        dims = (int(w.group(1)), int(h.group(1))) if w and h else None
    except Exception:
        dims = None
    _DIM_CACHE[src] = dims
    return dims


def canonical_for(slug):
    return SITE + "/" if slug == "" else f"{SITE}/{slug}"


def meta_prop(html, prop):
    m = re.search(rf'<meta property="{re.escape(prop)}" content="([^"]*)"', html)
    return m.group(1) if m else ""


def crumb_html(trail):
    lis = []
    for name, slug in trail:
        if slug is None:
            lis.append(f'        <li aria-current="page">{name}</li>')
        else:
            href = "/" if slug == "" else "/" + slug
            lis.append(f'        <li><a href="{href}">{name}</a></li>')
    return ('  <nav class="breadcrumb" aria-label="Breadcrumb">\n'
            '    <div class="container">\n'
            '      <ol>\n' + "\n".join(lis) + "\n      </ol>\n"
            "    </div>\n  </nav>\n")


def crumb_node(trail):
    items = []
    for i, (name, slug) in enumerate(trail, 1):
        it = {"@type": "ListItem", "position": i, "name": name}
        if slug is not None:
            it["item"] = canonical_for(slug)
        items.append(it)
    return {"@type": "BreadcrumbList", "itemListElement": items}


def jsonld_block(payload):
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    return f'  <script type="application/ld+json">\n{body}\n  </script>\n'


def patch(fn):
    path = os.path.join(ROOT, fn)
    html = open(path, encoding="utf-8").read()
    orig = html
    did = []
    indexable = fn in CORE
    trail = CRUMBS.get(fn)

    # --- meta description trim ---
    if fn in META:
        new = META[fn]
        html2 = re.sub(r'(<meta name="description" content=")[^"]*(">)',
                       lambda m: m.group(1) + new + m.group(2), html, count=1)
        if html2 != html:
            html = html2
            did.append(f"meta-desc({len(new)})")

    # --- Twitter Card (derive from OG) ---
    if indexable and 'name="twitter:card"' not in html:
        ogtitle = meta_prop(html, "og:title")
        ogdesc = meta_prop(html, "og:description")
        ogimg = meta_prop(html, "og:image")
        tw = ('  <meta name="twitter:card" content="summary_large_image">\n'
              f'  <meta name="twitter:title" content="{ogtitle}">\n'
              f'  <meta name="twitter:description" content="{ogdesc}">\n'
              f'  <meta name="twitter:image" content="{ogimg}">\n')
        m = re.search(r'<meta property="og:image"[^>]*>\s*\n', html)
        if m:
            html = html[:m.end()] + tw + html[m.end():]
            did.append("twitter")

    # --- JSON-LD business + breadcrumb (interior pages only) ---
    if indexable and "application/ld+json" not in html and trail:
        graph = {"@context": "https://schema.org", "@graph": [BUSINESS_NODE, crumb_node(trail)]}
        block = jsonld_block(graph)
        html = html.replace('<link rel="stylesheet" href="styles.css">',
                            block + '  <link rel="stylesheet" href="styles.css">', 1)
        did.append("jsonld")

    # --- skip-to-content link (after <body>) ---
    if "skip-link" not in html:
        html = html.replace("<body>",
                            '<body>\n  <a class="skip-link" href="#main">Skip to content</a>', 1)
        did.append("skip-link")

    # --- <header> landmark: cine-hero__bar div -> header ---
    open_marker = '<div class="cine-hero__bar">'
    if open_marker in html:
        i = html.find(open_marker)
        j = html.find("</div>", i)               # no nested <div> inside the bar
        html = (html[:i] + '<header class="cine-hero__bar">'
                + html[i + len(open_marker):j] + "</header>" + html[j + len("</div>"):])
        did.append("header")

    # --- <main id="main"> wrapper (before first <section>, close before <footer>) ---
    if not re.search(r"<main\b", html):
        m = re.search(r"[ \t]*<section\b", html)
        if m:
            html = html[:m.start()] + '  <main id="main">\n' + html[m.start():]
            html = html.replace("<footer", "</main>\n\n  <footer", 1)
            did.append("main")

    # --- footer column headings h4 -> h3 (kills H2->H4 skip; .footer__h keeps the look) ---
    if "<h4>" in html:
        html = html.replace("<h4>", '<h3 class="footer__h">').replace("</h4>", "</h3>")
        did.append("footer-h3")

    # --- homepage: visually-hidden <h2> in the showcase (kills H1->H3 skip) ---
    if fn == "index.html" and "What we do</h2>" not in html:
        anchor = '<section class="showcase bg-navy" id="services">'
        html = html.replace(anchor, anchor + '\n    <h2 class="sr-only">What we do</h2>', 1)
        did.append("showcase-h2")

    # --- visible breadcrumb nav below the hero (interior pages) ---
    if trail and 'class="breadcrumb"' not in html:
        mo = re.search(r'<main\b[^>]*>', html)
        if mo:
            sec = html.find("</section>", mo.end())   # end of the page hero
            if sec != -1:
                pt = sec + len("</section>")
                html = html[:pt] + "\n" + crumb_html(trail) + html[pt:]
                did.append("breadcrumb-nav")

    # --- explicit width/height on <img> ---
    def add_dims(m):
        tag = m.group(0)
        if re.search(r"\bwidth=", tag) and re.search(r"\bheight=", tag):
            return tag
        s = re.search(r'\bsrc="([^"]+)"', tag)
        if not s:
            return tag
        d = img_dims(s.group(1))
        if not d:
            return tag
        return re.sub(r"<img\b", f'<img width="{d[0]}" height="{d[1]}"', tag, count=1)

    new_html = re.sub(r"<img\b[^>]*>", add_dims, html)
    if new_html != html:
        did.append("img-dims")
        html = new_html

    if html != orig:
        open(path, "w", encoding="utf-8").write(html)
    return did


def main():
    files = list(CORE) + NOINDEX
    print(f"Patching {len(files)} pages under {ROOT}\n")
    for fn in files:
        changed = patch(fn)
        print(f"  {fn:30s} {', '.join(changed) if changed else 'no change (already compliant)'}")
    print("\nDone. Idempotent - safe to re-run.")


if __name__ == "__main__":
    main()
