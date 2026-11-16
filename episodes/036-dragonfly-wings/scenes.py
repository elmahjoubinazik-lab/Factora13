exec(open("engine/photo.py", encoding="utf-8").read())
# Episode 036 (Short seul, 9:16, ~34 s) - "Why Do Bacteria Die on Dragonfly Wings?"
# Sujet proposé par Nazik (2026-11-16, piste ChatGPT), dossier en 10 points validé le même jour (titre n° 1).
# 100 % images Runway (règle du 2026-11-16) : clips hook / reveal / twist, image fixe du labo, outro = fin du clip hook.
# Voix ElevenLabs « Jessica ». Musique originale Runway (rw/music.mp3). Mention IA obligatoire.
# Faits : Ivanova et al. 2013 (Nature Communications 4:2838) — ailes de Diplacodes bipunctata et silicium noir
# bactéricides (protubérances ≈ 240 nm) ; Bandara et al. 2017 (ACS Appl. Mater. Interfaces 9(8):6746) — Orthetrum
# villosovittatum / E. coli : adhérence forte puis cisaillement quand la bactérie bouge, membrane déchirée, sans
# perforation directe. Formulations prudentes : « in lab tests », « can tear open », « simplified illustration ».
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

def note(ctx, s, y, a=1.0):
    """Petite mention discrète (« SIMPLIFIED ILLUSTRATION »)."""
    if a <= 0: return
    font(ctx, 34 * U); w_ = ctx.text_extents(s).width + 40 * U
    rrect(ctx, CX - w_ / 2, y - 28 * U, w_, 56 * U, 28 * U); rgba(ctx, (0.0, 0.0, 0.0), 0.55 * a); ctx.fill()
    text(ctx, s, CX, y, 34 * U, (0.85, 0.90, 1.0), 0.9 * a)

OPTS = [("1", "POISON", CORAL), ("2", "TINY PILLARS", CYAN), ("3", "STATIC ELECTRICITY", PURPLE)]
def option_card(ctx, n, s_, col, y, k, good=False, dim=False):
    if k <= 0: return
    pw, ph = W * 0.84, 120 * U; x = CX + (1 - ease(k)) * W * 0.5
    a = 0.35 if dim else 1.0
    if good: col = GREEN; glow(ctx, x, y, pw * 0.6, GREEN, 0.45)
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.9 * k); ctx.fill()
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(7 * U); rgba(ctx, col, k * a); ctx.stroke()
    circle(ctx, x - pw / 2 + ph / 2, y, ph * 0.38, col, k * a); text(ctx, n, x - pw / 2 + ph / 2, y, 64 * U, DARK, k)
    font(ctx, 58 * U); tw = ctx.text_extents(s_).width; sz = 58 * U * min(1.0, (pw - ph * 1.5) / tw)
    text(ctx, s_, x + ph * 0.45, y, sz, WHITE, k * a)

def img_xy(nx, ny, zoom=1.0, fx=0.5, fy=0.5):
    """Point (nx, ny) d'une image Runway (coordonnées 0–1) → écran, avec le même cadrage que paint()."""
    sw, sh = 1536, 2752
    s = max(W / sw, H / sh) * zoom * 1.03
    return CX + (nx - fx) * sw * s, CY + (ny - fy) * sh * s

# ---------------------------------------------------------------- scènes
def hook_ov(ctx, t, d):
    poster_text(ctx, "WHY DO BACTERIA", CX, H * 0.105, 124 * U, GOLD, W * 0.88)
    poster_text(ctx, "DIE ON THIS WING?", CX, H * 0.172, 124 * U, WHITE, W * 0.88)
    pill(ctx, "IN LAB TESTS", CX, H * 0.238, CYAN, 44, prog(t, 0.4, 0.7))
sc_hook = clip_scene("hook", hook_ov, top_scrim=0.28, cover_t=0.2)

def sc_ask(ctx, t, d):
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.08 + 0.006 * t)
    rgba(ctx, (0.01, 0.02, 0.06), 0.62); ctx.paint()
    for i, (n, s_, col) in enumerate(OPTS):
        s0 = ST("ask", i)
        option_card(ctx, n, s_, col, H * (0.40 + 0.09 * i), prog(t, s0 - 0.05, s0 + 0.30))
    e0 = EN("ask", 2)
    if t < e0 + 0.1:
        poster_text(ctx, "HOW DO THEY DIE?", CX, H * 0.13, 120 * U, GOLD, W * 0.88)
    else:                                            # compte à rebours pendant la pause
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e0) / 3)))))
        x, y, r = CX, H * 0.15, 120 * U; frac = left / max(0.1, d - 0.1 - e0)
        glow(ctx, x, y, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), x, y, 170 * U, WHITE, 1.0, GOLD, fill=0.4)

def reveal_ov(ctx, t, d):
    option_card(ctx, "2", "IT'S NUMBER 2!", CYAN, H * 0.095, 1.0, good=True)
    poster_text(ctx, "TINY PILLARS", CX, H * 0.168, 124 * U, CYAN, W * 0.90)
    note(ctx, "SIMPLIFIED ILLUSTRATION", H * 0.228, prog(t, 0.6, 0.9))
sc_reveal = clip_scene("reveal", reveal_ov, top_scrim=0.26)

STEPS = [("STUCK", CYAN), ("MOVE", GOLD), ("TEAR", CORAL)]
def twist_ov(ctx, t, d):
    """« But they don't simply stab. » puis les 3 étapes calées sur la 2e phrase (stuck → move → tear)."""
    if t < EN("twist", 0) + 0.15:
        poster_text(ctx, "THEY DON'T", CX, H * 0.105, 124 * U, WHITE, W * 0.88)
        poster_text(ctx, "JUST STAB...", CX, H * 0.172, 124 * U, CORAL, W * 0.88)
    else:
        s1, e1 = ST("twist", 1), EN("twist", 1); L = e1 - s1
        t1, t2 = s1 + 0.30 * L, s1 + 0.62 * L       # « and when they try to move », « they can tear open »
        step = 0 if t < t1 else (1 if t < t2 else 2)
        for i, (s_, col) in enumerate(STEPS):
            x = CX + (i - 1) * 330 * U
            pill(ctx, s_, x, H * 0.115, col if i <= step else (0.35, 0.35, 0.45), 52)
            if i < 2: text(ctx, "→", x + 168 * U, H * 0.115, 52 * U, WHITE, 0.8)
    note(ctx, "SIMPLIFIED ILLUSTRATION", H * 0.238, 1.0)
sc_twist = clip_scene("twist", twist_ov, top_scrim=0.24)

def sc_lab(ctx, t, d):
    paint(ctx, load_img(RW + "/key_lab.png"), zoom=1.02 + 0.012 * t); scrim(ctx, 0.28)
    poster_text(ctx, "GERM-KILLING", CX, H * 0.105, 130 * U, GREEN, W * 0.88)
    poster_text(ctx, "SURFACES", CX, H * 0.172, 130 * U, WHITE, W * 0.88)
    pill(ctx, "INSPIRED BY DRAGONFLY WINGS", CX, H * 0.238, GOLD, 44, prog(t, 0.5, 0.8))

def sc_outro(ctx, t, d):
    """Retour à la libellule de la 1re image (boucle naturelle), puis « No poison. Just physics. » et le CTA."""
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.0 + 0.012 * t); scrim(ctx, 0.24)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0:
            poster_text(ctx, "NO POISON.", CX, H * 0.105, 130 * U, WHITE, W * 0.88)
            poster_text(ctx, "JUST PHYSICS.", CX, H * 0.172, 130 * U, GOLD, W * 0.88)
    else:
        rgba(ctx, (0.0, 0.02, 0.04), 0.45 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "DID YOU GET IT RIGHT?", "SEND THIS TO A GERMAPHOBE")

SHORT_SCENES = ["hook", "ask", "reveal", "twist", "lab", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, twist=sc_twist, lab=sc_lab, outro=sc_outro)

def cover(ctx):
    """Affiche : la libellule Runway, la question, sans la réponse ; titre et bandeau entre 14 % et 86 % de la hauteur."""
    paint(ctx, load_img(RW + "/key_hook.png"), fy=0.52, zoom=1.0)
    scrim(ctx, 0.36, 0.85)
    poster_text(ctx, "WHY DO BACTERIA", CX, H * 0.19, 140 * U, WHITE, W * 0.88)
    poster_text(ctx, "DIE ON THIS WING?", CX, H * 0.262, 140 * U, GOLD, W * 0.90)
    x, y = img_xy(0.70, 0.40, 1.0, fy=0.52)
    red_arrow(ctx, CX - 250 * U, H * 0.33, x - 40 * U, y - 10 * U, bend=0.25)
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "1, 2 OR 3?", CX, H * 0.80, 74 * U, (0.02, 0.03, 0.06))
