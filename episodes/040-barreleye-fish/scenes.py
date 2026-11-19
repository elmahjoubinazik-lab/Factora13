exec(open("engine/photo.py", encoding="utf-8").read())
# Episode 040 (Short seul, 9:16, ~35 s) - "The Fish With a See-Through Head | Animal Mystery #1"
# 1er épisode de la série « Animal Mysteries » (proposée à Nazik le 2026-11-19, lancée à sa demande pour le soir même).
# 100 % images Runway ; voix ElevenLabs « Jessica » ; musique originale Runway ; mention IA dans la description seulement
# (décision de Nazik du 2026-11-17).
# Faits : Macropinna microstoma (barreleye) ; bouclier transparent rempli de liquide sur la tête, yeux tubulaires verts à
# l'intérieur, qui pivotent vers le haut ou vers l'avant (Robison & Reisenbichler 2008, Copeia ; MBARI) ; les deux points
# au-dessus de la bouche sont les narines ; vit en général vers 600–800 m (≈ 2 000–2 600 ft) ; bouclier détruit par les
# filets, d'où des dessins anciens erronés ; filmé vivant par le ROV du MBARI dans les années 2000.
import json as _json
_TL = {sg["scene"]: sg for sg in _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))}
def ST(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["start"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9
def EN(scene, k):
    sg = _TL.get(scene)
    return sg["sents"][k]["end"] - sg["start"] if sg and k < len(sg["sents"]) else 1e9

DARK = (0.03, 0.02, 0.08)
SERIES = "ANIMAL MYSTERY #1"

def pill(ctx, s, x, y, col, size=46, a=1.0):
    if a <= 0: return
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 60 * U
    rrect(ctx, x - w_ / 2, y - size * 0.8 * U, w_, size * 1.6 * U, size * 0.8 * U); rgba(ctx, col, 0.96 * a); ctx.fill()
    text(ctx, s, x, y, size * U, DARK, a)

def ring(ctx, x, y, r, col, k):
    """Repère simple : cercle lumineux autour d'un détail de l'image."""
    if k <= 0: return
    rr = r * (1.5 - 0.5 * ease(k))
    neon_path(ctx, lambda c: c.arc(x, y, rr, 0, 2 * math.pi), col, 7 * U, k)

OPTS = [("1", "FAKE EYES", CORAL), ("2", "NOSTRILS", CYAN), ("3", "GLOWING LIGHTS", PURPLE)]
def option_card(ctx, n, s_, col, y, k, good=False):
    if k <= 0: return
    pw, ph = W * 0.84, 120 * U; x = CX + (1 - ease(k)) * W * 0.5
    if good: col = GREEN; glow(ctx, x, y, pw * 0.6, GREEN, 0.45)
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); rgba(ctx, (0.04, 0.03, 0.10), 0.9 * k); ctx.fill()
    rrect(ctx, x - pw / 2, y - ph / 2, pw, ph, ph / 2); ctx.set_line_width(7 * U); rgba(ctx, col, k); ctx.stroke()
    circle(ctx, x - pw / 2 + ph / 2, y, ph * 0.38, col, k); text(ctx, n, x - pw / 2 + ph / 2, y, 64 * U, DARK, k)
    font(ctx, 58 * U); tw = ctx.text_extents(s_).width; sz = 58 * U * min(1.0, (pw - ph * 1.5) / tw)
    text(ctx, s_, x + ph * 0.45, y, sz, WHITE, k)

def img_xy(nx, ny, zoom=1.0, fx=0.5, fy=0.5):
    """Point (nx, ny) d'une image Runway (coordonnées 0–1) → écran, avec le même cadrage que paint()."""
    sw, sh = 1536, 2752
    s = max(W / sw, H / sh) * zoom * 1.03
    return CX + (nx - fx) * sw * s, CY + (ny - fy) * sh * s

# positions dans key_hook (0–1), à régler après avoir vu l'image
NOSE = (0.815, 0.515)   # milieu des deux narines
EYES = (0.72, 0.45)     # milieu des deux yeux verts

# ---------------------------------------------------------------- scènes
def hook_ov(ctx, t, d):
    pill(ctx, SERIES, CX, H * 0.06, GOLD, 40, 1.0)
    poster_text(ctx, "SEE-THROUGH", CX, H * 0.12, 140 * U, CYAN, W * 0.88)
    poster_text(ctx, "HEAD?!", CX, H * 0.19, 150 * U, WHITE, W * 0.88)
    pill(ctx, "2,000 FT DEEP", CX, H * 0.255, CYAN, 42, prog(t, 0.6, 0.9))
sc_hook = clip_scene("hook", hook_ov, top_scrim=0.30, cover_t=0.2)

def sc_ask(ctx, t, d):
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.02 + 0.006 * t)
    rgba(ctx, (0.01, 0.02, 0.06), 0.55); ctx.paint()
    x, y = img_xy(NOSE[0], NOSE[1], 1.02 + 0.006 * t)
    ring(ctx, x, y, 90 * U, CORAL, prog(t, 0.0, 0.4))
    for i, (n, s_, col) in enumerate(OPTS):
        s0 = ST("ask", i)
        option_card(ctx, n, s_, col, H * (0.235 + 0.085 * i), prog(t, s0 - 0.05, s0 + 0.30))   # au-dessus du museau : le cercle des narines reste visible
    e0 = EN("ask", 2)
    if t < e0 + 0.1:
        poster_text(ctx, "WHAT ARE THESE?", CX, H * 0.13, 120 * U, GOLD, W * 0.88)
    else:
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e0) / 3)))))
        xx, yy, r = CX, H * 0.12, 110 * U; frac = left / max(0.1, d - 0.1 - e0)
        glow(ctx, xx, yy, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(xx, yy, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), xx, yy, 170 * U, WHITE, 1.0, GOLD, fill=0.4)

def reveal_ov(ctx, t, d):
    option_card(ctx, "2", "IT'S NUMBER 2!", CYAN, H * 0.095, 1.0, good=True)
    poster_text(ctx, "NOSTRILS!", CX, H * 0.17, 140 * U, CYAN, W * 0.90)
    s1, s2 = ST("reveal", 1), ST("reveal", 2)   # le nom de l'animal, à l'oral ET à l'écran (remarque de Nazik, 2026-11-19)
    pill(ctx, "THE BARRELEYE FISH", CX, H * 0.24, GOLD, 50, prog(t, s1, s1 + 0.3))
    pill(ctx, "REAL EYES: THE GREEN DOMES", CX, H * 0.30, GREEN, 42, prog(t, s2, s2 + 0.3))
sc_reveal = clip_scene("reveal", reveal_ov, top_scrim=0.28)

def twist_ov(ctx, t, d):
    poster_text(ctx, "ITS EYES", CX, H * 0.11, 130 * U, WHITE, W * 0.88)
    poster_text(ctx, "ROTATE", CX, H * 0.18, 150 * U, GREEN, W * 0.88)
    pill(ctx, "IT LOOKS UP THROUGH ITS OWN HEAD", CX, H * 0.25, GOLD, 40, prog(t, ST("twist", 1), ST("twist", 1) + 0.3))
sc_twist = clip_scene("twist", twist_ov, top_scrim=0.30)

def sc_fact(ctx, t, d):
    paint(ctx, load_img(RW + "/key_rov.png"), zoom=1.02 + 0.014 * t); scrim(ctx, 0.30)
    poster_text(ctx, "FILMED ALIVE", CX, H * 0.11, 130 * U, WHITE, W * 0.88)
    poster_text(ctx, "ONLY IN THE 2000s", CX, H * 0.18, 110 * U, GOLD, W * 0.90)
    pill(ctx, "NETS CRUSHED ITS CLEAR HEAD", CX, H * 0.25, CORAL, 42, prog(t, 0.3, 0.6))

def sc_outro(ctx, t, d):
    """Retour au poisson de la 1re image (boucle naturelle), puis l'abonnement pour l'épisode suivant (~2 s)."""
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.0 + 0.012 * t); scrim(ctx, 0.26)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0:
            poster_text(ctx, "DID YOU GET", CX, H * 0.11, 130 * U, WHITE, W * 0.88)
            poster_text(ctx, "IT RIGHT?", CX, H * 0.18, 140 * U, GOLD, W * 0.88)
    else:
        rgba(ctx, (0.0, 0.02, 0.04), 0.45 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "SUBSCRIBE FOR", "ANIMAL MYSTERY #2")

SHORT_SCENES = ["hook", "ask", "reveal", "twist", "fact", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, twist=sc_twist, fact=sc_fact, outro=sc_outro)

def cover(ctx):
    """Affiche : le poisson, la question sur les deux « yeux », sans la réponse ; série visible ; zone sûre 14–86 %."""
    paint(ctx, load_img(RW + "/key_hook.png"), fy=0.5, zoom=1.0)
    scrim(ctx, 0.38, 0.85)
    pill(ctx, SERIES, CX, H * 0.16, GOLD, 50, 1.0)
    poster_text(ctx, "WHAT ARE", CX, H * 0.235, 160 * U, WHITE, W * 0.88)
    poster_text(ctx, "THESE 2 DOTS?", CX, H * 0.31, 140 * U, CYAN, W * 0.92)
    x, y = img_xy(NOSE[0], NOSE[1], 1.0)
    ring(ctx, x, y, 95 * U, CORAL, 1.0)
    red_arrow(ctx, CX + 300 * U, H * 0.37, x + 70 * U, y - 80 * U, bend=-0.25)
