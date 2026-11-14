---
name: regarde
description: Regarder et décortiquer n'importe quelle vidéo (lien YouTube, Shorts, Instagram, Reels, TikTok, X/Twitter, ou fichier vidéo sur l'ordinateur) — téléchargement, sous-titres ou transcription locale gratuite, images horodatées en planches, puis analyse seconde par seconde (accroche, coupes, texte à l'écran, B-rolls, call to action). À utiliser dès que l'utilisatrice dit « regarde », « analyse / décortique cette vidéo », ou colle un lien vidéo à étudier.
---

# regarde — voir une vidéo et la décortiquer

Toute la communication avec l'utilisatrice se fait **en français**. Aucune API payante : tout tourne en local
(yt-dlp, ffmpeg, whisper.cpp modèle « base »).

## 1. Préparer la vidéo (script)

Le script `regarde.sh` est dans le même dossier que ce fichier (en général `~/.claude/skills/regarde/regarde.sh`).
Le lancer avec le lien ou le chemin du fichier, **entre guillemets**, avec un délai long (`timeout` 600000 ms : la
première fois, il installe les outils et compile whisper.cpp, ce qui peut prendre plusieurs minutes) :

```bash
bash ~/.claude/skills/regarde/regarde.sh "https://www.youtube.com/watch?v=XXXX"
bash ~/.claude/skills/regarde/regarde.sh "/Users/moi/Downloads/ma video.mov"
```

Sous Windows, Claude Code passe par Git Bash : la même commande fonctionne.

Ce que fait le script, toujours dans cet ordre :
1. **Outils** : vérifie `yt-dlp --version` et `ffmpeg -version` ; installe ce qui manque (Homebrew sur Mac, winget
   sur Windows, apt sur Linux) ; met yt-dlp à jour s'il a plus d'un mois (sa version est sa date).
2. **Dossier** `~/regarde/<nom-de-la-video>/` (nom tiré du titre ou du nom de fichier).
3. **Téléchargement** en mp4 avec yt-dlp → `video.mp4` (+ `info.json` : titre, chaîne, description, vues…).
   Si le site refuse (Instagram, TikTok, contenu réservé aux connectés), nouvel essai avec
   `--cookies-from-browser chrome` (connexion empruntée au navigateur ; autre navigateur :
   `REGARDE_BROWSER=firefox bash …regarde.sh "<lien>"`, ou `edge`, `safari`).
4. **Sous-titres** avec `yt-dlp --write-subs --write-auto-subs --skip-download` ; s'il n'y en a pas (ou pour un
   fichier local), **transcription locale avec whisper.cpp**, modèle `base` (installé et téléchargé la première fois
   dans `~/.local/share/whisper.cpp/`). Résultat : `transcript.txt`, une ligne par phrase : `[HH:MM:SS] texte`.
5. **Images** avec ffmpeg : une image par seconde si la vidéo dure moins de 2 min, une toutes les 2 s jusqu'à
   10 min, une toutes les 10 s au-delà, **plus une image à chaque changement de plan** (`select='gt(scene,0.3)'`).
   L'horodatage est écrit sur chaque image (`drawtext`). → `frames/00001.jpg…`, liste dans `frames_index.txt`
   (n° d'image → seconde), changements de plan dans `cuts.txt`.
6. **Planches** de 5 × 4 vignettes (filtre `tile`), 20 images par planche, dans l'ordre chronologique, de gauche à
   droite puis de haut en bas → `planches/planche_001.jpg…`.

La dernière sortie du script donne les chemins (`DOSSIER=`, `TRANSCRIPTION=`, `PLANCHES=`…) et la liste des planches.

## 2. Regarder

1. Lire `transcript.txt`, `cuts.txt`, `frames_index.txt` et, pour un lien, le titre et la description dans `info.json`
   (`python3 -c "import json;d=json.load(open('info.json'));print(d.get('title'),d.get('uploader'),d.get('view_count'),d.get('description'),sep='\n')"`).
2. Lire **toutes** les planches avec l'outil Read, dans l'ordre, sans en sauter. L'horodatage est en haut à gauche de
   chaque vignette.
3. Un détail illisible (petit texte à l'écran, objet ambigu) : ouvrir l'image seule dans `frames/`, ou extraire une
   image en pleine résolution au bon moment :
   `ffmpeg -ss 12.5 -i video.mp4 -frames:v 1 zoom_12s5.png` puis la lire.
4. `cuts.txt` vide ou incomplet = transitions en fondu ou fonds très semblables (le détecteur à 0,3 ne les voit pas) :
   repérer les coupes sur les planches (changement de décor, de cadrage, de mise en page) et, au besoin, vérifier avec
   des images extraites autour du moment.

**Honnêteté** : ne décrire que ce qui se voit sur les images ou s'entend dans la transcription. La musique, les
bruitages et le ton de la voix ne sont pas analysés (seule la parole est transcrite) : le dire plutôt que les inventer.
Une phrase de la transcription peut être approximative (transcription automatique) : la recouper avec les
sous-titres incrustés quand il y en a.

## 3. Rendre la vidéo décortiquée

En français, dans cet ordre :

1. **Fiche** : titre, chaîne/compte, plateforme, durée, format (vertical 9:16 / horizontal 16:9), langue, vues si
   connues, nombre de plans et rythme moyen (un plan toutes les N secondes).
2. **L'accroche (0–3 s)**, seconde par seconde : ce qu'on voit à la 1re image, le texte à l'écran, la 1re phrase
   prononcée, ce qui change entre 0, 1, 2 et 3 s, et pourquoi ça retient (ou pas) le spectateur.
3. **Le déroulé seconde par seconde**, en tableau, une ligne par plan (et une ligne par phrase dans un plan long) :

   | Temps | Phrase prononcée | Ce qui est montré (plan, cadrage, B-roll, animation) | Texte à l'écran | Coupe / transition |
   |---|---|---|---|---|

   Chaque phrase de la transcription doit apparaître, en face de ce qui est montré pendant qu'elle est dite.
4. **Les coupes** : liste des moments (mm:ss) et type (cut sec, fondu, zoom, changement de décor).
5. **Le texte à l'écran** : relevé complet (titres, chiffres, sous-titres incrustés, bandeaux, emojis), avec le moment.
6. **Les B-rolls** : chaque plan d'illustration (stock, gros plan, schéma, capture d'écran, animation), avec le moment.
7. **Le call to action** : quoi (abonnement, commentaire, partage, lien, vidéo suivante), quand, et sous quelle forme
   (oral, écrit, visuel) ; y compris les appels déguisés (question posée au public, « réponse demain », boucle).
8. **Structure et rythme** en 3–5 lignes : accroche → promesse → relances → révélation → fin / boucle.
9. **À retenir** (3 points maximum) : ce qui est concrètement réutilisable pour nos vidéos.

Terminer en indiquant le dossier où sont la vidéo, la transcription et les planches.

## En cas de problème

- « Sign in to confirm » / « login required » / vidéo Instagram ou TikTok refusée : se connecter au site dans le
  navigateur, puis relancer ; sous Windows, fermer Chrome avant (il verrouille ses cookies) ou utiliser
  `REGARDE_BROWSER=firefox` (ou `edge`).
- Un outil installé par winget reste introuvable : fermer et rouvrir le terminal / Claude Code (PATH mis à jour).
- Pas de transcription (vidéo sans parole, ou whisper.cpp impossible à installer) : faire l'analyse avec les images
  seules et le signaler.
- Vidéo privée ou supprimée : le dire, ne rien inventer.
