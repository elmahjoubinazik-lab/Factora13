exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Épisode 046 (Short seul, 9:16, ~32 s) — « How Can Owls Turn Their Heads So Far? » (Animal Mystery).
# Stratégie 30 jours validée par Nazik le 2026-11-22, semaine 1 = test de l'IMAGE 1 : l'animal EN ACTION en plein cadre
# dès la 1re image (la tête de la chouette déjà en train de tourner), au plus 3 mots à l'écran pendant la 1re seconde
# (« 270° » + petite pastille « ANIMAL MYSTERY ») ; dessins 100 % faits ici ; un nouveau plan toutes les ~5 s ;
# fin = la tête revient à la pose de l'image 1 (boucle) ; CTA texte « Follow Factora for more animal mysteries. ».
# Faits (Johns Hopkins, étude de 2013 sur des chouettes harfang, rayées et grands-ducs d'Amérique : NPR 2013-01-31,
# ScienceDaily 2013-01-31, Smithsonian) : rotation de la tête jusqu'à ≈ 270° ; 14 vertèbres cervicales (humain : 7) ;
# les trous des vertèbres où passe l'artère vertébrale sont ≈ 10 fois plus larges que l'artère (coussin d'air, l'artère
# peut bouger) ; à la base de la tête, les vaisseaux s'élargissent en réservoirs qui gardent du sang pour le cerveau et
# les yeux pendant la rotation ; chez l'humain, une torsion brutale du cou peut déchirer la paroi des artères (titre
# NPR : « How owls spin their heads without tearing arteries »). Yeux tubulaires fixés dans le crâne (anneaux
# sclérotiques) : la chouette ne peut pas les faire rouler. Les schémas sont signalés « Simplified illustration ».
import json as _json

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
def WT(word, n=0):
    """Début (temps absolu de la vidéo) de la n-ième occurrence du mot prononcé."""
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def SENT(scene, i=0): return _TL[scene]["sents"][i]["start"]
END_T = _TLL[-1]["end"] + 0.6                    # fin de la vidéo (render.py : fin de la voix + 0,6 s)

DARK = (0.03, 0.02, 0.08)
FEATH = (0.52, 0.37, 0.23)
FEATH_D = (0.20, 0.13, 0.08)
FEATH_L = (0.86, 0.74, 0.56)
DISC = (0.90, 0.58, 0.31)
RIM = (0.14, 0.08, 0.05)
BIB = (0.97, 0.94, 0.87)
IRIS = (1.0, 0.76, 0.10)
BEAKC = (0.23, 0.22, 0.26)
ART = (1.0, 0.24, 0.30)
BONE = (0.95, 0.88, 0.72)
BRAIN = (1.0, 0.56, 0.72)
MOONL = (0.72, 0.86, 1.0)
NAVF = (0.07, 0.10, 0.23)

def lerp(a, b, k): return a + (b - a) * k

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

def F(pts): return [(x * W, y * H) for x, y in pts]

# ---------------------------------------------------------------- textes (peu de mots)
def tag(ctx, s, y=0.083, a=1.0):
    """Mention discrète en haut à gauche (« Illustration » / « Simplified illustration »)."""
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def series_pill(ctx, a=1.0):
    if a <= 0: return
    s = "ANIMAL MYSTERY"; font(ctx, 30 * U); w_ = ctx.text_extents(s).width + 44 * U
    x0, y0 = W * 0.055, H * 0.060
    rrect(ctx, x0, y0 - 24 * U, w_, 48 * U, 24 * U); rgba(ctx, GOLD, 0.95 * a); ctx.fill()
    text(ctx, s, x0 + 22 * U, y0, 30 * U, DARK, a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, DARK, a)
    ctx.restore()

def label_box(ctx, s, x, y, col=GOLD, size=50, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    sc_ = 0.7 + 0.3 * ease(k)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 56 * U; h_ = size * 1.55 * U
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 22 * U); rgba(ctx, (0.02, 0.03, 0.09), 0.88 * a * ease(k)); ctx.fill()
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 22 * U); ctx.set_line_width(4.5 * U); rgba(ctx, col, a * ease(k)); ctx.stroke()
    text(ctx, s, 0, 0, size * U, col, a * ease(k))
    ctx.restore()

def leader(ctx, x0, y0, x1, y1, col, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    xe, ye = x0 + (x1 - x0) * ease(k), y0 + (y1 - y0) * ease(k)
    for w_, al, c_ in ((9 * U, 0.35, DARK), (4.5 * U, 1.0, col)):
        ctx.new_path(); ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        rgba(ctx, c_, al * a); ctx.stroke()
    if k > 0.95: circle(ctx, x1, y1, 11 * U, col, a); circle(ctx, x1, y1, 5 * U, WHITE, a)

def arrowhead(ctx, x, y, ang, col, size, a=1.0):
    ctx.new_path(); ctx.move_to(x + math.cos(ang) * size * 0.6, y + math.sin(ang) * size * 0.6)
    ctx.line_to(x + math.cos(ang + 2.5) * size, y + math.sin(ang + 2.5) * size)
    ctx.line_to(x + math.cos(ang - 2.5) * size, y + math.sin(ang - 2.5) * size); ctx.close_path()
    rgba(ctx, DARK, 0.6 * a); ctx.set_line_width(5 * U); ctx.stroke_preserve(); rgba(ctx, col, a); ctx.fill()

def red_x(ctx, x, y, r, a=1.0, k=1.0):
    if a <= 0 or k <= 0: return
    rr = r * (0.6 + 0.4 * ease(k) + 0.15 * math.sin(math.pi * clamp(k)))
    glow(ctx, x, y, rr * 2.2, CORAL, 0.35 * a)
    for (dx, dy) in ((1, 1), (1, -1)):
        for w_, c_, al in ((r * 0.42, DARK, 0.7), (r * 0.26, (1.0, 0.18, 0.20), 1.0)):
            ctx.new_path(); ctx.move_to(x - dx * rr * 0.7, y - dy * rr * 0.7); ctx.line_to(x + dx * rr * 0.7, y + dy * rr * 0.7)
            ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c_, al * a); ctx.stroke()

def cta_lines(ctx, lines, x, ys, size, a):
    """Texte contouré comme les sous-titres ; 1re ligne blanche, 2e or."""
    sz = size * U; maxw = W * 0.74
    cap_font(ctx, sz)
    widest = max(ctx.text_extents(l).width for l in lines)
    if widest > maxw: sz *= maxw / widest; cap_font(ctx, sz)
    for l, y, col in zip(lines, ys, (WHITE, GOLD)):
        e = ctx.text_extents(l); x0 = x - e.width / 2 - e.x_bearing; y0 = y + sz * 0.35
        ctx.move_to(x0 + 3 * U, y0 + 5 * U); ctx.text_path(l); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
        ctx.move_to(x0, y0); ctx.text_path(l); ctx.set_line_width(sz * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, (0.01, 0.02, 0.06), a); ctx.stroke_preserve(); rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- fond de nuit (pré-calculé)
def _build_night():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W), int(H)); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.08, 0.06, 0.24); g.add_color_stop_rgb(0.45, 0.05, 0.08, 0.22); g.add_color_stop_rgb(1, 0.01, 0.02, 0.06)
    c.set_source(g); c.paint()
    mx, my = W * 0.83, H * 0.205
    glow(c, mx, my, W * 0.70, (0.40, 0.50, 0.95), 0.30)
    glow(c, mx, my, W * 0.22, (0.85, 0.90, 1.0), 0.40)
    circle(c, mx, my, W * 0.058, (0.97, 0.96, 0.90), 1.0)
    for (dx, dy, r) in ((-0.018, -0.012, 0.012), (0.016, 0.010, 0.009), (0.004, 0.024, 0.006)):
        circle(c, mx + dx * W, my + dy * W, r * W, (0.85, 0.84, 0.78), 0.55)
    rnd = random.Random(3)
    for i in range(170):
        x, y = rnd.random() * W, rnd.random() * H * 0.55
        circle(c, x, y, rnd.uniform(1.0, 2.6) * U, WHITE, rnd.uniform(0.25, 0.85))
    # forêt lointaine (deux rangs de silhouettes douces)
    for col, a, base, hmin, hmax, seed in (((0.10, 0.13, 0.32), 0.80, 0.60, 0.12, 0.24, 5), ((0.05, 0.07, 0.19), 0.95, 0.70, 0.08, 0.18, 9)):
        r2 = random.Random(seed); x = -60.0
        while x < W + 60:
            w = r2.uniform(0.08, 0.15) * W; h = r2.uniform(hmin, hmax) * H
            c.save(); c.translate(x, base * H - h * 0.55); c.scale(w / 2, h / 2); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            rgba(c, col, a); c.fill()
            c.rectangle(x - w * 0.05, base * H - h * 0.25, w * 0.10, H); rgba(c, col, a); c.fill()
            x += w * 0.72
    g2 = cairo.LinearGradient(0, H * 0.55, 0, H); g2.add_color_stop_rgba(0, 0.02, 0.03, 0.09, 0.0); g2.add_color_stop_rgba(1, 0.01, 0.015, 0.05, 0.96)
    c.set_source(g2); c.paint()
    return s
_NIGHT = _build_night()
_FF = [(random.Random(40 + i).random(), random.Random(80 + i).random(), random.Random(120 + i).uniform(0.4, 1.0)) for i in range(14)]

def night_bg(ctx, T):
    ctx.set_source_surface(_NIGHT, 0, 0); ctx.paint()
    for i, (fx, fy, sp) in enumerate(_FF):     # lucioles : mouvement permanent
        x = (fx * W + 30 * U * math.sin(T * sp + i)) % W; y = H * (0.30 + 0.38 * fy) + 24 * U * math.sin(T * sp * 1.3 + i * 2)
        a = 0.45 + 0.35 * math.sin(T * 2.2 + i)
        glow(ctx, x, y, 26 * U, GOLD, 0.30 * a); circle(ctx, x, y, 4 * U, (1.0, 0.92, 0.55), a)

# ---------------------------------------------------------------- branche
BR_Y = H * 0.668
_RB = random.Random(21)
BARK = [(_RB.uniform(-0.05, 1.05) * W, BR_Y + _RB.uniform(-34, 30) * U, _RB.uniform(40, 120) * U, _RB.uniform(-0.06, 0.06)) for _ in range(46)]
def branch(ctx, T):
    top = [(-60, BR_Y - 48 * U), (W * 0.3, BR_Y - 42 * U), (W * 0.62, BR_Y - 46 * U), (W + 60, BR_Y - 36 * U)]
    bot = [(W + 60, BR_Y + 40 * U), (W * 0.62, BR_Y + 36 * U), (W * 0.3, BR_Y + 42 * U), (-60, BR_Y + 38 * U)]
    ctx.new_path(); smooth_open(ctx, top); ctx.line_to(*bot[0]); smooth_open(ctx, bot); ctx.close_path()
    g = cairo.LinearGradient(0, BR_Y - 48 * U, 0, BR_Y + 42 * U); g.add_color_stop_rgb(0, 0.36, 0.25, 0.16); g.add_color_stop_rgb(1, 0.10, 0.07, 0.05)
    ctx.set_source(g); ctx.fill()
    for (x, y, l, s) in BARK:
        ctx.new_path(); ctx.move_to(x, y); ctx.curve_to(x + l * 0.3, y + l * s - 4 * U, x + l * 0.7, y + l * s + 4 * U, x + l, y + l * s * 2)
        ctx.set_line_width(4 * U); rgba(ctx, (0.06, 0.04, 0.03), 0.55); ctx.stroke()
    ctx.new_path(); smooth_open(ctx, top); ctx.set_line_width(5 * U); rgba(ctx, MOONL, 0.45); ctx.stroke()

def foreground(ctx, T):
    g = cairo.LinearGradient(0, H * 0.70, 0, H); g.add_color_stop_rgba(0, 0.01, 0.015, 0.04, 0.0); g.add_color_stop_rgba(1, 0.0, 0.0, 0.02, 0.9)
    ctx.set_source(g); ctx.rectangle(0, H * 0.70, W, H * 0.30); ctx.fill()

# ---------------------------------------------------------------- chouette (grand-duc d'Amérique, face) ; tête « sphérique »
HC = (W * 0.46, H * 0.345)
RX, RY = W * 0.285, W * 0.238
BODYF = [(0.46, 0.405), (0.62, 0.415), (0.74, 0.445), (0.81, 0.50), (0.84, 0.56), (0.83, 0.615), (0.78, 0.655), (0.68, 0.680),
         (0.46, 0.690), (0.24, 0.680), (0.14, 0.655), (0.09, 0.615), (0.08, 0.56), (0.11, 0.50), (0.18, 0.445), (0.30, 0.415)]
WINGL = [(0.20, 0.44), (0.12, 0.50), (0.09, 0.57), (0.10, 0.63), (0.15, 0.675), (0.26, 0.692), (0.30, 0.62), (0.29, 0.53), (0.26, 0.47)]
WINGR = [(0.92 - x, y) for x, y in WINGL]
_RO = random.Random(7)
BARS = []
for i in range(15):
    yy = 0.500 + i * 0.0118
    xx = 0.26 + _RO.uniform(0, 0.03)
    while xx < 0.66:
        BARS.append((xx, yy + _RO.uniform(-0.003, 0.003), _RO.uniform(0.020, 0.034), _RO.uniform(0.6, 1.0))); xx += _RO.uniform(0.038, 0.052)
SPOTS = []                                       # taches de la tête, fixées à la tête : (longitude, latitude, longueur, teinte)
while len(SPOTS) < 360:
    a_ = _RO.uniform(-math.pi, math.pi); la = math.asin(_RO.uniform(-0.80, 0.97))
    fc = math.acos(max(-1, min(1, math.cos(a_) * math.cos(la + 0.06))))
    if fc < 1.10: continue                       # la face (disque facial) est dessinée à part
    SPOTS.append((a_, la, _RO.uniform(16, 36) * U, _RO.random()))
FUZZ = [1 + 0.018 * math.sin(k * 7.0) + 0.012 * math.sin(k * 13.0 + 1.0) for k in range(96)]

def V(a, lat, th, r=1.0):
    """Point de la tête (longitude a relative à la face, latitude lat) → (x, y écran, profondeur z)."""
    lon = a + th
    return (HC[0] + RX * math.sin(lon) * math.cos(lat) * r, HC[1] - RY * math.sin(lat) * r, math.cos(lon) * math.cos(lat))

def cap_pts(a0, lat0, th, rho, n=64, r=1.0):
    """Contour d'une calotte (centre a0, lat0 ; rayon angulaire rho) projeté ; les points cachés sont ramenés sur le bord."""
    lon = a0 + th
    f = (math.sin(lon) * math.cos(lat0), math.sin(lat0), math.cos(lon) * math.cos(lat0))
    e1 = (math.cos(lon), 0.0, -math.sin(lon))
    e2 = (-math.sin(lon) * math.sin(lat0), math.cos(lat0), -math.cos(lon) * math.sin(lat0))
    out = []
    for k in range(n):
        ps = 2 * math.pi * k / n
        p = [math.cos(rho) * f[j] + math.sin(rho) * (math.cos(ps) * e1[j] + math.sin(ps) * e2[j]) for j in range(3)]
        if p[2] < 0:
            l = math.hypot(p[0], p[1]) + 1e-9; p = [p[0] / l, p[1] / l, 0.0]
        out.append((HC[0] + RX * p[0] * r, HC[1] - RY * p[1] * r))
    return out, f[2]

def head_path(c):
    pts = [(HC[0] + RX * FUZZ[k] * math.cos(2 * math.pi * k / 96), HC[1] + RY * FUZZ[k] * math.sin(2 * math.pi * k / 96)) for k in range(96)]
    smooth_closed(c, pts)

def tuft(ctx, th, side, behind):
    a0 = 0.52 * side; bx, by, z = V(a0, 0.80, th)
    if (z < 0) != behind: return
    ox = (bx - HC[0]) / RX
    ang = -math.pi / 2 + 0.55 * ox                 # penche vers l'extérieur
    L, Wd = 170 * U, 64 * U
    tip = (bx + math.cos(ang) * L, by + math.sin(ang) * L)
    nx, ny = -math.sin(ang), math.cos(ang)
    pts = [(bx - nx * Wd * 0.6, by - ny * Wd * 0.6), (bx + math.cos(ang) * L * 0.55 - nx * Wd * 0.45, by + math.sin(ang) * L * 0.55 - ny * Wd * 0.45),
           tip, (bx + math.cos(ang) * L * 0.5 + nx * Wd * 0.35, by + math.sin(ang) * L * 0.5 + ny * Wd * 0.35), (bx + nx * Wd * 0.6, by + ny * Wd * 0.6)]
    ctx.new_path(); smooth_open(ctx, pts); ctx.close_path()
    rgba(ctx, mix(FEATH_D, FEATH, 0.35), 0.75 if behind else 1.0); ctx.fill_preserve()
    rgba(ctx, MOONL, 0.18); ctx.set_line_width(3 * U); ctx.stroke()
    for k in range(3):
        u = 0.3 + 0.2 * k
        ctx.new_path(); ctx.move_to(bx + math.cos(ang) * L * u, by + math.sin(ang) * L * u)
        ctx.line_to(bx + math.cos(ang) * L * (u + 0.15) + nx * Wd * 0.2, by + math.sin(ang) * L * (u + 0.15) + ny * Wd * 0.2)
        ctx.set_line_width(3.5 * U); rgba(ctx, FEATH_L, 0.45); ctx.stroke()

def owl_body(ctx, T):
    br = 1 + 0.007 * math.sin(T * 2.3)
    ctx.save(); ctx.translate(W * 0.46, H * 0.69); ctx.scale(br, br); ctx.translate(-W * 0.46, -H * 0.69)
    # queue sous la branche
    ctx.new_path(); smooth_closed(ctx, F([(0.40, 0.676), (0.52, 0.676), (0.54, 0.722), (0.46, 0.732), (0.38, 0.722)])); rgba(ctx, FEATH_D, 1); ctx.fill()
    body = F(BODYF)
    ctx.new_path(); smooth_closed(ctx, body)
    g = cairo.RadialGradient(W * 0.52, H * 0.50, W * 0.05, W * 0.46, H * 0.56, W * 0.48)
    g.add_color_stop_rgb(0, *mix(FEATH, FEATH_L, 0.35)); g.add_color_stop_rgb(1, *mix(FEATH, FEATH_D, 0.45))
    ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); smooth_closed(ctx, body); ctx.clip()
    # plastron clair et barré
    ctx.save(); ctx.translate(W * 0.46, H * 0.57); ctx.scale(W * 0.20, H * 0.115); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    g2 = cairo.RadialGradient(W * 0.46, H * 0.55, 0, W * 0.46, H * 0.57, W * 0.22)
    g2.add_color_stop_rgba(0, *FEATH_L, 0.95); g2.add_color_stop_rgba(1, *FEATH_L, 0.0); ctx.set_source(g2); ctx.fill()
    for (x, y, l, s) in BARS:
        ctx.new_path(); ctx.move_to(x * W, y * H); ctx.curve_to((x + l * 0.3) * W, y * H - 7 * U, (x + l * 0.7) * W, y * H - 7 * U, (x + l) * W, y * H)
        ctx.set_line_width(6 * U); rgba(ctx, FEATH_D, 0.70 * s); ctx.stroke()
    # ailes repliées
    for wing, sd in ((WINGL, -1), (WINGR, 1)):
        ctx.new_path(); smooth_closed(ctx, F(wing))
        g3 = cairo.LinearGradient(W * (0.46 + sd * 0.25), H * 0.45, W * (0.46 + sd * 0.38), H * 0.66)
        g3.add_color_stop_rgb(0, *mix(FEATH, FEATH_D, 0.35)); g3.add_color_stop_rgb(1, *FEATH_D); ctx.set_source(g3); ctx.fill()
        for row in range(4):
            for j in range(5):
                x = (0.46 + sd * (0.205 + 0.028 * j + 0.004 * row)) * W; y = (0.53 + 0.035 * row + 0.006 * j) * H
                ctx.new_path(); ctx.arc(x, y, 26 * U, 0.15 * math.pi, 0.85 * math.pi); ctx.set_line_width(4.5 * U); rgba(ctx, FEATH_L, 0.30); ctx.stroke()
    ctx.restore()
    ctx.new_path(); smooth_closed(ctx, body); ctx.set_line_width(5 * U); rgba(ctx, MOONL, 0.16); ctx.stroke()
    # plastron blanc sous la tête
    ctx.save(); ctx.translate(W * 0.46, H * 0.488); ctx.scale(W * 0.13, H * 0.030); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, BIB, 0.95); ctx.fill()
    ctx.restore()
    # pattes emplumées et serres sur la branche
    for fx in (0.39, 0.53):
        x = fx * W; y = H * 0.648
        ctx.save(); ctx.translate(x, y); ctx.scale(W * 0.050, H * 0.020); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        rgba(ctx, FEATH_L, 1); ctx.fill()
        for k in (-1, 0, 1):
            tx = x + k * 34 * U
            ctx.new_path(); ctx.move_to(tx, y + 10 * U); ctx.curve_to(tx + 6 * U, y + 30 * U, tx + 4 * U, y + 52 * U, tx - 12 * U, y + 60 * U)
            ctx.set_line_width(11 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.08, 0.07, 0.08), 1); ctx.stroke()

def owl_head(ctx, T, th, blink=0.0):
    tuft(ctx, th, -1, True); tuft(ctx, th, 1, True)
    # base de la tête
    ctx.new_path(); head_path(ctx)
    g = cairo.RadialGradient(HC[0] + RX * 0.35, HC[1] - RY * 0.40, RX * 0.1, HC[0], HC[1], RX * 1.15)
    g.add_color_stop_rgb(0, *mix(FEATH, FEATH_L, 0.30)); g.add_color_stop_rgb(1, *mix(FEATH, FEATH_D, 0.40))
    ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); head_path(ctx); ctx.clip()
    # taches (tournent avec la tête)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for (a_, la, l, s) in SPOTS:
        x, y, z = V(a_, la, th)
        if z <= 0.02: continue
        sx = max(0.25, abs(z) ** 0.5)
        col = FEATH_D if s < 0.62 else FEATH_L
        ctx.new_path(); ctx.move_to(x, y - l * 0.5); ctx.line_to(x + 3 * U * sx, y + l * 0.5)
        ctx.set_line_width(7 * U * sx); rgba(ctx, col, min(1.0, z * 3.0) * (0.75 if s < 0.62 else 0.55)); ctx.stroke()
    # disque facial
    disc, fz = cap_pts(0.0, -0.06, th, 1.02)
    if fz > -0.55:
        ctx.new_path(); smooth_closed(ctx, disc)
        fx_, fy_, _ = V(0.0, -0.06, th)
        g = cairo.RadialGradient(fx_, fy_, RX * 0.05, fx_, fy_, RX * 0.95)
        g.add_color_stop_rgb(0, *mix(DISC, FEATH_L, 0.25)); g.add_color_stop_rgb(1, *mix(DISC, FEATH, 0.35))
        ctx.set_source(g); ctx.fill_preserve()
        ctx.set_line_width(11 * U); rgba(ctx, RIM, 0.80); ctx.stroke()
        for sd in (-1, 1):                       # zones claires autour des yeux
            ex, ey, ez = V(0.40 * sd, 0.04, th)
            if ez > 0.06:
                pale, _ = cap_pts(0.40 * sd, 0.02, th, 0.40)
                ctx.new_path(); smooth_closed(ctx, pale); rgba(ctx, mix(DISC, FEATH_L, 0.55), 0.55); ctx.fill()
        c0 = V(0.0, 0.55, th); c1 = V(0.0, 0.02, th)
        if min(c0[2], c1[2]) > 0.05:
            ctx.new_path(); ctx.move_to(c0[0], c0[1]); ctx.line_to(c1[0], c1[1]); ctx.set_line_width(12 * U); rgba(ctx, mix(DISC, RIM, 0.5), 0.7); ctx.stroke()
        # sourcils clairs en V
        for sd in (-1, 1):
            p0 = V(0.06 * sd, 0.10, th); p1 = V(0.42 * sd, 0.30, th)
            if min(p0[2], p1[2]) > 0.05:
                ctx.new_path(); ctx.move_to(p0[0], p0[1]); ctx.curve_to(lerp(p0[0], p1[0], 0.4), p0[1] - 30 * U, lerp(p0[0], p1[0], 0.8), p1[1], p1[0], p1[1])
                ctx.set_line_width(20 * U * min(1, p0[2] * 2)); rgba(ctx, BIB, 0.85); ctx.stroke()
        # yeux
        for sd in (-1, 1):
            ex, ey, ez = V(0.40 * sd, 0.04, th)
            if ez < 0.06: continue
            ring, _ = cap_pts(0.40 * sd, 0.04, th, 0.262)
            ctx.new_path(); smooth_closed(ctx, ring); rgba(ctx, RIM, 1); ctx.fill()
            iris, _ = cap_pts(0.40 * sd, 0.04, th, 0.232)
            ctx.new_path(); smooth_closed(ctx, iris)
            gi = cairo.RadialGradient(ex, ey, 0, ex, ey, RX * 0.22)
            gi.add_color_stop_rgb(0, 1.0, 0.92, 0.45); gi.add_color_stop_rgb(1, *IRIS); ctx.set_source(gi); ctx.fill()
            pup, _ = cap_pts(0.40 * sd, 0.04, th, 0.115)
            ctx.new_path(); smooth_closed(ctx, pup); rgba(ctx, (0.02, 0.01, 0.02), 1); ctx.fill()
            circle(ctx, ex + RX * 0.045 * ez, ey - RY * 0.06, RX * 0.032 * ez, WHITE, 0.9)
            if blink > 0:                       # paupière
                ctx.save(); ctx.new_path(); smooth_closed(ctx, ring); ctx.clip()
                ctx.rectangle(ex - RX * 0.4, ey - RY * 0.30, RX * 0.8, RY * 0.56 * blink); rgba(ctx, mix(DISC, FEATH, 0.5), 1); ctx.fill(); ctx.restore()
        # bec (dépasse de la sphère : visible de profil)
        b0 = V(-0.10, -0.02, th, 1.02); b1 = V(0.10, -0.02, th, 1.02); bt = V(0.0, -0.26, th, 1.13)
        if bt[2] > -0.25:
            ctx.new_path(); ctx.move_to(b0[0], b0[1]); ctx.curve_to(b0[0], b0[1] + 20 * U, bt[0] - 6 * U, bt[1] - 18 * U, bt[0], bt[1])
            ctx.curve_to(bt[0] + 6 * U, bt[1] - 18 * U, b1[0], b1[1] + 20 * U, b1[0], b1[1]); ctx.close_path()
            rgba(ctx, BEAKC, 1); ctx.fill()
    # ombrage (clair de lune en haut à droite)
    g = cairo.LinearGradient(HC[0] + RX, HC[1] - RY, HC[0] - RX, HC[1] + RY)
    g.add_color_stop_rgba(0, 0.75, 0.85, 1.0, 0.10); g.add_color_stop_rgba(0.55, 0, 0, 0, 0.0); g.add_color_stop_rgba(1, 0.0, 0.0, 0.03, 0.40)
    ctx.set_source(g); ctx.paint()
    ctx.restore()
    ctx.new_path(); head_path(ctx); ctx.set_line_width(5 * U); rgba(ctx, MOONL, 0.20); ctx.stroke()
    tuft(ctx, th, -1, False); tuft(ctx, th, 1, False)

RING = (HC[0], HC[1] + RY * 0.62, RX * 1.20, RX * 0.21)
def ring_pt(phi):
    cx, cy, rx, ry = RING
    return (cx + rx * math.sin(phi), cy + ry * math.cos(phi))

def ring_arc(ctx, a0, a1, col, width, alpha, front, dash=None):
    """Arc de l'anneau de rotation entre a0 et a1 (radians) ; front = True : partie avant seulement, False : arrière."""
    n = max(2, int(abs(a1 - a0) / 0.03))
    pts = [a0 + (a1 - a0) * k / n for k in range(n + 1)]
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    if dash: ctx.set_dash(dash)
    seg = []
    for phi in pts:
        vis = (math.cos(phi) >= -0.02) == front
        if vis: seg.append(ring_pt(phi))
        elif len(seg) > 1:
            for w_, c_, al in ((width * 2.0, DARK, 0.45), (width, col, 1.0)):
                ctx.new_path(); ctx.move_to(*seg[0]); [ctx.line_to(*p) for p in seg[1:]]; ctx.set_line_width(w_); rgba(ctx, c_, al * alpha); ctx.stroke()
            seg = []
        else: seg = []
    if len(seg) > 1:
        for w_, c_, al in ((width * 2.0, DARK, 0.45), (width, col, 1.0)):
            ctx.new_path(); ctx.move_to(*seg[0]); [ctx.line_to(*p) for p in seg[1:]]; ctx.set_line_width(w_); rgba(ctx, c_, al * alpha); ctx.stroke()
    if dash: ctx.set_dash([])

def ring_head(ctx, phi, alpha):
    x, y = ring_pt(phi); cx, cy, rx, ry = RING
    ang = math.atan2(-ry * math.sin(phi), rx * math.cos(phi))
    glow(ctx, x, y, 60 * U, GOLD, 0.45 * alpha)
    arrowhead(ctx, x, y, ang, GOLD, 40 * U, alpha)

def owl_scene(ctx, T, th, blink=0.0, ring=None):
    """ring = (angle atteint, alpha, full) : anneau doré de la rotation ; full = cercle complet en pointillés + zone interdite."""
    night_bg(ctx, T)
    owl_body(ctx, T)
    branch(ctx, T)
    if ring:
        phi, ra, full, kx = ring
        if full:
            ring_arc(ctx, 0, 2 * math.pi, (0.75, 0.80, 0.95), 5 * U, 0.55 * ra, False, [14 * U, 12 * U])
            if kx > 0: ring_arc(ctx, 1.5 * math.pi, 2 * math.pi, (1.0, 0.20, 0.22), 9 * U, ra * kx, False)
        ring_arc(ctx, 0, phi, GOLD, 10 * U, 0.85 * ra, False)
    owl_head(ctx, T, th, blink)
    if ring:
        phi, ra, full, kx = ring
        if full:
            ring_arc(ctx, 0, 2 * math.pi, (0.75, 0.80, 0.95), 5 * U, 0.75 * ra, True, [14 * U, 12 * U])
            if kx > 0: ring_arc(ctx, 1.5 * math.pi, 2 * math.pi, (1.0, 0.20, 0.22), 9 * U, ra * kx, True)
        ring_arc(ctx, 0, phi, GOLD, 10 * U, ra, True)
        if phi > 0.05: ring_head(ctx, phi, ra)
        circle(ctx, *ring_pt(0), 12 * U, WHITE, 0.9 * ra)
    foreground(ctx, T)

# ---------------------------------------------------------------- fond « schéma »
def diagram_bg(ctx, T, a=1.0):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, 0.06, 0.05, 0.17, a); g.add_color_stop_rgba(1, 0.01, 0.02, 0.07, a)
    ctx.set_source(g); ctx.paint()
    glow(ctx, W * 0.46, H * 0.40, 0.75 * H, (0.20, 0.30, 0.70), 0.20 * a)
    rnd = random.Random(8)
    for i in range(18):
        x = rnd.random() * W; y = (rnd.random() * H - T * rnd.uniform(8, 25) * U) % H
        circle(ctx, x, y, rnd.uniform(2, 5) * U, rnd.choice([CYAN, PURPLE, GOLD]), (0.18 + 0.10 * math.sin(T * 2 + i)) * a)

def artery_line(ctx, pts, col=ART, width=14, a=1.0, depth=None):
    """Artère : halo + trait ; depth[i] < 0 → segment derrière (plus fin, plus sombre)."""
    for i in range(len(pts) - 1):
        d = 1.0 if depth is None else depth[i]
        wf = 1.0 if d >= 0 else 0.6; al = a if d >= 0 else 0.45 * a
        for w_, c_, aa in ((width * 2.4 * wf, col, 0.20), (width * wf, col, 1.0), (width * 0.35 * wf, mix(col, WHITE, 0.6), 0.8)):
            ctx.new_path(); ctx.move_to(*pts[i]); ctx.line_to(*pts[i + 1]); ctx.set_line_width(w_ * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            rgba(ctx, c_, aa * al); ctx.stroke()

# ---------------------------------------------------------------- plan B : cou humain (silhouette sans visage)
def human_sil(c):
    c.new_path()
    c.move_to(W * 0.08, H * 0.64)
    c.curve_to(W * 0.10, H * 0.55, W * 0.21, H * 0.52, W * 0.34, H * 0.505)
    c.curve_to(W * 0.37, H * 0.50, W * 0.385, H * 0.47, W * 0.385, H * 0.44)
    c.line_to(W * 0.385, H * 0.385)
    c.curve_to(W * 0.30, H * 0.365, W * 0.27, H * 0.31, W * 0.27, H * 0.26)
    c.curve_to(W * 0.27, H * 0.18, W * 0.36, H * 0.135, W * 0.46, H * 0.135)
    c.curve_to(W * 0.56, H * 0.135, W * 0.65, H * 0.18, W * 0.65, H * 0.26)
    c.curve_to(W * 0.65, H * 0.31, W * 0.62, H * 0.365, W * 0.535, H * 0.385)
    c.line_to(W * 0.535, H * 0.44)
    c.curve_to(W * 0.535, H * 0.47, W * 0.55, H * 0.50, W * 0.58, H * 0.505)
    c.curve_to(W * 0.71, H * 0.52, W * 0.82, H * 0.55, W * 0.84, H * 0.64)
    c.close_path()

def human_neck(ctx, T, twist, t_tear):
    diagram_bg(ctx, T)
    human_sil(ctx); rgba(ctx, NAVF, 0.96); ctx.fill()
    neon_path(ctx, human_sil, CYAN, 4 * U, 0.9)
    cx = W * 0.46
    for k in range(7):                                   # vertèbres cervicales (pâles)
        y = H * (0.388 + k * 0.0172)
        rrect(ctx, cx - W * 0.032, y, W * 0.064, H * 0.012, 6 * U); rgba(ctx, BONE, 0.30); ctx.fill()
    y0, y1 = H * 0.53, H * 0.375                         # bas / haut du cou
    tore = T >= t_tear
    for ph0 in (math.pi, 0.0):
        pts, dep = [], []
        n = 60
        for k in range(n + 1):
            y = lerp(y0, H * 0.30, k / n)
            f = clamp((y0 - y) / (y0 - y1))
            ph = ph0 + twist * f
            r = W * (0.050 if y > y1 else lerp(0.050, 0.028, clamp((y1 - y) / (y1 - H * 0.30))))
            pts.append((cx + r * math.cos(ph), y)); dep.append(math.sin(ph) * -1 if y > y1 else 1)
        if tore and ph0 == 0.0:
            mid = int(n * 0.42)
            artery_line(ctx, pts[:mid - 2], depth=dep[:mid - 2]); artery_line(ctx, pts[mid + 2:], depth=dep[mid + 2:])
            bx, by = pts[mid]
            kk = clamp((T - t_tear) / 0.35)
            glow(ctx, bx, by, 110 * U * (0.6 + 0.6 * kk), (1.0, 0.25, 0.20), 0.55 * (1.2 - 0.5 * kk))
            for j in range(9):
                an = j * 2 * math.pi / 9 + 0.3
                l0, l1 = 20 * U, (40 + 55 * kk) * U
                ctx.new_path(); ctx.move_to(bx + math.cos(an) * l0, by + math.sin(an) * l0); ctx.line_to(bx + math.cos(an) * l1, by + math.sin(an) * l1)
                ctx.set_line_width(6 * U); rgba(ctx, GOLD if j % 2 else ART, 0.9 * (1 - 0.6 * kk)); ctx.stroke()
            tear_pt = (bx, by)
        else:
            artery_line(ctx, pts, depth=dep)
    # flèche de torsion autour du cou
    rcx, rcy, rrx, rry = cx, H * 0.425, W * 0.125, H * 0.020
    if twist > 0.05:
        n = max(2, int(twist / 0.04)); prev = None
        for k in range(n + 1):
            ph = twist * k / n; p = (rcx + rrx * math.sin(ph), rcy + rry * math.cos(ph)); fr = math.cos(ph) >= 0
            if prev:
                ctx.new_path(); ctx.move_to(*prev); ctx.line_to(*p); ctx.set_line_width((10 if fr else 6) * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                rgba(ctx, GOLD, 1.0 if fr else 0.45); ctx.stroke()
            prev = p
        ang = math.atan2(-rry * math.sin(twist), rrx * math.cos(twist))
        arrowhead(ctx, prev[0], prev[1], ang, GOLD, 36 * U, 1.0 if math.cos(twist) >= 0 else 0.6)
    if tore:
        kk = prog(T, t_tear, t_tear + 0.3)
        tx_, ty_ = tear_pt
        leader(ctx, W * 0.74, H * 0.36, tx_ + 14 * U, ty_ - 10 * U, ART, 1.0, kk)
        pill(ctx, "TEAR!", W * 0.74, H * 0.34, ART, 52, 1.0, kk)

# ---------------------------------------------------------------- plan C : yeux en tubes (vue de dessus)
def lock_icon(ctx, x, y, s, a=1.0):
    ctx.new_path(); ctx.arc(x, y - s * 0.35, s * 0.42, math.pi, 2 * math.pi); ctx.set_line_width(s * 0.18); rgba(ctx, GOLD, a); ctx.stroke()
    rrect(ctx, x - s * 0.62, y - s * 0.38, s * 1.24, s * 0.95, s * 0.18); rgba(ctx, GOLD, a); ctx.fill()
    circle(ctx, x, y + s * 0.06, s * 0.13, DARK, a)

def eyes_diagram(ctx, T, tt):
    diagram_bg(ctx, T)
    cx, cy, R = W * 0.46, H * 0.40, W * 0.30
    def head(c): c.new_path(); c.arc(cx, cy, R, 0, 2 * math.pi)
    head(ctx); rgba(ctx, (0.10, 0.09, 0.20), 0.96); ctx.fill()
    for k in range(60):                                   # plumes (contour)
        an = 2 * math.pi * k / 60
        ctx.new_path(); ctx.move_to(cx + math.cos(an) * R * 0.86, cy + math.sin(an) * R * 0.86); ctx.line_to(cx + math.cos(an) * R * 0.97, cy + math.sin(an) * R * 0.97)
        ctx.set_line_width(5 * U); rgba(ctx, FEATH_L, 0.25); ctx.stroke()
    neon_path(ctx, head, GOLD, 4 * U, 0.85)
    ctx.new_path(); ctx.move_to(cx, cy - R - W * 0.06); ctx.line_to(cx - W * 0.035, cy - R + W * 0.02); ctx.line_to(cx + W * 0.035, cy - R + W * 0.02); ctx.close_path()
    rgba(ctx, BEAKC, 1); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, GOLD, 0.9); ctx.stroke()
    k_tube = prog(T, tt["tubes"] - 0.15, tt["tubes"] + 0.30)
    k_lock = prog(T, tt["locked"] - 0.05, tt["locked"] + 0.30)
    for sd in (-1, 1):
        rx_, ry_ = cx + sd * W * 0.105, cy + H * 0.030
        fx_, fy_ = cx + sd * W * 0.130, cy - H * 0.085
        ang = math.atan2(fy_ - ry_, fx_ - rx_); nx, ny = -math.sin(ang), math.cos(ang); hw = W * 0.048
        quad = [(rx_ + nx * hw, ry_ + ny * hw), (fx_ + nx * hw, fy_ + ny * hw), (fx_ - nx * hw, fy_ - ny * hw), (rx_ - nx * hw, ry_ - ny * hw)]
        ctx.new_path(); ctx.move_to(*quad[0]); [ctx.line_to(*p) for p in quad[1:]]; ctx.close_path()
        rgba(ctx, (0.14, 0.20, 0.40), 1); ctx.fill()
        ctx.new_path(); ctx.arc(rx_, ry_, hw, ang + math.pi / 2, ang + 3 * math.pi / 2); rgba(ctx, (0.85, 0.35, 0.45), 0.9); ctx.fill()   # rétine
        ctx.new_path(); ctx.arc(fx_, fy_, hw, ang - math.pi / 2, ang + math.pi / 2); rgba(ctx, (0.55, 0.85, 1.0), 0.55); ctx.fill()     # cornée
        ctx.new_path(); ctx.move_to(fx_ + nx * hw, fy_ + ny * hw); ctx.line_to(fx_ - nx * hw, fy_ - ny * hw); ctx.set_line_width(12 * U); rgba(ctx, IRIS, 1); ctx.stroke()
        glow(ctx, (rx_ + fx_) / 2, (ry_ + fy_) / 2, W * 0.12, CYAN, 0.25 * k_tube)
        def tube(c, quad=quad):
            c.move_to(*quad[0]); c.line_to(*quad[1]); c.move_to(*quad[2]); c.line_to(*quad[3])
        neon_path(ctx, tube, CYAN, 3.5 * U, 0.6 + 0.4 * k_tube)
        # anneau osseux (plaques sclérotiques) le long des parois
        for side in (1, -1):
            for j in range(5):
                u = 0.25 + 0.15 * j
                px, py = lerp(rx_, fx_, u) + side * nx * hw * 1.08, lerp(ry_, fy_, u) + side * ny * hw * 1.08
                rrect(ctx, px - 10 * U, py - 16 * U, 20 * U, 32 * U, 6 * U); rgba(ctx, BONE, 0.55 + 0.45 * k_lock); ctx.fill()
        if k_lock > 0:
            lx = cx + sd * W * 0.235; ly = cy - H * 0.03
            ctx.save(); ctx.translate(lx, ly); s_ = 0.6 + 0.4 * ease(k_lock) + 0.12 * math.sin(math.pi * k_lock); ctx.scale(s_, s_)
            glow(ctx, 0, 0, 70 * U, GOLD, 0.35 * k_lock); lock_icon(ctx, 0, 0, 52 * U, k_lock); ctx.restore()
    label_box(ctx, "TUBE-SHAPED EYES", cx, H * 0.165, GOLD, 50, 1.0, k_tube)
    # « It can't roll them » : l'œil rond humain roule, pas celui de la chouette
    k_roll = prog(T, tt["roll"] - 0.15, tt["roll"] + 0.25)
    if k_roll > 0:
        ex, ey, er = W * 0.17, H * 0.615, W * 0.062
        text(ctx, "YOU", ex, H * 0.548, 44 * U, CYAN, k_roll)
        circle(ctx, ex, ey, er * ease(k_roll), WHITE, k_roll)
        an = (T - tt["roll"]) * 4.0
        circle(ctx, ex + er * 0.42 * math.cos(an), ey + er * 0.42 * math.sin(an), er * 0.42, (0.30, 0.55, 0.95), k_roll)
        circle(ctx, ex + er * 0.42 * math.cos(an), ey + er * 0.42 * math.sin(an), er * 0.20, DARK, k_roll)
        ctx.new_path(); ctx.arc(ex, ey, er * 1.35, -2.4, 1.4); ctx.set_line_width(7 * U); rgba(ctx, GREEN, k_roll); ctx.stroke()
        arrowhead(ctx, ex + er * 1.35 * math.cos(1.4), ey + er * 1.35 * math.sin(1.4), 1.4 + math.pi / 2, GREEN, 26 * U, k_roll)
        k_x = prog(T, tt["roll"] + 0.25, tt["roll"] + 0.55)
        ox_, oy_ = cx + W * 0.13, cy - H * 0.05
        ctx.new_path(); ctx.arc(ox_, oy_, W * 0.085, -2.4, 1.4); ctx.set_line_width(7 * U); rgba(ctx, CORAL, 0.8 * k_x); ctx.stroke()
        red_x(ctx, ox_ + W * 0.11, oy_ + H * 0.03, 56 * U, 1.0, k_x)

# ---------------------------------------------------------------- plan D : vertèbres du cou (14 contre 7)
def head_icon_owl(ctx, x, y, s, a):
    def d(c):
        c.new_path(); c.arc(x, y, s, 0, 2 * math.pi)
    d(ctx); rgba(ctx, (0.12, 0.10, 0.22), a); ctx.fill()
    for sd in (-1, 1):
        ctx.new_path(); ctx.move_to(x + sd * s * 0.45, y - s * 0.82); ctx.line_to(x + sd * s * 0.80, y - s * 1.45); ctx.line_to(x + sd * s * 0.88, y - s * 0.58); ctx.close_path()
        rgba(ctx, GOLD, 0.9 * a); ctx.fill()
        circle(ctx, x + sd * s * 0.38, y - s * 0.05, s * 0.28, IRIS, a); circle(ctx, x + sd * s * 0.38, y - s * 0.05, s * 0.13, DARK, a)
    ctx.new_path(); ctx.move_to(x - s * 0.10, y + s * 0.22); ctx.line_to(x + s * 0.10, y + s * 0.22); ctx.line_to(x, y + s * 0.50); ctx.close_path(); rgba(ctx, GOLD, a); ctx.fill()
    neon_path(ctx, d, GOLD, 3.5 * U, a)

def head_icon_human(ctx, x, y, s, a):
    def d(c):
        c.new_path(); c.save(); c.translate(x, y); c.scale(0.86, 1.0); c.arc(0, 0, s, 0, 2 * math.pi); c.restore()
    d(ctx); rgba(ctx, NAVF, a); ctx.fill(); neon_path(ctx, d, CYAN, 3.5 * U, a)

OWL_NECK = [(0.27, 0.215), (0.31, 0.27), (0.31, 0.33), (0.25, 0.40), (0.23, 0.46), (0.27, 0.53), (0.29, 0.56)]
_ONP = []
def _neck_pts():
    pts = F(OWL_NECK); q = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(30):
            u = k / 30; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    out.append(pts[-1]); return out
_ONP = _neck_pts()
_OL = [0.0]
for i in range(1, len(_ONP)): _OL.append(_OL[-1] + math.hypot(_ONP[i][0] - _ONP[i - 1][0], _ONP[i][1] - _ONP[i - 1][1]))
def neck_at(f):
    L = f * _OL[-1]
    for i in range(1, len(_OL)):
        if _OL[i] >= L:
            u = (L - _OL[i - 1]) / max(1e-6, _OL[i] - _OL[i - 1]); p, q = _ONP[i - 1], _ONP[i]
            return (lerp(p[0], q[0], u), lerp(p[1], q[1], u)), math.atan2(q[1] - p[1], q[0] - p[0])
    return _ONP[-1], math.pi / 2

def vertebra_block(ctx, x, y, ang, w, h, col, a, k):
    if k <= 0: return
    s_ = 0.5 + 0.5 * ease(k) + 0.12 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang - math.pi / 2); ctx.scale(s_, s_)
    rrect(ctx, -w / 2, -h / 2, w, h, h * 0.35); rgba(ctx, col, a * ease(k)); ctx.fill_preserve()
    ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.5 * a * ease(k)); ctx.stroke()
    ctx.restore()

def bones_diagram(ctx, T):
    diagram_bg(ctx, T)
    t14, t7 = WT("fourteen") - 0.25, WT("seven") - 0.20
    ox, hx = W * 0.27, W * 0.66
    head_icon_owl(ctx, ox, H * 0.175, W * 0.075, 1.0)
    head_icon_human(ctx, hx, H * 0.175, W * 0.075, 1.0)
    text(ctx, "OWL", ox + W * 0.13, H * 0.180, 48 * U, GOLD, 1.0, align="l")
    text(ctx, "YOU", hx + W * 0.10, H * 0.180, 48 * U, CYAN, 1.0, align="l")
    n_owl = 0
    for i in range(14):
        k = prog(T, t14 + i * 0.065, t14 + i * 0.065 + 0.18)
        if k > 0: n_owl = i + 1
        (x, y), ang = neck_at((i + 0.5) / 14)
        vertebra_block(ctx, x, y, ang, W * 0.085, H * 0.0185, GOLD, 1.0, k)
    n_h = 0
    for i in range(7):
        k = prog(T, t7 + i * 0.07, t7 + i * 0.07 + 0.18)
        if k > 0: n_h = i + 1
        y = H * (0.235 + (i + 0.5) * 0.047)
        vertebra_block(ctx, hx, y, math.pi / 2, W * 0.10, H * 0.034, CYAN, 1.0, k)
    if n_owl > 0:
        glow(ctx, ox, H * 0.615, 120 * U, GOLD, 0.30)
        poster_text(ctx, str(n_owl), ox, H * 0.612, 150 * U, GOLD)
    if n_h > 0:
        glow(ctx, hx, H * 0.615, 120 * U, CYAN, 0.30)
        poster_text(ctx, str(n_h), hx, H * 0.612, 150 * U, CYAN)

# ---------------------------------------------------------------- plan E1 : une vertèbre en coupe (trous ≈ 10× l'artère)
def vertebra_xs(ctx, T, t_wide):
    diagram_bg(ctx, T)
    cx, cy = W * 0.46, H * 0.40
    bod = (cx, cy + H * 0.085, W * 0.13)
    arch = (cx, cy - H * 0.02, W * 0.125)
    fl = [(cx - W * 0.255, cy + H * 0.02), (cx + W * 0.255, cy + H * 0.02)]
    RF = W * 0.085; RA = RF / 10.0
    def shape(c):
        c.new_path(); c.arc(bod[0], bod[1], bod[2], 0, 2 * math.pi)
        c.new_sub_path(); c.arc(arch[0], arch[1], arch[2], 0, 2 * math.pi)
        for (x, y) in fl:
            c.new_sub_path(); c.arc(x, y, RF * 1.55, 0, 2 * math.pi)
    # os (union approchée : remplissages successifs)
    ctx.new_path(); ctx.move_to(cx - W * 0.07, cy - H * 0.05); ctx.line_to(cx, cy - H * 0.155); ctx.line_to(cx + W * 0.07, cy - H * 0.05); ctx.close_path()
    rgba(ctx, BONE, 0.95); ctx.fill()
    for (x, y, r) in (bod, arch):
        circle(ctx, x, y, r, BONE, 0.95)
    for (x, y) in fl:
        circle(ctx, x, y, RF * 1.55, BONE, 0.95)
        ctx.new_path(); ctx.move_to(x, y - RF * 1.2); ctx.line_to(cx, cy - H * 0.04); ctx.line_to(cx, cy + H * 0.06); ctx.line_to(x, y + RF * 1.2); ctx.close_path(); rgba(ctx, BONE, 0.95); ctx.fill()
    neon_path(ctx, shape, GOLD, 2.5 * U, 0.45)
    # canal de la moelle
    circle(ctx, arch[0], arch[1] - H * 0.005, W * 0.065, (0.04, 0.05, 0.13), 1); circle(ctx, arch[0], arch[1] - H * 0.005, W * 0.038, (1.0, 0.92, 0.62), 0.9)
    k = prog(T, t_wide - 0.10, t_wide + 0.30)
    for j, (x, y) in enumerate(fl):
        circle(ctx, x, y, RF, (0.04, 0.05, 0.13), 1)
        glow(ctx, x, y, RF * 0.95, CYAN, 0.22 + 0.25 * k)
        an = T * 2.6 + j * 2.0                            # l'artère bouge librement dans le trou (torsion)
        ax, ay = x + (RF - RA * 2.5) * 0.65 * math.cos(an), y + (RF - RA * 2.5) * 0.65 * math.sin(an)
        glow(ctx, ax, ay, RA * 5, ART, 0.6); circle(ctx, ax, ay, RA, ART, 1); circle(ctx, ax - RA * 0.3, ay - RA * 0.3, RA * 0.35, WHITE, 0.7)
        if k > 0:
            ctx.new_path(); ctx.arc(x, y, RF, 0, 2 * math.pi); ctx.set_line_width(7 * U); rgba(ctx, GOLD, k); ctx.stroke()
    x, y = fl[1]
    leader(ctx, W * 0.62, H * 0.235, x, y - RF - 8 * U, GOLD, 1.0, k)
    label_box(ctx, "10× WIDER", W * 0.58, H * 0.205, GOLD, 56, 1.0, k)
    kk = prog(T, t_wide + 0.6, t_wide + 0.9)
    x0, y0 = fl[0]
    if kk > 0:
        leader(ctx, W * 0.28, H * 0.585, x0, y0 + RF * 0.3, ART, 1.0, kk)
        label_box(ctx, "ARTERY", W * 0.28, H * 0.61, ART, 46, 1.0, kk)

# ---------------------------------------------------------------- plans E2–E3 : réservoirs et cerveau (vue de profil)
NECKS = F([(0.56, 0.64), (0.52, 0.58), (0.47, 0.52), (0.49, 0.46), (0.55, 0.40), (0.58, 0.355)])
def skull_side(c):
    c.new_path()
    pts = F([(0.62, 0.115), (0.72, 0.135), (0.78, 0.19), (0.78, 0.26), (0.73, 0.31), (0.64, 0.335), (0.55, 0.335), (0.47, 0.31),
             (0.38, 0.30), (0.30, 0.318), (0.33, 0.28), (0.36, 0.24), (0.42, 0.18), (0.50, 0.13)])
    smooth_closed(c, pts)

def blood_side(ctx, T, k_res, k_flow, twist):
    diagram_bg(ctx, T)
    skull_side(ctx); rgba(ctx, (0.10, 0.09, 0.20), 0.95); ctx.fill()
    neon_path(ctx, skull_side, GOLD, 4 * U, 0.85)
    # orbite (grand œil) et cerveau
    circle(ctx, W * 0.47, H * 0.235, W * 0.075, (0.05, 0.05, 0.12), 1)
    ctx.new_path(); ctx.arc(W * 0.47, H * 0.235, W * 0.075, 0, 2 * math.pi); ctx.set_line_width(5 * U); rgba(ctx, IRIS, 0.7); ctx.stroke()
    bx, by = W * 0.65, H * 0.205
    glow(ctx, bx, by, W * 0.16, BRAIN, 0.25 + 0.35 * k_flow * (0.8 + 0.2 * math.sin(T * 6)))
    ctx.save(); ctx.translate(bx, by); ctx.scale(W * 0.10, H * 0.052); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, BRAIN, 0.85); ctx.fill()
    for j in range(4):
        ctx.new_path(); ctx.arc(bx - W * 0.05 + j * W * 0.033, by, W * 0.03, math.pi * 1.1, math.pi * 1.9); ctx.set_line_width(4 * U); rgba(ctx, (0.75, 0.30, 0.45), 0.8); ctx.stroke()
    # colonne du cou (vertèbres le long de la courbe)
    q = [NECKS[0]] + NECKS + [NECKS[-1]]; neck = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for kk in range(20):
            u = kk / 20; u2, u3 = u * u, u * u * u
            neck.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    for i in range(0, len(neck) - 1, 7):
        p, qq = neck[i], neck[min(i + 1, len(neck) - 1)]
        vertebra_block(ctx, p[0], p[1], math.atan2(qq[1] - p[1], qq[0] - p[0]), W * 0.075, H * 0.014, BONE, 0.75, 1.0)
    # artère : parallèle à la colonne, avec ondulation de torsion
    art, dep = [], []
    for i, p in enumerate(neck):
        f = i / (len(neck) - 1)
        ph = twist * f
        art.append((p[0] + W * 0.055 * math.cos(ph), p[1])); dep.append(math.cos(ph))
    top = art[-1]
    art += [(top[0] + W * 0.02, top[1] - H * 0.03), (bx - W * 0.03, by + H * 0.04)]; dep += [1, 1]
    artery_line(ctx, art, depth=dep, width=16)
    # réservoirs à la base de la tête
    res = [(top[0] - W * 0.02, top[1] + H * 0.012), (top[0] + W * 0.075, top[1] - H * 0.010)]
    for j, (x, y) in enumerate(res):
        r = W * (0.012 + 0.030 * ease(k_res)) * (1 + 0.08 * math.sin(T * 5 + j) * k_res)
        glow(ctx, x, y, r * 2.4, ART, 0.40 * k_res); circle(ctx, x, y, r, ART, 0.95)
        circle(ctx, x - r * 0.3, y - r * 0.3, r * 0.25, WHITE, 0.6 * k_res)
    if k_res > 0:
        x, y = res[0]
        leader(ctx, W * 0.24, H * 0.47, x - W * 0.035, y + 4 * U, ART, 1.0, k_res)
        label_box(ctx, "RESERVOIRS", W * 0.24, H * 0.50, ART, 46, 1.0, k_res)
    # flux de sang vers le cerveau
    if k_flow > 0:
        L = [0.0]
        for i in range(1, len(art)): L.append(L[-1] + math.hypot(art[i][0] - art[i - 1][0], art[i][1] - art[i - 1][1]))
        for j in range(16):
            s = ((T * 0.55 + j / 16) % 1.0) * L[-1]
            for i in range(1, len(L)):
                if L[i] >= s:
                    u = (s - L[i - 1]) / max(1e-6, L[i] - L[i - 1]); p, qq = art[i - 1], art[i]
                    x, y = lerp(p[0], qq[0], u), lerp(p[1], qq[1], u)
                    glow(ctx, x, y, 24 * U, (1.0, 0.6, 0.6), 0.6 * k_flow); circle(ctx, x, y, 8 * U, WHITE, 0.95 * k_flow)
                    break
        label_box(ctx, "BRAIN", W * 0.70, H * 0.075, BRAIN, 44, 1.0, k_flow)
        leader(ctx, W * 0.70, H * 0.095, bx, by - H * 0.03, BRAIN, 1.0, k_flow)
    if twist > 0.05:
        rcx, rcy, rrx, rry = W * 0.50, H * 0.49, W * 0.15, H * 0.020
        n = max(2, int(twist / 0.05)); prev = None
        for kk in range(n + 1):
            ph = twist * kk / n; p = (rcx + rrx * math.sin(ph), rcy + rry * math.cos(ph)); fr = math.cos(ph) >= 0
            if prev:
                ctx.new_path(); ctx.move_to(*prev); ctx.line_to(*p); ctx.set_line_width((10 if fr else 6) * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                rgba(ctx, GOLD, 1.0 if fr else 0.45); ctx.stroke()
            prev = p
        arrowhead(ctx, prev[0], prev[1], math.atan2(-rry * math.sin(twist), rrx * math.cos(twist)), GOLD, 34 * U, 1.0)

# ---------------------------------------------------------------- montage (temps absolu)
T_SPIN1 = WT("degrees") + 0.05                       # fin de la grande rotation (au mot « degrees »)
T_B0 = SENT("hook", 1) - 0.10                        # cou humain
T_TEAR = WT("tear")
T_C0 = SENT("eyes", 0) - 0.10                        # yeux en tubes
T_C1 = WT("turns") - 0.40                            # « so it turns its head » : retour à la chouette
T_D0 = SENT("bones", 0) - 0.10                       # 14 contre 7
T_E0 = SENT("blood", 0) - 0.10                       # vertèbre en coupe
T_E1 = WT("with") - 0.10                             # réservoirs
T_F0 = SENT("close", 0) - 0.10                       # fin : la limite de 270°
T_AROUND = WT("around")
T_LIMIT = WT("limit")
T_CTA = END_T - 2.5
D2R = math.pi / 180.0

def th_hook(T):
    u = clamp(T / T_SPIN1)
    th = 20 + 250 * (1 - (1 - u) ** 2)
    if T > T_SPIN1: th = 270 + 7 * math.exp(-(T - T_SPIN1) * 5) * math.sin((T - T_SPIN1) * 14)
    return th * D2R

def th_final(T):
    t1 = T_F0 + 0.25; t2 = T_AROUND + 0.15
    if T < t1: return 0.0
    if T < t2: return 282 * D2R * ease((T - t1) / (t2 - t1))                 # tente de dépasser…
    th = 270 + 12 * math.exp(-(T - t2) * 6) * math.cos((T - t2) * 16)        # … et revient à la butée
    t3 = END_T - 1.25
    if T > t3: th = lerp(270, 30, ease((T - t3) / 1.05))                     # retour à la pose de l'image 1 (boucle)
    return th * D2R

def master(ctx, T):
    if T < T_B0:                                       # A — la tête tourne (image 1)
        th = th_hook(T)
        owl_scene(ctx, T, th, blink=max(0, 1 - abs(T - (T_SPIN1 + 0.55)) / 0.10), ring=(th, 1.0, False, 0))
        series_pill(ctx, 1.0)
        poster_text(ctx, "270°", W * 0.50, H * 0.140, 165 * U, GOLD, W * 0.46)
        if T > 1.2: tag(ctx, "Illustration", 0.118, prog(T, 1.2, 1.5))
    elif T < T_C0:                                     # B — cou humain
        tw = 270 * D2R * prog(T, T_B0 + 0.25, T_TEAR - 0.05)
        human_neck(ctx, T, tw, T_TEAR)
        tag(ctx, "Simplified illustration")
        pill(ctx, "HUMAN NECK", W * 0.46, H * 0.590, CYAN, 46, 1.0, prog(T, T_B0, T_B0 + 0.3))
    elif T < T_C1:                                     # C — yeux en tubes, fixés
        eyes_diagram(ctx, T, {"tubes": WT("tubes"), "locked": WT("locked"), "roll": WT("roll")})
        tag(ctx, "Simplified illustration")
    elif T < T_D0:                                     # C' — donc elle tourne la tête
        th = 160 * D2R * ease((T - T_C1) / max(0.3, T_D0 - T_C1 - 0.2))
        owl_scene(ctx, T, th, ring=(th, 1.0, False, 0))
        tag(ctx, "Illustration")
    elif T < T_E0:                                     # D — 14 vertèbres contre 7
        bones_diagram(ctx, T)
        tag(ctx, "Simplified illustration")
    elif T < T_E1:                                     # E1 — trous 10× plus larges que l'artère
        vertebra_xs(ctx, T, WT("extra-wide"))
        tag(ctx, "Simplified illustration")
    elif T < T_F0:                                     # E2–E3 — réservoirs, puis le sang arrive au cerveau pendant la torsion
        k_res = prog(T, WT("reservoirs") - 0.25, WT("reservoirs") + 0.35)
        k_flow = prog(T, WT("so") - 0.10, WT("so") + 0.35)
        tw = 200 * D2R * prog(T, WT("mid-twist") - 0.30, WT("mid-twist") + 0.50)
        blood_side(ctx, T, max(k_res, 0.0), k_flow, tw)
        tag(ctx, "Simplified illustration")
    else:                                              # F — la limite : trois quarts de tour
        th = th_final(T)
        kx = prog(T, T_AROUND - 0.05, T_AROUND + 0.25)
        ra = 1.0 - prog(T, END_T - 1.3, END_T - 1.0) * 0.0
        owl_scene(ctx, T, th, blink=max(0, 1 - abs(T - (T_LIMIT + 0.5)) / 0.10), ring=(min(th, 270 * D2R), ra, True, kx))
        if kx > 0:
            px, py = ring_pt(1.75 * math.pi)
            red_x(ctx, px - 36 * U, py - 70 * U, 52 * U, 1.0, kx)
        kl = prog(T, T_LIMIT - 0.75, T_LIMIT - 0.45) * (1 - prog(T, END_T - 1.4, END_T - 1.1))
        pill(ctx, "MAX 270°", W * 0.46, H * 0.555, GOLD, 60, 1.0, kl)
        tag(ctx, "Illustration")
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            font(ctx, 46 * U); txt = "FACTORA"
            w_ = ctx.text_extents(txt).width + 60 * U
            rrect(ctx, W * 0.46 - w_ / 2, H * 0.130 - 34 * U, w_, 68 * U, 34 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
            text(ctx, txt, W * 0.46, H * 0.130, 46 * U, GOLD, kc)
            cta_lines(ctx, ("Follow Factora for more", "animal mysteries."), W * 0.46, (H * 0.172, H * 0.204), 54, kc)

T_COVER = 0.10
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER                # 2 premières images (vignettes) = l'image 1
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t

def sc_hook(ctx, t, d): master(ctx, _abs_t("hook", t))
def sc_eyes(ctx, t, d): master(ctx, _abs_t("eyes", t))
def sc_bones(ctx, t, d): master(ctx, _abs_t("bones", t))
def sc_blood(ctx, t, d): master(ctx, _abs_t("blood", t))
def sc_close(ctx, t, d): master(ctx, _abs_t("close", t))

SHORT_SCENES = ["hook", "eyes", "bones", "blood", "close"]
SCENES = dict(hook=sc_hook, eyes=sc_eyes, bones=sc_bones, blood=sc_blood, close=sc_close)

def cover(ctx):
    """Affiche = l'image 1 (règle de la semaine 1 : la miniature YouTube est l'image 1), sans sous-titre."""
    master(ctx, T_COVER)
