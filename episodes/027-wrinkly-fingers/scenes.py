# Episode 027 (Short only) - "Why do your fingers wrinkle in water?" — mode Runway (2026-11-11, test demandé par Nazik)
# Clips Runway (build/rw/*.mp4, images clés key_*.png) découpés par engine/clips.py ; titres, chiffres et sources par-dessus.
# Facts: finger wrinkling is an active, nerve-controlled reflex (sympathetic vasoconstriction in the fingertip pulp);
# it does not occur when the digital/median nerve is damaged (used as a clinical immersion test); starts after ~5 min in
# warm water. Grip hypothesis: Kareklas et al., Biology Letters 2013; not replicated by Haseleu et al., PLOS ONE 2014.
exec(open("engine/photo.py", encoding="utf-8").read())

KEY_HOOK = os.path.join(RW, "key_hook.png")

def _nerves_fx(ctx, t, d):
    k = prog(t, 0.1, 1.6)
    s_ = 1 + 0.25 * math.exp(-((t - 1.6) * 6) ** 2) + 0.04 * math.sin(t * 7)
    ctx.save(); ctx.translate(CX, H * 0.085); ctx.scale(s_, s_)
    neon_text(ctx, f"{max(1, int(round(5 * k)))} MIN", 0, 0, 170 * U, GOLD, prog(t, 0, 0.25), CORAL, fill=0.45); ctx.restore()
    label(ctx, "IN WARM WATER", CX, H * 0.16, 46 * U, WHITE, prog(t, 0.3, 0.6))
    label(ctx, "NERVES SQUEEZE THE BLOOD VESSELS", CX, H * 0.215, 44 * U, CYAN, prog(t, 2.4, 2.8))
    label(ctx, "SKIN SINKS → WRINKLES", CX, H * 0.62, 56 * U, GOLD, prog(t, 5.2, 5.5))

def _proof(ctx, t, d):
    paint(ctx, load_img(KEY_HOOK), 0.36, 0.24, 1.55 + 0.12 * clamp(t / d))   # gros plan sur un bout de doigt ridé
    scrim(ctx, 0.22)
    label(ctx, "THE PROOF", CX, H * 0.07, 70 * U, GOLD, prog(t, 0, 0.2))
    k = prog(t, 0.9, 1.1)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.47); ctx.rotate(-0.08); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
        font(ctx, 62 * U); w_ = ctx.text_extents("NERVE CUT = NO WRINKLES").width + 70 * U
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.82 * k); ctx.fill()
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, CORAL, k); ctx.stroke()
        text(ctx, "NERVE CUT = NO WRINKLES", 0, 0, 62 * U, CORAL, k); ctx.restore()
    label(ctx, "DOCTORS USE IT AS A NERVE TEST", CX, H * 0.56, 40 * U, WHITE, prog(t, 1.8, 2.1))

def _grip_fx(ctx, t, d):
    label(ctx, "BETTER GRIP ON WET THINGS?", CX, H * 0.07, 58 * U, GREEN, prog(t, 0, 0.25))
    label(ctx, "BIOLOGY LETTERS, 2013", CX, H * 0.12, 36 * U, (0.9, 0.95, 1.0), prog(t, 0.5, 0.8))
    k = prog(t, 4.15, 4.35)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.30); ctx.rotate(0.07); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
        font(ctx, 60 * U); w_ = ctx.text_extents("NOT CONFIRMED").width + 80 * U
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.82 * k); ctx.fill()
        rrect(ctx, -w_ / 2, -60 * U, w_, 120 * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, GOLD, k); ctx.stroke()
        text(ctx, "NOT CONFIRMED", 0, 0, 60 * U, GOLD, k); ctx.restore()
        label(ctx, "PLOS ONE, 2014 · STILL DEBATED", CX, H * 0.375, 38 * U, WHITE, k)

SHORT_SCENES = ["hook", "nerves", "proof", "grip", "outro"]
SCENES = dict(hook=clip_scene("hook", None, 0.05, 0.08, cover_t=0.0),
              nerves=clip_scene("nerves", _nerves_fx, top_scrim=0.26),
              proof=with_cam(_proof, 0.03, 0.08),
              grip=clip_scene("grip", _grip_fx, top_scrim=0.18, fy=0.33, zoom=1.5),   # recadré : cache la bosse d'eau peu naturelle du bas du clip
              outro=loop_outro("WRINKLY FINGERS?", "SEND THIS TO A LONG-SHOWER FRIEND"))

def thumbnail(c):
    vgrad(c, (0.10, 0.20, 0.24), (0.02, 0.05, 0.07))
    thumb_text(c, "WHY DO FINGERS", "WRINKLE IN WATER?", "BODY")

def cover(ctx):
    """Affiche : la main ridée de l'accroche en grand ; titre dans la zone sûre (14–86 %), sous les doigts ; flèche vers un
    bout de doigt ridé ; pastille ; bandeau d'action. Ne cache pas les rides (le sujet)."""
    paint(ctx, load_img(KEY_HOOK))
    g = cairo.LinearGradient(0, H * 0.48, 0, H); g.add_color_stop_rgba(0, 0, 0.01, 0.02, 0); g.add_color_stop_rgba(0.30, 0, 0.01, 0.02, 0.80); g.add_color_stop_rgba(1, 0, 0.01, 0.02, 0.92)
    ctx.rectangle(0, H * 0.48, W, H * 0.52); ctx.set_source(g); ctx.fill()
    poster_text(ctx, "WHY DO YOUR", CX, H * 0.585, 118 * U, WHITE, W * 0.86)
    poster_text(ctx, "FINGERS", CX, H * 0.655, 150 * U, CYAN, W * 0.86)
    poster_text(ctx, "WRINKLE?", CX, H * 0.735, 165 * U, GOLD, W * 0.86)
    red_arrow(ctx, W * 0.80, H * 0.535, W * 0.57, H * 0.215, 0.30)
    ctx.save(); ctx.translate(W * 0.20, H * 0.47); ctx.rotate(-0.14)
    glow(ctx, 0, 0, 170 * U, CORAL, 0.45); circle(ctx, 0, 0, 118 * U, (0.95, 0.12, 0.16), 1.0)
    ctx.new_path(); ctx.arc(0, 0, 118 * U, 0, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, WHITE, 1); ctx.stroke()
    text(ctx, "NOT THE", 0, -30 * U, 42 * U, WHITE); text(ctx, "WATER?", 0, 30 * U, 48 * U, WHITE)
    ctx.restore()
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "COMMENT IF YOURS DO", CX, H * 0.835, 62 * U, (0.02, 0.03, 0.06))
