# Episode 034 (Short seul, 9:16, ~25 s) - "How many holes does a T-shirt have?" — The Holes Debate #3, la réponse
# (demande de Nazik, 2026-11-15 : la question posée à la fin du Short du pantalon, ép. 026, a eu des votes sur TikTok).
# Maths : un T-shirt = sphère privée de 4 disques (col, bas, 2 manches) → 1er nombre de Betti 3 → 3 trous ;
# règle pour un objet tubulaire d'un seul tenant : trous = ouvertures − 1 (paille 1, pantalon 2, T-shirt 3).
# Visuel : on étire le T-shirt sans le déchirer, l'ouverture du bas devient le bord extérieur, le col et les 2 manches
# deviennent les 3 trous. Dessins maison (néon sobre), sans IA. Toutes les tailles en multiples de U.
exec(open("episodes/032-seven-riddles/scenes.py", encoding="utf-8").read())   # tshirt, ellipse, options_row, card, ST…

HOLE = (0.01, 0.01, 0.05)
OPTS = [("1", "FOUR"), ("2", "THREE"), ("3", "ZERO")]
TCY = 0.42          # centre vertical du T-shirt (fraction de H)

def resample(pts, n=240):
    segs = [(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
    lens = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(lens)
    out, i, acc = [], 0, 0.0
    for k in range(n):
        s = tot * k / n
        while acc + lens[i] < s: acc += lens[i]; i += 1
        a, b = segs[i]; f = (s - acc) / lens[i]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out

def stadium_pts(hw=470, hh=215, n=240):
    r = hh; pts = [(-hw + r, -hh), (hw - r, -hh)]
    pts += [(hw - r + r * math.sin(a), -r * math.cos(a)) for a in [math.pi * i / 24 for i in range(1, 24)]]
    pts += [(hw - r, hh), (-hw + r, hh)]
    pts += [(-hw + r - r * math.sin(a), r * math.cos(a)) for a in [math.pi * i / 24 for i in range(1, 24)]]
    return resample(pts, n)

TS = [(-90, -300), (-45, -264), (0, -252), (45, -264), (90, -300), (300, -220), (380, -40), (230, 10), (220, 330),
      (-220, 330), (-230, 10), (-380, -40), (-300, -220)]
P_TS, P_FLAT = resample(TS), stadium_pts()
# ouvertures du T-shirt (cx, cy, rx, ry, angle) → trous de la forme aplatie (cx, cy, rx, ry)
OPEN3 = [((0, -268, 95, 28, 0.0), (0, 0, 88, 72)), ((-305, -12, 80, 24, 1.2), (-285, 0, 88, 72)), ((305, -12, 80, 24, -1.2), (285, 0, 88, 72))]
WAIST = (0, 330, 220, 30)

def outline(c, pts):
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path()

def rot_ellipse(c, x, y, rx, ry, an):
    c.save(); c.translate(x, y); c.rotate(an); c.scale(max(rx, 0.01), max(ry, 0.01)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()

def morph_shape(ctx, cx, cy, s, k, t, a=1.0):
    """T-shirt → forme plate à 3 trous, sans déchirer : le bas devient le bord doré, le col et les manches deviennent les trous."""
    S = s * U; e = ease(k)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(S, S)
    pts = [(p[0] + (q[0] - p[0]) * e, p[1] + (q[1] - p[1]) * e) for p, q in zip(P_TS, P_FLAT)]
    glow(ctx, 0, 0, 520, mix(PINK, PURPLE, e), 0.35 * a)
    outline(ctx, pts); g = cairo.LinearGradient(-470, -215, 470, 215)
    g.add_color_stop_rgba(0, *mix(PINK, NAVY, 0.4 + 0.1 * e), a); g.add_color_stop_rgba(0.5, *mix(PINK, WHITE, 0.15), a); g.add_color_stop_rgba(1, *mix(PINK, NAVY, 0.4 + 0.1 * e), a)
    ctx.set_source(g); ctx.fill()
    neon_path(ctx, lambda c: outline(c, pts), PINK, 5, a * (1 - e))
    neon_path(ctx, lambda c: outline(c, pts), GOLD, 8, a * e)          # l'ouverture du bas devient le bord extérieur
    if e < 1:
        ey = max(p[1] for p in pts); bx = [p[0] for p in pts if p[1] > ey - 6]
        erx, ery = max(20, (max(bx) - min(bx)) / 2), WAIST[3] * (1 - e); fa = clamp(1 - e / 0.25) ** 2
        rot_ellipse(ctx, WAIST[0], ey, erx, ery, 0); rgba(ctx, HOLE, a * fa); ctx.fill()
        neon_path(ctx, lambda c: rot_ellipse(c, WAIST[0], ey, erx, ery + 4, 0), GOLD, 7, a * fa)
    for (ox, oy, orx, ory, an), (hx, hy, hrx, hry) in OPEN3:
        x = ox + (hx - ox) * e; y = oy + (hy - oy) * e; rx = orx + (hrx - orx) * e; ry = ory + (hry - ory) * e; aa = an * (1 - e)
        rot_ellipse(ctx, x, y, rx, ry, aa); rgba(ctx, HOLE, a); ctx.fill()
        neon_path(ctx, lambda c, x=x, y=y, rx=rx, ry=ry, aa=aa: rot_ellipse(c, x, y, rx, ry, aa), CYAN, 7, a)
    ctx.restore()

def title(ctx, a=1.0):
    neon_text(ctx, "HOW MANY HOLES", CX, H * 0.105, 94 * U, WHITE, a, PURPLE, fill=0.3)
    neon_text(ctx, "IN A T-SHIRT?", CX, H * 0.162, 124 * U, GOLD, a, CORAL, fill=0.35)

def badge(ctx, x, y, n, k, col=GOLD):
    if k <= 0: return
    e = ease(k); glow(ctx, x, y, 110 * U * e, col, 0.5); circle(ctx, x, y, 54 * U * e, col, 1.0)
    ctx.new_path(); ctx.arc(x, y, 54 * U * e, 0, 2 * math.pi); ctx.set_line_width(6 * U); rgba(ctx, NAVY, 1); ctx.stroke()
    text(ctx, str(n), x, y, 72 * U * e, NAVY)

def stamp(ctx, s, x, y, col, k, ang=-0.08, size=74):
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, -w_ / 2, -size * 0.85 * U, w_, size * 1.7 * U, 18 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.88 * k); ctx.fill()
    rrect(ctx, -w_ / 2, -size * 0.85 * U, w_, size * 1.7 * U, 18 * U); ctx.set_line_width(8 * U); rgba(ctx, col, k); ctx.stroke()
    text(ctx, s, 0, 0, size * U, col, k); ctx.restore()

def hook_frame(ctx, t, a=1.0):
    neon_bg(ctx, t, tint=PINK)
    title(ctx, a)
    tshirt(ctx, CX, H * TCY, 1.2 * (1 + 0.012 * math.sin(t * 2.5)), a, t, rings=0.55 + 0.45 * math.sin(t * 3))
    options_row(ctx, t, OPTS, H * 0.665, a, sc=0.95)

# ---------------------------------------------------------------- scènes
def sc_hook(ctx, t, d):
    hook_frame(ctx, t)       # question + T-shirt + réponses numérotées dès l'image 1 (formule QUIZ)

def sc_openings(ctx, t, d):
    neon_bg(ctx, t, tint=PINK)
    s = 1.2; S = s * U; cy = H * TCY
    tshirt(ctx, CX, cy, s, 1.0, t, rings=1.0)
    pos = [(0, -268), (0, 330), (-305, -12), (305, -12)]          # col, bas, manche, manche (ordre de la phrase)
    for i, (ox, oy) in enumerate(pos):
        badge(ctx, CX + ox * S, cy + oy * S, i + 1, prog(t, 0.9 + 0.55 * i, 1.2 + 0.55 * i))
    neon_text(ctx, "4 OPENINGS", CX, H * 0.11, 130 * U, GOLD, prog(t, 0.1, 0.4), CORAL, fill=0.35)
    s1 = ST("openings", 1)
    stamp(ctx, "OPENING ≠ HOLE", CX, H * 0.183, CORAL, prog(t, s1, s1 + 0.3))

def sc_morph(ctx, t, d):
    neon_bg(ctx, t, tint=PURPLE)
    s1 = ST("morph", 1)
    k = prog(t, 0.3, min(s1 + 0.4, d * 0.7))
    s = 1.2 - 0.2 * ease(k); cy = H * TCY
    if k <= 0: tshirt(ctx, CX, cy, s, 1.0, t, rings=1.0)
    else:
        tshirt(ctx, CX, cy, s, 1.0 - ease(min(1.0, k * 4)), t)
        morph_shape(ctx, CX, cy, s, k, t, min(1.0, k * 4))
    if k < 1: neon_text(ctx, "STRETCH. DON'T TEAR.", CX, H * 0.12, 82 * U, CYAN, prog(t, 0, 0.3), PURPLE, fill=0.3)
    fk = prog(t, max(s1, d * 0.7), max(s1, d * 0.7) + 0.4)
    if fk:
        sc_ = 1 + 0.3 * (1 - fk) + 0.04 * math.sin(t * 7)
        ctx.save(); ctx.translate(CX, H * 0.13); ctx.scale(sc_, sc_)
        neon_text(ctx, "3 HOLES", 0, 0, 200 * U, GOLD, fk, CORAL, fill=0.5); ctx.restore()
        S = s * U
        for i, (_, (hx, hy, _, _)) in enumerate(OPEN3):
            j = [1, 0, 2][i]   # numéroter de gauche à droite
            text(ctx, str(j + 1), CX + hx * S, cy + hy * S, 110 * U, WHITE, prog(t, max(s1, d * 0.7) + 0.2 * j, max(s1, d * 0.7) + 0.2 * j + 0.3))

def eq_row(ctx, y, label, eq, col, k, big=False):
    if k <= 0: return
    x0 = CX + (1 - ease(k)) * W * 0.6; h_ = (170 if big else 130) * U; w_ = W * 0.86
    if big: glow(ctx, x0, y, w_ * 0.55, col, 0.35 * k)
    rrect(ctx, x0 - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); rgba(ctx, (0.03, 0.03, 0.10), 0.85 * k); ctx.fill()
    rrect(ctx, x0 - w_ / 2, y - h_ / 2, w_, h_, h_ / 2); ctx.set_line_width((8 if big else 5) * U); rgba(ctx, col, k); ctx.stroke()
    text(ctx, label, x0 - w_ * 0.25, y, (62 if big else 50) * U, col, k)
    neon_text(ctx, eq, x0 + w_ * 0.20, y, (110 if big else 80) * U, WHITE, k, col, fill=0.4)

def sc_rule(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    fk = prog(t, 0.05, 0.4)
    neon_text(ctx, "HOLES =", CX, H * 0.105, 112 * U, WHITE, fk, CYAN, fill=0.4)
    neon_text(ctx, "OPENINGS − 1", CX, H * 0.165, 124 * U, GOLD, fk, CORAL, fill=0.5)
    eq_row(ctx, H * 0.29, "STRAW", "2 − 1 = 1", CYAN, prog(t, 0.5, 0.85))
    eq_row(ctx, H * 0.375, "PANTS", "3 − 1 = 2", PINK, prog(t, 0.9, 1.25))
    eq_row(ctx, H * 0.475, "T-SHIRT", "4 − 1 = 3", GREEN, prog(t, 1.5, 1.9), big=True)
    three_holes(ctx, CX, H * 0.59, 0.78, prog(t, 2.0, 2.5), t)

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=GOLD)
    three_holes(ctx, CX, H * 0.62, 0.9, 0.25, t)
    cta(ctx, t, d, "MORE RIDDLES IN THE FULL VIDEO", "SEND THIS TO A FRIEND")
    lk = prog(t, d - 0.55, d - 0.1)       # boucle : la dernière image redevient la première
    if lk > 0:
        ctx.save(); ctx.push_group(); hook_frame(ctx, 0.0); ctx.pop_group_to_source(); ctx.paint_with_alpha(lk); ctx.restore()

SHORT_SCENES = ["hook", "openings", "morph", "rule", "outro"]
SCENES = dict(hook=sc_hook, openings=sc_openings, morph=sc_morph, rule=sc_rule, outro=sc_outro)

def poster_text(ctx, s, x, y, size, col, maxw=None):
    font(ctx, size); w = ctx.text_extents(s).width
    if maxw and w > maxw: size *= maxw / w; font(ctx, size)
    e = ctx.text_extents(s); x0 = x - e.width / 2 - e.x_bearing; y0 = y + size * 0.35
    ctx.save(); ctx.translate(10 * U, 14 * U); ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0, 0, 0), 0.75)
    ctx.set_line_width(size * 0.20); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); ctx.fill(); ctx.restore()
    ctx.move_to(x0, y0); ctx.text_path(s); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.set_line_width(size * 0.16)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve(); rgba(ctx, col, 1); ctx.fill()

def cover(ctx):
    """Affiche : la question, le T-shirt en très grand avec ses ouvertures lumineuses, les 3 réponses ; jamais la réponse.
    Titre et bandeau dans la zone sûre 3:4 des grilles de profil (14–86 % de la hauteur)."""
    neon_bg(ctx, 1.0, tint=PINK)
    tshirt(ctx, CX, H * 0.53, 1.15, 1.0, 0.3, rings=1.0)
    poster_text(ctx, "HOW MANY HOLES", CX, H * 0.20, 130 * U, WHITE, W * 0.86)
    poster_text(ctx, "IN A T-SHIRT?", CX, H * 0.275, 160 * U, GOLD, W * 0.86)
    rrect(ctx, CX - 500 * U, H * 0.80 - 60 * U, 1000 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 500 * U, H * 0.80 - 60 * U, 1000 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "4, 3 OR 0? COMMENT!", CX, H * 0.80, 70 * U, (0.02, 0.03, 0.06))
