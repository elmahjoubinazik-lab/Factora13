# Episode 028 (Short only) - "What happens if you drink too much water?" — mode Runway (2026-11-12, préparé pour validation)
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

def _hook_fx(ctx, t, d):
    k = prog(t, 3.0, 3.3)
    if k:
        sc_ = (1 + 0.5 * (1 - k)) * (1 + 0.03 * math.sin(t * 6))
        ctx.save(); ctx.translate(W * 0.74, H * 0.30); ctx.rotate(0.06); ctx.scale(sc_, sc_)
        speed_sign(ctx, 0, 0, 1.0, k, "1", "QUART / HOUR"); ctx.restore()
        label(ctx, "YOUR KIDNEYS", W * 0.74, H * 0.14, 50 * U, GOLD, k)

def _kidneys_fx(ctx, t, d):
    k = prog(t, 0.0, 0.25)
    ctx.save(); ctx.translate(CX, H * 0.085); s_ = 1 + 0.25 * math.exp(-((t - 0.4) * 6) ** 2); ctx.scale(s_, s_)
    neon_text(ctx, "≈ 1 QUART / HOUR", 0, 0, 92 * U, CYAN, k, PURPLE, fill=0.45); ctx.restore()
    label(ctx, "(ABOUT 1 LITER)", CX, H * 0.15, 40 * U, WHITE, prog(t, 0.3, 0.6))
    label(ctx, "FASTER → EXTRA WATER STAYS IN YOUR BLOOD", CX, H * 0.62, 42 * U, CORAL, prog(t, 1.6, 1.9))

def _cells_fx(ctx, t, d):
    label(ctx, "SODIUM GETS DILUTED", CX, H * 0.07, 60 * U, GOLD, prog(t, 0, 0.25))
    k = prog(t, 1.6, 1.9)
    if k:
        sc_ = 1 + 0.4 * (1 - k)
        ctx.save(); ctx.translate(CX, H * 0.15); ctx.scale(sc_, sc_)
        neon_text(ctx, "CELLS SWELL", 0, 0, 120 * U, CYAN, k, PURPLE, fill=0.5); ctx.restore()
    label(ctx, "EVEN IN YOUR BRAIN", CX, H * 0.22, 48 * U, CORAL, prog(t, 2.6, 2.9))

def _danger_fx(ctx, t, d):
    pulse = 0.18 + 0.10 * math.sin(t * 6)
    g = cairo.RadialGradient(CX, CY, H * 0.25, CX, CY, H * 0.75); g.add_color_stop_rgba(0, 1, 0.1, 0.1, 0); g.add_color_stop_rgba(1, 0.9, 0.05, 0.05, pulse)
    ctx.set_source(g); ctx.paint()
    for i, (w_, x) in enumerate((("HEADACHE", 0.22), ("NAUSEA", 0.50), ("CONFUSION", 0.78))):
        k = prog(t, 0.05 + 0.45 * i, 0.3 + 0.45 * i)
        if k:
            ctx.save(); ctx.translate(W * x, H * (0.10 + 0.045 * (i % 2))); s_ = 1 + 0.4 * (1 - k); ctx.scale(s_, s_)
            label(ctx, w_, 0, 0, 46 * U, CORAL, k); ctx.restore()
    k = prog(t, 1.85, 2.05)
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
              outro=loop_outro("SIP WHEN YOU'RE THIRSTY", "SEND THIS TO A WATER CHUGGER"))

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
    ctx.save(); ctx.translate(W * 0.80, H * 0.56); ctx.rotate(0.08); speed_sign(ctx, 0, 0, 0.78, 1.0, "1", "QUART / HOUR"); ctx.restore()
    label(ctx, "YOUR KIDNEYS", W * 0.80, H * 0.445, 40 * U, GOLD, 1.0)
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "SEND TO A WATER CHUGGER", CX, H * 0.835, 58 * U, (0.02, 0.03, 0.06))
