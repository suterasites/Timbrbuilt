"""Build Assets/service-area.svg: a static map of the inner-west suburbs Timbr Built works in.

Reads the Victorian suburb outlines the agency already caches from OpenStreetMap
(~/Sutera-Sites/CRM/operations/geo/vic-all-suburbs.json) so the home page needs no
map embed or third-party script. Water is just the background showing through
wherever no suburb is drawn, which is how the bay and the river appear.

Run from the site root:  python3 .build/build_service_area_map.py
"""
import json
import math
import os

SRC = os.path.expanduser('~/Sutera-Sites/CRM/operations/geo/vic-all-suburbs.json')
OUT = 'Assets/service-area.svg'

SERVED = {
    'Williamstown', 'Williamstown North', 'Newport', 'Spotswood', 'Yarraville', 'Seddon',
    'Footscray', 'West Footscray', 'Kingsville', 'South Kingsville', 'Altona', 'Altona North',
    'Seaholme', 'Maribyrnong',
}
LABELS = {  # name -> (dx, dy) nudge in px from the ring centroid, to stop small suburbs colliding
    'Williamstown': (0, 6), 'Newport': (0, 0), 'Spotswood': (10, 0), 'Yarraville': (6, 4),
    'Seddon': (-4, 2), 'Footscray': (10, -4), 'West Footscray': (-6, 0), 'Altona': (0, -16),
    'Altona North': (0, 0), 'Maribyrnong': (0, 4),
}
W, H = 700, 900
PAD = 0.012  # degrees of margin around the served area

WATER, LAND, LAND_EDGE = '#DCE2E1', '#F3F1EB', '#E2DED4'
SERVED_FILL, SERVED_EDGE, INK = '#E9DFCB', '#C9B993', '#5A4A33'


def rings_of(sub):
    return [[tuple(map(float, pt.split(','))) for pt in r.split()] for r in sub['r']]


data = json.load(open(SRC))['suburbs']
subs = {s['n']: rings_of(s) for s in data}
missing = SERVED - subs.keys()
assert not missing, f'no outline cached for {missing}'

pts = [p for n in SERVED for ring in subs[n] for p in ring]
lon0, lon1 = min(p[0] for p in pts) - PAD, max(p[0] for p in pts) + PAD
lat0, lat1 = min(p[1] for p in pts) - PAD, max(p[1] for p in pts) + PAD
kx = math.cos(math.radians((lat0 + lat1) / 2))
# grow the box to the canvas aspect, centred, so nothing is stretched
span_x, span_y = (lon1 - lon0) * kx, lat1 - lat0
if span_x / span_y < W / H:
    grow = (span_y * W / H - span_x) / kx / 2
    lon0, lon1 = lon0 - grow, lon1 + grow
else:
    grow = (span_x * H / W - span_y) / 2
    lat0, lat1 = lat0 - grow, lat1 + grow
scale = W / ((lon1 - lon0) * kx)


def xy(p):
    return (p[0] - lon0) * kx * scale, (lat1 - p[1]) * scale


def in_view(rings):
    return any(lon0 - .05 < x < lon1 + .05 and lat0 - .05 < y < lat1 + .05 for r in rings for x, y in r)


def path(rings):
    return ' '.join('M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in map(xy, r)) + ' Z' for r in rings)


def centroid(rings):
    ring = max(rings, key=len)
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(map(xy, ring), map(xy, ring[1:] + ring[:1])):
        f = x1 * y2 - x2 * y1
        a += f
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    return cx / (3 * a), cy / (3 * a)


out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-label="Map of the Melbourne inner-west suburbs Timbr Built works in">',
       f'<rect width="{W}" height="{H}" fill="{WATER}"/>',
       f'<g fill="{LAND}" stroke="{LAND_EDGE}" stroke-width="1" stroke-linejoin="round">']
out += [f'<path d="{path(r)}"/>' for n, r in subs.items() if n not in SERVED and in_view(r)]
out += ['</g>', f'<g fill="{SERVED_FILL}" stroke="{SERVED_EDGE}" stroke-width="1.2" stroke-linejoin="round">']
out += [f'<path d="{path(subs[n])}"/>' for n in sorted(SERVED)]
out += ['</g>', f'<g fill="{INK}" font-family="Helvetica, Arial, sans-serif" font-size="15" text-anchor="middle">']
for n, (dx, dy) in LABELS.items():
    x, y = centroid(subs[n])
    out.append(f'<text x="{x + dx:.0f}" y="{y + dy:.0f}">{n}</text>')
out += ['</g>', '</svg>']

open(OUT, 'w').write('\n'.join(out) + '\n')
print(f'wrote {OUT} ({os.path.getsize(OUT) // 1024} KB), lon {lon0:.3f}..{lon1:.3f}, lat {lat0:.3f}..{lat1:.3f}')
