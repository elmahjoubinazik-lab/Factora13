exec(open("engine/photo.py", encoding="utf-8").read())
# Episode 039 (Short seul, 9:16, ~43 s) - "GTA 6: Why Did It Take 13 Years?"
# Demande de Nazik (2026-11-17), voir 038 pour les règles (droits, mot-clé GTA6, CTA fort).
# Exactitude : on distingue l'OFFICIEL (2 reports, motif « qualité » ; la fuite de 2022 « sans effet à long terme ») du
# CONTEXTE constaté (Red Dead Redemption 2 sorti en oct. 2018 ; GTA V > 230 M d'exemplaires) — jamais présenté comme cause.
import json as _json
_TL = {sg["scene"]: sg for sg in _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["start"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9
def EN(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["end"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9

DARK = (0.03, 0.02, 0.08)

def pill(ctx, s, x, y, col, size=46, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96 * a); ctx.fill()
    text(ctx, s, x, y, size * U, DARK, a)

def pop(ctx, t, t0, fn):
    k = prog(t, t0, t0 + 0.35)
    if k <= 0: return
    s_ = ease(k) * (1 + 0.22 * math.sin(k * math.pi) * (1 - k))
    if s_ < 0.03: return   # échelle quasi nulle : cairo renvoie « out of memory » sur le dégradé du halo
    ctx.save(); fn(ctx, s_); ctx.restore()

def big(ctx, s, y, size, col, glow_col, t, t0=0.15, maxw=None):
    def fn(c, s_):
        c.translate(CX, y); c.scale(s_, s_)
        font(c, size * U); w_ = c.text_extents(s).width; sz = size * U * min(1.0, (maxw or W * 0.9) / max(1, w_))
        glow(c, 0, 0, sz * 2.2, glow_col, 0.35)
        neon_text(c, s, 0, 0, sz, col, 1.0, glow_col, fill=0.5)
    pop(ctx, t, t0, fn)

def counter(ctx, val, t, t0, t1, y, size, col, glow_col, suffix=""):
    v = int(round(val * ease(prog(t, t0, t1))))
    s = f"{v:,}{suffix}"
    font(ctx, size * U); w_ = ctx.text_extents(s).width; sz = size * U * min(1.0, W * 0.9 / max(1, w_))
    glow(ctx, CX, y, sz * 2.4, glow_col, 0.35)
    neon_text(ctx, s, CX, y, sz, col, 1.0, glow_col, fill=0.5)

def tag(ctx, s, col, t):
    pill(ctx, s, CX, H * 0.06, col, 44, prog(t, 0.0, 0.25))

def still(ctx, name, t, z0=1.02, dz=0.012, fy=0.5):
    paint(ctx, load_img(RW + f"/key_{name}.png"), fy=fy, zoom=z0 + dz * t); scrim(ctx, 0.30)

# ---------------------------------------------------------------- scènes
def hook_ov(ctx, t, d):
    big(ctx, "GTA 6", H * 0.11, 260, WHITE, PINK, t, -0.5)   # visible dès l'image 1
    poster_text(ctx, "WHY 13 YEARS?", CX, H * 0.19, 130 * U, GOLD, W * 0.9)
    if t > ST("hook", 0): pill(ctx, "GTA 5: 2013", CX - 230 * U, H * 0.255, CYAN, 46, prog(t, ST("hook", 0), ST("hook", 0) + 0.3))
    if t > ST("hook", 1): pill(ctx, "GTA 6: NOV 2026", CX + 230 * U, H * 0.255, PINK, 46, prog(t, ST("hook", 1), ST("hook", 1) + 0.3))
sc_hook = clip_scene("hook", hook_ov, top_scrim=0.32, cover_t=0.3)

def r1_ov(ctx, t, d):
    tag(ctx, "CONTEXT", CYAN, t)
    poster_text(ctx, "RED DEAD", CX, H * 0.125, 140 * U, CORAL, W * 0.88)
    poster_text(ctx, "REDEMPTION 2", CX, H * 0.19, 120 * U, WHITE, W * 0.88)
    pill(ctx, "RELEASED IN 2018, IN BETWEEN", CX, H * 0.255, GOLD, 44, prog(t, ST("r1", 1) + 1.5, ST("r1", 1) + 1.8))
sc_r1 = clip_scene("r1", r1_ov, top_scrim=0.32)

def sc_r2(ctx, t, d):
    still(ctx, "coins", t)
    tag(ctx, "CONTEXT", CYAN, t)
    poster_text(ctx, "GTA 5 NEVER STOPPED SELLING", CX, H * 0.125, 84 * U, GOLD, W * 0.92)
    counter(ctx, 230_000_000, t, 0.05, 2.6, H * 0.195, 140, WHITE, CYAN, "+")
    pill(ctx, "COPIES SOLD", CX, H * 0.26, GOLD, 44, prog(t, 2.0, 2.3))

def sc_r3(ctx, t, d):
    still(ctx, "calendar", t)
    tag(ctx, "OFFICIAL", GREEN, t)
    big(ctx, "DELAYED ×2", H * 0.13, 170, WHITE, PURPLE, t, 0.3)
    poster_text(ctx, "FALL 2025 → MAY 2026 → NOV 2026", CX, H * 0.2, 62 * U, GOLD, W * 0.92)
    pill(ctx, "REASON GIVEN: QUALITY", CX, H * 0.26, GREEN, 44, prog(t, 3.2, 3.5))

def twist_ov(ctx, t, d):
    if t < EN("twist", 0) + 0.15:
        big(ctx, "THE 2022 LEAK?", H * 0.14, 150, WHITE, GREEN, t, 0.1)
    else:
        tag(ctx, "OFFICIAL", GREEN, t - EN("twist", 0))
        poster_text(ctx, "NO LONG-TERM", CX, H * 0.125, 130 * U, WHITE, W * 0.88)
        poster_text(ctx, "EFFECT", CX, H * 0.19, 130 * U, GREEN, W * 0.88)
        pill(ctx, "ROCKSTAR, SEPTEMBER 2022", CX, H * 0.255, GOLD, 42, prog(t, EN("twist", 0) + 0.4, EN("twist", 0) + 0.7))
sc_twist = clip_scene("twist", twist_ov, top_scrim=0.32)

def sc_outro(ctx, t, d):
    """Retour sur la ville néon, « Worth the wait? », puis le CTA d'abonnement GTA 6."""
    paint(ctx, load_img(RW + "/key_city.png"), zoom=1.0 + 0.01 * t); scrim(ctx, 0.28)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0:
            poster_text(ctx, "WORTH THE WAIT?", CX, H * 0.12, 120 * U, WHITE, W * 0.9)
            pill(ctx, "COMMENT YES OR NO", CX, H * 0.19, GOLD, 52, prog(t, 0.6, 0.9))
    else:
        rgba(ctx, (0.02, 0.0, 0.05), 0.45 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "SUBSCRIBE FOR MORE", "INCREDIBLE FACTS")

SHORT_SCENES = ["hook", "r1", "r2", "r3", "twist", "outro"]
SCENES = dict(hook=sc_hook, r1=sc_r1, r2=sc_r2, r3=sc_r3, twist=sc_twist, outro=sc_outro)

def cover(ctx):
    """Affiche : le sablier sur la plage néon, « GTA 6 » géant, la question ; zone sûre 14–86 %."""
    paint(ctx, load_img(RW + "/key_hourglass.png"), fy=0.55, zoom=1.0)
    scrim(ctx, 0.40, 0.85)
    glow(ctx, CX, H * 0.235, 520 * U, PINK, 0.35)
    neon_text(ctx, "GTA 6", CX, H * 0.235, 330 * U, WHITE, 1.0, PINK, fill=0.55)
    poster_text(ctx, "WHY 13 YEARS?", CX, H * 0.345, 150 * U, GOLD, W * 0.92)   # comme dans la vidéo (plus percutant)
    rrect(ctx, CX - 470 * U, H * 0.47 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.47 - 60 * U, 940 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "2013 → 2026", CX, H * 0.47, 74 * U, (0.02, 0.03, 0.06))
