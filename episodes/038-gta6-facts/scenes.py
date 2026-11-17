exec(open("engine/photo.py", encoding="utf-8").read())
# Episode 038 (Short seul, 9:16, ~45 s) - "GTA 6: 5 Facts Most Players Don't Know"
# Demande de Nazik (2026-11-17) : 2 Shorts de 35–45 s sur GTA 6 (sortie le 19/11/2026), mot-clé GTA6 dans la miniature, le titre
# et la description, CTA fort « subscribe for more GTA 6, the phenomenon of 2026 ».
# DROITS : aucune image officielle (pas de logo, de personnage, d'affiche ni d'extrait de bande-annonce) ; images Runway 100 %
# originales (ville néon fictive, manette sans marque, mains sans visage) ; « GTA 6 » seulement en texte (usage nominatif).
# Faits vérifiés : bande-annonce 1 (déc. 2023) 90 421 491 vues YouTube en 24 h, records Guinness ; GTA V sorti en sept. 2013,
# > 230 M d'exemplaires (Take-Two, mai 2026) ; 13 ans d'écart = record de la série ; Leonida, État fictif inspiré de la
# Floride, avec Vice City ; fuite de 90 vidéos le 18/09/2022, confirmée par Rockstar (« work will continue as planned ») ;
# sortie le 19/11/2026 après 2 reports.
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
    """Apparition avec rebond de ce que dessine fn(ctx) (centré sur l'origine)."""
    k = prog(t, t0, t0 + 0.35)
    if k <= 0: return
    s_ = ease(k) * (1 + 0.22 * math.sin(k * math.pi) * (1 - k))
    if s_ < 0.03: return   # échelle quasi nulle : cairo renvoie « out of memory » sur le dégradé du halo
    ctx.save(); fn(ctx, s_); ctx.restore()

def big(ctx, s, y, size, col, glow_col, t, t0=0.15, maxw=None):
    """Grand titre néon qui claque à l'écran."""
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

def fact_tag(ctx, n, t):
    pill(ctx, f"FACT {n}/5", CX, H * 0.06, GOLD, 44, prog(t, 0.0, 0.25))

def still(ctx, name, t, z0=1.02, dz=0.012, fy=0.5):
    paint(ctx, load_img(RW + f"/key_{name}.png"), fy=fy, zoom=z0 + dz * t); scrim(ctx, 0.30)

# ---------------------------------------------------------------- scènes
def hook_ov(ctx, t, d):
    big(ctx, "GTA 6", H * 0.12, 300, WHITE, PINK, t, -0.5)   # visible dès l'image 1
    poster_text(ctx, "5 FACTS YOU DON'T KNOW", CX, H * 0.215, 92 * U, GOLD, W * 0.92)
    if t > ST("hook", 1): pill(ctx, "NUMBER 5 IS WILD", CX, H * 0.275, CYAN, 46, prog(t, ST("hook", 1), ST("hook", 1) + 0.3))
sc_hook = clip_scene("hook", hook_ov, top_scrim=0.32, cover_t=0.3)

def sc_f1(ctx, t, d):
    still(ctx, "controller", t)
    fact_tag(ctx, 1, t)
    counter(ctx, 90_000_000, t, 0.05, 2.4, H * 0.14, 150, WHITE, PINK)
    poster_text(ctx, "VIEWS IN 24 HOURS", CX, H * 0.205, 84 * U, GOLD, W * 0.9)
    if t > ST("f1", 1): pill(ctx, "WORLD RECORD (FIRST TRAILER, 2023)", CX, H * 0.265, CYAN, 40, prog(t, ST("f1", 1), ST("f1", 1) + 0.3))

def sc_f2(ctx, t, d):
    still(ctx, "calendar", t)
    fact_tag(ctx, 2, t)
    big(ctx, "13 YEARS", H * 0.135, 190, WHITE, PURPLE, t, 0.3)
    poster_text(ctx, "GTA 5 (2013) → GTA 6 (2026)", CX, H * 0.205, 72 * U, GOLD, W * 0.9)
    if t > ST("f2", 1): pill(ctx, "LONGEST WAIT IN THE SERIES", CX, H * 0.265, CYAN, 44, prog(t, ST("f2", 1), ST("f2", 1) + 0.3))

def sc_f3(ctx, t, d):
    still(ctx, "cases", t)
    fact_tag(ctx, 3, t)
    counter(ctx, 230_000_000, t, 0.05, 2.6, H * 0.14, 150, WHITE, CYAN, "+")
    poster_text(ctx, "GTA 5 COPIES SOLD", CX, H * 0.205, 84 * U, GOLD, W * 0.9)

def f4_ov(ctx, t, d):
    fact_tag(ctx, 4, t)
    poster_text(ctx, "VICE CITY", CX, H * 0.125, 150 * U, PINK, W * 0.88)
    poster_text(ctx, "IS BACK", CX, H * 0.19, 120 * U, WHITE, W * 0.88)
    pill(ctx, "LEONIDA = FICTIONAL FLORIDA", CX, H * 0.255, CYAN, 44, prog(t, 1.4, 1.7))
sc_f4 = clip_scene("f4", f4_ov, top_scrim=0.32)

def f5_ov(ctx, t, d):
    fact_tag(ctx, 5, t)
    big(ctx, "2022 LEAK", H * 0.13, 170, WHITE, GREEN, t, 0.2)
    poster_text(ctx, "≈ 90 CLIPS OF EARLY FOOTAGE", CX, H * 0.2, 72 * U, GOLD, W * 0.9)
    if t > ST("f5", 1): pill(ctx, "ROCKSTAR KEPT GOING", CX, H * 0.26, GREEN, 46, prog(t, ST("f5", 1), ST("f5", 1) + 0.3))
sc_f5 = clip_scene("f5", f5_ov, top_scrim=0.32)

def sc_outro(ctx, t, d):
    """Retour sur la ville de la 1re image, « NOV 19 », puis le CTA d'abonnement GTA 6."""
    paint(ctx, load_img(RW + "/key_city.png"), zoom=1.0 + 0.01 * t); scrim(ctx, 0.28)
    c0 = EN("outro", 0) + 0.05
    if t < c0 + 0.2:
        a = 1 - prog(t, c0, c0 + 0.2)
        if a > 0:
            big(ctx, "NOV 19", H * 0.13, 230, WHITE, PINK, t, 0.0)
            poster_text(ctx, "RELEASE DAY", CX, H * 0.21, 96 * U, GOLD, W * 0.88)
    else:
        rgba(ctx, (0.02, 0.0, 0.05), 0.45 * prog(t, c0, c0 + 0.4)); ctx.paint()
        cta(ctx, t - c0, d - c0, "SUBSCRIBE FOR MORE GTA 6", "THE PHENOMENON OF 2026")

SHORT_SCENES = ["hook", "f1", "f2", "f3", "f4", "f5", "outro"]
SCENES = dict(hook=sc_hook, f1=sc_f1, f2=sc_f2, f3=sc_f3, f4=sc_f4, f5=sc_f5, outro=sc_outro)

def cover(ctx):
    """Affiche : la ville néon, « GTA 6 » géant, la promesse, sans rien d'officiel ; zone sûre 14–86 %."""
    paint(ctx, load_img(RW + "/key_city.png"), fy=0.55, zoom=1.0)
    scrim(ctx, 0.40, 0.85)
    glow(ctx, CX, H * 0.235, 520 * U, PINK, 0.35)
    neon_text(ctx, "GTA 6", CX, H * 0.235, 330 * U, WHITE, 1.0, PINK, fill=0.55)
    poster_text(ctx, "5 FACTS YOU", CX, H * 0.335, 130 * U, GOLD, W * 0.90)
    poster_text(ctx, "DON'T KNOW", CX, H * 0.40, 130 * U, WHITE, W * 0.90)
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); rgba(ctx, GOLD, 1); ctx.fill()
    rrect(ctx, CX - 470 * U, H * 0.80 - 60 * U, 940 * U, 120 * U, 60 * U); ctx.set_line_width(7 * U); rgba(ctx, (0.01, 0.01, 0.02), 1); ctx.stroke()
    text(ctx, "NUMBER 5 IS WILD", CX, H * 0.80, 70 * U, (0.02, 0.03, 0.06))
