#!/usr/bin/env bash
# Installe les dépendances et télécharge la voix (≈350 Mo, une fois par session).
set -e
pip install -q kokoro-onnx soundfile pycairo numpy 2>&1 | grep -v WARNING || true
M="${FACTORA_MODELS:-$HOME/.cache/factora/models}"; mkdir -p "$M"
B=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s "$M/kokoro-v1.0.onnx" ] || curl -sSL -o "$M/kokoro-v1.0.onnx" $B/kokoro-v1.0.onnx
[ -s "$M/voices-v1.0.bin" ] || curl -sSL -o "$M/voices-v1.0.bin" $B/voices-v1.0.bin
which ffmpeg >/dev/null && echo "setup OK ($M)"
