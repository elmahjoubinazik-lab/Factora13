# Episode 030 (Short, actualité) - "Brooklyn building collapse: what we know" (informations au 12 novembre 2026)
# SUJET D'ACTUALITÉ GRAVE (8 morts) : ton sobre, schémas explicatifs uniquement (aucune image réaliste ni IA de l'événement,
# aucune victime représentée), pas de musique, pas de confettis ni de bouton d'abonnement, aucune cause affirmée.
# Faits (sources dans meta_en.json) : 11/11/2026, immeuble de 3 étages sur Flatbush Avenue (Flatbush, Brooklyn) effondré
# dans l'excavation voisine (chantier d'un immeuble résidentiel) ; 8 morts confirmés par le maire Zohran Mamdani le
# 12/11 au matin ; au moins 17 blessés ; enquête du Department of Buildings et des forces de l'ordre, cause non déterminée.
# Règle générale : NYC Building Code, chapitre 33 (BC 3309, protection des propriétés voisines lors des excavations).

INK = (0.92, 0.94, 0.98)
SOFTGOLD = (0.95, 0.80, 0.45)
EARTH_T = (0.36, 0.25, 0.16)
EARTH_B = (0.18, 0.12, 0.08)
CONC = (0.62, 0.64, 0.68)

def bg(ctx, t):
    vgrad(ctx, (0.05, 0.07, 0.13), (0.01, 0.02, 0.05))
    glow(ctx, CX, H * 0.40, W * 0.9, (0.25, 0.35, 0.55), 0.10)
    rnd = random.Random(11); x = -20 * U                   # silhouette de rue en arrière-plan (profondeur)
    while x < W:
        w = rnd.uniform(120, 260) * U; h = rnd.uniform(0.10, 0.26) * H
        ctx.rectangle(x, H * GY - h, w - 8 * U, h); rgba(ctx, (0.09, 0.12, 0.20), 0.9); ctx.fill()
        for i in range(int(h / (40 * U))):
            for j in range(int(w / (50 * U))):
                if rnd.random() < 0.3: ctx.rectangle(x + 14 * U + j * 50 * U, H * GY - h + 16 * U + i * 40 * U, 16 * U, 14 * U); rgba(ctx, SOFTGOLD, 0.25); ctx.fill()
        x += w

GY = 0.56          # niveau du sol (fraction de H)
BX0, BX1 = 0.05, 0.50   # immeuble
PX0, PX1 = 0.54, 0.97   # excavation

def ground(ctx, dig=1.0, a=1.0):
    """Coupe du sol : couches de terre ; l'excavation (à droite) se creuse quand dig passe de 0 à 1."""
    gy = H * GY; bot = H * 0.78
    g = cairo.LinearGradient(0, gy, 0, H * 0.90); g.add_color_stop_rgba(0, *EARTH_T, a); g.add_color_stop_rgba(1, *EARTH_B, a)
    ctx.rectangle(0, gy, W, H * 0.90 - gy); ctx.set_source(g); ctx.fill()
    rnd = random.Random(5)
    for i in range(70):                                   # cailloux / grain du sol
        circle(ctx, rnd.random() * W, gy + rnd.random() * (H * 0.90 - gy), rnd.uniform(2, 6) * U, (0.55, 0.42, 0.30), 0.35 * a)
    for k in (0.33, 0.66):                                # strates
        y = gy + (H * 0.90 - gy) * k
        ctx.move_to(0, y); ctx.curve_to(W * 0.3, y - 10 * U, W * 0.6, y + 12 * U, W, y - 4 * U)
        ctx.set_line_width(3 * U); rgba(ctx, (0.50, 0.38, 0.26), 0.5 * a); ctx.stroke()
    if dig > 0:                                           # l'excavation
        d = gy + (bot - gy) * ease(dig)
        ctx.rectangle(W * PX0, gy - 2 * U, W * (PX1 - PX0), d - gy + 2 * U); vgrad_box(ctx, W * PX0, gy, W * PX1, d, (0.03, 0.04, 0.08), (0.06, 0.06, 0.10), a)
        neon_path(ctx, lambda c: (c.move_to(W * PX0, gy), c.line_to(W * PX0, d), c.line_to(W * PX1, d), c.line_to(W * PX1, gy)), SOFTGOLD, 3 * U, 0.8 * a)
    ctx.move_to(0, gy); ctx.line_to(W * PX0 if dig > 0 else W, gy)
    if dig > 0: ctx.move_to(W * PX1, gy); ctx.line_to(W, gy)
    ctx.set_line_width(5 * U); rgba(ctx, (0.75, 0.62, 0.45), a); ctx.stroke()

def vgrad_box(ctx, x0, y0, x1, y1, c0, c1, a):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgba(0, *c0, a); g.add_color_stop_rgba(1, *c1, a); ctx.set_source(g); ctx.fill()

def building(ctx, a=1.0, tilt=0.0, sink=0.0, footing=True):
    """Immeuble de 3 étages en trait lumineux, avec sa fondation (semelle) sous le sol."""
    gy = H * GY; x0, x1 = W * BX0, W * BX1; top = gy - H * 0.29; fh = (gy - top) / 3
    ctx.save(); ctx.translate(x1, gy); ctx.rotate(tilt); ctx.translate(-x1, -gy + sink)
    ctx.rectangle(x0, top, x1 - x0, gy - top); vgrad_box(ctx, x0, top, x1, gy, (0.16, 0.20, 0.30), (0.10, 0.13, 0.20), 0.95 * a)
    for f in range(3):
        y = top + f * fh
        for c in range(3):
            wx = x0 + (x1 - x0) * (0.12 + 0.30 * c); ww = (x1 - x0) * 0.18
            rrect(ctx, wx, y + fh * 0.22, ww, fh * 0.52, 4 * U); rgba(ctx, (0.95, 0.80, 0.45), 0.55 * a); ctx.fill()
        ctx.move_to(x0, y + fh); ctx.line_to(x1, y + fh); ctx.set_line_width(2 * U); rgba(ctx, INK, 0.25 * a); ctx.stroke()
    neon_path(ctx, lambda c: c.rectangle(x0, top, x1 - x0, gy - top), INK, 3.5 * U, a)
    ctx.rectangle(x0 - 10 * U, top - 14 * U, x1 - x0 + 20 * U, 14 * U); rgba(ctx, INK, 0.8 * a); ctx.fill()   # corniche
    if footing:
        ctx.rectangle(x0 - 16 * U, gy, x1 - x0 + 32 * U, 26 * U); rgba(ctx, CONC, 0.95 * a); ctx.fill()
    ctx.restore()

def arrow(ctx, x0, y0, x1, y1, col, a, w=8):
    if a <= 0: return
    ctx.move_to(x0, y0); ctx.line_to(x1, y1); ctx.set_line_width(w * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, col, a); ctx.stroke()
    an = math.atan2(y1 - y0, x1 - x0); h = 30 * U
    ctx.move_to(x1, y1); ctx.line_to(x1 - math.cos(an - 0.5) * h, y1 - math.sin(an - 0.5) * h); ctx.line_to(x1 - math.cos(an + 0.5) * h, y1 - math.sin(an + 0.5) * h)
    ctx.close_path(); rgba(ctx, col, a); ctx.fill()

def caption_top(ctx, s, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, CX - e.width / 2 - 26 * U, y - size * 0.75, e.width + 52 * U, size * 1.5, size * 0.4); rgba(ctx, (0.02, 0.03, 0.06), 0.85 * a); ctx.fill()
    text(ctx, s, CX, y, size, col, a)

# ---------------------------------------------------------------- scenes
def sc_hook(ctx, t, d):
    bg(ctx, t)
    ground(ctx, 1.0)
    k = prog(t, 3.6, 6.0)                                  # schéma : l'immeuble bascule vers l'excavation
    building(ctx, 1.0, 0.42 * ease(k), 60 * U * ease(k))
    if k > 0:
        rnd = random.Random(2)
        for i in range(40):
            e = clamp((t - 3.6 - rnd.random() * 1.2) / 2.0)
            if e > 0:
                circle(ctx, W * rnd.uniform(0.35, 0.80), H * GY - e * rnd.uniform(40, 260) * U, (14 + 40 * e) * U, (0.70, 0.65, 0.60), 0.25 * (1 - e))
    caption_top(ctx, "FLATBUSH, BROOKLYN · NOV 11, 2026", H * 0.13, 50 * U, INK, prog(t, 3.2, 3.6))
    text(ctx, "SCHEMATIC ILLUSTRATION", W * 0.75, H * 0.80, 30 * U, (0.7, 0.75, 0.85), 0.8)

def sc_toll(ctx, t, d):
    bg(ctx, t)
    k1 = prog(t, 0.2, 0.6); k2 = prog(t, 1.4, 1.8)
    text(ctx, "8", W * 0.28, H * 0.30, 360 * U, INK, k1); text(ctx, "DEATHS", W * 0.28, H * 0.43, 64 * U, (0.8, 0.84, 0.92), k1)
    text(ctx, "17+", W * 0.71, H * 0.30, 280 * U, SOFTGOLD, k2); text(ctx, "INJURED", W * 0.71, H * 0.43, 64 * U, (0.8, 0.84, 0.92), k2)
    ctx.move_to(CX, H * 0.22); ctx.line_to(CX, H * 0.46); ctx.set_line_width(3 * U); rgba(ctx, INK, 0.3 * k1); ctx.stroke()
    text(ctx, "Source: NYC Mayor's Office · Nov 12, 2026", CX, H * 0.50, 36 * U, (0.7, 0.75, 0.85), prog(t, 0.6, 1.0))

def sc_soil(ctx, t, d):
    bg(ctx, t)
    dig = prog(t, 3.5, 5.0)
    ground(ctx, dig)
    building(ctx, 1.0)
    caption_top(ctx, "FOUNDATION", H * 0.20, 52 * U, CYAN, prog(t, 0.6, 0.9))
    arrow(ctx, W * 0.275, H * 0.235, W * 0.275, H * GY + 4 * U, CYAN, prog(t, 0.8, 1.1), 6)
    sk = prog(t, 1.4, 2.0)                                  # le sol porte la fondation
    for i, xf in enumerate((0.12, 0.275, 0.43)):
        arrow(ctx, W * xf, H * GY + 150 * U, W * xf, H * GY + 40 * U, GREEN, sk * (0.7 + 0.3 * math.sin(t * 4 + i)), 7)
    lk = prog(t, 5.0, 5.6)                                  # côté excavation : le sol perd son appui
    if lk:
        ctx.move_to(W * 0.40, H * GY + 30 * U); ctx.line_to(W * PX0, H * GY + 30 * U); ctx.line_to(W * PX0, H * 0.76); ctx.close_path()
        rgba(ctx, CORAL, 0.35 * lk); ctx.fill()
        for i in range(3):
            yy = H * GY + (70 + 60 * i) * U; off = 10 * U * math.sin(t * 6 + i)
            arrow(ctx, W * 0.43, yy, W * (PX0 + 0.06) + off, yy + 30 * U, CORAL, lk, 6)
        caption_top(ctx, "SOIL CAN LOSE ITS SUPPORT", H * 0.20, 52 * U, CORAL, lk)

def sc_rule(ctx, t, d):
    bg(ctx, t)
    ground(ctx, 1.0)
    building(ctx, 1.0)
    uk = prog(t, 1.0, 3.0)                                  # reprise en sous-œuvre : blocs de béton jusqu'au fond de fouille
    gy = H * GY; bot = H * 0.78
    for i in range(4):
        bk = clamp(uk * 4 - i)
        if bk > 0:
            y0 = gy + 26 * U + i * (bot - gy - 26 * U) / 4
            ctx.rectangle(W * 0.38, y0, W * 0.13, (bot - gy - 26 * U) / 4 - 6 * U); rgba(ctx, CONC, 0.95 * bk); ctx.fill()
            ctx.rectangle(W * 0.38, y0, W * 0.13, (bot - gy - 26 * U) / 4 - 6 * U); ctx.set_line_width(3 * U); rgba(ctx, WHITE, 0.6 * bk); ctx.stroke()
    caption_top(ctx, "UNDERPINNING", H * 0.20, 60 * U, GREEN, prog(t, 1.0, 1.4))
    arrow(ctx, W * 0.445, H * 0.235, W * 0.445, gy + 80 * U, GREEN, prog(t, 1.4, 1.8), 6)
    caption_top(ctx, "NYC CODE: PROTECT ADJOINING BUILDINGS", H * 0.12, 40 * U, INK, prog(t, 0.1, 0.4))

def sc_probe(ctx, t, d):
    bg(ctx, t)
    ground(ctx, 1.0, 0.45)
    building(ctx, 0.45, 0.42, 60 * U)
    mx = W * (0.35 + 0.25 * math.sin(t * 0.9)); my = H * 0.47
    ctx.new_path(); ctx.arc(mx, my, 120 * U, 0, 2 * math.pi); ctx.set_line_width(14 * U); rgba(ctx, INK, 0.9); ctx.stroke()
    ctx.move_to(mx + 85 * U, my + 85 * U); ctx.line_to(mx + 190 * U, my + 190 * U); ctx.set_line_width(24 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    k = prog(t, 0.3, 0.6)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.21); ctx.rotate(-0.04)
        font(ctx, 58 * U); w_ = ctx.text_extents("CAUSE: UNDER INVESTIGATION").width + 70 * U
        rrect(ctx, -w_ / 2, -58 * U, w_, 116 * U, 18 * U); rgba(ctx, (0.02, 0.03, 0.06), 0.88 * k); ctx.fill()
        rrect(ctx, -w_ / 2, -58 * U, w_, 116 * U, 18 * U); ctx.set_line_width(6 * U); rgba(ctx, SOFTGOLD, k); ctx.stroke()
        text(ctx, "CAUSE: UNDER INVESTIGATION", 0, 0, 58 * U, SOFTGOLD, k); ctx.restore()
    caption_top(ctx, "NYC DEPT. OF BUILDINGS · LAW ENFORCEMENT", H * 0.29, 38 * U, INK, prog(t, 1.6, 2.0))

def sc_outro(ctx, t, d):
    bg(ctx, t)
    k = prog(t, 0.1, 0.5)
    ctx.save(); ctx.translate(CX, H * 0.25); s_ = 1 + 0.04 * math.sin(t * 3); ctx.scale(s_, s_)
    neon_text(ctx, "311", 0, 0, 260 * U, CYAN, k, PURPLE, fill=0.35); ctx.restore()
    caption_top(ctx, "NEW CRACKS NEAR CONSTRUCTION?", H * 0.36, 48 * U, INK, prog(t, 0.6, 1.0))
    text(ctx, "REPORT THEM", CX, H * 0.41, 48 * U, CYAN, prog(t, 0.9, 1.3))
    mk = prog(t, 3.5, 4.3)
    text(ctx, "Our thoughts are with the victims", CX, H * 0.52, 60 * U, INK, mk)
    text(ctx, "and their families.", CX, H * 0.565, 60 * U, INK, mk)

SHORT_SCENES = ["hook", "toll", "soil", "rule", "probe", "outro"]
SCENES = dict(hook=sc_hook, toll=sc_toll, soil=sc_soil, rule=sc_rule, probe=sc_probe, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.05, 0.07, 0.13), (0.01, 0.02, 0.05))
    thumb_text(c, "BROOKLYN COLLAPSE", "WHAT WE KNOW", "NEWS")

def cover(ctx):
    """Affiche sobre : le schéma (immeuble + excavation), titre en 2 couleurs dans la zone sûre, bandeau date/lieu."""
    bg(ctx, 0)
    ctx.save(); ctx.translate(0, H * 0.19); ground(ctx, 1.0); building(ctx, 1.0, 0.12, 14 * U); ctx.restore()
    for dx, dy, col, a in ((8, 10, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "BROOKLYN", CX + dx * U, H * 0.20 + dy * U, 170 * U, col or INK, a)
        text(ctx, "COLLAPSE", CX + dx * U, H * 0.285 + dy * U, 170 * U, col or SOFTGOLD, a)
        text(ctx, "WHAT WE KNOW", CX + dx * U, H * 0.36 + dy * U, 100 * U, col or CYAN, a)
    rrect(ctx, CX - 470 * U, H * 0.83 - 52 * U, 940 * U, 104 * U, 52 * U); rgba(ctx, (0.02, 0.03, 0.06), 0.9); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.83 - 52 * U, 940 * U, 104 * U, 52 * U); ctx.set_line_width(5 * U); rgba(ctx, SOFTGOLD, 1); ctx.stroke()
    text(ctx, "FLATBUSH · NOV 11, 2026", CX, H * 0.83, 56 * U, SOFTGOLD)
