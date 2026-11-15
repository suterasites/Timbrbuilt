#!/usr/bin/env python3
"""
gen_carpenter_suburbs.py - Carpenter suburb pages on the REDESIGN (2026-11 onward).

Why this exists: build_carpentry_lps.py emits the pre-redesign markup (.section / .cards /
.steps), every class of which was deleted from styles.css on 2026-11-02. Running it now
would overwrite the three live carpenter pages with unstyled HTML. This script instead takes
the live, redesigned carpenter-yarraville.html as the SHELL - head scripts, topbar, menu,
What we do, How it works, standing FAQ, quote form, footer and callbar stay byte-identical -
and swaps only the localised strings for each new suburb.

Every swap asserts how many times the Yarraville string occurs in the shell, so a later edit
to the shell that moves or rewords a block fails loudly here instead of leaving Yarraville
copy on a Kingsville page. No Yarraville line from the shell may survive on a new page (the
service-area map alt is the one shared exception).

Site hard rules carried in the copy: no claimed project in any suburb, "qualified carpenter"
only (no licensed / registered / insured), no em dashes, no prices.

Run:  python3 .build/gen_carpenter_suburbs.py          (writes into the site root)
Re-runnable: rewrites only the pages listed in NEW; the shell is never modified.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SHELL = "carpenter-yarraville.html"

# The shell's own localised strings, exactly as they sit in carpenter-yarraville.html.
# (field, text, expected occurrences in the shell)
SRC = {
    "name": "Yarraville",
    "slug": "yarraville",
    "title": ("Carpenter in Yarraville | Timbr Built", 3),
    "desc": ("Carpenter in Yarraville for extension framing, floor and weatherboard repairs, doors, skirting and built-in storage. Free on-site measure, fixed written quote.", 3),
    "og_image": ("https://timbrbuilt.com.au/Assets/laundry-walnut-joinery.jpg", 2),
    "hero": ('<div class="phero__cell"><img width="1050" height="1400" src="Assets/laundry-walnut-joinery.jpg" alt="Laundry with walnut timber joinery, terrazzo splashback, stone benchtop and undermount sink" fetchpriority="high" decoding="async"></div>', 1),
    "cell2": ('<div class="phero__cell"><img width="1050" height="1400" src="Assets/framing-arched-window.jpg" alt="Timber roof framing with an arched window opening framed out" loading="lazy" decoding="async"></div>', 1),
    "lead": ("Framing, finish carpentry and built-in storage for Yarraville's cottages, where every room has to work hard and very little is square.", 1),
    "h2": ("Carpentry for Yarraville cottages", 1),
    "feature": ('<div class="detail__media"><img width="619" height="1100" src="Assets/build-cladding.jpg" alt="New build framed and clad by Timbr Built" loading="lazy" decoding="async"></div>', 1),
    "jobs_h2": ("What Yarraville homes need.", 1),
    "cta_img": ('<img width="1400" height="750" src="Assets/pergola-framing.jpg" alt="" loading="lazy" decoding="async">', 1),
    "cta": ("Send through what you have in mind and we will book a time to look at it, measure up and come back with a written price.", 1),
}

# Multi-part blocks, located by regex in the shell and rebuilt whole.
P_BLOCK = re.compile(r'(<div class="detail__body">\n)(.*?)(        <ul class="detail__list">\n)(.*?)(        </ul>)', re.S)
JOBS_BLOCK = re.compile(r'(<ul class="svc__grid svc__grid--3">\n)(.*?)(    </ul>)', re.S)
FAQ_HTML = re.compile(r'(<div class="faqs__list">\n)(        <details class="faqs__item" open>.*?</details>\n        <details class="faqs__item">.*?</details>\n)', re.S)
FAQ_JSON = re.compile(r'("mainEntity": \[\n)(        \{\n          "@type": "Question",.*?\n        \},\n        \{\n          "@type": "Question",.*?\n        \},\n)', re.S)
NEARBY = re.compile(r'(<p class="band__label">Serving Yarraville</p>\n    <div class="band__head">\n      <h2 class="band__title">Local, and close by.</h2>\n      <p class="band__lead">)(.*?)(</p>)', re.S)

NEW = [
    {
        "name": "Kingsville", "slug": "kingsville",
        "title": "Carpenter in Kingsville | Timbr Built",
        "desc": "Carpenter in Kingsville for bungalow verandahs, framing for alterations, matched skirting and architraves, doors and repairs. Free on-site measure, fixed written quote.",
        "hero": ("framing-curved-stair.jpg", 1170, 1560, "Timber stud framing and bent plywood forming a curved wall around a spiral staircase"),
        "cell2": ("laundry-walnut-joinery.jpg", 1050, 1400, "Laundry with walnut timber joinery and a stone benchtop"),
        "feature": ("facade-brick-cladding.jpg", 787, 1400, "New build facade in face brick with white cladding above"),
        "cta_img": ("pergola-framing.jpg", 1400, 750),
        "lead": "Verandahs, framing and trims for Kingsville's interwar homes, from a qualified carpenter working right across the inner west.",
        "h2": "Carpentry for Kingsville bungalows",
        "p1": "Kingsville is a small, settled pocket of the City of Maribyrnong, tucked in beside Yarraville, West Footscray and South Kingsville. Much of its housing went up between the wars: timber bungalows with a deep front porch, weatherboards on stumps, and solid rooms laid out one after another from the front door to the kitchen at the back.",
        "p2": "Those homes ask for a particular kind of carpentry. The front porch carries most of the character and most of the weather. Skirting, architraves and picture rails were run in wider profiles than anything sold as standard today. And when a family outgrows the layout, the change usually happens at the back, where a wall comes out and the house finally opens to the yard.",
        "list": ["Verandah posts, beams and boards", "Framing for alterations and extensions",
                 "Skirting, architraves and picture rails matched", "Doors hung, trimmed and refitted",
                 "Deck and pergola framing"],
        "jobs_h2": "What Kingsville homes need.",
        "jobs": [
            ("Bungalow porches",
             "On an interwar bungalow the porch is the face of the house. Timber posts rot where they meet the floor, beams take water at the ends and the boards cup. We replace the timber that has gone, keep what is sound, and match the post and beam detail so the porch still looks like it belongs to the house."),
            ("Opening up the back",
             "Bungalows were built as a run of separate rooms, with the kitchen and laundry at the rear. Joining them up to the yard means finding out what the wall is carrying, sizing a beam for the opening and framing it for new doors. Done properly, the new space reads as part of the house rather than a box on the back."),
            ("Trims that match",
             "Patch a wall or move a doorway in an interwar home and the new skirting has to meet the old. Many of the original profiles are no longer stock, so we take a sample at the measure and work out how it will be matched before the price is fixed, rather than settling for the nearest thing on the shelf."),
        ],
        "faq": [
            ("Do you work in Kingsville?",
             "Yes. Kingsville sits between Yarraville and Spotswood, a few minutes from most of the work we do in the inner west, so a quote visit is a short trip. Every job starts with a free on-site measure and a fixed written quote, with no obligation."),
            ("Can you match the old skirting and architraves?",
             "Usually. Some interwar profiles can still be bought, and the rest can be machined from a sample of the original. We take an offcut or a profile at the measure, tell you which way it will go, and include it in the written quote so there is no surprise once the old timber is off the wall."),
        ],
        "nearby": 'Kingsville sits between Yarraville, West Footscray and South Kingsville in the City of Maribyrnong. We are also the carpenter to call in <a href="carpenter-yarraville.html">Yarraville</a> and <a href="carpenter-footscray.html">Footscray</a>, and every suburb we cover is on the main <a href="carpentry.html">carpentry</a> page.',
        "decks": "decks-pergolas.html",
        "cta": "Tell us about the house and what needs doing. We will come out, measure up for free and send a fixed written quote before anything is booked.",
    },
    {
        "name": "Footscray", "slug": "footscray",
        "title": "Carpenter in Footscray | Timbr Built",
        "desc": "Carpenter in Footscray for cottage weatherboard and floor repairs, framing for alterations, doors, skirting and repairs between tenancies. Free on-site measure, fixed written quote.",
        "hero": ("facade-brick-cladding.jpg", 787, 1400, "New build facade in face brick with white cladding above"),
        "cell2": ("framing-curved-stair.jpg", 1170, 1560, "Timber stud framing forming a curved wall around a spiral staircase"),
        "feature": ("build-2.jpg", 562, 1000, "Structural carpentry and framing on a new build"),
        "cta_img": ("cta-deck.jpg", 1242, 800),
        "lead": "Repairs, alterations and finish carpentry for Footscray homes, from century-old cottages near the station to the rentals that need a carpenter between tenants.",
        "h2": "Carpentry for Footscray homes",
        "p1": "Footscray is the busy centre of the inner west, and its housing reflects a long history. Close to the station and the river the streets are lined with single-fronted Victorian and Edwardian cottages, many in weatherboard, some in brick, most of them more than a hundred years old. Around them, newer townhouses and apartments fill the blocks where old houses and yards once stood.",
        "p2": "So the carpentry here covers a wide range. In the old cottages it is weatherboards, floors and doors that have moved with a century of seasons, and framing when the back of the house is rebuilt. A good share of Footscray homes are rented, which brings the other half of the work: the repairs that come up between tenants and need doing properly rather than patched for the next inspection.",
        "list": ["Weatherboard and floor repairs", "Framing for alterations and extensions",
                 "Doors, skirting and architraves", "Repairs between tenancies",
                 "Built-in storage and joinery"],
        "jobs_h2": "What Footscray homes need.",
        "jobs": [
            ("Workers' cottages",
             "A cottage this old has rarely stayed square. Doors bind, boards split where the downpipe meets the wall and the floor runs downhill towards the back. We find out what is actually moving before quoting, and if the problem is underneath the house rather than in the timber, we will tell you so before anything new goes on."),
            ("Between tenancies",
             "When a rental changes hands the list is usually carpentry: a door that no longer latches, a damaged architrave, a soft patch in the floor, a back step that has gone. We quote the list as one job for the owner, and work out access with you or your property manager."),
            ("Rebuilding the back",
             "Plenty of Footscray cottages still have a lean-to or an old addition at the rear that has reached the end of its life. Replacing it means framing a new room and tying it into the original house, working with your designer or engineer where the job has one, and finishing the trims so old and new line up."),
        ],
        "faq": [
            ("Do you work in Footscray?",
             "Yes. Footscray is the middle of the inner west for us, with Seddon, Yarraville and West Footscray all a few minutes away. You get a free on-site measure and a fixed written quote before any work is booked."),
            ("Can you do repairs while the property is tenanted?",
             "Usually, yes. Most carpentry repairs can be done with tenants in place once access is arranged. Tell us whether you or a property manager is organising access, and the quote comes to you as the owner, itemised so you can see what each repair costs."),
        ],
        "nearby": 'Footscray sits at the heart of the City of Maribyrnong, between Seddon, West Footscray and Maribyrnong. We are also the carpenter to call in <a href="carpenter-yarraville.html">Yarraville</a> and <a href="carpenter-kingsville.html">Kingsville</a>, and every suburb we cover is on the main <a href="carpentry.html">carpentry</a> page.',
        "decks": "decks-pergolas-footscray.html",
        "cta": "Send us the job, or the whole list if it is a rental, and we will book a free measure in Footscray and come back with a fixed written price.",
    },
    {
        "name": "Altona", "slug": "altona",
        "title": "Carpenter in Altona | Timbr Built",
        "desc": "Carpenter in Altona for framing in post-war brick veneer and weatherboard homes, rear additions, doors, skirting, decks and pergolas. Free on-site measure, fixed written quote.",
        "hero": ("deck-weatherboard.jpg", 1050, 1400, "Oiled hardwood deck beside a weatherboard home"),
        "cell2": ("framing-arched-window.jpg", 1050, 1400, "Timber roof framing with an arched window opening framed out"),
        "feature": ("build-cladding.jpg", 619, 1100, "New build framed and clad by Timbr Built"),
        "cta_img": ("pergola-framing.jpg", 1400, 750),
        "lead": "Framing, alterations and outdoor carpentry for Altona's post-war homes, from a qualified carpenter working right around Hobsons Bay.",
        "h2": "Carpentry for Altona homes",
        "p1": "Much of Altona grew up after the war. Street after street is lined with brick veneer and weatherboard homes from the 1950s and 60s, single storey on generous blocks, with the bay and the Pier Street shops never far away. Many are still close to how they were built, and as they change hands they are being reworked inside or replaced with townhouses.",
        "p2": "The carpentry follows that. Inside a post-war home it is walls moving, doorways widening and rooms joined up to suit how people live now. Out the back it is usually a tired sunroom or lean-to that needs to become a proper room, and the deck or pergola that goes with it, built to stand up to the wind and salt air off the bay.",
        "list": ["Framing for internal alterations", "Rear additions and sunroom replacements",
                 "Doors, skirting and architraves", "Deck and pergola framing",
                 "Repairs and weatherboard replacement"],
        "jobs_h2": "What Altona homes need.",
        "jobs": [
            ("Behind the brick veneer",
             "A brick veneer home has a timber frame behind its brick skin, so changing the inside is carpentry. Moving a doorway, taking out a hallway wall or opening the kitchen to the living room starts with what the frame is carrying, and the trims are run through afterwards so the change does not show."),
            ("Replacing the sunroom",
             "A lot of Altona homes picked up a sunroom or enclosed back porch somewhere along the way, often lightly framed and cold in winter. Rebuilding it as a properly framed room, tied into the house and lined to match, turns a space the family avoids into one they use."),
            ("Outdoor timber by the bay",
             "Decks, pergolas and outdoor timber this close to the water take more weather than most. We frame them to suit the exposure, fix with hardware that will not stain the timber, and leave you a structure that does not need rebuilding in a few summers."),
        ],
        "faq": [
            ("Do you work in Altona?",
             "Yes. Altona is part of our regular patch around Hobsons Bay, along with Seaholme, Altona North and Williamstown. Every job starts with a free on-site measure and a fixed written quote, with no obligation."),
            ("Is a brick veneer house harder to alter?",
             "Not usually. Behind the brick is a timber frame, much like a weatherboard house, so internal changes are carpentry. What decides the job is whether a wall carries the roof. We check that at the measure, and anything structural is quoted with its beam and, where it is needed, a building permit."),
        ],
        "nearby": 'Altona sits on the bay in Hobsons Bay, with Seaholme, Altona North and Altona Meadows around it. We are also the carpenter to call in <a href="carpenter-williamstown.html">Williamstown</a> and <a href="carpenter-newport.html">Newport</a>, and every suburb we cover is on the main <a href="carpentry.html">carpentry</a> page.',
        "decks": "decks-pergolas-altona.html",
        "cta": "Tell us what you have in mind for the house. We will come out to Altona for a free measure and send a fixed written quote, with no obligation.",
    },
]


def esc(t):
    return t.replace("&", "&amp;")


def json_text(t):
    return t.replace("\\", "\\\\").replace('"', '\\"')


def swap(html, old, new, expected, label):
    n = html.count(old)
    if n != expected:
        sys.exit(f"shell drift: '{label}' occurs {n}x in {SHELL}, expected {expected}")
    return html.replace(old, new)


def sub_once(rx, html, fn, label):
    out, n = rx.subn(fn, html, count=1)
    if n != 1:
        sys.exit(f"shell drift: block '{label}' not found in {SHELL}")
    return out


def render(shell, s):
    """Return the shell with every localised string swapped for suburb `s`."""
    name, slug = s["name"], s["slug"]
    h = shell
    h = swap(h, SRC["title"][0], s["title"], SRC["title"][1], "title")
    h = swap(h, SRC["desc"][0], s["desc"], SRC["desc"][1], "desc")
    h = swap(h, SRC["og_image"][0], f"https://timbrbuilt.com.au/Assets/{s['hero'][0]}", SRC["og_image"][1], "og_image")
    src, w, hh, alt = s["hero"]
    h = swap(h, SRC["hero"][0], f'<div class="phero__cell"><img width="{w}" height="{hh}" src="Assets/{src}" alt="{alt}" fetchpriority="high" decoding="async"></div>', 1, "hero")
    src, w, hh, alt = s["cell2"]
    h = swap(h, SRC["cell2"][0], f'<div class="phero__cell"><img width="{w}" height="{hh}" src="Assets/{src}" alt="{alt}" loading="lazy" decoding="async"></div>', 1, "cell2")
    h = swap(h, SRC["lead"][0], esc(s["lead"]), 1, "lead")
    h = swap(h, SRC["h2"][0], esc(s["h2"]), 1, "h2")
    src, w, hh, alt = s["feature"]
    h = swap(h, SRC["feature"][0], f'<div class="detail__media"><img width="{w}" height="{hh}" src="Assets/{src}" alt="{alt}" loading="lazy" decoding="async"></div>', 1, "feature")
    h = swap(h, SRC["jobs_h2"][0], esc(s["jobs_h2"]), 1, "jobs_h2")
    src, w, hh = s["cta_img"]
    h = swap(h, SRC["cta_img"][0], f'<img width="{w}" height="{hh}" src="Assets/{src}" alt="" loading="lazy" decoding="async">', 1, "cta_img")
    h = swap(h, SRC["cta"][0], esc(s["cta"]), 1, "cta")

    paras = "".join(f"        <p>{esc(p)}</p>\n" for p in (s["p1"], s["p2"]))
    items = "".join(f"          <li>{esc(i)}</li>\n" for i in s["list"])
    h = sub_once(P_BLOCK, h, lambda m: m.group(1) + paras + m.group(3) + items + m.group(5), "detail body")

    cards = "".join(
        f'      <li class="svc__card"><h3 class="svc__name">{esc(t)}</h3><p class="svc__text">{esc(p)}</p></li>\n'
        for t, p in s["jobs"])
    h = sub_once(JOBS_BLOCK, h, lambda m: m.group(1) + cards + m.group(3), "local work cards")

    (q1, a1), (q2, a2) = s["faq"]
    faq_html = (
        f'        <details class="faqs__item" open>\n'
        f'          <summary>{esc(q1)}<span class="faqs__icon" aria-hidden="true"></span></summary>\n'
        f'          <div class="faqs__a"><p>{esc(a1)}</p></div>\n'
        f'        </details>\n'
        f'        <details class="faqs__item">\n'
        f'          <summary>{esc(q2)}<span class="faqs__icon" aria-hidden="true"></span></summary>\n'
        f'          <div class="faqs__a"><p>{esc(a2)}</p></div>\n'
        f'        </details>\n')
    h = sub_once(FAQ_HTML, h, lambda m: m.group(1) + faq_html, "faq html")

    def q_json(q, a):
        return ('        {\n'
                '          "@type": "Question",\n'
                f'          "name": "{json_text(q)}",\n'
                '          "acceptedAnswer": {\n'
                '            "@type": "Answer",\n'
                f'            "text": "{json_text(a)}"\n'
                '          }\n'
                '        },\n')
    h = sub_once(FAQ_JSON, h, lambda m: m.group(1) + q_json(q1, a1) + q_json(q2, a2), "faq schema")

    h = sub_once(NEARBY, h, lambda m: m.group(1) + s["nearby"] + m.group(3), "nearby band")

    # Remaining single-word / slug swaps, each pinned to its exact context.
    h = swap(h, "https://timbrbuilt.com.au/carpenter-yarraville", f"https://timbrbuilt.com.au/carpenter-{slug}", 3, "page url")
    h = swap(h, '"name": "Yarraville"', f'"name": "{name}"', 3, "areaServed x2 + breadcrumb name")
    h = swap(h, '"name": "Carpenter in Yarraville"', f'"name": "Carpenter in {name}"', 1, "service name")
    h = swap(h, '<li aria-current="page">Yarraville</li>', f'<li aria-current="page">{name}</li>', 1, "breadcrumb")
    h = swap(h, '<h1 class="phero__title">Carpenter in Yarraville.</h1>', f'<h1 class="phero__title">Carpenter in {name}.</h1>', 1, "h1")
    h = swap(h, '<p class="detail__label">Carpenter in Yarraville</p>', f'<p class="detail__label">Carpenter in {name}</p>', 1, "detail label")
    h = swap(h, '<h2 class="faqs__title">Carpentry in Yarraville.</h2>', f'<h2 class="faqs__title">Carpentry in {name}.</h2>', 1, "faq title")
    h = swap(h, 'href="decks-pergolas-yarraville.html">their own page</a>', f'href="{s["decks"]}">their own page</a>', 1, "decks link")
    h = swap(h, '<input type="hidden" name="_source" value="carpenter-yarraville">', f'<input type="hidden" name="_source" value="carpenter-{slug}">', 1, "form source")
    h = swap(h, '<p class="band__label">Serving Yarraville</p>', f'<p class="band__label">Serving {name}</p>', 1, "serving label")
    h = swap(h, '<h2 class="cta-tile__title">Need a carpenter in Yarraville?</h2>', f'<h2 class="cta-tile__title">Need a carpenter in {name}?</h2>', 1, "cta title")

    # No line of the shell's Yarraville copy may survive. New copy can name Yarraville as a
    # neighbour, so the test is "a Yarraville line identical to one in the shell", with the
    # service-area map alt (site chrome on every carpenter page) the only exemption.
    shell_lines = {ln.strip() for ln in shell.splitlines() if "Yarraville" in ln}
    leftovers = [ln.strip() for ln in h.splitlines()
                 if "Yarraville" in ln and ln.strip() in shell_lines and "service-area.svg" not in ln]
    if leftovers:
        sys.exit(f"{slug}: Yarraville copy left on the page:\n  " + "\n  ".join(leftovers))
    return h


def main():
    shell = open(os.path.join(ROOT, SHELL), encoding="utf-8").read()
    for s in NEW:
        out = render(shell, s)
        path = os.path.join(ROOT, f"carpenter-{s['slug']}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote carpenter-{s['slug']}.html")


if __name__ == "__main__":
    main()
