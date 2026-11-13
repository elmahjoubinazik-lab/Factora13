# Episode 028 (Short only) - "What happens if you drink too much water?" — mode Runway (2026-11-12) ; version QUIZ (2026-11-13,
# demande de Nazik : carte quiz au début, sans nouveau crédit Runway — mêmes clips ; ancienne version : build/scenes_v1.py)
# Facts (Mayo Clinic, Cleveland Clinic, MedlinePlus): hyponatremia / water intoxication; healthy kidneys excrete roughly
# 0.8–1.0 L of water per hour (about a quart); drinking much faster dilutes blood sodium, water moves into cells which swell,
# including brain cells → headache, nausea, confusion; severe cases are rare but can be fatal (water-drinking contests,
# endurance events). Prevention: drink to thirst. Prudent tone, no "lethal dose".
exec(open("engine/photo.py", encoding="utf-8").read())

KEY_HOOK = os.path.join(RW, "key_hook.png")

def speed_sign(ctx, x, y, s, a=1.0, num="1", unit="QUART / HOUR"):
    """Panneau de limitation de vitesse à l'américaine (blanc, bord noir) : SPEED LIMIT / 1 / QUART / HOUR."""
    if a <= 0: return
    w, h = 330 * U * s, 420 * U * s
    glow(ctx, x, y, w * 1.1, CYAN, 0.35 * a)
    rrect(ctx, x - w / 2 + 10 * U * s, y - h / 2 + 14 * U * s, w, h, 26 * U * s); rgba(ctx, (0, 0, 0), 0.45 * a); ctx.fill()
    rrect(ctx, x - w / 2, y - h / 2, w, h, 26 * U * s); rgba(ctx, (0.97, 0.97, 0.95), a); ctx.fill()
    rrect(ctx, x - w / 2 + 14 * U * s, y - h / 2 + 14 * U * s, w - 28 * U * s, h - 28 * U * s, 18 * U * s)
    ctx.set_line_width(7 * U * s); rgba(ctx, (0.05, 0.05, 0.06), a); ctx.stroke()
    ink = (0.05, 0.05, 0.06)
    text(ctx, "SPEED", x, y - h * 0.32, 58 * U * s, ink, a); text(ctx, "LIMIT", x, y - h * 0.18, 58 * U * s, ink, a)
    text(ctx, num, x, y + h * 0.06, 170 * U * s, ink, a)
    text(ctx, unit, x, y + h * 0.33, 40 * U * s, ink, a)

OPTS = [("1", "NEVER", CORAL), ("2", "ONLY DIRTY WATER", PURPLE), ("3", "YES, IF YOU DRINK IT TOO FAST", CYAN)]
QUESTION = "CAN TOO MUCH WATER HURT YOU?"

def check_mark(ctx, x, y, s, col, a):
    ctx.save(); ctx.translate(x, y); ctx.move_to(-0.45 * s, 0.0); ctx.line_to(-0.12 * s, 0.32 * s); ctx.line_to(0.5 * s, -0.38 * s)
    ctx.set_line_width(0.2 * s); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND); rgba(ctx, col, a); ctx.stroke(); ctx.restore()

def quiz_card(ctx, t, a=1.0, hot=(), answer=None, y0=0.43, gap=0.078):
    """Les 3 réponses numérotées (lisibles sans le son, dès l'image 1). hot : instants où la voix lit chaque réponse
    (petite pulsation) ; answer : index de la bonne réponse à révéler (les autres s'estompent)."""
    if a <= 0: return
    for i, (n, txt, col) in enumerate(OPTS):
        y = H * (y0 + gap * i)
        dim = 1.0 if answer is None or answer == i else 0.35
        good = answer == i
        c_ = GREEN if good else col
        pulse = 1 + (0.06 * math.exp(-((t - hot[i]) * 5) ** 2) if i < len(hot) else 0) + (0.05 * math.sin(t * 7) if good else 0)
        ctx.save(); ctx.translate(CX, y); ctx.scale(pulse, pulse)
        w_, h_ = W * 0.86, 128 * U
        if good: glow(ctx, 0, 0, w_ * 0.6, GREEN, 0.45 * a)
        rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, (0.02, 0.03, 0.08), 0.86 * a * dim); ctx.fill()
        rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); ctx.set_line_width(6 * U); rgba(ctx, c_, a * dim); ctx.stroke()
        circle(ctx, -w_ / 2 + h_ / 2, 0, h_ * 0.38, c_, a * dim)
        text(ctx, n, -w_ / 2 + h_ / 2, 0, 66 * U, (0.02, 0.03, 0.08), a * dim)
        font(ctx, 50 * U); tw = ctx.text_extents(txt).width; size = 50 * U * min(1.0, (w_ - h_ * 2.3) / tw)
        text(ctx, txt, -w_ / 2 + h_ * 1.05, 0, size, WHITE, a * dim, align="l")
        if good: check_mark(ctx, w_ / 2 - h_ * 0.55, 0, h_ * 0.55, GREEN, a)
        ctx.restore()

def comment_band(ctx, a, y=0.655):
    if a <= 0: return
    s_ = "COMMENT 1, 2 OR 3"; font(ctx, 58 * U); w_ = ctx.text_extents(s_).width + 90 * U
    rrect(ctx, CX - w_ / 2, H * y - 52 * U, w_, 104 * U, 52 * U); rgba(ctx, GOLD, a); ctx.fill()
    text(ctx, s_, CX, H * y, 58 * U, (0.02, 0.03, 0.06), a)

def _hook_fx(ctx, t, d):
    # la question reste à l'écran après le bandeau d'accroche du moteur (qui s'efface vers 3 s)
    kq = prog(t, 2.7, 3.1)
    if kq:
        label(ctx, "CAN TOO MUCH", CX, H * 0.135, 70 * U, WHITE, kq)
        label(ctx, "WATER HURT YOU?", CX, H * 0.19, 70 * U, GOLD, kq)
    quiz_card(ctx, t, 1.0, hot=(2.3, 3.6, 4.9))
    comment_band(ctx, 1.0)

def _kidneys_fx(ctx, t, d):
    k = prog(t, 1.8, 2.1)
    ctx.save(); ctx.translate(CX, H * 0.085); s_ = 1 + 0.25 * math.exp(-((t - 2.2) * 6) ** 2); ctx.scale(s_, s_)
    neon_text(ctx, "≈ 1 QUART / HOUR", 0, 0, 92 * U, CYAN, k, PURPLE, fill=0.45); ctx.restore()
    label(ctx, "(ABOUT 1 LITER)", CX, H * 0.15, 40 * U, WHITE, prog(t, 2.1, 2.4))
    ks = prog(t, 0.15, 0.45)
    if ks:
        sc_ = (1 + 0.5 * (1 - ks)) * (1 + 0.03 * math.sin(t * 6))
        ctx.save(); ctx.translate(W * 0.74, H * 0.42); ctx.rotate(0.06); ctx.scale(sc_, sc_)
        speed_sign(ctx, 0, 0, 1.0, ks, "1", "QUART / HOUR"); ctx.restore()
        label(ctx, "YOUR KIDNEYS", W * 0.74, H * 0.27, 50 * U, GOLD, ks)

def _cells_fx(ctx, t, d):
    label(ctx, "FASTER → SODIUM GETS DILUTED", CX, H * 0.07, 54 * U, GOLD, prog(t, 0.6, 0.9))
    k = prog(t, 3.6, 3.9)
    if k:
        sc_ = 1 + 0.4 * (1 - k)
        ctx.save(); ctx.translate(CX, H * 0.15); ctx.scale(sc_, sc_)
        neon_text(ctx, "CELLS SWELL", 0, 0, 120 * U, CYAN, k, PURPLE, fill=0.5); ctx.restore()
    label(ctx, "EVEN IN YOUR BRAIN", CX, H * 0.22, 48 * U, CORAL, prog(t, 4.6, 4.9))

def _danger_fx(ctx, t, d):
    pulse = 0.18 + 0.10 * math.sin(t * 6)
    g = cairo.RadialGradient(CX, CY, H * 0.25, CX, CY, H * 0.75); g.add_color_stop_rgba(0, 1, 0.1, 0.1, 0); g.add_color_stop_rgba(1, 0.9, 0.05, 0.05, pulse)
    ctx.set_source(g); ctx.paint()
    for i, (w_, x) in enumerate((("HEADACHE", 0.22), ("NAUSEA", 0.50), ("CONFUSION", 0.78))):
        k = prog(t, 0.05 + 0.45 * i, 0.3 + 0.45 * i)
        if k:
            ctx.save(); ctx.translate(W * x, H * (0.10 + 0.045 * (i % 2))); s_ = 1 + 0.4 * (1 - k); ctx.scale(s_, s_)
            label(ctx, w_, 0, 0, 46 * U, CORAL, k); ctx.restore()
    k = prog(t, 1.85, 2.05) * (1 - prog(t, 3.4, 3.6))
    kr = prog(t, 3.55, 3.85)
    if kr:   # « So the answer is three. » : révélation sur la carte quiz
        label(ctx, "THE ANSWER", CX, H * 0.33, 60 * U, GREEN, kr)
        quiz_card(ctx, t, kr, answer=2)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.45); ctx.rotate(-0.07); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
        font(ctx, 62 * U); w_ = ctx.text_extents("RARE, BUT CAN BE DEADLY").width + 70 * U
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.85 * k); ctx.fill()
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, (1.0, 0.2, 0.2), k); ctx.stroke()
        text(ctx, "RARE, BUT CAN BE DEADLY", 0, 0, 62 * U, (1.0, 0.35, 0.35), k); ctx.restore()

SHORT_SCENES = ["hook", "kidneys", "cells", "danger", "outro"]
SCENES = dict(hook=clip_scene("hook", _hook_fx, 0.05, 0.08, cover_t=0.8, fy=0.55, zoom=1.12),
              kidneys=clip_scene("kidneys", _kidneys_fx, top_scrim=0.20),
              cells=clip_scene("cells", _cells_fx, top_scrim=0.27),
              danger=clip_scene("danger", _danger_fx, top_scrim=0.18),
              outro=loop_outro("DID YOU GET IT RIGHT?", "SEND THIS TO A WATER CHUGGER"))

def thumbnail(c):
    vgrad(c, (0.05, 0.12, 0.22), (0.02, 0.04, 0.08))
    thumb_text(c, "TOO MUCH", "WATER?", "BODY")

def cover(ctx):
    """Affiche : le verre qui déborde (image clé de l'accroche), titre en 3 couleurs dans la zone sûre, panneau
    « SPEED LIMIT » comme élément accrocheur, bandeau d'action."""
    paint(ctx, load_img(KEY_HOOK), 0.5, 0.55, 1.1)
    scrim(ctx, 0.40, 0.88)
    poster_text(ctx, "CAN YOU DRINK", CX, H * 0.175, 112 * U, WHITE, W * 0.86)
    poster_text(ctx, "TOO MUCH", CX, H * 0.245, 150 * U, CYAN, W * 0.86)
    poster_text(ctx, "WATER?", CX, H * 0.325, 175 * U, GOLD, W * 0.86)
    quiz_card(ctx, 0.0, 1.0, y0=0.47, gap=0.082)
    comment_band(ctx, 1.0, y=0.775)
