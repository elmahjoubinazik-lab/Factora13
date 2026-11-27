exec(open("engine/photo.py", encoding="utf-8").read())   # load_img, paint, poster_text
# Épisode 053, version 2 (vidéo longue 16:9, ≈ 10 min) — « Why Some People Can't Fall Asleep Without the TV On ».
# Refaite à la demande de Nazik (2026-11-27 : « trop scientifique… il faut vulgariser, surprendre, de meilleurs exemples,
# des illustrations plus réalistes ») : on suit Maya (personnage fictif, annoncé comme tel) heure par heure, de 23 h 47 à 6 h 30,
# puis ce qu'elle change. Illustrations : Runway (nano-banana-2.1, même personnage de référence), animées ici en « Ken Burns »
# avec fondus enchaînés ; textes et repères dessinés par-dessus. Sujet inspiré d'une vidéo d'une autre chaîne (non vue, non
# reprise) : script, structure et images 100 % Factora. Voix : Matilda via Runway, découpée en phrases (align_voice.py).
import json as _json, re as _re

_TLL = _json.load(open(EP + "/build/timeline.json", encoding="utf-8"))
_TL = {sg["scene"]: sg for sg in _TLL}
_WORDS = {}
for sg in _TLL:
    L = []
    for se in sg["sents"]:
        txt = se["text"]; n = max(1, len(txt))
        for m in _re.finditer(r"\S+", txt):
            L.append((m.group().lower().strip(".,?!:;'\"…"), se["start"] + (se["end"] - se["start"]) * m.start() / n))
    _WORDS[sg["scene"]] = L
END_T = _TLL[-1]["end"] + 0.6
def S0(sc): return _TL[sc]["start"]
def S1(sc): return _TL[sc]["end"]
def SS(sc, k=0):
    s = _TL[sc]["sents"]; return s[min(k, len(s) - 1)]["start"]
def WT(sc, word, n=0):
    hits = [t for w, t in _WORDS[sc] if w == word.lower()]
    return hits[n] if n < len(hits) else SS(sc, 0)

DARK = (0.03, 0.02, 0.08)
IMG = EP + "/build/rw/img_s/"
def pk(T, a, dur=0.5): return prog(T, a, a + dur)

# ---------------------------------------------------------------- plans (image, début, mouvement, point de cadrage)
# mouvement : in / out / left / right / up / down ; (fx, fy) = point de l'image gardé au centre
PLAN = [
 ("intro", 0, "maya_awake", "in", (0.62, 0.50)), ("intro", 1, "maya_thoughts", "out", (0.55, 0.45)),
 ("intro", 2, "maya_remote", "in", (0.55, 0.45)), (("intro", "fifteen"), None, "maya_asleep_tv", "left", (0.55, 0.50)),
 ("intro", 3, "thumb_face", "in", (0.62, 0.45)), ("intro", 4, "tv_glow_room", "out", (0.50, 0.50)),
 ("poll", 0, "building", "up", (0.50, 0.55)),
 ("ch1", 0, "maya_midnight", "in", (0.60, 0.45)),
 ("screensaver", 0, "brain_screensaver", "in", (0.50, 0.48)), ("screensaver", 2, "ceiling_memories", "down", (0.60, 0.40)),
 ("screensaver", 3, "day_city", "right", (0.50, 0.50)), (("screensaver", "dark"), None, "maya_awake", "in", (0.62, 0.50)),
 ("screensaver", 4, "ceiling_memories", "in", (0.62, 0.35)),
 ("shock", 0, "lab_room", "in", (0.50, 0.50)), ("shock", 1, "lab_man", "in", (0.35, 0.55)), ("shock", 2, "button_press", "in", (0.45, 0.60)),
 ("shock", 3, "lab_man", "out", (0.40, 0.55)), ("shock", 4, "maya_midnight", "in", (0.62, 0.45)),
 ("ch2", 0, "tv_glow_room", "in", (0.50, 0.50)),
 ("tabs", 0, "tabs_worries", "in", (0.55, 0.40)), ("tabs", 2, "tabs_tv", "out", (0.55, 0.40)),
 ("rerun", 0, "sitcom_cozy", "in", (0.55, 0.45)), ("rerun", 1, "thriller_tense", "in", (0.35, 0.40)),
 (("rerun", "rerun"), None, "sitcom_cozy", "left", (0.55, 0.45)),
 ("effort", 0, "bed_frustrated", "in", (0.65, 0.50)), ("effort", 1, "couch_doze", "right", (0.40, 0.50)),
 ("effort", 2, "bed_frustrated", "out", (0.60, 0.50)), ("effort", 3, "maya_asleep_tv", "in", (0.60, 0.50)),
 ("company", 0, "alone_company", "in", (0.45, 0.40)), ("company", 2, "sitcom_cozy", "out", (0.40, 0.40)),
 ("company", 3, "partner_asleep", "in", (0.55, 0.50)),
 ("campfire", 0, "campfire_group", "in", (0.50, 0.55)), ("campfire", 1, "lone_figure", "in", (0.55, 0.60)),
 (("campfire", "silence"), None, "campfire_group", "out", (0.55, 0.55)),
 ("ch3", 0, "night_247", "in", (0.50, 0.45)),
 ("light", 0, "night_247", "left", (0.55, 0.50)), ("light", 1, "eye_closeup", "in", (0.45, 0.45)),
 ("light", 2, "flash_room", "out", (0.45, 0.45)), ("light", 3, "sleep_lab", "in", (0.70, 0.55)), ("light", 4, "night_247", "in", (0.60, 0.50)),
 ("phone", 0, "phone_face", "in", (0.62, 0.40)), ("phone", 1, "book_ereader", "right", (0.50, 0.50)), ("phone", 2, "tv_glow_room", "out", (0.50, 0.50)),
 ("weight", 0, "scale", "down", (0.50, 0.45)),
 ("sound", 0, "loud_ad", "in", (0.30, 0.35)), ("sound", 1, "loud_ad", "right", (0.65, 0.50)), ("sound", 2, "morning_alarm", "in", (0.65, 0.50)),
 ("cycles", 0, "sleep_stairs", "in", (0.50, 0.50)), ("cycles", 2, "loud_ad", "out", (0.40, 0.45)), ("cycles", 3, "infomercial", "in", (0.55, 0.45)),
 ("ch4", 0, "morning_alarm", "in", (0.60, 0.50)),
 ("morning", 0, "morning_alarm", "left", (0.65, 0.50)), ("morning", 1, "remote_reflex", "in", (0.45, 0.45)), ("morning", 2, "night_247", "out", (0.50, 0.50)),
 ("lonely", 0, "lonely_window", "in", (0.55, 0.45)), ("lonely", 1, "video_call", "in", (0.45, 0.40)),
 ("kids", 0, "kid_tablet", "in", (0.68, 0.45)), ("kids", 1, "bedtime_story", "in", (0.50, 0.45)),
 ("ch5", 0, "podcast_earbuds", "in", (0.60, 0.50)),
 ("tip_voice", 0, "podcast_earbuds", "out", (0.60, 0.50)), ("tip_voice", 2, "sleep_timer", "in", (0.45, 0.50)),
 ("tip_sound", 0, "fan", "left", (0.35, 0.50)),
 ("tip_list", 0, "todo", "in", (0.60, 0.55)),
 ("tb_a", 0, "breathing", "in", (0.62, 0.45)),
 ("tip_bed", 0, "armchair", "in", (0.55, 0.45)), ("tip_bed", 1, "doctor", "in", (0.55, 0.40)),
 ("outro", 0, "maya_peaceful", "in", (0.60, 0.50)), ("outro", 1, "building_dark", "up", (0.50, 0.55)),
]
_SH = []
for a, k, im, mv, f in PLAN:
    t = WT(a[0], a[1]) - 0.25 if isinstance(a, tuple) else (S0(a) if k == 0 else SS(a, k) - 0.3)
    _SH.append([max(0.0, t), im, mv, f])
_SH.sort(key=lambda x: x[0])
for i, s in enumerate(_SH): s.append(_SH[i + 1][0] if i + 1 < len(_SH) else END_T + 1)

def draw_shot(ctx, sh, T, a=1.0):
    t0, im, mv, (fx, fy), t1 = sh
    p = clamp((T - t0) / max(t1 - t0 + 0.8, 1.0))
    z, dx, dy = 1.04, 0.0, 0.0
    if mv == "in": z = 1.02 + 0.10 * p
    elif mv == "out": z = 1.12 - 0.10 * p
    elif mv == "left": z, dx = 1.10, 0.05 - 0.10 * p
    elif mv == "right": z, dx = 1.10, -0.05 + 0.10 * p
    elif mv == "up": z, dy = 1.10, 0.05 - 0.10 * p
    elif mv == "down": z, dy = 1.10, -0.05 + 0.10 * p
    paint(ctx, load_img(IMG + im + ".jpg"), fx + dx, fy + dy, z, a)

def background(ctx, T):
    i = max(0, max(j for j, s in enumerate(_SH) if s[0] <= T) if any(s[0] <= T for s in _SH) else 0)
    cur = _SH[i]; xf = 0.7
    if i > 0 and T - cur[0] < xf:
        draw_shot(ctx, _SH[i - 1], T); draw_shot(ctx, cur, T, ease((T - cur[0]) / xf))
    else: draw_shot(ctx, cur, T)
    # bas de l'image assombri : sous-titres lisibles
    g = cairo.LinearGradient(0, H * 0.66, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.62)
    ctx.rectangle(0, H * 0.66, W, H * 0.34); ctx.set_source(g); ctx.fill()

# ---------------------------------------------------------------- textes par-dessus
def pill(ctx, s, x, y, col, size=44, k=1.0, fg=DARK):
    if k <= 0: return
    sc_ = 0.6 + 0.4 * ease(k) + 0.08 * math.sin(math.pi * clamp(k))
    ctx.save(); ctx.translate(x, y); ctx.scale(sc_, sc_)
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 56 * U; h_ = size * 1.6 * U
    glow(ctx, 0, 0, w_ * 0.6, col, 0.25 * k)
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, h_ / 2); rgba(ctx, col, 0.96 * k); ctx.fill()
    text(ctx, s, 0, 0, size * U, fg, k)
    ctx.restore()

def big(ctx, s, x, y, size, col, k=1.0, maxw=None):
    if k <= 0: return
    ctx.save(); ctx.push_group()
    sc_ = 0.85 + 0.15 * ease(k); ctx.translate(x, y); ctx.scale(sc_, sc_); ctx.translate(-x, -y)
    poster_text(ctx, s, x, y, size * U, col, maxw or W * 0.9)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(ease(k)); ctx.restore()

def clock(ctx, s, k, x=None, y=None, size=64):
    """Heure de la nuit de Maya (réveil numérique)."""
    if k <= 0: return
    x = x if x is not None else 70 * U; y = y if y is not None else 70 * U
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 50 * U; h_ = size * 1.45 * U
    rrect(ctx, x, y, w_, h_, 14 * U); rgba(ctx, (0.02, 0.02, 0.05), 0.78 * k); ctx.fill()
    glow(ctx, x + w_ / 2, y + h_ / 2, w_ * 0.5, (1.0, 0.25, 0.25), 0.25 * k)
    text(ctx, s, x + w_ / 2, y + h_ / 2, size * U, (1.0, 0.35, 0.35), k)

def chapter(ctx, T, sc, hour, title):
    k = pk(T, S0(sc) + 0.1, 0.6) * (1 - pk(T, S1(sc) - 0.3, 0.3))
    rgba(ctx, (0.01, 0.01, 0.04), 0.55 * k); ctx.paint()
    clock(ctx, hour, k, x=CX - 150 * U, y=H * 0.30, size=80)
    big(ctx, title, CX, H * 0.56, 96, WHITE, pk(T, S0(sc) + 0.35, 0.6) * (1 - pk(T, S1(sc) - 0.3, 0.3)))

def note(ctx, s, k, y=0.20, x=None, size=40, col=WHITE):
    if k <= 0: return
    x = x if x is not None else W * 0.27
    font(ctx, size * U); w_ = ctx.text_extents(s).width + 48 * U
    rrect(ctx, x - w_ / 2, H * y - size * 0.85 * U, w_, size * 1.7 * U, 14 * U); rgba(ctx, (0.02, 0.02, 0.06), 0.70 * k); ctx.fill()
    text(ctx, s, x, H * y, size * U, col, k)

def breath_guide(ctx, T):
    """Respiration guidée : cercle qui se remplit (inspiration, 2e inspiration) puis se vide (longue expiration)."""
    a0, b0, c0, d0 = S0("tb_a"), S0("tb_b"), S0("tb_c"), S0("tb_d")
    if T < a0 + 1.5 or T > d0 + 1.5: return
    if T < b0: r = 0.45 + 0.35 * pk(T, WT("tb_a", "breathe") , 2.5); lab = "INHALE"
    elif T < c0: r = 0.80 + 0.20 * pk(T, b0 + 1.0, 1.5); lab = "+ A SECOND SIP"
    else: r = 1.0 - 0.55 * pk(T, c0 + 0.3, 4.5); lab = "SLOW EXHALE"
    k = pk(T, a0 + 1.5, 0.6) * (1 - pk(T, d0 + 1.0, 0.5))
    x, y, R = W * 0.25, H * 0.42, H * 0.20
    glow(ctx, x, y, R * r * 1.6, (0.65, 0.55, 1.0), 0.5 * k)
    circle(ctx, x, y, R * r, (0.75, 0.68, 1.0), 0.55 * k)
    ctx.new_path(); ctx.arc(x, y, R, 0, 2 * math.pi); ctx.set_line_width(4 * U); rgba(ctx, WHITE, 0.6 * k); ctx.stroke()
    text(ctx, lab, x, y + R + 50 * U, 44 * U, WHITE, k)

def overlays(ctx, T):
    L, R = W * 0.27, W * 0.73
    # intro : l'heure, puis les 3 questions
    clock(ctx, "11:47 PM", pk(T, 0.3, 0.5) * (1 - pk(T, SS("intro", 2) - 0.3, 0.4)))
    if T < SS("intro", 1) - 0.3:
        big(ctx, "WHY YOU NEED", L + 60 * U, H * 0.36, 96, WHITE, pk(T, 0.0, 0.4) * (1 - pk(T, SS("intro", 1) - 0.8, 0.5)))
        big(ctx, "THE TV ON", L + 60 * U, H * 0.50, 120, GOLD, pk(T, 0.2, 0.4) * (1 - pk(T, SS("intro", 1) - 0.8, 0.5)))
    if S0("intro") < T < S1("intro"):
        for j, (s_, w_) in enumerate((("WHY IT WORKS", "why"), ("IS IT BAD?", "bad"), ("WHAT TO DO INSTEAD", "instead"))):
            pill(ctx, s_, L, H * (0.22 + j * 0.11), (GOLD, CORAL, GREEN)[j], 40, pk(T, WT("intro", w_) - 0.2) * (1 - pk(T, S1("intro") - 0.4, 0.3)))
    # sondage
    if S0("poll") <= T < S1("poll"):
        e = 1 - pk(T, S1("poll") - 0.4, 0.3)
        big(ctx, "2 IN 3", L, H * 0.25, 130, GOLD, pk(T, WT("poll", "two") - 0.2) * e)
        note(ctx, "baby boomers", pk(T, WT("poll", "boomers") - 0.2) * e, y=0.36)
        big(ctx, "1 IN 2", R, H * 0.25, 130, CYAN, pk(T, WT("poll", "half") - 0.2) * e)
        note(ctx, "younger adults", pk(T, WT("poll", "younger") - 0.2) * e, y=0.36, x=R)
        pill(ctx, "YOU'RE NORMAL", CX, H * 0.52, GREEN, 54, pk(T, WT("poll", "normal") - 0.3) * e)
    chapter(ctx, T, "ch1", "11:48 PM", "WHY SILENCE IS SO LOUD") if S0("ch1") <= T < S1("ch1") else None
    # écran de veille
    if S0("screensaver") <= T < S1("screensaver"):
        e = 1 - pk(T, SS("screensaver", 2) - 0.4, 0.3)
        pill(ctx, "SURPRISE #1", L, H * 0.12, CORAL, 40, pk(T, S0("screensaver") + 0.3) * e, fg=WHITE)
        pill(ctx, "DEFAULT MODE NETWORK", L, H * 0.24, GOLD, 40, pk(T, WT("screensaver", "default") - 0.2) * e)
        note(ctx, "= your brain's screensaver", pk(T, WT("screensaver", "screensaver") - 0.2) * e, y=0.33)
        pill(ctx, "DAY: NOISE DROWNS IT OUT", L, H * 0.14, (0.35, 0.55, 0.95), 38, pk(T, SS("screensaver", 3)) * (1 - pk(T, WT("screensaver", "dark") - 0.4, 0.3)), fg=WHITE)
        pill(ctx, "NIGHT: FULL VOLUME", L, H * 0.14, CORAL, 40, pk(T, WT("screensaver", "volume") - 0.4) * (1 - pk(T, SS("screensaver", 4) - 0.3, 0.3)), fg=WHITE)
        pill(ctx, "COMMENT: WHAT DOES YOUR BRAIN REPLAY?", CX, H * 0.12, GOLD, 40, pk(T, SS("screensaver", 4) + 1.5) * (1 - pk(T, S1("screensaver") - 0.4, 0.3)))
    # l'expérience
    if S0("shock") <= T < S1("shock"):
        pill(ctx, "15 MINUTES ALONE · NOTHING TO DO", CX, H * 0.12, WHITE, 40, pk(T, WT("shock", "fifteen") - 0.2) * (1 - pk(T, SS("shock", 2) - 0.3, 0.3)))
        pill(ctx, "A MILD ELECTRIC SHOCK", CX, H * 0.12, GOLD, 42, pk(T, WT("shock", "shock") - 0.2) * (1 - pk(T, SS("shock", 3) - 0.3, 0.3)))
        e = 1 - pk(T, SS("shock", 4) - 0.3, 0.3)
        big(ctx, "2 IN 3 MEN", W * 0.76, H * 0.34, 100, CORAL, pk(T, WT("shock", "two") - 0.2) * e)
        note(ctx, "pressed it anyway", pk(T, WT("shock", "pressed") - 0.2) * e, y=0.44, x=W * 0.76)
        kc = pk(T, WT("shock", "hundred") - 0.6, 1.5)
        big(ctx, f"{int(190 * ease(kc))}×", W * 0.76, H * 0.60, 140, GOLD, kc * e)
        clock(ctx, "12:00 AM", pk(T, SS("shock", 4) + 0.5) * (1 - pk(T, S1("shock") - 0.3, 0.3)))
    chapter(ctx, T, "ch2", "12:00 AM", "WHY THE TV WORKS SO WELL") if S0("ch2") <= T < S1("ch2") else None
    if S0("tabs") <= T < S1("tabs"):
        big(ctx, "ONLY ~4 TABS", L, H * 0.20, 90, GOLD, pk(T, WT("tabs", "four") - 0.3) * (1 - pk(T, SS("tabs", 2) - 0.3, 0.3)))
        pill(ctx, "WORRIES LOSE THEIR SEATS", L, H * 0.14, GREEN, 40, pk(T, WT("tabs", "seats") - 1.0) * (1 - pk(T, S1("tabs") - 0.3, 0.3)))
    if S0("rerun") <= T < S1("rerun"):
        pill(ctx, "NEW SHOW = ALERT", L, H * 0.14, CORAL, 42, pk(T, WT("rerun", "alert") - 0.4) * (1 - pk(T, WT("rerun", "rerun") - 0.4, 0.3)), fg=WHITE)
        pill(ctx, "RERUN = NO CLIFFHANGER", L, H * 0.14, GREEN, 42, pk(T, WT("rerun", "cliffhanger") - 0.6) * (1 - pk(T, S1("rerun") - 0.3, 0.3)))
    if S0("effort") <= T < S1("effort"):
        pill(ctx, "THE HARDER YOU TRY, THE LESS YOU SLEEP", CX, H * 0.12, CORAL, 40, pk(T, WT("effort", "harder") - 0.4) * (1 - pk(T, SS("effort", 1) - 0.3, 0.3)), fg=WHITE)
        pill(ctx, "COUCH: 5 MIN · BED: 1 HOUR", W * 0.70, H * 0.14, GOLD, 40, pk(T, WT("effort", "couch") - 0.3) * (1 - pk(T, SS("effort", 2) - 0.3, 0.3)))
        pill(ctx, "NO PRESSURE = SLEEP SNEAKS IN", L, H * 0.14, GREEN, 40, pk(T, SS("effort", 3) + 0.5) * (1 - pk(T, S1("effort") - 0.3, 0.3)))
    if S0("company") <= T < S1("company"):
        pill(ctx, "PARASOCIAL RELATIONSHIPS", R, H * 0.14, PINK, 40, pk(T, WT("company", "parasocial") - 0.3) * (1 - pk(T, SS("company", 2) - 0.3, 0.3)), fg=WHITE)
        pill(ctx, "THE SHOW WORKED LIKE A FRIEND", R, H * 0.14, GOLD, 40, pk(T, WT("company", "friend") - 0.6) * (1 - pk(T, SS("company", 3) - 0.3, 0.3)))
        big(ctx, "IT'S COMPANY", L, H * 0.22, 90, GOLD, pk(T, WT("company", "company") - 0.3) * (1 - pk(T, S1("company") - 0.3, 0.3)))
    if S0("campfire") <= T < S1("campfire"):
        pill(ctx, "VOICES NEARBY = SAFE", L, H * 0.14, GREEN, 40, pk(T, WT("campfire", "voices") - 0.3) * (1 - pk(T, SS("campfire", 1) + 4.5, 0.3)))
        pill(ctx, "SILENCE = ALONE", R, H * 0.14, CORAL, 40, pk(T, WT("campfire", "silence") - 0.3) * (1 - pk(T, SS("campfire", 2) - 0.3, 0.3)), fg=WHITE)
        note(ctx, "only a theory", pk(T, SS("campfire", 2)) * (1 - pk(T, S1("campfire") - 0.3, 0.3)), y=0.14)
    chapter(ctx, T, "ch3", "2:47 AM", "WHAT THE TV DOES WHILE YOU SLEEP") if S0("ch3") <= T < S1("ch3") else None
    if S0("light") <= T < S1("light"):
        clock(ctx, "2:47 AM", pk(T, S0("light") + 0.2) * (1 - pk(T, SS("light", 1) - 0.3, 0.3)))
        pill(ctx, "SURPRISE #2", R, H * 0.12, CORAL, 40, pk(T, SS("light", 1)) * (1 - pk(T, SS("light", 2) - 0.3, 0.3)), fg=WHITE)
        note(ctx, "Your eyelids are not blackout curtains", pk(T, WT("light", "blackout") - 0.4) * (1 - pk(T, SS("light", 2) - 0.3, 0.3)), y=0.22, x=R)
        pill(ctx, "DARK → BRIGHT → DARK, ALL NIGHT", L, H * 0.14, GOLD, 38, pk(T, WT("light", "flashes") - 0.3) * (1 - pk(T, SS("light", 3) - 0.3, 0.3)))
        e = 1 - pk(T, SS("light", 4) - 0.3, 0.3)
        pill(ctx, "ONE NIGHT WITH THE LIGHTS ON", L, H * 0.12, WHITE, 38, pk(T, WT("light", "one") - 0.3) * e)
        pill(ctx, "HEART RATE ↑ DURING SLEEP", L, H * 0.22, CORAL, 38, pk(T, WT("light", "heart") - 0.3) * e, fg=WHITE)
        pill(ctx, "NEXT MORNING: SUGAR HANDLED WORSE", L, H * 0.32, GOLD, 36, pk(T, WT("light", "sugar") - 0.3) * e)
    if S0("phone") <= T < S1("phone"):
        pill(ctx, "PHONE IN YOUR FACE = MORE LIGHT", L, H * 0.14, CORAL, 40, pk(T, WT("phone", "foot") - 0.3) * (1 - pk(T, SS("phone", 1) + 4.0, 0.3)), fg=WHITE)
        pill(ctx, "E-READER: SLOWER TO FALL ASLEEP, GROGGIER", CX, H * 0.12, GOLD, 38, pk(T, WT("phone", "groggier") - 0.4) * (1 - pk(T, SS("phone", 2) - 0.3, 0.3)))
        big(ctx, "TV ACROSS THE ROOM > PHONE", CX, H * 0.20, 76, GREEN, pk(T, SS("phone", 2) + 0.5) * (1 - pk(T, S1("phone") - 0.3, 0.3)))
    if S0("weight") <= T < S1("weight"):
        big(ctx, "40,000+ WOMEN", L, H * 0.18, 80, WHITE, pk(T, WT("weight", "forty") - 0.3) * (1 - pk(T, S1("weight") - 0.3, 0.3)))
        big(ctx, "+11 LB", L, H * 0.34, 120, CORAL, pk(T, WT("weight", "eleven") - 0.3) * (1 - pk(T, S1("weight") - 0.3, 0.3)))
        pill(ctx, "A LINK, NOT PROOF", R, H * 0.14, GOLD, 40, pk(T, WT("weight", "prove") - 0.3) * (1 - pk(T, S1("weight") - 0.3, 0.3)))
    if S0("sound") <= T < S1("sound"):
        e = 1 - pk(T, SS("sound", 2) - 0.3, 0.3)
        for j, (s_, w_) in enumerate((("LOUD AD", "commercial"), ("LAUGH TRACK", "laugh"), ("DOOR SLAM", "door"))):
            pill(ctx, s_, W * (0.56 + j * 0.15), H * 0.12, CORAL, 34, pk(T, WT("sound", w_) - 0.2) * e, fg=WHITE)
        pill(ctx, "TINY AROUSALS YOU NEVER REMEMBER", L, H * 0.14, GOLD, 38, pk(T, WT("sound", "arousals") - 0.3) * e)
        big(ctx, "8 HOURS… STILL TIRED", L + 40 * U, H * 0.20, 76, WHITE, pk(T, SS("sound", 2) + 0.3) * (1 - pk(T, S1("sound") - 0.3, 0.3)))
    if S0("cycles") <= T < S1("cycles"):
        e = 1 - pk(T, SS("cycles", 2) - 0.3, 0.3)
        big(ctx, "4–6 CYCLES", L, H * 0.18, 100, (0.75, 0.68, 1.0), pk(T, WT("cycles", "four") - 0.3) * e)
        note(ctx, "of about 90 minutes, every night", pk(T, WT("cycles", "ninety") - 0.3) * e, y=0.29)
        pill(ctx, "BRIEF WAKE-UPS ARE NORMAL", L, H * 0.39, GREEN, 38, pk(T, WT("cycles", "between") - 0.3) * e)
        clock(ctx, "3:12 AM", pk(T, SS("cycles", 3)) * (1 - pk(T, S1("cycles") - 0.3, 0.3)))
        pill(ctx, "+30 MIN AWAKE", R, H * 0.14, CORAL, 40, pk(T, WT("cycles", "half") - 0.3) * (1 - pk(T, S1("cycles") - 0.3, 0.3)), fg=WHITE)
    chapter(ctx, T, "ch4", "6:30 AM", "SO, IS IT ACTUALLY BAD?") if S0("ch4") <= T < S1("ch4") else None
    if S0("morning") <= T < S1("morning"):
        pill(ctx, "HABIT LOOP: BED = TV", L, H * 0.14, GOLD, 40, pk(T, SS("morning", 1) + 0.5) * (1 - pk(T, SS("morning", 2) - 0.3, 0.3)))
        e = 1 - pk(T, S1("morning") - 0.3, 0.3)
        pill(ctx, "FALLING ASLEEP TO IT: OK", L, H * 0.14, GREEN, 40, pk(T, WT("morning", "falling") - 0.2) * e)
        pill(ctx, "ON ALL NIGHT: THE PROBLEM", L, H * 0.25, CORAL, 40, pk(T, WT("morning", "night") - 0.4) * e, fg=WHITE)
    if S0("lonely") <= T < S1("lonely"):
        pill(ctx, "LONELY → MORE BROKEN SLEEP", L, H * 0.14, PURPLE, 40, pk(T, WT("lonely", "broken") - 0.3) * (1 - pk(T, SS("lonely", 1) - 0.3, 0.3)), fg=WHITE)
    if S0("kids") <= T < S1("kids"):
        pill(ctx, "KIDS: NO SCREENS IN THE BEDROOM", R, H * 0.12, GREEN, 38, pk(T, WT("kids", "pediatricians") - 0.2) * (1 - pk(T, S1("kids") - 0.3, 0.3)))
        pill(ctx, "SCREENS OFF ~1 HOUR BEFORE BED", R, H * 0.22, GOLD, 38, pk(T, WT("kids", "hour") - 0.4) * (1 - pk(T, SS("kids", 1) - 0.3, 0.3)))
    chapter(ctx, T, "ch5", "THE NEXT NIGHT", "WHAT MAYA TRIED INSTEAD") if S0("ch5") <= T < S1("ch5") else None
    tips = (("tip_voice", 1, "1 · KEEP THE VOICE, LOSE THE LIGHT"), ("tip_voice", 2, "2 · SLEEP TIMER: 30 MINUTES"),
            ("tip_sound", 0, "3 · A STEADY SOUND (FAN, RAIN)"), ("tip_list", 0, "4 · 5-MINUTE TO-DO LIST"), ("tb_a", 0, "5 · CYCLIC SIGHING"),
            ("tip_bed", 0, "6 · AWAKE 20 MIN? GET UP"))
    for j, (sc, kk, s_) in enumerate(tips):
        t0 = SS(sc, kk) - 0.2; t1 = (SS(*tips[j + 1][:2]) - 0.4) if j + 1 < len(tips) else SS("tip_bed", 1) - 0.3
        if j == 4: t1 = S1("tb_d") - 0.3
        pill(ctx, s_, CX, H * 0.10, GREEN, 46, pk(T, t0) * (1 - pk(T, t1, 0.3)))
    if S0("tip_voice") <= T < SS("tip_voice", 1):
        note(ctx, "Not medical advice: what research has tested", pk(T, WT("tip_voice", "medical") - 0.3), y=0.12, x=CX)
    if S0("tip_list") <= T < S1("tip_list"):
        big(ctx, "≈ 9 MIN FASTER", L, H * 0.26, 100, GOLD, pk(T, WT("tip_list", "nine") - 0.3) * (1 - pk(T, S1("tip_list") - 0.3, 0.3)))
    breath_guide(ctx, T)
    if S0("tb_d") <= T < S1("tb_d"):
        pill(ctx, "5 MIN A DAY → BETTER MOOD", L, H * 0.25, GOLD, 40, pk(T, WT("tb_d", "five") - 0.3) * (1 - pk(T, S1("tb_d") - 0.3, 0.3)))
    if SS("tip_bed", 1) - 0.3 <= T < S1("tip_bed"):
        pill(ctx, "SHORTEN THE TIMER EACH WEEK", L, H * 0.12, GOLD, 38, pk(T, SS("tip_bed", 1)) * (1 - pk(T, S1("tip_bed") - 0.3, 0.3)))
        pill(ctx, "AWAKE MOST NIGHTS FOR WEEKS? SEE A DOCTOR", L + 60 * U, H * 0.22, GREEN, 36, pk(T, WT("tip_bed", "doctor") - 0.5) * (1 - pk(T, S1("tip_bed") - 0.3, 0.3)))
    # fin
    if S0("outro") <= T:
        pill(ctx, "3 WEEKS LATER", L, H * 0.12, GOLD, 42, pk(T, S0("outro") + 0.3) * (1 - pk(T, SS("outro", 1) - 0.3, 0.3)))
        big(ctx, "DO YOU SLEEP WITH THE TV ON?", CX, H * 0.26, 80, WHITE, pk(T, SS("outro", 2)) * (1 - pk(T, SS("outro", 3) - 0.3, 0.3)))
        pill(ctx, "WHAT DO YOU WATCH? TELL ME BELOW", CX, H * 0.40, GOLD, 44, pk(T, WT("outro", "watch") - 0.3) * (1 - pk(T, SS("outro", 3) - 0.3, 0.3)))
        if T >= SS("outro", 3) - 0.3:
            rgba(ctx, (0.02, 0.02, 0.06), 0.45 * pk(T, SS("outro", 3) - 0.3, 0.5)); ctx.paint()
            cta(ctx, T - (SS("outro", 3) - 0.3), END_T - SS("outro", 3) + 0.3, "WHAT DO YOU WATCH?", "TELL ME IN THE COMMENTS")
    if 2.0 < T < 9.0:   # personnage fictif, illustrations d'IA
        note(ctx, "Maya is a fictional character · AI-assisted illustrations", pk(T, 2.0) * (1 - pk(T, 8.5, 0.4)), y=0.94, x=CX, size=24, col=(0.85, 0.88, 1.0))

def master(ctx, T):
    background(ctx, T)
    overlays(ctx, T)

T_COVER = 0.6
def _abs_t(scene, t):
    if TNOW < 2.0 / FPS: return T_COVER
    return (0.0 if scene == _TLL[0]["scene"] else _TL[scene]["start"]) + t
def _scene(name):
    def f(ctx, t, d): master(ctx, _abs_t(name, t))
    return f
SCENES = {sg["scene"]: _scene(sg["scene"]) for sg in _TLL}
SHORT_SCENES = ["intro"]

def thumbnail(c):
    """Miniature 1280×720 : Maya éveillée, le visage éclairé par la télé (à droite) + « WHY YOU NEED THE TV ON » (à gauche)."""
    paint(c, load_img(IMG + "thumb_face.jpg"), 0.56, 0.48, 1.02)
    g = cairo.LinearGradient(0, 0, W * 0.62, 0); g.add_color_stop_rgba(0, 0.01, 0.01, 0.05, 0.92); g.add_color_stop_rgba(1, 0.01, 0.01, 0.05, 0.0)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    def tx(s_, x, y, sz, col):
        c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(sz)
        c.move_to(x + 6, y + 7); c.set_source_rgba(0, 0, 0, 0.85); c.show_text(s_)
        c.move_to(x, y); c.set_source_rgb(*col); c.show_text(s_)
    tx("WHY YOU", 50, 190, 118, (1, 1, 1))
    tx("NEED THE", 50, 323, 118, (1, 1, 1))
    tx("TV ON", 50, 478, 158, GOLD)
    c.select_font_face("Inter", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(44)
    w_ = c.text_extents("THE PSYCHOLOGY").width
    c.set_source_rgb(0.85, 0.12, 0.12); c.rectangle(50, 556, w_ + 50, 76); c.fill(); tx("THE PSYCHOLOGY", 75, 610, 44, (1, 1, 1))
