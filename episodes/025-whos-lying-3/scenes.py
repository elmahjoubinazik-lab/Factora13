# Episode 025 (Short only) - "Who's Lying? #3 — the impostor doctor" — night hospital, same series look as ep. 019
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration. All sizes in U.
# Fictional story. Clue: "98.6 degrees CELSIUS" is impossible (98.6 °F = 37 °C; 98.6 °C ≈ boiling water).
# Reuses badge/lamp/text helpers of ep. 019.
exec(open(os.path.join(os.path.dirname(EP.rstrip("/")), "019-whos-lying-1", "scenes.py"), encoding="utf-8").read())

COLS = [CYAN, GOLD, PINK, GREEN]
NAMES = ["DOCTOR 1", "DOCTOR 2", "DOCTOR 3", "DOCTOR 4"]
QUOTES = ["“HIS PULSE WAS 72 BEATS PER MINUTE”", "“HIS TEMPERATURE WAS 98.6 °C”",
          "“HIS BLOOD PRESSURE WAS 120 OVER 80”", "“I LISTENED TO HIS LUNGS. ALL CLEAR”"]
TEAL = (0.10, 0.32, 0.34)

def lin(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, c, al in stops: g.add_color_stop_rgba(o, c[0], c[1], c[2], al)
    return g

def label(ctx, s, x, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, x - e.width / 2 - 30 * U, y - size * 0.75, e.width + 60 * U, size * 1.5, size * 0.5); rgba(ctx, (0.01, 0.02, 0.03), 0.82 * a); ctx.fill()
    text(ctx, s, x, y, size, col, a)

def corridor(ctx, t, bright=0.0, tint=TEAL):
    """Night hospital corridor in perspective, flickering ceiling lights."""
    vx, vy = CX, H * 0.42
    top = mix((0.03, 0.06, 0.07), tint, 0.5 + 0.4 * bright)
    ctx.set_source(lin(0, 0, 0, H, [(0, mix(top, (0, 0, 0), 0.3), 1), (0.45, top, 1), (1, (0.02, 0.03, 0.04), 1)])); ctx.paint()
    # back wall
    bw, bh = W * 0.30, H * 0.20
    ctx.rectangle(vx - bw / 2, vy - bh / 2, bw, bh); rgba(ctx, mix(top, WHITE, 0.15 + 0.2 * bright), 1); ctx.fill()
    # floor + ceiling planes
    ctx.move_to(0, H); ctx.line_to(W, H); ctx.line_to(vx + bw / 2, vy + bh / 2); ctx.line_to(vx - bw / 2, vy + bh / 2); ctx.close_path()
    ctx.set_source(lin(0, vy + bh / 2, 0, H, [(0, mix(top, WHITE, 0.10), 1), (1, (0.04, 0.06, 0.07), 1)])); ctx.fill()
    ctx.move_to(0, 0); ctx.line_to(W, 0); ctx.line_to(vx + bw / 2, vy - bh / 2); ctx.line_to(vx - bw / 2, vy - bh / 2); ctx.close_path()
    rgba(ctx, (0.02, 0.03, 0.04), 1); ctx.fill()
    # doors on the side walls
    for side in (-1, 1):
        for k, f in enumerate((0.25, 0.55)):
            x0 = vx + side * (bw / 2 + (W / 2 - bw / 2) * f)
            x1 = vx + side * (bw / 2 + (W / 2 - bw / 2) * (f + 0.15))
            yt0 = vy - bh / 2 - (vy - bh / 2) * f * 0.6; yt1 = vy - bh / 2 - (vy - bh / 2) * (f + 0.15) * 0.6
            yb0 = vy + bh / 2 + (H - vy - bh / 2) * f * 0.55; yb1 = vy + bh / 2 + (H - vy - bh / 2) * (f + 0.15) * 0.55
            ctx.move_to(x0, yt0); ctx.line_to(x1, yt1); ctx.line_to(x1, yb1); ctx.line_to(x0, yb0); ctx.close_path()
            rgba(ctx, mix(top, (0.0, 0.0, 0.0), 0.45), 1); ctx.fill()
    # ceiling lights (one flickers)
    for k, f in enumerate((0.15, 0.4, 0.7)):
        y = (vy - bh / 2) * (1 - f) ; w = bw * 0.5 + (W * 0.6 - bw * 0.5) * (1 - f)
        on = 1.0 if k != 1 else (0.25 if int(t * 7) % 5 == 0 else 1.0)
        rrect(ctx, vx - w / 2, y - 14 * U * (1 - f + 0.3), w, 26 * U * (1 - f + 0.3), 8 * U); rgba(ctx, (0.85, 1.0, 0.98), 0.85 * on); ctx.fill()
        glow(ctx, vx, y, w * 0.8, (0.7, 1.0, 0.95), 0.18 * on * (0.5 + bright))

def doctor(ctx, x, y, s, col, kind, a=1.0, t=0.0, lit=0.5):
    """Shadowy doctor (feet at y): white coat, stethoscope, numbered colour, glowing eyes. kind 0 cap, 1 glasses, 2 ponytail, 3 mask."""
    if a <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    sway = 3 * math.sin(t * 1.3 + kind)
    ctx.save(); ctx.scale(1, 0.22); circle(ctx, 0, 0, 120, (0, 0, 0), 0.5 * a); ctx.restore()
    # legs (dark trousers)
    for lx in (-30, 30):
        rrect(ctx, lx - 19, -170, 38, 170, 14); rgba(ctx, mix(INK, col, 0.15), a); ctx.fill()
    # white coat
    coat = mix((0.55, 0.60, 0.66), WHITE, 0.3 + 0.5 * lit)
    ctx.move_to(-78, -380 + sway); ctx.line_to(78, -380 + sway); ctx.line_to(96, -110); ctx.line_to(-96, -110); ctx.close_path()
    ctx.set_source(lin(-96, 0, 96, 0, [(0, mix(coat, (0, 0, 0), 0.35), a), (0.45, coat, a), (1, mix(coat, (0, 0, 0), 0.45), a)])); ctx.fill()
    ctx.move_to(0, -380 + sway); ctx.line_to(0, -110); ctx.set_line_width(4); rgba(ctx, (0, 0, 0), 0.25 * a); ctx.stroke()
    # coloured scrubs V + badge
    ctx.move_to(-34, -380 + sway); ctx.line_to(0, -320 + sway); ctx.line_to(34, -380 + sway); ctx.close_path(); rgba(ctx, col, 0.9 * a); ctx.fill()
    rrect(ctx, 30, -300 + sway, 34, 24, 4); rgba(ctx, col, a); ctx.fill()
    # stethoscope
    ctx.new_path(); ctx.move_to(-30, -385 + sway); ctx.curve_to(-60, -300 + sway, -10, -260 + sway, -20, -230 + sway)
    ctx.set_line_width(7); rgba(ctx, (0.12, 0.12, 0.14), a); ctx.stroke()
    circle(ctx, -20, -222 + sway, 14, (0.75, 0.78, 0.82), a)
    # head
    circle(ctx, 0, -430 + sway, 54, mix(INK, col, 0.18 + 0.3 * lit), a)
    if kind == 0:
        ctx.new_path(); ctx.arc(0, -440 + sway, 58, math.pi, 2 * math.pi); ctx.close_path(); rgba(ctx, col, 0.85 * a); ctx.fill()
    elif kind == 1:
        for gx in (-17, 17):
            ctx.new_path(); ctx.arc(gx, -430 + sway, 15, 0, 2 * math.pi); ctx.set_line_width(5); rgba(ctx, (0.85, 0.85, 0.9), a); ctx.stroke()
    elif kind == 2:
        ctx.new_path(); ctx.arc(0, -445 + sway, 58, math.pi * 1.05, math.pi * 1.95); ctx.set_line_width(18); rgba(ctx, mix(INK, col, 0.5), a); ctx.stroke()
        rrect(ctx, 46, -440 + sway, 26, 90, 13); rgba(ctx, mix(INK, col, 0.5), a); ctx.fill()
    else:
        rrect(ctx, -40, -418 + sway, 80, 42, 14); rgba(ctx, (0.75, 0.90, 0.95), 0.9 * a); ctx.fill()
    ctx.new_path(); ctx.arc(0, -430 + sway, 54, 0, 2 * math.pi); ctx.set_line_width(6); rgba(ctx, col, (0.5 + 0.5 * lit) * a); ctx.stroke()
    ctx.restore()
    eyes(ctx, x, y - (440 - sway) * s, s, a, t + kind)

def lineup_docs(ctx, t, y, s=0.85, a=1.0, lit=0.7, stagger=True):
    for i in range(4):
        x = W * (0.14 + 0.24 * i)
        k = (prog(t, 0.1 + i * 0.25, 0.5 + i * 0.25) if stagger else 1.0) * a
        glow(ctx, x, y - 220 * U * s, 230 * U, COLS[i], 0.25 * k)
        doctor(ctx, x, y, s * U, COLS[i], i, k, t, lit)
        badge(ctx, x, y + 70 * U, i + 1, COLS[i], k)

# ---------------- scenes ----------------
def sc_hook(ctx, t, d):
    corridor(ctx, t, bright=1.0)
    lineup_docs(ctx, t, H * 0.67, 1.0, 1.0, 0.9, stagger=False)
    pulse = 1 + 0.04 * math.sin(t * 6)
    ctx.save(); ctx.translate(CX, H * 0.30); ctx.scale(pulse, pulse)
    for dx, dy, col, al in ((8, 10, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "WHO'S LYING?", dx * U, dy * U, 122 * U, col or CORAL, al)
    ctx.restore()
    chip(ctx, "CASE #3", t)

def file_card(ctx, x, y, s, a, t):
    ctx.save(); ctx.translate(x, y); ctx.rotate(0.12 * math.sin(t * 2)); ctx.scale(s, s)
    rrect(ctx, -150 * U, -200 * U, 300 * U, 400 * U, 16 * U); rgba(ctx, (0.92, 0.88, 0.75), a); ctx.fill()
    rrect(ctx, -150 * U, -200 * U, 300 * U, 70 * U, 16 * U); rgba(ctx, CORAL, a); ctx.fill()
    text(ctx, "PATIENT FILE", 0, -165 * U, 40 * U, WHITE, a)
    for k in range(6):
        rrect(ctx, -110 * U, (-100 + k * 45) * U, (220 - 40 * (k % 2)) * U, 14 * U, 7 * U); rgba(ctx, (0.45, 0.42, 0.38), 0.6 * a); ctx.fill()
    ctx.restore()

def sc_story(ctx, t, d):
    corridor(ctx, t, bright=0.3)
    k = prog(t, 0.2, 0.6); gone = prog(t, d * 0.35, d * 0.55)
    file_card(ctx, CX, H * 0.36 - gone * 200 * U, 1.0 - 0.6 * gone, (1 - gone) * k, t)
    if gone > 0:
        label(ctx, "THE FILE IS GONE", CX, H * 0.21, 92 * U, CORAL, gone)
    lineup_docs(ctx, t, H * 0.66, 0.8, prog(t, d * 0.6, d * 0.75), 0.5)
    label(ctx, "4 DOCTORS · 1 FAKE", CX, H * 0.105, 80 * U, WHITE, prog(t, d * 0.65, d * 0.8))

def prop(ctx, i, x, y, t, a):
    if a <= 0: return
    if i == 0:   # heart monitor, 72 BPM
        rrect(ctx, x - 190 * U, y - 150 * U, 380 * U, 260 * U, 26 * U); rgba(ctx, (0.03, 0.06, 0.06), a); ctx.fill()
        ctx.set_line_width(5 * U); rgba(ctx, (0.4, 0.5, 0.5), a); rrect(ctx, x - 190 * U, y - 150 * U, 380 * U, 260 * U, 26 * U); ctx.stroke()
        ctx.new_path()
        for k in range(120):
            u = k / 119; px = x - 170 * U + u * 340 * U
            ph = (u * 2 + t * 1.2) % 1.0
            spike = 70 * U * math.exp(-((ph - 0.5) * 30) ** 2) - 25 * U * math.exp(-((ph - 0.56) * 30) ** 2)
            (ctx.move_to if k == 0 else ctx.line_to)(px, y - 40 * U - spike)
        ctx.set_line_width(5 * U); rgba(ctx, GREEN, a); ctx.stroke()
        text(ctx, "72 BPM", x, y + 60 * U, 60 * U, GREEN, a)
    elif i == 1: # thermometer 98.6 °C
        rrect(ctx, x - 40 * U, y - 260 * U, 80 * U, 380 * U, 40 * U); rgba(ctx, (0.9, 0.93, 0.96), a); ctx.fill()
        circle(ctx, x, y + 130 * U, 62 * U, CORAL, a)
        rrect(ctx, x - 16 * U, y - 160 * U, 32 * U, 290 * U, 16 * U); rgba(ctx, CORAL, a); ctx.fill()
        for k in range(8):
            ctx.move_to(x + 40 * U, y - 220 * U + k * 40 * U); ctx.line_to(x + 62 * U, y - 220 * U + k * 40 * U)
        ctx.set_line_width(4 * U); rgba(ctx, (0.8, 0.85, 0.9), a); ctx.stroke()
        text(ctx, "98.6 °C", x, y - 310 * U, 60 * U, GOLD, a)
    elif i == 2: # blood pressure gauge 120/80
        circle(ctx, x, y - 40 * U, 150 * U, (0.92, 0.94, 0.97), a)
        ctx.new_path(); ctx.arc(x, y - 40 * U, 150 * U, 0, 2 * math.pi); ctx.set_line_width(10 * U); rgba(ctx, (0.55, 0.58, 0.65), a); ctx.stroke()
        ang = -math.pi * 1.2 + 0.9 * math.pi * (0.55 + 0.03 * math.sin(t * 3))
        ctx.move_to(x, y - 40 * U); ctx.line_to(x + math.cos(ang) * 120 * U, y - 40 * U + math.sin(ang) * 120 * U)
        ctx.set_line_width(7 * U); rgba(ctx, CORAL, a); ctx.stroke()
        text(ctx, "120/80", x, y + 170 * U, 64 * U, WHITE, a)
    else:        # stethoscope on lungs
        for sg in (-1, 1):
            ctx.save(); ctx.translate(x + sg * 75 * U, y - 40 * U); ctx.scale(1, 1.4)
            ctx.arc(0, 0, 70 * U, 0, 2 * math.pi); ctx.restore(); rgba(ctx, (0.95, 0.55, 0.6), 0.85 * a); ctx.fill()
        rrect(ctx, x - 12 * U, y - 200 * U, 24 * U, 90 * U, 10 * U); rgba(ctx, (0.95, 0.65, 0.68), a); ctx.fill()
        sx, sy = x + 60 * U + 30 * U * math.sin(t * 2), y - 30 * U
        ctx.move_to(sx, sy); ctx.curve_to(sx + 120 * U, sy - 120 * U, sx + 40 * U, sy - 260 * U, sx - 60 * U, sy - 260 * U)
        ctx.set_line_width(9 * U); rgba(ctx, (0.15, 0.15, 0.18), a); ctx.stroke()
        circle(ctx, sx, sy, 26 * U, (0.8, 0.82, 0.86), a)
        text(ctx, "ALL CLEAR", x, y + 150 * U, 56 * U, GREEN, a)

def suspect(i):
    def sc(ctx, t, d):
        corridor(ctx, t, bright=0.35, tint=mix(TEAL, COLS[i], 0.35))
        lamp(ctx, t, prog(t, 0, 0.3))
        k = prog(t, 0.05, 0.45)
        doctor(ctx, W * 0.32, H * 0.67 + (1 - k) * 60 * U, 1.15 * U, COLS[i], i, k, t, 0.85)
        prop(ctx, i, W * 0.74, H * 0.50, t, prog(t, 0.3, 0.7))
        badge(ctx, W * 0.12, H * 0.115, i + 1, COLS[i], k, 56)
        text(ctx, NAMES[i], W * 0.21, H * 0.115, 78 * U, WHITE, k, True, "l")
        qk = prog(t, d * 0.25, d * 0.4)
        if qk:
            font(ctx, 50 * U); qw = ctx.text_extents(QUOTES[i]).width
            qs = 50 * U * min(1, W * 0.84 / max(1, qw))
            rrect(ctx, CX - W * 0.46, H * 0.19 - 50 * U, W * 0.92, 100 * U, 50 * U); rgba(ctx, (0, 0, 0), 0.78 * qk); ctx.fill()
            ctx.set_line_width(3 * U); rgba(ctx, COLS[i], 0.8 * qk); rrect(ctx, CX - W * 0.46, H * 0.19 - 50 * U, W * 0.92, 100 * U, 50 * U); ctx.stroke()
            text(ctx, QUOTES[i], CX, H * 0.19, qs, COLS[i], qk)
    return sc

def board_docs(ctx, t, a=1.0):
    rrect(ctx, W * 0.05, H * 0.27, W * 0.9, H * 0.40, 24 * U); rgba(ctx, (0.20, 0.13, 0.10), a); ctx.fill()
    pts = [(W * (0.22 + 0.56 * (i % 2)), H * (0.36 + 0.19 * (i // 2))) for i in range(4)]
    ctx.set_line_width(5 * U)
    for (p, q) in [(0, 3), (1, 2), (0, 1), (2, 3)]:
        ctx.move_to(*pts[p]); ctx.line_to(*pts[q]); rgba(ctx, CORAL, 0.8 * a); ctx.stroke()
    for i, (x, y) in enumerate(pts):
        ctx.save(); ctx.translate(x, y); ctx.rotate((-0.08, 0.06, 0.07, -0.05)[i])
        rrect(ctx, -150 * U, -150 * U, 300 * U, 330 * U, 8 * U); rgba(ctx, (0.95, 0.94, 0.9), a); ctx.fill()
        ctx.rectangle(-130 * U, -130 * U, 260 * U, 240 * U); rgba(ctx, mix(INK, TEAL, 0.5), a); ctx.fill()
        ctx.restore()
        doctor(ctx, x, y + 100 * U, 0.42 * U, COLS[i], i, a, t, 0.8)
        badge(ctx, x, y + 150 * U, i + 1, COLS[i], a, 30)
        circle(ctx, x, y - 140 * U, 14 * U, CORAL, a)

def sc_think(ctx, t, d):
    corridor(ctx, t, bright=0.1, tint=(0.25, 0.06, 0.08))
    z = 1 + 0.10 * prog(t, 0, d)
    ctx.save(); ctx.translate(CX, H * 0.47); ctx.scale(z, z); ctx.translate(-CX, -H * 0.47)
    board_docs(ctx, t)
    ctx.restore()
    pulse = 1 + 0.10 * abs(math.sin(t * 5))
    ctx.save(); ctx.translate(CX, H * 0.155); ctx.scale(pulse, pulse)
    text(ctx, "WHO'S THE FAKE?", 0, 0, 112 * U, CORAL); ctx.restore()

def sc_outro(ctx, t, d):
    corridor(ctx, t, bright=0.0)
    board_docs(ctx, t, 0.22)
    cta(ctx, t, d, "WHO'S THE FAKE? 1, 2, 3 OR 4?", "COMMENT THE NUMBER")

SHORT_SCENES = ["hook", "story", "d1", "d2", "d3", "d4", "think", "outro"]
SCENES = dict(hook=sc_hook, story=sc_story, d1=suspect(0), d2=suspect(1), d3=suspect(2), d4=suspect(3), think=sc_think, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.06, 0.12, 0.14), (0.01, 0.02, 0.03))
    thumb_text(c, "WHO'S", "LYING?", "ONE DOCTOR IS FAKE")
