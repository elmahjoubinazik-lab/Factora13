# Factora — production et publication automatiques

Chaîne YouTube **Factora (@factoraofficiel, id UCzFd6_4jKV184oZtqr06ueA)** : vidéos éducatives sans visage, en français, sur des thèmes variés
(« Et si… ? », « Comment ça marche ? », « Pourquoi… ? »). Une vidéo longue (2–4 min, 16:9) + un Short (≤ 60 s, 9:16) par épisode.
Propriétaire : Nazik EL MAHJOUBI. Toute la communication avec elle se fait **en français**.

Paramètres : `config.json` (chaîne cible, dépôt d'hébergement des fichiers, rythme). Le dépôt est **public** : n'y écrire aucune donnée personnelle ni identifiant.

## Procédure quotidienne (session planifiée chaque jour à 19h23, heure suisse, sans intervention humaine)

### 0. Préparation
```bash
bash engine/setup.sh            # dépendances + voix Kokoro (≈1 min)
```
Toutes les actions YouTube Zapier se font avec `connection_id` donné dans le message de la tâche planifiée (non stocké ici : dépôt public).
Charger les outils Zapier (ToolSearch « select:mcp__Zapier__inspect_zapier_actions,mcp__Zapier__execute_zapier_read_action,mcp__Zapier__execute_zapier_write_action »).

**Garde-fou chaîne — obligatoire avant toute écriture YouTube :** appeler l'action YouTube « Make API GET Request »
sur `https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true`. Si l'`id` renvoyé n'est pas
`config.json → youtube_channel_id`, **NE RIEN PUBLIER** : envoyer l'e-mail d'alerte (étape 7) et s'arrêter.

### 1. Passer en public l'épisode de la veille
Pour chaque entrée de `published.json` avec `"status": "unlisted"` : lire son statut réel (GET `videos?part=status&id=…`).
- s'il est **encore « unlisted »** → PUT `videos?part=status` avec `{"id": …, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": false}}` ; noter `"status": "public"` ;
- s'il est « private » ou supprimé → Nazik l'a retiré : noter `"status": "retire"`, ne rien toucher.
Faire de même pour le Short associé.

### 2. Choisir le sujet
Premier sujet non coché de `topics.md`. **S'il reste moins de 10 sujets non cochés**, en ajouter 20 nouveaux à la fin (mêmes règles : intemporels, vérifiables, variés — science, corps humain, histoire, économie, nature, technologie ; jamais un sujet déjà traité). Créer `episodes/NNN-mot-cle/` (NNN = numéro suivant sur 3 chiffres).

### 3. Écrire l'épisode
- `script.json` : liste de segments `{"scene": "id", "text": ["phrase", …]}`. Modèle : `episodes/001-lune/script.json`.
  - 300–450 mots, 9–12 segments ; accroche forte en 2 phrases ; promesse tenue dans les 10 premières secondes ;
  - nombres écrits en toutes lettres (la voix les lit mieux) ; phrases courtes ;
  - **uniquement des faits établis** (NASA, ESA, CNRS, INSERM, OMS, Banque de France, encyclopédies…). Pas de chiffre douteux ;
    en cas de doute, formuler prudemment (« selon plusieurs études ») ou retirer. Lister les sources dans `meta.json` ;
  - fin : question au public + « Abonnez-vous à Factora, pour un nouveau fait fascinant chaque jour. »
- `scenes.py` : une fonction de dessin par scène `sc_xxx(ctx, t, d)` (t = temps local, d = durée), le dict `SCENES`,
  la liste `SHORT_SCENES` (segments gardés pour le Short, **≤ 60 s au total**, commencer par l'accroche, finir par l'outro),
  et `thumbnail(c)` (1280×720, utiliser `thumb_text(c, ligne1, ligne2, bandeau)`).
  Modèle complet : `episodes/001-lune/scenes.py`. Style maison : fond bleu nuit, accents or, aplats vectoriels, pas d'images externes.
  Les dessins doivent être **originaux et propres au sujet** (exigence YouTube « contenu authentique »).
  Éviter le bas de l'écran (sous-titres : ~0,80–0,92 H en 16:9, ~0,70–0,78 H en 9:16).
- `meta.json` : `title` (≤ 70 car., curiosité + mot-clé), `short_title` (finir par `#shorts`), `description` (avec `{CHAPITRES}`),
  `chapters` (id de scène → libellé ; chaque chapitre ≥ 10 s, le premier à 00:00), `tags`. Modèle : `episodes/001-lune/meta.json`.

### 4. Générer et contrôler
```bash
python3 engine/tts.py episodes/NNN-x
python3 engine/render.py long  episodes/NNN-x 5,20,40,60,80,100   # captures de contrôle (build/still_long_*.png)
python3 engine/render.py short episodes/NNN-x 5,20,40              # idem en vertical
```
**Regarder chaque capture** (outil Read) : textes qui se chevauchent, éléments hors cadre, sous-titres masqués, scène vide.
Corriger `scenes.py` et recommencer jusqu'à ce que ce soit propre. Puis :
```bash
python3 engine/render.py long episodes/NNN-x
python3 engine/render.py short episodes/NNN-x
python3 engine/render.py thumb episodes/NNN-x
```
Contrôles finaux : `ffprobe` (durée Short ≤ 60 s), volume (`volumedetect` : moyenne entre −24 et −16 dB), miniature lisible.
Construire la description : `python3 engine/description.py episodes/NNN-x` (→ `build/description.txt`, chapitres calculés).

### 5. Héberger les fichiers (lien public pour Zapier)
```bash
bash engine/host.sh episodes/NNN-x NNN   # pousse sur la branche « media » et affiche les 3 URL publiques
```
(Les « releases » GitHub sont interdites depuis les sessions : ne pas les utiliser.)

### 6. Publier via Zapier (action YouTube « Upload Video »)
Vidéo longue : `title`, `description` (= build/description.txt), `tags`, `video` = URL, `privacy_status` = `config.privacy_first`,
`made_for_kids` = false, `category_id` = "27" (Éducation), `default_language` = fr, `default_audio_language` = fr, `notify_subscribers` = true.
**Ne pas passer `thumbnail` dans l'upload** (s'il échoue, la vidéo est quand même créée → risque de doublon).
Après chaque upload, vérifier avec GET `search?part=snippet&forMine=true&type=video` que la vidéo existe une seule fois.
Puis action « Update Video Thumbnail » (`video_id`, `thumbnail` = URL miniature). Si refus « permissions… thumbnails »
(normalement résolu : téléphone vérifié le 2026-11-04) : continuer sans, noter `"thumbnail_set": false`, le signaler dans l'e-mail.
Lors de l'étape 1, réessayer la miniature des épisodes avec `"thumbnail_set": false` (fichier : régénérer avec `render.py thumb` puis `host.sh`, ou ignorer si impossible).
Short : `short_title`, description courte avec le lien `https://youtu.be/<long_id>` + hashtags, sans miniature, `notify_subscribers` = false.
Ajouter l'épisode dans `published.json` (`episode`, `topic`, `dir`, `date`, `long_id`, `short_id`, `status`, `thumbnail_set`).
Cocher le sujet dans `topics.md` (date + numéro). `git add -A && git commit && git push origin main`.

### 7. Prévenir Nazik
E-mail via Zapier Gmail à l'adresse donnée dans le message de la tâche planifiée, objet « Factora — épisode NNN en ligne (non répertorié) » :
titre, liens des 2 vidéos, rappel : « Elle passera en public automatiquement à la prochaine exécution.
Pour l'empêcher : mettez-la en Privé dans YouTube Studio. » En cas d'échec à une étape : e-mail « Factora — échec épisode NNN » avec l'erreur.

## Règles
- Jamais de contenu « conçu pour les enfants ». Jamais de copie d'une œuvre existante. Jamais de visage ou de voix d'une personne réelle.
- Une seule publication par exécution. Ne jamais republier un sujet déjà coché.
- Ne jamais écrire sur YouTube si le garde-fou chaîne échoue.
- Ne pas committer `build/` (vidéos lourdes) : elles vivent dans les releases du dépôt d'hébergement.
