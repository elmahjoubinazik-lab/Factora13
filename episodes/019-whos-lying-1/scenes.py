# Episode 019 (Short only) - "Who's Lying? #1" (science detective riddle, fictional story)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.

COLS = [GOLD, CYAN, CORAL, GREEN]
NAMES = ["GUARD", "CLEANER", "PHOTOGRAPHER", "CHEF"]

def bg(ctx, t, top=(0.14, 0.05, 0.30), bot=NAVY):
    vgrad(ctx, top, bot); stars(ctx, t, 0.3)

def person(ctx, x, y, s, col, kind, a=1.0, t=0.0):
    """Stylized character (feet at y). kind: 0 guard (cap), 1 cleaner (bandana), 2 photographer (beret), 3 chef (toque)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    bob = 4 * math.sin(t * 2 + kind)
    # shadow
    ctx.save(); ctx.scale(1, 0.25); circle(ctx, 0, 0, 80, (0, 0, 0), 0.35 * a); ctx.restore()
    # legs
    for lx in (-22, 22):
        rrect(ctx, lx - 14, -150, 28, 150, 12); rgba(ctx, mix(col, NAVY, 0.55), a); ctx.fill()
    # body
    rrect(ctx, -60, -330 + bob, 120, 200, 40)
    g = cairo.LinearGradient(0, -330, 0, -130); g.add_color_stop_rgba(0, *mix(col, WHITE, 0.2), a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.25), a)
    ctx.set_source(g); ctx.fill()
    # head
    circle(ctx, 0, -380 + bob, 50, (0.96, 0.82, 0.68), a)
    circle(ctx, -16, -385 + bob, 6, NAVY, a); circle(ctx, 16, -385 + bob, 6, NAVY, a)
    hy = -420 + bob
    if kind == 0:   # guard cap
        rrect(ctx, -55, hy - 20, 110, 30, 10); rgba(ctx, NAVY, a); ctx.fill()
        rrect(ctx, -10, hy - 34, 20, 18, 4); rgba(ctx, GOLD, a); ctx.fill()
    elif kind == 1: # bandana
        ctx.move_to(-52, hy + 2); ctx.line_to(52, hy + 2); ctx.line_to(0, hy - 30); ctx.close_path(); rgba(ctx, CYAN, a); ctx.fill()
    elif kind == 2: # beret
        ctx.save(); ctx.translate(8, hy - 6); ctx.scale(1, 0.45); circle(ctx, 0, 0, 58, CORAL, a); ctx.restore()
    else:           # chef toque
        rrect(ctx, -38, hy - 70, 76, 70, 12); rgba(ctx, WHITE, a); ctx.fill()
        for dx in (-26, 0, 26): circle(ctx, dx, hy - 72, 26, WHITE, a)
    ctx.restore()

def badge(ctx, x, y, n, col, a=1.0, r=46):
    glow(ctx, x, y, r * 2.2 * U, col, 0.45 * a)
    circle(ctx, x, y, r * U, col, a)
    text(ctx, str(n), x, y, r * 1.3 * U, NAVY, a)

def lineup(ctx, t, a=1.0, hl=-1, y=None):
    y = y if y is not None else H * 0.60
    for i in range(4):
        x = W * (0.14 + 0.24 * i)
        k = prog(t, 0.1 + i * 0.12, 0.5 + i * 0.12) * a
        dim = 1.0 if hl < 0 or hl == i else 0.35
        person(ctx, x, y + (1 - k) * 80 * U, 0.78 * U, COLS[i], i, k * dim, t)
        badge(ctx, x, y + 70 * U, i + 1, COLS[i], k * dim, 40)

def sc_hook(ctx, t, d):
    bg(ctx, t)
    # empty display case with a ghost coin
    cx, cy = CX, H * 0.31
    glow(ctx, cx, cy, 320 * U, GOLD, 0.35)
    rrect(ctx, cx - 170 * U, cy + 60 * U, 340 * U, 70 * U, 10 * U); rgba(ctx, (0.85, 0.82, 0.95)); ctx.fill()
    ctx.rectangle(cx - 150 * U, cy - 180 * U, 300 * U, 240 * U); rgba(ctx, CYAN, 0.12); ctx.fill()
    ctx.set_line_width(5 * U); rgba(ctx, CYAN, 0.8); ctx.rectangle(cx - 150 * U, cy - 180 * U, 300 * U, 240 * U); ctx.stroke()
    sp = abs(math.cos(t * 3))
    ctx.save(); ctx.translate(cx, cy - 50 * U); ctx.scale(max(0.08, sp), 1)
    circle(ctx, 0, 0, 80 * U, GOLD, 0.35 + 0.25 * math.sin(t * 4)); ctx.restore()
    text(ctx, "?", cx, cy - 50 * U, 120 * U, WHITE, 0.9)
    lineup(ctx, t, 1.0, -1, H * 0.60)
    chip(ctx, "WHO'S LYING? #1", t)

def skyline(ctx, y, a=1.0):
    random.seed(9)
    x = 0
    while x < W:
        w = random.uniform(70, 150) * U; h = random.uniform(120, 420) * U
        ctx.rectangle(x, y - h, w, h); rgba(ctx, (0.10, 0.12, 0.28), a); ctx.fill()
        for wy in range(int(h / (40 * U)) - 1):
            for wx in range(int(w / (34 * U))):
                if random.random() < 0.45:
                    ctx.rectangle(x + 10 * U + wx * 34 * U, y - h + 20 * U + wy * 40 * U, 14 * U, 18 * U); rgba(ctx, GOLD, 0.6 * a); ctx.fill()
        x += w + 8 * U

def sc_setting(ctx, t, d):
    bg(ctx, t, (0.04, 0.06, 0.22))
    skyline(ctx, H * 0.66)
    circle(ctx, W * 0.82, H * 0.18, 60 * U, MOON)
    # calendar card
    k = prog(t, 0.1, 0.6)
    cx, cy = W * 0.30, H * 0.36
    rrect(ctx, cx - 170 * U, cy - 190 * U, 340 * U, 380 * U, 30 * U); rgba(ctx, WHITE, k); ctx.fill()
    rrect(ctx, cx - 170 * U, cy - 190 * U, 340 * U, 110 * U, 30 * U); rgba(ctx, CORAL, k); ctx.fill()
    text(ctx, "DEC", cx, cy - 135 * U, 70 * U, WHITE, k)
    text(ctx, "21", cx, cy + 50 * U, 190 * U, NAVY, k)
    # clock
    k2 = prog(t, d * 0.3, d * 0.45)
    ox, oy = W * 0.72, H * 0.38
    circle(ctx, ox, oy, 150 * U, WHITE, k2)
    for i in range(12):
        an = i / 12 * 2 * math.pi
        circle(ctx, ox + math.cos(an) * 125 * U, oy + math.sin(an) * 125 * U, 7 * U, NAVY, k2)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(ox, oy); ctx.line_to(ox, oy - 105 * U); ctx.set_line_width(10 * U); rgba(ctx, NAVY, k2); ctx.stroke()
    an = -math.pi / 2 + 8 / 12 * 2 * math.pi
    ctx.move_to(ox, oy); ctx.line_to(ox + math.cos(an) * 75 * U, oy + math.sin(an) * 75 * U); ctx.set_line_width(14 * U); ctx.stroke()
    text(ctx, "8:00 PM", ox, oy + 210 * U, 70 * U, GOLD, k2)
    text(ctx, "NEW YORK", CX, H * 0.12, 90 * U, WHITE, prog(t, 0, 0.4))

def prop(ctx, kind, x, y, t, a):
    if kind == 0:   # flashlight + beam
        ctx.save(); ctx.translate(x, y); ctx.rotate(-0.3)
        g = cairo.LinearGradient(0, 0, 420 * U, 0); g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.6 * a); g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        ctx.move_to(40 * U, 0); ctx.line_to(420 * U, -140 * U); ctx.line_to(420 * U, 140 * U); ctx.close_path(); ctx.set_source(g); ctx.fill()
        rrect(ctx, -60 * U, -24 * U, 110 * U, 48 * U, 12 * U); rgba(ctx, (0.3, 0.32, 0.45), a); ctx.fill()
        ctx.restore()
    elif kind == 1: # mop + wet floor sign
        ctx.save(); ctx.translate(x, y)
        ctx.move_to(-120 * U, 140 * U); ctx.line_to(-20 * U, 140 * U); ctx.line_to(-70 * U, -60 * U); ctx.close_path(); rgba(ctx, GOLD, a); ctx.fill()
        text(ctx, "WET", -70 * U, 80 * U, 34 * U, NAVY, a)
        ctx.move_to(120 * U, -160 * U); ctx.line_to(80 * U, 120 * U); ctx.set_line_width(12 * U); rgba(ctx, (0.75, 0.6, 0.4), a); ctx.stroke()
        rrect(ctx, 30 * U, 110 * U, 110 * U, 40 * U, 14 * U); rgba(ctx, CYAN, a); ctx.fill()
        for i in range(5):
            ctx.save(); ctx.translate(-150 * U + i * 90 * U, 200 * U); ctx.scale(1, 0.25)
            circle(ctx, 0, 0, (40 + 10 * math.sin(t * 2 + i)) * U, CYAN, 0.4 * a); ctx.restore()
        ctx.restore()
    elif kind == 2: # camera + "sunset" sketch
        ctx.save(); ctx.translate(x, y)
        rrect(ctx, -110 * U, -70 * U, 220 * U, 140 * U, 22 * U); rgba(ctx, (0.25, 0.27, 0.4), a); ctx.fill()
        circle(ctx, 0, 0, 52 * U, (0.1, 0.1, 0.2), a); circle(ctx, 0, 0, 34 * U, CYAN, 0.8 * a); circle(ctx, -12 * U, -12 * U, 10 * U, WHITE, 0.8 * a)
        rrect(ctx, 50 * U, -95 * U, 50 * U, 30 * U, 8 * U); rgba(ctx, (0.25, 0.27, 0.4), a); ctx.fill()
        if (t * 2) % 1 < 0.15: glow(ctx, 75 * U, -80 * U, 160 * U, WHITE, 0.7 * a)
        ctx.restore()
        # sun half-disc on the horizon (the claim)
        sx, sy = x, y - 300 * U
        glow(ctx, sx, sy, 200 * U, CORAL, 0.5 * a)
        ctx.save(); ctx.rectangle(sx - 200 * U, sy - 200 * U, 400 * U, 200 * U); ctx.clip()
        circle(ctx, sx, sy, 110 * U, (1.0, 0.55, 0.3), a); ctx.restore()
        ctx.move_to(sx - 220 * U, sy); ctx.line_to(sx + 220 * U, sy); ctx.set_line_width(5 * U); rgba(ctx, CORAL, a); ctx.stroke()
    else:           # melting ice cream
        ctx.save(); ctx.translate(x, y)
        ctx.move_to(-60 * U, -20 * U); ctx.line_to(60 * U, -20 * U); ctx.line_to(0, 160 * U); ctx.close_path(); rgba(ctx, (0.9, 0.7, 0.4), a); ctx.fill()
        circle(ctx, 0, -60 * U, 75 * U, PINK, a)
        for i, dx in enumerate((-40, 5, 45)):
            ln = (40 + 30 * (0.5 + 0.5 * math.sin(t * 1.5 + i))) * U
            rrect(ctx, dx * U - 10 * U, -20 * U, 20 * U, ln, 10 * U); rgba(ctx, PINK, a); ctx.fill()
        ctx.restore()

QUOTES = ["“DOING MY ROUNDS”", "“MOPPING THE HALL”", "“SHOOTING THE SUNSET”", "“MY ICE CREAM WAS MELTING”"]

def suspect(i):
    def sc(ctx, t, d):
        bg(ctx, t, mix(COLS[i], NAVY, 0.75))
        k = prog(t, 0.0, 0.4)
        glow(ctx, W * 0.30, H * 0.40, 420 * U, COLS[i], 0.35 * k)
        person(ctx, W * 0.30, H * 0.62 + (1 - k) * 120 * U, 1.05 * U, COLS[i], i, k, t)
        prop(ctx, i, W * 0.72, H * 0.50, t, prog(t, 0.3, 0.8))
        badge(ctx, W * 0.12, H * 0.16, i + 1, COLS[i], k, 60)
        text(ctx, NAMES[i], W * 0.22, H * 0.16, 76 * U, WHITE, k, True, "l")
        qk = prog(t, d * 0.35, d * 0.5)
        if qk:
            font(ctx, 52 * U); qw = ctx.text_extents(QUOTES[i]).width
            qs = 52 * U * min(1, W * 0.86 / max(1, qw))
            rrect(ctx, CX - W * 0.46, H * 0.235 - 50 * U, W * 0.92, 100 * U, 50 * U); rgba(ctx, NAVY, 0.88 * qk); ctx.fill()
            text(ctx, QUOTES[i], CX, H * 0.235, qs, COLS[i], qk)
    return sc

def sc_think(ctx, t, d):
    bg(ctx, t, (0.20, 0.04, 0.26))
    lineup(ctx, 10, 1.0, -1, H * 0.60)
    r = 120 * U * (1 + 0.12 * math.sin(t * 12))
    glow(ctx, CX, H * 0.25, 260 * U, PINK, 0.5)
    circle(ctx, CX, H * 0.25, r, PINK)
    ctx.save(); ctx.translate(CX, H * 0.25); ctx.rotate(0.15 * math.sin(t * 6))
    text(ctx, "?", 0, 0, 170 * U, WHITE); ctx.restore()
    text(ctx, "WHO'S LYING?", CX, H * 0.12, 100 * U, GOLD, prog(t, 0, 0.3))

def sc_outro(ctx, t, d):
    bg(ctx, t)
    cta(ctx, t, d, "WHO'S LYING? 1, 2, 3 OR 4?", "COMMENT THE NUMBER")

SHORT_SCENES = ["hook", "setting", "s1", "s2", "s3", "s4", "think", "outro"]
SCENES = dict(hook=sc_hook, setting=sc_setting, s1=suspect(0), s2=suspect(1), s3=suspect(2), s4=suspect(3), think=sc_think, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.14, 0.05, 0.30), NAVY)
    thumb_text(c, "WHO'S", "LYING?", "CAN YOU SOLVE IT?")
