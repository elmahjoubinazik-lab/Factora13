exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Base reprise de l'épisode 044 (outils, textes, aliments, estomac) pour la révision 044c. Ancien en-tête :
# Épisode 044 (Short seul, 9:16, ~25 s) — « Why Doesn't Your Stomach Digest Itself? » (mystère du corps humain, pas Animal
# Mystery). Brief de Nazik (2026-11-21) : même charte et même clarté que le wombat (ép. 043) ; une question, une explication
# visuelle, pas de quiz ; voix exacte imposée, débit naturel ; sous-titres mot pour mot ; bas et bord droit libres ;
# « Simplified illustration » sur les schémas ; CTA texte « Follow Factora for more body mysteries. » sur les ~2,5 dernières s.
# Faits : la muqueuse gastrique (cellules de surface) sécrète un mucus en gel qui recouvre la paroi et la protège de l'acide
# et des enzymes du suc gastrique (Cleveland Clinic : Stomach, Mucosa ; Britannica : gastric mucosa). Explication volontairement
# simplifiée : pas de liste complète des défenses, pas de lésion, pas de cause d'ulcère, pas de conseil médical.
# Dessins 100 % faits ici (schémas, pas d'images médicales réelles).
import json as _json

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
END_T = _TLL[-1]["end"] + 0.6                       # fin de la vidéo (render.py ajoute 0,6 s)
def WT(word, n=0):
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9

DARK = (0.03, 0.02, 0.08)
MUC = (0.66, 0.90, 1.0)          # mucus (sécrétion, gel translucide)
MUC_L = (0.50, 0.85, 1.0)
TIS = (0.97, 0.56, 0.62)         # tissu vivant (paroi)
TIS_D = (0.70, 0.24, 0.34)
JUICE = (1.0, 0.72, 0.26)        # suc gastrique
FOODS = [(1.0, 0.56, 0.16), (0.40, 0.78, 0.32), (0.93, 0.80, 0.55), (0.92, 0.28, 0.24), (0.70, 0.42, 0.78), (1.0, 0.82, 0.30)]

def lerp(a, b, k): return a + (b - a) * k
def L2(p, q, k): return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))

# ---------------------------------------------------------------- outils
def catmull_closed(pts, per=16):
    n = len(pts); out = []
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for k in range(per):
            u = k / per; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    return out

def catmull_open(pts, per=16):
    q = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(per):
            u = k / per; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    out.append(pts[-1]); return out

def poly_path(ctx, pts, close=True):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if close: ctx.close_path()

def rpoly(ctx, pts, r):
    n = len(pts); ctx.new_path()
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        d1 = math.hypot(p0[0] - p1[0], p0[1] - p1[1]) + 1e-9; d2 = math.hypot(p2[0] - p1[0], p2[1] - p1[1]) + 1e-9
        rr = min(r, d1 * 0.45, d2 * 0.45)
        a = (p1[0] + (p0[0] - p1[0]) * rr / d1, p1[1] + (p0[1] - p1[1]) * rr / d1)
        b = (p1[0] + (p2[0] - p1[0]) * rr / d2, p1[1] + (p2[1] - p1[1]) * rr / d2)
        if i == 0: ctx.move_to(*a)
        else: ctx.line_to(*a)
        ctx.curve_to(a[0] + (p1[0] - a[0]) * 0.66, a[1] + (p1[1] - a[1]) * 0.66, b[0] + (p1[0] - b[0]) * 0.66, b[1] + (p1[1] - b[1]) * 0.66, b[0], b[1])
    ctx.close_path()

def hull(pts):
    pts = sorted(set(pts))
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def cut(poly, nx, ny, c, keep_pos=True):
    """Coupe un polygone convexe par la droite nx*x + ny*y = c (garde le côté > c si keep_pos)."""
    out = []; n = len(poly)
    def side(p): v = nx * p[0] + ny * p[1] - c; return v if keep_pos else -v
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]; sa, sb = side(a), side(b)
        if sa >= 0: out.append(a)
        if (sa >= 0) != (sb >= 0):
            k = sa / (sa - sb); out.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
    return out

# ---------------------------------------------------------------- textes (charte Factora : peu de mots)
def tag(ctx, s, a=1.0):
    if a <= 0: return
    font(ctx, 38 * U); w_ = ctx.text_extents(s).width + 48 * U
    x0, y0 = W * 0.055, H * 0.083
    rrect(ctx, x0, y0 - 30 * U, w_, 60 * U, 30 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, x0 + 24 * U, y0, 38 * U, (0.94, 0.96, 1.0), 0.95 * a, align="l")

def label2(ctx, main, sub, x, y, col, k=1.0, a=1.0):
    """Légende sur le schéma : mot principal + précision courte (« made by the lining » / « living tissue »)."""
    if k <= 0 or a <= 0: return
    sc_ = 0.7 + 0.3 * ease(k) + 0.06 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, 46 * U); w1 = ctx.text_extents(main).width; font(ctx, 29 * U); w2 = ctx.text_extents(sub).width
    w_ = max(w1, w2) + 56 * U; h_ = 108 * U
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 24 * U); rgba(ctx, (0.02, 0.03, 0.09), 0.88 * a * ease(k)); ctx.fill()
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 24 * U); ctx.set_line_width(5 * U); rgba(ctx, col, a * ease(k)); ctx.stroke()
    text(ctx, main, 0, -17 * U, 46 * U, col, a * ease(k))
    text(ctx, sub, 0, 29 * U, 29 * U, (0.92, 0.94, 1.0), 0.9 * a * ease(k), bold=False)
    ctx.restore()

def cta_lines(ctx, lines, x, ys, size, a):
    sz = size * U; maxw = W * 0.74
    cap_font(ctx, sz)
    widest = max(ctx.text_extents(l).width for l in lines)
    if widest > maxw: sz *= maxw / widest; cap_font(ctx, sz)
    for l, y, col in zip(lines, ys, (WHITE, GOLD)):
        e = ctx.text_extents(l); x0 = x - e.width / 2 - e.x_bearing; y0 = y + sz * 0.35
        ctx.move_to(x0 + 3 * U, y0 + 5 * U); ctx.text_path(l); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
        ctx.move_to(x0, y0); ctx.text_path(l); ctx.set_line_width(sz * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, (0.01, 0.02, 0.06), a); ctx.stroke_preserve(); rgba(ctx, col, a); ctx.fill()

def bg(ctx, T):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.07, 0.05, 0.17); g.add_color_stop_rgb(1, 0.01, 0.02, 0.07)
    ctx.set_source(g); ctx.paint()
    glow(ctx, W * 0.46, H * 0.43, 0.70 * H, (0.55, 0.20, 0.45), 0.20)
    rnd = random.Random(8)
    for i in range(18):
        x = rnd.random() * W; y = (rnd.random() * H - T * rnd.uniform(8, 25) * U) % H
        circle(ctx, x, y, rnd.uniform(2, 5) * U, rnd.choice([CYAN, PINK, GOLD]), 0.16 + 0.08 * math.sin(T * 2 + i))

# ---------------------------------------------------------------- aliments (polygones convexes qui se fragmentent peu à peu)
def _make_food():
    rnd = random.Random(21); out = []
    for i in range(9):
        r = rnd.uniform(0.75, 1.15); n = 9
        pts = [(math.cos(2 * math.pi * k / n + rnd.uniform(-0.25, 0.25)) * r * rnd.uniform(0.80, 1.0),
                math.sin(2 * math.pi * k / n + rnd.uniform(-0.25, 0.25)) * r * rnd.uniform(0.62, 0.85)) for k in range(n)]
        base = hull(pts)
        a1 = rnd.uniform(0, math.pi); n1 = (math.cos(a1), math.sin(a1))
        A, B = cut(base, n1[0], n1[1], 0.0, True), cut(base, n1[0], n1[1], 0.0, False)
        kids = []
        for half, sgn in ((A, 1), (B, -1)):
            a2 = a1 + math.pi / 2 + rnd.uniform(-0.4, 0.4); n2 = (math.cos(a2), math.sin(a2))
            cx_ = sum(p[0] for p in half) / len(half); cy_ = sum(p[1] for p in half) / len(half); c2 = n2[0] * cx_ + n2[1] * cy_
            kids.append((half, (n1[0] * sgn, n1[1] * sgn), [(cut(half, n2[0], n2[1], c2, True), n2), (cut(half, n2[0], n2[1], c2, False), (-n2[0], -n2[1]))]))
        out.append(dict(base=base, kids=kids, col=FOODS[i % len(FOODS)], rot=rnd.uniform(0, 6.28), spin=rnd.uniform(-0.25, 0.25),
                        orb=(rnd.uniform(0.15, 1.0), rnd.uniform(0.2, 1.0), rnd.uniform(0, 6.28)), size=rnd.uniform(0.85, 1.15),
                        s1=rnd.uniform(0.0, 0.45), s2=rnd.uniform(0.75, 1.35)))
    return out
FOOD = _make_food()

def _draw_piece(ctx, poly, x, y, sc, rot, col, a=1.0):
    pts = [(x + (p[0] * math.cos(rot) - p[1] * math.sin(rot)) * sc, y + (p[0] * math.sin(rot) + p[1] * math.cos(rot)) * sc) for p in poly]
    if len(pts) < 3: return
    rpoly(ctx, pts, sc * 0.22)
    g = cairo.LinearGradient(x - sc, y - sc, x + sc, y + sc)
    g.add_color_stop_rgba(0, *[min(1, c * 1.18) for c in col], a); g.add_color_stop_rgba(1, *[c * 0.72 for c in col], a)
    ctx.set_source(g); ctx.fill_preserve()
    ctx.set_line_width(max(1.5, sc * 0.05)); rgba(ctx, mix(col, (0.1, 0.05, 0.05), 0.55), 0.85 * a); ctx.stroke()
    cx_ = sum(p[0] for p in pts) / len(pts); cy_ = sum(p[1] for p in pts) / len(pts)
    circle(ctx, cx_ - sc * 0.22, cy_ - sc * 0.22, sc * 0.14, WHITE, 0.30 * a)

def food_pieces(ctx, T, cx, cy, rx, ry, scale, theta, brk1, brk2, a=1.0):
    """brk1, brk2 : avancement des 2 étapes de fragmentation (0..1) ; theta : angle de brassage."""
    for f in FOOD:
        ox, oy, ph = f["orb"]
        x = cx + math.cos(ph + theta) * rx * ox; y = cy + math.sin(ph + theta) * ry * oy
        sc = scale * f["size"] * (1 - 0.10 * brk1 - 0.08 * brk2); rot = f["rot"] + f["spin"] * T + 0.3 * theta
        k1 = clamp((brk1 - f["s1"]) / 0.45); k2 = clamp((brk2 - f["s1"] * 0.5) / 0.6) if k1 >= 1 else 0.0
        if k1 <= 0:
            _draw_piece(ctx, f["base"], x, y, sc, rot, f["col"], a); continue
        for half, nrm, quarters in f["kids"]:
            d1 = ease(k1) * 0.32 * sc
            rx_, ry_ = nrm[0] * math.cos(rot) - nrm[1] * math.sin(rot), nrm[0] * math.sin(rot) + nrm[1] * math.cos(rot)
            hx, hy = x + rx_ * d1, y + ry_ * d1
            if k2 <= 0:
                _draw_piece(ctx, half, hx, hy, sc, rot + 0.15 * ease(k1) * (1 if nrm[0] > 0 else -1), f["col"], a); continue
            for q, n2 in quarters:
                d2 = ease(k2) * 0.26 * sc
                qx, qy = n2[0] * math.cos(rot) - n2[1] * math.sin(rot), n2[0] * math.sin(rot) + n2[1] * math.cos(rot)
                _draw_piece(ctx, q, hx + qx * d2, hy + qy * d2, sc * (1 - 0.06 * k2), rot + 0.2 * k2, f["col"], a)

# brassage : angle intégré (lent, puis plus rapide à « mixed », puis plus calme)

def theta(T): return 0.10 * T                       # dérive lente des aliments (pas de brassage dans cette version)

# ---------------------------------------------------------------- estomac (vue d'ensemble, schéma)
ORG_C = (W * 0.45, H * 0.468); ORG_S = 1.30
_OUT = [(-10, -330), (40, -388), (130, -410), (212, -372), (262, -292), (292, -180), (302, -60), (290, 60), (252, 170), (182, 250), (82, 302),
        (-40, 312), (-160, 292), (-268, 240), (-350, 186), (-405, 128), (-428, 88), (-424, 42), (-352, 62), (-270, 100), (-182, 128), (-124, 92),
        (-104, 0), (-94, -120), (-84, -240), (-74, -330)]
STOM = catmull_closed(_OUT, 14)
ESO = [(-42, -322), (-44, -380), (-38, -430), (-34, -470)]
DUO = [(-418, 64), (-480, 78), (-540, 100), (-600, 116)]
FOCUS_L = (30.0, 280.0)           # point de la paroi (grande courbure, en bas) vers lequel on zoome
def org_pt(p): return (ORG_C[0] + p[0] * ORG_S, ORG_C[1] + p[1] * ORG_S)

def stomach(ctx, T, mk=0.35):
    wall, mu = 46.0, 12.0
    ctx.save(); ctx.translate(*ORG_C); ctx.scale(ORG_S, ORG_S)
    # œsophage et duodénum (tubes), qui s'effacent en transparence vers leurs extrémités (aucun bloc de couleur)
    for tube, grad in ((ESO, (0, -478, 0, -405)), (DUO, (-610, 0, -515, 0))):
        pts = catmull_open(tube, 10)
        ctx.push_group()
        poly_path(ctx, pts, False); ctx.set_line_width(86); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, TIS, 1); ctx.stroke()
        poly_path(ctx, pts, False); ctx.set_line_width(40); rgba(ctx, (0.30, 0.08, 0.16), 1); ctx.stroke()
        pat = ctx.pop_group()
        m = cairo.LinearGradient(*grad); m.add_color_stop_rgba(0, 0, 0, 0, 0); m.add_color_stop_rgba(1, 0, 0, 0, 1)
        ctx.set_source(pat); ctx.mask(m)
    neon_path(ctx, lambda c: poly_path(c, STOM), (1.0, 0.45, 0.55), 5.0, 0.55)
    ctx.save(); poly_path(ctx, STOM); ctx.clip()
    ctx.set_source_rgb(0.16, 0.05, 0.12); ctx.paint()
    lvl = -200 + 6 * math.sin(T * 1.7)                                                        # niveau du contenu (poche d'air en haut)
    g = cairo.LinearGradient(0, lvl, 0, 320); g.add_color_stop_rgba(0, *JUICE, 0.55); g.add_color_stop_rgba(1, 0.85, 0.45, 0.12, 0.75)
    ctx.new_path(); ctx.move_to(-500, lvl)
    for i in range(0, 41):
        xx = -500 + 900 * i / 40; ctx.line_to(xx, lvl + 7 * math.sin(xx * 0.02 + T * 2.2))
    ctx.line_to(400, 400); ctx.line_to(-500, 400); ctx.close_path(); ctx.set_source(g); ctx.fill()
    food_pieces(ctx, T, 70, 60, 165, 150, 54, theta(T) * 1.4, 0, 0)
    poly_path(ctx, STOM); ctx.set_line_width(2 * (wall + mu)); rgba(ctx, MUC, 0.35 + 0.5 * mk); ctx.stroke()   # mucus (fin, côté intérieur)
    poly_path(ctx, STOM); ctx.set_line_width(2 * wall)
    g = cairo.RadialGradient(0, -40, 120, 0, -40, 520); g.add_color_stop_rgb(0, *TIS); g.add_color_stop_rgb(1, *mix(TIS, TIS_D, 0.45))
    ctx.set_source(g); ctx.stroke()
    poly_path(ctx, STOM); ctx.set_line_width(wall); ctx.set_dash([18, 26], T * 6); rgba(ctx, (1.0, 0.80, 0.84), 0.35); ctx.stroke(); ctx.set_dash([])
    ctx.restore()
    ctx.restore()
