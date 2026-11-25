exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text (aucune image extérieure n'est chargée)
# Épisode 051 (Short seul, 9:16, ~30 s) — qui survit le plus longtemps sans manger ? (sujet choisi par Nazik le 2026-11-25
# d'après un Short à succès ; demande vérifiée : 2,5 M / 870 k / 276 k / 58 k vues en anglais). Stratégie 30 jours : image 1
# = les deux naufragés sur l'île (≥ 75 % de la largeur) + « WHO LASTS LONGER? » (3 mots) ; dessins 100 % faits ici,
# personnages inventés traités avec respect (aucune moquerie) ; un plan toutes les ~4–6 s ; fin = retour à l'île.
# Faits : avec de l'eau mais sans nourriture, la personne qui a le plus de réserves de graisse tient en général plus longtemps ;
# 1 livre de graisse ≈ 3 500 kcal (approximation classique) ≈ près de 2 jours d'énergie au repos ; le corps consomme aussi
# ses protéines (muscles, y compris le cœur), d'où une limite même avec beaucoup de graisse ; record médicalement suivi :
# un Écossais, 382 jours de jeûne (1965–1966), de 456 à 180 livres (−276 lb), avec vitamines et suivi hospitalier
# (Stewart & Fleming, Postgraduate Medical Journal, 1973). Aucun conseil médical ; mention « Never try this alone ».
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


# ---------------------------------------------------------------- l'île
_RI = random.Random(51)
def island(ctx, T):
    vgrad(ctx, (0.45, 0.78, 0.98), (0.85, 0.95, 1.0), 0, H * 0.50)
    glow(ctx, W * 0.80, H * 0.10, W * 0.40, (1.0, 0.95, 0.70), 0.6); circle(ctx, W * 0.80, H * 0.10, 85 * U, (1.0, 0.93, 0.55), 1)
    for (cx_, cy_, r, sp) in ((0.15, 0.08, 80, 12), (0.50, 0.14, 60, 18)):
        xx = (cx_ * W + T * sp * U) % (W * 1.2) - W * 0.1
        for d in (-1, 0, 1): circle(ctx, xx + d * r * 0.8 * U, H * cy_ + abs(d) * 15 * U, r * U * (0.8 if d else 1), WHITE, 0.9)
    ctx.rectangle(0, H * 0.36, W, H); g = cairo.LinearGradient(0, H * 0.36, 0, H); g.add_color_stop_rgb(0, 0.10, 0.55, 0.80); g.add_color_stop_rgb(1, 0.02, 0.25, 0.50); ctx.set_source(g); ctx.fill()
    for k in range(9):   # vagues
        y = H * (0.40 + k * 0.065); ph = T * 1.2 + k
        ctx.new_path()
        for j in range(41):
            x = W * j / 40; yy = y + 8 * U * math.sin(j * 0.6 + ph)
            (ctx.line_to if j else ctx.move_to)(x, yy)
        ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.18); ctx.stroke()
    ctx.new_path(); ellipse(ctx, W * 0.5, H * 0.66, W * 0.66, H * 0.085)
    g = cairo.LinearGradient(0, H * 0.55, 0, H * 0.72); g.add_color_stop_rgb(0, 0.98, 0.88, 0.62); g.add_color_stop_rgb(1, 0.88, 0.74, 0.45); ctx.set_source(g); ctx.fill()
    # palmier
    tx, ty = W * 0.10, H * 0.62
    ctx.new_path(); ctx.move_to(tx, ty); ctx.curve_to(tx + 20 * U, ty - H * 0.10, tx + 60 * U, ty - H * 0.20, tx + 40 * U, ty - H * 0.30)
    ctx.set_line_width(34 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.55, 0.38, 0.22), 1); ctx.stroke()
    px, py = tx + 40 * U, ty - H * 0.30
    for k in range(6):
        a = -math.pi * 0.95 + k * 0.38 + 0.05 * math.sin(T * 1.5 + k)
        ctx.new_path(); ctx.move_to(px, py); ctx.curve_to(px + math.cos(a) * 120 * U, py + math.sin(a) * 120 * U - 40 * U, px + math.cos(a) * 220 * U, py + math.sin(a) * 200 * U, px + math.cos(a) * 260 * U, py + math.sin(a) * 260 * U + 40 * U)
        ctx.set_line_width(26 * U); rgba(ctx, (0.20, 0.62, 0.28), 1); ctx.stroke()
    for d in (-1, 1): circle(ctx, px + d * 18 * U, py + 18 * U, 18 * U, (0.45, 0.30, 0.15), 1)

def person(ctx, x, y, s, shirt, skin, hair, big=False, T=0.0, ph=0.0, a=1.0, beard=False):
    """Naufragé de face, pieds en (x, y), s = hauteur totale. big : silhouette corpulente (dessin respectueux)."""
    ctx.save(); ctx.push_group()
    sway = 3 * U * math.sin(T * 1.6 + ph)
    x += sway
    tw = (0.34 if big else 0.22) * s; th = 0.33 * s
    hy = y - 0.86 * s; hr = 0.085 * s
    # jambes et pieds
    for sx in (-1, 1):
        lx = x + sx * (0.07 if big else 0.05) * s
        ctx.new_path(); ctx.move_to(lx, y - 0.36 * s); ctx.line_to(lx, y - 0.02 * s); ctx.set_line_width((0.085 if big else 0.06) * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, skin, 1); ctx.stroke()
        ctx.new_path(); ellipse(ctx, lx + sx * 0.02 * s, y, 0.045 * s, 0.018 * s); rgba(ctx, mix(skin, DARK, 0.1), 1); ctx.fill()
    # short
    ctx.new_path(); rrect(ctx, x - tw * 0.48, y - 0.46 * s, tw * 0.96, 0.17 * s, 0.03 * s); rgba(ctx, (0.85, 0.75, 0.55), 1); ctx.fill()
    # bras
    for sx in (-1, 1):
        ax = x + sx * tw * 0.47
        ctx.new_path(); ctx.move_to(ax, y - 0.74 * s); ctx.curve_to(ax + sx * 0.05 * s, y - 0.62 * s, ax + sx * 0.05 * s, y - 0.52 * s, ax + sx * 0.03 * s, y - 0.44 * s)
        ctx.set_line_width((0.07 if big else 0.055) * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, skin, 1); ctx.stroke()
    # t-shirt (torse)
    ctx.new_path()
    if big: ellipse(ctx, x, y - 0.60 * s, tw * 0.52, th * 0.52)
    else: rrect(ctx, x - tw * 0.5, y - 0.78 * s, tw, th, 0.05 * s)
    g = cairo.LinearGradient(0, y - 0.78 * s, 0, y - 0.44 * s); g.add_color_stop_rgb(0, *shirt); g.add_color_stop_rgb(1, *mix(shirt, DARK, 0.25)); ctx.set_source(g); ctx.fill()
    for sx in (-1, 1):   # manches
        ctx.new_path(); ellipse(ctx, x + sx * tw * 0.47, y - 0.73 * s, 0.05 * s, 0.045 * s); rgba(ctx, shirt, 1); ctx.fill()
    # cou + tête
    ctx.rectangle(x - 0.025 * s, hy + hr * 0.7, 0.05 * s, 0.06 * s); rgba(ctx, skin, 1); ctx.fill()
    circle(ctx, x, hy, hr, skin, 1)
    ctx.new_path(); ctx.arc(x, hy - hr * 0.15, hr * 1.02, math.pi * 1.05, math.pi * 1.95); ctx.close_path(); rgba(ctx, hair, 1); ctx.fill()
    if beard:
        ctx.new_path(); ctx.arc(x, hy + hr * 0.15, hr * 0.95, 0.1 * math.pi, 0.9 * math.pi); ctx.close_path(); rgba(ctx, hair, 1); ctx.fill()
    for sx in (-1, 1):
        circle(ctx, x + sx * hr * 0.38, hy - hr * 0.05, hr * 0.11, DARK, 1)
    ctx.new_path(); ctx.arc(x, hy + hr * 0.25, hr * 0.32, 0.15 * math.pi, 0.85 * math.pi); ctx.set_line_width(0.012 * s); rgba(ctx, DARK, 1); ctx.stroke()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()

THIN = dict(shirt=(0.95, 0.45, 0.30), skin=(0.96, 0.78, 0.62), hair=(0.18, 0.13, 0.10))
BIG = dict(shirt=(0.20, 0.62, 0.62), skin=(0.93, 0.74, 0.58), hair=(0.40, 0.25, 0.15))
def castaways(ctx, T, a_thin=1.0, a_big=1.0, glow_big=0.0, fy=0.675, s=0.45):
    if glow_big > 0: glow(ctx, W * 0.70, H * (fy - 0.20), W * 0.45, GOLD, 0.55 * glow_big)
    person(ctx, W * 0.30, H * fy, H * s, T=T, ph=0.0, a=a_thin, **THIN)
    person(ctx, W * 0.70, H * fy, H * s, T=T, ph=1.3, a=a_big, big=True, beard=True, **BIG)

def plate(ctx, x, y, r, a=1.0):
    ctx.new_path(); ellipse(ctx, x, y, r, r * 0.35); rgba(ctx, WHITE, a); ctx.fill_preserve(); ctx.set_line_width(4 * U); rgba(ctx, (0.6, 0.6, 0.65), a); ctx.stroke()
    ctx.new_path(); ellipse(ctx, x, y, r * 0.65, r * 0.22); ctx.set_line_width(3 * U); rgba(ctx, (0.75, 0.75, 0.8), a); ctx.stroke()

def island_scene(ctx, T, title=True, k_water=0.0, k_food=0.0, glow_big=0.0, a_thin=1.0):
    island(ctx, T)
    castaways(ctx, T, a_thin=a_thin, glow_big=glow_big)
    if title:
        poster_text(ctx, "WHO LASTS", W * 0.47, H * 0.105, 165 * U, WHITE, W * 0.86)
        poster_text(ctx, "LONGER?", W * 0.47, H * 0.180, 175 * U, GOLD, W * 0.86)
    icons(ctx, k_water, k_food, H * 0.43)

def icons(ctx, k_water, k_food, y):
    """eau ✓ (à gauche) / nourriture ✗ (à droite), de part et d'autre des naufragés."""
    if k_water > 0:
        ctx.save(); ctx.translate(W * 0.11, y); ctx.scale(ease(k_water), ease(k_water))
        circle(ctx, 0, 0, 62 * U, WHITE, 0.95); drop(ctx, 0, 6 * U, 34 * U, (0.10, 0.50, 0.90))
        ctx.new_path(); ctx.move_to(30 * U, 40 * U); ctx.line_to(46 * U, 58 * U); ctx.line_to(78 * U, 22 * U); ctx.set_line_width(12 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.15, 0.75, 0.30), 1); ctx.stroke()
        ctx.restore()
    if k_food > 0:
        ctx.save(); ctx.translate(W * 0.91, y); ctx.scale(ease(k_food), ease(k_food))
        circle(ctx, 0, 0, 62 * U, WHITE, 0.95); plate(ctx, 0, 6 * U, 44 * U); no_sign(ctx, 0, 0, 58 * U)
        ctx.restore()

# ---------------------------------------------------------------- graisse = nourriture en réserve
def fat_block(ctx, x, y, w, h, k):
    ctx.save(); ctx.translate(x, y); ctx.scale(0.6 + 0.4 * ease(k), 0.6 + 0.4 * ease(k))
    ctx.new_path(); ctx.move_to(-w / 2, -h / 2 + h * 0.18); ctx.line_to(-w / 2 + w * 0.18, -h / 2); ctx.line_to(w / 2, -h / 2); ctx.line_to(w / 2, h / 2 - h * 0.18); ctx.line_to(w / 2 - w * 0.18, h / 2); ctx.line_to(-w / 2, h / 2); ctx.close_path()
    rgba(ctx, (0.95, 0.80, 0.30), k); ctx.fill()
    ctx.new_path(); rrect(ctx, -w / 2, -h / 2 + h * 0.18, w - w * 0.18, h - h * 0.18, 10 * U)
    g = cairo.LinearGradient(0, -h / 2, 0, h / 2); g.add_color_stop_rgb(0, 1.0, 0.93, 0.60); g.add_color_stop_rgb(1, 0.98, 0.82, 0.38); ctx.set_source(g); ctx.fill()
    for (cx_, cy_, r) in ((-0.2, 0.1, 0.10), (0.1, 0.25, 0.07), (0.15, -0.05, 0.08), (-0.3, -0.15, 0.06)):
        circle(ctx, cx_ * w, cy_ * h + h * 0.09, r * w, (1.0, 0.97, 0.80), 0.6)
    text(ctx, "1 LB", -w * 0.09, h * 0.02, 120 * U, (0.55, 0.38, 0.08), 1.0)
    text(ctx, "OF FAT", -w * 0.09, h * 0.02 + 105 * U, 58 * U, (0.55, 0.38, 0.08), 1.0)
    ctx.restore()

def fuel_scene(ctx, T, k_fat, k_cal, k_days):
    vgrad(ctx, (0.10, 0.14, 0.30), (0.03, 0.05, 0.14))
    glow(ctx, W * 0.5, H * 0.30, W * 0.6, (1.0, 0.80, 0.30), 0.18)
    if k_fat > 0: fat_block(ctx, W * 0.48, H * 0.245, W * 0.80, H * 0.20, k_fat)
    if k_cal > 0:
        n = int(3500 * ease(k_cal))
        ctx.push_group()
        poster_text(ctx, f"{n:,}", W * 0.47, H * 0.445, 200 * U, GOLD, W * 0.86)
        poster_text(ctx, "CALORIES", W * 0.47, H * 0.522, 95 * U, WHITE, W * 0.80)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ease(min(1, k_cal * 3)))
    if k_days > 0:
        pill(ctx, "≈ 2 DAYS OF ENERGY", W * 0.47, H * 0.615, (0.35, 0.85, 0.55), 60, 1.0, k_days)
    tag(ctx, "Simplified illustration", 0.083)

# ---------------------------------------------------------------- muscles et cœur
def body_scene(ctx, T, k_shrink, k_heart, k_time):
    vgrad(ctx, (0.10, 0.12, 0.26), (0.03, 0.04, 0.12))
    x, y, s = W * 0.47, H * 0.67, H * 0.535
    sh = 1.0 - 0.30 * ease(k_shrink)
    hy = y - 0.88 * s
    circle(ctx, x, hy, 0.075 * s, (0.75, 0.80, 0.95), 0.9)
    ctx.new_path(); rrect(ctx, x - 0.17 * s, y - 0.78 * s, 0.34 * s, 0.38 * s, 0.06 * s); rgba(ctx, (0.75, 0.80, 0.95), 0.25); ctx.fill_preserve(); ctx.set_line_width(5 * U); rgba(ctx, (0.75, 0.80, 0.95), 0.8); ctx.stroke()
    for sx in (-1, 1):   # bras et jambes (muscles rouges qui fondent)
        for (px0, py0, px1, py1) in ((0.18, -0.74, 0.27, -0.44), (0.08, -0.40, 0.09, -0.02)):
            ctx.new_path(); ctx.move_to(x + sx * px0 * s, y + py0 * s); ctx.line_to(x + sx * px1 * s, y + py1 * s)
            ctx.set_line_width(0.095 * s * sh); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.88, 0.30, 0.35), 0.9); ctx.stroke()
            ctx.new_path(); ctx.move_to(x + sx * px0 * s, y + py0 * s); ctx.line_to(x + sx * px1 * s, y + py1 * s)
            ctx.set_line_width(0.012 * s); rgba(ctx, (1.0, 0.75, 0.75), 0.6); ctx.stroke()
    # cœur qui bat (plus faiblement)
    beat = 1 + 0.10 * (1 - 0.6 * k_heart) * max(0, math.sin(T * 7.0))
    hx, hy2, hs = x - 0.04 * s, y - 0.66 * s, 0.07 * s * beat * (1 - 0.15 * k_heart)
    glow(ctx, hx, hy2, hs * 3, (1.0, 0.25, 0.35), 0.45 * (1 - 0.5 * k_heart))
    ctx.new_path(); ctx.move_to(hx, hy2 + hs * 0.9)
    ctx.curve_to(hx - hs * 1.4, hy2 - hs * 0.1, hx - hs * 0.9, hy2 - hs * 1.2, hx, hy2 - hs * 0.45)
    ctx.curve_to(hx + hs * 0.9, hy2 - hs * 1.2, hx + hs * 1.4, hy2 - hs * 0.1, hx, hy2 + hs * 0.9); ctx.close_path()
    rgba(ctx, (0.95, 0.20, 0.30), 1); ctx.fill()
    if k_shrink > 0: pill(ctx, "MUSCLE BURNS TOO", W * 0.47, H * 0.126, (0.95, 0.40, 0.45), 54, 1.0, k_shrink, fg=WHITE)
    if k_heart > 0:
        leader(ctx, W * 0.80, H * 0.24, hx + hs, hy2, (0.95, 0.40, 0.45), 1.0, k_heart)
        pill(ctx, "EVEN THE HEART", W * 0.73, H * 0.215, (0.95, 0.40, 0.45), 44, 1.0, k_heart, fg=WHITE)
    if k_time > 0: pill(ctx, "FAT BUYS TIME", W * 0.47, H * 0.520, GOLD, 64, 1.0, k_time)
    tag(ctx, "Simplified illustration", 0.083)

# ---------------------------------------------------------------- le record (382 jours, suivi médical)
def calendar(ctx, x, y, w, h, day, flip):
    ctx.save(); ctx.translate(x, y)
    rrect(ctx, -w / 2, -h / 2, w, h, 26 * U); rgba(ctx, WHITE, 1); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h * 0.25, 26 * U); rgba(ctx, (0.90, 0.25, 0.28), 1); ctx.fill()
    ctx.rectangle(-w / 2, -h / 2 + h * 0.15, w, h * 0.10); rgba(ctx, (0.90, 0.25, 0.28), 1); ctx.fill()
    for dx in (-0.25, 0.25): circle(ctx, dx * w, -h / 2, 16 * U, (0.25, 0.25, 0.30), 1)
    text(ctx, "DAY", 0, -h / 2 + h * 0.13, 56 * U, WHITE, 1)
    fs = 230 * U if day < 100 else 200 * U
    text(ctx, str(day), 0, h * 0.12, fs, (0.15, 0.15, 0.20), 1)
    if flip > 0:   # page qui s'envole
        ctx.save(); ctx.translate(0, -h / 2 + h * 0.25); ctx.rotate(-flip * 0.6); ctx.translate(flip * w * 0.4, -flip * h * 0.3)
        rrect(ctx, -w / 2, 0, w, h * 0.75, 20 * U); rgba(ctx, (0.96, 0.96, 0.98), 1 - flip); ctx.fill(); ctx.restore()
    ctx.restore()

def record_scene(ctx, T, k_count, k_doc, k_lb):
    vgrad(ctx, (0.98, 0.90, 0.70), (0.92, 0.76, 0.50), 0, H)
    glow(ctx, W * 0.47, H * 0.33, W * 0.6, WHITE, 0.4)
    day = int(1 + 381 * ease(k_count)) if k_count > 0 else 1
    flip = (T * 8.0) % 1.0 if 0 < k_count < 1 else 0.0
    calendar(ctx, W * 0.47, H * 0.31, W * 0.56, H * 0.25, day, flip)
    if k_count >= 1:
        pill(ctx, "382 DAYS", W * 0.47, H * 0.485, (0.90, 0.25, 0.28), 70, 1.0, 1.0, fg=WHITE)
    text(ctx, "SCOTLAND · 1965–66", W * 0.47, H * 0.145, 40 * U, (0.35, 0.22, 0.10), 0.9 * ease(min(1, k_count * 3)))
    if k_doc > 0:
        pill(ctx, "DOCTORS WATCHING", W * 0.29, H * 0.565, (0.25, 0.55, 0.95), 50, 1.0, k_doc, fg=WHITE)
    if k_lb > 0:
        pill(ctx, "−276 LB", W * 0.74, H * 0.565, GOLD, 66, 1.0, k_lb)
    if k_doc > 0:
        text(ctx, "Never try this alone.", W * 0.47, H * 0.632, 46 * U, (0.40, 0.20, 0.10), ease(k_doc))

# ---------------------------------------------------------------- montage
T_B0 = SENT("answer") - 0.08
T_C0 = SENT("fuel") - 0.08
T_D0 = SENT("muscle") - 0.08
T_E0 = SENT("record") - 0.08
T_F0 = SENT("close") - 0.08
T_CTA = END_T - 2.4

def master(ctx, T):
    if T < T_B0:                                         # A — les naufragés (image 1)
        island_scene(ctx, T, True, prog(T, WT("water") - 0.15, WT("water") + 0.2), prog(T, WT("food") - 0.2, WT("food") + 0.15))
        if T > 1.2: tag(ctx, "Illustration", 0.250)
    elif T < T_C0:                                       # B — « Usually, the bigger one. »
        island_scene(ctx, T, False, 1.0, 1.0, glow_big=prog(T, T_B0, T_B0 + 0.4), a_thin=1.0 - 0.45 * prog(T, T_B0, T_B0 + 0.5))
        pill(ctx, "USUALLY HIM", W * 0.68, H * 0.165, GOLD, 64, 1.0, prog(T, WT("bigger") - 0.25, WT("bigger") + 0.1))
        tag(ctx, "Illustration", 0.083)
    elif T < T_D0:                                       # C — 1 livre de graisse = 3 500 calories ≈ 2 jours
        fuel_scene(ctx, T, prog(T, T_C0, T_C0 + 0.4), prog(T, WT("thirty-five") - 0.2, WT("calories") + 0.2), prog(T, WT("days") - 0.4, WT("days") + 0.05))
    elif T < T_E0:                                       # D — les muscles aussi, même le cœur
        body_scene(ctx, T, prog(T, WT("muscle") - 0.3, WT("muscle") + 0.5), prog(T, WT("heart") - 0.25, WT("heart") + 0.15), prog(T, WT("time") - 0.3, WT("time") + 0.05))
    elif T < T_F0:                                       # E — le record : 382 jours, suivi médical
        record_scene(ctx, T, prog(T, WT("fasted") - 0.2, WT("eighty-two") + 0.3), prog(T, WT("doctors") - 0.2, WT("doctors") + 0.2), prog(T, WT("seventy-six") - 0.2, WT("pounds") + 0.1))
    else:                                                # F — retour à l'île : la graisse, un réservoir de secours
        island_scene(ctx, T, False, 0.0, 0.0, glow_big=0.6)
        pill(ctx, "BACKUP TANK", W * 0.68, H * 0.165, GOLD, 64, 1.0, prog(T, WT("backup") - 0.2, WT("backup") + 0.15))
        tag(ctx, "Illustration", 0.083)
        kc = prog(T, T_CTA, T_CTA + 0.35)
        if kc > 0:
            font(ctx, 42 * U); txt = "FACTORA"; w_ = ctx.text_extents(txt).width + 56 * U
            rrect(ctx, W * 0.24 - w_ / 2, H * 0.165 - 31 * U, w_, 62 * U, 31 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
            text(ctx, txt, W * 0.24, H * 0.165, 42 * U, GOLD, kc)
            cta_lines(ctx, ("Follow Factora for more", "weird body facts."), W * 0.46, (H * 0.765, H * 0.797), 50, kc)

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
    """Affiche : les deux naufragés, « WHO LASTS LONGER? », eau ✓ / nourriture ✗, bandeau « NO FOOD. WATER ONLY. »
    (sans la réponse) ; tout l'essentiel entre 14 % et 86 % de la hauteur."""
    island(ctx, 1.0); castaways(ctx, 1.0, fy=0.70, s=0.38); icons(ctx, 1.0, 1.0, H * 0.47)
    poster_text(ctx, "WHO LASTS", W * 0.47, H * 0.175, 165 * U, WHITE, W * 0.86)
    poster_text(ctx, "LONGER?", W * 0.47, H * 0.250, 175 * U, GOLD, W * 0.86)
    font(ctx, 60 * U); txt = "NO FOOD. WATER ONLY."; w_ = ctx.text_extents(txt).width + 80 * U; h_ = 112 * U; y_ = H * 0.800
    glow(ctx, W * 0.47, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.47 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.47, y_, 60 * U, DARK)
