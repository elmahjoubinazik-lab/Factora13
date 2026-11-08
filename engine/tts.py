"""Voix off : génère build/voice.wav + build/timeline.json à partir de script.json.
Usage: python3 engine/tts.py EPISODE_DIR
Voix : Kokoro (licence Apache 2.0, usage commercial autorisé), réglée dans config.json → voix (mélange de styles, vitesse, traitement doux).
"""
import sys, os, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
EP = sys.argv[1].rstrip("/"); WD = EP + "/build"; os.makedirs(WD, exist_ok=True)
M = os.environ.get("FACTORA_MODELS", os.path.expanduser("~/.cache/factora/models"))
k = Kokoro(M + "/kokoro-v1.0.onnx", M + "/voices-v1.0.bin")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = json.load(open(ROOT + "/config.json", encoding="utf-8")).get("voix", {})
VOICE = sum(w * k.get_voice_style(n) for n, w in V.get("melange", {"ff_siwis": 1.0}).items())
SPEED = V.get("vitesse", 1.0)
WARM = "equalizer=f=180:t=q:w=1:g=2.5,equalizer=f=3500:t=q:w=1.5:g=-2,equalizer=f=7500:t=q:w=1:g=-4,acompressor=threshold=-22dB:ratio=2.5:attack=10:release=120,aecho=0.8:0.85:40|70:0.12|0.07,loudnorm=I=-16:TP=-1.5"
LANG = json.load(open(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/config.json", encoding="utf-8")).get("langue", "fr")
SCRIPT = EP + f"/script_{LANG}.json" if os.path.exists(EP + f"/script_{LANG}.json") else EP + "/script.json"
script = json.load(open(SCRIPT, encoding="utf-8"))
SR = 24000
def sil(s): return np.zeros(int(SR * s), dtype=np.float32)
out, t, timeline = [sil(0.1)], 0.1, []   # voix dès 0,1 s (avant : 0,4 s de silence au début = balayages)
for seg in script:
    s0, sents = t, []
    for txt in seg["text"]:
        a, _ = k.create(txt, voice=VOICE, speed=SPEED, lang=V.get("code_langue", "fr-fr"))
        a = a.astype(np.float32)
        sents.append({"text": txt, "start": t, "end": t + len(a) / SR})
        out += [a, sil(0.35)]; t += len(a) / SR + 0.35
    extra = float(seg.get("pause", 0))   # silence volontaire (ex. chronomètre « pause the video » des énigmes)
    out.append(sil(0.5 + extra)); t += 0.5 + extra
    timeline.append({"scene": seg["scene"], "start": s0, "end": t, "sents": sents})
sf.write(WD + "/voice.wav", np.concatenate(out), SR)
if V.get("traitement_doux"):   # même durée : les repères de timeline restent valables
    import subprocess
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", WD + "/voice.wav", "-af", WARM, "-ar", str(SR), WD + "/voice_w.wav"], check=True)
    w, _ = sf.read(WD + "/voice_w.wav", dtype="float32"); n = len(np.concatenate(out))
    w = np.pad(w, (0, max(0, n - len(w))))[:n]; sf.write(WD + "/voice.wav", w, SR)
json.dump(timeline, open(WD + "/timeline.json", "w"), ensure_ascii=False, indent=1)
print("OK voix", round(t, 1), "s")
for s in timeline: print(f'  {s["scene"]:<12} {s["start"]:6.1f}s → {s["end"]:6.1f}s')
