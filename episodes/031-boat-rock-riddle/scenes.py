# Episode 031 (Short) - "Boat and rock riddle: does the water rise or fall?" — « Can you solve it? #1 »
# Décision de Nazik (2026-11-13) : énigmes avec réponse le lendemain, dessins maison (néon sobre), sans images d'IA.
# Ne JAMAIS montrer la réponse ici (le niveau de l'eau ne bouge pas à l'écran). Réponse (vidéo du lendemain) : le niveau
# BAISSE — dans la barque, la pierre déplace son POIDS en eau ; au fond, seulement son VOLUME (pierre ≈ 2,5× plus dense).
# Exécuté dans engine/render.py (helpers du moteur). Toutes les tailles en multiples de U.

POOL_L, POOL_R = W * 0.07, W * 0.93
POOL_T, POOL_B = H * 0.37, H * 0.632
WATER_Y = H * 0.435
OPTS = [("1", "UP", CYAN), ("2", "DOWN", CORAL), ("3", "SAME", PURPLE)]
ROCK = [(1.00, 0.10), (0.78, 0.62), (0.30, 0.98), (-0.35, 0.92), (-0.86, 0.55), (-1.00, -0.05), (-0.72, -0.62),
        (-0.18, -0.95), (0.42, -0.86), (0.88, -0.48)]

def surface_y(x, t):
    return WATER_Y + 7 * U * math.sin(x / (95 * U) + t * 2.4) + 4 * U * math.sin(x / (41 * U) - t * 3.1)

def pool(ctx, t, a=1.0):
    """Coupe de la piscine : murs carrelés néon, eau en dégradé, marque du niveau d'eau (avec « ? »)."""
    if a <= 0: return
    # carrelage du fond (traits très discrets)
    for i in range(1, 9):
        x = POOL_L + (POOL_R - POOL_L) * i / 9
        ctx.move_to(x, WATER_Y + 30 * U); ctx.line_to(x, POOL_B); ctx.set_line_width(2 * U); rgba(ctx, CYAN, 0.08 * a); ctx.stroke()
    # eau
    ctx.new_path(); ctx.move_to(POOL_L, POOL_B)
    n = 60
    for i in range(n + 1):
        x = POOL_L + (POOL_R - POOL_L) * i / n
        ctx.line_to(x, surface_y(x, t))
    ctx.line_to(POOL_R, POOL_B); ctx.close_path()
    g = cairo.LinearGradient(0, WATER_Y, 0, POOL_B)
    g.add_color_stop_rgba(0, 0.20, 0.75, 1.0, 0.55 * a); g.add_color_stop_rgba(1, 0.05, 0.15, 0.55, 0.85 * a)
    ctx.set_source(g); ctx.fill()
    glow(ctx, CX, WATER_Y + 60 * U, W * 0.45, CYAN, 0.18 * a)
    neon_path(ctx, lambda c: [c.move_to(POOL_L, surface_y(POOL_L, t))] + [c.line_to(POOL_L + (POOL_R - POOL_L) * i / n, surface_y(POOL_L + (POOL_R - POOL_L) * i / n, t)) for i in range(n + 1)], CYAN, 4 * U, 0.8 * a)
    # murs et fond
    neon_path(ctx, lambda c: (c.move_to(POOL_L, POOL_T), c.line_to(POOL_L, POOL_B), c.line_to(POOL_R, POOL_B), c.line_to(POOL_R, POOL_T)), WHITE, 6 * U, 0.85 * a, CYAN)
    # rebords
    for x0 in (POOL_L - 40 * U, POOL_R):
        rrect(ctx, x0, POOL_T - 14 * U, 40 * U, 28 * U, 8 * U); rgba(ctx, WHITE, 0.55 * a); ctx.fill()

def level_mark(ctx, t, a=1.0, big=False):
    """Repère pointillé du niveau d'eau + « ? » (on ne montre jamais s'il monte ou descend)."""
    if a <= 0: return
    ctx.set_dash([26 * U, 18 * U], -t * 60 * U)
    ctx.move_to(POOL_L + 10 * U, WATER_Y); ctx.line_to(POOL_R - 10 * U, WATER_Y)
    ctx.set_line_width(5 * U); rgba(ctx, GOLD, 0.9 * a); ctx.stroke(); ctx.set_dash([])
    x, y = POOL_R - 70 * U, WATER_Y - 95 * U
    s = (1.35 if big else 1.0) * (1 + 0.06 * math.sin(t * 6))
    glow(ctx, x, y, 110 * U * s, GOLD, 0.35 * a)
    circle(ctx, x, y, 58 * U * s, (0.06, 0.04, 0.10), 0.9 * a)
    neon_path(ctx, lambda c: c.arc(x, y, 58 * U * s, 0, 2 * math.pi), GOLD, 5 * U, a)
    text(ctx, "?", x, y, 80 * U * s, GOLD, a)
    if big:
        for sgn in (-1, 1):   # flèches haut / bas autour du repère (les deux possibilités, sans réponse)
            yy = WATER_Y + sgn * 70 * U
            neon_path(ctx, lambda c, yy=yy, sgn=sgn: (c.move_to(POOL_L + 120 * U, yy), c.line_to(POOL_L + 120 * U, yy + sgn * 70 * U),
                                                         c.move_to(POOL_L + 95 * U, yy + sgn * 45 * U), c.line_to(POOL_L + 120 * U, yy + sgn * 72 * U),
                                                         c.line_to(POOL_L + 145 * U, yy + sgn * 45 * U)), WHITE, 5 * U, 0.9 * a)

def rock_shape(ctx, x, y, r, ang, a=1.0):
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang)
    def path(c):
        c.move_to(ROCK[0][0] * r, ROCK[0][1] * r)
        for px, py in ROCK[1:]: c.line_to(px * r, py * r)
        c.close_path()
    ctx.new_path(); path(ctx)
    g = cairo.RadialGradient(-0.3 * r, -0.4 * r, 0.1 * r, 0, 0, 1.2 * r)
    g.add_color_stop_rgba(0, 0.78, 0.74, 0.70, a); g.add_color_stop_rgba(1, 0.30, 0.28, 0.30, a)
    ctx.set_source(g); ctx.fill()
    for (sx, sy, ex, ey) in ((-0.5, -0.2, -0.1, 0.25), (0.2, -0.5, 0.45, -0.1), (0.1, 0.3, 0.5, 0.45)):   # fissures
        ctx.move_to(sx * r, sy * r); ctx.line_to(ex * r, ey * r); ctx.set_line_width(3 * U); rgba(ctx, (0.15, 0.14, 0.16), 0.7 * a); ctx.stroke()
    neon_path(ctx, path, GOLD, 4 * U, a)
    ctx.restore()

def boat(ctx, t, a=1.0, with_rock=True):
    """Barque néon qui flotte (la pierre dedans tant qu'elle n'est pas jetée)."""
    if a <= 0: return None
    bob = 6 * U * math.sin(t * 2.0); tilt = 0.03 * math.sin(t * 1.6)
    x, y = CX - 40 * U, WATER_Y + bob
    ctx.save(); ctx.translate(x, y); ctx.rotate(tilt)
    tw, bw, hh = 420 * U, 270 * U, 110 * U          # haut, bas, hauteur de la coque ; 45 U sous la ligne d'eau
    def hull(c):
        c.move_to(-tw / 2, -hh + 45 * U); c.line_to(tw / 2, -hh + 45 * U); c.line_to(bw / 2, 45 * U); c.line_to(-bw / 2, 45 * U); c.close_path()
    ctx.new_path(); hull(ctx)
    g = cairo.LinearGradient(0, -hh, 0, 45 * U); g.add_color_stop_rgba(0, 1.0, 0.45, 0.35, 0.95 * a); g.add_color_stop_rgba(1, 0.55, 0.12, 0.18, 0.95 * a)
    ctx.set_source(g); ctx.fill()
    ctx.move_to(-tw / 2 + 20 * U, -hh + 75 * U); ctx.line_to(tw / 2 - 20 * U, -hh + 75 * U); ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.35 * a); ctx.stroke()
    neon_path(ctx, hull, CORAL, 5 * U, a)
    # rame posée en travers
    neon_path(ctx, lambda c: (c.move_to(-tw * 0.62, -hh * 0.2), c.line_to(-tw * 0.18, -hh * 0.95)), GOLD, 4 * U, 0.8 * a)
    ctx.restore()
    rx, ry = x + 40 * U, y - hh + 45 * U - 62 * U
    if with_rock: rock_shape(ctx, rx, ry, 72 * U, 0.1 * math.sin(t), a)
    return rx, ry

def options_row(ctx, t, a=1.0, hot=None, y=0.29):
    """Les 3 réponses numérotées, en ligne, visibles dès l'image 1 (hot : index de la réponse lue → pulsation)."""
    if a <= 0: return
    pw, ph = W * 0.28, 112 * U
    for i, (n, s, col) in enumerate(OPTS):
        x = CX + (i - 1) * (pw + 26 * U)
        p = 1 + (0.10 * (0.5 + 0.5 * math.sin(t * 9)) if hot == i else 0)
        ctx.save(); ctx.translate(x, H * y); ctx.scale(p, p)
        if hot == i: glow(ctx, 0, 0, pw * 0.8, col, 0.45 * a)
        rrect(ctx, -pw / 2, -ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.88 * a); ctx.fill()
        rrect(ctx, -pw / 2, -ph / 2, pw, ph, ph / 2); ctx.set_line_width(5 * U); rgba(ctx, col, a); ctx.stroke()
        circle(ctx, -pw / 2 + ph / 2, 0, ph * 0.36, col, a)
        text(ctx, n, -pw / 2 + ph / 2, 0, 58 * U, (0.04, 0.03, 0.10), a)
        text(ctx, s, ph * 0.42, 0, 54 * U, WHITE, a)
        ctx.restore()

def title(ctx, t, a=1.0):
    """La question, toujours lisible en haut (après le bandeau d'accroche du moteur, qui s'efface vers 3 s)."""
    neon_text(ctx, "ROCK OUT OF THE BOAT:", CX, H * 0.115, 70 * U, WHITE, a, PURPLE, fill=0.2)
    neon_text(ctx, "WATER UP OR DOWN?", CX, H * 0.185, 84 * U, GOLD, a, CORAL, fill=0.25)

def comment_band(ctx, a=1.0, y=0.665):
    if a <= 0: return
    s_ = "COMMENT 1, 2 OR 3"; font(ctx, 56 * U); w_ = ctx.text_extents(s_).width + 90 * U
    rrect(ctx, CX - w_ / 2, H * y - 50 * U, w_, 100 * U, 50 * U); rgba(ctx, GOLD, a); ctx.fill()
    text(ctx, s_, CX, H * y, 56 * U, (0.03, 0.02, 0.08), a)

def base(ctx, t, tint=PURPLE, title_a=None):
    neon_bg(ctx, t, tint=tint)
    pool(ctx, t)
    title(ctx, t, 1.0 if title_a is None else title_a)   # question lisible dès l'image 1 (pas de bandeau moteur : hook_text vide)

def sc_hook(ctx, t, d):
    base(ctx, t)
    boat(ctx, t)
    level_mark(ctx, t, 0.9)
    options_row(ctx, t)
    comment_band(ctx)

def sc_drop(ctx, t, d):
    base(ctx, t)
    rx0, ry0 = CX, WATER_Y - 125 * U
    k = clamp(t / (d * 0.42))                    # vol de la pierre (arc vers la droite)
    boat(ctx, t, with_rock=False)
    hit_x = CX + 300 * U
    if k < 1:
        x = rx0 + (hit_x - rx0) * k; y = ry0 - 220 * U * math.sin(math.pi * k) + (WATER_Y - ry0) * k ** 2
        rock_shape(ctx, x, y, 72 * U, k * 2.5)
    else:
        e = clamp((t - d * 0.42) / (d * 0.5)); e2 = 1 - (1 - e) ** 2
        x = hit_x + 30 * U * math.sin(e * 6); y = WATER_Y + (POOL_B - 80 * U - WATER_Y) * e2
        rock_shape(ctx, x, y, 72 * U, 2.5 + e * 1.2)
        th = t - d * 0.42                           # éclaboussures + ronds dans l'eau
        rnd = random.Random(5)
        for i in range(26):
            ang = rnd.uniform(math.pi * 1.1, math.pi * 1.9); sp = rnd.uniform(400, 900) * U
            px = hit_x + math.cos(ang) * sp * th; py = WATER_Y + math.sin(ang) * sp * th + 1400 * U * th * th
            if py < WATER_Y + 10 * U: circle(ctx, px, py, rnd.uniform(6, 13) * U, CYAN, clamp(1 - th / 0.8))
        for j in range(3):
            rr = (th - j * 0.18) * 520 * U
            if rr > 0:
                ctx.save(); ctx.translate(hit_x, WATER_Y); ctx.scale(1, 0.22)
                ctx.new_path(); ctx.arc(0, 0, rr, 0, 2 * math.pi); ctx.restore()
                ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.5 * clamp(1 - rr / (520 * U))); ctx.stroke()
        for b in range(8):                          # bulles qui remontent derrière la pierre
            by = y - ((t * 260 * U + b * 70 * U) % (y - WATER_Y + 1))
            circle(ctx, x + 25 * U * math.sin(b * 1.7 + t * 4), by, (6 + b % 3 * 3) * U, WHITE, 0.35)
    level_mark(ctx, t, 0.9)
    options_row(ctx, t)
    comment_band(ctx)

def _rock_bottom(ctx, t):
    rock_shape(ctx, CX + 300 * U, POOL_B - 80 * U, 72 * U, 3.7)

def sc_ask(ctx, t, d):
    base(ctx, t, tint=CYAN)
    boat(ctx, t, with_rock=False)
    _rock_bottom(ctx, t)
    level_mark(ctx, t, 1.0, big=True)
    options_row(ctx, t)
    comment_band(ctx)

def sc_options(ctx, t, d):
    base(ctx, t, tint=PINK)
    boat(ctx, t, with_rock=False)
    _rock_bottom(ctx, t)
    level_mark(ctx, t, 0.9)
    hot = 0 if t < d * 0.25 else (1 if t < d * 0.48 else 2)
    options_row(ctx, t, hot=hot)
    comment_band(ctx)

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=GOLD)
    ctx.save(); pool(ctx, t, 0.2); boat(ctx, t, 0.2, with_rock=False); ctx.restore()
    cta(ctx, t, d, "ANSWER TOMORROW", "COMMENT 1, 2 OR 3")

SHORT_SCENES = ["hook", "drop", "ask", "options", "outro"]
SCENES = dict(hook=sc_hook, drop=sc_drop, ask=sc_ask, options=sc_options, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.04, 0.22), (0.01, 0.02, 0.08))
    thumb_text(c, "ROCK OUT OF A BOAT", "WATER UP OR DOWN?", "RIDDLE")

def cover(ctx):
    """Affiche : la question en très gros, la piscine avec la barque et la pierre, les 3 réponses, « COMMENT 1, 2 OR 3 »
    et « ANSWER TOMORROW » — dans la zone sûre (14–86 % de la hauteur), sans jamais montrer la réponse."""
    t = 0.6
    neon_bg(ctx, t)
    neon_text(ctx, "CAN YOU SOLVE IT?", CX, H * 0.165, 80 * U, CYAN, 1.0, PURPLE, fill=0.25)
    neon_text(ctx, "ROCK OUT OF THE BOAT:", CX, H * 0.225, 70 * U, WHITE, 1.0, PURPLE, fill=0.3)
    neon_text(ctx, "WATER UP OR DOWN?", CX, H * 0.29, 86 * U, GOLD, 1.0, CORAL, fill=0.35)
    ctx.save(); ctx.translate(0, H * 0.035); pool(ctx, t); boat(ctx, t); level_mark(ctx, t, 1.0); ctx.restore()
    options_row(ctx, t, y=0.765)
    comment_band(ctx, 1.0, y=0.835)
    neon_text(ctx, "ANSWER TOMORROW", CX, H * 0.708, 62 * U, GREEN, 1.0, CYAN, fill=0.25)
