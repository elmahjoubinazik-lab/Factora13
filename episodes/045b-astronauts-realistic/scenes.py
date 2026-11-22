exec(open("engine/photo.py", encoding="utf-8").read())   # poster_text
# Épisode 045b — VERSION RÉALISTE (images Runway) de l'ép. 045, demandée par Nazik le 2026-11-22 : « des images plus
# réalistes grâce à Runway, modifie les images mais pas la mise en scène et le scénario ». Même voix, même découpage, mêmes
# textes et repères ; les dessins sont remplacés par : astronaute détouré (le MÊME dans les deux fenêtres, seul le tronc
# s'allonge, ≤ 3 %), fonds Terre / orbite, astronaute en apesanteur (plan Gen-4.5, visière fermée, pas de visage), colonne
# vertébrale réaliste (état Terre → état microgravité). Tout ce qui est texte, ligne ou mesure reste ajouté au montage.
# (En-tête de l'ép. 045 :)
# Épisode 045 (Short seul, 9:16, ~36 s) — « Why Do Astronauts Get Taller in Space? » (brief de Nazik, 2026-11-22).
# Faits : la NASA indique qu'en microgravité la colonne peut se redresser et s'allonger, d'où une hausse TEMPORAIRE de
# taille pouvant atteindre 3 % (≈ 2 in pour 6 ft) ; retour à la taille habituelle sur Terre (Spinal Ultrasound, ISS).
# Scott Kelly : « about 2 inches » rapporté par la presse (CNN, 3 mars 2016) après ~340 jours ; revenu à sa taille en
# moins de deux jours ; chiffre approximatif (d'autres comptes rendus disent ≈ 1,5 in). Pas de croissance osseuse.
# Personne réelle : jamais de visage → astronaute dessiné, visière dorée (« Illustration »). Mêmes dessin, pose et échelle
# pour la comparaison EARTH / SPACE ; seule la longueur du tronc change (≈ 3 % de la taille au maximum).
import json as _json
_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_FIRST = _TLL[0]["scene"]
_WORDS = [w for sg in _TLL for se in sg["sents"] for w in se.get("words", [])]
END_T = _TLL[-1]["end"] + 0.6
def WT(word, n=0):
    hits = [w[1] for w in _WORDS if w[0].lower().strip(".,?!") == word.lower()]
    return hits[n] if n < len(hits) else 1e9
def lerp(a, b, k): return a + (b - a) * k
DARK = (0.03, 0.02, 0.08)
SUIT = (0.95, 0.96, 0.98); SUIT_S = (0.70, 0.74, 0.82)
BONE = (0.95, 0.90, 0.80); BONE_D = (0.62, 0.54, 0.42); DISC = (0.55, 0.85, 1.0)

# ---------------------------------------------------------------- outils
def catmull_open(pts, per=16):
    q = [pts[0]] + list(pts) + [pts[-1]]; out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(per):
            u = k / per; u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in range(2)))
    out.append(pts[-1]); return out

def tag(ctx, s, a=1.0):
    font(ctx, 38 * U); w_ = ctx.text_extents(s).width + 48 * U
    x0, y0 = W * 0.055, H * 0.083
    rrect(ctx, x0, y0 - 30 * U, w_, 60 * U, 30 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, x0 + 24 * U, y0, 38 * U, (0.94, 0.96, 1.0), 0.95 * a, align="l")

def pill_txt(ctx, s, x, y, col, size=40, a=1.0, fill=False):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 50 * U; h_ = size * 1.55 * U
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); rgba(ctx, col if fill else (0.02, 0.03, 0.09), (0.95 if fill else 0.86) * a); ctx.fill()
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); ctx.set_line_width(4 * U); rgba(ctx, col, a); ctx.stroke()
    text(ctx, s, x, y, size * U, DARK if fill else col, a)

def big_label(ctx, s, x, y, size, col, a=1.0):
    if a <= 0: return
    ctx.push_group(); poster_text(ctx, s, x, y, size * U, col, W * 0.32); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

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

def band(ctx):
    rrect(ctx, W * 0.07, H * 0.676, W * 0.78, H * 0.072, 30 * U); rgba(ctx, (0.01, 0.01, 0.05), 0.55); ctx.fill()

_rs = random.Random(3)
STARS2 = [(_rs.random(), _rs.random(), _rs.uniform(1.0, 3.2), _rs.random() * 6.28) for _ in range(220)]
def space_bg(ctx, T, x0=0, y0=0, w=None, h=None, earth=True):
    w = w or W; h = h or H
    g = cairo.LinearGradient(0, y0, 0, y0 + h); g.add_color_stop_rgb(0, 0.02, 0.02, 0.07); g.add_color_stop_rgb(1, 0.05, 0.04, 0.14)
    ctx.set_source(g); ctx.rectangle(x0, y0, w, h); ctx.fill()
    for (u, v, r, ph) in STARS2:
        circle(ctx, x0 + u * w, y0 + v * h, r * U * 0.8, WHITE, 0.35 + 0.35 * math.sin(T * 1.3 + ph))
    if earth:   # limbe de la Terre en bas, halo bleu
        cx, cy, R = x0 + w * 0.5, y0 + h + w * 1.25, w * 1.42
        glow(ctx, cx, cy - R, w * 0.9, (0.30, 0.60, 1.0), 0.35)
        ctx.new_path(); ctx.arc(cx, cy, R, 0, 2 * math.pi)
        g = cairo.RadialGradient(cx, cy - R, R * 0.02, cx, cy, R); g.add_color_stop_rgb(0, 0.30, 0.55, 0.95); g.add_color_stop_rgb(0.25, 0.10, 0.30, 0.65); g.add_color_stop_rgb(1, 0.03, 0.08, 0.22)
        ctx.set_source(g); ctx.fill()
        ctx.new_path(); ctx.arc(cx, cy, R + 6 * U, 0, 2 * math.pi); ctx.set_line_width(10 * U); rgba(ctx, (0.55, 0.85, 1.0), 0.45); ctx.stroke()

def earth_bg(ctx, x0, y0, w, h, ground_y):
    g = cairo.LinearGradient(0, y0, 0, ground_y); g.add_color_stop_rgb(0, 0.20, 0.36, 0.62); g.add_color_stop_rgb(1, 0.55, 0.72, 0.90)
    ctx.set_source(g); ctx.rectangle(x0, y0, w, ground_y - y0); ctx.fill()
    g = cairo.LinearGradient(0, ground_y, 0, y0 + h); g.add_color_stop_rgb(0, 0.50, 0.52, 0.58); g.add_color_stop_rgb(1, 0.30, 0.31, 0.36)
    ctx.set_source(g); ctx.rectangle(x0, ground_y, w, y0 + h - ground_y); ctx.fill()
    for i in range(7):
        xx = x0 + w * (i + 0.5) / 7; ctx.new_path(); ctx.move_to(xx, ground_y); ctx.line_to(x0 + w * 0.5 + (xx - x0 - w * 0.5) * 2.2, y0 + h)
        ctx.set_line_width(2 * U); rgba(ctx, WHITE, 0.10); ctx.stroke()

# ---------------------------------------------------------------- astronaute (vue de face ; 1000 unités = taille ; pieds à y = 0)
TORSO_GAIN = 30.0     # 3 % de 1000 : seul le tronc (colonne) s'allonge
def astronaut(ctx, cx, feet_y, s, ext=0.0, a=1.0, ghost=False):
    if a <= 0: return
    d = TORSO_GAIN * ext
    ctx.save(); ctx.translate(cx, feet_y); ctx.scale(s, s)
    if ghost:
        ctx.push_group()
    def part(path_fn, col, line=True):
        ctx.new_path(); path_fn()
        if ghost:
            ctx.set_dash([18, 12]); ctx.set_line_width(7); rgba(ctx, CYAN, 1); ctx.stroke(); ctx.set_dash([]); return
        g = cairo.LinearGradient(-200, 0, 200, 0); g.add_color_stop_rgb(0, *mix(col, SUIT_S, 0.55)); g.add_color_stop_rgb(0.45, *col); g.add_color_stop_rgb(1, *mix(col, SUIT_S, 0.35))
        ctx.set_source(g); ctx.fill_preserve()
        if line: ctx.set_line_width(6); rgba(ctx, (0.35, 0.38, 0.46), 0.9); ctx.stroke()
        else: ctx.new_path()
    # sac à dos (derrière les épaules)
    part(lambda: rrect(ctx, -175, -790 - d, 350, 330 + d, 40), (0.84, 0.86, 0.90))
    # jambes et bottes
    for sx in (-1, 1):
        part(lambda sx=sx: (ctx.move_to(sx * 20, -470), ctx.line_to(sx * 135, -470), ctx.line_to(sx * 120, -80), ctx.line_to(sx * 35, -80), ctx.close_path()), SUIT)
        part(lambda sx=sx: rrect(ctx, sx * 128 - (88 if sx > 0 else 0) + (0 if sx > 0 else -2), -95, 92, 95, 22), (0.80, 0.82, 0.86))
        for k in (0, 1):   # plis du genou
            ctx.new_path(); ctx.move_to(sx * 40, -270 + k * 24); ctx.line_to(sx * 122, -276 + k * 24)
            if not ghost: ctx.set_line_width(5); rgba(ctx, SUIT_S, 0.8); ctx.stroke()
    # tronc (la partie qui s'allonge)
    part(lambda: rrect(ctx, -150, -770 - d, 300, 310 + d, 60), SUIT)
    part(lambda: rrect(ctx, -75, -690 - d, 150, 105, 14), (0.88, 0.90, 0.94))   # boîtier de commande
    if not ghost:
        for i, col in enumerate((CORAL, GOLD, CYAN, GREEN)):
            circle(ctx, -45 + i * 30, -655 - d, 9, col, 1)
        ctx.new_path(); ctx.move_to(-150, -500); ctx.line_to(150, -500); ctx.set_line_width(14); rgba(ctx, SUIT_S, 0.9); ctx.stroke()   # ceinture
        circle(ctx, 95, -735 - d, 24, (0.30, 0.45, 0.85), 1); circle(ctx, 95, -735 - d, 16, (0.95, 0.85, 0.4), 1)                    # écusson générique
    # bras et gants
    for sx in (-1, 1):
        part(lambda sx=sx: (ctx.move_to(sx * 140, -760 - d), ctx.line_to(sx * 205, -735 - d), ctx.line_to(sx * 238, -420), ctx.line_to(sx * 172, -410), ctx.line_to(sx * 150, -620 - d * 0.5), ctx.close_path()), SUIT)
        part(lambda sx=sx: (ctx.save(), ctx.translate(sx * 205, -390), ctx.scale(1, 1.15), ctx.arc(0, 0, 42, 0, 2 * math.pi), ctx.restore()), (0.82, 0.84, 0.88))
    # casque et visière dorée (pas de visage)
    part(lambda: rrect(ctx, -70, -800 - d, 140, 40, 16), (0.80, 0.82, 0.86))
    part(lambda: ctx.arc(0, -875 - d, 125, 0, 2 * math.pi), SUIT)
    if not ghost:
        ctx.new_path(); ctx.save(); ctx.translate(0, -870 - d); ctx.scale(1.0, 0.82); ctx.arc(0, 0, 98, 0, 2 * math.pi); ctx.restore()
        g = cairo.LinearGradient(-90, -950 - d, 90, -790 - d); g.add_color_stop_rgb(0, 1.0, 0.86, 0.45); g.add_color_stop_rgb(0.5, 0.80, 0.52, 0.12); g.add_color_stop_rgb(1, 0.45, 0.24, 0.05)
        ctx.set_source(g); ctx.fill()
        ctx.new_path(); ctx.save(); ctx.translate(-40, -905 - d); ctx.rotate(-0.5); ctx.scale(1, 0.45); ctx.arc(0, 0, 38, 0, 2 * math.pi); ctx.restore(); rgba(ctx, WHITE, 0.55); ctx.fill()
    if ghost:
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
    ctx.restore()

# ---------------------------------------------------------------- comparaison EARTH / SPACE (deux fenêtres)
WY0, WY1 = H * 0.235, H * 0.660
WIN_L = (W * 0.07, W * 0.445); WIN_R = (W * 0.475, W * 0.85)
FEET = WY1 - 80 * U
FIG_S = 0.60 * U
def head_y(ext): return FEET - (1000 + TORSO_GAIN * ext) * FIG_S

def compare(ctx, T, ext_r, right_mode="space", label_r="SPACE", ghost_ext=None, ghost_a=0.0, show_lines=1.0, space_line=0.0):
    for (x0, x1), mode, lab in ((WIN_L, "earth", "EARTH"), (WIN_R, right_mode, label_r)):
        ctx.save(); rrect(ctx, x0, WY0, x1 - x0, WY1 - WY0, 40 * U); ctx.clip()
        if mode == "earth": earth_bg(ctx, x0, WY0, x1 - x0, WY1 - WY0, FEET)
        elif mode == "space": space_bg(ctx, T, x0, WY0, x1 - x0, WY1 - WY0)
        else:   # transition espace → Terre (k = mode)
            k = float(mode); space_bg(ctx, T, x0, WY0, x1 - x0, WY1 - WY0)
            ctx.push_group(); earth_bg(ctx, x0, WY0, x1 - x0, WY1 - WY0, FEET); ctx.pop_group_to_source(); ctx.paint_with_alpha(k)
        if mode != "earth":   # repère des pieds (même niveau des deux côtés)
            ctx.new_path(); ctx.move_to(x0, FEET); ctx.line_to(x1, FEET); ctx.set_dash([14 * U, 10 * U]); ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.35); ctx.stroke(); ctx.set_dash([])
        cx = (x0 + x1) / 2
        if x0 == WIN_R[0] and ghost_ext is not None and ghost_a > 0:
            astronaut(ctx, cx, FEET, FIG_S, ghost_ext, ghost_a, ghost=True)
        astronaut(ctx, cx, FEET, FIG_S, 0.0 if x0 == WIN_L[0] else ext_r)
        ctx.restore()
        rrect(ctx, x0, WY0, x1 - x0, WY1 - WY0, 40 * U); ctx.set_line_width(5 * U); rgba(ctx, (0.80, 0.90, 1.0), 0.5); ctx.stroke()
        pill_txt(ctx, lab, cx, WY0 + 52 * U, GOLD if mode == "earth" or lab.startswith("BACK") else CYAN, 34)
    if show_lines > 0:   # lignes de taille : référence (Terre) et taille de droite
        yr = head_y(0.0); y2 = head_y(ext_r)
        ctx.new_path(); ctx.move_to(WIN_L[0] + 20 * U, yr); ctx.line_to(WIN_R[1] - 20 * U, yr); ctx.set_dash([16 * U, 10 * U]); ctx.set_line_width(4 * U)
        rgba(ctx, GOLD, 0.9 * show_lines); ctx.stroke(); ctx.set_dash([])
        if space_line > 0:   # fin : la hauteur atteinte dans l'espace reste indiquée (pointillés cyan) au-dessus de la taille actuelle
            y3 = head_y(1.0); xr0, xr1 = WIN_R[0] + 30 * U, WIN_R[1] - 30 * U
            ctx.new_path(); ctx.move_to(xr0, y3); ctx.line_to(xr1, y3); ctx.set_dash([12 * U, 8 * U]); ctx.set_line_width(5 * U); rgba(ctx, CYAN, space_line); ctx.stroke(); ctx.set_dash([])
            bx = WIN_R[1] - 52 * U
            ctx.new_path(); ctx.move_to(bx, yr); ctx.line_to(bx, y3); ctx.set_line_width(6 * U); rgba(ctx, CYAN, space_line); ctx.stroke()
            for yy in (yr, y3):
                ctx.new_path(); ctx.move_to(bx - 12 * U, yy); ctx.line_to(bx + 12 * U, yy); ctx.stroke()
        if ext_r > 0.02:
            xr0, xr1 = WIN_R[0] + 30 * U, WIN_R[1] - 30 * U
            ctx.new_path(); ctx.move_to(xr0, y2); ctx.line_to(xr1, y2); ctx.set_line_width(5 * U); rgba(ctx, CYAN, show_lines); ctx.stroke()
            bx = WIN_R[1] - 52 * U   # petite accolade entre les deux lignes
            ctx.new_path(); ctx.move_to(bx, yr); ctx.line_to(bx, y2); ctx.set_line_width(6 * U); rgba(ctx, CYAN, show_lines); ctx.stroke()
            for yy in (yr, y2):
                ctx.new_path(); ctx.move_to(bx - 12 * U, yy); ctx.line_to(bx + 12 * U, yy); ctx.stroke()
    return head_y(ext_r)

# ---------------------------------------------------------------- Scott Kelly (illustration, pas un portrait)
def kelly_shot(ctx, T, t0):
    space_bg(ctx, T)
    k = ease(prog(T, t0, t0 + 0.6)); bob = 10 * U * math.sin(T * 1.4)
    astronaut(ctx, W * 0.645, H * 0.615 + bob, 0.60 * U, 0.93)
    kn = prog(T, WT("scott") - 0.05, WT("scott") + 0.3)
    if kn > 0: pill_txt(ctx, "SCOTT KELLY", W * 0.25, H * 0.33, GOLD, 44, kn, fill=True)
    kd = prog(T, WT("two") - 0.05, WT("two") + 0.3)
    if kd > 0:
        big_label(ctx, "ABOUT 2 IN", W * 0.25, H * 0.395, 84, WHITE, kd)
        big_label(ctx, "5 CM", W * 0.25, H * 0.448, 84, CYAN, kd)
        text(ctx, "Reported case", W * 0.25, H * 0.492, 34 * U, (0.90, 0.93, 1.0), 0.9 * kd, bold=False)

# ---------------------------------------------------------------- colonne vertébrale (coupe de profil simplifiée)
SP_X, SP_BOT, SP_S = W * 0.50, H * 0.640, 0.80 * U
_EARTH_C = [(0, 0), (-30, -95), (-40, -180), (-12, -250), (30, -340), (44, -430), (24, -510), (-6, -570), (-26, -630), (-14, -700)]
_ITEMS = [(40, 120, 11)] * 5 + [(30, 96, 6)] * 12 + [(22, 76, 5)] * 7     # (hauteur vertèbre, largeur, disque) du bas vers le haut
def spine_items(m):
    """m = 0 : sur Terre (courbures marquées, disques comprimés) ; m = 1 : microgravité (plus droite, disques un peu plus épais)."""
    total = sum(h + dsc * (1 + 0.28 * m) for h, w, dsc in _ITEMS)
    pts = catmull_open([(x * (1 - 0.45 * m), y) for x, y in _EARTH_C], 20)
    L = [0.0]
    for i in range(1, len(pts)): L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    sc = total / L[-1]; pts = [(x * sc, y * sc) for x, y in pts]; L = [l * sc for l in L]
    def at(d):
        i = max(1, min(len(L) - 1, next((k for k in range(len(L)) if L[k] >= d), len(L) - 1)))
        u = (d - L[i - 1]) / max(1e-9, L[i] - L[i - 1]); p = (lerp(pts[i - 1][0], pts[i][0], u), lerp(pts[i - 1][1], pts[i][1], u))
        return p, math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])
    out, d = [], 0.0
    for h, w, dsc in _ITEMS:
        dh = dsc * (1 + 0.28 * m)
        out.append(("disc", at(d + dh / 2), w * 0.92, dh)); d += dh
        out.append(("vert", at(d + h / 2), w, h)); d += h
    return out, at(d)[0]

def spine(ctx, T, m, arrows=0.0, glow_v=0.0, ref=False):
    items, top = spine_items(m)
    ctx.save(); ctx.translate(SP_X, SP_BOT); ctx.scale(SP_S, SP_S)
    # sacrum
    ctx.new_path(); ctx.move_to(-70, 0); ctx.line_to(70, 0); ctx.line_to(40, 120); ctx.line_to(-20, 150); ctx.close_path()
    rgba(ctx, BONE, 0.9); ctx.fill_preserve(); ctx.set_line_width(5); rgba(ctx, BONE_D, 1); ctx.stroke()
    for kind, ((x, y), ang), w, h in items:
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang + math.pi / 2)
        if kind == "disc":
            rrect(ctx, -w / 2, -h / 2, w, h, h / 2); rgba(ctx, DISC, 0.85); ctx.fill()
        else:
            ctx.new_path(); ctx.move_to(w * 0.40, -h * 0.25); ctx.line_to(w * 0.95, -h * 0.05); ctx.line_to(w * 0.95, h * 0.18); ctx.line_to(w * 0.40, h * 0.25); ctx.close_path()
            rgba(ctx, mix(BONE, BONE_D, 0.25), 1); ctx.fill_preserve(); ctx.set_line_width(4); rgba(ctx, BONE_D, 1); ctx.stroke()   # apophyse (vers l'arrière)
            rrect(ctx, -w / 2, -h / 2, w, h, 10)
            g = cairo.LinearGradient(-w / 2, 0, w / 2, 0); g.add_color_stop_rgb(0, *mix(BONE, BONE_D, 0.3)); g.add_color_stop_rgb(0.5, *BONE); g.add_color_stop_rgb(1, *mix(BONE, BONE_D, 0.35))
            ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(4); rgba(ctx, BONE_D, 1); ctx.stroke()
            if glow_v > 0:
                rrect(ctx, -w / 2, -h / 2, w, h, 10); ctx.set_line_width(9); rgba(ctx, GOLD, 0.9 * glow_v); ctx.stroke()
        ctx.restore()
    ctx.restore()
    if arrows > 0:   # charge (pesanteur) : flèches discrètes vers le bas, de part et d'autre de la colonne
        for side in (-1, 1):
            for j in range(3):
                x = SP_X + side * 250 * U; y = H * (0.32 + 0.10 * j) + 10 * U * math.sin(T * 3 + j)
                ctx.new_path(); ctx.move_to(x, y - 50 * U); ctx.line_to(x, y + 30 * U); ctx.set_line_width(8 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, GOLD, 0.85 * arrows); ctx.stroke()
                ctx.new_path(); ctx.move_to(x - 20 * U, y + 14 * U); ctx.line_to(x, y + 46 * U); ctx.line_to(x + 20 * U, y + 14 * U); ctx.close_path(); rgba(ctx, GOLD, 0.85 * arrows); ctx.fill()
    return (SP_X + top[0] * SP_S, SP_BOT + top[1] * SP_S)

def spine_panel(ctx, T, m, arrows, state_lab, glow_v=0.0, show_ref=0.0):
    x0, x1 = W * 0.07, W * 0.85
    ctx.save(); rrect(ctx, x0, WY0, x1 - x0, WY1 - WY0, 40 * U); ctx.clip()
    space_bg(ctx, T, x0, WY0, x1 - x0, WY1 - WY0, earth=False)
    glow(ctx, SP_X, (WY0 + WY1) / 2, 520 * U, (0.55, 0.45, 1.0), 0.18)
    _, top0 = spine_items(0.0)
    y_ref = SP_BOT + top0[1] * SP_S
    tx, ty = spine(ctx, T, m, arrows, glow_v)
    if show_ref > 0:
        ctx.new_path(); ctx.move_to(SP_X - 230 * U, y_ref); ctx.line_to(SP_X + 230 * U, y_ref); ctx.set_dash([14 * U, 10 * U]); ctx.set_line_width(4 * U)
        rgba(ctx, GOLD, 0.9 * show_ref); ctx.stroke(); ctx.set_dash([])
        if ty < y_ref - 4 * U:
            ctx.new_path(); ctx.move_to(SP_X - 230 * U, ty); ctx.line_to(SP_X + 230 * U, ty); ctx.set_line_width(5 * U); rgba(ctx, CYAN, show_ref); ctx.stroke()
    ctx.restore()
    rrect(ctx, x0, WY0, x1 - x0, WY1 - WY0, 40 * U); ctx.set_line_width(5 * U); rgba(ctx, (0.80, 0.90, 1.0), 0.5); ctx.stroke()
    pill_txt(ctx, state_lab, W * 0.22, WY0 + 52 * U, GOLD if state_lab == "EARTH" else CYAN, 34)

# ---------------------------------------------------------------- montage (temps absolu)
T_KELLY = _TL["kelly"]["start"]; T_WHY = _TL["why"]["start"]; T_NASA = _TL["nasa"]["start"]
T_BONES = WT("it's") if WT("it's") < 1e8 else WT("not") - 0.25
T_BACK = _TL["back"]["start"]; T_END0 = _TL["end"]["start"]; T_CTA = END_T - 2.5
def master(ctx, T):
    space_bg(ctx, T, earth=False)
    tagx = "AI illustration"
    if T < T_KELLY:                                            # 1. accroche : même astronaute, EARTH / SPACE
        ext = 0.93 * ease(prog(T, WT("taller") - 0.1, WT("taller") + 0.7))
        compare(ctx, T, ext)
        ka = 1 - prog(T, T_KELLY - 0.35, T_KELLY)
        g = cairo.LinearGradient(0, 0, 0, H * 0.23); g.add_color_stop_rgba(0, 0.01, 0.01, 0.04, 0.55 * ka); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.23); ctx.fill()
        ctx.push_group(); poster_text(ctx, "TALLER", W * 0.46, H * 0.132, 128 * U, WHITE, W * 0.80); poster_text(ctx, "IN SPACE?", W * 0.46, H * 0.192, 128 * U, GOLD, W * 0.80)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ka)
    elif T < T_WHY:                                            # 2. Scott Kelly (illustration)
        kelly_shot(ctx, T, T_KELLY)
    elif T < T_NASA:                                           # 3. colonne : charge sur Terre → moins de charge en microgravité
        tagx = "Simplified AI illustration"
        t_mg = WT("microgravity"); t_un = WT("unloaded"); t_st = WT("straighten")
        arrows = 1 - prog(T, t_un - 0.1, t_un + 0.6)
        m = ease(prog(T, t_st - 0.1, t_st + 1.6))
        lab = "MICROGRAVITY" if T >= t_mg - 0.05 else "EARTH"
        spine_panel(ctx, T, m, arrows, lab, show_ref=prog(T, t_st - 0.3, t_st + 0.2))
    elif T < T_BONES - 0.05:                                   # 4. « up to 3 % »
        compare(ctx, T, 1.0)
        k3 = prog(T, WT("three") - 0.05, WT("three") + 0.3)
        if k3 > 0: pill_txt(ctx, "UP TO 3%", (WIN_R[0] + WIN_R[1]) / 2, H * 0.203, CYAN, 50, k3, fill=True)
    elif T < T_BACK:                                           # 5. pas une croissance des os
        tagx = "Simplified AI illustration"
        gv = prog(T, WT("bones") - 0.4, WT("bones"))
        spine_panel(ctx, T, 1.0, 0.0, "MICROGRAVITY", glow_v=gv, show_ref=1.0)
        kb = prog(T, WT("growth") - 0.1, WT("growth") + 0.3)
        if kb > 0: pill_txt(ctx, "NOT BONE GROWTH", W * 0.46, WY1 - 60 * U, GOLD, 40, kb, fill=True)
    elif T < T_END0:                                           # 6. retour sur Terre : la taille revient peu à peu
        kt = ease(prog(T, WT("earth") - 0.2, WT("earth") + 0.6))
        ext = 1.0 - ease(prog(T, WT("gravity") - 0.1, WT("usual") + 0.3))
        compare(ctx, T, ext, right_mode=("%.3f" % kt) if kt < 1 else "earth", label_r="BACK ON EARTH" if kt > 0.5 else "SPACE")
        ktp = prog(T, WT("return") - 0.1, WT("return") + 0.3)
        if ktp > 0: pill_txt(ctx, "TEMPORARY", W * 0.46, H * 0.205, GOLD, 52, ktp, fill=True)
    else:                                                      # 7. avant / après : la hauteur de l'espace en pointillés
        kg = prog(T, WT("space", 1) - 0.1, WT("space", 1) + 0.4)
        compare(ctx, T, 0.0, right_mode="earth", label_r="BACK ON EARTH", ghost_ext=1.0, ghost_a=0.85 * kg, space_line=kg)
        if kg > 0:
            pill_txt(ctx, "DASHED = IN SPACE", (WIN_R[0] + WIN_R[1]) / 2, WY1 - 38 * U, CYAN, 26, kg)
        ktp = 1 - prog(T, T_CTA - 0.4, T_CTA)
        if ktp > 0: pill_txt(ctx, "TEMPORARY", W * 0.46, H * 0.205, GOLD, 52, ktp, fill=True)
    band(ctx)
    tag(ctx, tagx)
    kc = prog(T, T_CTA, T_CTA + 0.35)
    if kc > 0:
        font(ctx, 44 * U); txt = "FACTORA"; w_ = ctx.text_extents(txt).width + 56 * U
        rrect(ctx, W * 0.46 - w_ / 2, H * 0.122 - 32 * U, w_, 64 * U, 32 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
        text(ctx, txt, W * 0.46, H * 0.122, 44 * U, GOLD, kc)
        cta_lines(ctx, ("Follow Factora for more", "body mysteries."), W * 0.46, (H * 0.160, H * 0.192), 52, kc)

def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return 2.6
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t
SHORT_SCENES = [s["scene"] for s in _TLL]
SCENES = {s["scene"]: (lambda name: (lambda ctx, t, d: master(ctx, _abs_t(name, t))))(s["scene"]) for s in _TLL}

def cover(ctx):
    """Affiche : le même astronaute EARTH / SPACE, l'écart de taille désigné, la question ; tout entre 14 % et 86 % de H."""
    space_bg(ctx, 2.6, earth=False)
    ctx.save(); ctx.translate(0, H * 0.078); compare(ctx, 2.6, 1.0); ctx.restore()
    g = cairo.LinearGradient(0, 0, 0, H * 0.30); g.add_color_stop_rgba(0, 0.01, 0.01, 0.04, 0.6); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.30); ctx.fill()
    poster_text(ctx, "TALLER", W * 0.46, H * 0.198, 150 * U, WHITE, W * 0.86)
    poster_text(ctx, "IN SPACE?", W * 0.46, H * 0.266, 150 * U, GOLD, W * 0.86)
    gy = head_y(1.0) + H * 0.078
    red_arrow(ctx, W * 0.93, H * 0.232, WIN_R[1] - 60 * U, gy + 8 * U, bend=0.28, width=24)
    font(ctx, 56 * U); txt = "WHAT HAPPENS TO THE SPINE?"; w_ = ctx.text_extents(txt).width + 70 * U; h_ = 110 * U
    y_ = H * 0.805
    glow(ctx, W * 0.46, y_, w_ * 0.6, GOLD, 0.30)
    rrect(ctx, W * 0.46 - w_ / 2, y_ - h_ / 2, w_, h_, h_ / 2); rgba(ctx, GOLD, 0.97); ctx.fill()
    text(ctx, txt, W * 0.46, y_, 56 * U, DARK)


# =============================================================================================================
# SURCHARGES « RÉALISTES » (images Runway) — mêmes signatures que les fonctions vectorielles ci-dessus
# =============================================================================================================
import numpy as _np
from PIL import Image as _PI
RWD = EP + "/build/rw/"
_KEEP = []
def _surf_from(im, alpha=False):
    a = _np.asarray(im.convert("RGBA")).astype(_np.float32)
    al = a[..., 3:4] / 255.0 if alpha else _np.ones(a.shape[:2] + (1,), _np.float32)
    rgb = a[..., :3] * al
    buf = _np.empty(a.shape[:2] + (4,), _np.uint8)
    buf[..., 0] = rgb[..., 2]; buf[..., 1] = rgb[..., 1]; buf[..., 2] = rgb[..., 0]; buf[..., 3] = (al[..., 0] * 255).astype(_np.uint8)
    h, w = buf.shape[:2]; _KEEP.append(buf)
    return cairo.ImageSurface.create_for_data(memoryview(buf), cairo.FORMAT_ARGB32, w, h, w * 4)
def _load(path, width=None, alpha=False):
    im = _PI.open(path)
    if width and im.width > width: im = im.resize((width, int(im.height * width / im.width)), _PI.LANCZOS)
    return _surf_from(im, alpha), im

_EARTH, _ = _load(RWD + "earth_bg.png", 900)
_SPACE, _ = _load(RWD + "space_bg.png", 900)
_CUT, _cutim = _load(RWD + "astronaut_cut.png", 1100, alpha=True)
_al = _np.asarray(_cutim.convert("RGBA"))[..., 3]
_rows = _np.where(_al.max(axis=1) > 40)[0]; _cols = _np.where(_al.max(axis=0) > 40)[0]
CUT_TOP, CUT_BOT = float(_rows[0]), float(_rows[-1]); CUT_CX = float((_cols[0] + _cols[-1]) / 2)
CUT_H = CUT_BOT - CUT_TOP
F_SH, F_WA = 0.205, 0.470            # épaules et taille (fractions de la hauteur, depuis le haut du casque) : seule cette bande s'allonge

def paint_cover(ctx, surf, x0, y0, w, h, fy=0.5, a=1.0):
    sw, sh = surf.get_width(), surf.get_height(); s = max(w / sw, h / sh)
    ox = x0 + (w - sw * s) / 2; oy = y0 + (h - sh * s) * fy
    ctx.save(); ctx.rectangle(x0, y0, w, h); ctx.clip(); ctx.translate(ox, oy); ctx.scale(s, s)
    ctx.set_source_surface(surf, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(a); ctx.restore()

_space_bg_vec = space_bg
def space_bg(ctx, T, x0=0, y0=0, w=None, h=None, earth=True):
    if w is None: return _space_bg_vec(ctx, T, earth=False)          # fond plein écran : champ d'étoiles sobre
    paint_cover(ctx, _SPACE, x0, y0, w, h, 0.62)

def earth_bg(ctx, x0, y0, w, h, ground_y):
    paint_cover(ctx, _EARTH, x0, y0, w, h, 0.72)
    g = cairo.RadialGradient(x0 + w / 2, ground_y, 5, x0 + w / 2, ground_y, w * 0.30)   # ombre portée au sol
    g.add_color_stop_rgba(0, 0, 0, 0, 0.45); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.save(); ctx.translate(0, ground_y); ctx.scale(1, 0.16); ctx.translate(0, -ground_y); ctx.set_source(g)
    ctx.arc(x0 + w / 2, ground_y, w * 0.30, 0, 2 * math.pi); ctx.fill(); ctx.restore()

def _astro_parts(ctx, cx, feet_y, k, delta):
    ys = CUT_TOP + F_SH * CUT_H; yw = CUT_TOP + F_WA * CUT_H
    y_w = feet_y - (CUT_BOT - yw) * k; band = (yw - ys) * k + delta; y_s = y_w - band
    sy = band / ((yw - ys) * k)
    for (clip0, clip1, ty, syy, anchor) in ((y_w - 1, feet_y + 40 * U, feet_y - CUT_BOT * k, 1.0, None),
                                            (y_s - 1, y_w + 1, None, sy, "torso"),
                                            (y_s - 2000, y_s + 1, feet_y - CUT_BOT * k - delta, 1.0, None)):
        ctx.save(); ctx.rectangle(cx - 2000, clip0, 4000, clip1 - clip0); ctx.clip()
        if anchor == "torso":
            ctx.translate(cx, y_w); ctx.scale(k, k * syy); ctx.translate(-CUT_CX, -yw)
        else:
            ctx.translate(cx - CUT_CX * k, ty); ctx.scale(k, k)
        ctx.set_source_surface(_CUT, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint(); ctx.restore()

def astronaut(ctx, cx, feet_y, s, ext=0.0, a=1.0, ghost=False):
    if a <= 0: return
    k = 1000 * s / CUT_H; delta = TORSO_GAIN * ext * s
    ctx.push_group(); _astro_parts(ctx, cx, feet_y, k, delta); pat = ctx.pop_group()
    if ghost:
        rgba(ctx, CYAN, 0.55 * a); ctx.mask(pat)
    else:
        ctx.set_source(pat); ctx.paint_with_alpha(a)

def kelly_shot(ctx, T, t0):
    paint(ctx, frame("kelly", T - t0), zoom=1.0 / 1.03)
    g = cairo.LinearGradient(0, H * 0.06, 0, H * 0.36); g.add_color_stop_rgba(0, 0.0, 0.01, 0.04, 0.70); g.add_color_stop_rgba(1, 0, 0, 0, 0)   # haut à gauche : loin du casque
    ctx.set_source(g); ctx.rectangle(0, 0, W * 0.62, H * 0.36); ctx.fill()
    kn = prog(T, WT("scott") - 0.05, WT("scott") + 0.3)
    if kn > 0: pill_txt(ctx, "SCOTT KELLY", W * 0.25, H * 0.135, GOLD, 44, kn, fill=True)
    kd = prog(T, WT("two") - 0.05, WT("two") + 0.3)
    if kd > 0:
        big_label(ctx, "ABOUT 2 IN", W * 0.25, H * 0.192, 80, WHITE, kd)
        big_label(ctx, "5 CM", W * 0.25, H * 0.240, 80, CYAN, kd)
        text(ctx, "Reported case", W * 0.25, H * 0.279, 34 * U, (0.90, 0.93, 1.0), 0.9 * kd, bold=False)

def _spine_top(im):
    a = _np.asarray(im.convert("L")).astype(_np.float32) / 255.0
    h, w = a.shape; c = a[:, int(w * 0.25):int(w * 0.75)]
    rows = _np.where((c > 0.55).sum(axis=1) > 3)[0]
    return rows[0] / h, rows[-1] / h, _np.asarray(im.convert("RGB"))[5, 5] / 255.0
_SP_E, _spe = _load(RWD + "spine_earth.png", 900)
_SP_M, _spm = _load(RWD + "spine_micro.png", 900)
SPE_TOP, SPE_BOT, SP_BGC = _spine_top(_spe)
SPM_TOP, SPM_BOT, _c2 = _spine_top(_spm)
_lum = _np.asarray(_spm.convert("L")).astype(_np.float32) / 255.0
_ga = _np.clip((_lum - 0.40) / 0.25, 0, 1)
_SP_GLOW = _surf_from(_PI.fromarray(_np.dstack([_np.full_like(_lum, 255), _np.full_like(_lum, 200), _np.full_like(_lum, 70), _ga * 255]).astype(_np.uint8), "RGBA"), alpha=True)
SP_GAIN = 0.035                       # ≈ 3,5 % de longueur de colonne en plus : effet léger, sans « élastique »

def _arrows(ctx, T, a):
    for side in (-1, 1):
        for j in range(3):
            x = SP_X + side * 250 * U; y = H * (0.32 + 0.10 * j) + 10 * U * math.sin(T * 3 + j)
            ctx.new_path(); ctx.move_to(x, y - 50 * U); ctx.line_to(x, y + 30 * U); ctx.set_line_width(8 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, GOLD, 0.85 * a); ctx.stroke()
            ctx.new_path(); ctx.move_to(x - 20 * U, y + 14 * U); ctx.line_to(x, y + 46 * U); ctx.line_to(x + 20 * U, y + 14 * U); ctx.close_path(); rgba(ctx, GOLD, 0.85 * a); ctx.fill()

def spine_panel(ctx, T, m, arrows, state_lab, glow_v=0.0, show_ref=0.0):
    x0, x1 = W * 0.07, W * 0.85; wh = WY1 - WY0
    ctx.save(); rrect(ctx, x0, WY0, x1 - x0, wh, 40 * U); ctx.clip()
    rgba(ctx, tuple(SP_BGC), 1); ctx.paint()
    sh = wh * 0.92; sw = sh * _SP_E.get_width() / _SP_E.get_height(); ix = SP_X - sw / 2; iy = WY0 + wh * 0.055
    ybot = iy + SPE_BOT * sh; st = 1 + SP_GAIN * m                   # microgravité : colonne un peu plus longue (ancrée au sacrum)
    for surf, al, stretch in ((_SP_E, 1 - m, 1.0), (_SP_M, m, st)):
        if al <= 0: continue
        ctx.save(); ctx.translate(0, ybot); ctx.scale(1, stretch); ctx.translate(0, -ybot)
        ctx.translate(ix, iy); ctx.scale(sw / surf.get_width(), sh / surf.get_height())
        ctx.set_source_surface(surf, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.get_source().set_extend(cairo.EXTEND_PAD)   # bords prolongés : pas de bande
        ctx.paint_with_alpha(al); ctx.restore()
    if glow_v > 0:   # surbrillance dorée des seuls os (masque de luminance), pas du fond
        ctx.save(); ctx.translate(0, ybot); ctx.scale(1, st); ctx.translate(0, -ybot)
        ctx.translate(ix, iy); ctx.scale(sw / _SP_GLOW.get_width(), sh / _SP_GLOW.get_height())
        ctx.set_source_surface(_SP_GLOW, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint_with_alpha(0.55 * glow_v); ctx.restore()
    if arrows > 0: _arrows(ctx, T, arrows)
    if show_ref > 0:
        y_ref = iy + SPE_TOP * sh; y_now = ybot - (ybot - (iy + lerp(SPE_TOP, SPM_TOP, m) * sh)) * st
        ctx.new_path(); ctx.move_to(SP_X - 120 * U, y_ref); ctx.line_to(SP_X + 190 * U, y_ref); ctx.set_dash([14 * U, 10 * U]); ctx.set_line_width(4 * U)
        rgba(ctx, GOLD, 0.9 * show_ref); ctx.stroke(); ctx.set_dash([])
        if y_now < y_ref - 4 * U:
            ctx.new_path(); ctx.move_to(SP_X - 120 * U, y_now); ctx.line_to(SP_X + 190 * U, y_now); ctx.set_line_width(5 * U); rgba(ctx, CYAN, show_ref); ctx.stroke()
    ctx.restore()
    rrect(ctx, x0, WY0, x1 - x0, wh, 40 * U); ctx.set_line_width(5 * U); rgba(ctx, (0.80, 0.90, 1.0), 0.5); ctx.stroke()
    pill_txt(ctx, state_lab, W * 0.22, WY0 + 52 * U, GOLD if state_lab == "EARTH" else CYAN, 34)
