#!/usr/bin/env python3
"""
build_bathroom_lps.py - generate the Bathroom Renovation suburb landing pages for Timbr Built.

One page per target suburb: bathroom-renovations-<slug>.html. The chrome (head scripts, cinematic
navbar, menu overlay, rich footer, callbar) is IDENTICAL to the hand-authored pages - the site's
hard rule - and only the localised copy + per-suburb schema vary. Copy is genuinely localised
(area, council, housing character, nearby suburbs) so the pages are not thin doorway duplicates,
and it NEVER claims a specific project in a suburb (site hard rule) - only service-area framing.

Filenames are deliberately `bathroom-renovations-<slug>` so the WP HQ coverage detector attributes
each to (Bathroom Renovations x <suburb>): the service term "bathroom renovation" is a substring and
the suburb slug is a contiguous token-run (so "west footscray" beats "footscray").

Honesty guardrails (site CLAUDE.md): "qualified carpenter" only - no "licensed / registered builder
/ insured" claims; Timbr coordinates the licensed plumber, waterproofer, tiler and electrician and
builds the joinery in-house; no fabricated projects, reviews or years-in-trade.

Run:  python3 .build/build_bathroom_lps.py     (writes into the site root, one dir up)
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
        "lead": "Full bathroom renovations for Footscray homes, coordinated by one carpenter from the strip-out to the final fit-off.",
        "hook1": "Footscray's streets are full of Victorian terraces, workers' cottages and California bungalows, and a lot of them still have their original bathroom. On a compact inner-west block the bathroom is often the room that dates the whole house, so a well-planned renovation is one of the highest-value changes you can make.",
        "hook2": "We run the full job, coordinating the plumber, waterproofer, tiler and electrician while building the vanity and joinery ourselves. Everything is waterproofed to the Australian Standard and set out properly, so the finish looks the part and holds up for years.",
        "nearby": [("Seddon", "seddon"), ("Yarraville", "yarraville"), ("West Footscray", "west-footscray")],
    },
    {
        "name": "Yarraville", "slug": "yarraville",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Bathroom renovations for Yarraville's period homes, coordinated start to finish and finished sympathetically.",
        "hook1": "Yarraville is a tightly-held village of weatherboard cottages and period homes, where a renovated bathroom has to sit comfortably with the character of the house rather than feel bolted on. Getting the proportions, tiling and joinery right is what makes an old bathroom feel considered instead of generic.",
        "hook2": "We manage the whole renovation with one point of contact, coordinating every trade and building the vanity and cabinetry in-house. Waterproofing is done to standard and the tiling set out carefully, so the room is put together properly and lasts.",
        "nearby": [("Seddon", "seddon"), ("Footscray", "footscray"), ("Newport", "newport")],
    },
    {
        "name": "Maribyrnong", "slug": "maribyrnong",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Full bathroom renovations in Maribyrnong, managed by one carpenter and built to last.",
        "hook1": "Maribyrnong mixes established homes with newer townhouses, and its bathrooms range from tired originals to builder-grade fit-outs that never quite worked. Either way, a proper renovation turns the room into something that suits how the household actually uses it.",
        "hook2": "We coordinate the plumber, waterproofer, tiler and electrician, and build the vanity and storage ourselves, for a bathroom put together properly. You get a free on-site measure and a fixed written quote before anything starts.",
        "nearby": [("West Footscray", "west-footscray"), ("Footscray", "footscray"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Seddon", "slug": "seddon",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Bathroom renovations for Seddon's period cottages, coordinated end to end by a local carpenter.",
        "hook1": "Seddon is a small, sought-after pocket of period cottages on compact blocks, where bathrooms are often small and original. When space is tight, a smart layout and the right joinery make all the difference between a cramped room and one that feels generous.",
        "hook2": "We manage the full renovation, coordinating every trade and building the vanity and cabinetry to suit the space. Waterproofing to standard, careful tiling, and one point of contact from strip-out to fit-off.",
        "nearby": [("Yarraville", "yarraville"), ("Footscray", "footscray"), ("Newport", "newport")],
    },
    {
        "name": "West Footscray", "slug": "west-footscray",
        "area": "Melbourne's inner west", "council": "the City of Maribyrnong",
        "lead": "Full bathroom renovations for West Footscray homes, coordinated by one carpenter and finished to last.",
        "hook1": "West Footscray is full of California bungalows and post-war family homes, often with a main bathroom that has not been touched in decades. A full renovation is a chance to fix the layout, add proper storage and bring the room up to the standard of the rest of the house.",
        "hook2": "We handle the whole job, coordinating the plumber, waterproofer, tiler and electrician while building the joinery ourselves. Everything is waterproofed to the Australian Standard, so the finish lasts and the wet areas stay sound.",
        "nearby": [("Footscray", "footscray"), ("Maribyrnong", "maribyrnong"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Altona", "slug": "altona",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Bathroom renovations in Altona, coordinated start to finish and built for a coastal home.",
        "hook1": "Altona is a bayside suburb of mid-century homes and beach cottages, where bathrooms cope with salt air and moisture year round. Good ventilation, moisture-resistant materials and proper waterproofing matter even more this close to the water.",
        "hook2": "We run the full renovation with one point of contact, coordinating every trade and building the vanity and cabinetry ourselves. Waterproofing is done to standard and the room set up to handle the conditions, so it stays looking the part.",
        "nearby": [("Williamstown", "williamstown"), ("Newport", "newport"), ("Point Cook", "point-cook")],
    },
    {
        "name": "Williamstown", "slug": "williamstown",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Bathroom renovations for Williamstown's heritage homes, coordinated end to end and finished sympathetically.",
        "hook1": "Williamstown is a heritage bayside suburb of period homes near the water, where a renovated bathroom has to respect a character house and stand up to the salt air off the bay. That is a detailing job as much as a building one.",
        "hook2": "We manage the whole renovation, coordinating the plumber, waterproofer, tiler and electrician and building the joinery in-house so the detailing is consistent. Waterproofing to standard, careful tiling, and one carpenter across the job.",
        "nearby": [("Newport", "newport"), ("Altona", "altona"), ("Yarraville", "yarraville")],
    },
    {
        "name": "Newport", "slug": "newport",
        "area": "the Hobsons Bay bayside", "council": "the City of Hobsons Bay",
        "lead": "Full bathroom renovations for Newport homes, managed by a local carpenter from strip-out to fit-off.",
        "hook1": "Newport is an established family suburb of period and post-war homes, many with original bathrooms that are due for an update. A full renovation is the chance to modernise the layout and add the storage a family bathroom actually needs.",
        "hook2": "We coordinate every trade and build the vanity and cabinetry ourselves, for a bathroom put together properly and finished to last. Free on-site measure, fixed written quote, and one point of contact throughout.",
        "nearby": [("Williamstown", "williamstown"), ("Yarraville", "yarraville"), ("Altona", "altona")],
    },
    {
        "name": "Werribee", "slug": "werribee",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Bathroom renovations in Werribee, coordinated start to finish and built to suit the home.",
        "hook1": "Werribee runs from established homes through to newer estates, so its bathrooms range from dated originals to builder-grade fit-outs ready for an upgrade. A proper renovation turns either one into a room that works for the household.",
        "hook2": "We manage the full job, coordinating the plumber, waterproofer, tiler and electrician while building the joinery ourselves. Waterproofing to the Australian Standard, careful tiling, and a fixed written quote before we start.",
        "nearby": [("Hoppers Crossing", "hoppers-crossing"), ("Point Cook", "point-cook"), ("Tarneit", "tarneit")],
    },
    {
        "name": "Hoppers Crossing", "slug": "hoppers-crossing",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Full bathroom renovations in Hoppers Crossing, coordinated by one carpenter and built for family life.",
        "hook1": "Hoppers Crossing is an established Wyndham suburb of family homes, where the main bathroom and ensuite do a lot of work. A well-planned renovation adds the storage and durability a busy household needs, without the builder-grade compromises.",
        "hook2": "We coordinate every trade and build the vanity and cabinetry in-house, for a bathroom that is put together properly and holds up. Free on-site measure and a fixed written quote up front.",
        "nearby": [("Werribee", "werribee"), ("Point Cook", "point-cook"), ("Tarneit", "tarneit")],
    },
    {
        "name": "Point Cook", "slug": "point-cook",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Bathroom and ensuite renovations for Point Cook's contemporary homes, coordinated end to end.",
        "hook1": "Point Cook is made up of newer master-planned estates, and a lot of its homes came with builder-grade bathrooms that are ready for something better. A renovation is the chance to upgrade the finishes, joinery and layout to match the rest of a contemporary home.",
        "hook2": "We run the full renovation with one point of contact, coordinating the trades and building the vanity and storage ourselves. Waterproofing to standard, considered tiling, and a finish that suits the house.",
        "nearby": [("Altona", "altona"), ("Werribee", "werribee"), ("Hoppers Crossing", "hoppers-crossing")],
    },
    {
        "name": "Tarneit", "slug": "tarneit",
        "area": "Melbourne's western growth corridor", "council": "the City of Wyndham",
        "lead": "Bathroom and ensuite renovations in Tarneit, coordinated start to finish by a local carpenter.",
        "hook1": "Tarneit is one of Melbourne's fastest-growing suburbs, full of newer homes with standard builder bathrooms. Upgrading the vanity, tiling and fixtures is one of the quickest ways to lift a new-build home above the estate default.",
        "hook2": "We manage the whole job, coordinating every trade and building the joinery ourselves, so the room is finished properly and to a higher standard. Free on-site measure, fixed written quote, and one point of contact throughout.",
        "nearby": [("Werribee", "werribee"), ("Hoppers Crossing", "hoppers-crossing"), ("Point Cook", "point-cook")],
    },
]

# FAQ - matches the depth of the hub page. Items 0 and 3 are localised per suburb (0 opens);
# the rest are the standing bathroom answers, kept consistent with bathroom-renovations.html.
def faq_items(s):
    return [
        (f"Do you renovate bathrooms in {s['name']}?",
         f"Yes. Timbr Built is based in Melbourne's inner west and works across {s['area']}, including {s['name']} and the surrounding suburbs. Every job starts with a free on-site measure, then a fixed written quote with no obligation."),
        ("How much does a bathroom renovation cost?",
         "It depends on the size of the room, the fixtures and tiles you choose, and how much has to change behind the walls. Rather than guess, we give you a fixed written quote after a free on-site measure, so the price you see is the price you pay."),
        ("How long does a bathroom renovation take?",
         "Most full bathroom renovations take a few weeks on site once we start, depending on the size of the room, the finishes and how much needs to change behind the walls. You will get a realistic timeline with your quote."),
        (f"Do you renovate older bathrooms in {s['name']} homes?",
         f"Yes, and a lot of our work is exactly that. Older {s['name']} homes often hide surprises once the old bathroom comes out, like tired plumbing, movement or previous waterproofing that has failed. We deal with what we find and put it back properly, so the new bathroom is sound."),
        ("Do you handle the waterproofing and tiling?",
         "Yes. We coordinate the waterproofing and tiling as part of the job, with waterproofing done to the Australian Standard for wet areas. Getting that layer right is what keeps a bathroom sound, so we never cut corners on it."),
        ("Can I stay in the house during the renovation?",
         "Usually yes. If it is your only bathroom we will talk through the timing so you are not left without one for long. We keep the work area contained and the rest of the house clean while the bathroom is out of action."),
    ]


# Shared depth sections - keep a suburb page carrying the same service detail as the hub. Each
# suburb still has its own hero, intro, serving band and two localised FAQ answers, so these
# shared blocks are supporting content, not the whole page.
WHAT_WE_DO = '''  <!-- WHAT WE DO -->
  <section class="section bg-stone">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">What we do</span>
        <h2 class="h-display">A full renovation, managed properly.</h2>
        <p class="lead">From a full main-bathroom rebuild to an ensuite or a smaller refresh, we run the whole job so it lands on one schedule and one standard.</p>
      </div>
      <div class="cards cards--4">
        <div class="card"><div class="card__body">
          <h3>Full renovations</h3>
          <p>Complete bathroom renovations from the strip-out to the final fit-off, with every trade coordinated so nothing falls between the plumber, tiler and electrician.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Waterproofing &amp; tiling</h3>
          <p>Waterproofing done to the Australian Standard and tiling set out carefully, floors and walls, so the wet areas are right before anything goes back in.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Vanities &amp; joinery</h3>
          <p>Custom vanities, mirror cabinets, shaving cabinets and storage built in-house to suit your space, rather than off-the-shelf units squeezed in.</p>
        </div></div>
        <div class="card"><div class="card__body">
          <h3>Ensuites &amp; laundries</h3>
          <p>Ensuites, powder rooms and laundries handled with the same care, whether it is a full renovation or a smaller makeover.</p>
        </div></div>
      </div>
    </div>
  </section>'''

DONE_PROPERLY = '''  <!-- DONE PROPERLY -->
  <section class="section bg-surface">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Done properly</span>
        <h2 class="h-display">The parts you don't see matter most.</h2>
      </div>
      <div class="split">
        <div>
          <p>A bathroom lives or dies on the work you never see once it is finished. Waterproofing to the Australian Standard, proper falls to the drain, solid framing behind the fixtures and the right substrate under the tiles are what keep a bathroom sound for the long run. We get those right before we worry about the finishes.</p>
        </div>
        <div>
          <p>Because one carpenter coordinates the plumber, waterproofer, tiler and electrician, the trades turn up in the right order and nothing gets missed between them. You deal with one person from the first measure to the final fit-off, and you get a fixed written quote up front, so the price you see is the price you pay.</p>
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
        <div class="step"><div class="step__n">01</div><h3>Get in touch</h3><p>Tell us about your bathroom, the look you are after and rough timing.</p></div>
        <div class="step"><div class="step__n">02</div><h3>Free on-site measure</h3><p>We visit, take measurements, talk through layout and finishes, and confirm scope.</p></div>
        <div class="step"><div class="step__n">03</div><h3>Fixed written quote</h3><p>A clear price with no mid-job surprises, and a booked start date.</p></div>
        <div class="step"><div class="step__n">04</div><h3>Built &amp; finished</h3><p>Every trade coordinated through to handover, and the site left clean.</p></div>
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
    links = [f'<a class="area-link" href="bathroom-renovations-{slug}.html">{name}</a>' for name, slug in nearby]
    if len(links) > 1:
        joined = ", ".join(links[:-1]) + " and " + links[-1]
    else:
        joined = links[0]
    return joined


def page_html(s):
    slug = s["slug"]
    url = f"{DOMAIN}/bathroom-renovations-{slug}.html"
    title = f"Bathroom Renovations in {esc(s['name'])} | Timbr Built"
    desc = (f"Full bathroom renovations in {s['name']}, managed start to finish by a local carpenter. "
            f"Waterproofing, tiling and custom joinery coordinated. Free measure and fixed quote.")
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
      "name": "Bathroom Renovations in {s['name']}",
      "serviceType": "Bathroom renovation",
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
        {{ "@type": "ListItem", "position": 3, "name": "Bathroom Renovations", "item": "{DOMAIN}/bathroom-renovations.html" }},
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
  <meta property="og:title" content="Bathroom Renovations in {esc(s['name'])} | Timbr Built">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/Assets/bathroom-featured.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Bathroom Renovations in {esc(s['name'])} | Timbr Built">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{DOMAIN}/Assets/bathroom-featured.jpg">
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
      <img width="1050" height="1400" src="Assets/bathroom-featured.jpg" alt="Renovated bathroom with walk-in shower, brass tapware and freestanding bath" fetchpriority="high" decoding="async">
    </div>
    <div class="container page-hero__inner">
      <span class="eyebrow">Bathroom Renovations &middot; {esc(s['name'])}</span>
      <h1 class="page-hero__title">Bathroom renovations in {esc(s['name'])}.</h1>
      <p class="page-hero__lead">{esc(s['lead'])}</p>
    </div>
  </section>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/services.html">Services</a></li>
        <li><a href="/bathroom-renovations.html">Bathroom Renovations</a></li>
        <li aria-current="page">{esc(s['name'])}</li>
      </ol>
    </div>
  </nav>

  <!-- LOCAL INTRO + WHAT'S INCLUDED -->
  <section class="section bg-surface">
    <div class="container">
      <div class="feature">
        <div class="feature__media"><img width="1050" height="1400" src="Assets/bathroom-timber-vanity.jpg" alt="Bathroom with timber vanity, round vessel basin and tiled bath" loading="lazy" decoding="async"></div>
        <div class="feature__body">
          <span class="eyebrow">Bathroom renovations in {esc(s['name'])}</span>
          <h2>Bathrooms, built for {esc(s['name'])} homes</h2>
          <p>{esc(s['hook1'])}</p>
          <p>{esc(s['hook2'])}</p>
          <ul class="feature__list">
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Full renovations, strip-out to fit-off</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Waterproofing and tiling coordinated</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Custom vanities, mirror units and storage</li>
            <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>Ensuites, powder rooms and laundries</li>
          </ul>
          <a href="contact.html" class="btn btn-primary mt-sm">Get a quote</a>
        </div>
      </div>
    </div>
  </section>

{WHAT_WE_DO}

{DONE_PROPERLY}

{HOW_WE_WORK}

  <!-- FAQ -->
  <section class="section bg-navy faq-section">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow" style="justify-content:center">FAQ</span>
        <h2 class="h-display">Bathroom renovations in {esc(s['name'])}.</h2>
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
        <p class="lead">Timbr Built is based in Melbourne's inner west and works throughout {esc(s['area'])}, part of {esc(s['council'])}. We also renovate bathrooms in nearby {nearby_html}. If your suburb is not listed, get in touch and we will let you know.</p>
      </div>
    </div>
  </section>

  <!-- IMAGE CTA -->
  <section class="cta-feature-section">
    <div class="container">
      <div class="cta-feature">
        <div class="cta-feature__media">
          <img width="1050" height="1400" src="Assets/bathroom-terrazzo.jpg" alt="" loading="lazy" decoding="async">
        </div>
        <div class="cta-feature__body">
          <h2>Planning a bathroom reno in {esc(s['name'])}?</h2>
          <p>Tell us about your space and we will book a free on-site measure in {esc(s['name'])}, then come back with a fixed written quote, no obligation.</p>
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
        path = os.path.join(ROOT, f"bathroom-renovations-{s['slug']}.html")
        with open(path, "w") as fh:
            fh.write(page_html(s))
        written.append(os.path.basename(path))
    print(f"Wrote {len(written)} suburb LPs:")
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
