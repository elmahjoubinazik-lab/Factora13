TR = {"en": {
 "ET SI LA LUNE": "WHAT IF THE MOON",
 "DISPARAISSAIT ?": "DISAPPEARED?",
 "ET SI LA LUNE DISPARAISSAIT ?": "WHAT IF THE MOON DISAPPEARED?",
 "AVEC LA LUNE": "WITH THE MOON",
 "SANS LA LUNE": "WITHOUT THE MOON",
 "CONSÉQUENCE 1 · DES NUITS NOIRES": "CONSEQUENCE 1 · PITCH-BLACK NIGHTS",
 "DES MILLIERS D'ESPÈCES RÉGLÉES SUR LA LUNE": "THOUSANDS OF SPECIES TIMED BY THE MOON",
 "MARÉES ≈ 3× PLUS FAIBLES": "TIDES ≈ 3× WEAKER",
 "CONSÉQUENCE 2 · LES MARÉES": "CONSEQUENCE 2 · THE TIDES",
 "marée haute": "high tide",
 "marée basse": "low tide",
 "ZONE DE MARÉE : RÉDUITE": "TIDAL ZONE: SHRINKING",
 "ZONE DE MARÉE": "TIDAL ZONE",
 "SANS LA LUNE : INSTABLE": "WITHOUT THE MOON: UNSTABLE",
 "LA LUNE STABILISE L'AXE": "THE MOON STEADIES THE AXIS",
 "CONSÉQUENCE 3 · L'INCLINAISON": "CONSEQUENCE 3 · EARTH'S TILT",
 "AVEC LA LUNE : STABLE": "WITH THE MOON: STABLE",
 "SANS LA LUNE : ILLUSTRATION SIMPLIFIÉE": "WITHOUT THE MOON: SIMPLIFIED ILLUSTRATION",
 "inclinaison de l'axe → sur des millions d'années": "axial tilt → over millions of years",
 "PLUS D'ÉCLIPSE TOTALE": "NO MORE TOTAL ECLIPSES",
 "+3,8 cm / an": "+3.8 cm / year",
 "dans ~{} millions d'années": "in ~{} million years",
 "un fait fascinant chaque semaine": "fascinating facts, explained",
 "S'ABONNER": "SUBSCRIBE",
 "Laquelle vous a le plus surpris ?": "Which one surprised you most?",
 "3 CONSÉQUENCES": "3 CONSEQUENCES"
}}

# Scènes de l'épisode « Et si la Lune disparaissait ? »
# Ce fichier est exécuté dans l'espace de noms de engine/render.py : tous les helpers
# (W, H, U, CX, CY, VERT, couleurs, vgrad, circle, glow, text, rrect, stars, moon, earth, sun, chip, houses, prog, ease, mix...) sont disponibles.

def sc_hook(ctx, t, d):
    k = prog(t, 3.6, 5.6)          # disparition de la Lune
    vgrad(ctx, mix(NAVY2, NAVY, k), mix((0.2, 0.25, 0.45), (0.04, 0.05, 0.1), k))
    stars(ctx, t, 0.6 + 0.4 * k)
    mx, my = (CX + 380 * U, CY - 260 * U) if not VERT else (CX, CY - 420 * U)
    moon(ctx, mx, my, 120 * U * (1 + 0.04 * t / d), 1 - k)
    if k > 0:
        ctx.set_dash([14 * U, 14 * U]); ctx.arc(mx, my, 120 * U, 0, 2 * math.pi)
        rgba(ctx, WHITE, 0.35 * k * (1 - prog(t, 7, 9))); ctx.set_line_width(3 * U); ctx.stroke(); ctx.set_dash([])
    houses(ctx, H * 0.83, mix((0.06, 0.08, 0.16), (0.01, 0.01, 0.03), k))
    q = prog(t, d - 3.2, d - 2.4)
    if q: text(ctx, "?", mx, my, 260 * U, GOLD, q)

def sc_title(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.7)
    z = 1 + 0.05 * t / d
    ctx.save(); ctx.translate(CX, CY); ctx.scale(z, z); ctx.translate(-CX, -CY)
    yo = -40 * U if not VERT else -120 * U
    ctx.set_dash([16 * U, 12 * U]); ctx.arc(CX, CY + yo - 200 * U, 90 * U, 0, 2 * math.pi)
    rgba(ctx, MOON, 0.6); ctx.set_line_width(4 * U); ctx.stroke(); ctx.set_dash([])
    a = prog(t, 0, 0.5)
    if VERT:
        text(ctx, T("ET SI LA LUNE"), CX, CY + yo, 96 * U, WHITE, a)
        text(ctx, T("DISPARAISSAIT ?"), CX, CY + yo + 115 * U, 96 * U, GOLD, a)
    else:
        text(ctx, T("ET SI LA LUNE DISPARAISSAIT ?"), CX, CY + yo, (104 if LANG == "fr" else 86) * U, WHITE, a)
    ctx.restore()

def landscape(ctx, x0, x1, lit, t, y0=0, y1=None):
    y1 = H if y1 is None else y1; hz = y0 + (y1 - y0) * 0.7
    ctx.save(); ctx.rectangle(x0, y0, x1 - x0, y1 - y0); ctx.clip()
    top = mix((0.01, 0.01, 0.02), (0.14, 0.2, 0.38), lit); bot = mix((0.02, 0.02, 0.04), (0.25, 0.32, 0.5), lit)
    vgrad(ctx, top, bot)
    stars(ctx, t, 1.0 - 0.5 * lit)
    if lit: moon(ctx, (x0 + x1) / 2, y0 + (y1 - y0) * (0.47 if VERT else 0.38), 70 * U)
    # collines
    rgba(ctx, mix((0.02, 0.02, 0.03), (0.12, 0.2, 0.22), lit))
    ctx.move_to(x0, y1); ctx.line_to(x0, hz)
    for i in range(21):
        xx = x0 + (x1 - x0) * i / 20
        ctx.line_to(xx, hz - 40 * U * math.sin(i * 0.6) - 20 * U * math.sin(i * 1.7))
    ctx.line_to(x1, y1); ctx.close_path(); ctx.fill()
    # promeneur
    px = x0 + (x1 - x0) * (0.3 + 0.03 * t); py = hz
    ctx.save(); ctx.translate(px, py); ctx.scale(1.6, 1.6); ctx.translate(-px, -py)
    c = mix((0.08, 0.08, 0.1), (0.9, 0.9, 0.95), lit)
    circle(ctx, px, py - 95 * U, 14 * U, c)
    ctx.set_line_width(9 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c)
    sw = math.sin(t * 5) * 14 * U
    ctx.move_to(px, py - 80 * U); ctx.line_to(px, py - 40 * U)
    ctx.move_to(px, py - 40 * U); ctx.line_to(px - sw, py)
    ctx.move_to(px, py - 40 * U); ctx.line_to(px + sw, py)
    ctx.move_to(px, py - 70 * U); ctx.line_to(px + sw, py - 48 * U)
    ctx.stroke()
    ctx.restore()
    ctx.restore()

def sc_night(ctx, t, d):
    if VERT:
        landscape(ctx, 0, W, 1, t, 0, H * 0.46); landscape(ctx, 0, W, 0, t, H * 0.46, H)
        text(ctx, T("AVEC LA LUNE"), CX, H * 0.14, 44 * U, WHITE)
        text(ctx, T("SANS LA LUNE"), CX, H * 0.52, 44 * U, GOLD)
        rgba(ctx, GOLD); ctx.rectangle(0, H * 0.46 - 2 * U, W, 4 * U); ctx.fill()
    else:
        sp = W / 2
        landscape(ctx, 0, sp, 1, t); landscape(ctx, sp, W, 0, t)
        rgba(ctx, GOLD); ctx.rectangle(sp - 2 * U, 0, 4 * U, H); ctx.fill()
        text(ctx, T("AVEC LA LUNE"), sp / 2, H * 0.2, 48 * U, WHITE)
        text(ctx, T("SANS LA LUNE"), sp * 1.5, H * 0.2, 48 * U, GOLD)
    chip(ctx, T("CONSÉQUENCE 1 · DES NUITS NOIRES"), t)

def coral_branch(ctx, x, y, ang, ln, depth, w):
    if depth == 0 or ln < 6 * U: return
    x2, y2 = x + math.cos(ang) * ln, y + math.sin(ang) * ln
    ctx.set_line_width(w); ctx.move_to(x, y); ctx.line_to(x2, y2); ctx.stroke()
    coral_branch(ctx, x2, y2, ang - 0.45, ln * 0.72, depth - 1, w * 0.75)
    coral_branch(ctx, x2, y2, ang + 0.4, ln * 0.7, depth - 1, w * 0.75)

def sc_coral(ctx, t, d):
    vgrad(ctx, (0.05, 0.3, 0.5), (0.01, 0.07, 0.16))
    # rayons de lune sous l'eau
    for i in range(6):
        x = W * (0.1 + i * 0.17) + math.sin(t * 0.5 + i) * 30 * U
        g = cairo.LinearGradient(0, 0, 0, H * 0.8)
        g.add_color_stop_rgba(0, 0.8, 0.9, 1, 0.12); g.add_color_stop_rgba(1, 0.8, 0.9, 1, 0)
        ctx.set_source(g); ctx.move_to(x - 40 * U, 0); ctx.line_to(x + 40 * U, 0); ctx.line_to(x + 140 * U, H * 0.8); ctx.line_to(x - 60 * U, H * 0.8); ctx.close_path(); ctx.fill()
    glow(ctx, CX, -60 * U, 300 * U, MOON, 0.35)
    # sable
    rgba(ctx, (0.55, 0.45, 0.3)); ctx.move_to(0, H)
    for i in range(31): ctx.line_to(W * i / 30, H * 0.86 + 15 * U * math.sin(i * 0.8))
    ctx.line_to(W, H); ctx.close_path(); ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    cols = [CORAL, (1.0, 0.65, 0.3), (0.85, 0.4, 0.75), (1.0, 0.55, 0.6)]
    n = 7 if not VERT else 5
    for i in range(n):
        x = W * (i + 0.5) / n
        rgba(ctx, cols[i % 4]); coral_branch(ctx, x, H * 0.87, -math.pi / 2 + 0.1 * math.sin(i), 120 * U * (0.8 + 0.3 * (i % 3) / 2), 5, 18 * U)
    # ponte synchronisée
    sp = prog(t, 5.5, 8.0)
    random.seed(11)
    for j in range(240):
        x0 = W * random.random(); sp_speed = random.uniform(40, 110) * U; ph = random.random() * 6
        tt = max(0.0, t - 5.5 - random.random() * 1.5)
        y = H * 0.8 - tt * sp_speed
        if y < 0 or tt <= 0: continue
        circle(ctx, x0 + math.sin(tt + ph) * 20 * U, y, random.uniform(3, 7) * U, (1, 0.75, 0.8), 0.85 * sp)
    chip(ctx, T("DES MILLIERS D'ESPÈCES RÉGLÉES SUR LA LUNE"), t)

def sc_tides(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    s = d  # phases: 0-? montrer la Lune, puis disparition et marée réduite
    gone = prog(t, 7.5, 9.5)
    ex, ey = (CX - 120 * U, CY) if not VERT else (CX, CY)
    R = 190 * U
    bulge = (1 - gone) * 1.0 + gone * 0.31
    pulse = 1 + 0.03 * math.sin(t * 2)
    # bourrelet d'eau
    ctx.save(); ctx.translate(ex, ey)
    if VERT: ctx.rotate(-math.pi / 2)
    ctx.scale(R * (1 + 0.38 * bulge * pulse), R * (1 + 0.02))
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
    rgba(ctx, (0.35, 0.7, 1.0), 0.55); ctx.fill()
    earth(ctx, ex, ey, R)
    if VERT: mx, my = CX, CY - 560 * U
    else: mx, my = ex + 620 * U, ey
    moon(ctx, mx, my, 70 * U, 1 - gone)
    if VERT: sx, sy = CX, CY + 600 * U
    else: sx, sy = 170 * U, ey
    if VERT: sy = CY + 790 * U
    sun(ctx, sx, sy, 55 * U, t, prog(t, 4.0, 5.0))
    if gone > 0:
        ly = ey + R + 150 * U if not VERT else ey + R + 150 * U
        lx = ex if not VERT else CX
        text(ctx, T("MARÉES ≈ 3× PLUS FAIBLES"), lx if not VERT else CX, ey - R - 110 * U if not VERT else CY - 330 * U, 52 * U, GOLD, gone)
    chip(ctx, T("CONSÉQUENCE 2 · LES MARÉES"), t)

def sc_shore(ctx, t, d):
    vgrad(ctx, (0.45, 0.65, 0.85), (0.85, 0.9, 0.95), 0, H)
    weak = prog(t, d * 0.35, d * 0.55)
    amp = (1 - weak) * 110 * U + weak * 35 * U
    lvl = H * 0.58 + amp * math.sin(t * 1.4)
    # plage en pente
    rgba(ctx, (0.85, 0.75, 0.55)); ctx.move_to(0, H); ctx.line_to(0, H * 0.82); ctx.line_to(W, H * 0.35); ctx.line_to(W, H); ctx.close_path(); ctx.fill()
    # estran (zone colorée)
    def beach_x(y): return (H * 0.82 - y) / (H * 0.82 - H * 0.35) * W
    yA, yB = H * 0.58 - amp, H * 0.58 + amp
    ctx.move_to(beach_x(yA), yA); ctx.line_to(beach_x(yB), yB); ctx.line_to(beach_x(yB), yB + 18 * U); ctx.line_to(beach_x(yA), yA + 18 * U); ctx.close_path()
    rgba(ctx, (0.5, 0.42, 0.3), 0.9); ctx.fill()
    # mer
    g = cairo.LinearGradient(0, lvl, 0, H); g.add_color_stop_rgba(0, *SEA, 0.92); g.add_color_stop_rgba(1, *SEA_D, 0.98)
    ctx.set_source(g); ctx.move_to(0, lvl)
    for i in range(41): ctx.line_to(W * i / 40, lvl + 6 * U * math.sin(i * 0.9 + t * 3))
    ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); ctx.fill()
    # crabes et coquillages sur l'estran
    random.seed(5)
    for i in range(10):
        y = random.uniform(H * 0.58 - 110 * U, H * 0.58 + 110 * U)
        if y < lvl and abs(y - H * 0.58) < amp + 5:
            x = beach_x(y) + 30 * U
            circle(ctx, x, y - 6 * U, 9 * U, CORAL); circle(ctx, x + 25 * U, y - 4 * U, 6 * U, (0.2, 0.2, 0.35))
    ctx.set_dash([12 * U, 10 * U]); ctx.set_line_width(3 * U); rgba(ctx, NAVY, 0.6)
    for yy, nm in [(H * 0.58 - amp, T("marée haute")), (H * 0.58 + amp, T("marée basse"))]:
        ctx.move_to(0, yy); ctx.line_to(W, yy); ctx.stroke()
    ctx.set_dash([])
    for yy, nm in [(H * 0.58 - amp, T("marée haute")), (H * 0.58 + amp, T("marée basse"))]:
        text(ctx, nm, 40 * U, yy - 24 * U, 28 * U, NAVY if yy < lvl else WHITE, 0.9, False, "l")
    lab = T("ZONE DE MARÉE : RÉDUITE") if weak > 0.5 else T("ZONE DE MARÉE")
    text(ctx, lab, CX if VERT else W * 0.7, H * 0.2 if not VERT else H * 0.25, 46 * U, NAVY, 1)

def sc_tilt(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    R = 200 * U
    wob = prog(t, d * 0.62, d * 0.8)
    ang = math.radians(23.4) + wob * math.radians(18) * math.sin(t * 1.3) * math.sin(t * 0.37 + 1)
    earth(ctx, CX, CY, R)
    ctx.save(); ctx.translate(CX, CY); ctx.rotate(ang)
    ctx.set_line_width(6 * U); rgba(ctx, WHITE); ctx.move_to(0, -R * 1.5); ctx.line_to(0, R * 1.5); ctx.stroke()
    ctx.restore()
    ctx.set_dash([12 * U, 10 * U]); rgba(ctx, WHITE, 0.5); ctx.set_line_width(3 * U)
    ctx.move_to(CX, CY - R * 1.5); ctx.line_to(CX, CY + R * 1.5); ctx.stroke(); ctx.set_dash([])
    deg = math.degrees(ang)
    ctx.arc(CX, CY, R * 1.25, -math.pi / 2, -math.pi / 2 + ang); rgba(ctx, GOLD); ctx.set_line_width(5 * U); ctx.stroke()
    text(ctx, (f"{deg:.1f}°".replace(".", ",") if LANG == "fr" else f"{deg:.1f}°"), CX + R * 1.5, CY - R * 1.0, 64 * U, GOLD)
    if wob > 0.1: text(ctx, T("SANS LA LUNE : INSTABLE"), CX, CY - R * 1.75, 50 * U, CORAL, wob)
    else: text(ctx, T("LA LUNE STABILISE L'AXE"), CX, CY - R * 1.75, 50 * U, WHITE, prog(t, d * 0.4, d * 0.5))
    chip(ctx, T("CONSÉQUENCE 3 · L'INCLINAISON"), t)

def sc_climate(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY)
    x0, x1 = W * 0.1, W * 0.9
    rows = [(T("AVEC LA LUNE : STABLE"), H * 0.25, 0.12, WHITE), (T("SANS LA LUNE : ILLUSTRATION SIMPLIFIÉE"), H * 0.58, 1.0, CORAL)]
    p = prog(t, 0.3, d * 0.8)
    random.seed(2)
    noise = [random.uniform(-1, 1) for _ in range(400)]
    for label, yc, amp, col in rows:
        text(ctx, label, x0, yc - 165 * U, 34 * U, col, 1, True, "l")
        rgba(ctx, WHITE, 0.25); ctx.set_line_width(2 * U); ctx.move_to(x0, yc); ctx.line_to(x1, yc); ctx.stroke()
        ctx.set_line_width(6 * U); rgba(ctx, col)
        n = int(300 * p)
        for i in range(n):
            x = x0 + (x1 - x0) * i / 300
            v = math.sin(i * 0.12) * 0.5 + 0.5 * math.sin(i * 0.031 + 1) * (amp > 0.5) + noise[i] * 0.25 * amp
            y = yc - v * 90 * U * amp - math.sin(i * 0.12) * 18 * U
            (ctx.line_to if i else ctx.move_to)(x, y)
        ctx.stroke()
    text(ctx, T("inclinaison de l'axe → sur des millions d'années"), CX, H * 0.74, 30 * U, WHITE, 0.7, False)

def sc_eclipse(ctx, t, d):
    vgrad(ctx, (0.02, 0.02, 0.05), NAVY); stars(ctx, t, 0.4)
    sx, sy, r = CX, CY - (60 * U if not VERT else 120 * U), 170 * U
    cover = prog(t, 0.5, 3.0)
    gone = prog(t, 3.6, 5.0)
    sun(ctx, sx, sy, r, t, 1)
    mx = sx + (1 - cover) * 480 * U
    if cover > 0.95 and gone < 1:
        glow(ctx, sx, sy, r * 1.7, WHITE, 0.6 * (1 - gone))
    circle(ctx, mx, sy, r * 1.01, (0.02, 0.02, 0.04), 1 - gone)
    if gone > 0:
        text(ctx, T("PLUS D'ÉCLIPSE TOTALE"), CX, sy + r + 120 * U, 60 * U, GOLD, gone)

def sc_distance(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.5)
    if VERT:
        ex, ey = CX, H * 0.72; earth(ctx, ex, ey, 150 * U)
        my = H * 0.32 - 120 * U * prog(t, 3, d); moon(ctx, CX, my, 55 * U)
        ctx.set_dash([10 * U, 10 * U]); rgba(ctx, WHITE, 0.5); ctx.set_line_width(3 * U); ctx.move_to(CX, ey - 170 * U); ctx.line_to(CX, my + 70 * U); ctx.stroke(); ctx.set_dash([])
        tx, ty = CX, (ey + my) / 2
    else:
        ex, ey = W * 0.22, CY; earth(ctx, ex, ey, 170 * U)
        mx = W * 0.68 + 160 * U * prog(t, 3, d); moon(ctx, mx, ey, 60 * U)
        ctx.set_dash([10 * U, 10 * U]); rgba(ctx, WHITE, 0.5); ctx.set_line_width(3 * U); ctx.move_to(ex + 190 * U, ey); ctx.line_to(mx - 75 * U, ey); ctx.stroke(); ctx.set_dash([])
        tx, ty = (ex + mx) / 2, ey - 90 * U
    text(ctx, T("+3,8 cm / an"), tx, ty, 72 * U, GOLD, prog(t, 3.5, 4.3))
    yrs = int(600 * prog(t, 7.5, d - 1))
    if yrs: text(ctx, T("dans ~{} millions d'années").format(yrs), tx, ty + (180 if not VERT else 90) * U, 40 * U, WHITE, 0.9, False)

def sc_outro(ctx, t, d):
    vgrad(ctx, NAVY2, NAVY); stars(ctx, t, 0.6)
    yo = -80 * U if not VERT else -200 * U
    moon(ctx, CX, CY + yo - 190 * U, 70 * U)
    text(ctx, "FACTORA", CX, CY + yo, 140 * U, WHITE, prog(t, 0, 0.6))
    text(ctx, T("un fait fascinant chaque semaine"), CX, CY + yo + 100 * U, 38 * U, GOLD, prog(t, 0.4, 1.0), False)
    k = prog(t, d * 0.55, d * 0.65)
    if k:
        bw, bh = 520 * U, 110 * U
        pop = 1 + 0.05 * math.sin(t * 6)
        ctx.save(); ctx.translate(CX, CY + yo + 260 * U); ctx.scale(pop * k, pop * k)
        rrect(ctx, -bw / 2, -bh / 2, bw, bh, 22 * U); rgba(ctx, (0.85, 0.12, 0.12)); ctx.fill()
        text(ctx, T("S'ABONNER"), 0, 0, 52 * U, WHITE)
        ctx.restore()
    q = prog(t, d * 0.3, d * 0.4)
    if q and k < 1: text(ctx, T("Laquelle vous a le plus surpris ?"), CX, CY + yo + 260 * U, 44 * U, WHITE, q * (1 - k))

SHORT_SCENES = ["hook", "night", "tides", "outro"]

SCENES = dict(hook=sc_hook, title=sc_title, night=sc_night, coral=sc_coral, tides=sc_tides, shore=sc_shore,
              tilt=sc_tilt, climate=sc_climate, eclipse=sc_eclipse, distance=sc_distance, outro=sc_outro)



def thumbnail(c):
    """Miniature 1280x720 (appelée par render.py en mode thumb)."""
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(180):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.8), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .9)); c.fill()
    mx, my, r = 1050, 360, 190
    rg = cairo.RadialGradient(mx, my, 0, mx, my, r * 2); rg.add_color_stop_rgba(0, .95, .93, .85, .45); rg.add_color_stop_rgba(1, .95, .93, .85, 0); c.set_source(rg); c.arc(mx, my, r * 2, 0, 6.3); c.fill()
    c.save(); c.rectangle(0, 0, mx, H); c.clip(); c.arc(mx, my, r, 0, 6.3); c.set_source_rgb(.95, .93, .85); c.fill()
    for dx, dy, rr in [(-.45, -.2, .18), (-.2, .35, .12), (-.6, .25, .08)]:
        c.arc(mx + dx * r, my + dy * r, rr * r, 0, 6.3); c.set_source_rgb(.82, .8, .72); c.fill()
    c.restore()
    c.set_dash([18, 14]); c.arc(mx, my, r, -math.pi / 2, math.pi / 2); c.set_source_rgba(1, 1, 1, .7); c.set_line_width(5); c.stroke(); c.set_dash([])
    thumb_text(c, T("ET SI LA LUNE"), T("DISPARAISSAIT ?"), T("3 CONSÉQUENCES"))
