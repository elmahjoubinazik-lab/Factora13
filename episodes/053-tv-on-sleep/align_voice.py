"""Découpe précise des fichiers « <scène>_full.mp3 » en phrases : horodatage par mot avec whisper.cpp (modèle base, local),
alignement sur le texte du script (difflib), coupe dans le silence qui précède le 1er mot de chaque élément."""
import json, os, re, subprocess, difflib
import numpy as np
EP = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(EP, "build", "rw", "voice"); SR = 24000
WB = os.path.expanduser("~/.local/share/whisper.cpp/build/bin/whisper-cli"); WM = os.path.expanduser("~/.local/share/whisper.cpp/models/ggml-base.bin")
TMP = os.path.join(EP, "build", "align"); os.makedirs(TMP, exist_ok=True)
def toks(s): return re.findall(r"[a-z0-9']+", s.lower())
def load(p):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, dtype=np.float32)
for seg in json.load(open(os.path.join(EP, "script_en.json"), encoding="utf-8")):
    sc, texts = seg["scene"], seg["text"]; src = os.path.join(D, sc + "_full.mp3")
    if len(texts) == 1:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:a", "libmp3lame", "-b:a", "192k", os.path.join(D, f"{sc}_0.mp3")], check=True); continue
    wav = os.path.join(TMP, sc + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ar", "16000", "-ac", "1", wav], check=True)
    subprocess.run([WB, "-m", WM, "-f", wav, "-l", "en", "-ml", "1", "-sow", "-oj", "-of", os.path.join(TMP, sc), "-np"], capture_output=True, check=True)
    js = json.load(open(os.path.join(TMP, sc + ".json"), encoding="utf-8"))
    wt, wtime = [], []
    for it in js["transcription"]:
        for t in toks(it["text"]): wt.append(t); wtime.append(it["offsets"]["from"] / 1000.0)
    st, el = [], []
    for k, t in enumerate(texts):
        for w in toks(t): st.append(w); el.append(k)
    sm = difflib.SequenceMatcher(None, st, wt, autojunk=False); mp = {}
    for b in sm.get_matching_blocks():
        for i in range(b.size): mp[b.a + i] = b.b + i
    # silences (≥ 0,1 s)
    a = load(src); hop = int(0.01 * SR); fr = len(a) // hop
    rms = np.sqrt(np.mean(a[:fr * hop].reshape(fr, hop) ** 2, axis=1)); voiced = rms > 0.006
    runs, i = [], 0
    while i < fr:
        if not voiced[i]:
            j = i
            while j < fr and not voiced[j]: j += 1
            if (j - i) >= 10: runs.append((i * 0.01, j * 0.01))
            i = j
        else: i += 1
    cuts = []
    for k in range(1, len(texts)):
        i0 = el.index(k); w = next((mp[i] for i in range(i0, min(i0 + 4, len(st))) if i in mp), None)
        if w is None: cuts.append(None); continue
        t = wtime[w]
        cand = [r for r in runs if r[0] < t + 0.15 and (not cuts or cuts[-1] is None or r[1] > cuts[-1] + 0.3)]
        r = min(cand, key=lambda r: abs(r[1] - t)) if cand else None
        cuts.append((r[0] + r[1]) / 2 if r and abs(r[1] - t) < 0.9 else t - 0.08)
    if None in cuts: print("!!", sc, "alignement incomplet", cuts); continue
    bounds = [0.0] + cuts + [len(a) / SR]
    for j in range(len(texts)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", f"{bounds[j]:.3f}", "-to", f"{bounds[j+1]:.3f}", "-c:a", "libmp3lame", "-b:a", "192k",
                        os.path.join(D, f"{sc}_{j}.mp3")], check=True)
    print(sc, [round(c, 2) for c in cuts], "| début des éléments :", [" ".join(st[el.index(k):el.index(k) + 3]) for k in range(1, len(texts))],
          "| whisper :", [" ".join(wt[mp.get(el.index(k), 0):mp.get(el.index(k), 0) + 3]) for k in range(1, len(texts))])
