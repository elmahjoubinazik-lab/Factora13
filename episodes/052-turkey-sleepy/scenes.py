exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Épisode 052 (Short seul, 9:16, ~31 s) — Thanksgiving : ce n'est pas la dinde qui fait dormir (demande de Nazik, 2026-11-26,
# pour le soir même). Image 1 = un homme endormi sur le canapé, la dinde rôtie au premier plan + « NOT THE TURKEY » (3 mots).
# Faits : le tryptophane (acide aminé, précurseur de la sérotonine et de la mélatonine) n'est pas plus abondant dans la dinde
# que dans le poulet ou le bœuf ; la somnolence vient surtout du repas (quantité, glucides, alcool) ; estimation souvent
# citée : ≈ 3 000 calories pour le repas de Thanksgiving (Calorie Control Council). Dessins 100 % faits ici.
# Voix : Jessica via Runway (fichiers, pas d'horodatage par mot → WT() estime l'instant d'un mot dans sa phrase).
import json as _json, re as _re

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WT = []
for sg in _TLL:
    for se in sg["sents"]:
        txt = se["text"]; n = max(1, len(txt))
        for m in _re.finditer(r"\S+", txt):
            _WT.append((m.group().lower().strip(".,?!:;'\""), se["start"] + (se["end"] - se["start"]) * m.start() / n))
def WT(word, n=0):
    hits = [t for w, t in _WT if w == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def SENT(scene, i=0): return _TL[scene]["sents"][i]["start"]
END_T = _TLL[-1]["end"] + 0.6

DARK = (0.03, 0.02, 0.08)
def lerp(a, b, k): return a + (b - a) * k

# ---------------------------------------------------------------- textes
def tag(ctx, s, y=0.083, a=1.0):
    if a <= 0: return
    font(ctx, 32 * U); w_ = ctx.text_extents(s).width + 40 * U
    x0, y0 = W * 0.055, H * y
    rrect(ctx, x0, y0 - 25 * U, w_, 50 * U, 25 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.50 * a); ctx.fill()
    text(ctx, s, x0 + 20 * U, y0, 32 * U, (0.92, 0.94, 1.0), 0.92 * a, align="l")

def pill(ctx, s, x, y, col, size=50, a=1.0, k=1.0, fg=DARK):
    if a <= 0 or k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 64 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.7, col, 0.35 * a)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.97 * a); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, a)
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

def ellipse(ctx, x, y, rx, ry, rot=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()

def no_sign(ctx, x, y, r, a=1.0):
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(r * 0.16); rgba(ctx, (0.92, 0.15, 0.18), a); ctx.stroke()
    ctx.new_path(); ctx.move_to(x - r * 0.7, y - r * 0.7); ctx.line_to(x + r * 0.7, y + r * 0.7); ctx.stroke()

def drop(ctx, x, y, r, col, a=1.0):
    ctx.new_path(); ctx.move_to(x, y - r * 1.6)
    ctx.curve_to(x + r * 0.4, y - r * 0.9, x + r, y - r * 0.2, x + r, y + r * 0.25)
    ctx.arc(x, y + r * 0.25, r, 0, math.pi)
    ctx.curve_to(x - r, y - r * 0.2, x - r * 0.4, y - r * 0.9, x, y - r * 1.6); ctx.close_path()
    rgba(ctx, col, a); ctx.fill()



# ---------------------------------------------------------------- objets dessinés
BROWN = (0.70, 0.36, 0.12)
def roast_turkey(ctx, x, y, s, a=1.0, halo=0.0, T=0.0):
    """Dinde rôtie sur son plat, vue de face ; (x, y) = centre du corps, s = demi-largeur du corps."""
    ctx.save(); ctx.push_group()
    # plat + garniture
    ctx.new_path(); ellipse(ctx, x, y + 0.52 * s, 1.50 * s, 0.30 * s)
    g = cairo.LinearGradient(0, y + 0.25 * s, 0, y + 0.82 * s); g.add_color_stop_rgb(0, 0.98, 0.98, 1.0); g.add_color_stop_rgb(1, 0.78, 0.80, 0.86)
    ctx.set_source(g); ctx.fill()
    ctx.new_path(); ellipse(ctx, x, y + 0.50 * s, 1.30 * s, 0.22 * s); ctx.set_line_width(0.025 * s); rgba(ctx, (0.70, 0.72, 0.80), 1); ctx.stroke()
    for i in range(14):   # herbes et canneberges autour
        ang = math.pi * (0.05 + 0.9 * i / 13)
        gx, gy = x - math.cos(ang) * 1.22 * s, y + 0.52 * s + math.sin(ang) * 0.12 * s
        if i % 2: circle(ctx, gx, gy, 0.07 * s, (0.80, 0.10, 0.18), 1)
        else: ctx.new_path(); ellipse(ctx, gx, gy, 0.11 * s, 0.05 * s, ang); rgba(ctx, (0.25, 0.62, 0.25), 1); ctx.fill()
    # cuisses (derrière les pilons)
    for sx in (-1, 1):
        ctx.new_path(); ellipse(ctx, x + sx * 0.62 * s, y + 0.12 * s, 0.36 * s, 0.30 * s, sx * 0.5); rgba(ctx, (0.62, 0.30, 0.10), 1); ctx.fill()
    # corps
    ctx.new_path(); ellipse(ctx, x, y, s, 0.64 * s)
    g = cairo.RadialGradient(x - 0.30 * s, y - 0.30 * s, 0.1 * s, x, y, 1.1 * s)
    g.add_color_stop_rgb(0, 1.00, 0.78, 0.42); g.add_color_stop_rgb(0.55, 0.86, 0.50, 0.18); g.add_color_stop_rgb(1, 0.58, 0.26, 0.08)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(0.03 * s); rgba(ctx, (0.45, 0.20, 0.06), 0.8); ctx.stroke()
    for k in range(3):   # plis de la peau
        ctx.new_path(); ctx.arc(x + (k - 1) * 0.35 * s, y + 0.05 * s, 0.30 * s, 0.25 * math.pi, 0.75 * math.pi)
        ctx.set_line_width(0.025 * s); rgba(ctx, (0.55, 0.25, 0.08), 0.5); ctx.stroke()
    ctx.new_path(); ellipse(ctx, x - 0.35 * s, y - 0.32 * s, 0.30 * s, 0.12 * s, -0.4); rgba(ctx, (1.0, 0.95, 0.85), 0.45); ctx.fill()
    # pilons dressés + os + papillotes
    for sx in (-1, 1):
        ctx.new_path(); ellipse(ctx, x + sx * 0.62 * s, y - 0.10 * s, 0.30 * s, 0.15 * s, sx * -1.0)
        g = cairo.LinearGradient(x + sx * 0.4 * s, y + 0.1 * s, x + sx * 0.8 * s, y - 0.3 * s); g.add_color_stop_rgb(0, 0.80, 0.42, 0.14); g.add_color_stop_rgb(1, 0.95, 0.62, 0.28)
        ctx.set_source(g); ctx.fill()
        bx, by = x + sx * 0.84 * s, y - 0.40 * s
        ctx.new_path(); ctx.move_to(x + sx * 0.74 * s, y - 0.28 * s); ctx.line_to(bx, by); ctx.set_line_width(0.09 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.98, 0.95, 0.88), 1); ctx.stroke()
        for d in (-1, 1): circle(ctx, bx + d * 0.045 * s, by - 0.03 * s, 0.055 * s, (0.98, 0.95, 0.88), 1)
        ctx.new_path()   # papillote
        for j in range(9):
            r = (0.13 if j % 2 else 0.08) * s; ang = -math.pi * j / 8
            ctx.line_to(bx + math.cos(ang) * r, by - 0.05 * s + math.sin(ang) * r * 0.9)
        ctx.close_path(); rgba(ctx, WHITE, 1); ctx.fill()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()
    if halo > 0:
        hy = y - 0.95 * s + 0.03 * s * math.sin(T * 3)
        glow(ctx, x, hy, 0.6 * s, GOLD, 0.5 * halo)
        ctx.new_path(); ellipse(ctx, x, hy, 0.48 * s * ease(halo), 0.10 * s * ease(halo)); ctx.set_line_width(0.07 * s); rgba(ctx, (1.0, 0.85, 0.25), halo); ctx.stroke()

def room(ctx, T):
    vgrad(ctx, (0.45, 0.24, 0.22), (0.24, 0.11, 0.14), 0, H * 0.62)
    # fenêtre (nuit) et lampe
    wx, wy, ww, wh = W * 0.66, H * 0.215, W * 0.26, H * 0.085
    rrect(ctx, wx - 14 * U, wy - 14 * U, ww + 28 * U, wh + 28 * U, 10 * U); rgba(ctx, (0.55, 0.36, 0.22), 1); ctx.fill()
    g = cairo.LinearGradient(0, wy, 0, wy + wh); g.add_color_stop_rgb(0, 0.06, 0.08, 0.25); g.add_color_stop_rgb(1, 0.18, 0.16, 0.40)
    ctx.rectangle(wx, wy, ww, wh); ctx.set_source(g); ctx.fill()
    circle(ctx, wx + ww * 0.72, wy + wh * 0.32, 26 * U, (1.0, 0.96, 0.80), 1)
    for i in range(7):
        sx_, sy_ = wx + ww * ((i * 0.37) % 1), wy + wh * ((i * 0.61) % 0.9 + 0.05)
        circle(ctx, sx_, sy_, 3.5 * U, WHITE, 0.5 + 0.5 * math.sin(T * 3 + i))
    ctx.rectangle(wx + ww / 2 - 5 * U, wy, 10 * U, wh); rgba(ctx, (0.55, 0.36, 0.22), 1); ctx.fill()
    glow(ctx, W * 0.10, H * 0.26, W * 0.35, (1.0, 0.75, 0.35), 0.55)
    ctx.new_path(); ctx.move_to(W * 0.05, H * 0.30); ctx.line_to(W * 0.15, H * 0.30); ctx.line_to(W * 0.13, H * 0.235); ctx.line_to(W * 0.07, H * 0.235); ctx.close_path(); rgba(ctx, (1.0, 0.88, 0.60), 1); ctx.fill()
    # sol
    g = cairo.LinearGradient(0, H * 0.60, 0, H); g.add_color_stop_rgb(0, 0.42, 0.25, 0.15); g.add_color_stop_rgb(1, 0.16, 0.09, 0.06)
    ctx.rectangle(0, H * 0.60, W, H * 0.40); ctx.set_source(g); ctx.fill()

def couch_back(ctx):
    for (x0, x1, y0, y1, col) in ((0.07, 0.93, 0.30, 0.48, (0.58, 0.18, 0.22)),):
        rrect(ctx, W * x0, H * y0, W * (x1 - x0), H * (y1 - y0), 40 * U)
        g = cairo.LinearGradient(0, H * y0, 0, H * y1); g.add_color_stop_rgb(0, *mix(col, WHITE, 0.12)); g.add_color_stop_rgb(1, *mix(col, DARK, 0.25)); ctx.set_source(g); ctx.fill()
    for cx_ in (0.30, 0.70):   # coussins du dossier
        rrect(ctx, W * (cx_ - 0.19), H * 0.32, W * 0.38, H * 0.12, 30 * U); rgba(ctx, (0.66, 0.22, 0.26), 1); ctx.fill()

def couch_front(ctx):
    rrect(ctx, W * 0.09, H * 0.455, W * 0.82, H * 0.07, 26 * U)
    g = cairo.LinearGradient(0, H * 0.455, 0, H * 0.525); g.add_color_stop_rgb(0, 0.70, 0.25, 0.28); g.add_color_stop_rgb(1, 0.45, 0.12, 0.16); ctx.set_source(g); ctx.fill()
    for sx in (0.035, 0.885):
        rrect(ctx, W * sx, H * 0.38, W * 0.08, H * 0.15, 30 * U)
        g = cairo.LinearGradient(0, H * 0.38, 0, H * 0.53); g.add_color_stop_rgb(0, 0.66, 0.22, 0.26); g.add_color_stop_rgb(1, 0.40, 0.11, 0.14); ctx.set_source(g); ctx.fill()

SKIN = (0.96, 0.78, 0.62)
def sleeper(ctx, T, awake=0.0):
    """Homme assoupi sur le canapé (ventre plein, tête penchée, bouche entrouverte)."""
    x, y = W * 0.45, H * 0.415
    br = 1 + 0.025 * math.sin(T * 2.2)
    # bras + torse (pull)
    ctx.save(); ctx.translate(x, y); ctx.scale(br, br)
    ctx.new_path(); ellipse(ctx, 0, 0, W * 0.15, H * 0.085)
    g = cairo.LinearGradient(0, -H * 0.08, 0, H * 0.08); g.add_color_stop_rgb(0, 0.95, 0.62, 0.20); g.add_color_stop_rgb(1, 0.72, 0.40, 0.10); ctx.set_source(g); ctx.fill()
    for k in (-1, 0, 1):   # rayures du pull
        ctx.new_path(); ctx.arc(0, -H * 0.02 + k * H * 0.035, W * 0.15, 0.15 * math.pi, 0.85 * math.pi); ctx.set_line_width(9 * U); rgba(ctx, (0.55, 0.28, 0.08), 0.35); ctx.stroke()
    for sx in (-1, 1):
        ctx.new_path(); ctx.move_to(sx * W * 0.13, -H * 0.05); ctx.curve_to(sx * W * 0.17, H * 0.01, sx * W * 0.10, H * 0.04, sx * W * 0.03, H * 0.035)
        ctx.set_line_width(34 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.85, 0.52, 0.15), 1); ctx.stroke()
        circle(ctx, sx * W * 0.025, H * 0.035, 20 * U, SKIN, 1)
    ctx.restore()
    # tête penchée
    hx, hy, r = x - W * 0.07, y - H * 0.105, W * 0.072
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(-0.32 * (1 - awake))
    ctx.rectangle(-14 * U, r * 0.6, 28 * U, r * 0.6); rgba(ctx, SKIN, 1); ctx.fill()
    circle(ctx, 0, 0, r, SKIN, 1)
    ctx.new_path(); ctx.arc(0, -r * 0.12, r * 1.03, math.pi * 1.02, math.pi * 1.98); ctx.close_path(); rgba(ctx, (0.30, 0.18, 0.10), 1); ctx.fill()
    for sx in (-1, 1):   # yeux fermés
        ctx.new_path(); ctx.arc(sx * r * 0.38, -r * 0.02, r * 0.16, 0.1 * math.pi, 0.9 * math.pi); ctx.set_line_width(7 * U); rgba(ctx, DARK, 1); ctx.stroke()
        circle(ctx, sx * r * 0.62, r * 0.28, r * 0.13, (1.0, 0.55, 0.50), 0.45)
    ctx.new_path(); ellipse(ctx, r * 0.05, r * 0.45, r * 0.13, r * (0.10 + 0.03 * math.sin(T * 2.2))); rgba(ctx, (0.45, 0.12, 0.12), 1); ctx.fill()
    ctx.restore()
    return hx, hy, r

def zzz(ctx, T, x, y, a=1.0):
    for i in range(3):
        ph = (T * 0.45 + i / 3) % 1
        xx, yy = x + ph * W * 0.16, y - ph * H * 0.10
        sz = (44 + 60 * ph) * U
        text(ctx, "Z", xx, yy, sz, WHITE, a * math.sin(math.pi * ph) ** 0.8)

def table_turkey(ctx, T, halo=0.0):
    rrect(ctx, W * 0.10, H * 0.625, W * 0.80, H * 0.028, 10 * U); rgba(ctx, (0.55, 0.32, 0.17), 1); ctx.fill()
    for sx in (0.16, 0.80): ctx.rectangle(W * sx, H * 0.65, W * 0.04, H * 0.05); rgba(ctx, (0.42, 0.24, 0.12), 1); ctx.fill()
    glow(ctx, W * 0.5, H * 0.57, W * 0.35, (1.0, 0.70, 0.30), 0.35)
    roast_turkey(ctx, W * 0.5, H * 0.572, W * 0.195, halo=halo, T=T)

def living_room(ctx, T, halo=0.0):
    room(ctx, T); couch_back(ctx)
    hx, hy, r = sleeper(ctx, T)
    couch_front(ctx)
    zzz(ctx, T, hx + r * 0.9, hy - r * 0.9)
    table_turkey(ctx, T, halo)

# ---------------------------------------------------------------- icônes
def drumstick(ctx, x, y, s, meat=(0.85, 0.50, 0.18), rot=-0.6):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    ctx.new_path(); ctx.move_to(0.30 * s, 0); ctx.line_to(0.85 * s, 0); ctx.set_line_width(0.13 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.98, 0.95, 0.88), 1); ctx.stroke()
    for d in (-1, 1): circle(ctx, 0.88 * s, d * 0.07 * s, 0.08 * s, (0.98, 0.95, 0.88), 1)
    ctx.new_path(); ellipse(ctx, 0, 0, 0.45 * s, 0.30 * s)
    g = cairo.RadialGradient(-0.12 * s, -0.10 * s, 0.05 * s, 0, 0, 0.5 * s); g.add_color_stop_rgb(0, *mix(meat, WHITE, 0.35)); g.add_color_stop_rgb(1, *mix(meat, DARK, 0.30))
    ctx.set_source(g); ctx.fill()
    ctx.restore()

def steak(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-0.45 * s, -0.10 * s); ctx.curve_to(-0.40 * s, -0.40 * s, 0.20 * s, -0.42 * s, 0.45 * s, -0.20 * s)
    ctx.curve_to(0.60 * s, 0.05 * s, 0.35 * s, 0.35 * s, 0.0, 0.30 * s); ctx.curve_to(-0.30 * s, 0.28 * s, -0.50 * s, 0.15 * s, -0.45 * s, -0.10 * s); ctx.close_path()
    rgba(ctx, (0.98, 0.92, 0.80), 1); ctx.fill_preserve(); ctx.save(); ctx.clip()
    ctx.new_path(); ellipse(ctx, -0.02 * s, -0.04 * s, 0.42 * s, 0.26 * s)
    g = cairo.RadialGradient(-0.1 * s, -0.1 * s, 0.05 * s, 0, 0, 0.45 * s); g.add_color_stop_rgb(0, 0.72, 0.28, 0.20); g.add_color_stop_rgb(1, 0.42, 0.14, 0.10); ctx.set_source(g); ctx.fill()
    for k in range(3):
        ctx.new_path(); ctx.move_to(-0.30 * s + k * 0.18 * s, -0.25 * s); ctx.line_to(-0.10 * s + k * 0.18 * s, 0.15 * s); ctx.set_line_width(0.04 * s); rgba(ctx, (0.25, 0.08, 0.05), 0.7); ctx.stroke()
    ctx.restore(); ctx.restore()

def plate_icon(ctx, x, y, s):
    ctx.new_path(); ellipse(ctx, x, y, s, s * 0.42); rgba(ctx, WHITE, 0.95); ctx.fill()
    ctx.new_path(); ellipse(ctx, x, y, s * 0.72, s * 0.30); ctx.set_line_width(4 * U); rgba(ctx, (0.75, 0.77, 0.85), 1); ctx.stroke()

def sandwich(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ellipse(ctx, 0, 0.30 * s, 0.95 * s, 0.22 * s); rgba(ctx, (0.90, 0.62, 0.30), 1); ctx.fill()        # pain du bas
    ctx.new_path()                                                                                                    # salade
    for j in range(13):
        ctx.line_to(-0.95 * s + j * 0.158 * s, 0.10 * s + (0.08 * s if j % 2 else -0.02 * s))
    ctx.line_to(0.95 * s, 0.22 * s); ctx.line_to(-0.95 * s, 0.22 * s); ctx.close_path(); rgba(ctx, (0.35, 0.75, 0.30), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, 0, 0.05 * s, 0.98 * s, 0.17 * s); rgba(ctx, (0.92, 0.70, 0.35), 1); ctx.fill()        # poulet pané
    ctx.new_path(); ellipse(ctx, 0, -0.18 * s, 0.98 * s, 0.38 * s); ctx.rectangle(-0.98 * s, -0.18 * s, 1.96 * s, 0.22 * s)
    g = cairo.LinearGradient(0, -0.56 * s, 0, 0.04 * s); g.add_color_stop_rgb(0, 0.98, 0.72, 0.35); g.add_color_stop_rgb(1, 0.80, 0.48, 0.18); ctx.set_source(g); ctx.fill()
    for (sx_, sy_) in ((-0.4, -0.3), (0.0, -0.42), (0.35, -0.28), (-0.15, -0.18), (0.55, -0.12)):
        ctx.new_path(); ellipse(ctx, sx_ * s, sy_ * s, 0.05 * s, 0.025 * s, 0.4); rgba(ctx, (1.0, 0.96, 0.85), 1); ctx.fill()
    ctx.restore()

def moon(ctx, x, y, r, a=1.0):
    glow(ctx, x, y, r * 2.2, (0.75, 0.70, 1.0), 0.45 * a)
    ctx.save(); ctx.push_group()
    circle(ctx, x, y, r, (1.0, 0.95, 0.70), 1)
    ctx.set_operator(cairo.OPERATOR_CLEAR); circle(ctx, x + r * 0.45, y - r * 0.25, r * 0.85, WHITE, 1)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()

def big_plate(ctx, x, y, R, k_items):
    """Assiette de Thanksgiving vue de dessus ; les aliments arrivent un à un (k_items 0→1)."""
    glow(ctx, x, y, R * 1.3, (1.0, 0.75, 0.40), 0.35)
    circle(ctx, x, y + R * 0.04, R * 1.02, (0, 0, 0), 0.30)
    circle(ctx, x, y, R, (0.97, 0.97, 1.0), 1); ctx.new_path(); ctx.arc(x, y, R * 0.78, 0, 2 * math.pi); ctx.set_line_width(5 * U); rgba(ctx, (0.80, 0.82, 0.90), 1); ctx.stroke()
    items = []
    def it(i, fn):
        kk = clamp(k_items * 6 - i)
        if kk <= 0: return
        ctx.save(); sc = 0.4 + 0.6 * ease(kk); ctx.translate(x, y); ctx.scale(sc, sc); ctx.translate(-x, -y); fn(); ctx.restore()
    def turkey_slices():
        for j in range(3):
            ctx.new_path(); ellipse(ctx, x - R * 0.30 + j * R * 0.12, y - R * 0.30 + j * R * 0.05, R * 0.30, R * 0.17, -0.3)
            rgba(ctx, (0.95, 0.85, 0.70), 1); ctx.fill_preserve(); ctx.set_line_width(6 * U); rgba(ctx, (0.80, 0.55, 0.30), 1); ctx.stroke()
    def mash():
        circle(ctx, x + R * 0.30, y - R * 0.25, R * 0.27, (0.98, 0.95, 0.85), 1); circle(ctx, x + R * 0.30, y - R * 0.27, R * 0.13, (0.55, 0.32, 0.15), 1)
    def stuffing():
        rr = random.Random(7)
        for _ in range(16): circle(ctx, x - R * 0.28 + rr.uniform(-1, 1) * R * 0.18, y + R * 0.28 + rr.uniform(-1, 1) * R * 0.14, R * 0.07, (0.62 + rr.uniform(-.08, .08), 0.40, 0.18), 1)
    def beans():
        for j in range(6):
            ctx.new_path(); ellipse(ctx, x + R * 0.18 + j * R * 0.06, y + R * 0.30, R * 0.035, R * 0.20, 0.5); rgba(ctx, (0.25, 0.60, 0.25), 1); ctx.fill()
    def cranberry():
        circle(ctx, x + R * 0.02, y + R * 0.02, R * 0.15, (0.70, 0.05, 0.15), 1); circle(ctx, x - R * 0.03, y - R * 0.02, R * 0.05, (1.0, 0.5, 0.55), 0.6)
    def roll():
        ctx.new_path(); ellipse(ctx, x + R * 0.58, y + R * 0.02, R * 0.16, R * 0.13); rgba(ctx, (0.92, 0.62, 0.28), 1); ctx.fill()
        ctx.new_path(); ellipse(ctx, x + R * 0.55, y - R * 0.02, R * 0.08, R * 0.04); rgba(ctx, (1.0, 0.85, 0.55), 1); ctx.fill()
    for i, fn in enumerate((turkey_slices, mash, stuffing, beans, cranberry, roll)): it(i, fn)

def pie_slice(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-0.55 * s, 0.30 * s); ctx.line_to(0.55 * s, 0.30 * s); ctx.line_to(0.0, -0.45 * s); ctx.close_path()
    g = cairo.LinearGradient(0, -0.45 * s, 0, 0.3 * s); g.add_color_stop_rgb(0, 0.95, 0.58, 0.20); g.add_color_stop_rgb(1, 0.82, 0.42, 0.12); ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.move_to(-0.60 * s, 0.30 * s); ctx.line_to(0.60 * s, 0.30 * s); ctx.set_line_width(0.14 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.88, 0.68, 0.40), 1); ctx.stroke()
    circle(ctx, 0, -0.02 * s, 0.13 * s, WHITE, 1); circle(ctx, 0.08 * s, -0.10 * s, 0.09 * s, WHITE, 1)
    ctx.restore()

def wine_glass(ctx, x, y, s):
    ctx.save(); ctx.translate(x, y)
    ctx.new_path(); ctx.move_to(-0.32 * s, -0.45 * s); ctx.curve_to(-0.34 * s, -0.05 * s, -0.15 * s, 0.05 * s, 0, 0.05 * s); ctx.curve_to(0.15 * s, 0.05 * s, 0.34 * s, -0.05 * s, 0.32 * s, -0.45 * s); ctx.close_path()
    rgba(ctx, (0.85, 0.90, 1.0), 0.35); ctx.fill_preserve(); ctx.set_line_width(5 * U); rgba(ctx, WHITE, 0.9); ctx.stroke()
    ctx.new_path(); ctx.move_to(-0.31 * s, -0.25 * s); ctx.curve_to(-0.30 * s, -0.02 * s, -0.12 * s, 0.03 * s, 0, 0.03 * s); ctx.curve_to(0.12 * s, 0.03 * s, 0.30 * s, -0.02 * s, 0.31 * s, -0.25 * s); ctx.close_path()
    rgba(ctx, (0.55, 0.05, 0.15), 1); ctx.fill()
    ctx.new_path(); ctx.move_to(0, 0.05 * s); ctx.line_to(0, 0.38 * s); ctx.set_line_width(0.05 * s); rgba(ctx, WHITE, 0.9); ctx.stroke()
    ctx.new_path(); ellipse(ctx, 0, 0.40 * s, 0.22 * s, 0.05 * s); rgba(ctx, WHITE, 0.9); ctx.fill()
    ctx.restore()

def carbs_icon(ctx, x, y, s):
    ctx.new_path(); ellipse(ctx, x, y + 0.20 * s, 0.55 * s, 0.16 * s); rgba(ctx, (0.75, 0.80, 0.90), 1); ctx.fill()   # bol
    circle(ctx, x, y + 0.05 * s, 0.42 * s, (0.98, 0.95, 0.85), 1)                                                     # purée
    circle(ctx, x, y - 0.02 * s, 0.16 * s, (0.95, 0.80, 0.30), 1)                                                     # beurre
    ctx.rectangle(x - 0.60 * s, y + 0.05 * s, 1.2 * s, 0.30 * s); rgba(ctx, (0.75, 0.80, 0.90), 1); ctx.fill()
    for d in (-1, 1):   # petits pains
        ctx.new_path(); ellipse(ctx, x + d * 0.62 * s, y + 0.28 * s, 0.26 * s, 0.20 * s); rgba(ctx, (0.92, 0.62, 0.28), 1); ctx.fill()
        ctx.new_path(); ellipse(ctx, x + d * 0.60 * s, y + 0.22 * s, 0.13 * s, 0.06 * s); rgba(ctx, (1.0, 0.85, 0.55), 1); ctx.fill()

def sleepy_face(ctx, x, y, r, k):
    circle(ctx, x, y, r, (1.0, 0.82, 0.30), 1)
    lid = 0.15 + 0.85 * k
    for sx in (-1, 1):
        ex = x + sx * r * 0.36
        circle(ctx, ex, y - r * 0.10, r * 0.15, WHITE, 1); circle(ctx, ex, y - r * 0.06, r * 0.08, DARK, 1)
        ctx.rectangle(ex - r * 0.17, y - r * 0.27, r * 0.34, r * 0.32 * lid); rgba(ctx, (0.92, 0.70, 0.22), 1); ctx.fill()
    ctx.new_path(); ellipse(ctx, x, y + r * 0.42, r * 0.16 * (0.6 + 0.4 * k), r * 0.12 * (0.4 + 0.6 * k)); rgba(ctx, (0.45, 0.12, 0.12), 1); ctx.fill()

# ---------------------------------------------------------------- scènes
def title2(ctx, l1, l2, y1=0.105, y2=0.180, c2=GOLD, a=1.0):
    if a <= 0: return
    ctx.push_group()
    poster_text(ctx, l1, W * 0.47, H * y1, 150 * U, WHITE, W * 0.86)
    poster_text(ctx, l2, W * 0.47, H * y2, 170 * U, c2, W * 0.86)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

def myth_scene(ctx, T, k_tryp, k_amino, k_sleep):
    vgrad(ctx, (0.32, 0.12, 0.20), (0.10, 0.04, 0.10))
    roast_turkey(ctx, W * 0.47, H * 0.33, W * 0.30, T=T)
    if k_tryp > 0:
        leader(ctx, W * 0.47, H * 0.215, W * 0.47, H * 0.250, (0.95, 0.40, 0.45), 1.0, k_tryp)
        pill(ctx, "TRYPTOPHAN", W * 0.47, H * 0.135, (0.95, 0.40, 0.45), 72, 1.0, k_tryp, fg=WHITE)
    if k_amino > 0: text(ctx, "AN AMINO ACID", W * 0.47, H * 0.188, 46 * U, (1.0, 0.85, 0.85), ease(k_amino))
    if k_sleep > 0:
        ax = W * 0.47
        ctx.new_path(); ctx.move_to(ax, H * 0.48); ctx.line_to(ax, H * (0.48 + 0.045 * ease(k_sleep))); ctx.set_line_width(12 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, WHITE, 0.9); ctx.stroke()
        moon(ctx, W * 0.20, H * 0.585, 58 * U * ease(k_sleep), k_sleep)
        pill(ctx, "SLEEP HORMONES", W * 0.57, H * 0.585, (0.60, 0.55, 1.0), 58, 1.0, k_sleep, fg=WHITE)
    tag(ctx, "Simplified illustration", 0.040)

COLS = (0.20, 0.50, 0.80)
def compare_scene(ctx, T, ks, k_same, k_sand):
    vgrad(ctx, (0.10, 0.14, 0.30), (0.03, 0.05, 0.14))
    pill(ctx, "TRYPTOPHAN", W * 0.5, H * 0.105, (0.95, 0.40, 0.45), 64, 1.0, 1.0, fg=WHITE)
    dim = 1.0 - 0.75 * ease(k_sand)
    ctx.push_group()
    names = ("TURKEY", "CHICKEN", "BEEF"); levels = (1.0, 1.0, 0.96)
    for i, (cx_, k) in enumerate(zip(COLS, ks)):
        if k <= 0: continue
        x = W * cx_; e = ease(k)
        plate_icon(ctx, x, H * 0.235, W * 0.14 * (0.6 + 0.4 * e))
        if i == 0: drumstick(ctx, x - W * 0.02, H * 0.225, W * 0.17 * e, meat=(0.78, 0.40, 0.12))
        elif i == 1: drumstick(ctx, x - W * 0.02, H * 0.225, W * 0.14 * e, meat=(0.95, 0.68, 0.30))
        else: steak(ctx, x, H * 0.225, W * 0.22 * e)
        text(ctx, names[i], x, H * 0.300, 50 * U, WHITE, e)
        bh = H * 0.20 * levels[i] * ease(clamp(k * 1.4 - 0.2)); bw = W * 0.15; bot = H * 0.56
        rrect(ctx, x - bw / 2, bot - H * 0.20, bw, H * 0.20, 18 * U); rgba(ctx, WHITE, 0.10); ctx.fill()
        if bh > 1:
            rrect(ctx, x - bw / 2, bot - bh, bw, bh, 18 * U)
            g = cairo.LinearGradient(0, bot - bh, 0, bot); g.add_color_stop_rgb(0, 1.0, 0.55, 0.60); g.add_color_stop_rgb(1, 0.80, 0.25, 0.35); ctx.set_source(g); ctx.fill()
    if k_same > 0:
        ctx.new_path(); ctx.move_to(W * 0.11, H * 0.36 - 0.5); ctx.line_to(W * 0.89, H * 0.36); ctx.set_line_width(5 * U); ctx.set_dash([16 * U, 12 * U]); rgba(ctx, WHITE, 0.7 * k_same); ctx.stroke(); ctx.set_dash([])
        pill(ctx, "≈ THE SAME", W * 0.5, H * 0.615, GOLD, 64, 1.0, k_same)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(dim)
    if k_sand > 0:
        e = ease(k_sand)
        glow(ctx, W * 0.5, H * 0.34, W * 0.45, (1.0, 0.75, 0.35), 0.45 * e)
        sandwich(ctx, W * 0.5, H * 0.34, W * 0.30 * (0.5 + 0.5 * e))
        pill(ctx, "NO NAP AFTER THIS", W * 0.5, H * 0.50, (0.35, 0.85, 0.55), 58, 1.0, k_sand)
    tag(ctx, "Simplified illustration", 0.040)

def cause_scene(ctx, T, k_plate, k_cal):
    vgrad(ctx, (0.38, 0.17, 0.12), (0.12, 0.05, 0.06))
    big_plate(ctx, W * 0.5, H * 0.275, W * 0.36, k_plate)
    if k_cal > 0:
        n = int(3000 * ease(k_cal))
        ctx.push_group()
        poster_text(ctx, f"{n:,}", W * 0.47, H * 0.515, 210 * U, GOLD, W * 0.86)
        poster_text(ctx, "CALORIES", W * 0.47, H * 0.585, 95 * U, WHITE, W * 0.80)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ease(min(1, k_cal * 3)))
        text(ctx, "ONE ESTIMATE · ONE MEAL", W * 0.47, H * 0.632, 44 * U, (1.0, 0.93, 0.86), ease(k_cal))
    tag(ctx, "Illustration", 0.040)

def carbs_scene(ctx, T, k1, k2, k3, k_drowsy):
    vgrad(ctx, (0.18, 0.12, 0.32), (0.05, 0.04, 0.12))
    for (cx_, k, lab, fn) in ((0.19, k1, "CARBS", carbs_icon), (0.51, k2, "PIE", pie_slice), (0.82, k3, "WINE", wine_glass)):
        if k <= 0: continue
        e = ease(k); x = W * cx_
        glow(ctx, x, H * 0.22, W * 0.18, (1.0, 0.75, 0.40), 0.35 * e)
        fn(ctx, x, H * 0.22, W * {carbs_icon: 0.16, pie_slice: 0.26, wine_glass: 0.30}[fn] * e)
        text(ctx, lab, x, H * 0.325, 58 * U, WHITE, e)
    lvl = 0.30 * ease(k1) + 0.30 * ease(k2) + 0.30 * ease(k3) + 0.10 * ease(k_drowsy)
    bx, by, bw, bh = W * 0.14, H * 0.43, W * 0.56, H * 0.05
    rrect(ctx, bx, by, bw, bh, bh / 2); rgba(ctx, WHITE, 0.15); ctx.fill()
    if lvl > 0.01:
        rrect(ctx, bx, by, bw * lvl, bh, bh / 2)
        g = cairo.LinearGradient(bx, 0, bx + bw, 0); g.add_color_stop_rgb(0, 1.0, 0.85, 0.30); g.add_color_stop_rgb(1, 0.65, 0.45, 1.0); ctx.set_source(g); ctx.fill()
    text(ctx, "SLEEPINESS", bx, by - 40 * U, 42 * U, (0.85, 0.85, 1.0), 0.9, align="l")
    sleepy_face(ctx, W * 0.82, by + bh / 2, 72 * U, lvl)
    if k_drowsy > 0: pill(ctx, "DROWSY", W * 0.47, H * 0.56, (0.65, 0.45, 1.0), 72, 1.0, k_drowsy, fg=WHITE)
    tag(ctx, "Simplified illustration", 0.040)

# ---------------------------------------------------------------- montage
T_B0 = SENT("myth") - 0.08
T_C0 = SENT("compare") - 0.08
T_D0 = SENT("cause") - 0.08
T_E0 = SENT("carbs") - 0.08
T_F0 = SENT("close") - 0.08
T_CTA = END_T - 2.2

def master(ctx, T):
    if T < T_B0:                                         # A — la sieste après le repas (image 1)
        living_room(ctx, T)
        title2(ctx, "NOT THE", "TURKEY")
        if T > 1.2: tag(ctx, "Illustration", 0.040)
    elif T < T_C0:                                       # B — on accuse le tryptophane
        myth_scene(ctx, T, prog(T, WT("tryptophan") - 0.25, WT("tryptophan") + 0.15), prog(T, WT("amino") - 0.2, WT("amino") + 0.2),
                   prog(T, WT("sleep") - 0.25, WT("sleep") + 0.15))
    elif T < T_D0:                                       # C — dinde = poulet ≈ bœuf ; le sandwich au poulet
        ks = (prog(T, T_C0, T_C0 + 0.5), prog(T, WT("chicken") - 0.25, WT("chicken") + 0.35), prog(T, WT("beef") - 0.25, WT("beef") + 0.35))
        compare_scene(ctx, T, ks, prog(T, WT("beef") + 0.35, WT("beef") + 0.65), prog(T, WT("sandwich") - 0.6, WT("sandwich") - 0.2))
    elif T < T_E0:                                       # D — le vrai coupable : le repas (≈ 3 000 kcal)
        cause_scene(ctx, T, prog(T, T_D0, T_D0 + 1.4), prog(T, WT("three") - 0.2, WT("calories") + 0.2))
    elif T < T_F0:                                       # E — glucides, tarte, vin → somnolence
        carbs_scene(ctx, T, prog(T, WT("carbs") - 0.25, WT("carbs") + 0.15), prog(T, WT("pie") - 0.2, WT("pie") + 0.15),
                    prog(T, WT("wine") - 0.2, WT("wine") + 0.15), prog(T, WT("drowsy") - 0.25, WT("drowsy") + 0.15))
    else:                                                # F — retour au salon : la dinde, innocente
        k_inn = prog(T, WT("innocent") - 0.3, WT("innocent") + 0.2)
        living_room(ctx, T, halo=k_inn)
        if k_inn > 0: pill(ctx, "INNOCENT", W * 0.76, H * 0.425, GOLD, 64, 1.0, k_inn)
        title2(ctx, "HAPPY", "THANKSGIVING!", a=prog(T, WT("happy") - 0.2, WT("happy") + 0.2))
        tag(ctx, "Illustration", 0.040)
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            cta_lines(ctx, ("Follow Factora for more", "food myths."), W * 0.46, (H * 0.765, H * 0.797), 50, kc)

T_COVER = 0.6
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t
def _scene(name):
    def f(ctx, t, d): master(ctx, _abs_t(name, t))
    return f
SCENES = {sg["scene"]: _scene(sg["scene"]) for sg in _TLL}
SHORT_SCENES = [sg["scene"] for sg in _TLL]

def cover(ctx):
    """Affiche : la sieste et la dinde, « IT'S NOT THE TURKEY » + « SO WHY ARE YOU SLEEPY? » (sans donner la cause) ;
    tout l'essentiel entre 14 % et 86 % de la hauteur."""
    living_room(ctx, 1.0)
    title2(ctx, "IT'S NOT", "THE TURKEY", y1=0.175, y2=0.250)
    font(ctx, 58 * U); txt = "SO WHY ARE YOU SLEEPY?"; w_ = ctx.text_extents(txt).width + 80 * U; h_ = 112 * U; y_ = H * 0.800
    glow(ctx, W * 0.47, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.47 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.47, y_, 58 * U, DARK)
