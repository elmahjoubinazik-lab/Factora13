# Episode 024 (Short only) - "Hand dryer or paper towel: which is cleaner?" — realistic shaded illustrations
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Facts: UConn (AEM 2018: hot-air dryers deposit restroom bacteria on hands, HEPA ~4x fewer), Leeds (J Hosp Infect 2014,
# funded by the European Tissue Symposium: ~27x more airborne germs near jet dryers), CDC (towel or dryer both OK; dry hands fully).

SKIN = (0.86, 0.74, 0.66)   # désaturé : la finition ffmpeg (+75 % de saturation) le rend orangé sinon
GERMC = (0.35, 0.95, 0.45)

def lin(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c, al in stops: g.add_color_stop_rgba(o, c[0], c[1], c[2], al)
    return g

def label(ctx, s, x, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.02, 0.02, 0.04), 0.78 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

def bathroom(ctx, t, floor_y=None):
    floor_y = floor_y or H * 0.80
    ctx.set_source(lin(0, 0, 0, floor_y, [(0, (0.10, 0.20, 0.24), 1), (1, (0.16, 0.30, 0.34), 1)])); ctx.paint()
    ctx.set_line_width(3 * U)
    for i in range(0, 30):
        ctx.move_to(0, i * 120 * U); ctx.line_to(W, i * 120 * U)
    for j in range(0, 10):
        ctx.move_to(j * 160 * U, 0); ctx.line_to(j * 160 * U, floor_y)
    rgba(ctx, WHITE, 0.06); ctx.stroke()
    glow(ctx, W * 0.3, H * 0.1, 900 * U, (0.9, 1.0, 1.0), 0.10)
    ctx.rectangle(0, floor_y, W, H - floor_y)
    ctx.set_source(lin(0, floor_y, 0, H, [(0, (0.22, 0.24, 0.26), 1), (1, (0.06, 0.07, 0.08), 1)])); ctx.fill()

def germ(ctx, x, y, r, t, a=1.0, col=GERMC):
    if a <= 0 or r <= 0: return
    glow(ctx, x, y, r * 2.6, col, 0.30 * a)
    ctx.set_line_width(max(1.0, r * 0.22)); rgba(ctx, col, a)
    for i in range(8):
        an = i * math.pi / 4 + t * 1.5
        ctx.move_to(x + math.cos(an) * r, y + math.sin(an) * r); ctx.line_to(x + math.cos(an) * r * 1.5, y + math.sin(an) * r * 1.5); ctx.stroke()
    circle(ctx, x, y, r, col, 0.9 * a); circle(ctx, x - r * 0.3, y - r * 0.3, r * 0.3, WHITE, 0.6 * a)

def hand(ctx, x, y, s, ang, a=1.0, wet=0.0, mirror=1):
    """Open hand, palm facing the viewer, fingers up (y = wrist)."""
    if a <= 0: return
    S = U * s
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(mirror, 1)
    skin = lambda: lin(-90 * S, 0, 90 * S, 0, [(0, mix(SKIN, (0.5, 0.3, 0.2), 0.25), a), (0.45, mix(SKIN, WHITE, 0.15), a), (1, mix(SKIN, (0.5, 0.3, 0.2), 0.3), a)])
    rrect(ctx, -60 * S, -40 * S, 120 * S, 120 * S, 30 * S); ctx.set_source(skin()); ctx.fill()           # wrist
    rrect(ctx, -95 * S, -200 * S, 190 * S, 190 * S, 70 * S); ctx.set_source(skin()); ctx.fill()          # palm
    for i, (fx, fl) in enumerate(((-66, 150), (-22, 180), (22, 172), (64, 140))):
        rrect(ctx, (fx - 21) * S, (-180 - fl) * S, 42 * S, (fl + 40) * S, 21 * S); ctx.set_source(skin()); ctx.fill()
        ctx.move_to((fx - 12) * S, (-185 - fl * 0.45) * S); ctx.line_to((fx + 12) * S, (-185 - fl * 0.45) * S)
        ctx.set_line_width(3 * S); rgba(ctx, (0.55, 0.35, 0.25), 0.4 * a); ctx.stroke()
    ctx.save(); ctx.translate(-110 * S, -90 * S); ctx.rotate(-0.7)
    rrect(ctx, -22 * S, -120 * S, 46 * S, 140 * S, 23 * S); ctx.set_source(skin()); ctx.fill(); ctx.restore()  # thumb
    if wet > 0:
        rnd = random.Random(6)
        for i in range(9):
            dx, dy = rnd.uniform(-80, 80) * S, rnd.uniform(-320, -40) * S; r = rnd.uniform(13, 20) * S
            ctx.save(); ctx.translate(dx, dy); ctx.scale(0.8, 1)
            ctx.arc(0, 0, r, 0, 2 * math.pi); ctx.restore()
            rgba(ctx, (0.55, 0.80, 1.0), 0.55 * wet * a); ctx.fill()
            circle(ctx, dx - r * 0.3, dy - r * 0.35, r * 0.3, WHITE, 0.9 * wet * a)
    ctx.restore()

def hot_dryer(ctx, x, y, s, a=1.0):
    """Wall-mounted hot-air hand dryer; returns nozzle position."""
    S = U * s
    w, h = 420 * S, 320 * S
    ctx.save(); ctx.translate(x + 18 * S, y + 22 * S); rrect(ctx, -w / 2, -h / 2, w, h, 70 * S); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill(); ctx.restore()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 70 * S)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.70, 0.72, 0.76), a), (0.3, (0.97, 0.97, 0.99), a), (1, (0.62, 0.64, 0.68), a)])); ctx.fill()
    for k in range(6):                                                        # intake grille on the side
        rrect(ctx, x - w / 2 + 40 * S, y - h / 2 + 60 * S + k * 30 * S, 120 * S, 12 * S, 6 * S); rgba(ctx, (0.25, 0.27, 0.30), 0.85 * a); ctx.fill()
    circle(ctx, x + 110 * S, y - 40 * S, 22 * S, (0.3, 0.8, 0.4), 0.9 * a)
    rrect(ctx, x - 70 * S, y + h / 2 - 10 * S, 140 * S, 70 * S, 20 * S)
    ctx.set_source(lin(0, y + h / 2, 0, y + h / 2 + 60 * S, [(0, (0.55, 0.57, 0.60), a), (1, (0.25, 0.26, 0.28), a)])); ctx.fill()
    return (x, y + h / 2 + 55 * S), (x - w / 2 + 100 * S, y - 10 * S)

def towel_box(ctx, x, y, s, a=1.0):
    S = U * s
    w, h = 300 * S, 380 * S
    ctx.save(); ctx.translate(x + 16 * S, y + 20 * S); rrect(ctx, -w / 2, -h / 2, w, h, 40 * S); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill(); ctx.restore()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 40 * S)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.80, 0.82, 0.86), a), (0.35, (1, 1, 1), a), (1, (0.70, 0.72, 0.76), a)])); ctx.fill()
    rrect(ctx, x - w / 2 + 30 * S, y - h / 2 + 30 * S, w - 60 * S, 150 * S, 20 * S); rgba(ctx, (0.55, 0.75, 0.85), 0.35 * a); ctx.fill()
    # paper towel hanging out
    ctx.move_to(x - 90 * S, y + h / 2 - 20 * S); ctx.line_to(x + 90 * S, y + h / 2 - 20 * S); ctx.line_to(x + 80 * S, y + h / 2 + 130 * S)
    ctx.curve_to(x + 30 * S, y + h / 2 + 145 * S, x - 30 * S, y + h / 2 + 120 * S, x - 85 * S, y + h / 2 + 135 * S); ctx.close_path()
    ctx.set_source(lin(x - 90 * S, 0, x + 90 * S, 0, [(0, (0.85, 0.80, 0.70), a), (0.5, (0.98, 0.95, 0.88), a), (1, (0.82, 0.77, 0.66), a)])); ctx.fill()

def air_stream(ctx, t, x, y0, y1, a=1.0, spread=120):
    for k in range(9):
        e = (t * 1.6 + k / 9) % 1.0
        yy = y0 + (y1 - y0) * e; xx = x + (k - 4) * spread / 4 * U * (0.4 + e)
        ctx.move_to(xx, yy); ctx.line_to(xx + (k - 4) * 4 * U, yy + 60 * U)
        ctx.set_line_width(6 * U); rgba(ctx, (0.85, 0.95, 1.0), 0.45 * a * (1 - e)); ctx.stroke()

def dryer_closeup(ctx, t, scale=1.0, germ_a=1.0, dark=0.45, cx=None, top=None, gap=1000):
    """Dramatic close-up: big hot-air dryer above freshly washed (wet) hands, glowing bacteria raining down."""
    cx = cx if cx is not None else CX
    top = top if top is not None else H * 0.30
    bathroom(ctx, t)
    rgba(ctx, (0.0, 0.02, 0.03), dark); ctx.paint()
    (nx, ny), _ = hot_dryer(ctx, cx, top, 2.1 * scale)
    glow(ctx, nx, ny + 380 * U * scale, 700 * U * scale, GERMC, 0.22 * germ_a)
    air_stream(ctx, t, nx, ny, ny + 520 * U * scale, 1.0, spread=260)
    hy = ny + gap * U * scale
    hand(ctx, nx - 120 * U * scale, hy, 1.45 * scale, -0.12, 1.0, wet=0.9)
    hand(ctx, nx + 120 * U * scale, hy, 1.45 * scale, 0.12, 1.0, wet=0.9, mirror=-1)
    rnd = random.Random(21)
    for i in range(34):
        e = (t * 0.9 + rnd.random()) % 1.0
        germ(ctx, nx + rnd.uniform(-330, 330) * U * scale * (0.4 + e), ny + 40 * U + e * (gap - 360) * U * scale, rnd.uniform(11, 20) * U * scale, t, germ_a * (0.6 + 0.4 * (1 - e)))
    for i in range(16):
        germ(ctx, nx + rnd.uniform(-300, 300) * U * scale, hy - rnd.uniform(80, 420) * U * scale, rnd.uniform(9, 15) * U * scale, t, germ_a * 0.9)
    return nx, ny, hy

def sc_hook(ctx, t, d):
    dryer_closeup(ctx, t, 0.9, prog(t, 0, 0.4) * 0.6 + 0.4, top=H * 0.37, gap=820)

def sc_vs(ctx, t, d):
    bathroom(ctx, t)
    (nx, ny), _ = hot_dryer(ctx, W * 0.30, H * 0.40, 1.15)
    air_stream(ctx, t, nx, ny, ny + 300 * U)
    hand(ctx, nx - 60 * U, ny + 520 * U, 0.85, -0.15, 1.0)
    hand(ctx, nx + 70 * U, ny + 520 * U, 0.85, 0.15, 1.0, mirror=-1)
    rnd = random.Random(2)
    for i in range(10):
        e = (t * 1.2 + rnd.random()) % 1.0
        germ(ctx, nx + rnd.uniform(-130, 130) * U, ny + e * 260 * U, 11 * U, t, 0.9)
    towel_box(ctx, W * 0.76, H * 0.40, 1.15)
    sc_ = 1 + 0.06 * math.sin(t * 6)
    ctx.save(); ctx.translate(W * 0.54, H * 0.43); ctx.scale(sc_, sc_)
    label(ctx, "VS", 0, 0, 90 * U, GOLD, 1.0); ctx.restore()

def sc_dryer(ctx, t, d):
    bathroom(ctx, t)
    (nx, ny), (ix, iy) = hot_dryer(ctx, CX + 60 * U, H * 0.30, 1.35)
    # room air with bacteria pulled into the intake
    rnd = random.Random(8)
    k = prog(t, 0.2, d * 0.5)
    for i in range(18):
        e = ((t * 0.5 + rnd.random()) % 1.0)
        sx, sy = rnd.uniform(-W * 0.05, W * 0.25), rnd.uniform(H * 0.15, H * 0.55)
        px, py = sx + (ix - sx) * e, sy + (iy - sy) * e
        germ(ctx, px, py, 10 * U, t, 0.85 * (1 - e * 0.7))
    # ...and blown onto the hands
    air_stream(ctx, t, nx, ny, ny + 320 * U)
    hy = ny + 560 * U
    hand(ctx, nx - 75 * U, hy, 1.0, -0.12, 1.0)
    hand(ctx, nx + 75 * U, hy, 1.0, 0.12, 1.0, mirror=-1)
    for i in range(14):
        e = (t * 1.3 + rnd.random()) % 1.0
        germ(ctx, nx + rnd.uniform(-150, 150) * U, ny + e * 330 * U, 11 * U, t, 0.9 * k)
    stuck = prog(t, d * 0.45, d * 0.85)
    for i in range(12):
        germ(ctx, nx + rnd.uniform(-200, 200) * U, hy - rnd.uniform(60, 330) * U, 9 * U, t, stuck)
    label(ctx, "BATHROOM AIR IN → ONTO YOUR HANDS", CX, H * 0.07, 50 * U, GERMC, prog(t, 0, 0.3))
    text(ctx, "UNIVERSITY OF CONNECTICUT, 2018", CX, H * 0.112, 38 * U, (0.85, 0.9, 0.95), prog(t, d * 0.3, d * 0.45))

def jet_dryer(ctx, x, y, s, a=1.0):
    S = U * s
    w, h = 380 * S, 640 * S
    ctx.save(); ctx.translate(x + 18 * S, y + 22 * S); rrect(ctx, -w / 2, -h / 2, w, h, 60 * S); rgba(ctx, (0, 0, 0), 0.35 * a); ctx.fill(); ctx.restore()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 60 * S)
    ctx.set_source(lin(x - w / 2, 0, x + w / 2, 0, [(0, (0.45, 0.47, 0.52), a), (0.3, (0.80, 0.82, 0.86), a), (1, (0.35, 0.37, 0.42), a)])); ctx.fill()
    rrect(ctx, x - w / 2 + 30 * S, y - h / 2 + 120 * S, w - 60 * S, 330 * S, 30 * S); rgba(ctx, (0.05, 0.06, 0.08), a); ctx.fill()   # hands slot
    return (x, y - h / 2 + 120 * S), (x, y - h / 2 + 450 * S)

def sc_jet(ctx, t, d):
    bathroom(ctx, t)
    (sx, sy), (bx, by) = jet_dryer(ctx, CX, H * 0.43, 1.25)
    # hands going down into the slot
    hk = prog(t, 0, 0.6)
    ctx.save(); ctx.rectangle(0, 0, W, sy + 220 * U); ctx.clip()
    hand(ctx, CX - 40 * U, sy - 40 * U + 120 * U * hk, 0.75, math.pi, 1.0, wet=0.8)
    hand(ctx, CX + 40 * U, sy - 40 * U + 120 * U * hk, 0.75, math.pi, 1.0, wet=0.8, mirror=-1)
    ctx.restore()
    # droplets + germs sprayed out into the room
    rnd = random.Random(12)
    for i in range(70):
        ph = rnd.random(); e = (t * 0.9 + ph) % 1.0
        side = -1 if i % 2 else 1
        ang = rnd.uniform(-0.9, 0.5)
        sp = rnd.uniform(500, 1100) * U
        px = CX + side * (180 * U + math.cos(ang) * sp * e); py = sy + 120 * U + math.sin(ang) * sp * e + 500 * U * e * e
        al = clamp(1.3 - e)
        circle(ctx, px, py, 14 * U, (0.70, 0.90, 1.0), 0.75 * al)
        circle(ctx, px - 4 * U, py - 4 * U, 5 * U, WHITE, 0.8 * al)
        if i % 2 == 0: germ(ctx, px, py, 13 * U, t, al)
    k = prog(t, 0.1, d * 0.45)
    n = int(round(27 * k))
    sc_ = 1 + 0.05 * math.sin(t * 7)
    ctx.save(); ctx.translate(CX, H * 0.105); ctx.scale(sc_, sc_)
    neon_text(ctx, f"{n}× MORE", 0, 0, 150 * U, GERMC, prog(t, 0.05, 0.3), CYAN, fill=0.3); ctx.restore()
    text(ctx, "AIRBORNE GERMS NEAR JET DRYERS", CX, H * 0.175, 46 * U, WHITE, prog(t, 0.2, 0.5))
    # the twist: who paid for the study
    fk = prog(t, d * 0.62, d * 0.72)
    if fk:
        ctx.save(); ctx.translate(CX, H * 0.62); ctx.rotate(-0.08); ctx.scale(1 + 0.5 * (1 - fk), 1 + 0.5 * (1 - fk))
        font(ctx, 60 * U); w_ = ctx.text_extents("FUNDED BY THE PAPER INDUSTRY").width + 70 * U
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); rgba(ctx, (0, 0, 0), 0.55 * fk); ctx.fill()
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); ctx.set_line_width(9 * U); rgba(ctx, GOLD, fk); ctx.stroke()
        text(ctx, "FUNDED BY THE PAPER INDUSTRY", 0, 0, 60 * U, GOLD, fk); ctx.restore()
    text(ctx, "UNIVERSITY OF LEEDS, 2014", CX, H * 0.675, 38 * U, (0.85, 0.9, 0.95), fk)

def check(ctx, x, y, s, a, col=GREEN):
    if a <= 0: return
    ctx.move_to(x - 40 * s * U, y); ctx.line_to(x - 10 * s * U, y + 32 * s * U); ctx.line_to(x + 48 * s * U, y - 36 * s * U)
    ctx.set_line_width(16 * s * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke()

def sc_verdict(ctx, t, d):
    bathroom(ctx, t)
    t2 = d * 0.48
    if t < t2:
        towel_box(ctx, W * 0.28, H * 0.40, 1.05)
        hot_dryer(ctx, W * 0.72, H * 0.38, 1.05)
        k1 = prog(t, 0.3, 0.7); k2 = prog(t, 0.6, 1.0)
        check(ctx, W * 0.28, H * 0.60, 1.4, k1); check(ctx, W * 0.72, H * 0.60, 1.4, k2)
        label(ctx, "CDC: BOTH WORK", CX, H * 0.10, 70 * U, GREEN, prog(t, 0, 0.3))
    else:
        k = prog(t, t2, d * 0.95)
        wet = 1 - k
        hand(ctx, CX - 110 * U, H * 0.58, 1.35, -0.1, 1.0, wet=wet)
        hand(ctx, CX + 110 * U, H * 0.58, 1.35, 0.1, 1.0, wet=wet, mirror=-1)
        rnd = random.Random(3)
        for i in range(10):                    # drips with germs falling from wet hands
            e = (t * 1.1 + rnd.random()) % 1.0
            px = CX + rnd.uniform(-260, 260) * U; py = H * 0.40 + e * H * 0.25
            circle(ctx, px, py, 10 * U, (0.75, 0.92, 1.0), 0.6 * wet)
            if i % 2 == 0: germ(ctx, px + 14 * U, py, 8 * U, t, 0.8 * wet)
        if k > 0.85:
            glow(ctx, CX, H * 0.45, 500 * U, GREEN, 0.3 * prog(t, d * 0.82, d * 0.95))
        label(ctx, "DRY THEM COMPLETELY", CX, H * 0.10, 66 * U, GOLD, prog(t, t2, t2 + 0.3))
        text(ctx, "WET HANDS SPREAD GERMS MORE EASILY", CX, H * 0.155, 42 * U, WHITE, prog(t, d * 0.65, d * 0.8))

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=CYAN)
    cta(ctx, t, d, "TEAM TOWEL OR TEAM DRYER?", "COMMENT BELOW")

SHORT_SCENES = ["hook", "vs", "dryer", "jet", "verdict", "outro"]
SCENES = dict(hook=sc_hook, vs=sc_vs, dryer=sc_dryer, jet=sc_jet, verdict=sc_verdict, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.10, 0.20, 0.24), (0.02, 0.05, 0.07))
    thumb_text(c, "HAND DRYER", "OR PAPER TOWEL?", "SCIENCE")

def cover(ctx):
    """Poster cover (Nazik 2026-11-10: soignée, qui attrape l'œil, accroche intrigante, sans donner la réponse)."""
    nx, ny, hy = dryer_closeup(ctx, 0.6, 0.78, 1.0, 0.35, top=H * 0.415, gap=800)
    g = cairo.LinearGradient(0, 0, 0, H * 0.36); g.add_color_stop_rgba(0, 0, 0.02, 0.03, 0.92); g.add_color_stop_rgba(1, 0, 0.02, 0.03, 0)
    ctx.rectangle(0, 0, W, H * 0.36); ctx.set_source(g); ctx.fill()
    for dx, dy, col, a in ((9, 11, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "IS YOUR DRYER", CX + dx * U, H * 0.085 + dy * U, 118 * U, col or WHITE, a)
        text(ctx, "BLOWING THIS", CX + dx * U, H * 0.16 + dy * U, 128 * U, col or GERMC, a)
        text(ctx, "ON YOU?", CX + dx * U, H * 0.235 + dy * U, 150 * U, col or GOLD, a)
    # sticker
    ctx.save(); ctx.translate(W * 0.82, H * 0.60); ctx.rotate(0.18)
    circle(ctx, 0, 0, 150 * U, CORAL, 1.0)
    ctx.new_path(); ctx.arc(0, 0, 150 * U, 0, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, WHITE, 0.9); ctx.stroke()
    text(ctx, "27×", 0, -25 * U, 110 * U, WHITE, 1.0); text(ctx, "MORE GERMS?", 0, 60 * U, 36 * U, WHITE, 1.0)
    ctx.restore()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); rgba(ctx, (0.02, 0.03, 0.05), 0.88); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.94 - 58 * U, 940 * U, 116 * U, 58 * U); ctx.set_line_width(6 * U); rgba(ctx, GOLD, 1); ctx.stroke()
    text(ctx, "TOWEL OR DRYER?", CX, H * 0.94, 66 * U, GOLD)
