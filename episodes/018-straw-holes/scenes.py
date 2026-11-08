# Episode 018 (Short only) - "How many holes does a straw have?" (topology debate)
# Executed inside engine/render.py (helpers available). Vertical layout. Original vector illustration.
# All sizes in multiples of U.

def bg(ctx, t, top=(0.12, 0.05, 0.32), bot=NAVY):
    vgrad(ctx, top, bot); stars(ctx, t, 0.35)

STRIPE = CORAL

def straw_body(ctx, cx, cy, rx, h, thick, t, a=1.0, spin=0.0):
    """Cylinder seen slightly from above: rx = radius (x), ellipse ratio 0.32, height h, wall thickness thick.
    When h -> 0 and thick grows, it turns into a flat ring / donut."""
    ry = rx * 0.32
    top = cy - h / 2; bot = cy + h / 2
    # body
    if h > 1:
        ctx.save()
        ctx.new_path(); ctx.move_to(cx - rx, top); ctx.line_to(cx - rx, bot)
        ctx.save(); ctx.translate(cx, bot); ctx.scale(1, ry / rx); ctx.arc_negative(0, 0, rx, math.pi, 0); ctx.restore()
        ctx.line_to(cx + rx, top); ctx.close_path(); ctx.clip()
        g = cairo.LinearGradient(cx - rx, 0, cx + rx, 0)
        g.add_color_stop_rgba(0, 0.75, 0.80, 0.95, a); g.add_color_stop_rgba(0.35, 1, 1, 1, a); g.add_color_stop_rgba(1, 0.55, 0.60, 0.80, a)
        ctx.set_source(g); ctx.paint()
        # diagonal stripes (scroll with spin)
        n = 9
        for i in range(-2, n + 2):
            y0 = top + (i / n) * (h + 2 * rx) - rx + (spin % 1) * (h + 2 * rx) / n
            ctx.new_path(); ctx.move_to(cx - rx, y0); ctx.line_to(cx + rx, y0 - rx * 0.9)
            ctx.line_to(cx + rx, y0 - rx * 0.9 + (h + 2 * rx) / n * 0.45); ctx.line_to(cx - rx, y0 + (h + 2 * rx) / n * 0.45); ctx.close_path()
            rgba(ctx, STRIPE, 0.85 * a); ctx.fill()
        ctx.restore()
    # top opening: outer ellipse + inner dark hole
    ctx.save(); ctx.translate(cx, top); ctx.scale(1, ry / rx)
    ctx.new_path(); ctx.arc(0, 0, rx, 0, 2 * math.pi)
    g = cairo.RadialGradient(0, 0, max(1, rx - thick), 0, 0, rx)
    g.add_color_stop_rgba(0, 1.0, 0.85, 0.45, a); g.add_color_stop_rgba(1, 1.0, 0.55, 0.25, a)
    ctx.set_source(g); ctx.fill()
    ctx.new_path(); ctx.arc(0, 0, max(1, rx - thick), 0, 2 * math.pi)
    g2 = cairo.RadialGradient(0, -rx * 0.2, 0, 0, 0, rx); g2.add_color_stop_rgba(0, 0.02, 0.02, 0.10, a); g2.add_color_stop_rgba(1, 0.10, 0.06, 0.25, a)
    ctx.set_source(g2); ctx.fill()
    ctx.restore()

def sc_hook(ctx, t, d):
    bg(ctx, t)
    cx, cy = CX, H * 0.43
    glow(ctx, cx, cy, 520 * U, CORAL, 0.25)
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.18 + 0.04 * math.sin(t * 1.5)); ctx.translate(-cx, -cy)
    straw_body(ctx, cx, cy, 110 * U, 820 * U * (0.8 + 0.2 * prog(t, 0, 0.8)), 22 * U, t, 1.0, t * 0.4)
    ctx.restore()
    for i, (n, col) in enumerate([("0", CORAL), ("1", GOLD), ("2", CYAN)]):
        k = prog(t, 1.2 + i * 0.35, 1.7 + i * 0.35)
        x = CX + (i - 1) * 330 * U; y = H * 0.615 + 10 * U * math.sin(t * 3 + i)
        if k:
            circle(ctx, x, y, 95 * U * ease(k), col, 0.95)
            text(ctx, n, x, y, 120 * U * ease(k), NAVY)
    chip(ctx, "THE STRAW DEBATE", t)

def card(ctx, x, y, w, h, col, big, label, a, hl=0.0):
    if a <= 0: return
    glow(ctx, x, y, w * 0.8, col, (0.25 + 0.3 * hl) * a)
    rrect(ctx, x - w / 2, y - h / 2, w, h, 40 * U)
    g = cairo.LinearGradient(0, y - h / 2, 0, y + h / 2); g.add_color_stop_rgba(0, *mix(col, WHITE, 0.15), 0.95 * a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.35), 0.95 * a)
    ctx.set_source(g); ctx.fill()
    text(ctx, big, x, y - h * 0.12, 170 * U, NAVY, a)
    font(ctx, 40 * U); lw = ctx.text_extents(label).width
    text(ctx, label, x, y + h * 0.32, 40 * U * min(1, (w - 30 * U) / max(1, lw)), NAVY, a)

def sc_camps(ctx, t, d):
    bg(ctx, t, (0.05, 0.10, 0.32))
    w, h = 300 * U, 420 * U
    ys = H * 0.42
    k0 = prog(t, 0.2, 0.7); k2 = prog(t, d * 0.28, d * 0.4); k1 = prog(t, d * 0.5, d * 0.6)
    card(ctx, CX - 340 * U, ys, w, h, CORAL, "0", "A ROLLED SHEET", k0)
    card(ctx, CX + 340 * U, ys, w, h, CYAN, "2", "ONE PER END", k2)
    card(ctx, CX, ys - 40 * U, w, h, GOLD, "1", "?", k1, 1.0)
    # countdown + comment now
    ck = prog(t, d * 0.62, d * 0.7)
    if ck:
        rem = max(1, 3 - int((t - d * 0.66) / max(0.3, d * 0.11)))
        text(ctx, "COMMENT NOW", CX, H * 0.155, 84 * U, WHITE, ck)
        r = 110 * U * (1 + 0.15 * math.sin(t * 12))
        circle(ctx, CX, H * 0.62, r, PINK, ck)
        text(ctx, str(rem), CX, H * 0.62, 140 * U, WHITE, ck)
    else:
        chip(ctx, "PICK YOUR CAMP", t)

def donut(ctx, cx, cy, R, r, a=1.0, col=GOLD):
    """Torus seen from above at an angle: ring of radius R, tube radius r."""
    ry_ratio = 0.42
    glow(ctx, cx, cy, (R + r) * 1.5, col, 0.35 * a)
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, ry_ratio)
    ctx.new_path(); ctx.arc(0, 0, R + r, 0, 2 * math.pi); ctx.arc_negative(0, 0, max(1, R - r), 2 * math.pi, 0)
    g = cairo.RadialGradient(0, 0, max(1, R - r), 0, 0, R + r)
    g.add_color_stop_rgba(0, *mix(col, NAVY, 0.45), a); g.add_color_stop_rgba(0.45, *mix(col, WHITE, 0.35), a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.3), a)
    ctx.set_source(g); ctx.fill()
    ctx.restore()

def sc_answer(ctx, t, d):
    bg(ctx, t, (0.04, 0.16, 0.30))
    cx, cy = CX, H * 0.50
    k = prog(t, d * 0.22, d * 0.62)          # squash progress
    dk = prog(t, d * 0.55, d * 0.72)         # ring -> donut
    if dk < 1:
        h = 640 * U * (1 - k) + 6 * U
        rx = 120 * U + 230 * U * k
        thick = 24 * U + 150 * U * k
        straw_body(ctx, cx, cy, rx, h, thick, t, 1 - dk, t * 0.3 * (1 - k))
    if dk > 0:
        donut(ctx, cx, cy, 300 * U, 130 * U * (0.6 + 0.4 * dk), dk, GOLD)
        # sprinkles
        random.seed(3)
        for i in range(36):
            an = random.uniform(0, 2 * math.pi); rr = random.uniform(230, 380) * U
            x, y = cx + math.cos(an) * rr, cy + math.sin(an) * rr * 0.42
            ctx.save(); ctx.translate(x, y); ctx.rotate(random.uniform(0, 3))
            rrect(ctx, -12 * U, -4 * U, 24 * U, 8 * U, 4 * U); rgba(ctx, [PINK, CYAN, CORAL, GREEN][i % 4], dk); ctx.fill(); ctx.restore()
    big = prog(t, 0.2, 0.7)
    text(ctx, "MATHEMATICIANS:", CX, H * 0.15, 56 * U, WHITE, big)
    s = 1 + 0.06 * math.sin(t * 6)
    ctx.save(); ctx.translate(CX, H * 0.235); ctx.scale(s, s)
    text(ctx, "1 HOLE", 0, 0, 170 * U, GOLD, big); ctx.restore()
    ek = prog(t, d * 0.78, d * 0.88)
    if ek:
        for sx in (-1, 1):
            ax = cx + sx * 300 * U
            ctx.move_to(ax, cy + 230 * U); ctx.line_to(cx, cy + 40 * U)
        ctx.set_line_width(6 * U); ctx.set_dash([18 * U, 12 * U], -t * 40 * U); rgba(ctx, CYAN, ek); ctx.stroke(); ctx.set_dash([])
        text(ctx, "2 ENDS = SAME HOLE", CX, cy + 300 * U, 64 * U, CYAN, ek)

def pants(ctx, cx, cy, s, a, col):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s)
    glow(ctx, 0, 0, 420, col, 0.3 * a)
    ctx.new_path()
    ctx.move_to(-230, -300); ctx.line_to(230, -300); ctx.line_to(270, 330); ctx.line_to(60, 330); ctx.line_to(0, -40)
    ctx.line_to(-60, 330); ctx.line_to(-270, 330); ctx.close_path()
    g = cairo.LinearGradient(0, -300, 0, 330); g.add_color_stop_rgba(0, *mix(col, WHITE, 0.2), a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.35), a)
    ctx.set_source(g); ctx.fill()
    ctx.rectangle(-230, -300, 460, 60); rgba(ctx, mix(col, NAVY, 0.5), a); ctx.fill()
    for bx in (-150, -50, 50, 150):
        ctx.rectangle(bx - 10, -300, 20, 60); rgba(ctx, NAVY, 0.6 * a); ctx.fill()
    circle(ctx, 0, -270, 14, GOLD, a)
    ctx.restore()

def double_donut(ctx, cx, cy, s, a, col):
    ctx.save(); ctx.translate(cx, cy); ctx.scale(s, s * 0.5)
    glow(ctx, 0, 0, 520, col, 0.35 * a)
    ctx.new_path()
    rrect(ctx, -440, -220, 880, 440, 220)
    ctx.new_sub_path(); ctx.arc_negative(-200, 0, 95, 2 * math.pi, 0)
    ctx.new_sub_path(); ctx.arc_negative(200, 0, 95, 2 * math.pi, 0)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    g = cairo.LinearGradient(0, -220, 0, 220); g.add_color_stop_rgba(0, *mix(col, WHITE, 0.35), a); g.add_color_stop_rgba(1, *mix(col, NAVY, 0.35), a)
    ctx.set_source(g); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    ctx.restore()

def sc_pants(ctx, t, d):
    bg(ctx, t, (0.18, 0.05, 0.30))
    cx, cy = CX, H * 0.44
    ps = 1.2 * U
    pants(ctx, cx, cy, ps * (1 + 0.02 * math.sin(t * 3)), 1.0, PURPLE)
    ok = prog(t, d * 0.42, d * 0.52)
    if ok:
        for i, (x, y) in enumerate([(cx, cy - 300 * ps), (cx - 165 * ps, cy + 330 * ps), (cx + 165 * ps, cy + 330 * ps)]):
            pk = prog(t, d * (0.42 + 0.05 * i), d * (0.5 + 0.05 * i))
            glow(ctx, x, y, 90 * U, GOLD, 0.5 * pk)
            circle(ctx, x, y, 34 * U * (1 + 0.15 * math.sin(t * 8 + i)), GOLD, pk)
    qk = prog(t, d * 0.72, d * 0.8)
    if qk:
        # big pulsing question mark over the pants
        s2 = 1 + 0.08 * math.sin(t * 6)
        ctx.save(); ctx.translate(cx, cy); ctx.scale(s2 * qk, s2 * qk)
        glow(ctx, 0, 0, 300 * U, PINK, 0.5)
        text(ctx, "?", 8 * U, 12 * U, 420 * U, (0, 0, 0), 0.4)
        text(ctx, "?", 0, 0, 420 * U, PINK)
        ctx.restore()
    if ok and not qk:
        text(ctx, "3 OPENINGS", CX, H * 0.155, 100 * U, GOLD, ok)
    elif qk:
        text(ctx, "HOW MANY HOLES?", CX, H * 0.155, 100 * U, PINK, qk)
    else:
        text(ctx, "AND A PAIR OF PANTS?", CX, H * 0.155, 80 * U, WHITE, prog(t, 0.1, 0.6))

def sc_outro(ctx, t, d):
    bg(ctx, t, (0.18, 0.05, 0.30))
    pants(ctx, CX, H * 0.42, 1.5 * U, 0.22, PURPLE)
    cta(ctx, t, d, "HOW MANY HOLES IN PANTS?", "SUBSCRIBE FOR THE ANSWER")

SHORT_SCENES = ["hook", "camps", "answer", "pants", "outro"]
SCENES = dict(hook=sc_hook, camps=sc_camps, answer=sc_answer, pants=sc_pants, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.12, 0.05, 0.32), NAVY)
    thumb_text(c, "HOW MANY HOLES", "IN A STRAW?", "0, 1 OR 2?")
