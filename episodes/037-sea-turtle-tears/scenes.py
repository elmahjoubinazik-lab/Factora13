exec(open("engine/photo.py", encoding="utf-8").read())
# Episode 037 (Short seul, 9:16, ~35 s) - "Why Do Sea Turtles Cry? It's Not Sadness"
# Sujet proposé par Nazik (2026-11-17, piste ChatGPT), dossier en 10 points validé (« merci de préparer la vidéo ») ;
# Nazik publie elle-même (pas de mise en ligne YouTube par l'API).
# 100 % images Runway : clips hook / reveal / twist, images fixes fact et outro (retour à la 1re image).
# Voix ElevenLabs « Jessica ». Musique originale Runway (rw/music.mp3). Mention IA obligatoire.
# Faits : reins des reptiles incapables de produire une urine plus salée que l'eau de mer → glandes à sel lacrymales
# (Science Focus, The Conversation, Olive Ridley Project) ; sécrétion « presque deux fois » plus concentrée que l'eau de mer
# (NOAA ; tortue luth : pic ≈ 1 650 mOsm/kg, Hudson & Lutz 1986) ; tortue luth en train de manger : ≈ 10–15 ml par g de
# glande et par heure, glandes ≈ 622 g → ≈ 6–9 L/h (Davenport et al. 2017, J. Exp. Biol.) → « an estimated two gallons an hour ».
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

OPTS = [("1", "IT'S SAD", CYAN), ("2", "IT'S IN PAIN", CORAL), ("3", "TOO MUCH SALT", GOLD)]
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
    poster_text(ctx, "WHY IS THIS", CX, H * 0.105, 130 * U, WHITE, W * 0.88)
    poster_text(ctx, "TURTLE CRYING?", CX, H * 0.172, 130 * U, GOLD, W * 0.88)
sc_hook = clip_scene("hook", hook_ov, top_scrim=0.28, cover_t=0.2)

def sc_ask(ctx, t, d):
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.08 + 0.006 * t)
    rgba(ctx, (0.01, 0.02, 0.06), 0.62); ctx.paint()
    for i, (n, s_, col) in enumerate(OPTS):
        s0 = ST("ask", i)
        option_card(ctx, n, s_, col, H * (0.40 + 0.09 * i), prog(t, s0 - 0.05, s0 + 0.30))
    e0 = EN("ask", 2)
    if t < e0 + 0.1:
        poster_text(ctx, "WHY THE TEARS?", CX, H * 0.13, 120 * U, GOLD, W * 0.88)
    else:                                            # compte à rebours pendant la pause
        left = max(0.0, (d - 0.1) - t); n = max(1, min(3, int(math.ceil(left / max(0.3, (d - 0.1 - e0) / 3)))))
        x, y, r = CX, H * 0.15, 120 * U; frac = left / max(0.1, d - 0.1 - e0)
        glow(ctx, x, y, r * 1.6, GOLD, 0.35)
        neon_path(ctx, lambda c: c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac), GOLD, 12 * U)
        neon_text(ctx, str(n), x, y, 170 * U, WHITE, 1.0, GOLD, fill=0.4)

def reveal_ov(ctx, t, d):
    option_card(ctx, "3", "IT'S NUMBER 3!", GOLD, H * 0.095, 1.0, good=True)
    poster_text(ctx, "TOO MUCH SALT", CX, H * 0.168, 124 * U, GOLD, W * 0.90)
    pill(ctx, "JELLYFISH = SALTY WATER", CX, H * 0.238, CYAN, 44, prog(t, ST("reveal", 1), ST("reveal", 1) + 0.3))
sc_reveal = clip_scene("reveal", reveal_ov, top_scrim=0.26)

def twist_ov(ctx, t, d):
    """1re phrase : les reins ne suivent pas ; 2e phrase : les glandes à sel, puis « presque 2× plus salé »."""
    if t < EN("twist", 0) + 0.15:
        poster_text(ctx, "KIDNEYS CAN'T", CX, H * 0.105, 124 * U, WHITE, W * 0.88)
        poster_text(ctx, "KEEP UP", CX, H * 0.172, 124 * U, CORAL, W * 0.88)
    else:
        s1, e1 = ST("twist", 1), EN("twist", 1); L = e1 - s1
        poster_text(ctx, "SALT GLANDS", CX, H * 0.12, 128 * U, GOLD, W * 0.84)
        pill(ctx, "ALMOST 2× SALTIER THAN SEAWATER", CX, H * 0.19, CYAN, 44, prog(t, s1 + 0.45 * L, s1 + 0.45 * L + 0.3))
    note(ctx, "SIMPLIFIED ILLUSTRATION", H * 0.25, 1.0)
def sc_twist(ctx, t, d):
    """1re phrase sur l'image clé fixe (léger recul), puis le clip Runway, qui part de cette même image, à vitesse
    presque normale pendant la 2e phrase (sinon le clip étiré sur 8,7 s serait au ralenti ×0,58)."""
    sw = EN("twist", 0) + 0.1
    if t < sw: paint(ctx, load_img(RW + "/key_twist.png"), zoom=1.0 + 0.04 * (1 - t / sw))
    else: paint(ctx, frame("twist", t - sw))
    scrim(ctx, 0.26)
    twist_ov(ctx, t, d)

def sc_fact(ctx, t, d):
    paint(ctx, load_img(RW + "/key_fact.png"), zoom=1.02 + 0.014 * t); scrim(ctx, 0.30)
    k = prog(t, 0.25, 0.65); sc_ = ease(k) * (1 + 0.25 * math.sin(k * math.pi) * (1 - k))
    if sc_ > 0:
        ctx.save(); ctx.translate(CX, H * 0.12); ctx.scale(sc_, sc_)
        glow(ctx, 0, 0, 420 * U, CYAN, 0.35)
        neon_text(ctx, "≈ 2 GALLONS", 0, 0, 124 * U, WHITE, 1.0, CYAN, fill=0.45)
        ctx.restore()
    poster_text(ctx, "AN HOUR", CX, H * 0.19, 120 * U, GOLD, W * 0.88) if t > 0.6 else None
    pill(ctx, "ESTIMATE, WHILE FEEDING (≈ 8 LITERS)", CX, H * 0.25, GOLD, 40, prog(t, 1.2, 1.5))

def sc_outro(ctx, t, d):
    """Retour à la tortue de la 1re image (boucle naturelle), « Not sadness. Survival. », puis le CTA."""
    paint(ctx, load_img(RW + "/key_hook.png"), zoom=1.0 + 0.012 * t); scrim(ctx, 0.24)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0:
            poster_text(ctx, "NOT SADNESS.", CX, H * 0.105, 130 * U, WHITE, W * 0.88)
            poster_text(ctx, "SURVIVAL.", CX, H * 0.172, 140 * U, GOLD, W * 0.88)
    else:
        rgba(ctx, (0.0, 0.02, 0.04), 0.45 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "DID YOU GET IT RIGHT?", "SEND THIS TO A TURTLE LOVER")

SHORT_SCENES = ["hook", "ask", "reveal", "twist", "fact", "outro"]
SCENES = dict(hook=sc_hook, ask=sc_ask, reveal=sc_reveal, twist=sc_twist, fact=sc_fact, outro=sc_outro)

EYE = (0.51, 0.53)   # position de l'œil dans key_hook
def cover(ctx):
    """Affiche : la tortue qui pleure, la question, sans la réponse ; titre et bandeau entre 14 % et 86 % de la hauteur."""
    paint(ctx, load_img(RW + "/key_hook.png"), fy=0.52, zoom=1.0)
    scrim(ctx, 0.36, 0.85)
    poster_text(ctx, "WHY IS THIS", CX, H * 0.19, 165 * U, WHITE, W * 0.88)
    poster_text(ctx, "TURTLE CRYING?", CX, H * 0.265, 150 * U, GOLD, W * 0.90)
    x, y = img_xy(EYE[0], EYE[1], 1.0, fy=0.52)
    red_arrow(ctx, CX + 330 * U, H * 0.31, x + 120 * U, y - 115 * U, bend=-0.25)
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "1, 2 OR 3?", CX, H * 0.80, 74 * U, (0.02, 0.03, 0.06))
