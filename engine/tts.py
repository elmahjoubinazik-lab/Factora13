"""Voix off : génère build/voice.wav + build/timeline.json à partir de script_<langue>.json.
Usage: python3 engine/tts.py EPISODE_DIR
Deux moteurs (config.json → voix, surchargé par meta_<langue>.json → voix) :
- "provider": "kokoro" (défaut) : Kokoro local (licence Apache 2.0, usage commercial autorisé) — mélange de styles, vitesse, traitement doux ;
- "provider": "elevenlabs" (décision de Nazik, 2026-11-15 : voix plus expressive, abonnement Starter) : API ElevenLabs
  « with-timestamps » (la clé est injectée par le proxy de l'environnement : jamais de clé dans le dépôt). Une requête par scène
  (meilleure intonation), horodatage caractère par caractère → débuts et fins de phrases exacts pour les sous-titres et ST().
  Réglages : "voice_id", "model" (défaut eleven_v4), "el_speed" (0,7–1,2), "voice_settings" (facultatif). Cache dans
  build/el_cache/ : relancer tts.py ne recoûte pas de crédits tant que le texte et les réglages ne changent pas.
"""
import sys, os, re, json, hashlib, base64, subprocess, urllib.request, numpy as np, soundfile as sf
EP = sys.argv[1].rstrip("/"); WD = EP + "/build"; os.makedirs(WD, exist_ok=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = json.load(open(ROOT + "/config.json", encoding="utf-8"))
V = CFG.get("voix", {})
LANG = CFG.get("langue", "fr")
_MP = EP + f"/meta_{LANG}.json"
if os.path.exists(_MP):   # réglage de voix propre à un épisode (ex. « Who's Lying? » : voix grave, plus lente)
    _vo = json.load(open(_MP, encoding="utf-8")).get("voix")
    if _vo: V = {**V, **_vo}
PROVIDER = V.get("provider", "kokoro")
WARM = "equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=3500:t=q:w=1.5:g=-2,equalizer=f=7500:t=q:w=1:g=-4,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=120,aecho=0.8:0.85:40|70:0.12|0.07,loudnorm=I=-16:TP=-1.5"
CLEAN = "highpass=f=70,acompressor=threshold=-20dB:ratio=2:attack=8:release=120,loudnorm=I=-16:TP=-1.5"
SCRIPT = EP + f"/script_{LANG}.json" if os.path.exists(EP + f"/script_{LANG}.json") else EP + "/script.json"
script = json.load(open(SCRIPT, encoding="utf-8"))
SR = 24000
def sil(s): return np.zeros(int(SR * s), dtype=np.float32)

# ---------------------------------------------------------------- ElevenLabs
def el_segment(text, speed):
    """Une scène → (audio float32 à SR, liste (début, fin) de chaque caractère). Cache disque par empreinte."""
    body = {"text": text, "model_id": V.get("model", "eleven_v4")}
    vs = dict(V.get("voice_settings", {}))
    if speed != 1.0: vs["speed"] = round(max(0.7, min(1.2, speed)), 3)
    if vs: body["voice_settings"] = vs
    key = hashlib.sha1(json.dumps([V["voice_id"], body], sort_keys=True).encode()).hexdigest()[:16]
    cd = WD + "/el_cache"; os.makedirs(cd, exist_ok=True); cj = f"{cd}/{key}.json"
    if not os.path.exists(cj):
        req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{V['voice_id']}/with-timestamps?output_format=mp3_44100_128",
                                     data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json", "xi-api-key": os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")})
        try:
            d = json.loads(urllib.request.urlopen(req, timeout=240).read())
        except urllib.error.HTTPError as e:
            sys.exit(f"ElevenLabs {e.code} : {e.read()[:300]!r}")
        open(f"{cd}/{key}.mp3", "wb").write(base64.b64decode(d["audio_base64"]))
        json.dump(d["alignment"], open(cj, "w"))
    al = json.load(open(cj))
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{cd}/{key}.mp3", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.float32).copy()
    times = list(zip(al["character_start_times_seconds"], al["character_end_times_seconds"]))
    return squeeze(a, times, float(V.get("max_pause", 0.28)))

def squeeze(a, times, gap):
    """Raccourcit les silences internes trop longs (> gap s) et le silence de début/fin (règle « aucun silence inutile »
    du master prompt, 2026-11-15) ; les horodatages des caractères sont recalés sur l'audio raccourci."""
    hop = int(SR * 0.01); n = len(a) // hop
    rms = np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, axis=1)) if n else np.zeros(0)
    quiet = rms < 10 ** (-40 / 20)
    cuts, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            r0, r1 = i * hop / SR, j * hop / SR
            if i == 0: cuts.append((0.0, max(0.0, r1 - 0.06)))                    # début : 60 ms max
            elif j >= n: cuts.append((r0 + 0.10, len(a) / SR))                    # fin : 100 ms max
            elif r1 - r0 > gap: cuts.append((r0 + gap / 2, r1 - gap / 2))          # milieu : gap max
            i = j
        else: i += 1
    cuts = [(c0, c1) for c0, c1 in cuts if c1 - c0 > 0.01]
    if not cuts: return a, times
    keep, prev = [], 0
    for c0, c1 in cuts:
        keep.append(a[prev:int(c0 * SR)]); prev = int(c1 * SR)
    keep.append(a[prev:])
    def remap(x):
        sh = 0.0
        for c0, c1 in cuts:
            if x >= c1: sh += c1 - c0
            elif x > c0: sh += x - c0
        return max(0.0, x - sh)
    return np.concatenate(keep), [(remap(s), remap(e)) for s, e in times]

out, t, timeline = [sil(0.1)], 0.1, []   # voix dès 0,1 s (avant : 0,4 s de silence au début = balayages)
if PROVIDER == "elevenlabs":
    for seg in script:
        s0, sents = t, []
        text = " ".join(seg["text"])
        a, times = el_segment(text, float(V.get("el_speed", 1.0)) * float(seg.get("speed", 1.0)))
        pos = 0
        for txt in seg["text"]:   # repères de phrase à partir de l'horodatage des caractères
            i0 = text.index(txt, pos); i1 = i0 + len(txt) - 1; pos = i1 + 1
            st = times[min(i0, len(times) - 1)][0]; en = times[min(i1, len(times) - 1)][1]
            # horodatage de chaque mot (sous-titres synchronisés mot pour mot, ép. 043) : [mot, début, fin]
            words = [[m.group(), t + times[min(i0 + m.start(), len(times) - 1)][0], t + times[min(i0 + m.end() - 1, len(times) - 1)][1]]
                     for m in re.finditer(r"\S+", txt)]
            sents.append({"text": txt, "start": t + st, "end": t + en, "words": words})
        out.append(a); t += len(a) / SR
        extra = float(seg.get("pause", 0))   # silence volontaire (chronomètre des énigmes)
        out.append(sil(0.25 + extra)); t += 0.25 + extra
        timeline.append({"scene": seg["scene"], "start": s0, "end": t, "sents": sents})
    POST = CLEAN
else:
    from kokoro_onnx import Kokoro
    M = os.environ.get("FACTORA_MODELS", os.path.expanduser("~/.cache/factora/models"))
    k = Kokoro(M + "/kokoro-v1.0.onnx", M + "/voices-v1.0.bin")
    VOICE = sum(w * k.get_voice_style(n) for n, w in V.get("melange", {"ff_siwis": 1.0}).items())
    SPEED = V.get("vitesse", 1.0)
    for seg in script:
        s0, sents = t, []
        for txt in seg["text"]:
            a, _ = k.create(txt, voice=VOICE, speed=SPEED * float(seg.get("speed", 1.0)), lang=V.get("code_langue", "fr-fr"))   # "speed" par segment : rythme variable (suspense)
            a = a.astype(np.float32)
            sents.append({"text": txt, "start": t, "end": t + len(a) / SR})
            out += [a, sil(0.35)]; t += len(a) / SR + 0.35
        extra = float(seg.get("pause", 0))   # silence volontaire (ex. chronomètre « pause the video » des énigmes)
        out.append(sil(0.5 + extra)); t += 0.5 + extra
        timeline.append({"scene": seg["scene"], "start": s0, "end": t, "sents": sents})
    POST = WARM if V.get("traitement_doux") else None
sf.write(WD + "/voice.wav", np.concatenate(out), SR)
if POST:   # même durée : les repères de timeline restent valables
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WD + "/voice.wav", "-af", POST, "-ar", str(SR), WD + "/voice_w.wav"], check=True)
    w, _ = sf.read(WD + "/voice_w.wav", dtype="float32"); n = len(np.concatenate(out))
    w = np.pad(w, (0, max(0, n - len(w))))[:n]; sf.write(WD + "/voice.wav", w, SR)
json.dump(timeline, open(WD + "/timeline.json", "w"), ensure_ascii=False, indent=1)
print("OK voix", PROVIDER, round(t, 1), "s")
for s in timeline: print(f'  {s["scene"]:<12} {s["start"]:6.1f}s → {s["end"]:6.1f}s')
