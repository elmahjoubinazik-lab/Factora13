"""Voix off : génère build/voice.wav + build/timeline.json à partir de script.json.
Usage: python3 engine/tts.py EPISODE_DIR
Voix : Kokoro « ff_siwis » (française, licence Apache 2.0, usage commercial autorisé).
"""
import sys, os, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
EP = sys.argv[1].rstrip("/"); WD = EP + "/build"; os.makedirs(WD, exist_ok=True)
M = os.environ.get("FACTORA_MODELS", os.path.expanduser("~/.cache/factora/models"))
k = Kokoro(M + "/kokoro-v1.0.onnx", M + "/voices-v1.0.bin")
script = json.load(open(EP + "/script.json", encoding="utf-8"))
SR = 24000
def sil(s): return np.zeros(int(SR * s), dtype=np.float32)
out, t, timeline = [sil(0.4)], 0.4, []
for seg in script:
    s0, sents = t, []
    for txt in seg["text"]:
        a, _ = k.create(txt, voice="ff_siwis", speed=1.0, lang="fr-fr")
        a = a.astype(np.float32)
        sents.append({"text": txt, "start": t, "end": t + len(a) / SR})
        out += [a, sil(0.35)]; t += len(a) / SR + 0.35
    out.append(sil(0.5)); t += 0.5
    timeline.append({"scene": seg["scene"], "start": s0, "end": t, "sents": sents})
sf.write(WD + "/voice.wav", np.concatenate(out), SR)
json.dump(timeline, open(WD + "/timeline.json", "w"), ensure_ascii=False, indent=1)
print("OK voix", round(t, 1), "s")
for s in timeline: print(f'  {s["scene"]:<12} {s["start"]:6.1f}s → {s["end"]:6.1f}s')
