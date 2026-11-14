#!/usr/bin/env bash
# regarde.sh — prépare une vidéo pour que Claude puisse la « regarder ».
# Usage : bash regarde.sh "<lien YouTube/Instagram/TikTok/X ou chemin d'un fichier vidéo>" [dossier racine, défaut ~/regarde]
# Résultat dans <racine>/<nom-de-la-video>/ : video.mp4, info.json (liens), transcript.txt (+ .srt/.vtt),
# frames/NNNNN.jpg (images horodatées), frames_index.txt, cuts.txt (changements de plan), planches/planche_NNN.jpg (5x4).
# Aucune API payante : sous-titres via yt-dlp, sinon transcription locale whisper.cpp (modèle base).
set -o pipefail      # (pas de -u : le bash 3.2 du Mac plante sur les tableaux vides)
SRC="${1:?usage: bash regarde.sh <lien ou fichier> [racine]}"
ROOT="${2:-$HOME/regarde}"
BROWSER="${REGARDE_BROWSER:-chrome}"   # navigateur dont on emprunte la connexion si le site l'exige (chrome, firefox, edge, safari)
log() { echo "[regarde] $*" >&2; }
die() { echo "[regarde] ERREUR : $*" >&2; exit 1; }

case "$(uname -s)" in Darwin) OS=mac ;; Linux) OS=linux ;; MINGW*|MSYS*|CYGWIN*) OS=windows ;; *) OS=other ;; esac
SUDO=""; if [ "$OS" = linux ] && [ "$(id -u)" != 0 ] && command -v sudo >/dev/null; then SUDO=sudo; fi
LOCALBIN="$HOME/.local/bin"; mkdir -p "$LOCALBIN"; export PATH="$LOCALBIN:$PATH"

# ---------------------------------------------------------------- 1. outils : yt-dlp et ffmpeg
install_tool() {   # $1 = yt-dlp | ffmpeg
  log "installation de $1 ($OS)…"
  case "$OS" in
    mac) command -v brew >/dev/null || die "Homebrew absent : installez-le depuis https://brew.sh puis relancez"; brew install "$1" ;;
    windows) case "$1" in
        yt-dlp) winget install -e --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements ;;
        ffmpeg) winget install -e --id Gyan.FFmpeg --accept-source-agreements --accept-package-agreements ;; esac
      log "si $1 reste introuvable, fermez et rouvrez le terminal (PATH mis à jour par winget)" ;;
    linux) command -v apt-get >/dev/null || die "apt-get absent : installez $1 avec le gestionnaire de paquets de votre système"
      $SUDO apt-get update -qq && $SUDO apt-get install -y -qq "$1" ;;
    *) die "système non reconnu : installez $1 à la main" ;;
  esac
}
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || install_tool ffmpeg
command -v yt-dlp >/dev/null || install_tool yt-dlp
# yt-dlp sans dépôt système (ex. image sans apt) : binaire officiel, autonome et auto-mis à jour (yt-dlp -U)
if ! command -v yt-dlp >/dev/null; then
  log "yt-dlp : installation du binaire officiel dans $LOCALBIN"
  curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o "$LOCALBIN/yt-dlp" && chmod +x "$LOCALBIN/yt-dlp" || die "impossible d'installer yt-dlp"
fi
command -v ffmpeg >/dev/null || die "ffmpeg introuvable après installation"
ffmpeg -version | head -1 >&2; log "yt-dlp $(yt-dlp --version)"

# yt-dlp de plus d'un mois → mise à jour (les sites changent souvent, un vieux yt-dlp échoue)
V=$(yt-dlp --version | cut -d. -f1-3 | tr -d .)          # AAAAMMJJ
TODAY=$(date +%Y%m%d)
age_days() { local y1=${1:0:4} m1=$((10#${1:4:2})) d1=$((10#${1:6:2})) y2=${2:0:4} m2=$((10#${2:4:2})) d2=$((10#${2:6:2}))
  echo $(( (y2*365 + m2*30 + d2) - (y1*365 + m1*30 + d1) )); }
if [ "${#V}" = 8 ] && [ "$(age_days "$V" "$TODAY")" -gt 31 ]; then
  log "yt-dlp a plus d'un mois ($V) : mise à jour"
  case "$OS" in
    mac) brew upgrade yt-dlp || true ;;
    windows) winget upgrade -e --id yt-dlp.yt-dlp --accept-source-agreements --accept-package-agreements || true ;;
    *) if [ -w "$(command -v yt-dlp)" ] && yt-dlp -U >&2; then :; else
         # paquet apt souvent ancien : on le double par le binaire officiel (prioritaire dans le PATH)
         curl -fsSL https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o "$LOCALBIN/yt-dlp" && chmod +x "$LOCALBIN/yt-dlp"; fi ;;
  esac
  hash -r; log "yt-dlp $(yt-dlp --version)"
fi

# ---------------------------------------------------------------- 2. dossier de travail + téléchargement
slug() { printf '%s' "$1" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//' | cut -c1-60; }
IS_URL=0; case "$SRC" in http://*|https://*|www.*) IS_URL=1 ;; esac
YTDLP_COOKIES=()
if [ $IS_URL = 1 ]; then
  TITLE=$(yt-dlp --no-warnings --skip-download --print "%(title)s" "$SRC" 2>/dev/null | head -1)
  if [ -z "$TITLE" ]; then
    log "lecture refusée sans connexion : nouvel essai avec la connexion du navigateur (--cookies-from-browser $BROWSER)"
    YTDLP_COOKIES=(--cookies-from-browser "$BROWSER")
    TITLE=$(yt-dlp --no-warnings --skip-download "${YTDLP_COOKIES[@]}" --print "%(title)s" "$SRC" 2>/dev/null | head -1)
  fi
  NAME=$(slug "${TITLE:-$(basename "${SRC%%\?*}")}"); [ -n "$NAME" ] || NAME="video-$(date +%Y%m%d-%H%M%S)"
else
  [ -f "$SRC" ] || die "fichier introuvable : $SRC"
  b=$(basename "$SRC"); NAME=$(slug "${b%.*}"); [ -n "$NAME" ] || NAME="video-$(date +%Y%m%d-%H%M%S)"
fi
DIR="$ROOT/$NAME"; mkdir -p "$DIR/frames" "$DIR/planches"; cd "$DIR" || die "dossier $DIR"
log "dossier : $DIR"

if [ $IS_URL = 1 ]; then
  if [ ! -s video.mp4 ]; then
    FMT='bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b'
    dl() { yt-dlp --no-warnings --no-playlist -f "$FMT" --merge-output-format mp4 --write-info-json -o "video.%(ext)s" "$@" "$SRC"; }
    if ! dl "${YTDLP_COOKIES[@]}"; then
      [ ${#YTDLP_COOKIES[@]} = 0 ] && { log "téléchargement refusé : nouvel essai avec --cookies-from-browser $BROWSER"; YTDLP_COOKIES=(--cookies-from-browser "$BROWSER"); dl "${YTDLP_COOKIES[@]}"; } || true
    fi
    [ -s video.mp4 ] || { f=$(ls video.* 2>/dev/null | grep -v '\.json$' | head -1); [ -n "$f" ] && ffmpeg -y -loglevel error -i "$f" -c copy video.mp4; }
    [ -s video.mp4 ] || die "téléchargement impossible : vidéo privée ou supprimée, ou le site exige une connexion. Connectez-vous au site dans $BROWSER (et fermez-le sous Windows), ou relancez avec REGARDE_BROWSER=firefox (ou edge, safari)"
    [ -f video.info.json ] && mv -f video.info.json info.json
  fi
else
  [ -s video.mp4 ] || { case "$SRC" in *.mp4|*.MP4) cp "$SRC" video.mp4 ;; *) ffmpeg -y -loglevel error -i "$SRC" -c:v libx264 -c:a aac video.mp4 ;; esac; }
fi

# ---------------------------------------------------------------- 3. sous-titres, sinon transcription locale
vtt_to_txt() {   # VTT/SRT → lignes « [HH:MM:SS] texte », balises et doublons des sous-titres auto retirés
  awk 'BEGIN{t=""; last=""}
       /-->/ { split($1,a,"."); split(a[1],b,","); t=b[1]; if (length(t)==5) t="00:" t; next }
       /^(WEBVTT|Kind:|Language:|NOTE|[0-9]+$|$)/ { next }
       { gsub(/<[^>]*>/,""); gsub(/&amp;/,"\\&"); gsub(/&gt;/,">"); gsub(/&lt;/,"<"); gsub(/^[ \t]+|[ \t]+$/,"");
         if ($0 != "" && $0 != last) { print "[" t "] " $0; last=$0 } }' "$1"
}
rm -f transcript.txt
if [ $IS_URL = 1 ]; then
  yt-dlp --no-warnings --skip-download --write-subs --write-auto-subs --sub-langs "fr,fr-FR,en,en-US,en-GB,.*-orig" --sub-format "vtt/srt/best" \
    "${YTDLP_COOKIES[@]}" -o "subs.%(ext)s" "$SRC" >/dev/null 2>&1 || true
  SUB=$(ls subs.*.vtt subs.*.srt 2>/dev/null | grep -E 'orig' | head -1); [ -n "$SUB" ] || SUB=$(ls subs.*.vtt subs.*.srt 2>/dev/null | head -1)
  if [ -n "$SUB" ]; then vtt_to_txt "$SUB" > transcript.txt; log "sous-titres : $SUB"; fi
fi
if [ ! -s transcript.txt ]; then
  log "pas de sous-titres : transcription locale avec whisper.cpp (modèle base)"
  WDIR="$HOME/.local/share/whisper.cpp"; MODEL="$WDIR/models/ggml-base.bin"; mkdir -p "$WDIR/models"
  WBIN=$(command -v whisper-cli || command -v whisper-cpp || ls "$WDIR"/build/bin/whisper-cli "$WDIR"/build/bin/Release/whisper-cli.exe "$WDIR"/bin/whisper-cli.exe "$WDIR"/bin/Release/whisper-cli.exe 2>/dev/null | head -1)
  if [ -z "$WBIN" ]; then
    case "$OS" in
      mac) brew install whisper-cpp && WBIN=$(command -v whisper-cli || command -v whisper-cpp) ;;
      windows) curl -fsSL https://github.com/ggml-org/whisper.cpp/releases/latest/download/whisper-bin-x64.zip -o "$WDIR/w.zip" \
                 && (cd "$WDIR" && { unzip -qo w.zip -d bin 2>/dev/null || powershell -NoProfile -Command "Expand-Archive -Force w.zip bin"; }) && WBIN=$(ls "$WDIR"/bin/whisper-cli.exe "$WDIR"/bin/Release/whisper-cli.exe 2>/dev/null | head -1) ;;
      *) command -v cmake >/dev/null && command -v g++ >/dev/null || { [ -n "$(command -v apt-get)" ] && $SUDO apt-get install -y -qq cmake g++ make git; }
         [ -d "$WDIR/.git" ] || { rm -rf "$WDIR.tmp"; git clone -q --depth 1 https://github.com/ggml-org/whisper.cpp "$WDIR.tmp" && cp -r "$WDIR.tmp/." "$WDIR/"; rm -rf "$WDIR.tmp"; }
         (cd "$WDIR" && cmake -S . -B build -DCMAKE_BUILD_TYPE=Release >/dev/null && cmake --build build -j --config Release --target whisper-cli >/dev/null) \
           && WBIN="$WDIR/build/bin/whisper-cli" ;;
    esac
  fi
  if [ ! -s "$MODEL" ]; then log "téléchargement du modèle whisper « base » (≈ 140 Mo, une seule fois)"
    curl -fL --retry 3 -s https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin -o "$MODEL.part" && mv -f "$MODEL.part" "$MODEL" \
      || { rm -f "$MODEL.part"; log "téléchargement du modèle base impossible"; }; fi
  if [ -n "$WBIN" ] && [ -s "$MODEL" ]; then
    ffmpeg -y -loglevel error -i video.mp4 -vn -ar 16000 -ac 1 -c:a pcm_s16le audio.wav
    if [ -s audio.wav ]; then
      "$WBIN" -m "$MODEL" -f audio.wav -l auto -osrt -of transcript >/dev/null 2>&1 && vtt_to_txt transcript.srt > transcript.txt
    else log "la vidéo n'a pas de piste audio"; fi
    rm -f audio.wav
  else log "whisper.cpp indisponible : pas de transcription"; fi
fi
[ -s transcript.txt ] || echo "(aucune parole détectée ou transcription indisponible)" > transcript.txt

# ---------------------------------------------------------------- 4. images horodatées + planches 5x4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4 | cut -d. -f1); DUR=${DUR:-0}
WH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0:s=x video.mp4 | head -1); VW=${WH%x*}; VH=${WH#*x}
if [ "$DUR" -lt 120 ]; then INT=1; elif [ "$DUR" -le 600 ]; then INT=2; else INT=10; fi
if [ "${VH:-1}" -gt "${VW:-1}" ]; then TH=400; else TH=288; fi        # hauteur d'une vignette (vertical / horizontal)
TW=$(( TH * ${VW:-16} / ${VH:-9} )); FS=$(( TW / 8 )); [ $FS -gt $(( TH / 9 )) ] && FS=$(( TH / 9 ))   # l'horodatage tient dans la vignette
VS="-fps_mode vfr"; ffmpeg -hide_banner -h long 2>/dev/null | grep -q fps_mode || VS="-vsync vfr"   # ffmpeg récent / ancien
log "durée ${DUR}s, ${VW}x${VH} : 1 image toutes les ${INT}s + 1 à chaque changement de plan"
rm -f frames/*.jpg planches/*.jpg
SEL="select='isnan(prev_t)+gte(floor(t/$INT)-floor(prev_t/$INT),1)+gt(scene,0.3)'"
TXT="drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=$FS:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=6"
FONT=""
if ! ffmpeg -v error -f lavfi -i color=c=black:s=64x64:d=0.1 -vf "$TXT" -f null - 2>/dev/null; then   # pas de police par défaut
  for f in /System/Library/Fonts/Supplemental/Arial.ttf /Library/Fonts/Arial.ttf C:/Windows/Fonts/arial.ttf /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf; do
    [ -f "$f" ] && { FONT=":fontfile='$f'"; break; }; done
fi
TXT="drawtext=text='%{pts\:hms}'$FONT:x=6:y=6:fontsize=$FS:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=6"
ffmpeg -hide_banner -y -i video.mp4 -vf "$SEL,showinfo,scale=-2:$TH,$TXT" $VS -q:v 3 frames/%05d.jpg 2> frames_log.txt \
  || ffmpeg -hide_banner -y -i video.mp4 -vf "$SEL,showinfo,scale=-2:$TH" $VS -q:v 3 frames/%05d.jpg 2> frames_log.txt
grep -o 'n: *[0-9]* .*pts_time:[0-9.]*' frames_log.txt | awk '{for(i=1;i<=NF;i++) if ($i ~ /^pts_time:/) {split($i,a,":"); printf "%05d  %s s\n", NR, a[2]}}' > frames_index.txt
# changements de plan seuls (liste des coupes)
ffmpeg -hide_banner -i video.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 \
  | awk '{s=int($1); printf "%02d:%02d:%02d.%03d\n", s/3600, (s%3600)/60, s%60, ($1-s)*1000}' > cuts.txt
N=$(ls frames/*.jpg 2>/dev/null | wc -l)
ffmpeg -hide_banner -loglevel error -y -framerate 1 -i frames/%05d.jpg -vf "tile=5x4:padding=6:margin=6:color=0x101010" -q:v 3 planches/planche_%03d.jpg
rm -f frames_log.txt
echo "DOSSIER=$DIR"
echo "VIDEO=$DIR/video.mp4  DUREE=${DUR}s  FORMAT=${VW}x${VH}"
echo "TRANSCRIPTION=$DIR/transcript.txt"
echo "COUPES=$DIR/cuts.txt ($(wc -l < cuts.txt) changements de plan)"
echo "IMAGES=$N dans $DIR/frames (index : $DIR/frames_index.txt)"
echo "PLANCHES=$(ls planches/*.jpg | wc -l) dans $DIR/planches"
ls -1 "$DIR"/planches/*.jpg
