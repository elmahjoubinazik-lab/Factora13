# Episode 030 (Short, actualité) - "Brooklyn building collapse: what we know" — VERSION RUNWAY (demande de Nazik 2026-11-12)
# SUJET GRAVE (8 morts) : les images Runway sont des VISUALISATIONS EXPLICATIVES (coupes transparentes façon schéma),
# jamais une image réaliste de l'effondrement, des décombres, des secours ou des victimes ; mention permanente
# « AI ILLUSTRATION · NOT FOOTAGE » ; ton sobre, pas de musique, pas de confettis ; aucune cause affirmée.
# Faits et sources : voir meta_en.json. Ancienne version 100 % vectorielle : scenes_vector.py.
exec(open("engine/photo.py", encoding="utf-8").read())

INK = (0.92, 0.94, 0.98)
SOFTGOLD = (0.95, 0.80, 0.45)
KEY_HOOK = os.path.join(RW, "key_hook.png")

def ai_tag(ctx):
    """Avertissement permanent (demande de Nazik 2026-11-12) : images purement illustratives, pas de vraies images."""
    font(ctx, 32 * U); s1 = "ILLUSTRATIVE IMAGES ONLY"; s2 = "NOT REAL IMAGES OF THE EVENT"
    w = max(ctx.text_extents(s1).width, ctx.text_extents(s2).width) + 50 * U; y = H * 0.835
    rrect(ctx, CX - w / 2, y - 50 * U, w, 100 * U, 22 * U); rgba(ctx, (0.02, 0.03, 0.06), 0.82); ctx.fill()
    rrect(ctx, CX - w / 2, y - 50 * U, w, 100 * U, 22 * U); ctx.set_line_width(3 * U); rgba(ctx, SOFTGOLD, 0.8); ctx.stroke()
    text(ctx, s1, CX, y - 20 * U, 32 * U, SOFTGOLD, 1.0); text(ctx, s2, CX, y + 22 * U, 28 * U, (0.85, 0.88, 0.95), 1.0)

def caption_top(ctx, s, y, size, col, a):
    if a <= 0: return
    font(ctx, size); e = ctx.text_extents(s)
    rrect(ctx, CX - e.width / 2 - 26 * U, y - size * 0.75, e.width + 52 * U, size * 1.5, size * 0.4); rgba(ctx, (0.02, 0.03, 0.06), 0.85 * a); ctx.fill()
    text(ctx, s, CX, y, size, col, a)

def dark_bg(ctx, t, darken=0.6):
    paint(ctx, load_img(os.path.join(CLIPS, "outro_bg.jpg")), zoom=1.0 + 0.02 * t)
    rgba(ctx, (0.01, 0.02, 0.05), darken); ctx.paint()

def _hook_fx(ctx, t, d):
    caption_top(ctx, "FLATBUSH, BROOKLYN · NOV 11, 2026", H * 0.13, 50 * U, INK, prog(t, 3.2, 3.6))
    ai_tag(ctx)

def sc_toll(ctx, t, d):
    dark_bg(ctx, t, 0.7)
    k1 = prog(t, 0.2, 0.6); k2 = prog(t, 1.4, 1.8)
    text(ctx, "8", W * 0.28, H * 0.30, 360 * U, INK, k1); text(ctx, "DEATHS", W * 0.28, H * 0.43, 64 * U, (0.8, 0.84, 0.92), k1)
    text(ctx, "17+", W * 0.71, H * 0.30, 280 * U, SOFTGOLD, k2); text(ctx, "INJURED", W * 0.71, H * 0.43, 64 * U, (0.8, 0.84, 0.92), k2)
    ctx.move_to(CX, H * 0.22); ctx.line_to(CX, H * 0.46); ctx.set_line_width(3 * U); rgba(ctx, INK, 0.3 * k1); ctx.stroke()
    text(ctx, "Source: NYC Mayor's Office · Nov 12, 2026", CX, H * 0.50, 36 * U, (0.7, 0.75, 0.85), prog(t, 0.6, 1.0))
    ai_tag(ctx)

def _soil_fx(ctx, t, d):
    caption_top(ctx, "FOUNDATION ON SOIL", H * 0.11, 56 * U, CYAN, prog(t, 0.4, 0.8))
    caption_top(ctx, "SOIL CAN LOSE ITS SUPPORT", H * 0.18, 52 * U, CORAL, prog(t, 3.6, 4.0))
    ai_tag(ctx)

def _rule_fx(ctx, t, d):
    caption_top(ctx, "NYC CODE: PROTECT ADJOINING BUILDINGS", H * 0.11, 40 * U, INK, prog(t, 0.1, 0.4))
    caption_top(ctx, "UNDERPINNING", H * 0.18, 64 * U, GREEN, prog(t, 1.2, 1.6))
    ai_tag(ctx)

def sc_probe(ctx, t, d):
    paint(ctx, load_img(KEY_HOOK), 0.5, 0.55, 1.15 + 0.1 * clamp(t / d))
    rgba(ctx, (0.01, 0.02, 0.05), 0.5); ctx.paint()
    mx = W * (0.38 + 0.22 * math.sin(t * 0.9)); my = H * 0.52
    ctx.new_path(); ctx.arc(mx, my, 130 * U, 0, 2 * math.pi); ctx.set_line_width(14 * U); rgba(ctx, INK, 0.9); ctx.stroke()
    ctx.move_to(mx + 92 * U, my + 92 * U); ctx.line_to(mx + 200 * U, my + 200 * U); ctx.set_line_width(24 * U); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
    k = prog(t, 0.3, 0.6)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.21); ctx.rotate(-0.04)
        font(ctx, 58 * U); w_ = ctx.text_extents("CAUSE: UNDER INVESTIGATION").width + 70 * U
        rrect(ctx, -w_ / 2, -58 * U, w_, 116 * U, 18 * U); rgba(ctx, (0.02, 0.03, 0.06), 0.88 * k); ctx.fill()
        rrect(ctx, -w_ / 2, -58 * U, w_, 116 * U, 18 * U); ctx.set_line_width(6 * U); rgba(ctx, SOFTGOLD, k); ctx.stroke()
        text(ctx, "CAUSE: UNDER INVESTIGATION", 0, 0, 58 * U, SOFTGOLD, k); ctx.restore()
    caption_top(ctx, "NYC DEPT. OF BUILDINGS · LAW ENFORCEMENT", H * 0.29, 38 * U, INK, prog(t, 1.6, 2.0))
    ai_tag(ctx)

def sc_outro(ctx, t, d):
    dark_bg(ctx, t, 0.72)
    k = prog(t, 0.1, 0.5)
    ctx.save(); ctx.translate(CX, H * 0.25); s_ = 1 + 0.04 * math.sin(t * 3); ctx.scale(s_, s_)
    neon_text(ctx, "311", 0, 0, 260 * U, CYAN, k, PURPLE, fill=0.35); ctx.restore()
    caption_top(ctx, "NEW CRACKS NEAR CONSTRUCTION?", H * 0.36, 48 * U, INK, prog(t, 0.6, 1.0))
    text(ctx, "REPORT THEM", CX, H * 0.41, 48 * U, CYAN, prog(t, 0.9, 1.3))
    mk = prog(t, 3.5, 4.3)
    text(ctx, "Our thoughts are with the victims", CX, H * 0.52, 60 * U, INK, mk)
    text(ctx, "and their families.", CX, H * 0.565, 60 * U, INK, mk)
    ai_tag(ctx)

SHORT_SCENES = ["hook", "toll", "soil", "rule", "probe", "outro"]
SCENES = dict(hook=clip_scene("hook", _hook_fx, 0.04, 0.0, top_scrim=0.2, cover_t=0.3),
              toll=sc_toll,
              soil=clip_scene("soil", _soil_fx, top_scrim=0.24),
              rule=clip_scene("rule", _rule_fx, top_scrim=0.24),
              probe=sc_probe, outro=sc_outro)

def thumbnail(c):
    vgrad(c, (0.05, 0.07, 0.13), (0.01, 0.02, 0.05))
    thumb_text(c, "BROOKLYN COLLAPSE", "WHAT WE KNOW", "NEWS")

def cover(ctx):
    """Affiche sobre : la coupe explicative (image clé), titre en 3 lignes dans la zone sûre, bandeau date/lieu."""
    paint(ctx, load_img(KEY_HOOK), 0.5, 0.6, 1.05)
    scrim(ctx, 0.42, 0.9)
    for dx, dy, col, a in ((8, 10, (0, 0, 0), 0.7), (0, 0, None, 1.0)):
        text(ctx, "BROOKLYN", CX + dx * U, H * 0.20 + dy * U, 170 * U, col or INK, a)
        text(ctx, "COLLAPSE", CX + dx * U, H * 0.285 + dy * U, 170 * U, col or SOFTGOLD, a)
        text(ctx, "WHAT WE KNOW", CX + dx * U, H * 0.36 + dy * U, 100 * U, col or CYAN, a)
    rrect(ctx, CX - 470 * U, H * 0.83 - 52 * U, 940 * U, 104 * U, 52 * U); rgba(ctx, (0.02, 0.03, 0.06), 0.9); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.83 - 52 * U, 940 * U, 104 * U, 52 * U); ctx.set_line_width(5 * U); rgba(ctx, SOFTGOLD, 1); ctx.stroke()
    text(ctx, "FLATBUSH · NOV 11, 2026", CX, H * 0.83, 56 * U, SOFTGOLD)
    text(ctx, "Illustration only · not a real image", CX, H * 0.875, 36 * U, (0.85, 0.88, 0.95), 0.95)
