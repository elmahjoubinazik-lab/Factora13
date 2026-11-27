"""Découpe chaque fichier de voix « <scène>_full.mp3 » (une génération par segment) en fichiers par phrase
« <scène>_<j>.mp3 », aux silences les plus proches des frontières attendues (proportion de caractères) :
le moteur (fournisseur « files ») a alors l'heure exacte de chaque phrase pour les sous-titres et les animations."""
import json, os, subprocess, sys
import numpy as np
EP = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(EP, "build", "rw", "voice"); SR = 24000
def load(p):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32)
for seg in json.load(open(os.path.join(EP, "script_en.json"), encoding="utf-8")):
    sc, texts = seg["scene"], seg["text"]; src = os.path.join(D, sc + "_full.mp3")
    a = load(src); n = len(texts)
    if n == 1:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(D, f"{sc}_0.mp3")], check=True)
        print(sc, "1 phrase"); continue
    hop = int(0.01 * SR); fr = len(a) // hop
    rms = np.sqrt(np.mean(a[:fr * hop].reshape(fr, hop) ** 2, axis=1))
    voiced = rms > max(0.006, 0.12 * np.median(rms[rms > 0.01]) if (rms > 0.01).any() else 0.006)
    idx = np.where(voiced)[0]; t0, t1 = idx[0] * 0.01, idx[-1] * 0.01
    runs, i = [], 0   # silences ≥ 0,12 s : (centre, longueur)
    while i < fr:
        if not voiced[i]:
            j = i
            while j < fr and not voiced[j]: j += 1
            if (j - i) * 0.01 >= 0.12 and i * 0.01 > t0 and j * 0.01 < t1: runs.append(((i + j) / 2 * 0.01, (j - i) * 0.01))
            i = j
        else: i += 1
    L = [len(t) for t in texts]; cum = np.cumsum(L)[:-1] / sum(L)
    # frontière attendue en temps de PAROLE (silences exclus) : les pauses dramatiques (« … ») ne faussent plus l'estimation
    cv = np.cumsum(voiced) / voiced.sum()
    def expected(e): return float(np.searchsorted(cv, e)) * 0.01
    cuts, last = [], t0
    for e in cum:
        exp = expected(e)
        cand = [r for r in runs if r[0] > last + 0.5]
        best = min(cand, key=lambda r: abs(r[0] - exp) - 0.5 * min(r[1], 0.7))
        cuts.append(best[0]); last = best[0]
    bounds = [0.0] + cuts + [len(a) / SR]
    for j in range(n):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{bounds[j]:.3f}", "-to", f"{bounds[j+1]:.3f}", "-c:a", "libmp3lame", "-b:a", "192k",
                        os.path.join(D, f"{sc}_{j}.mp3")], check=True)
    print(sc, "coupes", [round(c, 2) for c in cuts], "attendues", [round(expected(e), 2) for e in cum])
