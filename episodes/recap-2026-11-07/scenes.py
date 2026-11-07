# Weekly recap 2026-11-07 - "7 Mind-Blowing Facts From This Week"
# Reuses illustrations from the episodes via episode_scenes() (engine), plus intro / title cards / outro drawn here.

A005 = episode_scenes("episodes/005-airplane")
A009 = episode_scenes("episodes/009-hole-earth")
A015 = episode_scenes("episodes/015-no-water")
A013 = episode_scenes("episodes/013-toilet-plume")
A012 = episode_scenes("episodes/012-midterms")
A003 = episode_scenes("episodes/003-blue-sky")
A002 = episode_scenes("episodes/002-earth-spin")

CYAN = (0.35, 0.85, 0.98)
GREEN = (0.42, 0.88, 0.58)
PINK = (1.0, 0.62, 0.78)
TOPICS = [
    ("HOW CAN A 400-TON JET FLY?", GOLD),
    ("A HOLE THROUGH THE EARTH", CORAL),
    ("YOUR BODY WITHOUT WATER", CYAN),
    ("THE LID-OPEN FLUSH", GREEN),
    ("WHY 51 VOTES AREN'T ENOUGH", GOLD),
    ("WHY IS THE SKY BLUE?", CYAN),
    ("IF THE EARTH STOPPED SPINNING", PINK),
]

def bg(ctx, t):
    vgrad(ctx, (0.07, 0.10, 0.24), NAVY); stars(ctx, t, 0.6)

def card(n):
    title, c = TOPICS[n - 1]
    def sc(ctx, t, d):
        bg(ctx, t)
        k = prog(t, 0, 0.6)
        glow(ctx, W * 0.5, H * 0.42, 420 * U, c, 0.25 * k)
        # big rotating ring
        ctx.new_path(); ctx.arc(W * 0.5, H * 0.4, 230 * U * (0.8 + 0.2 * k), t * 0.6, t * 0.6 + 4.6)
        ctx.set_line_width(14 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); rgba(ctx, c, 0.9 * k); ctx.stroke()
        ctx.new_path(); ctx.arc(W * 0.5, H * 0.4, 190 * U, -t * 0.4, -t * 0.4 + 2.5)
        ctx.set_line_width(5 * U); rgba(ctx, WHITE, 0.4 * k); ctx.stroke()
        s = 1.4 - 0.4 * ease(prog(t, 0, 0.7))
        ctx.save(); ctx.translate(W * 0.5, H * 0.4); ctx.scale(s, s)
        text(ctx, "#%d" % n, 6 * U, 8 * U, 230 * U, (0, 0, 0), 0.4 * k)
        text(ctx, "#%d" % n, 0, 0, 230 * U, c, k)
        ctx.restore()
        tk = prog(t, 0.3, 1.0)
        text(ctx, title, W * 0.5 + (1 - tk) * 80 * U, H * 0.7, 72 * U, WHITE, tk)
        # progress dots
        for i in range(7):
            x = W * 0.5 + (i - 3) * 46 * U
            circle(ctx, x, H * 0.08, (14 if i == n - 1 else 9) * U, TOPICS[i][1] if i < n else (0.35, 0.4, 0.55), k)
        chip(ctx, "THIS WEEK ON FACTORA", t)
    return sc

def sc_intro(ctx, t, d):
    bg(ctx, t)
    k = prog(t, 0, 0.8)
    for i, (title, c) in enumerate(TOPICS):
        ang = i / 7 * 2 * math.pi + t * 0.25
        r = 330 * U
        x, y = W * 0.5 + math.cos(ang) * r * 1.6, H * 0.45 + math.sin(ang) * r * 0.9
        a = prog(t, 0.3 + i * 0.35, 0.8 + i * 0.35)
        glow(ctx, x, y, 90 * U, c, 0.3 * a)
        circle(ctx, x, y, 46 * U, c, a)
        text(ctx, str(i + 1), x, y, 48 * U, NAVY, a)
    text(ctx, "7 FASCINATING FACTS", W * 0.5, H * 0.4, 96 * U, WHITE, k)
    text(ctx, "FROM THIS WEEK", W * 0.5, H * 0.52, 72 * U, GOLD, prog(t, 0.5, 1.2))
    chip(ctx, "WEEKLY RECAP", t)

def sc_outro(ctx, t, d):
    bg(ctx, t)
    for i, (title, c) in enumerate(TOPICS):
        k = prog(t, 0.2 + i * 0.25, 0.6 + i * 0.25)
        y = H * (0.12 + 0.085 * i)
        rrect(ctx, W * 0.08, y - 32 * U, W * 0.5, 64 * U, 32 * U); rgba(ctx, (0.08, 0.12, 0.26), 0.9 * k); ctx.fill()
        circle(ctx, W * 0.08 + 32 * U, y, 26 * U, c, k)
        text(ctx, str(i + 1), W * 0.08 + 32 * U, y, 30 * U, NAVY, k)
        text(ctx, title, W * 0.08 + 80 * U, y, 34 * U, WHITE, k, True, "l")
    q = prog(t, d * 0.3, d * 0.4)
    text(ctx, "WHICH ONE", W * 0.79, H * 0.32, 80 * U, WHITE, q)
    text(ctx, "SURPRISED YOU?", W * 0.79, H * 0.42, 70 * U, GOLD, q)
    sk = prog(t, d * 0.55, d * 0.65)
    if sk:
        pulse = 1 + 0.04 * math.sin(t * 5)
        ctx.save(); ctx.translate(W * 0.79, H * 0.58); ctx.scale(pulse * sk, pulse * sk)
        rrect(ctx, -260 * U, -55 * U, 520 * U, 110 * U, 22 * U); rgba(ctx, CORAL); ctx.fill()
        text(ctx, "SUBSCRIBE", 0, 0, 56 * U, WHITE); ctx.restore()

SCENES = {"intro": sc_intro, "outro": sc_outro,
          "c1": card(1), "e005_wing": A005["wing"], "e005_cruise": A005["cruise"], "e005_glide": A005["glide"],
          "c2": card(2), "e009_layers": A009["layers"], "e009_heat": A009["heat"], "e009_center": A009["center"], "e009_antipode": A009["antipode"],
          "c3": card(3), "e015_day1": A015["day1"], "e015_strange": A015["strange"], "e015_camel": A015["camel"], "e015_toomuch": A015["toomuch"],
          "c4": card(4), "e013_plume": A013["plume"], "e013_lid": A013["lid"],
          "c5": card(5), "e012_house": A012["house"], "e012_sixty": A012["sixty"], "e012_both": A012["both"],
          "c6": card(6), "e003_scatter": A003["scatter"], "e003_sunset": A003["sunset"], "e003_space": A003["space"],
          "c7": card(7), "e002_speed": A002["speed"], "e002_day": A002["day"]}
SHORT_SCENES = []

def thumbnail(c):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .08, .11, .26); g.add_color_stop_rgb(1, .02, .03, .08); c.set_source(g); c.paint()
    random.seed(1)
    for _ in range(140):
        c.arc(random.random() * W, random.random() * H, random.uniform(.5, 1.6), 0, 6.3); c.set_source_rgba(1, 1, 1, random.uniform(.3, .8)); c.fill()
    # mosaic of 4 icons on the right
    cells = [(860, 160), (1110, 160), (860, 470), (1110, 470)]
    for i, (x, y) in enumerate(cells):
        col = [GOLD, CYAN, GREEN, CORAL][i]
        glow(c, x, y, 150, col, 0.3)
        rrect(c, x - 110, y - 120, 220, 240, 26); c.set_source_rgba(0.08, 0.12, 0.26, 0.95); c.fill()
        c.set_line_width(5); rgba(c, col); rrect(c, x - 110, y - 120, 220, 240, 26); c.stroke()
    # plane
    x, y = cells[0]
    c.save(); c.translate(x, y); c.rotate(-0.3)
    rrect(c, -80, -12, 160, 24, 12); rgba(c, WHITE); c.fill()
    c.move_to(-10, 0); c.line_to(20, -70); c.line_to(40, -70); c.line_to(30, 0); c.close_path(); c.fill()
    c.move_to(-10, 0); c.line_to(20, 70); c.line_to(40, 70); c.line_to(30, 0); c.close_path(); c.fill()
    c.move_to(-70, 0); c.line_to(-80, -35); c.line_to(-65, -35); c.line_to(-55, 0); c.close_path(); c.fill()
    c.restore()
    # water drop
    x, y = cells[1]
    c.save(); c.translate(x, y); c.scale(60, 60)
    c.move_to(0, -1.4); c.curve_to(0.9, -0.2, 1.0, 1.0, 0, 1.0); c.curve_to(-1.0, 1.0, -0.9, -0.2, 0, -1.4); c.restore()
    rgba(c, CYAN); c.fill()
    # green spray
    x, y = cells[2]
    random.seed(4)
    for _ in range(90):
        rr = random.random() ** 0.7 * 90; an = random.uniform(-2.6, -0.5)
        circle(c, x + math.cos(an) * rr * 0.8, y + 60 + math.sin(an) * rr * 1.3, random.uniform(2, 6), GREEN, random.uniform(0.5, 1))
    rrect(c, x - 60, y + 50, 120, 50, 14); rgba(c, WHITE); c.fill()
    # earth
    x, y = cells[3]
    earth(c, x, y, 75)
    thumb_text(c, "7 MIND-BLOWING", "FACTS THIS WEEK", "WEEKLY RECAP")
