#!/usr/bin/env bash
# Héberge les fichiers d'un épisode sur la branche durable « backlog » (ajout, jamais d'écrasement)
# et affiche leurs 3 URL publiques, figées sur le commit. Usage: bash engine/host.sh episodes/NNN-x NNN
set -e
EP="$(cd "$1" && pwd)"; N="$2"
REPO=$(python3 -c "import json;print(json.load(open('config.json'))['video_host_repo'])")
R="https://github.com/$REPO"
TMP=$(mktemp -d); cd "$TMP"; git init -q -b backlog
if git fetch -q --depth 1 "$R" backlog 2>/dev/null; then git checkout -q -B backlog FETCH_HEAD; fi
mkdir -p "ep$N"; cp "$EP/build/video_long.mp4" "$EP/build/video_short.mp4" "$EP/build/miniature.png" "ep$N/"
git add -A && git -c user.name="Factora" -c user.email="noreply@anthropic.com" commit -qm "Fichiers épisode $N"
git push -q "$R" HEAD:backlog 2>&1 | grep -v "^remote:" >&2 || true
SHA=$(git rev-parse HEAD)
for f in video_long.mp4 video_short.mp4 miniature.png; do echo "https://raw.githubusercontent.com/$REPO/$SHA/ep$N/$f"; done
