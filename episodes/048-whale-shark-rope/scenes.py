exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Épisode 048 (Short seul, 9:16, ~36 s) — « One Borrowed Knife Saved a Whale Shark » (sujet proposé par Nazik le 2026-11-22
# à partir d'une publication Little Big Things ; leur vidéo n'est PAS reprise : tout est dessiné ici, sans aucune personne
# réelle reconnaissable). Demande de Nazik : « Ajoute de l'émotionnel » → la blessure, le moment où elle reste immobile à la
# surface pendant les 30 minutes, la délivrance au ralenti, une voix plus posée et une musique qui monte ; uniquement des
# faits rapportés.
# Faits (Hawaii News Now 2026-11-12, KHON2, Yahoo/A-Z Animals) : début novembre 2026, au large de Waikiki (Turtle Canyon),
# l'équipage d'une excursion de snorkeling et des plongeurs trouvent une jeune femelle requin-baleine prise dans une corde
# « épaisse comme une jambe » qui entaillait ses nageoires pectorales ; un plongeur demande un couteau aux bateaux voisins,
# il faut 30 minutes pour la libérer ; elle reste près de la surface pendant qu'on coupe ; la corde est remise au DLNR.
# Requins : pas de nage en arrière (PBS NOVA ; DLNR Hawaï). Requin-baleine : plus grand poisson, « En danger » sur la liste
# rouge de l'UICN depuis 2016.
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

DARK = (0.02, 0.04, 0.10)
SKIN = (0.22, 0.32, 0.42)
SKIN_D = (0.10, 0.16, 0.24)
BELLY = (0.80, 0.86, 0.90)
ROPE = (0.45, 0.38, 0.22)
ALGAE = (0.32, 0.58, 0.26)
WOUND = (0.95, 0.35, 0.38)
SUIT = (0.06, 0.07, 0.09)

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

def tag(ctx, s, y=0.083, a=1.0):
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
    sz = size * U; maxw = W * 0.74
    cap_font(ctx, sz)
    widest = max(ctx.text_extents(l).width for l in lines)
    if widest > maxw: sz *= maxw / widest; cap_font(ctx, sz)
    for l, y, col in zip(lines, ys, (WHITE, GOLD)):
        e = ctx.text_extents(l); x0 = x - e.width / 2 - e.x_bearing; y0 = y + sz * 0.35
        ctx.move_to(x0 + 3 * U, y0 + 5 * U); ctx.text_path(l); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
        ctx.move_to(x0, y0); ctx.text_path(l); ctx.set_line_width(sz * 0.16); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, (0.01, 0.02, 0.06), a); ctx.stroke_preserve(); rgba(ctx, col, a); ctx.fill()

# ---------------------------------------------------------------- océan (fond pré-calculé + rayons et particules animés)
def _build_ocean():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W), int(H)); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.42, 0.86, 0.98); g.add_color_stop_rgb(0.10, 0.16, 0.66, 0.90); g.add_color_stop_rgb(0.50, 0.04, 0.38, 0.70)
    g.add_color_stop_rgb(1, 0.01, 0.10, 0.28)
    c.set_source(g); c.paint()
    glow(c, W * 0.55, -H * 0.05, W * 0.9, (0.8, 0.97, 1.0), 0.45)
    return s
_OCEAN = _build_ocean()
_RP = random.Random(6)
SNOW = [(_RP.random(), _RP.random(), _RP.uniform(1.5, 5), _RP.uniform(0.01, 0.04)) for _ in range(120)]

def ocean(ctx, T, dark=0.0):
    ctx.set_source_surface(_OCEAN, 0, 0); ctx.paint()
    for i in range(6):                                   # rayons de soleil
        x0 = W * (0.10 + 0.17 * i) + 60 * U * math.sin(T * 0.4 + i)
        g = cairo.LinearGradient(x0, 0, x0 + W * 0.25, H * 0.85)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.16); g.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.new_path(); ctx.move_to(x0 - W * 0.03, 0); ctx.line_to(x0 + W * 0.05, 0); ctx.line_to(x0 + W * 0.33, H * 0.85); ctx.line_to(x0 + W * 0.17, H * 0.85); ctx.close_path()
        ctx.set_source(g); ctx.fill()
    for k in range(12):                                  # surface (reflets mouvants)
        y = H * 0.012 + k * 9 * U; x = (k * 173 + T * 60) % W
        ctx.new_path(); ctx.move_to(x - W * 0.3, y); ctx.curve_to(x - W * 0.1, y - 8 * U, x + W * 0.1, y + 8 * U, x + W * 0.3, y)
        ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.30); ctx.stroke()
    for (sx, sy, r, sp) in SNOW:
        y = ((sy - T * sp) % 1.0) * H; x = sx * W + 12 * U * math.sin(T + sy * 9)
        circle(ctx, x, y, r * U, WHITE, 0.35)
    if dark > 0: rgba(ctx, (0.0, 0.03, 0.10), dark); ctx.paint()

# ---------------------------------------------------------------- requin-baleine (profil, tête à gauche ; repère normalisé x ∈ [0, 1])
TOP = [(0.00, 0.00), (0.02, -0.055), (0.08, -0.085), (0.18, -0.105), (0.30, -0.115), (0.42, -0.112), (0.55, -0.100), (0.68, -0.080), (0.78, -0.055), (0.86, -0.035), (0.90, -0.028)]
BOT = [(0.90, 0.025), (0.86, 0.032), (0.78, 0.050), (0.66, 0.075), (0.52, 0.095), (0.38, 0.105), (0.24, 0.100), (0.12, 0.085), (0.05, 0.060), (0.01, 0.025)]
PECT = [(0.22, 0.085), (0.30, 0.17), (0.37, 0.245), (0.41, 0.235), (0.37, 0.14), (0.33, 0.095)]
DORS1 = [(0.49, -0.100), (0.56, -0.205), (0.62, -0.215), (0.63, -0.185), (0.61, -0.090)]
DORS2 = [(0.75, -0.062), (0.785, -0.115), (0.81, -0.060)]
CAUD = [(0.885, -0.030), (0.95, -0.15), (1.01, -0.265), (1.035, -0.25), (0.97, -0.08), (0.95, 0.0), (0.99, 0.10), (1.00, 0.15), (0.97, 0.14), (0.90, 0.03)]
_RS = random.Random(13)
SPOTS = []
for i in range(220):
    x = _RS.uniform(0.04, 0.86); y = _RS.uniform(-0.10, 0.06)
    SPOTS.append((x, y, _RS.uniform(0.0035, 0.0075)))
STRIPES = [0.16 + 0.045 * k for k in range(16)]

def _bend(p, T):
    x, y = p
    if x > 0.70: y += 0.030 * math.sin(T * 2.2 - x * 5.0) * (x - 0.70) / 0.30
    return (x, y)

def shark_path(ctx, T, parts):
    for part in parts:
        smooth_closed(ctx, [_bend(p, T) for p in part])

def whale_shark(ctx, T, x0, y0, L, ang=0.0, rope=1.0, rope_tight=0.0, wound=0.0, a=1.0):
    """Requin-baleine de profil : (x0, y0) = bout du museau, L = longueur ; rope ∈ [0, 1] = corde présente (1) ou tombée (0)."""
    ctx.save(); ctx.translate(x0, y0); ctx.rotate(ang); ctx.scale(L, L)
    lw = 1.0 / L
    body = TOP + BOT
    if rope > 0:
        rope_line(ctx, [(0.305, -0.140), (0.315, -0.06), (0.325, 0.03), (0.335, 0.125)], 0.026, a * rope * 0.85)
    # nageoires arrière (dorsales, caudale), pectorale lointaine
    for part, col in ((DORS1, SKIN_D), (DORS2, SKIN_D), (CAUD, SKIN_D)):
        ctx.new_path(); smooth_closed(ctx, [_bend(p, T) for p in part]); rgba(ctx, col, a); ctx.fill()
    ctx.new_path(); smooth_closed(ctx, [_bend(p, T) for p in body])
    g = cairo.LinearGradient(0, -0.12, 0, 0.11)
    g.add_color_stop_rgba(0, *SKIN, a); g.add_color_stop_rgba(0.55, *mix(SKIN, BELLY, 0.25), a); g.add_color_stop_rgba(1, *BELLY, a)
    ctx.set_source(g); ctx.fill()
    ctx.save(); ctx.new_path(); smooth_closed(ctx, [_bend(p, T) for p in body]); ctx.clip()
    for xs in STRIPES:                                    # bandes claires (damier)
        ctx.new_path(); ctx.move_to(xs, -0.13); ctx.line_to(xs + 0.01, 0.05); ctx.set_line_width(0.0035); rgba(ctx, WHITE, 0.30 * a); ctx.stroke()
    for (sx, sy, r) in SPOTS:
        bx, by = _bend((sx, sy), T)
        if by < 0.06: circle(ctx, bx, by, r, (0.92, 0.96, 1.0), 0.85 * a)
    for k in range(3):                                    # crêtes du dos
        ctx.new_path(); ctx.move_to(0.12, -0.09 + k * 0.02); ctx.curve_to(0.4, -0.10 + k * 0.022, 0.6, -0.085 + k * 0.02, 0.86, -0.03 + k * 0.01)
        ctx.set_line_width(0.004); rgba(ctx, WHITE, 0.22 * a); ctx.stroke()
    g2 = cairo.LinearGradient(0, -0.12, 0, 0.11); g2.add_color_stop_rgba(0, 0.6, 0.9, 1.0, 0.18); g2.add_color_stop_rgba(0.4, 0, 0, 0, 0); g2.add_color_stop_rgba(1, 0, 0, 0.05, 0.25)
    ctx.set_source(g2); ctx.paint()
    ctx.restore()
    for k in range(5):                                    # fentes branchiales
        x = 0.155 + k * 0.018
        ctx.new_path(); ctx.move_to(x, -0.045); ctx.curve_to(x + 0.006, -0.01, x + 0.006, 0.03, x, 0.06); ctx.set_line_width(0.0045); rgba(ctx, SKIN_D, 0.8 * a); ctx.stroke()
    ctx.new_path(); ctx.move_to(0.004, 0.012); ctx.curve_to(0.03, 0.030, 0.06, 0.034, 0.085, 0.028); ctx.set_line_width(0.006); rgba(ctx, (0.05, 0.07, 0.10), a); ctx.stroke()   # bouche
    circle(ctx, 0.078, -0.012, 0.0085, (0.04, 0.05, 0.07), a); circle(ctx, 0.0805, -0.0145, 0.0028, WHITE, 0.8 * a)                                                         # œil
    # nageoire pectorale (devant), blessée par la corde
    ctx.new_path(); smooth_closed(ctx, PECT)
    g3 = cairo.LinearGradient(0.25, 0.09, 0.40, 0.24); g3.add_color_stop_rgba(0, *mix(SKIN, BELLY, 0.2), a); g3.add_color_stop_rgba(1, *SKIN_D, a)
    ctx.set_source(g3); ctx.fill()
    if wound > 0:
        for k in range(5):
            x = 0.27 + k * 0.012
            ctx.new_path(); ctx.move_to(x, 0.095 + k * 0.004); ctx.line_to(x + 0.03, 0.135 + k * 0.006); ctx.set_line_width(0.006); rgba(ctx, WOUND, 0.75 * wound * a); ctx.stroke()
    if rope > 0: rope_on_shark(ctx, T, rope, rope_tight, a)
    ctx.restore()

_RR = random.Random(21)
TUFTS = [(_RR.uniform(0, 1), _RR.uniform(-1, 1), _RR.uniform(0.6, 1.3)) for _ in range(46)]
def rope_line(ctx, pts, width, a=1.0, sway=0.0):
    """Corde épaisse torsadée, couverte d'algues ; pts en coordonnées courantes, width dans la même unité."""
    for w_, col, al in ((width * 1.25, (0.10, 0.08, 0.05), 0.55), (width, ROPE, 1.0)):
        ctx.new_path(); smooth_open(ctx, pts); ctx.set_line_width(w_); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        rgba(ctx, col, al * a); ctx.stroke()
    n = len(pts)
    for k in range(n - 1):                                # torsade
        for j in range(3):
            u = j / 3.0; x = lerp(pts[k][0], pts[k + 1][0], u); y = lerp(pts[k][1], pts[k + 1][1], u)
            dx, dy = pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]; l = math.hypot(dx, dy) + 1e-9; nx, ny = -dy / l, dx / l
            ctx.new_path(); ctx.move_to(x + nx * width * 0.45, y + ny * width * 0.45); ctx.line_to(x - nx * width * 0.45 + dx / l * width * 0.35, y - ny * width * 0.45 + dy / l * width * 0.35)
            ctx.set_line_width(width * 0.12); rgba(ctx, (0.25, 0.20, 0.10), 0.7 * a); ctx.stroke()
    for (u, side, s) in TUFTS:                            # algues et petites balanes
        i = min(n - 2, int(u * (n - 1))); f = u * (n - 1) - i
        x = lerp(pts[i][0], pts[i + 1][0], f); y = lerp(pts[i][1], pts[i + 1][1], f)
        ctx.new_path(); ctx.move_to(x, y)
        ctx.curve_to(x + side * width * 0.5, y - width * 0.4 * s, x + side * width * 0.9 + sway * width * 0.3, y - width * 0.9 * s, x + side * width * 0.6 + sway * width * 0.6, y - width * 1.4 * s)
        ctx.set_line_width(width * 0.16); rgba(ctx, ALGAE, 0.9 * a); ctx.stroke()
        circle(ctx, x - side * width * 0.25, y + width * 0.2, width * 0.10, (0.90, 0.90, 0.82), 0.8 * a)

def rope_on_shark(ctx, T, k, tight, a):
    sway = math.sin(T * 1.7)
    loop = [(0.335, -0.125), (0.345, -0.05), (0.36, 0.03), (0.37, 0.10), (0.36, 0.16)]
    rope_line(ctx, [(x + 0.004 * tight * math.sin(T * 20), y) for x, y in loop], 0.030, a * k, sway)
    hang = [(0.36, 0.16), (0.34, 0.24), (0.38, 0.33), (0.35, 0.43), (0.39, 0.52)]
    hang = [(x + 0.02 * math.sin(T * 1.3 + j), y) for j, (x, y) in enumerate(hang)]
    rope_line(ctx, hang, 0.028, a * k, sway)

# ---------------------------------------------------------------- plongeur (silhouette, aucun visage)
def diver(ctx, x, y, s, ang=0.0, arm=0.0, knife=True, a=1.0):
    """Plongeur de profil, tête vers la gauche ; arm ∈ [-1, 1] = mouvement du bras (scie)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    rrect(ctx, 0.05, -0.33, 0.55, 0.17, 0.08); rgba(ctx, (0.55, 0.58, 0.62), a); ctx.fill()        # bouteille
    ctx.new_path(); smooth_closed(ctx, [(-0.05, -0.18), (0.30, -0.22), (0.62, -0.18), (0.80, -0.10), (0.80, -0.02), (0.55, 0.04), (0.20, 0.06), (-0.05, 0.02)])
    rgba(ctx, SUIT, a); ctx.fill()
    for dy, col in ((-0.07, SUIT), (0.0, SUIT)):                                                      # jambes et palmes
        ctx.new_path(); ctx.move_to(0.78, dy - 0.03); ctx.line_to(1.10, dy - 0.05 + 0.03 * math.sin(arm * 2)); ctx.set_line_width(0.07); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, a); ctx.stroke()
        ctx.new_path(); ctx.move_to(1.08, dy - 0.08); ctx.line_to(1.42, dy - 0.10 + 0.06 * math.sin(arm * 2)); ctx.line_to(1.40, dy - 0.01); ctx.line_to(1.08, dy - 0.01); ctx.close_path()
        rgba(ctx, (0.10, 0.45, 0.85), a); ctx.fill()
    circle(ctx, -0.13, -0.12, 0.11, SUIT, a)                                                          # tête (cagoule)
    rrect(ctx, -0.26, -0.18, 0.10, 0.09, 0.03); rgba(ctx, (0.55, 0.90, 1.0), 0.85 * a); ctx.fill()   # masque (reflet)
    circle(ctx, -0.21, -0.04, 0.035, (0.25, 0.25, 0.28), a)                                           # détendeur
    hx, hy = -0.35 + 0.05 * arm, 0.18 + 0.03 * arm                                                    # bras + couteau
    ctx.new_path(); ctx.move_to(0.05, -0.05); ctx.line_to(-0.15, 0.08); ctx.line_to(hx, hy); ctx.set_line_width(0.065); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    rgba(ctx, SUIT, a); ctx.stroke()
    if knife:
        ctx.new_path(); ctx.move_to(hx, hy); ctx.line_to(hx - 0.16, hy + 0.05); ctx.line_to(hx - 0.02, hy + 0.04); ctx.close_path(); rgba(ctx, (0.90, 0.93, 0.97), a); ctx.fill()
    ctx.restore()
    return (x + (hx - 0.12) * s * math.cos(ang), y + (hy + 0.04) * s)

# ---------------------------------------------------------------- plans
def shot_wide(ctx, T, rope=1.0, wound=0.0, diver_k=1.0, dx=0.0, push=0.0):
    ocean(ctx, T)
    z = 1.0 + 0.05 * push
    ctx.save(); ctx.translate(W * 0.46, H * 0.42); ctx.scale(z, z); ctx.translate(-W * 0.46, -H * 0.42)
    L = W * 1.55
    whale_shark(ctx, T, -W * 0.05 + dx, H * 0.585 + 10 * U * math.sin(T * 0.8), L, -0.42, rope=rope, wound=wound)
    if diver_k > 0:
        diver(ctx, W * (0.92 - 0.20 * ease(diver_k)), H * (0.255 + 0.01 * math.sin(T)), W * 0.20, 0.10, arm=math.sin(T * 3) * 0.3)
    ctx.restore()

def shot_closeup(ctx, T, zoom, cx, cy, rope=1.0, tight=0.0, wound=0.0, diver_s=0.0, saw=0.0):
    """Gros plan : on agrandit le requin autour d'un point (cx, cy) en coordonnées normalisées."""
    ocean(ctx, T)
    L = W * 1.18 * zoom
    x0 = W * 0.46 - cx * L; y0 = H * 0.40 - cy * L
    whale_shark(ctx, T, x0, y0 + 8 * U * math.sin(T * 0.8), L, 0.0, rope=rope, rope_tight=tight, wound=wound)
    if diver_s > 0:
        hand = diver(ctx, W * 0.72, H * 0.22, W * 0.55 * diver_s, 0.55, arm=saw)
        return hand

def eye_closeup(ctx, T, k_timer):
    ocean(ctx, T, dark=0.15)
    L = W * 7.5
    cx, cy = 0.078, -0.012
    x0 = W * 0.46 - cx * L; y0 = H * 0.40 - cy * L
    whale_shark(ctx, T * 0.4, x0, y0 + 6 * U * math.sin(T * 0.6), L, 0.0, rope=0.0)
    # plongeur flou au loin, qui coupe
    ctx.save(); ctx.push_group()
    diver(ctx, W * 0.78, H * 0.13, W * 0.22, 0.4, arm=math.sin(T * 6))
    ctx.pop_group_to_source(); ctx.paint_with_alpha(0.55); ctx.restore()
    glow(ctx, W * 0.46, H * 0.40, W * 0.30, (0.7, 0.95, 1.0), 0.18 + 0.06 * math.sin(T * 1.5))

def diagram_shark(ctx, T, k_fwd, k_back, k_x, tight):
    ocean(ctx, T, dark=0.55)
    L = W * 0.86; x0, y0 = W * 0.07, H * 0.36
    def sil(c):
        c.save(); c.translate(x0, y0); c.scale(L, L)
        smooth_closed(c, TOP + BOT); smooth_closed(c, PECT); smooth_closed(c, DORS1); smooth_closed(c, CAUD)
        c.restore()
    sil(ctx); rgba(ctx, (0.06, 0.12, 0.24), 0.9); ctx.fill()
    neon_path(ctx, sil, CYAN, 3.5 * U, 0.9)
    ctx.save(); ctx.translate(x0, y0); ctx.scale(L, L); rope_on_shark(ctx, T, 1.0, tight, 1.0); ctx.restore()
    ya = H * 0.56
    if k_fwd > 0:
        xe = lerp(W * 0.42, W * 0.12, ease(k_fwd))
        ctx.new_path(); ctx.move_to(W * 0.42, ya); ctx.line_to(xe + 30 * U, ya); ctx.set_line_width(16 * U); rgba(ctx, GREEN, 1); ctx.stroke()
        arrowhead(ctx, xe, ya, math.pi, GREEN, 50 * U, 1.0)
    if k_back > 0:
        xe = lerp(W * 0.52, W * 0.82, ease(k_back))
        ctx.new_path(); ctx.move_to(W * 0.52, ya); ctx.line_to(xe - 30 * U, ya); ctx.set_line_width(16 * U); rgba(ctx, CORAL, 1); ctx.stroke()
        arrowhead(ctx, xe, ya, 0.0, CORAL, 50 * U, 1.0)
        red_x(ctx, W * 0.68, ya, 60 * U, 1.0, k_x)

# ---------------------------------------------------------------- montage
T_B0 = SENT("wound", 0) - 0.08
T_C0 = SENT("stuck", 0) - 0.08
T_D0 = SENT("cut", 0) - 0.08
T_E0 = SENT("stay", 1) - 0.10             # gros plan sur l'œil quand elle « reste » (« She stayed right there… »)
T_F0 = SENT("free", 0) - 0.08
T_G0 = SENT("count", 0) - 0.08
T_H0 = SENT("close", 0) - 0.08
T_CTA = END_T - 2.5

def master(ctx, T):
    if T < T_B0:                                          # A — piégé
        shot_wide(ctx, T, rope=1.0, wound=0.0, diver_k=prog(T, 0.0, 4.0), push=T / 5.0)
        series_pill(ctx, 1.0)
        kp = 1.0 - prog(T, T_B0 - 0.3, T_B0)
        poster_text(ctx, "TRAPPED", W * 0.46, H * 0.135, 175 * U, CORAL, W * 0.80)
        if T > 1.2: tag(ctx, "Illustration", 0.195, prog(T, 1.2, 1.5))
    elif T < T_C0:                                        # B — la corde entaille la nageoire
        z = lerp(2.3, 2.6, prog(T, T_B0, T_C0))
        shot_closeup(ctx, T, z, 0.34, 0.12, rope=1.0, tight=0.5, wound=prog(T, WT("cutting") - 0.3, WT("fins") + 0.2))
        kl = prog(T, WT("rope") - 0.1, WT("rope") + 0.3)
        pill(ctx, "AS THICK AS A LEG", W * 0.46, H * 0.115, GOLD, 50, 1.0, kl)
        tag(ctx, "Illustration", 0.170)
    elif T < T_D0:                                        # C — pas de marche arrière
        diagram_shark(ctx, T, prog(T, WT("sharks") - 0.1, WT("sharks") + 0.5), prog(T, WT("backward") - 0.3, WT("backward") + 0.3),
                      prog(T, WT("backward") + 0.2, WT("backward") + 0.5), prog(T, WT("couldn't") - 0.1, WT("herself") + 0.3))
        pill(ctx, "NO REVERSE", W * 0.46, H * 0.115, CORAL, 52, 1.0, prog(T, WT("backward") - 0.1, WT("backward") + 0.3))
        tag(ctx, "Simplified illustration", 0.170)
    elif T < T_E0:                                        # D — le couteau
        saw = math.sin((T - WT("started")) * 9) if T > WT("started") else 0.0
        shot_closeup(ctx, T, 2.0, 0.34, 0.10, rope=1.0, tight=0.2, wound=1.0, diver_s=1.0, saw=saw)
        kk = prog(T, WT("knife") - 0.1, WT("knife") + 0.3)
        if kk > 0:
            glow(ctx, W * 0.42, H * 0.36, 90 * U * (0.8 + 0.4 * math.sin(T * 9)), WHITE, 0.45 * kk)
        tag(ctx, "Illustration")
    elif T < T_F0:                                        # E — elle reste, 30 minutes
        k_t = prog(T, WT("stayed") - 0.1, WT("minutes") + 0.3)
        eye_closeup(ctx, T, k_t)
        mins = int(30 * k_t)
        if k_t > 0:
            glow(ctx, W * 0.46, H * 0.62, 130 * U, GOLD, 0.30)
            poster_text(ctx, f"{mins} MIN", W * 0.46, H * 0.62, 120 * U, GOLD)
        tag(ctx, "Illustration")
    elif T < T_G0:                                        # F — la corde tombe, elle est libre
        kf = prog(T, WT("fell") - 0.2, WT("free") + 0.4)
        ocean(ctx, T)
        L = W * 1.55
        whale_shark(ctx, T, -W * 0.05 - W * 0.10 * ease(prog(T, WT("free") - 0.2, T_G0)), H * 0.585, L, -0.42, rope=0.0, wound=0.6)
        ctx.save(); ctx.translate(-W * 0.05, H * 0.585); ctx.rotate(-0.42); ctx.scale(L, L)
        ctx.translate(0.36, 0.30 * ease(kf)); ctx.rotate(0.6 * ease(kf)); ctx.translate(-0.36, 0)
        rope_on_shark(ctx, T, 1.0 - 0.6 * kf, 0.0, 1.0)
        ctx.restore()
        kb = prog(T, WT("free") - 0.15, WT("free") + 0.6)
        if kb > 0:
            glow(ctx, W * 0.46, H * 0.36, W * 0.8 * ease(kb), (0.85, 1.0, 1.0), 0.40 * (1 - kb * 0.5))
            rnd = random.Random(5)
            for i in range(24):
                bx = W * rnd.uniform(0.2, 0.75); by = H * (0.55 - 0.45 * ((kb + rnd.random()) % 1.0))
                ctx.new_path(); ctx.arc(bx, by, rnd.uniform(6, 16) * U, 0, 2 * math.pi); ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.6 * kb); ctx.stroke()
        tag(ctx, "Illustration")
    elif T < T_H0:                                        # G — en danger ; chacun compte
        u = prog(T, T_G0, T_H0)
        ocean(ctx, T)
        whale_shark(ctx, T, W * (0.20 - 0.08 * u), H * (0.42 - 0.04 * u), W * (0.70 - 0.12 * u), -0.10, rope=0.0, wound=0.3)
        pill(ctx, "ENDANGERED", W * 0.46, H * 0.115, CORAL, 56, 1.0, prog(T, WT("endangered") - 0.2, WT("endangered") + 0.2))
        kc = prog(T, WT("counts") - 0.3, WT("counts") + 0.3)
        if kc > 0: text(ctx, "IUCN Red List", W * 0.46, H * 0.170, 36 * U, WHITE, 0.85 * kc)
        tag(ctx, "Illustration", 0.230)
    else:                                                 # H — sauvée par un couteau emprunté (boucle vers l'image 1)
        u = prog(T, T_H0, END_T)
        shot_wide(ctx, T, rope=0.0, wound=0.2, diver_k=1.0, push=1.0 - u)
        kk = prog(T, WT("knife") + 0.0 if WT("knife", 1) > 1e8 else WT("knife", 1) - 0.1, END_T)
        tag(ctx, "Illustration")
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            font(ctx, 46 * U); txt = "FACTORA"
            w_ = ctx.text_extents(txt).width + 60 * U
            rrect(ctx, W * 0.46 - w_ / 2, H * 0.130 - 34 * U, w_, 68 * U, 34 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
            text(ctx, txt, W * 0.46, H * 0.130, 46 * U, GOLD, kc)
            cta_lines(ctx, ("Follow Factora for more", "animal mysteries."), W * 0.46, (H * 0.172, H * 0.204), 54, kc)

T_COVER = 0.6
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t

def _mk(name):
    def sc(ctx, t, d): master(ctx, _abs_t(name, t))
    return sc
SHORT_SCENES = ["hook", "wound", "stuck", "cut", "stay", "free", "count", "close"]
SCENES = {n: _mk(n) for n in SHORT_SCENES}

def cover(ctx):
    """Miniature : le requin-baleine pris dans la corde, le plongeur qui arrive ; « TRAPPED » + bandeau d'action."""
    shot_wide(ctx, 1.0, rope=1.0, wound=0.0, diver_k=1.0)
    g = cairo.LinearGradient(0, 0, 0, H * 0.30); g.add_color_stop_rgba(0, 0.0, 0.03, 0.10, 0.55); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.30); ctx.fill()
    poster_text(ctx, "TRAPPED", W * 0.46, H * 0.180, 200 * U, CORAL, W * 0.86)
    txt = "SHE DIDN'T SWIM AWAY"; fs = 62 * U; font(ctx, fs)
    if ctx.text_extents(txt).width > W * 0.74: fs *= W * 0.74 / ctx.text_extents(txt).width; font(ctx, fs)
    w_ = ctx.text_extents(txt).width + 80 * U; h_ = fs * 1.9; y_ = H * 0.775
    glow(ctx, W * 0.46, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.46 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.46, y_, fs, DARK)
