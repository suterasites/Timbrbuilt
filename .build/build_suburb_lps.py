#!/usr/bin/env python3
"""
build_suburb_lps.py - generate the Decks & Pergolas suburb landing pages for Timbr Built.

One page per target suburb: decks-pergolas-<slug>.html. The chrome (head scripts, cinematic
navbar, menu overlay, rich footer, callbar) is IDENTICAL to the hand-authored pages - the site's
hard rule - and only the localised copy + per-suburb schema vary. Copy is genuinely localised
(area, council, housing character, nearby suburbs) so the pages are not thin doorway duplicates,
and it NEVER claims a specific project in a suburb (site hard rule) - only service-area framing.

Filenames are deliberately `decks-pergolas-<slug>` so the WP HQ coverage detector attributes each
to (Decks & Pergolas x <suburb>): the service term "pergola" is a substring and the suburb slug is
a contiguous token-run (so "west footscray" beats "footscray").

Run:  python3 .build/build_suburb_lps.py        (writes into the site root, one dir up)
Re-runnable: overwrites the generated files in place; hand pages are untouched.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # site root (where the .html files live)
DOMAIN = "https://timbrbuilt.com.au"

# Per-suburb data. `area`/`council` are factual geography; `hook1`/`hook2` describe the local
# housing character (period homes inner-west, coastal bayside, new estates in Wyndham) - real
# context, not fabricated project claims. `nearby` cross-links the cluster (name, slug).
SUBURBS = [
    {
        "name": "Footscray", "slug": "footscray",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Hardwood decks and pergolas for Footscray homes, built to handle Melbourne weather and finished to last.",
        "hook1": "Footscray's streets are full of Victorian terraces, workers' cottages and California bungalows, many now being renovated and extended. On compact inner-west blocks a well-built deck is some of the most valuable living space you can add, turning a tight backyard into a proper place to sit, cook and entertain.",
        "hook2": "We build hardwood and merbau decks, pergolas, patios and privacy screens that suit the character of Footscray homes and stand up to the local climate. Every job is set out properly, built by a qualified carpenter and oiled so it still looks the part years down the track.",
        "nearby": [("Seddon", "seddon"), ("Yarraville", "yarraville"), ("West Footscray", "west-footscray")],
    },
    {
        "name": "Yarraville", "slug": "yarraville",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Decks and pergolas for Yarraville's period homes, built by a local carpenter and finished properly.",
        "hook1": "Yarraville is a tightly-held village of weatherboard cottages and period homes on leafy streets. Outdoor timber here has to be sympathetic to the character of the house, so we build decks and pergolas that feel like they have always belonged, rather than something bolted on.",
        "hook2": "From a compact rear deck off the kitchen to a full pergola over an entertaining area, we work in hardwood and merbau, set out for the fall of the land and finished with an oil that suits the timber. One carpenter, start to finish, so the detailing is consistent.",
        "nearby": [("Seddon", "seddon"), ("Footscray", "footscray"), ("Newport", "newport")],
    },
    {
        "name": "Maribyrnong", "slug": "maribyrnong",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Hardwood decks and pergolas in Maribyrnong, built for the aspect and finished to last.",
        "hook1": "Maribyrnong mixes established homes with newer townhouses along the river, and a lot of its backyards have an aspect worth making the most of. A deck or pergola in the right spot turns that into usable outdoor living, whether you are chasing morning sun or afternoon shade.",
        "hook2": "We build hardwood and merbau decking, pergolas, patios and screens, set out carefully and finished so they hold up to sun and rain. You get a free on-site measure and a fixed written quote before anything starts.",
        "nearby": [("West Footscray", "west-footscray"), ("Footscray", "footscray"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Seddon", "slug": "seddon",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Decks and pergolas for Seddon's tightly-held period homes, built and finished by a local carpenter.",
        "hook1": "Seddon is a small, sought-after pocket of period cottages on compact blocks. When space is at a premium, a deck or pergola is the smartest way to add somewhere to sit and entertain without losing the whole yard, and getting the setout right matters even more.",
        "hook2": "We build hardwood and merbau decks, pergolas and screens scaled to the block, with the joinery and finishing done properly so the result suits a character home. Free measure, fixed written price, one point of contact throughout.",
        "nearby": [("Yarraville", "yarraville"), ("Footscray", "footscray"), ("Newport", "newport")],
    },
    {
        "name": "West Footscray", "slug": "west-footscray",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Hardwood decks and pergolas for West Footscray homes, built for entertaining and made to last.",
        "hook1": "West Footscray is full of California bungalows and post-war family homes, often on more generous blocks than the suburbs closer in. That space is made for a proper entertaining deck or a pergola over the alfresco, and it is worth building it once and building it right.",
        "hook2": "We build hardwood and merbau decking, pergolas, patios and privacy screens, set out for the site and finished with an oil that stands up to the weather. A qualified carpenter runs the job from measure to handover.",
        "nearby": [("Footscray", "footscray"), ("Maribyrnong", "maribyrnong"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Altona", "slug": "altona",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Decks and pergolas in Altona, built in hardwood to stand up to the bay weather and salt air.",
        "hook1": "Altona is a bayside suburb of mid-century homes and beach cottages, close enough to the water that outdoor timber has to be chosen and finished for salt air and sun. Done right, a deck here is where a lot of the year gets spent.",
        "hook2": "We build hardwood and merbau decks, pergolas and screens finished to handle coastal exposure, so they weather gracefully instead of drying out and greying off. You get a free on-site measure and a fixed written quote up front.",
        "nearby": [("Williamstown", "williamstown"), ("Newport", "newport"), ("Point Cook", "point-cook")],
    },
    {
        "name": "Williamstown", "slug": "williamstown",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Decks and pergolas for Williamstown's heritage homes, built for the sea air and finished sympathetically.",
        "hook1": "Williamstown is a heritage bayside suburb of period homes near the water, where a deck or pergola has to sit comfortably with a character streetscape and cope with the salt air off the bay. That is a detailing job as much as a building one.",
        "hook2": "We build hardwood and merbau decks, pergolas, verandahs and screens that suit period homes and are finished to weather the coastal conditions. One qualified carpenter runs the job, so the trim and the finish are consistent throughout.",
        "nearby": [("Newport", "newport"), ("Altona", "altona"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Newport", "slug": "newport",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Hardwood decks and pergolas for Newport homes, built by a local carpenter and finished to last.",
        "hook1": "Newport is an established family suburb of period and post-war homes with backyards made for classic decks and pergolas. Being close to the bay, the timber and the finish still need to be chosen for the conditions, and that is where doing it properly pays off.",
        "hook2": "We build hardwood and merbau decking, pergolas, patios and privacy screens, set out for the site and oiled to hold up outdoors. Free on-site measure, fixed written quote, and one point of contact from start to finish.",
        "nearby": [("Williamstown", "williamstown"), ("Yarraville", "yarraville"), ("Altona", "altona")],
    },
    {
        "name": "Werribee", "slug": "werribee",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Decks and pergolas in Werribee, built for bigger blocks and made for entertaining.",
        "hook1": "Werribee runs from established homes through to newer estates, and a lot of its blocks are big enough for a serious outdoor space. A well-planned deck and pergola turns a large backyard into a proper entertaining area rather than just open lawn.",
        "hook2": "We build hardwood and merbau decking, pergolas, patios and screens scaled to the block and finished to stand up to the western sun. You get a free on-site measure and a fixed written quote before we start.",
        "nearby": [("Hoppers Crossing", "hoppers-crossing"), ("Point Cook", "point-cook"), ("Tarneit", "tarneit")],
    },
    {
        "name": "Hoppers Crossing", "slug": "hoppers-crossing",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Family-friendly decks and pergolas in Hoppers Crossing, built to make the most of a generous backyard.",
        "hook1": "Hoppers Crossing is an established Wyndham suburb where homes tend to come with generous backyards. That space suits a family-friendly deck and a pergola for shade, giving you somewhere the whole household actually uses through the warmer months.",
        "hook2": "We build hardwood and merbau decks, pergolas, patios and privacy screens, set out for the site and finished to handle the sun and the seasons. A qualified carpenter runs the job from the first measure to handover.",
        "nearby": [("Werribee", "werribee"), ("Point Cook", "point-cook"), ("Tarneit", "tarneit")],
    },
    {
        "name": "Point Cook", "slug": "point-cook",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Decks and pergolas for Point Cook's contemporary homes, built to extend your alfresco living.",
        "hook1": "Point Cook is made up of newer master-planned estates with a strong outdoor-living culture, and a lot of homes are built with alfresco areas crying out to be finished off. A deck or pergola extends that space and ties the backyard back to the house.",
        "hook2": "We build hardwood and merbau decking, pergolas and screens that suit contemporary homes and are finished to weather well. You get a free on-site measure and a fixed written quote, with one carpenter across the whole job.",
        "nearby": [("Altona", "altona"), ("Werribee", "werribee"), ("Hoppers Crossing", "hoppers-crossing")],
    },
    {
        "name": "Tarneit", "slug": "tarneit",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Decks and pergolas in Tarneit, built to finish off a new-build backyard properly.",
        "hook1": "Tarneit is one of Melbourne's fastest-growing suburbs, full of new homes with backyards that are a blank slate. A deck and pergola is usually the first thing that turns a bare new-build yard into somewhere you actually want to spend time.",
        "hook2": "We build hardwood and merbau decks, pergolas, patios and screens designed to suit new homes and finished to hold up outdoors. Free on-site measure, fixed written quote, and a qualified carpenter on the tools start to finish.",
        "nearby": [("Werribee", "werribee"), ("Hoppers Crossing", "hoppers-crossing"), ("Point Cook", "point-cook")],
    },
]

# FAQ - matches the depth of the hub page. Items 0 and 3 are localised per suburb (0 opens);
# the rest are the standing deck/pergola answers, kept identical to decks-pergolas.html.
def faq_items(s):
    return [
        (f"Do you build decks and pergolas in {s['name']}?",
         f"Yes. Timbr Built is based in Melbourne's inner west and works across {s['area']}, including {s['name']} and the surrounding suburbs. Every job starts with a free on-site measure, then a fixed written quote with no obligation."),
        ("How much does a deck cost?",
         "It depends on the size, the timber you choose, the height off the ground and whether a permit is needed. Rather than guess, we give you a fixed written quote after a free on-site measure, so the price you see is the price you pay."),
        ("What timber is best for a deck in Melbourne?",
         "For most jobs we recommend an Australian hardwood like spotted gum or blackbutt, or merbau as a mid-range option. All three handle our weather well and take an oil finish. We will walk you through the trade-offs in cost, colour and upkeep before you decide."),
        (f"Do I need a permit for a deck or pergola in {s['name']}?",
         f"Sometimes. Low decks and small pergolas often do not, but height, size and boundary setbacks can trigger a building permit, and {s['council']} sets the local planning rules. We will let you know where your job sits and sort the paperwork if it is needed."),
        ("How long will my deck take to build?",
         "Most residential decks and pergolas are a matter of days to a couple of weeks on site once we start, depending on size and access. You will get a realistic timeline with your quote."),
        ("Do you repair or restore old decks?",
         "Yes. We reboard, re-level and re-oil tired decks, and repair rot, movement or a failing sub-frame. If it is worth saving we will tell you, and if it is not, we will tell you that too."),
    ]


# Shared depth sections - identical to the decks-pergolas.html hub, so a suburb page carries the
# same service detail. Each suburb still has its own hero, intro, serving band and two localised
# FAQ answers, so these shared blocks are supporting content, not the whole page.
WHAT_WE_BUILD = '''  <!-- WHAT WE BUILD -->
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">What we build</span>
        <h2 class="h-display">Outdoor timber, done properly.</h2>
        <p class="lead">From a compact rear deck to a full pergola over the alfresco, we build the outdoor structures that make a backyard usable.</p>
      </div>
      <div class="cards cards--4">
        <div class="card"><div class="card__body">
          <h3>Decks</h3>
          <p>Hardwood and merbau decks on a sound sub-frame, set out for drainage and finished level with your indoor floors so inside and out flow together.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Pergolas &amp; verandahs</h3>
          <p>Pergolas, verandahs and patio roofs for shade and shelter, sized and pitched to suit the house and built to handle Melbourne's wind and rain.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Screens &amp; privacy</h3>
          <p>Timber privacy screens, slatted panels and balustrades that block the wrong sightlines and tidy up the edges of a deck or courtyard.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Repairs &amp; restoration</h3>
          <p>Reboarding, re-levelling and re-oiling tired decks, plus repairs to rot, movement or a sub-frame that has seen better days.</p>
        </div></div>
      </div>
    </div>
  </section>'''

CHOOSING_TIMBER = '''  <!-- CHOOSING TIMBER -->
  <section class="section bg-surface">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Choosing the right timber</span>
        <h2 class="h-display">The timber sets the look and the upkeep.</h2>
      </div>
      <div class="split">
        <div>
          <p>The timber you choose sets how the deck looks and how much upkeep it asks for. Australian hardwoods like spotted gum and blackbutt are dense, hard-wearing and take an oil finish beautifully. Merbau is a popular mid-range option, rich in colour and stable underfoot. Treated pine is the budget choice and works well painted or under a roof.</p>
        </div>
        <div>
          <p>Near the bay, salt air and sun are hard on outdoor timber, so the finish matters as much as the species. We oil decks to feed the timber and slow the greying, and we will tell you honestly what each option needs year to year so there are no surprises. If you would rather not oil at all, we will talk through low-maintenance and composite alternatives too.</p>
        </div>
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
        <div class="step"><div class="step__n">01</div><h3>Get in touch</h3><p>Tell us about your yard, the look you are after and rough timing.</p></div>
        <div class="step"><div class="step__n">02</div><h3>Free on-site measure</h3><p>We visit, take levels, talk through timber and design, and confirm scope.</p></div>
        <div class="step"><div class="step__n">03</div><h3>Fixed written quote</h3><p>A clear price with no mid-job surprises, and a booked start date.</p></div>
        <div class="step"><div class="step__n">04</div><h3>Built &amp; finished</h3><p>One carpenter through to handover, oiled and the site left clean.</p></div>
      </div>
    </div>
  </section>'''


def esc(t):
    return t.replace("&", "&amp;")


def render_faq_html(items):
    chev = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 9l6 6 6-6"/></svg>'
    out = []
    for i, (q, a) in enumerate(items):
        openattr = " open" if i == 0 else ""
        out.append(
            f'''        <details class="faq__item"{openattr}>
          <summary>{esc(q)}{chev}</summary>
          <div class="faq__a"><p>{esc(a)}</p></div>
        </details>''')
    return "\n".join(out)


def render_faq_schema(items):
    entities = []
    for q, a in items:
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


def render_nearby(nearby):
    links = [f'<a class="area-link" href="decks-pergolas-{slug}.html">{name}</a>' for name, slug in nearby]
    if len(links) > 1:
        joined = ", ".join(links[:-1]) + " and " + links[-1]
    else:
        joined = links[0]
    return joined


def page_html(s):
    slug = s["slug"]
    # Clean URL: Cloudflare 308s .html -> extensionless, so declaring the .html
    # form here hands Google a canonical that redirects. Site swept 2026-09-02.
    url = f"{DOMAIN}/decks-pergolas-{slug}"
    title = f"Decks &amp; Pergolas in {esc(s['name'])} | Timbr Built"
    desc = (f"Hardwood decks and pergolas in {s['name']}, built for Melbourne weather by a local "
            f"carpenter. Free on-site measure and a fixed written quote. Call Timbr Built.")
    og_desc = desc
    items = faq_items(s)
    faq_html = render_faq_html(items)
    faq_schema = render_faq_schema(items)
    nearby_html = render_nearby(s["nearby"])

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
      "name": "Decks & Pergolas in {s['name']}",
      "serviceType": "Deck and pergola construction",
      "provider": {{ "@id": "{DOMAIN}/#business" }},
      "areaServed": {{ "@type": "City", "name": "{s['name']}" }},
      "url": "{url}"
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_schema}
      ]
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "{DOMAIN}/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Services", "item": "{DOMAIN}/services.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "Decks & Pergolas", "item": "{DOMAIN}/decks-pergolas.html" }},
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
  <meta property="og:title" content="Decks &amp; Pergolas in {esc(s['name'])} | Timbr Built">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/Assets/deck-weatherboard.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Decks &amp; Pergolas in {esc(s['name'])} | Timbr Built">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{DOMAIN}/Assets/deck-weatherboard.jpg">
    <script type="application/ld+json">
{jsonld}
  </script>
  <link rel="stylesheet" href="styles.css">
  <style>.area-link{{color:var(--timber);font-weight:600}}.area-link:hover{{text-decoration:underline}}</style>
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
      <img width="1050" height="1400" src="Assets/deck-weatherboard.jpg" alt="Oiled hardwood deck beside a weatherboard home" fetchpriority="high" decoding="async">
    </div>
    <div class="container page-hero__inner">
      <span class="eyebrow">Decks &amp; Pergolas &middot; {esc(s['name'])}</span>
      <h1 class="page-hero__title">Decks &amp; pergolas in {esc(s['name'])}.</h1>
      <p class="page-hero__lead">{esc(s['lead'])}</p>
    </div>
  </section>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/services.html">Services</a></li>
        <li><a href="/decks-pergolas.html">Decks &amp; Pergolas</a></li>
        <li aria-current="page">{esc(s['name'])}</li>
      </ol>
    </div>
  </nav>

  <!-- LOCAL INTRO + WHAT'S INCLUDED -->
  <section class="section bg-surface">
    <div class="container">
      <div class="feature">
        <div class="feature__media"><img width="618" height="1100" src="Assets/deck.jpg" alt="Freshly oiled hardwood deck with pergola post" loading="lazy" decoding="async"></div>
        <div class="feature__body">
          <span class="eyebrow">Decks &amp; pergolas in {esc(s['name'])}</span>
          <h2>Outdoor timber, built for {esc(s['name'])} homes</h2>
          <p>{esc(s['hook1'])}</p>
          <p>{esc(s['hook2'])}</p>
          <ul class="feature__list">
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Hardwood and merbau decking</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Pergolas, patios and verandahs</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Timber screens and privacy structures</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Oiling and finishing</li>
          </ul>
          <a href="contact.html" class="btn btn-primary mt-sm">Get a quote</a>
        </div>
      </div>
    </div>
  </section>

{WHAT_WE_BUILD}

{CHOOSING_TIMBER}

{HOW_WE_WORK}

  <!-- FAQ -->
  <section class="section bg-navy faq-section">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow" style="justify-content:center">FAQ</span>
        <h2 class="h-display">Decks &amp; pergolas in {esc(s['name'])}.</h2>
      </div>
      <div class="faq">
{faq_html}
      </div>
    </div>
  </section>

  <!-- SERVICE AREA / NEARBY -->
  <section class="section bg-surface">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Serving {esc(s['name'])}</span>
        <h2 class="h-display">Local, and close by.</h2>
        <p class="lead">Timbr Built is based in Melbourne's inner west and works throughout {esc(s['area'])}, part of {esc(s['council'])}. We also build decks and pergolas in nearby {nearby_html}. If your suburb is not listed, get in touch and we will let you know.</p>
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
          <h2>Planning a deck or pergola in {esc(s['name'])}?</h2>
          <p>Tell us about your yard and we will book a free on-site measure in {esc(s['name'])}, then come back with a fixed written quote in time for summer.</p>
          <div class="cta-feature__actions">
            <a href="contact.html" class="btn btn-light btn-lg">Get a free quote</a>
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
        path = os.path.join(ROOT, f"decks-pergolas-{s['slug']}.html")
        with open(path, "w") as fh:
            fh.write(page_html(s))
        written.append(os.path.basename(path))
    print(f"Wrote {len(written)} suburb LPs:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
