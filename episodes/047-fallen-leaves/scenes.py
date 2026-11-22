exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Épisode 047 (Short seul, 9:16, ~33 s) — « Forests Eat Their Own Leaves » (sujet proposé par Nazik le 2026-11-22, après une
# promenade en forêt : « où vont les feuilles mortes une fois tombées ? » ; sa photo du chemin sert de référence : surtout
# des feuilles de hêtre et de chêne). Stratégie 30 jours, semaine 1 : l'image 1 montre le sujet en action (tapis de
# feuilles + feuilles qui tombent), au plus 3 mots à l'écran ; dessins 100 % faits ici ; un nouveau plan toutes les ~5 s ;
# fin = les feuilles retombent (boucle) ; CTA texte « Follow Factora for more nature mysteries. ».
# Faits : champignons = principaux décomposeurs de la litière (hyphes blancs, enzymes) ; la nuit, certains vers de terre
# (Lumbricus terrestris, « nightcrawler ») tirent les feuilles dans leurs galeries (Darwin 1881 ; Minnesota Forest
# Resources Council) ; acariens et collemboles fragmentent la litière, les bactéries finissent ; la minéralisation de la
# litière fraîche fournit environ la moitié du CO2 rejeté chaque année par le sol des forêts tempérées de feuillus (PMC) ;
# une feuille de chêne perd 25 à 55 % de sa masse la 1re année (revue) ; le reste devient humus et ses nutriments
# retournent aux racines. Les schémas sont signalés « Simplified illustration ».
import json as _json

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
def WT(word, n=0):
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!:") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def SENT(scene, i=0): return _TL[scene]["sents"][i]["start"]
END_T = _TLL[-1]["end"] + 0.6

DARK = (0.03, 0.02, 0.08)
SOIL = (0.17, 0.11, 0.08)
SOIL_D = (0.09, 0.06, 0.05)
HUMUS = (0.11, 0.07, 0.05)
BARK = (0.56, 0.58, 0.55)
MOSS = (0.40, 0.55, 0.22)
LEAF_COLS = [(0.80, 0.42, 0.17), (0.70, 0.34, 0.14), (0.88, 0.55, 0.24), (0.62, 0.30, 0.13), (0.84, 0.62, 0.34), (0.74, 0.48, 0.24), (0.92, 0.66, 0.30)]
HYPHA = (0.97, 0.96, 0.90)
WORM = (0.86, 0.48, 0.52)
BACT = (0.35, 0.95, 0.60)
CO2C = (0.55, 0.88, 1.0)

def lerp(a, b, k): return a + (b - a) * k

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

# ---------------------------------------------------------------- textes
def tag(ctx, s, y=0.083, a=1.0):
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0):
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
    for w_, al, c_ in ((9 * U, 0.35, DARK), (4.5 * U, 1.0, col)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rgba(ctx, c_, al * a); ctx.stroke()
    if k > 0.95: circle(ctx, x1, y1, 11 * U, col, a); circle(ctx, x1, y1, 5 * U, WHITE, a)

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

# ---------------------------------------------------------------- feuilles (hêtre : ovale, nervures parallèles ; chêne : lobée)
def _beech():
    n = 36; R = []
    for i in range(n + 1):
        t = i / n
        w = 0.33 * math.sin(math.pi * min(1.0, t * 1.04)) ** 0.85 * (1 - 0.18 * t) * (1 + 0.05 * math.sin(t * math.pi * 14))
        R.append((w, 0.5 - t))
    return R + [(-x, y) for x, y in reversed(R)][1:-1]
def _oak():
    n = 90; R = []
    for i in range(n + 1):
        t = i / n
        env = math.sin(math.pi * t) ** 0.55 * (0.55 + 0.45 * t)
        w = 0.40 * env * (0.50 + 0.50 * abs(math.cos(math.pi * 4.5 * t)) ** 0.7)
        R.append((w, 0.5 - t))
    return R + [(-x, y) for x, y in reversed(R)][1:-1]
SHAPES = {"beech": _beech(), "oak": _oak()}
def _w_at(kind, t):
    pts = SHAPES[kind]; n = (len(pts) + 2) // 2
    i = min(n - 1, int(t * (n - 1))); return pts[i][0]

def leaf_path(ctx, kind):
    smooth_closed(ctx, SHAPES[kind])

def draw_leaf(ctx, x, y, L, ang, kind, col, a=1.0, detail=True, flip=1.0):
    if a <= 0 or L <= 0.5: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(L * flip, L)
    ctx.new_path(); leaf_path(ctx, kind)
    if detail:
        g = cairo.LinearGradient(-0.3, -0.5, 0.3, 0.5)
        g.add_color_stop_rgba(0, *mix(col, WHITE, 0.18), a); g.add_color_stop_rgba(1, *mix(col, (0.2, 0.08, 0.03), 0.30), a)
        ctx.set_source(g); ctx.fill_preserve()
        ctx.set_line_width(0.018); rgba(ctx, mix(col, (0.15, 0.06, 0.02), 0.55), 0.9 * a); ctx.stroke()
        ctx.new_path(); ctx.move_to(0, 0.62); ctx.line_to(0, -0.46); ctx.set_line_width(0.022); rgba(ctx, mix(col, (0.25, 0.10, 0.04), 0.45), a); ctx.stroke()
        for k in range(1, 8):
            t = k / 8.5; y0 = 0.5 - t; w = _w_at(kind, min(1.0, t + 0.07)) * 0.88
            for sd in (-1, 1):
                ctx.new_path(); ctx.move_to(0, y0); ctx.line_to(sd * w, y0 - 0.075); ctx.set_line_width(0.012); rgba(ctx, mix(col, (0.25, 0.10, 0.04), 0.35), 0.8 * a); ctx.stroke()
    else:
        rgba(ctx, col, a); ctx.fill()
    ctx.restore()

# ---------------------------------------------------------------- forêt (fond pré-calculé) + tapis de feuilles
HZ = H * 0.36
def _build_forest():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W), int(H)); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, HZ + H * 0.05)
    g.add_color_stop_rgb(0, 0.86, 0.84, 0.80); g.add_color_stop_rgb(0.6, 0.92, 0.74, 0.52); g.add_color_stop_rgb(1, 0.80, 0.52, 0.32)
    c.set_source(g); c.paint()
    glow(c, W * 0.50, HZ - H * 0.02, W * 0.75, (1.0, 0.80, 0.50), 0.45)
    rnd = random.Random(11)
    for layer, (n, a, wmin, wmax, col) in enumerate(((26, 0.30, 0.010, 0.022, (0.55, 0.45, 0.40)), (16, 0.55, 0.020, 0.040, (0.45, 0.42, 0.40)), (9, 0.95, 0.045, 0.085, BARK))):
        for i in range(n):
            x = rnd.uniform(-0.05, 1.05) * W
            if layer == 2 and 0.28 * W < x < 0.70 * W: x = rnd.choice((rnd.uniform(-0.05, 0.24), rnd.uniform(0.74, 1.05))) * W
            w = rnd.uniform(wmin, wmax) * W
            base = HZ + (layer * 0.06 + rnd.uniform(0.00, 0.04)) * H
            g2 = cairo.LinearGradient(x - w / 2, 0, x + w / 2, 0)
            g2.add_color_stop_rgba(0, *mix(col, (0.2, 0.2, 0.2), 0.35), a); g2.add_color_stop_rgba(0.6, *col, a); g2.add_color_stop_rgba(1, *mix(col, (0.1, 0.1, 0.1), 0.40), a)
            c.set_source(g2); c.rectangle(x - w / 2, -10, w, base + 10); c.fill()
            if layer == 2:
                g3 = cairo.LinearGradient(0, base - H * 0.18, 0, base)
                g3.add_color_stop_rgba(0, *MOSS, 0.0); g3.add_color_stop_rgba(1, *MOSS, 0.85)
                c.set_source(g3); c.rectangle(x - w / 2, base - H * 0.18, w * 0.55, H * 0.18); c.fill()
    # sol nu (terre sombre + gravillons), visible quand les feuilles disparaissent
    g4 = cairo.LinearGradient(0, HZ, 0, H); g4.add_color_stop_rgb(0, 0.30, 0.22, 0.17); g4.add_color_stop_rgb(1, 0.13, 0.09, 0.07)
    c.set_source(g4); c.rectangle(0, HZ, W, H - HZ); c.fill()
    for i in range(500):
        d = rnd.random(); y = HZ + (H * 0.98 - HZ) * d ** 1.3; x = rnd.uniform(0, W); r = (1.5 + 9 * d ** 1.5) * U
        circle(c, x, y, r, rnd.choice([(0.45, 0.42, 0.40), (0.30, 0.25, 0.22), (0.55, 0.52, 0.48)]), 0.55)
    return s
_FOREST = _build_forest()

_RC = random.Random(5)
CARPET = []
for i in range(760):
    d = _RC.random() ** 0.85
    y = HZ + (H * 1.02 - HZ) * d ** 1.25
    L = (16 + 175 * d ** 1.7) * U
    CARPET.append(dict(x=_RC.uniform(-0.05, 1.05) * W, y=y, L=L, ang=_RC.uniform(-math.pi, math.pi), kind=_RC.choice(["beech", "beech", "oak"]),
                       col=_RC.choice(LEAF_COLS), tv=_RC.uniform(0, 1), tr=_RC.uniform(0, 1), fl=_RC.choice((-1, 1))))
CARPET.sort(key=lambda l: l["y"])
FALL = [dict(x=_RC.uniform(0.05, 0.85), ph=_RC.uniform(0, 1), sp=_RC.uniform(0.10, 0.17), L=_RC.uniform(60, 150) * U, kind=_RC.choice(["beech", "oak"]),
             col=_RC.choice(LEAF_COLS), sw=_RC.uniform(0.8, 1.6)) for i in range(16)]

def carpet(ctx, T, vanish, refill):
    """vanish, refill ∈ [0, 1] : part du tapis disparue (de loin en près, au hasard) / revenue (boucle de fin)."""
    for l in CARPET:
        gone = clamp((vanish - l["tv"] * 0.85) / 0.15)
        back = clamp((refill - l["tr"] * 0.85) / 0.15)
        k = 1 - gone * (1 - back)
        if k <= 0.01: continue
        sh = 0.55 + 0.45 * k
        col = mix(l["col"], (0.20, 0.12, 0.07), (1 - k) * 0.6)
        draw_leaf(ctx, l["x"], l["y"], l["L"] * sh, l["ang"], l["kind"], col, min(1.0, k * 1.6), detail=l["L"] > 70 * U, flip=l["fl"])

def falling(ctx, T, a=1.0, upto=1.0):
    for i, f in enumerate(FALL):
        u = (f["ph"] + T * f["sp"]) % 1.0
        if u > upto: continue
        y = -H * 0.05 + u * H * 0.95
        x = f["x"] * W + 70 * U * f["sw"] * math.sin(T * 1.6 * f["sw"] + i)
        ang = 0.8 * math.sin(T * 2.0 * f["sw"] + i * 1.7)
        sq = 0.55 + 0.45 * abs(math.cos(T * 2.3 * f["sw"] + i))   # la feuille tourne sur elle-même
        draw_leaf(ctx, x, y, f["L"], ang, f["kind"], f["col"], a, detail=True, flip=sq)

def forest(ctx, T, vanish=0.0, refill=0.0, fall_a=1.0):
    ctx.set_source_surface(_FOREST, 0, 0); ctx.paint()
    carpet(ctx, T, vanish, refill)
    g = cairo.LinearGradient(0, H * 0.72, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0.02, 0.01, 0.01, 0.75)
    ctx.set_source(g); ctx.rectangle(0, H * 0.72, W, H * 0.28); ctx.fill()
    falling(ctx, T, fall_a)

# ---------------------------------------------------------------- plan B : la feuille mangée par les champignons (gros plan)
LC = (W * 0.46, H * 0.385); LL = H * 0.46
_RH = random.Random(17)
def _hyphae():
    br = []
    for k in range(34):
        side = _RH.choice((-1, 1)); t0 = _RH.uniform(0.05, 0.95)
        x0 = side * _w_at("beech", t0) * LL * 0.98; y0 = (0.5 - t0) * LL
        ang = math.atan2(0, -side) + _RH.uniform(-0.8, 0.8)
        pts = [(x0, y0)]
        for j in range(26):
            ang += _RH.uniform(-0.45, 0.45); st = _RH.uniform(10, 22) * U
            x0 += math.cos(ang) * st; y0 += math.sin(ang) * st; pts.append((x0, y0))
        br.append((pts, _RH.uniform(0, 0.45)))
    return br
HYPHAE = _hyphae()
HOLES = [(_RH.uniform(-0.25, 0.25), _RH.uniform(-0.40, 0.42), _RH.uniform(0.025, 0.07), _RH.uniform(0, 1)) for _ in range(46)]
BITES = [(-0.30, 0.10, 0.10), (0.27, -0.18, 0.09), (0.20, 0.30, 0.08)]

def soil_macro(ctx, T):
    g = cairo.RadialGradient(W * 0.46, H * 0.40, W * 0.1, W * 0.46, H * 0.45, H * 0.75)
    g.add_color_stop_rgb(0, 0.27, 0.18, 0.12); g.add_color_stop_rgb(1, 0.07, 0.045, 0.035); ctx.set_source(g); ctx.paint()
    rnd = random.Random(23)
    for i in range(260):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H); r = rnd.uniform(3, 16) * U
        circle(ctx, x, y, r, rnd.choice([(0.32, 0.23, 0.17), (0.18, 0.12, 0.09), (0.40, 0.34, 0.28)]), 0.6)
    for i in range(10):                                  # feuilles brunes autour, déjà décomposées
        draw_leaf(ctx, rnd.uniform(0, W), rnd.uniform(0, H * 0.75), rnd.uniform(160, 300) * U, rnd.uniform(-3, 3), rnd.choice(["beech", "oak"]), (0.33, 0.20, 0.11), 0.75, detail=True)

def fungi_leaf(ctx, T, k_bite, k_grow, k_dig):
    ctx.push_group()
    draw_leaf(ctx, LC[0], LC[1], LL, 0.12, "beech", mix((0.86, 0.50, 0.20), (0.30, 0.18, 0.10), 0.55 * k_dig), 1.0, detail=True)
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    ctx.save(); ctx.translate(*LC); ctx.rotate(0.12)
    for (bx, by, r) in BITES:                              # « They get eaten » : morceaux qui disparaissent
        if k_bite > 0:
            for j in range(4):
                circle(ctx, bx * LL + math.cos(j * 1.6) * r * LL * 0.5, by * LL + math.sin(j * 1.6) * r * LL * 0.5, r * LL * 0.55 * ease(k_bite), WHITE, 1)
    for (hx, hy, r, t0) in HOLES:                          # tissus digérés : la feuille devient dentelle
        kk = clamp((k_dig - t0 * 0.8) / 0.2)
        if kk > 0: circle(ctx, hx * LL, hy * LL, r * LL * ease(kk), WHITE, 1)
    ctx.restore(); ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()
    # filaments blancs (hyphes) qui envahissent la feuille
    ctx.save(); ctx.translate(*LC); ctx.rotate(0.12); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for pts, t0 in HYPHAE:
        g = clamp((k_grow - t0) / 0.55)
        if g <= 0: continue
        m = max(2, int(len(pts) * g))
        for w_, al in ((9 * U, 0.18), (3.2 * U, 0.95)):
            ctx.new_path(); ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:m]]
            ctx.set_line_width(w_); rgba(ctx, HYPHA, al); ctx.stroke()
        circle(ctx, pts[m - 1][0], pts[m - 1][1], 5 * U, WHITE, 0.9)
    ctx.restore()

def mushroom(ctx, x, y, s, k):
    if k <= 0: return
    s *= ease(k)
    ctx.new_path(); ctx.move_to(x - s * 0.12, y); ctx.curve_to(x - s * 0.10, y - s * 0.5, x - s * 0.08, y - s * 0.75, x - s * 0.06, y - s * 0.85)
    ctx.line_to(x + s * 0.06, y - s * 0.85); ctx.curve_to(x + s * 0.08, y - s * 0.75, x + s * 0.10, y - s * 0.5, x + s * 0.12, y); ctx.close_path()
    rgba(ctx, (0.95, 0.92, 0.84), 1); ctx.fill()
    ctx.new_path(); ctx.arc(x, y - s * 0.82, s * 0.42, math.pi, 2 * math.pi); ctx.close_path()
    g = cairo.LinearGradient(x, y - s * 1.25, x, y - s * 0.8); g.add_color_stop_rgb(0, 0.78, 0.50, 0.30); g.add_color_stop_rgb(1, 0.55, 0.32, 0.18)
    ctx.set_source(g); ctx.fill()

# ---------------------------------------------------------------- plan C : le ver de terre tire une feuille dans sa galerie (coupe)
SURF = H * 0.27
def cross_bg(ctx, T, night=True, humus=0.0):
    g = cairo.LinearGradient(0, 0, 0, SURF)
    if night: g.add_color_stop_rgb(0, 0.05, 0.06, 0.20); g.add_color_stop_rgb(1, 0.10, 0.12, 0.30)
    else: g.add_color_stop_rgb(0, 0.86, 0.84, 0.80); g.add_color_stop_rgb(1, 0.90, 0.70, 0.48)
    ctx.set_source(g); ctx.rectangle(0, 0, W, SURF); ctx.fill()
    if night:
        circle(ctx, W * 0.80, H * 0.10, W * 0.05, (0.96, 0.95, 0.88), 1); glow(ctx, W * 0.80, H * 0.10, W * 0.25, (0.6, 0.7, 1.0), 0.25)
        rnd = random.Random(4)
        for i in range(60): circle(ctx, rnd.uniform(0, W), rnd.uniform(0, SURF * 0.9), rnd.uniform(1, 2.5) * U, WHITE, rnd.uniform(0.3, 0.9))
    g = cairo.LinearGradient(0, SURF, 0, H); g.add_color_stop_rgb(0, 0.36, 0.25, 0.17); g.add_color_stop_rgb(0.45, 0.27, 0.19, 0.13); g.add_color_stop_rgb(1, 0.15, 0.10, 0.08)
    ctx.set_source(g); ctx.rectangle(0, SURF, W, H - SURF); ctx.fill()
    if humus > 0:                                        # couche d'humus qui s'épaissit
        hh = H * 0.09 * ease(humus)
        g = cairo.LinearGradient(0, SURF, 0, SURF + hh); g.add_color_stop_rgba(0, *HUMUS, 0.95); g.add_color_stop_rgba(1, *HUMUS, 0.0)
        ctx.set_source(g); ctx.rectangle(0, SURF, W, hh); ctx.fill()
    rnd = random.Random(9)
    for i in range(140):
        x, y = rnd.uniform(0, W), rnd.uniform(SURF + 20 * U, H); r = rnd.uniform(4, 18) * U
        ctx.save(); ctx.translate(x, y); ctx.scale(1.0, 0.7); ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
        rgba(ctx, rnd.choice([(0.45, 0.40, 0.36), (0.22, 0.16, 0.12), (0.55, 0.50, 0.44)]), 0.7); ctx.fill()
    for i in range(16):                                   # feuilles sur la surface
        draw_leaf(ctx, rnd.uniform(-0.05, 1.05) * W, SURF - rnd.uniform(0, 14) * U, rnd.uniform(110, 190) * U, math.pi / 2 + rnd.uniform(-0.4, 0.4),
                  rnd.choice(["beech", "oak"]), rnd.choice(LEAF_COLS), 1.0, detail=True)

BUR_X = W * 0.46
BURROW = [(BUR_X, SURF + 4 * U), (BUR_X + 30 * U, SURF + H * 0.10), (BUR_X - 20 * U, SURF + H * 0.20), (BUR_X + 26 * U, SURF + H * 0.32), (BUR_X, SURF + H * 0.42)]
def _poly_len(pts):
    L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    return L
def _sample(pts, per=20):
    q = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(per):
            u = k / per; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    out.append(pts[-1]); return out
_BP = _sample(BURROW); _BL = _poly_len(_BP)
def bur_at(s):
    """Point du terrier à la distance s (px) depuis l'entrée ; s < 0 : au-dessus de la surface, vers la gauche (la feuille)."""
    if s <= 0: return (BUR_X + s * 0.85, SURF - 10 * U), 0.0
    for i in range(1, len(_BL)):
        if _BL[i] >= s:
            u = (s - _BL[i - 1]) / max(1e-6, _BL[i] - _BL[i - 1]); p, q = _BP[i - 1], _BP[i]
            return (lerp(p[0], q[0], u), lerp(p[1], q[1], u)), math.atan2(q[1] - p[1], q[0] - p[0])
    return _BP[-1], math.pi / 2

def earthworm(ctx, T, head_s, length=H * 0.30, a=1.0):
    pts = [bur_at(head_s + length * k / 40)[0] for k in range(41)]
    for w_, col, al in ((44 * U, (0.35, 0.15, 0.17), 0.8), (36 * U, WORM, 1.0)):
        ctx.new_path(); smooth_open(ctx, pts); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, col, al * a); ctx.stroke()
    ctx.new_path(); smooth_open(ctx, pts[:10]); ctx.set_line_width(10 * U); rgba(ctx, (1.0, 0.75, 0.78), 0.6 * a); ctx.stroke()
    for k in range(2, 40, 2):                              # anneaux
        (x, y), an = bur_at(head_s + length * k / 40)
        nx, ny = -math.sin(an), math.cos(an)
        ctx.new_path(); ctx.move_to(x - nx * 16 * U, y - ny * 16 * U); ctx.line_to(x + nx * 16 * U, y + ny * 16 * U)
        ctx.set_line_width(3 * U); rgba(ctx, (0.55, 0.25, 0.30), 0.55 * a); ctx.stroke()
    (x, y), an = bur_at(head_s + length * 0.30)            # clitellum
    nx, ny = -math.sin(an), math.cos(an)
    ctx.new_path(); ctx.move_to(x - nx * 19 * U, y - ny * 19 * U); ctx.line_to(x + nx * 19 * U, y + ny * 19 * U); ctx.set_line_width(26 * U)
    rgba(ctx, (0.78, 0.36, 0.40), a); ctx.stroke()

def worm_scene(ctx, T, t0, t_grab, t1):
    """t0 : le ver sort ; t_grab : il saisit la feuille ; t1 : la feuille est dans la galerie."""
    cross_bg(ctx, T, night=True)
    ctx.new_path(); smooth_open(ctx, _BP); ctx.set_line_width(58 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.10, 0.06, 0.05), 0.9); ctx.stroke()
    if T < t_grab: head = lerp(H * 0.20, -W * 0.13, ease((T - t0) / max(0.1, t_grab - t0)))
    else: head = lerp(-W * 0.13, H * 0.17, ease((T - t_grab) / max(0.1, t1 - t_grab)))
    # la feuille (tirée par la pointe)
    lx0, ly0 = BUR_X - W * 0.20, SURF - 10 * U
    if T < t_grab:
        glow(ctx, lx0, ly0, 170 * U, GOLD, 0.25)
        draw_leaf(ctx, lx0, ly0, 230 * U, math.pi / 2, "beech", (0.86, 0.50, 0.20), 1.0)
    else:
        (hx, hy), an = bur_at(head - 10 * U)
        cx_, cy_ = hx - math.cos(an) * 115 * U, hy - math.sin(an) * 115 * U
        squeeze = 1.0 - 0.5 * clamp(head / (60 * U))         # la feuille se roule en entrant dans la galerie
        draw_leaf(ctx, cx_, cy_, 230 * U, an + math.pi / 2, "beech", (0.86, 0.50, 0.20), 1.0, flip=squeeze)
    earthworm(ctx, T, head)

# ---------------------------------------------------------------- plan D : acariens, collemboles, bactéries (loupe)
MG = (W * 0.46, H * 0.395); MR = W * 0.40
_RT = random.Random(31)
CRUMBS = [(_RT.uniform(-1, 1), _RT.uniform(-1, 1), _RT.uniform(6, 22), _RT.uniform(0, 1), _RT.choice(LEAF_COLS)) for _ in range(90)]
BAC = [(_RT.uniform(-0.8, 0.8), _RT.uniform(-0.8, 0.8), _RT.uniform(0, 6.28), _RT.uniform(0, 1)) for _ in range(70)]

def mite(ctx, x, y, s, ang, T):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    for sd in (-1, 1):
        for k in range(4):
            a0 = -0.9 + k * 0.6 + 0.15 * math.sin(T * 12 + k)
            ctx.new_path(); ctx.move_to(sd * s * 0.4, (k - 1.5) * s * 0.25); ctx.line_to(sd * s * (0.95 + 0.1 * k % 2), (k - 1.5) * s * 0.45 + a0 * s * 0.1)
            ctx.set_line_width(s * 0.07); rgba(ctx, (0.30, 0.12, 0.08), 1); ctx.stroke()
    ctx.save(); ctx.scale(1, 1.15); ctx.arc(0, 0, s * 0.5, 0, 2 * math.pi); ctx.restore()
    g = cairo.RadialGradient(-s * 0.15, -s * 0.2, s * 0.05, 0, 0, s * 0.6); g.add_color_stop_rgb(0, 0.85, 0.38, 0.22); g.add_color_stop_rgb(1, 0.45, 0.14, 0.08)
    ctx.set_source(g); ctx.fill()
    circle(ctx, 0, -s * 0.62, s * 0.18, (0.40, 0.14, 0.08), 1)
    ctx.restore()

def springtail(ctx, x, y, s, ang, T):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    for sd in (-1, 1):
        for k in range(3):
            ctx.new_path(); ctx.move_to(sd * s * 0.15, -s * 0.2 + k * s * 0.22); ctx.line_to(sd * s * 0.42, -s * 0.12 + k * s * 0.25)
            ctx.set_line_width(s * 0.06); rgba(ctx, (0.35, 0.32, 0.45), 1); ctx.stroke()
        ctx.new_path(); ctx.move_to(sd * s * 0.06, -s * 0.62); ctx.line_to(sd * s * 0.32, -s * 0.95); ctx.set_line_width(s * 0.05); ctx.stroke()
    ctx.new_path(); ctx.move_to(0, s * 0.55); ctx.line_to(-s * 0.08, s * 0.95); ctx.move_to(0, s * 0.55); ctx.line_to(s * 0.08, s * 0.95)   # fourche (saut)
    ctx.set_line_width(s * 0.05); rgba(ctx, (0.45, 0.42, 0.55), 1); ctx.stroke()
    ctx.save(); ctx.scale(0.32, 1.0); ctx.arc(0, 0, s * 0.62, 0, 2 * math.pi); ctx.restore()
    g = cairo.LinearGradient(-s * 0.2, 0, s * 0.2, 0); g.add_color_stop_rgb(0, 0.42, 0.40, 0.62); g.add_color_stop_rgb(1, 0.68, 0.66, 0.86)
    ctx.set_source(g); ctx.fill()
    circle(ctx, 0, -s * 0.58, s * 0.16, (0.30, 0.28, 0.42), 1)
    ctx.restore()

def micro_scene(ctx, T, k_mite, k_spring, k_shred, k_bact):
    soil_macro(ctx, T)
    rgba(ctx, (0, 0, 0), 0.35); ctx.paint()
    ctx.save(); ctx.new_path(); ctx.arc(MG[0], MG[1], MR, 0, 2 * math.pi); ctx.clip()
    g = cairo.RadialGradient(MG[0], MG[1], MR * 0.1, MG[0], MG[1], MR); g.add_color_stop_rgb(0, 0.33, 0.22, 0.15); g.add_color_stop_rgb(1, 0.17, 0.11, 0.08)
    ctx.set_source(g); ctx.paint()
    # gros fragment de feuille qui se réduit en miettes
    fk = 1 - 0.75 * k_shred
    draw_leaf(ctx, MG[0], MG[1] + MR * 0.05, MR * 1.25 * fk, 0.6, "oak", (0.80, 0.48, 0.20), 0.95 * (0.3 + 0.7 * fk), detail=True)
    for (cx_, cy_, r, t0, col) in CRUMBS:
        kk = clamp((k_shred - t0 * 0.7) / 0.3)
        if kk > 0: circle(ctx, MG[0] + cx_ * MR * 0.8, MG[1] + cy_ * MR * 0.8, r * U * ease(kk), mix(col, (0.25, 0.15, 0.08), 0.35), 0.95)
    if k_bact > 0:
        for (bx, by, an, t0) in BAC:
            kk = clamp((k_bact - t0 * 0.7) / 0.3)
            if kk <= 0: continue
            x, y = MG[0] + bx * MR, MG[1] + by * MR
            ctx.save(); ctx.translate(x, y); ctx.rotate(an + T * 0.5); s_ = ease(kk)
            rrect(ctx, -18 * U * s_, -7 * U * s_, 36 * U * s_, 14 * U * s_, 7 * U * s_); rgba(ctx, BACT, 0.9); ctx.fill(); ctx.restore()
    for i in range(3):                                     # acariens (marchent)
        if k_mite <= 0: break
        ang = T * 0.6 + i * 2.1
        x = MG[0] + MR * 0.45 * math.cos(ang); y = MG[1] + MR * 0.45 * math.sin(ang)
        mite(ctx, x, y, 70 * U * ease(k_mite), ang + math.pi, T)
    for i in range(3):                                     # collemboles (sautent)
        if k_spring <= 0: break
        ph = (T * 0.9 + i / 3) % 1.0
        x = MG[0] + MR * (-0.55 + 1.1 * ((i * 0.37 + T * 0.12) % 1.0))
        y = MG[1] + MR * (0.25 - 0.55 * i / 2) - 90 * U * math.sin(math.pi * min(1, ph * 3)) * (ph < 0.34)
        springtail(ctx, x, y, 80 * U * ease(k_spring), 0.4 * math.sin(T * 3 + i), T)
    ctx.restore()
    for w_, al in ((26 * U, 0.35), (12 * U, 1.0)):
        ctx.new_path(); ctx.arc(MG[0], MG[1], MR, 0, 2 * math.pi); ctx.set_line_width(w_); rgba(ctx, (0.85, 0.88, 0.95) if al == 1 else DARK, al); ctx.stroke()
    glow(ctx, MG[0] - MR * 0.45, MG[1] - MR * 0.55, MR * 0.35, WHITE, 0.10)

# ---------------------------------------------------------------- plan E : le carbone repart dans l'air (CO2)
_RB = random.Random(44)
BUBBLES = [(_RB.uniform(0.05, 0.85), _RB.uniform(0, 1), _RB.uniform(0.10, 0.22), _RB.uniform(14, 34), _RB.random() < 0.28) for _ in range(40)]
def co2_scene(ctx, T, k_c, k_air):
    forest(ctx, T, vanish=0.55, refill=0.0, fall_a=0.0)
    rgba(ctx, (0.05, 0.03, 0.10), 0.25); ctx.paint()
    if k_c > 0:                                          # points de carbone dans les feuilles
        rnd = random.Random(3)
        for i in range(60):
            x = rnd.uniform(0.05, 0.85) * W; y = HZ + (H * 0.72 - HZ) * rnd.random() ** 0.8
            circle(ctx, x, y, 7 * U * ease(k_c), (0.12, 0.10, 0.12), 0.9 * k_c); circle(ctx, x, y, 3 * U * ease(k_c), WHITE, 0.6 * k_c)
    for (bx, ph, sp, r, lab) in BUBBLES:
        if k_air <= 0: break
        u = (ph + T * sp) % 1.0
        y = H * 0.70 - u * H * 0.62; x = bx * W + 30 * U * math.sin(T * 1.5 + ph * 9)
        a = k_air * clamp(min(u * 5, (1 - u) * 4))
        rr = r * U * (1.3 if lab else 1.0)
        glow(ctx, x, y, rr * 2.4, CO2C, 0.35 * a)
        ctx.new_path(); ctx.arc(x, y, rr, 0, 2 * math.pi); rgba(ctx, CO2C, 0.25 * a); ctx.fill_preserve(); ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.8 * a); ctx.stroke()
        if lab and rr > 24 * U: text(ctx, "CO₂", x, y, rr * 0.75, WHITE, a)

# ---------------------------------------------------------------- plan F : l'humus nourrit les racines
ROOTS = []
_RR = random.Random(52)
def _roots():
    out = []
    for k in range(9):
        x0, y0 = W * 0.70 + _RR.uniform(-40, 40) * U, SURF + 30 * U
        ang = math.pi / 2 + _RR.uniform(-1.0, 1.0); pts = [(x0, y0)]
        for j in range(18):
            ang += _RR.uniform(-0.25, 0.25); st = _RR.uniform(25, 45) * U
            x0 += math.cos(ang) * st; y0 += math.sin(ang) * st * 0.8; pts.append((x0, y0))
        out.append(pts)
    return out
ROOTS = _roots()
def soil_scene(ctx, T, k_h, k_feed):
    cross_bg(ctx, T, night=False, humus=k_h)
    # tronc (à droite)
    tx = W * 0.70
    g = cairo.LinearGradient(tx - W * 0.09, 0, tx + W * 0.09, 0); g.add_color_stop_rgb(0, 0.40, 0.41, 0.39); g.add_color_stop_rgb(0.6, *BARK); g.add_color_stop_rgb(1, 0.32, 0.33, 0.31)
    ctx.set_source(g); ctx.rectangle(tx - W * 0.09, 0, W * 0.18, SURF + 40 * U); ctx.fill()
    for pts in ROOTS:
        for w_, col, al in ((22 * U, (0.25, 0.17, 0.11), 1.0), (12 * U, (0.55, 0.40, 0.27), 1.0)):
            ctx.new_path(); smooth_open(ctx, pts); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, al); ctx.stroke()
    if k_feed > 0:                                       # nutriments qui remontent par les racines
        for i, pts in enumerate(ROOTS):
            L = _poly_len(pts)
            for j in range(3):
                s = (1 - ((T * 0.55 + j / 3 + i * 0.13) % 1.0)) * L[-1]
                for q in range(1, len(L)):
                    if L[q] >= s:
                        u = (s - L[q - 1]) / max(1e-6, L[q] - L[q - 1]); x = lerp(pts[q - 1][0], pts[q][0], u); y = lerp(pts[q - 1][1], pts[q][1], u)
                        glow(ctx, x, y, 26 * U, GOLD, 0.55 * k_feed); circle(ctx, x, y, 8 * U, (1.0, 0.95, 0.7), k_feed); break
        for j in range(5):
            y = SURF - ((T * 0.4 + j / 5) % 1.0) * SURF
            glow(ctx, tx, y, 30 * U, GOLD, 0.45 * k_feed); circle(ctx, tx, y, 8 * U, (1.0, 0.95, 0.7), k_feed)

# ---------------------------------------------------------------- montage
T_VAN0, T_VAN1 = WT("vanish", 0) - 0.25, WT("vanish", 0) + 1.20     # les feuilles disparaissent (« Then the leaves vanish too »)
T_B0 = SENT("fungi", 0) - 0.08
T_C0 = SENT("worms", 0) - 0.08
T_D0 = SENT("tiny", 0) - 0.08
T_E0 = SENT("air", 0) - 0.08
T_F0 = SENT("close", 0) - 0.08
T_G0 = SENT("close", 1) - 0.08
T_CTA = END_T - 2.5

def master(ctx, T):
    if T < T_B0:                                         # A — le tapis de feuilles, puis il disparaît
        van = prog(T, T_VAN0, T_VAN1)
        forest(ctx, T, vanish=van, fall_a=1.0 - 0.7 * van)
        kq = 1.0 - prog(T, T_B0 - 0.25, T_B0)
        poster_text(ctx, "WHERE'D", W * 0.46, H * 0.120, 150 * U, WHITE, W * 0.80)
        poster_text(ctx, "THEY GO?", W * 0.46, H * 0.185, 150 * U, GOLD, W * 0.80)
        if T > 1.2: tag(ctx, "Illustration", 0.240)
    elif T < T_C0:                                       # B — « They get eaten. Fungi… »
        soil_macro(ctx, T)
        k_bite = prog(T, WT("eaten") - 0.20, WT("eaten") + 0.25)
        k_grow = prog(T, WT("fungi") - 0.10, WT("digest") + 0.30)
        k_dig = prog(T, WT("digest") - 0.30, T_C0 + 0.05)
        fungi_leaf(ctx, T, k_bite, k_grow, k_dig)
        for j, (mx, sz) in enumerate(((0.16, 120), (0.24, 85), (0.74, 105))):
            mushroom(ctx, mx * W, H * 0.66, sz * U, prog(T, WT("threads") + j * 0.15, WT("threads") + 0.4 + j * 0.15))
        pill(ctx, "FUNGI", W * 0.46, H * 0.105, (0.95, 0.94, 0.86), 54, 1.0, prog(T, WT("fungi") - 0.1, WT("fungi") + 0.25))
        tag(ctx, "Illustration")
    elif T < T_D0:                                       # C — le ver tire une feuille
        worm_scene(ctx, T, T_C0, WT("drag") - 0.10, WT("burrows") + 0.30)
        kl = prog(T, WT("earthworms") - 0.1, WT("earthworms") + 0.25)
        (hx, hy), _ = bur_at(H * 0.12)
        leader(ctx, W * 0.72, H * 0.43, hx + 30 * U, hy, WORM, 1.0, kl)
        pill(ctx, "EARTHWORM", W * 0.72, H * 0.40, WORM, 48, 1.0, kl)
        tag(ctx, "Simplified illustration")
    elif T < T_E0:                                       # D — à la loupe
        k_m = prog(T, WT("mites") - 0.1, WT("mites") + 0.3); k_s = prog(T, WT("springtails") - 0.1, WT("springtails") + 0.3)
        k_sh = prog(T, WT("shred") - 0.1, WT("bacteria") + 0.2); k_b = prog(T, WT("bacteria") - 0.1, WT("job") + 0.3)
        micro_scene(ctx, T, k_m, k_s, k_sh, k_b)
        pill(ctx, "MITES", W * 0.20, H * 0.105, (0.85, 0.38, 0.22), 44, 1.0, k_m)
        pill(ctx, "SPRINGTAILS", W * 0.60, H * 0.105, (0.68, 0.66, 0.90), 44, 1.0, k_s)
        pill(ctx, "BACTERIA", W * 0.46, H * 0.66, BACT, 48, 1.0, k_b)
        tag(ctx, "Simplified illustration", 0.150)
    elif T < T_F0:                                       # E — CO2 dans l'air
        k_c = prog(T, WT("carbon") - 0.1, WT("carbon") + 0.3) * (1 - prog(T, WT("air") - 0.1, WT("air") + 0.4) * 0.8)
        k_a = prog(T, WT("air") - 0.2, WT("air") + 0.3)
        co2_scene(ctx, T, k_c, k_a)
        kd = prog(T, WT("dioxide") - 0.3, WT("dioxide") + 0.1)
        if kd > 0:
            glow(ctx, W * 0.46, H * 0.16, W * 0.30, CO2C, 0.35 * kd)
            poster_text(ctx, "CO₂", W * 0.46, H * 0.16, 190 * U * (0.7 + 0.3 * ease(kd)), CO2C)
        tag(ctx, "Simplified illustration")
    elif T < T_G0:                                       # F — l'humus nourrit les arbres
        k_h = prog(T, WT("soil") - 0.4, WT("soil") + 0.4); k_f = prog(T, WT("feeds") - 0.2, WT("trees") + 0.2)
        soil_scene(ctx, T, k_h, k_f)
        kl = prog(T, WT("soil") - 0.1, WT("soil") + 0.25)
        leader(ctx, W * 0.24, H * 0.455, W * 0.30, SURF + H * 0.04, (0.95, 0.80, 0.55), 1.0, kl)
        pill(ctx, "SOIL", W * 0.24, H * 0.48, (0.95, 0.80, 0.55), 52, 1.0, kl)
        tag(ctx, "Simplified illustration")
    else:                                                # G — « The forest eats its own leaves. » : les feuilles retombent (boucle)
        rf = prog(T, T_G0, END_T - 0.3)
        forest(ctx, T, vanish=1.0, refill=rf, fall_a=1.0)
        tag(ctx, "Illustration")
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            font(ctx, 46 * U); txt = "FACTORA"
            w_ = ctx.text_extents(txt).width + 60 * U
            rrect(ctx, W * 0.46 - w_ / 2, H * 0.130 - 34 * U, w_, 68 * U, 34 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
            text(ctx, txt, W * 0.46, H * 0.130, 46 * U, GOLD, kc)
            cta_lines(ctx, ("Follow Factora for more", "nature mysteries."), W * 0.46, (H * 0.172, H * 0.204), 54, kc)

T_COVER = 0.40
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t

def sc_hook(ctx, t, d): master(ctx, _abs_t("hook", t))
def sc_fungi(ctx, t, d): master(ctx, _abs_t("fungi", t))
def sc_worms(ctx, t, d): master(ctx, _abs_t("worms", t))
def sc_tiny(ctx, t, d): master(ctx, _abs_t("tiny", t))
def sc_air(ctx, t, d): master(ctx, _abs_t("air", t))
def sc_close(ctx, t, d): master(ctx, _abs_t("close", t))

SHORT_SCENES = ["hook", "fungi", "worms", "tiny", "air", "close"]
SCENES = dict(hook=sc_hook, fungi=sc_fungi, worms=sc_worms, tiny=sc_tiny, air=sc_air, close=sc_close)

def cover(ctx):
    """Miniature / affiche (demande de Nazik, 2026-11-22 : « fais-moi la miniature ») : le tapis de feuilles de l'image 1,
    une grande feuille de hêtre mordue au premier plan (l'indice, sans la réponse), la question et un bandeau d'action ;
    tout l'essentiel entre 14 % et 86 % de la hauteur (grilles 3:4 d'Instagram et TikTok)."""
    forest(ctx, T_COVER)
    g = cairo.LinearGradient(0, 0, 0, H * 0.34); g.add_color_stop_rgba(0, 0.02, 0.01, 0.01, 0.65); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.34); ctx.fill()
    cx, cy, L, ang = W * 0.47, H * 0.515, H * 0.36, 0.30
    glow(ctx, cx, cy, L * 0.75, (1.0, 0.75, 0.35), 0.45)
    ctx.save(); ctx.translate(cx + 18 * U, cy + 26 * U); ctx.rotate(ang); ctx.scale(L * 1.04, L * 1.04); ctx.new_path(); leaf_path(ctx, "beech"); ctx.restore()
    rgba(ctx, (0.04, 0.02, 0.01), 0.80); ctx.fill()                 # ombre portée : les morsures ressortent en sombre
    ctx.push_group()
    draw_leaf(ctx, cx, cy, L, ang, "beech", (0.90, 0.52, 0.20), 1.0, detail=True)
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang)
    for (bx, by, r) in ((0.24, -0.13, 0.115), (0.22, 0.10, 0.095), (-0.24, 0.22, 0.10)):
        for j in range(4):
            circle(ctx, bx * L + math.cos(j * 1.6) * r * L * 0.5, by * L + math.sin(j * 1.6) * r * L * 0.5, r * L * 0.55, WHITE, 1)
    ctx.restore(); ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()
    poster_text(ctx, "WHERE'D", W * 0.47, H * 0.175, 165 * U, WHITE, W * 0.86)
    poster_text(ctx, "THEY GO?", W * 0.47, H * 0.250, 175 * U, GOLD, W * 0.86)
    red_arrow(ctx, W * 0.86, H * 0.36, W * 0.66, H * 0.445, bend=-0.30, width=24)
    font(ctx, 66 * U); txt = "WHO ATE THIS LEAF?"; w_ = ctx.text_extents(txt).width + 80 * U; h_ = 120 * U
    y_ = H * 0.775
    glow(ctx, W * 0.47, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.47 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.47, y_, 66 * U, DARK)
