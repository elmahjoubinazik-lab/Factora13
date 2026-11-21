exec(open(EP + "/scenes_base.py", encoding="utf-8").read())   # outils, textes, aliments, estomac (repris de l'ép. 044)
# Épisode 044c — révision « Why Doesn't Your Stomach Digest Itself? » (brief de Nazik / Instinct, 2026-11-22) : ~45 s,
# exemple historique vérifié (Alexis St. Martin, blessure accidentelle en 1822 → fistule gastrique ; William Beaumont a
# étudié la digestion par cette ouverture, notamment avec des aliments attachés à un fil ; expériences éthiquement
# problématiques — Becker Library, WashU) + vrai mécanisme : les cellules de surface libèrent du bicarbonate DANS le gel
# de mucus, qui neutralise l'acide près de la paroi (surface des cellules proche de la neutralité, contenu acide au-dessus ;
# Shorrock & Rees 1988, Am J Med, PMID 3279766 ; Allen & Flemström 2005) ; le gel ralentit l'acide ; autres défenses :
# cellules jointives, réparation de surface. Le cas historique N'EST PAS la découverte de ce mécanisme.
# Personne réelle : jamais de visage → silhouette de profil générique (« Historical illustration »), pas un portrait.
# Symboles + (acide) et − (bicarbonate) : convention pédagogique animée au montage (pas de microscopie, pas d'IA).
# Le seul plan généré (Runway, ép. 044b) est l'estomac entier ; tout le reste est dessiné ici.

SEPIA = (0.93, 0.86, 0.70)
INK = (0.09, 0.07, 0.06)
ACID = (1.0, 0.40, 0.20)
BICA = (0.35, 0.93, 1.0)
T_END = END_T

def band(ctx):
    """Zone sombre fixe sous les sous-titres (ne masque jamais les cellules : le schéma s'arrête au-dessus)."""
    rrect(ctx, W * 0.07, H * 0.676, W * 0.78, H * 0.072, 30 * U); rgba(ctx, (0.01, 0.01, 0.05), 0.55); ctx.fill()

def pill_txt(ctx, s, x, y, col, size=40, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 50 * U; h_ = size * 1.55 * U
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); rgba(ctx, (0.02, 0.03, 0.09), 0.86 * a); ctx.fill()
    rrect(ctx, x - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); ctx.set_line_width(4 * U); rgba(ctx, col, a); ctx.stroke()
    text(ctx, s, x, y, size * U, col, a)

def label1(ctx, s, x, y, col, k=1.0, size=44):
    """Légende d'une ligne (une seule idée à la fois)."""
    if k <= 0: return
    sc_ = 0.75 + 0.25 * ease(k)
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 56 * U; h_ = size * 1.75 * U
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 22 * U); rgba(ctx, (0.02, 0.03, 0.09), 0.88 * ease(k)); ctx.fill()
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 22 * U); ctx.set_line_width(5 * U); rgba(ctx, col, ease(k)); ctx.stroke()
    text(ctx, s, 0, 0, size * U, col, ease(k))
    ctx.restore()

# ---------------------------------------------------------------- portrait historique (silhouette générique, pas un visage)
OV_C = (W * 0.46, H * 0.40); OV_RX, OV_RY = W * 0.27, H * 0.165
_BUST = [(70, 30), (75, -40), (88, -110), (96, -175), (88, -240), (52, -288), (0, -310), (-52, -298), (-88, -268), (-104, -228),
         (-108, -196), (-122, -178), (-146, -146), (-122, -136), (-126, -118), (-116, -106), (-124, -94), (-108, -78), (-112, -58),
         (-86, -34), (-70, -4), (-104, 22), (-170, 70), (-230, 170), (-260, 330), (260, 330), (230, 160), (170, 70), (110, 40)]
_rp = random.Random(11)
GRAIN = [(_rp.uniform(-1, 1), _rp.uniform(-1, 1), _rp.uniform(0.6, 2.2), _rp.random()) for _ in range(500)]
def portrait(ctx, a=1.0):
    if a <= 0: return
    ctx.push_group()
    cx, cy = OV_C
    ctx.save(); ctx.translate(cx, cy); ctx.scale(OV_RX, OV_RY); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.save(); ctx.clip()
    g = cairo.RadialGradient(cx - OV_RX * 0.2, cy - OV_RY * 0.3, 10, cx, cy, OV_RY * 1.1)
    g.add_color_stop_rgb(0, *SEPIA); g.add_color_stop_rgb(1, 0.72, 0.60, 0.42); ctx.set_source(g); ctx.paint()
    for (u, v, r, k) in GRAIN:
        circle(ctx, cx + u * OV_RX, cy + v * OV_RY, r * U, (0.45, 0.32, 0.18) if k > 0.5 else (1, 0.96, 0.85), 0.10)
    s = 1.0 * U                                          # tête entière dans l'ovale, buste coupé par le cadre
    ctx.save(); ctx.translate(cx + OV_RX * 0.06, cy + OV_RY * 0.20); ctx.scale(s, s)
    ctx.new_path(); smooth = catmull_closed(_BUST, 6); poly_path(ctx, smooth); rgba(ctx, INK, 0.95); ctx.fill()
    ctx.new_path(); ctx.move_to(78, -150); ctx.curve_to(118, -120, 132, -80, 120, -40); ctx.curve_to(104, -70, 96, -110, 78, -150)   # cheveux noués (queue)
    rgba(ctx, INK, 0.95); ctx.fill()
    for pts in ([(-96, 8), (-64, -26), (-40, 14), (-72, 36)], [(-40, 14), (-12, -22), (10, 12), (-18, 34)]):   # col de chemise montant
        ctx.new_path(); ctx.move_to(*pts[0])
        for q in pts[1:]: ctx.line_to(*q)
        ctx.close_path(); rgba(ctx, (0.90, 0.84, 0.70), 0.95); ctx.fill()
    ctx.new_path(); ctx.move_to(-66, 40); ctx.curve_to(-90, 70, -60, 100, -40, 70); ctx.curve_to(-20, 100, 10, 70, -14, 40); ctx.close_path()   # cravate nouée
    rgba(ctx, (0.30, 0.22, 0.16), 1); ctx.fill()
    for pts in ([(-104, 22), (-60, 120), (-150, 330), (-230, 330), (-200, 150)], [(110, 40), (40, 120), (90, 330), (200, 330), (190, 150)]):   # revers du manteau
        ctx.new_path(); ctx.move_to(*pts[0])
        for q in pts[1:]: ctx.line_to(*q)
        ctx.close_path(); rgba(ctx, (0.17, 0.13, 0.11), 1); ctx.fill()
    ctx.restore(); ctx.restore()
    ctx.save(); ctx.translate(cx, cy); ctx.scale(OV_RX, OV_RY); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    ctx.set_line_width(22 * U); rgba(ctx, (0.62, 0.46, 0.20), 1); ctx.stroke_preserve()
    ctx.set_line_width(7 * U); rgba(ctx, (0.96, 0.82, 0.48), 1); ctx.stroke()
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

# ---------------------------------------------------------------- schéma : torse, estomac, ouverture (fistule), aliment au fil
TOR_C = (W * 0.46, H * 0.458); TOR_S = 1.30
_TORSO_L = [(-52, -430), (-58, -370), (-150, -350), (-240, -318), (-292, -262), (-296, -150), (-262, -20), (-222, 120), (-226, 240), (-238, 330)]
def tor_pt(p): return (TOR_C[0] + p[0] * TOR_S * U / 1.333, TOR_C[1] + p[1] * TOR_S * U / 1.333)
ST_C = (W * 0.545, H * 0.470); ST_K = 0.43           # petit estomac dans le torse (côté gauche du patient = droite de l'image)
RING_L = (150.0, 40.0)                               # point de l'estomac (repère local de l'ép. 044) où se trouve l'ouverture
def ring_pt():
    return (ST_C[0] + (ORG_C[0] + RING_L[0] * ORG_S - ORG_C[0]) * ST_K, ST_C[1] + (ORG_C[1] + RING_L[1] * ORG_S - ORG_C[1]) * ST_K)

def torso_schematic(ctx, T, a=1.0, string_k=0.0):
    if a <= 0: return
    ctx.push_group()
    L = [tor_pt(p) for p in _TORSO_L]; R = [(2 * TOR_C[0] - x, y) for (x, y) in L]
    def outline(c):
        pts = catmull_open(L, 8); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        pts = catmull_open(R, 8); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
    body = catmull_open(L, 8) + list(reversed(catmull_open(R, 8)))
    poly_path(ctx, body); rgba(ctx, (0.07, 0.10, 0.23), 0.85); ctx.fill()
    neon_path(ctx, outline, CYAN, 4 * U, 0.8)
    for i in range(4):   # côtes, très discrètes
        y = TOR_C[1] + (-250 + i * 38) * TOR_S * U / 1.333
        ctx.new_path(); ctx.move_to(TOR_C[0] - 20 * U, y); ctx.curve_to(TOR_C[0] - 120 * U, y + 20 * U, TOR_C[0] - 200 * U, y + 50 * U, TOR_C[0] - 250 * U, y + 90 * U)
        ctx.move_to(TOR_C[0] + 20 * U, y); ctx.curve_to(TOR_C[0] + 120 * U, y + 20 * U, TOR_C[0] + 200 * U, y + 50 * U, TOR_C[0] + 250 * U, y + 90 * U)
        ctx.set_line_width(3 * U); rgba(ctx, CYAN, 0.18); ctx.stroke()
    ctx.save(); ctx.translate(*ST_C); ctx.scale(ST_K, ST_K); ctx.translate(-ORG_C[0], -ORG_C[1]); stomach(ctx, T, mk=0.9); ctx.restore()
    rx, ry = ring_pt()
    glow(ctx, rx, ry, 70 * U, GOLD, 0.45)
    circle(ctx, rx, ry, 21 * U, (0.12, 0.04, 0.08), 1)
    ctx.new_path(); ctx.arc(rx, ry, 21 * U, 0, 2 * math.pi); ctx.set_line_width(6 * U); rgba(ctx, GOLD, 1); ctx.stroke()
    if string_k > 0:   # un morceau d'aliment attaché à un fil entre par l'ouverture
        top = (rx - 70 * U, H * 0.215)
        k = ease(clamp(string_k)); fx_, fy_ = L2((top[0] + 10 * U, top[1] + 90 * U), (rx, ry), k)
        ctx.new_path(); ctx.move_to(*top); ctx.curve_to(top[0] + 40 * U, top[1] + 120 * U, fx_ - 20 * U, fy_ - 90 * U, fx_, fy_)
        ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.85); ctx.stroke()
        sc_ = 26 * U * (1 - 0.55 * clamp((string_k - 0.75) / 0.25))
        _draw_piece(ctx, FOOD[2]["base"], fx_, fy_ + sc_ * 0.6, sc_, 0.4, FOOD[2]["col"], 1 - clamp((string_k - 0.9) / 0.1))
    ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

# ---------------------------------------------------------------- coupe de la paroi : mucus + bicarbonate (repère « contenu »)
PX0, PX1, PY0, PY1 = W * 0.06, W * 0.86, H * 0.245, H * 0.665
PCX, PCY = (PX0 + PX1) / 2, (PY0 + PY1) / 2
Y_MUC, Y_CELL, Y_MUS = H * 0.424, H * 0.493, H * 0.580
XL, XR = PX0 - 420 * U, PX1 + 420 * U                 # le contenu dépasse du cadre (zooms arrière sans bord)
PR = 46 * U
_rc = random.Random(5)
CELLS = []; _x = XL
while _x < XR:
    w_ = _rc.uniform(64, 80) * U; CELLS.append((_x, w_, _rc.uniform(-8, 8) * U, _rc.random())); _x += w_
FIBERS = [(_rc.uniform(XL, XR), _rc.uniform(Y_MUS + 14 * U, PY1 + 300 * U), _rc.uniform(90, 170) * U, _rc.uniform(10, 18) * U, _rc.random()) for _ in range(150)]
def muc_top(x, T): return Y_MUC + 9 * U * math.sin(x * 0.010 / U + T * 0.9) + 5 * U * math.sin(x * 0.023 / U - T * 0.6)
GEL = Y_CELL - Y_MUC
_ra = random.Random(19)
ACIDS = [(_ra.uniform(XL + 100 * U, XR - 100 * U), _ra.uniform(0, 1), _ra.uniform(0.15, 0.80), _ra.uniform(0, 9)) for _ in range(46)]
BICAS = [(_ra.uniform(XL + 60 * U, XR - 60 * U), _ra.uniform(0.18, 0.55), _ra.uniform(0, 1.6), _ra.uniform(0, 6.28)) for _ in range(44)]
REPAIR_CELL = None

T_PANEL0 = WT("itself") + 0.25; T_PANEL1 = T_PANEL0 + 0.55
T_REL = WT("release"); T_BIC = WT("bicarbonate"); T_ACID = WT("acid") - 0.35; T_LESS = WT("less")
T_SLOW = WT("slow"); T_TJ = WT("tightly"); T_REP = WT("surface", 2)
T_NAME = WT("that", 1) - 0.05 if WT("that", 1) < 1e8 else WT("patient's") - 0.3
T_MOD = WT("modern") - 0.35; T_CTA = T_END - 2.5

def acid_state(i, T):
    """Position (contenu) et état d'une particule d'acide : descend vite dans le contenu, lentement dans le gel,
    neutralisée dans la zone du bicarbonate (près des cellules) ; puis repart d'en haut."""
    x0, ph, depth, seed = ACIDS[i]
    v_c, v_g = 150 * U, 34 * U
    top = PY0 - 260 * U
    d_c = Y_MUC - top; d_g = GEL * (0.35 + 0.45 * depth)
    cyc = d_c / v_c + d_g / v_g + 0.35
    tt = (T - T_ACID + ph * cyc) % cyc
    if tt < d_c / v_c:
        y = top + v_c * tt; inside = 0.0; dead = 0.0
    elif tt < d_c / v_c + d_g / v_g:
        y = Y_MUC + v_g * (tt - d_c / v_c); inside = 1.0; dead = 0.0
    else:
        y = Y_MUC + d_g; inside = 1.0; dead = (tt - d_c / v_c - d_g / v_g) / 0.35
    x = x0 + 22 * U * math.sin(T * 1.3 + seed) + (12 * U * math.sin(T * 3.1 + seed) if inside else 0)
    return x, y, inside, dead, (v_g if inside else v_c)

def sym(ctx, x, y, r, col, sign, a=1.0):
    if a <= 0: return
    circle(ctx, x, y, r * 1.6, col, 0.18 * a); circle(ctx, x, y, r, col, 0.95 * a)
    ctx.set_line_width(r * 0.28); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, (0.05, 0.05, 0.10), a)
    ctx.new_path(); ctx.move_to(x - r * 0.5, y); ctx.line_to(x + r * 0.5, y); ctx.stroke()
    if sign == "+": ctx.new_path(); ctx.move_to(x, y - r * 0.5); ctx.line_to(x, y + r * 0.5); ctx.stroke()

def section_content(ctx, T, acid_on=1.0, bica_on=1.0, grad_on=0.0, trails=0.0, tj=0.0, rep=0.0, food_a=1.0):
    """Coupe dessinée dans le repère « contenu » (la caméra est appliquée avant)."""
    g = cairo.LinearGradient(0, PY0 - 300 * U, 0, Y_MUC + 20 * U)
    g.add_color_stop_rgb(0, 0.30, 0.15, 0.08); g.add_color_stop_rgb(1, 0.64, 0.36, 0.12)
    ctx.set_source(g); ctx.rectangle(XL, PY0 - 420 * U, XR - XL, Y_MUC - PY0 + 450 * U); ctx.fill()
    # aliments (au-dessus du gel, jamais dedans)
    ctx.save(); ctx.new_path(); ctx.move_to(XL, PY0 - 420 * U)
    for i in range(0, 81):
        xx = XL + (XR - XL) * i / 80; ctx.line_to(xx, muc_top(xx, T) - 8 * U)
    ctx.line_to(XR, PY0 - 420 * U); ctx.close_path(); ctx.clip()
    food_pieces(ctx, T, W * 0.46, (PY0 + Y_MUC) / 2 - 20 * U, 440 * U, 150 * U, 58 * U, theta(T), 0, 0, food_a)
    ctx.restore()
    # base du gel, muscle, cellules
    ctx.new_path(); ctx.move_to(XL, Y_CELL + 40 * U)
    for i in range(0, 81):
        xx = XL + (XR - XL) * i / 80; ctx.line_to(xx, muc_top(xx, T))
    ctx.line_to(XR, Y_CELL + 40 * U); ctx.close_path(); rgba(ctx, (0.12, 0.24, 0.34), 1); ctx.fill()
    g = cairo.LinearGradient(0, Y_MUS, 0, PY1 + 300 * U); g.add_color_stop_rgb(0, 0.80, 0.30, 0.38); g.add_color_stop_rgb(1, 0.45, 0.12, 0.22)
    ctx.set_source(g); ctx.rectangle(XL, Y_MUS, XR - XL, PY1 + 400 * U - Y_MUS); ctx.fill()
    for (x, y, l, h, k) in FIBERS:
        ctx.save(); ctx.translate(x, y); ctx.scale(l / 2, h / 2); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        rgba(ctx, mix((0.92, 0.42, 0.48), (0.60, 0.16, 0.26), k), 0.55); ctx.fill()
    ctx.rectangle(XL, Y_MUS - 6 * U, XR - XL, 14 * U); rgba(ctx, (1.0, 0.82, 0.84), 0.55); ctx.fill()
    rc = min(range(len(CELLS)), key=lambda i: abs(CELLS[i][0] + CELLS[i][1] / 2 - W * 0.50))   # cellule de la « réparation »
    for i, (x, w_, dy, k) in enumerate(CELLS):
        top = Y_CELL + dy * 0.4; bot = Y_MUS - 8 * U
        dent = 0.0
        if rep > 0 and i == rc: dent = 26 * U * (1 - ease(clamp((rep - 0.35) / 0.65))) * ease(clamp(rep / 0.3))
        lean = 0.0
        if rep > 0 and abs(i - rc) == 1: lean = (1 if i < rc else -1) * 10 * U * math.sin(math.pi * clamp((rep - 0.25) / 0.75))
        rrect(ctx, x + 3 * U + max(0, lean), top + dent, w_ - 6 * U + abs(lean), bot - top - dent, 22 * U)
        g = cairo.LinearGradient(0, top, 0, bot); g.add_color_stop_rgb(0, 1.0, 0.74, 0.78); g.add_color_stop_rgb(1, *TIS)
        ctx.set_source(g); ctx.fill_preserve(); ctx.set_line_width(3 * U); rgba(ctx, TIS_D, 0.85); ctx.stroke()
        br = 1 + 0.04 * math.sin(T * 2.2 + i)
        ctx.save(); ctx.translate(x + w_ / 2, bot - 52 * U); ctx.scale(w_ * 0.26 * br, 30 * U * br); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
        rgba(ctx, (0.50, 0.24, 0.52), 0.92); ctx.fill()
        if rep > 0 and i == rc and 0.3 < rep < 1.4:
            glow(ctx, x + w_ / 2, top + 10 * U, 70 * U, WHITE, 0.35 * math.sin(math.pi * clamp((rep - 0.3) / 1.1)))
    if tj > 0:   # jonctions serrées entre cellules voisines, côté surface
        for (x, w_, dy, k) in CELLS:
            top = Y_CELL + dy * 0.4
            ctx.new_path(); ctx.move_to(x + 2 * U, top + 4 * U); ctx.line_to(x + 2 * U, top + 70 * U)
            ctx.set_line_width(16 * U); rgba(ctx, GOLD, 0.35 * tj); ctx.stroke_preserve(); ctx.set_line_width(6 * U); rgba(ctx, (1, 0.95, 0.7), 0.95 * tj); ctx.stroke()
    # gel de mucus
    ctx.new_path(); ctx.move_to(XL, Y_CELL + 30 * U)
    for i in range(0, 81):
        xx = XL + (XR - XL) * i / 80; ctx.line_to(xx, muc_top(xx, T))
    ctx.line_to(XR, Y_CELL + 30 * U); ctx.close_path()
    g = cairo.LinearGradient(0, Y_MUC, 0, Y_CELL + 20 * U); g.add_color_stop_rgba(0, *MUC, 0.42); g.add_color_stop_rgba(1, *MUC_L, 0.72)
    ctx.set_source(g); ctx.fill_preserve()
    if grad_on > 0:   # gradient d'acidité : plus acide en haut du gel, beaucoup moins près des cellules
        g = cairo.LinearGradient(0, Y_MUC, 0, Y_CELL); g.add_color_stop_rgba(0, *ACID, 0.30 * grad_on); g.add_color_stop_rgba(0.55, 0.9, 0.9, 0.5, 0.06 * grad_on); g.add_color_stop_rgba(1, 0.30, 1.0, 0.65, 0.34 * grad_on)
        ctx.set_source(g); ctx.fill()
    ctx.new_path()
    for s_ in range(3):
        ctx.new_path()
        for i in range(0, 61):
            xx = XL + (XR - XL) * i / 60; yy = Y_MUC + (34 + 32 * s_) * U + 7 * U * math.sin(xx * 0.012 / U + s_ * 2 + T * 0.7)
            (ctx.move_to if i == 0 else ctx.line_to)(xx, yy)
        ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.16); ctx.stroke()
    def mt(c):
        c.move_to(XL, muc_top(XL, T))
        for i in range(1, 81):
            xx = XL + (XR - XL) * i / 80; c.line_to(xx, muc_top(xx, T))
    neon_path(ctx, mt, MUC, 3.0 * U, 0.85)
    # bicarbonate : libéré PAR les cellules DANS le gel, reste près des cellules
    if bica_on > 0:
        for (x, hgt, e, ph) in BICAS:
            t0 = T_REL + e * 0.8
            if T < t0: continue
            u = clamp((T - t0) / 1.2)
            y = Y_CELL - 6 * U - ease(u) * hgt * GEL + 5 * U * math.sin(T * 2 + ph)
            xx = x + 6 * U * math.sin(T * 1.7 + ph)
            sym(ctx, xx, y, 15 * U, BICA, "-", bica_on * clamp((T - t0) / 0.3))
    # acide : diffuse depuis le contenu, ralenti dans le gel, neutralisé près des cellules
    if acid_on > 0:
        for i in range(len(ACIDS)):
            x, y, inside, dead, v = acid_state(i, T)
            if trails > 0 and dead <= 0:
                ln = v * 0.22 * trails
                ctx.new_path(); ctx.move_to(x, y - ln); ctx.line_to(x, y - 18 * U); ctx.set_line_width(6 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
                rgba(ctx, ACID, 0.35 * trails); ctx.stroke()
            if dead > 0:
                if dead < 1:
                    ctx.new_path(); ctx.arc(x, y, (16 + 40 * dead) * U, 0, 2 * math.pi); ctx.set_line_width(5 * U); rgba(ctx, WHITE, 0.8 * (1 - dead) * acid_on); ctx.stroke()
                    sym(ctx, x, y, 15 * U * (1 - dead), ACID, "+", (1 - dead) * acid_on)
                continue
            sym(ctx, x, y, 15 * U, ACID, "+", acid_on)

CAM = [   # (temps, zoom, foyer x, foyer y) — variations de cadrage dans la fenêtre
    (0.0, 1.0, PCX, PCY), (T_REL - 0.3, 1.0, PCX, PCY), (T_REL + 0.6, 1.38, W * 0.40, Y_CELL - 30 * U),
    (T_LESS - 1.6, 1.38, W * 0.40, Y_CELL - 30 * U), (T_LESS - 0.4, 0.95, PCX, PCY + 20 * U),
    (T_SLOW - 0.5, 0.95, PCX, PCY + 20 * U), (T_SLOW + 0.4, 0.80, PCX, PCY + 30 * U),
    (T_TJ - 1.4, 0.80, PCX, PCY + 30 * U), (T_TJ - 0.4, 1.70, W * 0.50, Y_CELL + 30 * U),
    (T_NAME, 1.70, W * 0.50, Y_CELL + 30 * U), (T_NAME + 0.01, 1.0, PCX, PCY), (99, 1.0, PCX, PCY)]
def cam(T):
    for (t0, z0, x0, y0), (t1, z1, x1, y1) in zip(CAM, CAM[1:]):
        if t0 <= T < t1:
            k = ease((T - t0) / max(0.01, t1 - t0)) if (z0 != z1 or x0 != x1 or y0 != y1) else 0
            return lerp(z0, z1, k), lerp(x0, x1, k), lerp(y0, y1, k)
    return 1.0, PCX, PCY
def C(T, x, y):
    z, fx, fy = cam(T); return PCX + (x - fx) * z, PCY + (y - fy) * z

def section(ctx, T, a=1.0, **kw):
    ctx.save(); rrect(ctx, PX0, PY0, PX1 - PX0, PY1 - PY0, PR); ctx.clip()
    z, fx, fy = cam(T)
    ctx.save(); ctx.translate(PCX, PCY); ctx.scale(z, z); ctx.translate(-fx, -fy)
    section_content(ctx, T, **kw)
    ctx.restore(); ctx.restore()
    rrect(ctx, PX0, PY0, PX1 - PX0, PY1 - PY0, PR); ctx.set_line_width(6 * U); rgba(ctx, (0.80, 0.90, 1.0), 0.55 * a); ctx.stroke()

def clamp_in_panel(y, m=70):
    return max(PY0 + m * U, min(PY1 - m * U, y))

# ---------------------------------------------------------------- montage (temps absolu)
T_SCHEM = WT("opening") - 0.15
T_DOC = WT("doctors")
T_RUN0 = WT("but")
def master(ctx, T):
    bg(ctx, T)
    tag_txt = "Historical illustration"
    if T < T_RUN0:                                                      # 1. histoire : silhouette, puis schéma de l'ouverture
        ks = ease(prog(T, T_SCHEM, T_SCHEM + 0.5))
        if ks < 1: portrait(ctx, 1 - ks)
        if ks > 0:
            zk = ease(prog(T, T_DOC - 0.2, T_RUN0 - 0.2)); z = 1 + 0.45 * zk
            rx, ry = ring_pt(); tx, ty = L2((rx, ry), (W * 0.48, H * 0.45), zk)
            ctx.save(); ctx.translate(tx, ty); ctx.scale(z, z); ctx.translate(-rx, -ry)
            torso_schematic(ctx, T, ks, prog(T, T_DOC, T_DOC + 1.6))
            ctx.restore()
            tag_txt = "Simplified illustration"
        ka = 1 - prog(T, T_RUN0 - 0.35, T_RUN0)
        g = cairo.LinearGradient(0, 0, 0, H * 0.24); g.add_color_stop_rgba(0, 0.01, 0.01, 0.04, 0.55 * ka); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        ctx.set_source(g); ctx.rectangle(0, 0, W, H * 0.24); ctx.fill()
        ctx.push_group(); poster_text(ctx, "A WINDOW INTO", W * 0.46, H * 0.128, 112 * U, WHITE, W * 0.80); poster_text(ctx, "DIGESTION?", W * 0.46, H * 0.183, 124 * U, GOLD, W * 0.80)
        ctx.pop_group_to_source(); ctx.paint_with_alpha(ka)
    elif T < T_NAME:                                                     # 2. estomac entier (plan Runway), puis la coupe
        tag_txt = "Simplified illustration"
        pk = ease(prog(T, T_PANEL0, T_PANEL1))
        if pk < 1:
            tl = T - T_RUN0
            paint(ctx, frame("question", tl), zoom=1.0 / 1.03)
        if pk > 0:
            if pk < 1:
                rgba(ctx, (0.04, 0.03, 0.11), 0.85 * pk); ctx.paint()
                cx, cy = PCX, (Y_MUC + Y_CELL) / 2; sc_ = 0.35 + 0.65 * pk
                ctx.save(); ctx.translate(cx, cy); ctx.scale(sc_, sc_); ctx.translate(-cx, -cy)
                ctx.push_group(); section(ctx, T, bica_on=0, acid_on=0); ctx.pop_group_to_source(); ctx.paint_with_alpha(pk); ctx.restore()
            else:
                acid_on = prog(T, T_ACID, T_ACID + 0.6)
                grad = prog(T, T_LESS - 0.1, T_LESS + 0.5)
                trails = prog(T, T_SLOW - 0.3, T_SLOW + 0.3) * (1 - prog(T, T_TJ - 1.4, T_TJ - 0.8))
                tj = prog(T, T_TJ - 0.1, T_TJ + 0.35)
                rep = max(0.0, (T - (T_REP - 0.45)) / 1.6) if T > T_REP - 0.45 else 0.0
                section(ctx, T, bica_on=1.0, acid_on=acid_on, grad_on=grad, trails=trails, tj=tj, rep=rep)
                # légendes successives (une idée à la fois), posées sur les couches
                k1 = prog(T, T_BIC - 0.05, T_BIC + 0.30) * (1 - prog(T, T_LESS - 0.6, T_LESS - 0.2))
                if k1 > 0:
                    x, y = C(T, W * 0.40, Y_MUC + GEL * 0.30); label1(ctx, "MUCUS + BICARBONATE", PCX, clamp_in_panel(y), CYAN, k1)
                k2 = prog(T, T_LESS - 0.05, T_LESS + 0.30) * (1 - prog(T, T_SLOW - 0.4, T_SLOW))
                if k2 > 0:
                    x, y = C(T, PCX, Y_MUC + GEL * 0.55); label1(ctx, "LESS ACIDIC NEAR THE CELLS", PCX, clamp_in_panel(y), (0.45, 1.0, 0.70), k2, 40)
                k3 = prog(T, T_TJ - 0.05, T_TJ + 0.30) * (1 - prog(T, T_REP - 0.6, T_REP - 0.25))
                if k3 > 0:
                    x, y = C(T, PCX, Y_MUS + 60 * U); label1(ctx, "TIGHTLY JOINED CELLS", PCX, clamp_in_panel(y), GOLD, k3)
                k4 = prog(T, T_REP - 0.05, T_REP + 0.30)
                if k4 > 0:
                    x, y = C(T, PCX, Y_MUS + 60 * U); label1(ctx, "SURFACE REPAIR", PCX, clamp_in_panel(y), (1.0, 0.75, 0.80), k4)
    else:                                                                 # 3. retour à l'histoire, puis l'explication moderne
        km = ease(prog(T, T_MOD, T_MOD + 0.5))
        if km < 1:
            portrait(ctx, 1 - km)
            kn = prog(T, T_NAME + 0.3, T_NAME + 0.8) * (1 - km)
            if kn > 0:
                poster_text_a(ctx, "ALEXIS ST. MARTIN", W * 0.46, H * 0.612, 66 * U, WHITE, kn)
            ke = prog(T, WT("ethically") - 0.1, WT("ethically") + 0.3) * (1 - km)
            if ke > 0: text(ctx, "Ethically troubling experiments", W * 0.46, H * 0.650, 34 * U, (0.95, 0.88, 0.75), 0.92 * ke, bold=False)
            kh = prog(T, WT("revealed") - 0.1, WT("revealed") + 0.3) * (1 - km)
            if kh > 0: pill_txt(ctx, "HISTORICAL OBSERVATION", W * 0.46, OV_C[1] - OV_RY - 5 * U, (0.96, 0.82, 0.48), 36, kh)
        if km > 0:
            tag_txt = "Simplified illustration" if km > 0.5 else tag_txt
            ctx.push_group(); section(ctx, T, bica_on=1.0, acid_on=1.0, grad_on=1.0); ctx.pop_group_to_source(); ctx.paint_with_alpha(km)
            pill_txt(ctx, "MODERN EXPLANATION", PCX, PY0 + 60 * U, CYAN, 36, prog(T, T_MOD + 0.2, T_MOD + 0.6))
    band(ctx)
    tag(ctx, tag_txt)
    kc = prog(T, T_CTA, T_CTA + 0.35)                                    # fin : petit nom + CTA texte (sans bouton)
    if kc > 0:
        font(ctx, 44 * U); txt = "FACTORA"; w_ = ctx.text_extents(txt).width + 56 * U
        rrect(ctx, W * 0.46 - w_ / 2, H * 0.127 - 32 * U, w_, 64 * U, 32 * U); rgba(ctx, (0, 0, 0), 0.45 * kc); ctx.fill()
        text(ctx, txt, W * 0.46, H * 0.127, 44 * U, GOLD, kc)
        cta_lines(ctx, ("Follow Factora for more", "body mysteries."), W * 0.46, (H * 0.168, H * 0.200), 54, kc)

def poster_text_a(ctx, s, x, y, size, col, a):
    ctx.push_group(); poster_text(ctx, s, x, y, size, col, W * 0.80); ctx.pop_group_to_source(); ctx.paint_with_alpha(a)

def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return 1.2
    return (0.0 if scene == _FIRST else _TL[scene]["start"]) + t
SHORT_SCENES = [s["scene"] for s in _TLL]
SCENES = {s["scene"]: (lambda name: (lambda ctx, t, d: master(ctx, _abs_t(name, t))))(s["scene"]) for s in _TLL}

def cover(ctx):
    master(ctx, 1.2)
