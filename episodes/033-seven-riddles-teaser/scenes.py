# Episode 033 (vertical 9:16, ~72 s) - extrait de « Test Your Logic: 7 Riddles » (épisode 032) pour TikTok et Instagram
# (demande de Nazik, 2026-11-14) : accroche, énigme 1 avec chrono de 15 s et réponse, énigme 7 SANS réponse, renvoi vers
# la vidéo complète sur YouTube. Réutilise les dessins de l'épisode 032 (batte, balle, portes, chèvre, cartes…), mise en page
# verticale propre. Dessins maison, sans IA. Toutes les tailles en multiples de U.
exec(open("episodes/032-seven-riddles/scenes.py", encoding="utf-8").read())   # dessins + ST() (lit le timeline de CET épisode)

def top_title(ctx, s, col, a=1.0, y=0.105):
    neon_text(ctx, s, CX, H * y, 64 * U, col, a, PURPLE, fill=0.25)

def pill(ctx, s, y, col, a=1.0, size=44):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, CX - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, a); ctx.fill()
    text(ctx, s, CX, y, size * U, (0.03, 0.02, 0.08), a)

def sc_intro(ctx, t, d):
    neon_bg(ctx, t, tint=PURPLE)
    k = 1.0   # titre visible dès la 1re image (la 1re seconde décide si le spectateur reste)
    neon_text(ctx, "TEST YOUR", CX, H * 0.15, 130 * U, WHITE, k, PURPLE, fill=0.3)
    neon_text(ctx, "LOGIC", CX, H * 0.23, 200 * U, GOLD, k, CORAL, fill=0.35)
    for j in range(7):   # les 7 énigmes en pastilles (4 + 3)
        kk = 0.35 + 0.65 * prog(t, 0.1 + j * 0.15, 0.4 + j * 0.15)
        row, col_ = (0, j) if j < 4 else (1, j - 4)
        n = 4 if row == 0 else 3
        x = CX + (col_ - (n - 1) / 2) * 250 * U; y = H * (0.37 + 0.105 * row)
        circle(ctx, x, y, 95 * U * kk, mix(TINT[j], NAVY, 0.6), kk)
        neon_path(ctx, lambda c, x=x, y=y, kk=kk: c.arc(x, y, 95 * U * max(kk, 0.01), 0, 2 * math.pi), TINT[j], 5 * U, kk)
        neon_text(ctx, str(j + 1), x, y, 95 * U, WHITE, kk, TINT[j], fill=0.3)
    pill(ctx, "15 SECONDS EACH", H * 0.56, CYAN, prog(t, 1.5, 1.9), 50)
    neon_text(ctx, "CAN YOU GET 7/7?", CX, H * 0.635, 92 * U, GOLD, prog(t, 2.8, 3.3), CORAL, fill=0.3)

def sc_r1_q(ctx, t, d):
    bg(ctx, t, 0)
    pill(ctx, "RIDDLE 1/7", H * 0.09, PURPLE, 1.0, 46)
    neon_text(ctx, "A BAT + A BALL = $1.10", CX, H * 0.165, 74 * U, WHITE, prog(t, ST("r1_q", 1), ST("r1_q", 1) + 0.4), PURPLE, fill=0.25)
    neon_text(ctx, "THE BAT COSTS $1.00 MORE", CX, H * 0.215, 62 * U, GOLD, prog(t, ST("r1_q", 2), ST("r1_q", 2) + 0.4), CORAL, fill=0.25)
    k = prog(t, 0.2, 0.7)
    bat(ctx, CX - 20 * U, H * 0.38, 1.35, -0.35 + 0.03 * math.sin(t * 1.5), k)
    ball(ctx, CX + 300 * U, H * 0.47 + 12 * U * math.sin(t * 3), 95 * U, k, t)
    kq = prog(t, ST("r1_q", 3), ST("r1_q", 3) + 0.4)
    neon_text(ctx, "THE BALL = ?", CX, H * 0.60, 130 * U, CYAN, kq, PURPLE, fill=0.3)

def sc_r1_t(ctx, t, d):
    bg(ctx, t, 0)
    DUR = 15.0; start = max(0.0, d - DUR - 0.3); left = DUR if t < start else max(0.0, DUR - (t - start))
    pill(ctx, "RIDDLE 1/7", H * 0.09, PURPLE, 1.0, 46)
    neon_text(ctx, "BAT + BALL = $1.10 · BAT = BALL + $1", CX, H * 0.15, 46 * U, WHITE, 1.0, PURPLE, fill=0.2)
    pill(ctx, "COMMENT YOUR ANSWER!", H * 0.21, GOLD, 0.85 + 0.15 * math.sin(t * 4), 46)
    x, y, r = CX, H * 0.40, 290 * U
    frac = left / DUR; col = GREEN if left > 8 else (GOLD if left > 3 else CORAL)
    glow(ctx, x, y, r * 1.5, col, 0.35)
    ctx.new_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.set_line_width(30 * U); rgba(ctx, (0.2, 0.2, 0.3), 0.6); ctx.stroke()
    neon_path(ctx, lambda c: c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), col, 15 * U)
    pulse = 1 + 0.06 * math.exp(-((left % 1.0) - 0.98) ** 2 * 400) if left > 0 else 1
    ctx.save(); ctx.translate(x, y); ctx.scale(pulse, pulse); neon_text(ctx, str(int(math.ceil(left))), 0, 0, 280 * U, col, 1.0, WHITE, fill=0.35); ctx.restore()
    text(ctx, "PAUSE THE VIDEO", CX, H * 0.57, 56 * U, WHITE, 0.95)
    text(ctx, "IF YOU NEED MORE TIME", CX, H * 0.605, 44 * U, (0.8, 0.8, 0.9), 0.95)
    if t >= start + DUR / 2:
        card(ctx, "HINT: DOES BAT + BALL REALLY = $1.10?", CX, H * 0.66, CYAN, prog(t, start + DUR / 2, start + DUR / 2 + 0.5), 38)

def sc_r1_a(ctx, t, d):
    bg(ctx, t, 0)
    pill(ctx, "RIDDLE 1/7", H * 0.09, PURPLE, 1.0, 46)
    s1, s2 = ST("r1_a", 1), ST("r1_a", 2)
    if t < s2:
        big_answer(ctx, t, "10¢ ?", CORAL, prog(t, 0.8, 1.3), y=H * 0.24, size=230)
        if t > s1:
            card(ctx, "BALL 10¢ + BAT $1.10", CX, H * 0.40, CORAL, prog(t, s1, s1 + 0.5), 60)
            card(ctx, "= $1.20!", CX, H * 0.47, CORAL, prog(t, s1 + 2.0, s1 + 2.5), 60)
            cross(ctx, CX, H * 0.24, 190 * U, prog(t, s1 + 3.0, s1 + 3.4))
    else:
        big_answer(ctx, t, "5¢", GREEN, prog(t, s2, s2 + 0.6), y=H * 0.24, size=300)
        k3 = prog(t, s2 + 1.6, s2 + 2.2)
        card(ctx, "BALL 5¢", CX, H * 0.40, GREEN, k3, 64)
        card(ctx, "BAT $1.05", CX, H * 0.47, GOLD, k3, 64)
        card(ctx, "TOTAL $1.10", CX, H * 0.54, CYAN, k3, 64)
        ball(ctx, CX - 330 * U, H * 0.62, 60 * U, k3, t)
        bat(ctx, CX + 120 * U, H * 0.62, 0.9, -0.1, k3)

def sc_r7_q(ctx, t, d):
    bg(ctx, t, 6)
    pill(ctx, "RIDDLE 7/7 · FINAL BOSS", H * 0.09, PURPLE, 1.0, 46)
    neon_text(ctx, "FOOLED EVEN", CX, H * 0.15, 80 * U, WHITE, prog(t, 0.5, 1.0), PURPLE, fill=0.25)
    neon_text(ctx, "MATHEMATICIANS", CX, H * 0.20, 90 * U, GOLD, prog(t, 1.0, 1.5), CORAL, fill=0.3)
    s2, s3 = ST("r7_q", 2), ST("r7_q", 3)
    for n, x in ((1, CX - 360 * U), (2, CX), (3, CX + 360 * U)):
        ok = prog(t, s2 + 2.4, s2 + 3.8) if n == 3 else 0.0
        door(ctx, x, H * 0.40, n, prog(t, ST("r7_q", 1), ST("r7_q", 1) + 0.5), ok, "goat" if n == 3 else None, GOLD if n == 1 and t > s2 else None)
    if t > s2: card(ctx, "YOUR PICK", CX - 360 * U, H * 0.282, GOLD, prog(t, s2, s2 + 0.5), 40)
    options_row(ctx, t, OPTIONS[6], H * 0.60, prog(t, s3, s3 + 0.4), sc=0.95)
    if t > s3: neon_text(ctx, "STAY OR SWITCH?", CX, H * 0.665, 84 * U, CYAN, prog(t, s3, s3 + 0.4), PURPLE, fill=0.3)

def sc_outro(ctx, t, d):
    neon_bg(ctx, t, tint=GOLD)
    s1 = ST("outro", 1)
    if t < s1 + 0.2:
        neon_text(ctx, "STAY OR SWITCH?", CX, H * 0.30, 110 * U, CYAN, prog(t, 0.0, 0.4), PURPLE, fill=0.3)
        pill(ctx, "COMMENT YOUR ANSWER!", H * 0.40, GOLD, prog(t, 0.3, 0.7), 56)
    else:
        cta(ctx, t - s1, d - s1, "ANSWER + 5 MORE RIDDLES", "FULL VIDEO ON YOUTUBE: FACTORA")

SHORT_SCENES = ["intro", "r1_q", "r1_t", "r1_a", "r7_q", "outro"]
SCENES = dict(intro=sc_intro, r1_q=sc_r1_q, r1_t=sc_r1_t, r1_a=sc_r1_a, r7_q=sc_r7_q, outro=sc_outro)

def cover(ctx):
    """Affiche verticale : TEST YOUR LOGIC / CAN YOU GET 7/7? + batte, balle et les 3 portes, dans la zone sûre."""
    t = 0.5
    neon_bg(ctx, t, tint=PURPLE)
    neon_text(ctx, "TEST YOUR", CX, H * 0.18, 130 * U, WHITE, 1.0, PURPLE, fill=0.3)
    neon_text(ctx, "LOGIC", CX, H * 0.26, 210 * U, GOLD, 1.0, CORAL, fill=0.35)
    bat(ctx, CX - 90 * U, H * 0.39, 1.0, -0.30, 1.0)
    ball(ctx, CX + 330 * U, H * 0.40, 75 * U, 1.0, t)
    for n, x in ((1, CX - 330 * U), (2, CX), (3, CX + 330 * U)):
        door(ctx, x, H * 0.585, n, 1.0, 0.0, None, None)
    pill(ctx, "7 RIDDLES · 15 SECONDS EACH", H * 0.725, CYAN, 1.0, 50)
    neon_text(ctx, "CAN YOU GET 7/7?", CX, H * 0.80, 100 * U, GOLD, 1.0, CORAL, fill=0.35)
