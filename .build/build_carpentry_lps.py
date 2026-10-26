#!/usr/bin/env python3
"""
build_carpentry_lps.py - generate the Carpenter suburb landing pages for Timbr Built.

One page per suburb: carpenter-<slug>.html. Third sibling of build_suburb_lps.py (decks) and
build_bathroom_lps.py. The chrome (head scripts, cinematic navbar, menu overlay, rich footer,
callbar) is IDENTICAL to the hand-authored pages - the site's hard rule - and only the localised
copy + per-suburb schema vary.

Why "carpenter-" and not "carpentry-": the hub was retargeted off the bare "carpentry" head term on
2026-09-09 (commit 55dfbfd) because that is an informational search a local trade cannot win. The
searches it now shows for are "carpenter <place>", so the page name, title and H1 follow the
searcher's word. WP HQ attributes these pages to the Carpentry row through its `term: carpenter`
in Apps/sutera-seo/clients.yaml.

Unlike the decks and bathroom pages these carry the quote form. The 2026-09-01 Yarraville caller
landed on a suburb page that had nothing to act on but a tel: link (CRM notes, 2026-09-02).

Copy is written per suburb, not templated with the name swapped: housing character, the carpentry
that housing actually needs, and the local planning context are all different. Shared blocks (What
we do, the standing FAQ answers, the contact lead) are verbatim from carpentry.html / index.html so
they read as site components rather than copied prose. It NEVER claims a specific project in a
suburb (site hard rule), and says "qualified carpenter" only - no licensed / registered builder /
insured claims until Luca's registration is confirmed.

Run:  python3 .build/build_carpentry_lps.py     (writes into the site root, one dir up)
Re-runnable: overwrites the generated files in place; hand pages are untouched.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # site root (where the .html files live)
DOMAIN = "https://timbrbuilt.com.au"

# Per-suburb data. `p1`/`p2` describe the housing and what it asks of a carpenter, `jobs` are the
# three local work cards, `faq` the two localised questions (the first opens), `nearby` and `cta`
# close the page. `links` cross-link the carpenter cluster (name, slug).
SUBURBS = [
    {
        "name": "Newport", "slug": "newport", "council": "Hobsons Bay City Council",
        "desc": "Carpenter in Newport for framing, weatherboard and floor repairs, doors, skirting and built-ins. Free on-site measure and a fixed written quote.",
        "hero": ("hero-build.jpg", 900, 1600, "New build home with vertical cladding and black-framed windows"),
        "feature": ("build-2.jpg", 562, 1000, "Structural carpentry and framing on a new build"),
        "lead": "Framing, finish work and the repairs Newport's older homes keep asking for, from a qualified carpenter working right across Hobsons Bay.",
        "h2": "Carpentry for Newport homes",
        "p1": "Newport's housing runs from period to post-war. Close to the village and the station the streets are lined with Victorian and Edwardian weatherboards, many of them a century old and carrying the movement and patch-ups to match. Further west, towards Newport Lakes, post-war weatherboard and brick veneer homes sit on wider blocks, and plenty of them are due for the first serious renovation of their lives.",
        "p2": "That mix sets the carpentry. In the older homes it means openings out of square, floors that have dropped at the edges and weatherboards that have taken years of weather off the bay. In the post-war homes it is more often a wall coming out to open up the kitchen, a rear extension being framed, and new doors, skirting and built-ins once the plaster is up.",
        "list": ["Wall, floor and roof framing", "Weatherboard repairs and replacement",
                 "Doors, skirting and architraves", "Built-in storage and joinery",
                 "Deck and pergola framing"],
        "jobs_h2": "What Newport homes need.",
        "jobs": [
            ("Period weatherboards",
             "Rot starts in the same places on Newport's older homes: the bottom boards, under the window sills and anywhere water sits against the wall. Replacing boards properly means matching the profile and fixing back to sound timber, so the problem does not return in two winters."),
            ("Opening up post-war homes",
             "Many of the post-war homes on the western side were built with a closed-off kitchen and a separate lounge. Taking out the wall between them, framing the new opening and finishing it so it looks original changes how the whole house lives."),
            ("Floors, doors and trims",
             "A floor that dips at the edges, a door that binds every winter and skirting pulling off the wall often share one cause underneath. We find it first, and if it is the stumps rather than the timber we will say so, so new trim is never fixed to a moving problem."),
        ],
        "faq": [
            ("Do you work in Newport?",
             "Yes. Newport sits in the middle of the patch we cover, between Williamstown, Yarraville and Altona, so we are never far from a quote visit. Every job starts with a free on-site measure and a fixed written quote, with no obligation."),
            ("Can you take out a wall to open up the kitchen?",
             "Usually, yes. The first question is whether the wall is load-bearing. If it is, the opening needs a beam sized for the span and the roof above it, and structural work like that can need a building permit. We work out what the wall is carrying at the measure and tell you what is involved before you commit to anything."),
        ],
        "nearby": "Newport sits between Williamstown, Spotswood and Altona North in Hobsons Bay, a short drive from anywhere in the inner west.",
        "links": [("Williamstown", "williamstown"), ("Yarraville", "yarraville")],
        "cta": "Tell us what needs doing and we will come out for a free measure in Newport, then send a fixed written quote you can hold us to.",
    },
    {
        "name": "Williamstown", "slug": "williamstown", "council": "Hobsons Bay City Council",
        "desc": "Carpenter in Williamstown for weatherboard, verandah and floor repairs, period trims, framing and built-ins. Free on-site measure and a fixed written quote.",
        "hero": ("deck-weatherboard.jpg", 1050, 1400, "Oiled hardwood deck beside a weatherboard home"),
        "feature": ("framing-arched-window.jpg", 1050, 1400, "Timber roof framing with an arched window opening framed out"),
        "lead": "Carpentry for one of Melbourne's oldest suburbs. Weatherboard and verandah repairs, trims matched to what is already there, and the framing behind a renovation.",
        "h2": "Carpentry for Williamstown's period homes",
        "p1": "Williamstown is one of the oldest suburbs in Melbourne, and much of its housing shows it in the best way: Victorian cottages, Edwardian weatherboards and timber verandahs on streets that have changed very little in a century. The sea air that makes it a good place to live is hard on timber, and a weatherboard or verandah post facing the bay works much harder than one further inland.",
        "p2": "Carpentry here is mostly about matching what is already there. Weatherboard, skirting and architrave profiles from a hundred years ago are rarely on the shelf, so a repair has to be matched carefully rather than patched with the nearest thing at the timber yard. Done well, you cannot see where the old work stops and the new work starts.",
        "list": ["Weatherboard repairs and replacement", "Verandah posts, beams and boards",
                 "Period skirting, architraves and doors", "Framing for extensions and alterations",
                 "Built-in storage and joinery"],
        "jobs_h2": "What Williamstown homes need.",
        "jobs": [
            ("Weatherboards and salt air",
             "Near the water, paint fails sooner and the bottom boards and window sills go first. We cut out what has rotted, replace it with a matching profile and prime every face, end grain included, so the new board lasts as long as the old one did."),
            ("Verandahs",
             "On a period home the verandah is usually the first thing to show its age: posts rotting at the base, a sagging beam, boards that have cupped. We repair or rebuild the timber so it suits the front of the house, rather than swapping in something that looks bolted on."),
            ("Renovating behind the facade",
             "Plenty of Williamstown renovations keep the front rooms as they were and change everything behind them. That means framing a rear extension, tying it into an old structure that has moved over the years, then running the trims through so the two halves feel like one house."),
        ],
        "faq": [
            ("Do you work in Williamstown?",
             "Yes. Williamstown and the streets around it are a regular part of our area, along with Newport next door and Altona further along the bay. You get a free on-site measure and a fixed written quote before any work is booked."),
            ("Will a heritage overlay affect my job?",
             "It depends on your address and the work. Large parts of Williamstown sit under a heritage overlay, which can mean a planning permit for changes visible from the street, such as a new verandah or different windows. Like-for-like repairs that do not change how the house looks generally do not need one. We will raise it at the measure, and a planning property report for your address settles it either way."),
        ],
        "nearby": "Williamstown sits on the bay next to Newport and Williamstown North, at the eastern end of Hobsons Bay.",
        "links": [("Newport", "newport"), ("Yarraville", "yarraville")],
        "cta": "Tell us about the house and the job. We will see it in person, measure up for free and put the price in writing before anything starts.",
    },
    {
        "name": "Yarraville", "slug": "yarraville", "council": "Maribyrnong City Council",
        "desc": "Carpenter in Yarraville for extension framing, floor and weatherboard repairs, doors, skirting and built-in storage. Free on-site measure, fixed written quote.",
        "hero": ("laundry-walnut-joinery.jpg", 1050, 1400, "Laundry with walnut timber joinery, terrazzo splashback, stone benchtop and undermount sink"),
        "feature": ("build-cladding.jpg", 619, 1100, "New build framed and clad by Timbr Built"),
        "lead": "Framing, finish carpentry and built-in storage for Yarraville's cottages, where every room has to work hard and very little is square.",
        "h2": "Carpentry for Yarraville cottages",
        "p1": "Yarraville's streets are full of single-fronted workers' cottages and Edwardian weatherboards on narrow blocks, with the village shops at the centre. They are homes with real character and not much floor area, so when they are renovated the work tends to go one of two ways: out the back with an extension, or into the rooms that are already there to get more out of every wall.",
        "p2": "Both are carpentry. An extension starts with framing that has to tie into a hundred-year-old structure that has moved over the years. Getting more out of a small room means built-in robes, shelving and storage scribed to walls that are rarely straight, and doors and trims that suit the house rather than fight it.",
        "list": ["Framing for rear extensions", "Built-in robes, shelving and storage",
                 "Doors, skirting and architraves", "Floor and weatherboard repairs",
                 "Deck and pergola framing"],
        "jobs_h2": "What Yarraville homes need.",
        "jobs": [
            ("Built-ins for small rooms",
             "Plenty of Yarraville cottages were built without wardrobes, and a freestanding unit eats a small bedroom. A built-in that runs to the ceiling and is scribed to the walls gives the floor back, and matching its doors and trims to the rest of the house keeps it looking original."),
            ("Extensions out the back",
             "The back of a single-fronted cottage is where most of the change happens: a lean-to replaced, or a kitchen and living area added. We frame it properly, deal with the levels where new meets old, and work alongside your designer or engineer where the job has one."),
            ("Repairs between the big jobs",
             "A front door that sticks every winter, a board split beside the downpipe, a back step gone soft. Small jobs on old houses are still worth doing properly, and we will quote them rather than tell you to wait for the renovation."),
        ],
        "faq": [
            ("Do you work in Yarraville?",
             "Yes. Yarraville is a short trip for us, with Seddon, Footscray and Spotswood all close by. Book a free on-site measure and you get a fixed written quote, not an estimate that moves once the work starts."),
            ("Do I need council approval for work at the front of the house?",
             "Sometimes. Maribyrnong City Council has heritage overlays across parts of Yarraville, and inside one a change you can see from the street can need a planning permit even when it is small. Work at the back of the house is usually simpler. Your property report shows whether an overlay applies, and we will check it with you at the measure."),
        ],
        "nearby": "Yarraville sits between Seddon, Footscray and Spotswood in the City of Maribyrnong, close to everywhere else we work in the inner west.",
        "links": [("Newport", "newport"), ("Williamstown", "williamstown")],
        "cta": "Send through what you have in mind and we will book a time to look at it, measure up and come back with a written price.",
    },
]

# Standing answers, verbatim from the carpentry.html hub FAQ. The third links to the suburb's
# own decks page, which every one of these suburbs has.
STANDING_FAQ = [
    ("Do you take on small carpentry jobs?",
     "Yes. A single door that will not shut, a run of skirting after a new floor goes in or a rotten weatherboard is a normal week for us, alongside the bigger framing work. If it is genuinely a handyman job we will say so rather than quote it."),
    ("What does a carpenter cost?",
     "It depends on the work, the access and how long we are on site, so we do not publish an hourly rate that would be wrong for half the jobs. You get a free on-site measure and a fixed written quote before anything starts."),
    ("Can you do the deck or pergola as well?",
     "Yes. Deck subframes and pergola framing are carpentry, and we build the finished structure too. Decks and pergolas have their own page, with timber options and permits covered in more detail."),
]

# Verbatim from the carpentry.html hub, so the four service cards read as a component.
WHAT_WE_DO = '''  <!-- WHAT WE DO -->
  <section class="section bg-surface">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">What we do</span>
        <h2 class="h-display">Carpentry, from the frame out.</h2>
        <p class="lead">Most calls land in one of four places. Whichever yours is, it is the same carpenter on the tools from the first measure to the last cut.</p>
      </div>
      <div class="cards cards--4">
        <div class="card"><div class="card__body">
          <h3>Structural carpentry</h3>
          <p>Wall, floor and roof framing, subfloors, beams and the structural changes that come with an extension or a wall coming out. The part of the job nobody sees once it is finished, and the part everything else sits on.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Finish carpentry</h3>
          <p>Doors, skirting, architraves, linings and stairs, set out square and scribed to walls that never are. This is the stage where a renovation either looks sharp or looks close enough.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Deck &amp; pergola carpentry</h3>
          <p>Deck subframes, pergola posts and outdoor timber built to take the weather this side of town. If you want the finished structure rather than the carpentry behind it, that lives on our <a href="decks-pergolas.html">decks and pergolas</a> page.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Repairs &amp; alterations</h3>
          <p>Rotten weatherboards, sagging floors, doors that have not closed properly in years, and the jobs that are too small for a builder and too involved for a handyman. Fixed quote, booked date, done.</p>
        </div></div>
      </div>
    </div>
  </section>'''

HOW_WE_WORK = '''  <!-- HOW WE WORK -->
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow" style="justify-content:center">How we work</span>
        <h2 class="h-display">From measure to handover.</h2>
      </div>
      <div class="steps">
        <div class="step"><div class="step__n">01</div><h3>Get in touch</h3><p>Tell us what needs doing, where the house is and rough timing.</p></div>
        <div class="step"><div class="step__n">02</div><h3>Free on-site measure</h3><p>We look at the job, take levels and confirm the scope with you.</p></div>
        <div class="step"><div class="step__n">03</div><h3>Fixed written quote</h3><p>A clear price before anything starts, and a booked start date.</p></div>
        <div class="step"><div class="step__n">04</div><h3>Built &amp; finished</h3><p>One carpenter through to handover, and the site left clean.</p></div>
      </div>
    </div>
  </section>'''

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'


def esc(t):
    return t.replace("&", "&amp;")


def faq_items(s):
    return list(s["faq"]) + STANDING_FAQ


def render_faq_html(s):
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg>'
    out = []
    for i, (q, a) in enumerate(faq_items(s)):
        openattr = " open" if i == 0 else ""
        body = esc(a)
        if q.startswith("Can you do the deck"):
            body = body.replace("have their own page",
                                f'have <a href="decks-pergolas-{s["slug"]}.html">their own page</a>')
        out.append(
            f'''        <details class="faq__item"{openattr}>
          <summary>{esc(q)}{chev}</summary>
          <div class="faq__a"><p>{body}</p></div>
        </details>''')
    return "\n".join(out)


def render_faq_schema(s):
    entities = []
    for q, a in faq_items(s):
        q_j = q.replace('"', '\\"')
        a_j = a.replace('"', '\\"')
        entities.append(
            '        {\n'
            '          "@type": "Question",\n'
            f'          "name": "{q_j}",\n'
            '          "acceptedAnswer": {\n'
            '            "@type": "Answer",\n'
            f'            "text": "{a_j}"\n'
            '          }\n'
            '        }')
    return ",\n".join(entities)


def render_jobs(s):
    cards = []
    for h, p in s["jobs"]:
        cards.append(
            f'''        <div class="card"><div class="card__body">
          <h3>{esc(h)}</h3>
          <p>{esc(p)}</p>
        </div></div>''')
    return "\n".join(cards)


def render_links(s):
    links = [f'<a class="area-link" href="carpenter-{slug}.html">{name}</a>' for name, slug in s["links"]]
    return " and ".join(links)


def page_html(s):
    slug = s["slug"]
    name = esc(s["name"])
    # Clean URL: Cloudflare 308s .html -> extensionless, so the canonical is the clean form.
    url = f"{DOMAIN}/carpenter-{slug}"
    title = f"Carpenter in {name} | Timbr Built"
    desc = s["desc"]
    hero_src, hero_w, hero_h, hero_alt = s["hero"]
    feat_src, feat_w, feat_h, feat_alt = s["feature"]
    feature_list = "\n".join(f"            <li>{CHECK}{esc(li)}</li>" for li in s["list"])

    jsonld = f'''{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "GeneralContractor",
      "@id": "{DOMAIN}/#business",
      "name": "Timbr Built",
      "image": "{DOMAIN}/Assets/logo-navy.png",
      "logo": "{DOMAIN}/Assets/logo-navy.png",
      "telephone": "+61484698553",
      "email": "timbrbuilt@gmail.com",
      "url": "{DOMAIN}/",
      "priceRange": "$$",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "Melbourne",
        "addressRegion": "VIC",
        "addressCountry": "AU"
      }},
      "areaServed": {{
        "@type": "City",
        "name": "{s['name']}"
      }}
    }},
    {{
      "@type": "Service",
      "name": "Carpenter in {s['name']}",
      "serviceType": "Carpenter",
      "provider": {{ "@id": "{DOMAIN}/#business" }},
      "areaServed": {{ "@type": "City", "name": "{s['name']}" }},
      "url": "{url}"
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{render_faq_schema(s)}
      ]
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "{DOMAIN}/services.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "Carpentry", "item": "{DOMAIN}/carpentry.html" }},
        {{ "@type": "ListItem", "position": 4, "name": "{s['name']}" }}
      ]
    }}
  ]
}}'''

    return f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow">
  <link rel="icon" href="Assets/icon-navy.png">
  <link rel="apple-touch-icon" href="Assets/icon-navy.png">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/Assets/{hero_src}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{DOMAIN}/Assets/{hero_src}">
    <script type="application/ld+json">
{jsonld}
  </script>
  <link rel="stylesheet" href="styles.css">
  <style>.area-link{{color:var(--timber);font-weight:600}}.area-link:hover{{text-decoration:underline}}.faq__a a{{color:inherit;text-decoration:underline}}@media (min-width:900px){{.cards--3{{grid-template-columns:repeat(3,1fr)}}}}</style>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-DX5560F0FC"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-DX5560F0FC');
  </script>
  <!-- Sutera lead events (GA4) -->
  <script>/* SUTERA_LEAD_EVENTS */
  (function(){{
    function ev(n, p){{ if (typeof window.gtag === 'function') {{ window.gtag('event', n, Object.assign({{transport_type:'beacon'}}, p||{{}})); }} }}
    document.addEventListener('click', function(e){{
      var a = e.target.closest ? e.target.closest('a[href^="tel:"]') : null;
      if (a) ev('click_to_call', {{ link_url: a.getAttribute('href') }});
    }}, true);
    document.addEventListener('submit', function(e){{
      var f = e.target;
      if (!f || f.tagName !== 'FORM' || f.hasAttribute('data-no-lead')) return;
      var action = f.getAttribute('action') || '';
      var isLead = /formspree/i.test(action) || f.querySelector('input[type="email"], input[type="tel"], textarea');
      if (isLead) ev('generate_lead', {{ form_id: f.id || f.getAttribute('name') || 'contact' }});
    }}, true);
  }})();
  </script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <!-- PERSISTENT CINEMATIC NAVBAR -->
  <header class="cine-hero__bar">
    <button class="cine-menu" data-menu-toggle aria-label="Open menu">
      <span class="bars"><span></span><span></span><span></span></span> Menu
    </button>
    <a class="cine-brand" href="index.html" aria-label="Timbr Built home"><img width="2342" height="379" src="Assets/wordmark-white-trim.png" alt="Timbr Built"></a>
    <nav class="cine-hero__nav">
      <a class="count-pill" href="services.html">Services <span class="n">4</span>
        <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 9l4-4 4 4M8 15l4 4 4-4"/></svg>
      </a>
      <a class="count-pill" href="projects.html">Projects <span class="n">16</span>
        <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 9l4-4 4 4M8 15l4 4 4-4"/></svg>
      </a>
      <a href="contact.html">Contact</a>
    </nav>
  </header>
  <!-- FULL-SCREEN MENU OVERLAY -->
  <div class="menu-overlay" id="menuOverlay">
    <img width="950" height="894" class="menu-overlay__brand" src="Assets/icon-white-mark.png" alt="" aria-hidden="true">
    <div class="menu-overlay__top">
      <button class="menu-overlay__close" data-menu-toggle aria-label="Close menu">
        Close
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 6l12 12M18 6L6 18"/></svg>
      </button>
    </div>
    <nav class="menu-overlay__links">
      <a class="mrow mrow--link" href="index.html">Home</a>
      <details class="mrow mrow--group" open>
        <summary class="mrow__head">Services <svg class="mrow__chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg></summary>
        <div class="mrow__sub">
          <a href="services.html">All services</a>
          <a href="carpentry.html">Carpentry</a>
          <a href="bathroom-renovations.html">Bathroom renovations</a>
          <a href="decks-pergolas.html">Decks &amp; pergolas</a>
          <a href="lockups-new-builds.html">Lockups &amp; new builds</a>
        </div>
      </details>
      <a class="mrow mrow--link" href="projects.html">Projects</a>
      <a class="mrow mrow--link" href="about.html">About</a>
      <a class="mrow mrow--link" href="contact.html">Contact</a>
    </nav>
    <div class="menu-overlay__foot">
      <a href="tel:+61484698553" data-conversion="call">0484 698 553</a>
      <a href="mailto:timbrbuilt@gmail.com">timbrbuilt@gmail.com</a>
      <span>Melbourne's Inner West, VIC</span>
    </div>
  </div>

  <!-- CINEMATIC PAGE HERO -->
  <main id="main">
  <section class="page-hero">
    <div class="page-hero__media">
      <img width="{hero_w}" height="{hero_h}" src="Assets/{hero_src}" alt="{hero_alt}" fetchpriority="high" decoding="async">
    </div>
    <div class="container page-hero__inner">
      <span class="eyebrow">Carpentry &middot; {name}</span>
      <h1 class="page-hero__title">Carpenter in {name}.</h1>
      <p class="page-hero__lead">{esc(s['lead'])}</p>
    </div>
  </section>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/services.html">Services</a></li>
        <li><a href="/carpentry.html">Carpentry</a></li>
        <li aria-current="page">{name}</li>
      </ol>
    </div>
  </nav>

  <!-- LOCAL INTRO + WHAT'S INCLUDED -->
  <section class="section bg-surface">
    <div class="container">
      <div class="feature">
        <div class="feature__media"><img width="{feat_w}" height="{feat_h}" src="Assets/{feat_src}" alt="{feat_alt}" loading="lazy" decoding="async"></div>
        <div class="feature__body">
          <span class="eyebrow">Carpenter in {name}</span>
          <h2>{esc(s['h2'])}</h2>
          <p>{esc(s['p1'])}</p>
          <p>{esc(s['p2'])}</p>
          <ul class="feature__list">
{feature_list}
          </ul>
          <a href="#quote" class="btn btn-primary mt-sm">Get a quote</a>
        </div>
      </div>
    </div>
  </section>

  <!-- LOCAL WORK -->
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Local work</span>
        <h2 class="h-display">{esc(s['jobs_h2'])}</h2>
      </div>
      <div class="cards cards--3">
{render_jobs(s)}
      </div>
    </div>
  </section>

{WHAT_WE_DO}

{HOW_WE_WORK}

  <!-- FAQ -->
  <section class="section bg-navy faq-section">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow" style="justify-content:center">FAQ</span>
        <h2 class="h-display">Carpentry in {name}.</h2>
      </div>
      <div class="faq">
{render_faq_html(s)}
      </div>
    </div>
  </section>

  <!-- QUOTE FORM -->
  <section class="section bg-surface" id="quote">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow" style="justify-content:center">Get a quote</span>
        <h2 class="h-display">Talk to Timbr Built.</h2>
        <p class="lead" style="margin:0 auto">Tell us about your project and we'll book a free on-site measure, then come back with a fixed written price. Prefer to talk? Call Luca directly on 0484 698 553.</p>
      </div>
      <div class="split" style="align-items:flex-start">
        <div>
          <ul class="contact-list">
            <li>
              <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h2.28a1 1 0 01.95.68l1.5 4.5a1 1 0 01-.27 1.06L7.91 10.91a12.05 12.05 0 005.18 5.18l1.67-1.55a1 1 0 011.06-.27l4.5 1.5a1 1 0 01.68.95V19a2 2 0 01-2 2h-1C9.72 21 3 14.28 3 6V5z"/></svg></span>
              <div><div class="lbl">Phone</div><a class="val" href="tel:+61484698553" data-conversion="call">0484 698 553</a></div>
            </li>
            <li>
              <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4h16v16H4z"/><path stroke-linecap="round" stroke-linejoin="round" d="M4 6l8 6 8-6"/></svg></span>
              <div><div class="lbl">Email</div><a class="val" href="mailto:timbrbuilt@gmail.com">timbrbuilt@gmail.com</a></div>
            </li>
            <li>
              <span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 21s-7-6-7-11a7 7 0 1114 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></span>
              <div><div class="lbl">Service area</div><span class="val">Melbourne's inner west &amp; Hobsons Bay</span></div>
            </li>
            <li>
              <span class="ic">{CHECK}</span>
              <div><div class="lbl">Quotes</div><span class="val">Free on-site measure, fixed price</span></div>
            </li>
          </ul>
        </div>
        <div>
          <form class="form-card" action="https://formspree.io/f/mpqgvdlj" method="POST" data-track-gclid>
            <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
            <input type="hidden" name="_next" value="https://timbrbuilt.com.au/thank-you">
            <input type="hidden" name="_source" value="carpenter-{slug}">
            <input type="hidden" name="gclid" value="">
            <input type="hidden" name="landing_url" value="">
            <input type="hidden" name="referrer" value="">
            <div class="field-row">
              <div class="field">
                <label for="q-name">Name <span class="req">*</span></label>
                <input class="input" id="q-name" name="name" type="text" required autocomplete="name" placeholder="Your name">
              </div>
              <div class="field">
                <label for="q-phone">Phone <span class="req">*</span></label>
                <input class="input" id="q-phone" name="phone" type="tel" required inputmode="tel" autocomplete="tel" placeholder="04XX XXX XXX">
              </div>
            </div>
            <div class="field-row">
              <div class="field">
                <label for="q-email">Email <span class="opt">(optional)</span></label>
                <input class="input" id="q-email" name="email" type="email" autocomplete="email" placeholder="you@email.com">
              </div>
              <div class="field">
                <label for="q-suburb">Suburb <span class="req">*</span></label>
                <input class="input" id="q-suburb" name="suburb" type="text" required placeholder="e.g. {name}">
              </div>
            </div>
            <div class="field">
              <label for="q-service">What do you need? <span class="req">*</span></label>
              <select class="input" id="q-service" name="service" required>
                <option value="" disabled>Select a service</option>
                <option selected>Carpentry</option>
                <option>Bathroom renovation</option>
                <option>Deck or pergola</option>
                <option>New build or lockup</option>
                <option>Something else</option>
              </select>
            </div>
            <div class="field">
              <label for="q-message">Project details <span class="opt">(optional)</span></label>
              <textarea class="input" id="q-message" name="message" rows="3" placeholder="Tell us a bit about the job, the house and your timing..."></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-lg" style="width:100%">Request My Free Quote</button>
            <p class="form-note">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.6-4A12 12 0 0112 2.9 12 12 0 013.4 6 12 12 0 003 9c0 5.6 3.8 10.3 9 11.6 5.2-1.3 9-6 9-11.6 0-1-.1-2.1-.4-3z"/></svg>
              Free, no-obligation quote. Your details stay private.
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>

  <!-- SERVICE AREA / NEARBY -->
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Serving {name}</span>
        <h2 class="h-display">Local, and close by.</h2>
        <p class="lead">{esc(s['nearby'])} We are also the carpenter to call in {render_links(s)}, and every suburb we cover is on the main <a class="area-link" href="carpentry.html">carpentry</a> page.</p>
      </div>
    </div>
  </section>

  <!-- IMAGE CTA -->
  <section class="cta-feature-section">
    <div class="container">
      <div class="cta-feature">
        <div class="cta-feature__media">
          <img width="1400" height="750" src="Assets/pergola-framing.jpg" alt="" loading="lazy" decoding="async">
        </div>
        <div class="cta-feature__body">
          <h2>Need a carpenter in {name}?</h2>
          <p>{esc(s['cta'])}</p>
          <div class="cta-feature__actions">
            <a href="#quote" class="btn btn-light btn-lg">Get a free quote</a>
            <a href="tel:+61484698553" data-conversion="call" class="btn cta-feature__ghost btn-lg">Talk to us</a>
          </div>
        </div>
      </div>
    </div>
  </section>
  </main>

  <footer class="footer">
    <div class="container">
      <div class="footer__main">
        <div>
          <div class="footer__cols">
            <div class="footer__col">
              <h3 class="footer__h">Explore</h3>
              <nav class="footer__nav">
                <a href="services.html">Services</a>
                <a href="projects.html">Projects</a>
                <a href="about.html">About</a>
                <a href="contact.html">Contact</a>
              </nav>
            </div>
            <div class="footer__col">
              <h3 class="footer__h">Our services</h3>
              <ul>
                <li><a href="carpentry.html">Carpentry</a></li>
                <li><a href="bathroom-renovations.html">Bathroom Renovations</a></li>
                <li><a href="decks-pergolas.html">Decks &amp; Pergolas</a></li>
                <li><a href="lockups-new-builds.html">Lockups &amp; New Builds</a></li>
              </ul>
            </div>
            <div class="footer__col">
              <h3 class="footer__h">Reach us <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6"/></svg></h3>
              <div class="footer__reach">
                <a href="tel:+61484698553" data-conversion="call">0484 698 553</a>
                <a href="mailto:timbrbuilt@gmail.com">timbrbuilt@gmail.com</a>
                <span>Melbourne's Inner West</span>
                <span>Hobsons Bay, VIC</span>
              </div>
            </div>
          </div>
        </div>
        <div class="footer__cards">
          <a class="fcard" href="contact.html">
            <div class="fcard__thumb"><img width="292" height="520" src="Assets/bathroom-arched-cabinet-sm.jpg" alt="" loading="lazy"></div>
            <h3>Get a free quote</h3>
            <p>Tell us about your project. Free on-site measure and a fixed written price, no obligation.</p>
            <span class="fcard__btn">Request a quote <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6"/></svg></span>
          </a>
          <a class="fcard" href="projects.html">
            <div class="fcard__thumb"><img width="390" height="520" src="Assets/bathroom-barn-door-sm.jpg" alt="" loading="lazy"></div>
            <h3>Recent work</h3>
            <p>See finished bathrooms, decks and new builds across Melbourne's inner west.</p>
            <span class="fcard__btn">View projects <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 6l6 6-6 6"/></svg></span>
          </a>
        </div>
      </div>
      <div class="footer__bottom">
        <div class="meta">
          <span>&copy; <span id="year"></span> Timbr Built</span>
          <span>ABN 35 667 385 734</span>
          <span>Melbourne's Inner West, VIC</span>
        </div>
        <div class="meta"><a href="privacy.html">Privacy Policy</a></div>
      </div>
    </div>
  </footer>
  <div class="callbar">
    <a href="tel:+61484698553" data-conversion="call"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h2.28a1 1 0 01.95.68l1.5 4.5a1 1 0 01-.27 1.06L7.91 10.91a12.05 12.05 0 005.18 5.18l1.67-1.55a1 1 0 011.06-.27l4.5 1.5a1 1 0 01.68.95V19a2 2 0 01-2 2h-1C9.72 21 3 14.28 3 6V5z"/></svg>Call</a>
    <a href="contact.html" class="is-quote">Get a Quote</a>
  </div>

  <script src="main.js" defer></script>
</body>
</html>
'''


def main():
    written = []
    for s in SUBURBS:
        path = os.path.join(ROOT, f"carpenter-{s['slug']}.html")
        with open(path, "w") as fh:
            fh.write(page_html(s))
        written.append(os.path.basename(path))
    print(f"Wrote {len(written)} carpenter suburb LPs:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
