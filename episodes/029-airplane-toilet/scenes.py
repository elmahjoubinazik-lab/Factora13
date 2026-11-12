# Episode 029 (Short only) - "Where does airplane toilet waste really go?" — mode Runway (2026-11-12)
# Facts: airliners use vacuum toilets (valve + pressure difference between cabin and outside air, or a vacuum generator on
# the ground / at low altitude) that pull waste into sealed tanks, usually in the rear; little rinse water; nothing is
# dumped in flight; tanks are drained after landing by a lavatory service truck; "blue ice" comes from rare leaks that
# freeze on the fuselage (FAA). Sources in meta_en.json.
exec(open("engine/photo.py", encoding="utf-8").read())

KEY_HOOK = os.path.join(RW, "key_hook.png")
KEY_TANK = os.path.join(RW, "key_tank.png")

def stamp(ctx, s, x, y, col, k, ang=-0.07, size=60):
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); sc_ = 1 + 0.6 * (1 - k); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 70 * U
    rrect(ctx, -w_ / 2, -size * U, w_, 2 * size * U, 20 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.85 * k); ctx.fill()
    rrect(ctx, -w_ / 2, -size * U, w_, 2 * size * U, 20 * U); ctx.set_line_width(8 * U); rgba(ctx, col, k); ctx.stroke()
    text(ctx, s, 0, 0, size * U, col, k); ctx.restore()

def _hook_fx(ctx, t, d):
    k = prog(t, 0.2, 0.5)
    if k:
        ctx.save(); ctx.translate(W * 0.73, H * 0.44); s_ = 1 + 0.3 * (1 - k); ctx.scale(s_, s_)
        label(ctx, "35,000 FT ✈", 0, 0, 52 * U, CYAN, k); ctx.restore()

def _vacuum_fx(ctx, t, d):
    k = prog(t, 0.0, 0.25)
    sc_ = 1 + 0.25 * math.exp(-((t - 1.6) * 5) ** 2) + 0.03 * math.sin(t * 7)
    ctx.save(); ctx.translate(CX, H * 0.085); ctx.scale(sc_, sc_)
    neon_text(ctx, "VACUUM", 0, 0, 170 * U, CYAN, k, PURPLE, fill=0.45); ctx.restore()
    label(ctx, "NOT WATER", CX, H * 0.16, 46 * U, CORAL, prog(t, 0.3, 0.6))
    label(ctx, "VALVE OPENS → PRESSURE DIFFERENCE", CX, H * 0.215, 42 * U, WHITE, prog(t, 1.8, 2.1))
    stamp(ctx, "WHOOSH!", CX, H * 0.47, GOLD, prog(t, 3.6, 3.8), 0.06, 80)

def _tank(ctx, t, d):
    paint(ctx, load_img(KEY_TANK), 0.55, 0.62, 1.15 + 0.25 * clamp(t / d))   # zoom lent vers le réservoir
    scrim(ctx, 0.22)
    label(ctx, "SEALED TANK", CX, H * 0.07, 70 * U, GOLD, prog(t, 0, 0.25))
    label(ctx, "AT THE BACK OF THE PLANE", CX, H * 0.125, 42 * U, WHITE, prog(t, 0.4, 0.7))
    stamp(ctx, "NOTHING DUMPED IN THE SKY", CX, H * 0.47, CORAL, prog(t, 2.7, 2.9))

def _truck_fx(ctx, t, d):
    label(ctx, "AFTER LANDING", CX, H * 0.07, 66 * U, GOLD, prog(t, 0, 0.25))
    label(ctx, "A SERVICE TRUCK DRAINS IT", CX, H * 0.125, 44 * U, WHITE, prog(t, 0.5, 0.8))
    k = prog(t, 2.6, 2.85)
    if k:
        ctx.save(); ctx.translate(CX, H * 0.42); s_ = 1 + 0.4 * (1 - k); ctx.scale(s_, s_)
        neon_text(ctx, "BLUE ICE", 0, 0, 150 * U, CYAN, k, PURPLE, fill=0.5); ctx.restore()
        label(ctx, "= RARE LEAKS THAT FREEZE", CX, H * 0.50, 44 * U, WHITE, prog(t, 3.0, 3.3))

SHORT_SCENES = ["hook", "vacuum", "tank", "truck", "outro"]
SCENES = dict(hook=clip_scene("hook", _hook_fx, 0.05, 0.08, cover_t=0.4),
              vacuum=clip_scene("vacuum", _vacuum_fx, top_scrim=0.26),
              tank=with_cam(_tank, 0.03, 0.08),
              truck=clip_scene("truck", _truck_fx, top_scrim=0.20),
              outro=loop_outro("SCARED OF PLANE TOILETS?", "SEND THIS TO A NERVOUS FLYER"))

def thumbnail(c):
    vgrad(c, (0.05, 0.12, 0.22), (0.02, 0.04, 0.08))
    thumb_text(c, "AIRPLANE TOILET", "WHERE DOES IT GO?", "AVIATION")

def cover(ctx):
    """Affiche : les toilettes d'avion en inox (image clé), titre dans la zone sûre, flèche dans la cuvette, pastille
    d'altitude, bandeau d'action."""
    paint(ctx, load_img(KEY_HOOK), 0.5, 0.55, 1.05)
    scrim(ctx, 0.40, 0.88)
    poster_text(ctx, "WHERE DOES", CX, H * 0.175, 130 * U, WHITE, W * 0.86)
    poster_text(ctx, "IT REALLY", CX, H * 0.250, 140 * U, CYAN, W * 0.86)
    poster_text(ctx, "GO?", CX, H * 0.335, 200 * U, GOLD, W * 0.86)
    red_arrow(ctx, W * 0.80, H * 0.40, W * 0.53, H * 0.66, -0.30)
    ctx.save(); ctx.translate(W * 0.20, H * 0.47); ctx.rotate(-0.12)
    glow(ctx, 0, 0, 170 * U, CYAN, 0.45); circle(ctx, 0, 0, 120 * U, (0.10, 0.45, 0.95), 1.0)
    ctx.new_path(); ctx.arc(0, 0, 120 * U, 0, 2 * math.pi); ctx.set_line_width(8 * U); rgba(ctx, WHITE, 1); ctx.stroke()
    text(ctx, "35,000", 0, -22 * U, 60 * U, WHITE); text(ctx, "FEET", 0, 40 * U, 46 * U, WHITE)
    ctx.restore()
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 480 * U, H * 0.835 - 56 * U, 960 * U, 112 * U, 56 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "SEND TO A NERVOUS FLYER", CX, H * 0.835, 60 * U, (0.02, 0.03, 0.06))
