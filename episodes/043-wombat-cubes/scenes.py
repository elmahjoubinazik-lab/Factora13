exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text, scrim (aucune image extérieure n'est chargée)
# Épisode 043 (Short seul, 9:16, ~25 s) — « How Do Wombats Poop Cubes? » (série Animal Mystery).
# Brief de Nazik (2026-11-21) : UN seul mystère, anomalie visible dès l'image 1 (gros plan des crottes cubiques), puis une
# démonstration simple ; voix exacte imposée, débit naturel (el_speed 1.0) ; sous-titres mot pour mot ; bas et bord droit
# libres pour l'interface Shorts ; aucun écran noir, aucune fin d'abonnement ; illustrations 100 % dessinées ici.
# Faits (Yang et al. 2021, Soft Matter 17:475–488, « Intestines of non-uniform stiffness mold the corners of wombat
# feces » ; résumé PubMed 33289747 ; communiqués Univ. of Tasmania et Georgia Tech) : wombat commun (bare-nosed,
# Vombatus ursinus) ; les cubes se forment DANS l'intestin (dernière partie, ≈ 17 % de sa longueur), pas à la sortie ;
# la paroi alterne des zones plus rigides (≈ 2× plus épaisses, ≈ 4× plus rigides) et plus souples (deux de chaque sur la
# circonférence) ; un modèle d'anneau élastique amorti à zones rigides/souples alternées montre que des contractions
# répétées forment les coins (contraction plus rapide des zones rigides, mouvement plus lent au centre des zones
# souples) ; les coins s'accentuent progressivement. Dessin : coins aux 4 jonctions rigide/souple (interprétation du
# modèle, signalée « Simplified illustration »). Les crottes sont « à peu près » cubiques, coins arrondis.
# Échelle réelle respectée : cubes ≈ 2 cm, wombat ≈ 1 m (les cubes sont minuscules dans le plan large).
import json as _json
import numpy as _npx
from PIL import Image as _PI, ImageFilter as _IF

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
def WT(word, n=0):
    """Début (temps absolu de la vidéo) de la n-ième occurrence du mot prononcé."""
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def WE(word, n=0):
    hits = [w[2] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9

DARK = (0.03, 0.02, 0.08)
NAVB = (0.030, 0.045, 0.11)
STIFF_C = (1.0, 0.58, 0.16)      # orange : zones plus rigides
SOFT_C = (0.25, 0.82, 1.0)       # cyan : zones plus souples
POO = (0.40, 0.29, 0.18)
FUR = (0.46, 0.38, 0.30)
FUR_D = (0.22, 0.17, 0.13)
FUR_L = (0.72, 0.62, 0.49)
CLAW = (0.82, 0.76, 0.66)
SUNC = (1.0, 0.80, 0.42)
TISSUE = (0.86, 0.50, 0.52)

def lerp(a, b, k): return a + (b - a) * k
def L2(p, q, k): return (lerp(p[0], q[0], k), lerp(p[1], q[1], k))

# ---------------------------------------------------------------- outils de tracé
def smooth_closed(c, pts):
    n = len(pts); c.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
    c.close_path()

def smooth_open(c, pts):
    q = [pts[0]] + list(pts) + [pts[-1]]; c.move_to(*pts[0])
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])

def catmull(pts, per=24):
    """Polyligne lissée (Catmull-Rom) → liste de points."""
    q = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(per):
            u = k / per; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    out.append(pts[-1]); return out

def rpoly(ctx, pts, r):
    """Polygone à coins arrondis (rayon r)."""
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
    if len(pts) < 3: return pts
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

def inside(pt, poly):
    x, y = pt; c = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1: c = not c
    return c

# ---------------------------------------------------------------- textes (identité Factora, peu de mots)
def tag(ctx, s, a=1.0):
    """Mention discrète et persistante en haut à gauche (« Illustration » / « Simplified illustration »)."""
    if a <= 0: return
    font(ctx, 34 * U); w_ = ctx.text_extents(s).width + 44 * U
    x0, y0 = W * 0.055, H * 0.083
    rrect(ctx, x0, y0 - 27 * U, w_, 54 * U, 27 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 22 * U, y0, 34 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0):
    """Étiquette pleine (couleur de la zone) ; k = apparition (rebond)."""
    if a <= 0 or k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, DARK, a)
    ctx.restore()

def leader(ctx, x0, y0, x1, y1, col, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    xe, ye = x0 + (x1 - x0) * ease(k), y0 + (y1 - y0) * ease(k)
    for w_, al in ((9 * U, 0.35), (4.5 * U, 1.0)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rgba(ctx, col if al == 1.0 else DARK, al * a); ctx.stroke()
    if k > 0.95: circle(ctx, x1, y1, 11 * U, col, a); circle(ctx, x1, y1, 5 * U, WHITE, a)

def label_box(ctx, s, x, y, col=GOLD, size=50, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 56 * U; h_ = size * 1.55 * U
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, 22 * U); rgba(ctx, (0.02, 0.03, 0.09), 0.88 * a); ctx.fill()
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, 22 * U); ctx.set_line_width(4.5 * U); rgba(ctx, col, a); ctx.stroke()
    text(ctx, s, x, y, size * U, col, a)

def arrow(ctx, x0, y0, x1, y1, col, a=1.0, k=1.0, width=8):
    if a <= 0 or k <= 0: return
    xe, ye = x0 + (x1 - x0) * ease(k), y0 + (y1 - y0) * ease(k)
    ang = math.atan2(ye - y0, xe - x0); hl = 30 * U
    for col_, w_, al in ((DARK, width * 2.2, 0.6), (col, width, 1.0)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe - math.cos(ang) * hl * 0.5, ye - math.sin(ang) * hl * 0.5)
        ctx.set_line_width(w_ * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col_, al * a); ctx.stroke()
    ctx.new_path(); ctx.move_to(xe, ye)
    ctx.line_to(xe - math.cos(ang - 0.5) * hl, ye - math.sin(ang - 0.5) * hl); ctx.line_to(xe - math.cos(ang + 0.5) * hl, ye - math.sin(ang + 0.5) * hl)
    ctx.close_path(); rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- caméra (repère « monde » = écran du plan large)
HZ = 1380.0                                   # horizon (px monde)
PC = (228.0, 1530.0)                          # centre du groupe de crottes (posées sur le rocher)
def cam_at(P, S, z): return ((P[0] - (S[0] - CX) / z, P[1] - (S[1] - CY) / z), z)
K_CLOSE0 = cam_at(PC, (W * 0.46, H * 0.43), 12.2)
K_CLOSE = cam_at(PC, (W * 0.46, H * 0.43), 13.0)
K_CLOSE2 = cam_at(PC, (W * 0.46, H * 0.43), 13.8)
K_WIDE = ((CX, CY), 1.0)
K_WIDE2 = cam_at((640.0, 1400.0), (640.0 * 1.0, 1400.0), 1.035)

def cam_mix(K0, K1, u):
    """Zoom continu autour d'un pivot fixe (log-zoom), u déjà adouci."""
    (c0, z0), (c1, z1) = K0, K1
    if abs(z0 - z1) < 1e-6: return (L2(c0, c1, u), z0)
    z = math.exp(lerp(math.log(z0), math.log(z1), u))
    k = (1 / z0 - 1 / z) / (1 / z0 - 1 / z1)
    return (L2(c0, c1, k), z)

def apply_cam(ctx, K):
    (cx, cy), z = K
    ctx.translate(CX, CY); ctx.scale(z, z); ctx.translate(-cx, -cy)

def to_screen(K, p):
    (cx, cy), z = K
    return ((p[0] - cx) * z + CX, (p[1] - cy) * z + CY)

# ---------------------------------------------------------------- décor lointain (pré-calculé, flou de profondeur)
BG_X0, BG_Y0, BG_W, BG_H = -260, -320, 1960, 3240
def _build_bg():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, BG_W, BG_H); c = cairo.Context(s); c.translate(-BG_X0, -BG_Y0)
    g = cairo.LinearGradient(0, BG_Y0, 0, HZ)
    for st_, col in ((0, (0.05, 0.06, 0.17)), (0.42, (0.16, 0.12, 0.30)), (0.74, (0.62, 0.32, 0.30)), (0.92, (0.98, 0.62, 0.34)), (1, (1.0, 0.78, 0.46))):
        g.add_color_stop_rgb(st_, *col)
    c.set_source(g); c.rectangle(BG_X0, BG_Y0, BG_W, HZ - BG_Y0 + 2); c.fill()
    sx, sy = 1130, HZ - 150
    for r_, col, al in ((900, (1.0, 0.55, 0.28), 0.40), (380, SUNC, 0.55)):
        gg = cairo.RadialGradient(sx, sy, 0, sx, sy, r_); gg.add_color_stop_rgba(0, *col, al); gg.add_color_stop_rgba(1, *col, 0)
        c.set_source(gg); c.paint()
    c.arc(sx, sy, 95, 0, 2 * math.pi); c.set_source_rgb(1.0, 0.88, 0.62); c.fill()
    rnd = random.Random(4)
    # eucalyptus : troncs pâles, houppiers clairsemés bleu-vert, 2 plans (le plus lointain voilé)
    for layer, (n, haze, sc_) in enumerate(((9, 0.62, 0.65), (6, 0.28, 1.0))):
        for i in range(n):
            tx = BG_X0 + (i + rnd.uniform(0.1, 0.9)) * BG_W / n; base = HZ + 8; th = rnd.uniform(520, 820) * sc_
            trunk = mix((0.80, 0.74, 0.66), (0.62, 0.42, 0.42), haze); lean = rnd.uniform(-40, 40) * sc_
            c.new_path(); c.move_to(tx - 9 * sc_, base)
            c.curve_to(tx - 6 * sc_ + lean * 0.3, base - th * 0.4, tx - 4 * sc_ + lean * 0.7, base - th * 0.7, tx + lean, base - th)
            c.line_to(tx + lean + 5 * sc_, base - th); c.curve_to(tx + 6 * sc_ + lean * 0.7, base - th * 0.7, tx + 8 * sc_ + lean * 0.3, base - th * 0.4, tx + 11 * sc_, base)
            c.close_path(); c.set_source_rgb(*trunk); c.fill()
            for b in range(3):   # branches
                by = base - th * rnd.uniform(0.55, 0.85); bx = tx + lean * (base - by) / th; dx = rnd.choice((-1, 1)) * rnd.uniform(60, 150) * sc_
                c.new_path(); c.move_to(bx, by); c.curve_to(bx + dx * 0.4, by - 30 * sc_, bx + dx * 0.8, by - 70 * sc_, bx + dx, by - 120 * sc_)
                c.set_line_width(6 * sc_); c.set_source_rgb(*trunk); c.stroke()
            for k in range(14):   # touffes de feuillage
                fx = tx + lean + rnd.uniform(-190, 190) * sc_; fy = base - th + rnd.uniform(-90, 260) * sc_; fr = rnd.uniform(50, 110) * sc_
                col = mix(mix((0.20, 0.30, 0.26), (0.36, 0.44, 0.34), rnd.random()), (0.62, 0.42, 0.42), haze)
                c.save(); c.translate(fx, fy); c.scale(1.0, 0.62); c.arc(0, 0, fr, 0, 2 * math.pi); c.restore()
                c.set_source_rgba(*col, 0.80); c.fill()
    # herbes sèches et buissons à l'horizon, sol lointain doré
    g = cairo.LinearGradient(0, HZ, 0, BG_Y0 + BG_H)
    for st_, col in ((0, (0.78, 0.58, 0.34)), (0.15, (0.55, 0.40, 0.24)), (0.5, (0.36, 0.26, 0.17)), (1, (0.20, 0.14, 0.10))):
        g.add_color_stop_rgb(st_, *col)
    c.set_source(g); c.rectangle(BG_X0, HZ, BG_W, BG_Y0 + BG_H - HZ); c.fill()
    for i in range(90):
        bx = BG_X0 + rnd.random() * BG_W; by = HZ + rnd.uniform(-6, 30); r_ = rnd.uniform(20, 60)
        c.save(); c.translate(bx, by); c.scale(1.0, 0.45); c.arc(0, 0, r_, math.pi, 2 * math.pi); c.restore()
        c.set_source_rgba(*mix((0.45, 0.36, 0.22), (0.25, 0.28, 0.18), rnd.random()), 0.9); c.fill()
    s.flush()
    a = _npx.ndarray((BG_H, BG_W, 4), _npx.uint8, s.get_data()).copy()
    im = _PI.fromarray(a, "RGBA").filter(_IF.GaussianBlur(5))
    b = _npx.array(im, dtype=_npx.uint8, copy=True)
    out = cairo.ImageSurface.create_for_data(memoryview(b), cairo.FORMAT_ARGB32, BG_W, BG_H, BG_W * 4)
    return out, b
_BG = _build_bg()

def far_bg(ctx, K):
    """Décor lointain avec parallaxe (il bouge et grossit moins que le premier plan)."""
    (cx, cy), z = K
    zb = z ** 0.32; cb = (CX + (cx - CX) * 0.55, CY + (cy - CY) * 0.55)
    ctx.save(); ctx.translate(CX, CY); ctx.scale(zb, zb); ctx.translate(-cb[0], -cb[1])
    ctx.set_source_surface(_BG[0], BG_X0, BG_Y0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint(); ctx.restore()

# ---------------------------------------------------------------- sol, herbes, litière (repère monde)
_RG = random.Random(12)
TUSSOCKS = [(_RG.uniform(-200, 1640), HZ + (_RG.random() ** 1.6) * 420, _RG.uniform(0.6, 1.3)) for _ in range(46)]
LITTER = [(_RG.uniform(-200, 1640), HZ + 20 + _RG.random() * 700, _RG.uniform(0, 6.28), _RG.uniform(0.6, 1.4), _RG.random()) for _ in range(160)]
def euc_leaf(ctx, x, y, ang, s, col, a=1.0):
    """Feuille d'eucalyptus sèche (longue, en faucille)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    ctx.new_path(); ctx.move_to(-22, 0); ctx.curve_to(-10, -7, 10, -7, 24, -2); ctx.curve_to(10, 3, -8, 4, -22, 0); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()
    ctx.new_path(); ctx.move_to(-22, 0); ctx.curve_to(-8, -2, 8, -2, 23, -2); ctx.set_line_width(0.6); rgba(ctx, mix(col, (0.1, 0.08, 0.05), 0.4), 0.6 * a); ctx.stroke()
    ctx.restore()

def tussock(ctx, x, y, s, t):
    rnd = random.Random(int(x * 7 + y))
    for i in range(16):
        ang = -math.pi / 2 + rnd.uniform(-0.9, 0.9); h = rnd.uniform(40, 80) * s; sw = 4 * s * math.sin(t * 1.4 + x * 0.02 + i)
        ex, ey = x + math.cos(ang) * h + sw, y + math.sin(ang) * h
        ctx.new_path(); ctx.move_to(x + rnd.uniform(-8, 8) * s, y); ctx.curve_to(x, y - h * 0.4, (x + ex) / 2, (y + ey) / 2 - 6 * s, ex, ey)
        ctx.set_line_width(2.4 * s); rgba(ctx, mix((0.86, 0.70, 0.42), (0.40, 0.34, 0.20), rnd.random() * 0.7), 0.9); ctx.stroke()

def near_ground(ctx, t):
    g = cairo.LinearGradient(0, HZ - 10, 0, 2700)
    g.add_color_stop_rgba(0, 0.62, 0.47, 0.29, 0.0); g.add_color_stop_rgba(0.04, 0.58, 0.44, 0.28, 1.0)
    g.add_color_stop_rgba(0.35, 0.40, 0.30, 0.20, 1.0); g.add_color_stop_rgba(1, 0.17, 0.12, 0.09, 1.0)
    ctx.set_source(g); ctx.rectangle(-400, HZ - 10, 2300, 1500); ctx.fill()
    for (x, y, ang, s, k) in LITTER:
        euc_leaf(ctx, x, y, ang, s * (0.6 + 0.7 * (y - HZ) / 700), mix((0.62, 0.46, 0.30), (0.36, 0.26, 0.18), k), 0.85)
    for (x, y, s) in TUSSOCKS:
        if y < 1560: tussock(ctx, x, y, s * (0.5 + 0.8 * (y - HZ) / 420), t)

# ---------------------------------------------------------------- wombat commun (profil, tête à gauche ; repère local)
BODY = [(-225, -130), (-150, -174), (-40, -202), (80, -216), (190, -207), (275, -170), (328, -106), (348, -28), (342, 52), (318, 120),
        (276, 174), (210, 204), (90, 212), (-40, 210), (-150, 198), (-220, 168), (-262, 108), (-272, 30), (-256, -60)]
HEAD = [(-200, -146), (-262, -166), (-332, -160), (-394, -140), (-442, -108), (-476, -72), (-496, -36), (-502, -2), (-494, 32),
        (-472, 56), (-430, 76), (-370, 92), (-304, 102), (-244, 94), (-206, 58), (-192, -40)]
NOSE = [(-462, -64), (-486, -52), (-504, -24), (-506, 6), (-496, 26), (-476, 32), (-458, 18), (-450, -14), (-452, -46)]
EAR = [(-266, -160), (-276, -194), (-268, -224), (-246, -234), (-226, -218), (-222, -182)]
NFL = [(-240, 140), (-150, 150), (-140, 196), (-136, 228), (-128, 242), (-140, 256), (-224, 256), (-240, 242), (-242, 196)]
NHL = [(194, 150), (298, 150), (310, 196), (302, 228), (308, 242), (296, 256), (206, 256), (196, 240), (200, 196)]
FFL = [(x + 54, y - 6) for x, y in NFL]
FHL = [(x - 48, y - 6) for x, y in NHL]
def _ccw(p):
    a = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
    return list(p) if a > 0 else list(reversed(p))
BODY, HEAD, NOSE, EAR, NFL, NHL, FFL, FHL = [_ccw(p) for p in (BODY, HEAD, NOSE, EAR, NFL, NHL, FFL, FHL)]
SIL = [BODY, HEAD, NFL, NHL]
WB_POS = (859.0, 1348.0, 0.96)                 # wombat dans le plan large : nez ≈ 0,27 W, croupe ≈ 0,83 W, pattes au sol à 0,62 H

def _fur_strokes():
    rnd = random.Random(31); out = []
    for poly, n, kind in ((BODY, 2600, 0), (HEAD, 900, 1), (NFL, 260, 2), (NHL, 260, 2)):
        xs = [p[0] for p in poly]; ys = [p[1] for p in poly]; c = 0
        while c < n:
            x, y = rnd.uniform(min(xs), max(xs)), rnd.uniform(min(ys), max(ys))
            if not inside((x, y), poly): continue
            if kind == 2 and inside((x, y), BODY): continue     # pas de « chaussette » : poils des pattes seulement sous le ventre
            if kind == 1 and inside((x, y), BODY) and x > -230: continue
            if kind == 0: ang = 0.10 + 0.55 * clamp((y + 60) / 240) - 0.25 * clamp((-y - 120) / 90)
            elif kind == 1: ang = 0.05 + 0.25 * (y / 90)
            else: ang = 1.35 + rnd.uniform(-0.2, 0.2)
            ang += rnd.uniform(-0.25, 0.25); ln = rnd.uniform(10, 22) * (0.7 if kind == 1 else 1.0)
            out.append((x, y, ang, ln, rnd.random(), rnd.uniform(1.4, 2.6))); c += 1
    return out
_FUR = _fur_strokes()

def _sil_path(ctx, parts=SIL):
    for p in parts:
        smooth_closed(ctx, p)

def wombat(ctx, t, breathe=True, blink_at=(), sniff_at=(), flick_at=()):
    x0, y0, s = WB_POS
    ctx.save(); ctx.translate(x0, y0); ctx.scale(s, s)
    b = 1 + (0.010 * math.sin(t * 2.4) if breathe else 0)
    # pattes du fond (plus sombres)
    for leg in (FFL, FHL):
        ctx.new_path(); smooth_closed(ctx, leg)
        g = cairo.LinearGradient(0, 150, 0, 256); g.add_color_stop_rgb(0, *mix(FUR_D, (0, 0, 0), 0.35)); g.add_color_stop_rgb(1, *mix(FUR_D, FUR, 0.25))
        ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.translate(0, 254); ctx.scale(1, b); ctx.translate(0, -254)
    ctx.push_group()
    ctx.new_path(); _sil_path(ctx); smooth_closed(ctx, EAR); rgba(ctx, FUR, 1); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_ATOP)
    for (x, y, ang, ln, k, w_) in _FUR:   # poils (texture rêche du wombat commun)
        ctx.new_path(); ctx.move_to(x, y); ctx.line_to(x + math.cos(ang) * ln, y + math.sin(ang) * ln)
        ctx.set_line_width(w_); rgba(ctx, FUR_L if k > 0.55 else FUR_D, 0.30 if k > 0.55 else 0.34); ctx.stroke()
    # volume : ventre et pattes dans l'ombre, contre-jour doré sur le dos, lumière douce de face
    g = cairo.LinearGradient(0, -120, 0, 260); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(0.55, 0.05, 0.03, 0.02, 0.30); g.add_color_stop_rgba(1, 0.04, 0.02, 0.02, 0.62)
    ctx.set_source(g); ctx.paint()
    g = cairo.RadialGradient(520, -420, 60, 520, -420, 760); g.add_color_stop_rgba(0, 1.0, 0.66, 0.30, 0.55); g.add_color_stop_rgba(1, 1.0, 0.66, 0.30, 0)
    ctx.set_source(g); ctx.paint()
    g = cairo.RadialGradient(-300, -120, 30, -300, -120, 380); g.add_color_stop_rgba(0, 1.0, 0.92, 0.80, 0.16); g.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(g); ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    # modelé : joue / mâchoire, épaule, jonction des pattes (ombres douces)
    for pts, w_, al in (([(-440, 70), (-380, 86), (-306, 94), (-252, 80), (-228, 46)], 16, 0.16),):
        ctx.new_path(); smooth_open(ctx, pts); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, FUR_D, al); ctx.stroke()
    ctx.pop_group_to_source(); ctx.paint()
    # oreille (intérieur sombre), contre-jour sur les bords
    fl = max([0.0] + [math.exp(-((t - ft) / 0.12) ** 2) for ft in flick_at])
    ctx.save(); ctx.translate(-244, -180); ctx.rotate(-0.25 * fl); ctx.translate(244, 180)
    ctx.new_path(); smooth_closed(ctx, [(-260, -170), (-266, -196), (-258, -218), (-244, -224), (-232, -210), (-230, -184)])
    rgba(ctx, (0.16, 0.11, 0.09), 0.85); ctx.fill()
    ctx.restore()
    # truffe nue granuleuse (signe distinctif du wombat commun)
    sn = max([0.0] + [math.exp(-((t - st_) / 0.10) ** 2) for st_ in sniff_at])
    ctx.save(); ctx.translate(-478, -12); ctx.scale(1 + 0.04 * sn, 1 - 0.05 * sn); ctx.translate(478, 12)
    ctx.new_path(); smooth_closed(ctx, NOSE); g = cairo.LinearGradient(-500, -60, -450, 30); g.add_color_stop_rgb(0, 0.20, 0.17, 0.16); g.add_color_stop_rgb(1, 0.06, 0.05, 0.05)
    ctx.set_source(g); ctx.fill()
    rnd = random.Random(3)
    for i in range(70):
        px, py = rnd.uniform(-504, -452), rnd.uniform(-60, 28)
        if inside((px, py), NOSE): circle(ctx, px, py, rnd.uniform(1.0, 2.2), (0.30, 0.27, 0.26), 0.55)
    ctx.new_path(); ctx.move_to(-503, -6); ctx.curve_to(-498, -16, -486, -14, -484, -4); ctx.curve_to(-490, 2, -498, 2, -503, -6); rgba(ctx, (0.0, 0.0, 0.0), 0.95); ctx.fill()
    ctx.new_path(); ctx.move_to(-488, -50); ctx.curve_to(-478, -56, -464, -54, -458, -44); ctx.set_line_width(4); rgba(ctx, (1, 0.92, 0.85), 0.35); ctx.stroke()
    ctx.restore()
    ctx.new_path(); ctx.move_to(-486, 40); ctx.curve_to(-474, 50, -456, 52, -440, 48); ctx.set_line_width(3); rgba(ctx, (0.08, 0.06, 0.05), 0.7); ctx.stroke()
    # œil (petit, loin de la truffe)
    bl = max([0.0] + [clamp(1 - abs(t - bt) / 0.09) for bt in blink_at])
    circle(ctx, -380, -76, 17, (0.20, 0.15, 0.12), 0.8)
    ctx.save(); ctx.translate(-380, -76); ctx.scale(1, max(0.08, 1 - bl)); circle(ctx, 0, 0, 11, (0.05, 0.03, 0.03), 1); ctx.restore()
    if bl < 0.5: circle(ctx, -384, -80, 3.6, WHITE, 0.85)
    # griffes
    for (gx, gy) in ((-238, 248), (-228, 252), (-216, 254), (-204, 255), (198, 250), (208, 254), (220, 255)):
        ctx.new_path(); ctx.move_to(gx + 4, gy - 4); ctx.curve_to(gx - 6, gy - 2, gx - 12, gy + 2, gx - 16, gy + 6); ctx.set_line_width(4.5); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rgba(ctx, CLAW, 0.95); ctx.stroke()
    # frange de poils en contre-jour sur le dos
    rnd = random.Random(17)
    top = sorted([p for p in BODY if p[1] < -40 and p[0] > -240], key=lambda p: p[0])
    edge = catmull(top, 8)
    for i in range(1, len(edge) - 1, 1):
        (xa, ya), (xb, yb) = edge[i - 1], edge[i + 1]
        nx, ny = (yb - ya), -(xb - xa); nl = math.hypot(nx, ny) + 1e-9; nx, ny = nx / nl, ny / nl
        if ny > 0: nx, ny = -nx, -ny
        x, y = edge[i]; ln = rnd.uniform(5, 13)
        ctx.new_path(); ctx.move_to(x - nx * 3, y - ny * 3); ctx.line_to(x + nx * ln + 4, y + ny * ln)
        ctx.set_line_width(rnd.uniform(1.3, 2.4)); rgba(ctx, mix(FUR_L, SUNC, 0.45), 0.55); ctx.stroke()
    ctx.restore()
    ctx.restore()

def wombat_ground_shadow(ctx):
    x0, y0, s = WB_POS
    g = cairo.RadialGradient(x0 + 20 * s, y0 + 254 * s, 10, x0 + 20 * s, y0 + 254 * s, 420 * s)
    g.add_color_stop_rgba(0, 0.05, 0.03, 0.02, 0.55); g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
    ctx.save(); ctx.translate(0, y0 + 254 * s); ctx.scale(1, 0.12); ctx.translate(0, -(y0 + 254 * s))
    ctx.set_source(g); ctx.arc(x0 + 20 * s, y0 + 254 * s, 420 * s, 0, 2 * math.pi); ctx.fill(); ctx.restore()

def wombat_outline(ctx):
    """Silhouette du wombat (repère monde) : pour le schéma « rayons X »."""
    x0, y0, s = WB_POS
    ctx.save(); ctx.translate(x0, y0); ctx.scale(s, s); ctx.new_path(); _sil_path(ctx, [BODY, HEAD, NFL, NHL, FFL, FHL]); ctx.restore()

# ---------------------------------------------------------------- rocher et crottes cubiques (≈ 2 cm : 18 px monde)
ROCK_TOP = [(80, 1538), (128, 1512), (210, 1500), (300, 1502), (366, 1516), (392, 1540), (360, 1560), (280, 1570), (180, 1572), (104, 1562)]
ROCK = [(78, 1538), (122, 1511), (210, 1499), (300, 1501), (368, 1515), (396, 1546), (404, 1598), (390, 1646), (342, 1672), (250, 1682), (160, 1680), (98, 1664), (66, 1624), (62, 1576)]
_RR = random.Random(8)
ROCK_GRAIN = []
while len(ROCK_GRAIN) < 2600:
    p = (_RR.uniform(140, 320), _RR.uniform(1496, 1640))
    if inside(p, ROCK): ROCK_GRAIN.append((p[0], p[1], _RR.uniform(0.06, 0.32), _RR.random()))
MOTTLE = []
while len(MOTTLE) < 90:
    p = (_RR.uniform(70, 400), _RR.uniform(1500, 1680))
    if inside(p, ROCK): MOTTLE.append((p[0], p[1], _RR.uniform(3, 16), _RR.random()))
LICHEN = []
for _c in range(16):
    cx_, cy_ = _RR.uniform(90, 390), _RR.uniform(1540, 1670); col_ = _RR.random() > 0.6
    for _k in range(30):
        p = (cx_ + _RR.gauss(0, 2.2), cy_ + _RR.gauss(0, 1.4))
        if inside(p, ROCK) and not (175 < p[0] < 265 and p[1] < 1560): LICHEN.append((p[0], p[1], _RR.uniform(0.25, 0.8), col_))
CUBES = [((214, 1521), 0.42, 17.5, 1, 0.97), ((244, 1524), 0.95, 18.5, 2, 1.0), ((206, 1537), 0.20, 18.0, 3, 0.94), ((238, 1541), 0.62, 19.0, 4, 1.03)]

def rock(ctx):
    ctx.new_path(); smooth_closed(ctx, ROCK)
    g = cairo.LinearGradient(0, 1500, 0, 1706); g.add_color_stop_rgb(0, 0.46, 0.42, 0.38); g.add_color_stop_rgb(1, 0.20, 0.18, 0.17)
    ctx.set_source(g); ctx.fill()
    ctx.new_path(); smooth_closed(ctx, ROCK_TOP)
    g = cairo.LinearGradient(100, 1500, 380, 1560); g.add_color_stop_rgb(0, 0.66, 0.60, 0.52); g.add_color_stop_rgb(1, 0.52, 0.47, 0.42)
    ctx.set_source(g); ctx.fill()
    g = cairo.RadialGradient(380, 1480, 10, 380, 1480, 260); g.add_color_stop_rgba(0, 1.0, 0.70, 0.36, 0.30); g.add_color_stop_rgba(1, 1.0, 0.70, 0.36, 0)
    ctx.new_path(); smooth_closed(ctx, ROCK); ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); smooth_closed(ctx, ROCK); ctx.clip()
    for (x, y, r_, k) in MOTTLE:
        g = cairo.RadialGradient(x, y, 0, x, y, r_); col = (0.80, 0.76, 0.68) if k > 0.5 else (0.18, 0.16, 0.15)
        g.add_color_stop_rgba(0, *col, 0.16); g.add_color_stop_rgba(1, *col, 0); ctx.set_source(g); ctx.arc(x, y, r_, 0, 2 * math.pi); ctx.fill()
    g = cairo.LinearGradient(0, 1556, 0, 1580); g.add_color_stop_rgba(0, 0.10, 0.08, 0.07, 0.0); g.add_color_stop_rgba(1, 0.10, 0.08, 0.07, 0.30)
    ctx.set_source(g); ctx.rectangle(40, 1556, 400, 140); ctx.fill()
    for (x, y, r_, k) in ROCK_GRAIN:
        circle(ctx, x, y, r_, (0.86, 0.82, 0.76) if k > 0.5 else (0.20, 0.18, 0.17), 0.40)
    for (x, y, r_, k) in LICHEN:
        circle(ctx, x, y, r_, (0.88, 0.60, 0.26) if k else (0.70, 0.74, 0.58), 0.55)
    ctx.restore()
    euc_leaf(ctx, 286, 1536, 0.25, 0.9, (0.60, 0.46, 0.32), 0.95)
    euc_leaf(ctx, 160, 1528, -0.4, 0.75, (0.50, 0.40, 0.28), 0.9)

_FACES = [((2, 6, 7, 3), (0, 1, 0)), ((1, 3, 7, 5), (0, 0, 1)), ((0, 4, 6, 2), (0, 0, -1)), ((4, 5, 7, 6), (1, 0, 0)), ((0, 2, 3, 1), (-1, 0, 0))]
PHI = math.radians(32)
LIGHT = (-0.45, 0.80, 0.40); LN = math.sqrt(sum(v * v for v in LIGHT)); LIGHT = tuple(v / LN for v in LIGHT)
RIM = (0.75, 0.25, -0.60)

def poo_cube(ctx, x, y, e, yaw, seed, tone=1.0, sq=1.0):
    """Crotte « cubique » : faces à peu près planes, coins et arêtes arrondis, fibres végétales (vue de 3/4, d'en haut).
    sq = netteté des coins (1 = cube aux coins arrondis)."""
    rnd = random.Random(seed)
    V = []
    for i in range(8):
        sx, sy, sz = (1 if i & 4 else -1), (1 if i & 2 else -1), (1 if i & 1 else -1)
        V.append((sx * 0.5 * (1 + rnd.uniform(-0.10, 0.10)), sy * 0.5 * (1 + rnd.uniform(-0.08, 0.05)), sz * 0.5 * (1 + rnd.uniform(-0.10, 0.10))))
    ca, sa, cp, sp = math.cos(yaw), math.sin(yaw), math.cos(PHI), math.sin(PHI)
    def rot(v): return (v[0] * ca + v[2] * sa, v[1], -v[0] * sa + v[2] * ca)
    def proj(v):
        r = rot(v); return (x + e * r[0], y + e * (-r[1] * cp + r[2] * sp - 0.5 * cp))
    P = [proj(v) for v in V]
    base = mix(POO, (0.36, 0.32, 0.26), 0.25 * rnd.random())
    # ombre portée
    g = cairo.RadialGradient(x, y + e * 0.12, 0, x, y + e * 0.12, e * 0.95)
    g.add_color_stop_rgba(0, 0.05, 0.03, 0.02, 0.6); g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
    ctx.save(); ctx.translate(x, y + e * 0.12); ctx.scale(1, 0.42); ctx.translate(-x, -(y + e * 0.12)); ctx.set_source(g)
    ctx.arc(x, y + e * 0.12, e * 0.95, 0, 2 * math.pi); ctx.fill(); ctx.restore()
    vis = []
    for idx, n in _FACES:
        nr = rot(n)
        if nr[1] * sp + nr[2] * cp > 0.03:
            lam = max(0.0, sum(nr[j] * LIGHT[j] for j in range(3))); rim = max(0.0, sum(nr[j] * RIM[j] for j in range(3)))
            col = tuple(min(1.0, base[j] * tone * (0.42 + 0.95 * lam) + (0.30, 0.17, 0.05)[j] * rim) for j in range(3))
            vis.append((idx, col))
    hp = hull(P)
    hp = [(p[0] + rnd.uniform(-0.02, 0.02) * e, p[1] + rnd.uniform(-0.02, 0.02) * e) for p in hp]
    rad = e * (0.10 + 0.10 * (1 - sq))
    rpoly(ctx, hp, rad * 1.6); rgba(ctx, mix(base, (0, 0, 0), 0.45), 1); ctx.fill()
    ctx.save(); rpoly(ctx, hp, rad * 1.6); ctx.clip()
    for idx, col in vis:
        pts = [P[i] for i in idx]; c0 = (sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4)
        pts = [L2(c0, p, 0.985) for p in pts]
        rpoly(ctx, pts, rad); g = cairo.LinearGradient(pts[0][0], pts[0][1], pts[2][0], pts[2][1])
        g.add_color_stop_rgb(0, *[min(1, v * 1.10) for v in col]); g.add_color_stop_rgb(1, *[v * 0.86 for v in col]); ctx.set_source(g); ctx.fill()
    # arêtes arrondies : fondu entre faces voisines + reflet sur les arêtes du dessus
    for i1 in range(len(vis)):
        for i2 in range(i1 + 1, len(vis)):
            sh = [v for v in vis[i1][0] if v in vis[i2][0]]
            if len(sh) != 2: continue
            a_, b_ = P[sh[0]], P[sh[1]]; cm = mix(vis[i1][1], vis[i2][1], 0.5)
            for w_, al in ((0.16, 0.35), (0.09, 0.45)):
                ctx.new_path(); ctx.move_to(*L2(a_, b_, 0.08)); ctx.line_to(*L2(a_, b_, 0.92)); ctx.set_line_width(e * w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                rgba(ctx, cm, al); ctx.stroke()
            if 0 in (vis[i1][0], vis[i2][0]) or (2, 6, 7, 3) in (vis[i1][0], vis[i2][0]):
                ctx.new_path(); ctx.move_to(*L2(a_, b_, 0.12)); ctx.line_to(*L2(a_, b_, 0.88)); ctx.set_line_width(e * 0.03)
                rgba(ctx, mix(cm, (1.0, 0.85, 0.65), 0.45), 0.55); ctx.stroke()
    # fibres végétales et grains (texture mate)
    for idx, col in vis:
        q = [P[i] for i in idx]
        def bil(u, v): return (q[0][0] * (1 - u) * (1 - v) + q[1][0] * u * (1 - v) + q[2][0] * u * v + q[3][0] * (1 - u) * v,
                              q[0][1] * (1 - u) * (1 - v) + q[1][1] * u * (1 - v) + q[2][1] * u * v + q[3][1] * (1 - u) * v)
        for k in range(46):
            u, v = rnd.uniform(0.08, 0.92), rnd.uniform(0.08, 0.92); ang = rnd.uniform(0, 6.28); ln = rnd.uniform(0.05, 0.15)
            p0 = bil(u, v); p1 = bil(clamp(u + math.cos(ang) * ln), clamp(v + math.sin(ang) * ln))
            light = rnd.random() > 0.45
            ctx.new_path(); ctx.move_to(*p0); ctx.line_to(*p1); ctx.set_line_width(e * rnd.uniform(0.008, 0.017)); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            rgba(ctx, (0.80, 0.68, 0.46) if light else (0.13, 0.09, 0.06), rnd.uniform(0.30, 0.55)); ctx.stroke()
        for k in range(50):
            p0 = bil(rnd.random(), rnd.random()); circle(ctx, p0[0], p0[1], e * rnd.uniform(0.004, 0.012), (0.9, 0.8, 0.6) if rnd.random() > 0.5 else (0.1, 0.07, 0.05), 0.5)
        for k in range(7):   # bosses et creux (surface irrégulière)
            p0 = bil(rnd.uniform(0.15, 0.85), rnd.uniform(0.15, 0.85)); r_ = e * rnd.uniform(0.08, 0.20)
            g = cairo.RadialGradient(p0[0], p0[1], 0, p0[0], p0[1], r_); col = (0.70, 0.56, 0.38) if rnd.random() > 0.5 else (0.08, 0.05, 0.03)
            g.add_color_stop_rgba(0, *col, 0.22); g.add_color_stop_rgba(1, *col, 0); ctx.set_source(g); ctx.arc(p0[0], p0[1], r_, 0, 2 * math.pi); ctx.fill()
    if vis and vis[0][0] == (2, 6, 7, 3):   # petite fissure de séchage sur le dessus
        q = [P[i] for i in vis[0][0]]; a_ = L2(q[0], q[1], 0.3); b_ = L2(q[3], q[2], 0.55); m_ = L2(a_, b_, 0.5)
        ctx.new_path(); ctx.move_to(*a_); ctx.curve_to(m_[0] + e * 0.04, m_[1], m_[0] - e * 0.03, m_[1], b_[0], b_[1]); ctx.set_line_width(e * 0.008); rgba(ctx, (0.08, 0.05, 0.03), 0.35); ctx.stroke()
    ctx.restore()
    rpoly(ctx, hp, rad * 1.6); ctx.set_line_width(e * 0.016); rgba(ctx, (0.06, 0.04, 0.03), 0.30); ctx.stroke()

def cubes_on_rock(ctx):
    for (p, yaw, e, seed, tone) in sorted(CUBES, key=lambda c: c[0][1]):
        poo_cube(ctx, p[0], p[1], e, yaw, seed, tone)

def foreground(ctx, t):
    rnd = random.Random(44)
    for i in range(36):   # herbes au pied du rocher, devant le wombat
        bx = rnd.uniform(-60, 1500); by = rnd.uniform(1650, 1760); h = rnd.uniform(40, 110)
        if 440 < bx < 1300 and by < 1700: continue
        sw = 6 * math.sin(t * 1.2 + i)
        ctx.new_path(); ctx.move_to(bx - 3, by); ctx.curve_to(bx, by - h * 0.5, bx + sw * 0.6, by - h * 0.8, bx + sw, by - h)
        ctx.curve_to(bx + sw * 0.5, by - h * 0.75, bx + 2, by - h * 0.4, bx + 3, by); ctx.close_path()
        rgba(ctx, mix((0.84, 0.66, 0.36), (0.30, 0.22, 0.12), 0.3 + 0.5 * rnd.random()), 0.95); ctx.fill()

# ---------------------------------------------------------------- plan « nature » : décor + wombat + rocher, mise au point
def _blur_layer(draw, radius):
    """Dessine les plans du fond dans une petite surface, la floute (profondeur de champ) et la renvoie."""
    sw, sh = W // 4, H // 4
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, sw, sh); c = cairo.Context(s); c.scale(0.25, 0.25); draw(c); s.flush()
    a = _npx.ndarray((sh, sw, 4), _npx.uint8, s.get_data()).copy()
    im = _PI.fromarray(a, "RGBA").filter(_IF.GaussianBlur(max(0.1, radius / 4)))
    b = _npx.array(im, dtype=_npx.uint8, copy=True)
    return cairo.ImageSurface.create_for_data(memoryview(b), cairo.FORMAT_ARGB32, sw, sh, sw * 4), b

def nature(ctx, T, K, wombat_kw=None):
    (_, z) = K
    blur = 30.0 * clamp((z - 1.6) / 6.0) * U
    def back(c):
        far_bg(c, K)
        c.save(); apply_cam(c, K); near_ground(c, T); wombat_ground_shadow(c); wombat(c, T, **(wombat_kw or {})); c.restore()
    if blur > 1.0:
        s, keep = _blur_layer(back, blur)
        ctx.save(); ctx.scale(4, 4); ctx.set_source(cairo.SurfacePattern(s)); ctx.get_source().set_filter(cairo.FILTER_BILINEAR); ctx.paint(); ctx.restore()
    else:
        back(ctx)
    ctx.save(); apply_cam(ctx, K); rock(ctx); cubes_on_rock(ctx); foreground(ctx, T); ctx.restore()
    g = cairo.RadialGradient(W * 0.46, H * 0.45, H * 0.28, W * 0.46, H * 0.45, H * 0.78)   # vignette douce
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.02, 0.01, 0.04, 0.50); ctx.set_source(g); ctx.paint()

# ---------------------------------------------------------------- intestin simplifié (repère local du wombat)
GUT = [(-190, -60), (-196, 20), (-150, 86), (-70, 112), (10, 84), (30, 14), (90, -42), (170, -36), (206, 22), (186, 84), (224, 118),
       (284, 106), (322, 74), (340, 58)]
_GUTP = catmull(GUT, 30)
_GL = [0.0]
for i in range(1, len(_GUTP)): _GL.append(_GL[-1] + math.hypot(_GUTP[i][0] - _GUTP[i - 1][0], _GUTP[i][1] - _GUTP[i - 1][1]))
GUT_LEN = _GL[-1]
FINAL = 0.80                                   # dernière partie de l'intestin (≈ 17–20 % de la longueur) : surlignée
def gut_at(f):
    """Point et angle de la tangente à la fraction f de la longueur."""
    d = clamp(f) * GUT_LEN
    i = max(1, min(len(_GL) - 1, next((k for k in range(len(_GL)) if _GL[k] >= d), len(_GL) - 1)))
    k = (d - _GL[i - 1]) / max(1e-9, _GL[i] - _GL[i - 1]); p = L2(_GUTP[i - 1], _GUTP[i], k)
    return p, math.atan2(_GUTP[i][1] - _GUTP[i - 1][1], _GUTP[i][0] - _GUTP[i - 1][0])

def gut_path(ctx, f0, f1):
    pts = [p for p, l in zip(_GUTP, _GL) if f0 * GUT_LEN <= l <= f1 * GUT_LEN]
    if f1 * GUT_LEN > (pts[-1:] and _GL[_GUTP.index(pts[-1])] or 0): pts = pts + [gut_at(f1)[0]]
    if len(pts) < 2: return False
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    return True

def superellipse(ctx, cx, cy, rx, ry, n, rot=0.0, steps=72, deform=None):
    ctx.new_path()
    for i in range(steps + 1):
        th = 2 * math.pi * i / steps; c, s = math.cos(th), math.sin(th)
        x = rx * (abs(c) ** (2 / n)) * (1 if c >= 0 else -1); y = ry * (abs(s) ** (2 / n)) * (1 if s >= 0 else -1)
        if deform: x, y = deform(th, x, y)
        X = cx + x * math.cos(rot) - y * math.sin(rot); Y = cy + x * math.sin(rot) + y * math.cos(rot)
        (ctx.move_to if i == 0 else ctx.line_to)(X, Y)
    ctx.close_path()

def gut_world(ctx, T, draw_k=1.0, glow_final=0.0, a=1.0, flow=True):
    """Intestin schématique dans la silhouette (repère monde)."""
    x0, y0, s = WB_POS
    ctx.save(); ctx.translate(x0, y0); ctx.scale(s, s)
    k = clamp(draw_k)
    if k > 0:
        if gut_path(ctx, 0, k):
            for w_, col, al in ((62, TISSUE, 0.25), (46, TISSUE, 0.95), (30, (0.36, 0.13, 0.17), 1.0)):
                ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, al * a)
                ctx.stroke_preserve()
            ctx.new_path()
        if k > FINAL and glow_final > 0 and gut_path(ctx, FINAL, k):   # dernière partie surlignée en or
            for w_, al in ((110, 0.10), (78, 0.22), (54, 0.85)):
                ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, GOLD, al * a * glow_final); ctx.stroke_preserve()
            ctx.new_path()
            if gut_path(ctx, FINAL, k):
                ctx.set_line_width(30); rgba(ctx, (0.36, 0.13, 0.17), a); ctx.stroke()
        # contenu : boules molles au début, de plus en plus « carrées » dans la dernière partie (formées DEDANS)
        n = 15
        for i in range(n):
            f = (i + 0.5) / n * 0.97
            if flow and f < FINAL - 0.04: f = (f + 0.02 * T) % (FINAL - 0.04)
            if f > k - 0.02: continue
            p, ang = gut_at(f)
            sq = clamp((f - (FINAL - 0.06)) / (1 - FINAL))
            nexp = 2.0 + 3.2 * sq
            r_ = 11.5 + 1.5 * sq
            superellipse(ctx, p[0], p[1], r_, r_, nexp, ang, 40)
            rgba(ctx, mix((0.55, 0.40, 0.24), POO, sq), a); ctx.fill_preserve()
            ctx.set_line_width(2.2); rgba(ctx, (0.15, 0.09, 0.05), 0.8 * a); ctx.stroke()
    ctx.restore()

def gut_point_world(f):
    p, _ = gut_at(f); x0, y0, s = WB_POS
    return (x0 + p[0] * s, y0 + p[1] * s)

# ---------------------------------------------------------------- coupe transversale (repère écran)
XC = (W * 0.46, H * 0.405)
XR = 262.0 * U                            # rayon du contenu (px)
def xsection(ctx, T, cx, cy, sc_, a=1.0):
    """Paroi : 2 zones plus rigides (haut/bas, ≈ 2× plus épaisses) et 2 plus souples (gauche/droite) ;
    contractions répétées → coins progressivement plus marqués aux jonctions (pas un moule carré)."""
    if a <= 0: return
    t_on = WT("contracts"); t_cor = WT("corners")
    # contractions : impulsions régulières à partir de « contracts »
    P = 0.62; pulses = [t_on + i * P for i in range(6) if t_on + i * P < t_cor + 0.4]
    def pulse(dt, rate):   # montée rapide (zones rigides) ou plus lente (centre des zones souples), puis relâchement
        if dt < 0 or dt > P: return 0.0
        up = clamp(dt / (0.16 if rate > 1 else 0.30)); down = clamp((P - dt) / 0.30)
        return min(up, down)
    fast = max([0.0] + [pulse(T - p, 2) for p in pulses]); slow = max([0.0] + [pulse(T - p, 1) for p in pulses])
    done = sum(1 for p in pulses if T > p + 0.2)
    sqk = clamp(done / max(1, len(pulses)))
    if T > t_cor: sqk = 1.0
    nexp = 2.0 + 2.2 * ease(sqk) + 0.5 * ease(sqk) * fast
    R = XR * sc_
    def wsoft(th):   # 1 au centre des zones souples (gauche/droite), 0 au centre des zones rigides (haut/bas)
        return clamp(0.5 + 0.5 * math.cos(2 * th) * 1.6)
    def deform(th, x, y):
        ws = wsoft(th); d = 1 - 0.055 * ((1 - ws) * fast + ws * slow)
        return x * d, y * d
    def ring_pts(off_soft, off_stiff, steps=180, nn=None):
        pts = []; ne = nn or nexp
        for i in range(steps):
            th = 2 * math.pi * i / steps; c, s_ = math.cos(th), math.sin(th)
            x = R * (abs(c) ** (2 / ne)) * (1 if c >= 0 else -1); y = R * (abs(s_) ** (2 / ne)) * (1 if s_ >= 0 else -1)
            x, y = deform(th, x, y)
            rr = math.hypot(x, y) + 1e-9; ws = wsoft(th); off = (off_soft * ws + off_stiff * (1 - ws)) * sc_
            pts.append((cx + x + x / rr * off, cy + y + y / rr * off))
        return pts
    # couleurs des zones : neutres, puis orange (« stiffer ») et cyan (« softer ») au mot prononcé
    kst = prog(T, WT("stiffer") - 0.05, WT("stiffer") + 0.30); kso = prog(T, WT("softer") - 0.05, WT("softer") + 0.30)
    outer = ring_pts(70, 128, nn=2.0 + (nexp - 2.0) * 0.18); inner = ring_pts(6, 6)
    # paroi : segments colorés selon la zone
    n = len(outer)
    for i in range(n):
        th = 2 * math.pi * (i + 0.5) / n; ws = wsoft(th)
        base = TISSUE
        col = mix(mix(base, STIFF_C, kst), mix(base, SOFT_C, kso), clamp((ws - 0.35) / 0.3))
        j = (i + 1) % n
        ctx.new_path(); ctx.move_to(*inner[i]); ctx.line_to(*outer[i]); ctx.line_to(*outer[j]); ctx.line_to(*inner[j]); ctx.close_path()
        rgba(ctx, col, a); ctx.fill_preserve(); ctx.set_line_width(1.2); ctx.stroke()
    # halo néon sur le contour extérieur, texture de muscle (fines stries)
    def outer_path(c):
        c.move_to(*outer[0])
        for p in outer[1:]: c.line_to(*p)
        c.close_path()
    ctx.save(); ctx.new_path(); outer_path(ctx); ctx.set_line_width(10 * U * sc_); rgba(ctx, WHITE, 0.25 * a); ctx.stroke(); ctx.restore()
    for i in range(0, n, 3):
        p0 = L2(inner[i], outer[i], 0.25); p1 = L2(inner[i], outer[i], 0.80)
        ctx.new_path(); ctx.move_to(*p0); ctx.line_to(*p1); ctx.set_line_width(1.6 * sc_); rgba(ctx, (1, 1, 1), 0.10 * a); ctx.stroke()
    # contenu (coupe) : brun, fibres
    ctx.new_path(); ctx.move_to(*inner[0])
    for p in inner[1:]: ctx.line_to(*p)
    ctx.close_path()
    g = cairo.RadialGradient(cx - R * 0.3, cy - R * 0.35, R * 0.1, cx, cy, R * 1.1)
    g.add_color_stop_rgb(0, 0.56, 0.41, 0.26); g.add_color_stop_rgb(1, 0.30, 0.20, 0.12)
    ctx.save(); ctx.set_source(g); ctx.fill_preserve(); ctx.clip()
    rnd = random.Random(5)
    for i in range(160):
        px, py = cx + rnd.uniform(-1, 1) * R, cy + rnd.uniform(-1, 1) * R; ang = rnd.uniform(0, 6.28); ln = rnd.uniform(8, 26) * U * sc_
        ctx.new_path(); ctx.move_to(px, py); ctx.line_to(px + math.cos(ang) * ln, py + math.sin(ang) * ln); ctx.set_line_width(rnd.uniform(1.5, 3.2) * U * sc_)
        rgba(ctx, (0.82, 0.70, 0.48) if rnd.random() > 0.5 else (0.16, 0.10, 0.06), 0.45 * a); ctx.stroke()
    ctx.restore()
    ctx.new_path(); ctx.move_to(*inner[0])
    for p in inner[1:]: ctx.line_to(*p)
    ctx.close_path(); ctx.set_line_width(4 * U * sc_); rgba(ctx, (0.12, 0.07, 0.04), 0.9 * a); ctx.stroke()
    # flèches de contraction (vers l'intérieur) pendant chaque impulsion
    if fast > 0.05 and T < t_cor + 0.3:
        for i in range(8):
            th = 2 * math.pi * i / 8 + math.pi / 8; ws = wsoft(th)
            off = (64 * ws + 122 * (1 - ws)) * sc_; r0 = R + off + 105 * U * sc_; r1 = R + off + 28 * U * sc_
            amp = (1 - ws) * fast + ws * slow
            x0_, y0_ = cx + math.cos(th) * r0, cy + math.sin(th) * r0
            x1_, y1_ = cx + math.cos(th) * r1, cy + math.sin(th) * r1
            arrow(ctx, x0_, y0_, x1_, y1_, WHITE, 0.95 * amp * a, 1.0, 9)
    # coins : repères dorés au mot « corners »
    kc = prog(T, t_cor - 0.10, t_cor + 0.25)
    if kc > 0:
        for i in range(4):
            th = math.pi / 4 + i * math.pi / 2
            cxp = R * (abs(math.cos(th)) ** (2 / nexp)) * (1 if math.cos(th) >= 0 else -1); cyp = R * (abs(math.sin(th)) ** (2 / nexp)) * (1 if math.sin(th) >= 0 else -1)
            puls = 1 + 0.25 * math.exp(-((T - t_cor - 0.25) / 0.18) ** 2)
            glow(ctx, cx + cxp, cy + cyp, 60 * U * puls, GOLD, 0.55 * kc * a)
            circle(ctx, cx + cxp, cy + cyp, 15 * U * puls * ease(kc), GOLD, a); circle(ctx, cx + cxp, cy + cyp, 6 * U * ease(kc), WHITE, a)
    return outer

# ---------------------------------------------------------------- fond « schéma » (identité Factora : bleu nuit + néon)
def diagram_bg(ctx, T, a=1.0):
    if a <= 0: return
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, 0.06, 0.05, 0.17, a); g.add_color_stop_rgba(1, 0.01, 0.02, 0.07, a)
    ctx.set_source(g); ctx.paint()
    glow(ctx, W * 0.46, H * 0.40, 0.75 * H, (0.20, 0.30, 0.70), 0.20 * a)
    rnd = random.Random(8)
    for i in range(18):
        x = rnd.random() * W; y = (rnd.random() * H - T * rnd.uniform(8, 25) * U) % H
        circle(ctx, x, y, rnd.uniform(2, 5) * U, rnd.choice([CYAN, PURPLE, GOLD]), (0.18 + 0.10 * math.sin(T * 2 + i)) * a)

def xray(ctx, T, K, k, draw_k, glow_final, lab=None):
    """Schéma « rayons X » : silhouette néon du wombat + intestin simplifié."""
    diagram_bg(ctx, T, 0.93 * k)
    ctx.save(); apply_cam(ctx, K)
    z = K[1]
    ctx.push_group()
    neon_path(ctx, lambda c: wombat_outline(c), SOFT_C, 3.4 / z * U, 1.0)
    wombat_outline(ctx); ctx.set_operator(cairo.OPERATOR_SOURCE); rgba(ctx, (0.07, 0.10, 0.23), 1.0); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(0.92 * k)
    x0, y0, s = WB_POS
    ctx.save(); ctx.translate(x0, y0); ctx.scale(s, s)
    neon_path(ctx, lambda c: smooth_closed(c, NOSE), SOFT_C, 2.6 / z * U / s, 0.55 * k)
    neon_path(ctx, lambda c: smooth_closed(c, EAR), SOFT_C, 2.6 / z * U / s, 0.55 * k)
    circle(ctx, -380, -76, 9, SOFT_C, 0.8 * k)
    ctx.restore()
    gut_world(ctx, T, draw_k, glow_final, k)
    ctx.restore()

# ---------------------------------------------------------------- montage (temps absolu de la vidéo)
T_PULL0, T_PULL1 = WT("cubes", 0), WT("cubes", 0) + 0.85              # recul : des crottes au wombat
T_X0 = WT("scientists") + 0.05                                        # passage au schéma
T_IN = WT("inside", 0)
T_ZIN0 = WT("its") - 0.30; T_ZIN1 = WT("its") + 0.35                    # plongée vers la coupe
T_ZOUT0 = WT("so") - 0.02; T_ZOUT1 = WT("so") + 0.55                    # retour au schéma d'ensemble
T_BEFORE = WT("before")
T_NAT0 = WT("a", 1) - 0.05; T_NAT1 = WT("a", 1) + 0.60                        # retour au wombat (illustration)
T_END0 = WT("nature") - 0.12; T_END1 = WT("nature") + 0.75              # retour au gros plan du début
GUT_F = 0.90                                                          # point de la dernière partie où l'on « coupe »
K_OVER = cam_at((820.0, 1380.0), (W * 0.47, H * 0.42), 1.32)
K_OVER2 = cam_at((820.0, 1380.0), (W * 0.47, H * 0.42), 1.37)
def K_GUT(z): return cam_at(gut_point_world(GUT_F), XC, z)

def camera(T):
    if T < T_PULL0: return cam_mix(K_CLOSE0, K_CLOSE, clamp(T / max(T_PULL0, 0.1)))
    if T < T_PULL1: return cam_mix(K_CLOSE, K_WIDE, ease((T - T_PULL0) / (T_PULL1 - T_PULL0)))
    if T < T_X0: return cam_mix(K_WIDE, K_WIDE2, clamp((T - T_PULL1) / max(0.1, T_X0 - T_PULL1)))
    if T < T_X0 + 0.9: return cam_mix(K_WIDE2, K_OVER, ease((T - T_X0) / 0.9))
    if T < T_ZIN0: return cam_mix(K_OVER, K_OVER2, clamp((T - T_X0 - 0.9) / max(0.1, T_ZIN0 - T_X0 - 0.9)))
    if T < T_ZIN1: return cam_mix(K_OVER2, K_GUT(7.0), ease((T - T_ZIN0) / (T_ZIN1 - T_ZIN0)))
    if T < T_ZOUT0: return K_GUT(7.0)
    if T < T_ZOUT1: return cam_mix(K_GUT(7.0), K_OVER, ease((T - T_ZOUT0) / (T_ZOUT1 - T_ZOUT0)))
    if T < T_NAT0: return cam_mix(K_OVER, K_OVER2, clamp((T - T_ZOUT1) / max(0.1, T_NAT0 - T_ZOUT1)))
    if T < T_NAT1: return cam_mix(K_OVER2, K_WIDE, ease((T - T_NAT0) / (T_NAT1 - T_NAT0)))
    if T < T_END0: return cam_mix(K_WIDE, K_WIDE2, clamp((T - T_NAT1) / max(0.1, T_END0 - T_NAT1)))
    if T < T_END1: return cam_mix(K_WIDE2, K_CLOSE, ease((T - T_END0) / (T_END1 - T_END0)))
    return cam_mix(K_CLOSE, K_CLOSE2, clamp((T - T_END1) / 3.0))

WOMBAT_KW = dict(blink_at=(3.2, WT("tube") + 0.2), sniff_at=(WT("how") + 0.1, WT("soft") + 0.1), flick_at=(WT("how") + 0.35, WT("corners", 1)))

def master(ctx, T):
    K = camera(T)
    xk = prog(T, T_X0, T_X0 + 0.55) * (1 - prog(T, T_NAT0, T_NAT1))          # part du schéma (0 = illustration nature)
    xs_in = prog(T, T_ZIN0 + 0.15, T_ZIN1 + 0.10); xs_out = prog(T, T_ZOUT0, T_ZOUT1 - 0.10)
    xs = xs_in * (1 - xs_out)                                                # part de la coupe transversale
    if xk < 1 or xs < 1:
        if xk < 1: nature(ctx, T, K, WOMBAT_KW)
        if xk > 0 and xs < 1:
            draw_k = prog(T, T_X0 + 0.25, T_X0 + 1.35)
            gl = prog(T, T_IN - 0.15, T_IN + 0.35)
            xray(ctx, T, K, xk, draw_k, gl)
    if xs > 0:
        diagram_bg(ctx, T, xs)
        gp = to_screen(K, gut_point_world(GUT_F))
        cx, cy = L2(gp, XC, ease(xs)); sc_ = lerp(0.10, 1.0, ease(xs))
        xsection(ctx, T, cx, cy, sc_, clamp(xs * 1.6))
    # ---- textes (au mot près)
    if T < 3.2:   # accroche écrite, 0–3 s
        ka = 1 - prog(T, 2.75, 3.15)
        if ka > 0:
            ctx.save(); ctx.translate(0, -30 * U * (1 - ka))
            g = cairo.LinearGradient(0, 0, 0, H * 0.28); g.add_color_stop_rgba(0, 0.01, 0.01, 0.04, 0.55 * ka); g.add_color_stop_rgba(1, 0, 0, 0, 0)
            ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.28); ctx.fill()
            ctx.push_group(); poster_text(ctx, "CUBE-SHAPED", W * 0.46, H * 0.150, 138 * U, WHITE, W * 0.80); poster_text(ctx, "POOP?", W * 0.46, H * 0.213, 150 * U, GOLD, W * 0.80)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(ka); ctx.restore()
    # mention persistante : illustration / schéma simplifié
    if xk > 0.5 or xs > 0.5: tag(ctx, "Simplified illustration")
    elif T > 0.0: tag(ctx, "Illustration")
    # schéma d'ensemble : « FORMING INSIDE » (au mot « inside »), puis « ALREADY CUBES » (au mot « before »)
    K_now = K
    fpt = to_screen(K_now, gut_point_world(0.90))
    k1 = prog(T, T_IN - 0.05, T_IN + 0.30) * (1 - prog(T, T_ZIN0 - 0.2, T_ZIN0 + 0.1))
    if k1 > 0 and xs < 0.5:
        lx, ly = W * 0.50, H * 0.215
        arrow(ctx, lx + 40 * U, ly + 60 * U, fpt[0] - 6 * U, fpt[1] - 52 * U, GOLD, k1, k1)
        label_box(ctx, "FORMING INSIDE", lx, ly, GOLD, 54, k1)
    k2 = prog(T, T_BEFORE - 0.05, T_BEFORE + 0.30) * (1 - prog(T, T_NAT0, T_NAT0 + 0.3))
    if k2 > 0:
        lx, ly = W * 0.50, H * 0.215
        arrow(ctx, lx + 40 * U, ly + 60 * U, fpt[0] - 6 * U, fpt[1] - 52 * U, GOLD, k2, k2)
        label_box(ctx, "ALREADY CUBES", lx, ly, GOLD, 54, k2)
    # coupe : légendes STIFFER / SOFTER au mot prononcé
    if xs > 0.6:
        a_ = clamp((xs - 0.6) / 0.4)
        R = XR
        ks = prog(T, WT("stiffer") - 0.05, WT("stiffer") + 0.30)
        ko = prog(T, WT("softer") - 0.05, WT("softer") + 0.30)
        tx_, ty_ = XC[0] - R * 0.36, XC[1] - R * 1.28
        sx_, sy_ = XC[0] + R * 1.10 * math.cos(-0.55), XC[1] + R * 1.10 * math.sin(-0.55)
        p1 = (W * 0.27, H * 0.168); p2 = (W * 0.66, H * 0.168)
        leader(ctx, p1[0], p1[1] + 30 * U, tx_, ty_, STIFF_C, a_, ks)
        leader(ctx, p2[0], p2[1] + 30 * U, sx_, sy_, SOFT_C, a_, ko)
        pill(ctx, "STIFFER", p1[0], p1[1], STIFF_C, 54, a_, ks)
        pill(ctx, "SOFTER", p2[0], p2[1], SOFT_C, 54, a_, ko)
    # fin : petit nom de la chaîne seulement
    kf = prog(T, T_END1 - 0.1, T_END1 + 0.4)
    if kf > 0:
        font(ctx, 46 * U); txt = "FACTORA"
        ctx.save(); rgba(ctx, (0, 0, 0), 0.45 * kf)
        w_ = ctx.text_extents(txt).width + 60 * U
        rrect(ctx, W * 0.46 - w_ / 2, H * 0.155 - 34 * U, w_, 68 * U, 34 * U); ctx.fill(); ctx.restore()
        text(ctx, txt, W * 0.46, H * 0.155, 46 * U, GOLD, kf)

def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return 0.9      # 2 premières images (vignettes) : le gros plan + l'accroche écrite
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t

def sc_hook(ctx, t, d): master(ctx, _abs_t("hook", t))
def sc_explain(ctx, t, d): master(ctx, _abs_t("explain", t))
def sc_close(ctx, t, d): master(ctx, _abs_t("close", t))

SHORT_SCENES = ["hook", "explain", "close"]
SCENES = dict(hook=sc_hook, explain=sc_explain, close=sc_close)

def cover(ctx):
    master(ctx, 0.9)
