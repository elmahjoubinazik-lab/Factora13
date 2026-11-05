# Factora — production et publication automatiques

Chaîne YouTube **Factora (@factoraofficiel, id UCzFd6_4jKV184oZtqr06ueA)** — ne pas publier sur @factora13 (UCYxSS4wKZUa3kmLnTYiGmuw), autre chaîne : vidéos éducatives sans visage, en français, sur des thèmes variés
(« What if…? », « How does … work? », « Why…? »). **Toutes les vidéos sont en ANGLAIS** (décision de Nazik, 2026-11-04) ; `config.json → langue` = "en". Une vidéo longue (2–4 min, 16:9) + un Short (≤ 60 s, 9:16) par épisode.
Propriétaire : Nazik EL MAHJOUBI. Toute la communication avec elle se fait **en français**.

Paramètres : `config.json` (chaîne cible, dépôt d'hébergement des fichiers, rythme). Le dépôt est **public** : n'y écrire aucune donnée personnelle ni identifiant.

## Procédure de publication (session planifiée tous les 2 jours à 19h23, heure suisse, sans intervention humaine)

### 0. Préparation
```bash
bash engine/setup.sh            # dépendances + voix Kokoro (≈1 min)
```
Toutes les actions YouTube Zapier se font avec `connection_id` donné dans le message de la tâche planifiée (non stocké ici : dépôt public).
Charger les outils Zapier (ToolSearch « select:mcp__Zapier__inspect_zapier_actions,mcp__Zapier__execute_zapier_read_action,mcp__Zapier__execute_zapier_write_action »).

**Garde-fou chaîne — obligatoire avant toute écriture YouTube :** appeler l'action YouTube « Make API GET Request »
sur `https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true`. Si l'`id` renvoyé n'est pas
`config.json → youtube_channel_id`, **NE RIEN PUBLIER** : envoyer l'e-mail d'alerte (étape 7) et s'arrêter.

### 1. Passer en public l'épisode précédent
Pour chaque entrée de `published.json` avec `"status": "unlisted"` : lire son statut réel (GET `videos?part=status&id=…`).
- s'il est **encore « unlisted »** → PUT `videos?part=status` avec `{"id": …, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": false}}` ; noter `"status": "public"` ;
- s'il est « private » ou supprimé → Nazik l'a retiré : noter `"status": "retire"`, ne rien toucher.
Faire de même pour le Short associé.
Si l'entrée a un champ `remplace_ids` et vient d'être passée en public : supprimer ces anciennes vidéos (DELETE `videos?id=…`), puis retirer le champ.

### 1 bis. Écouler la file d'attente YouTube
YouTube limite le nombre de mises en ligne par 24 h. Les épisodes de `published.json` avec `"status": "attente_youtube"`
(déjà publiés sur TikTok, fichiers hébergés dans `urls`) sont mis en ligne **avant** le nouvel épisode, dans l'ordre des numéros :
vidéo longue en **public** directement (contenu déjà validé), vérifier qu'elle existe une seule fois, miniature, puis Short en public
(description avec le lien `https://youtu.be/<long_id>`). Remplir `long_id`, `short_id`, `thumbnail_set`, `"status": "public"`.
Si YouTube répond « exceeded the number of videos they may upload » : **arrêter les envois YouTube pour cette exécution**
(ne pas réessayer), garder le reste en attente, et continuer la procédure (le nouvel épisode ira lui aussi en attente, voir étape 6).

### 2. Choisir le sujet
Premier sujet non coché de `topics.md`. **S'il reste moins de 10 sujets non cochés**, en ajouter 20 nouveaux à la fin (mêmes règles : intemporels, vérifiables, variés — science, corps humain, histoire, économie, nature, technologie ; jamais un sujet déjà traité). Créer `episodes/NNN-mot-cle/` (NNN = numéro suivant sur 3 chiffres).

### 3. Écrire l'épisode
- `script_en.json` (langue de la chaîne ; `script.json` = ancien français, ne plus l'utiliser) : liste de segments `{"scene": "id", "text": ["phrase", …]}`. Modèle : `episodes/001-lune/script_en.json`. Rédiger directement en anglais naturel (américain), pas une traduction.
  - 300–450 mots, 9–12 segments ; accroche forte en 2 phrases ; promesse tenue dans les 10 premières secondes ;
  - nombres écrits en toutes lettres (la voix les lit mieux) ; phrases courtes ;
  - textes dessinés à l'écran : écrire directement en anglais dans `scenes.py` (ou clé française + dictionnaire `TR["en"]` comme l'épisode 001) ;
  - **uniquement des faits établis** (NASA, ESA, CNRS, INSERM, OMS, Banque de France, encyclopédies…). Pas de chiffre douteux ;
    en cas de doute, formuler prudemment (« selon plusieurs études ») ou retirer. Lister les sources dans `meta.json` ;
  - fin : question au public + « And subscribe to Factora, so you never miss a fascinating fact. » (ne jamais citer de fréquence de publication : elle peut changer)
- `scenes.py` : une fonction de dessin par scène `sc_xxx(ctx, t, d)` (t = temps local, d = durée), le dict `SCENES`,
  la liste `SHORT_SCENES` (segments gardés pour le Short, **≤ 60 s au total** — vérifier avec build/timeline.json, la voix est lente, commencer par l'accroche, finir par l'outro),
  et `thumbnail(c)` (1280×720, utiliser `thumb_text(c, ligne1, ligne2, bandeau)`).
  Modèle complet : `episodes/001-lune/scenes.py`. Style maison : fond bleu nuit, accents or, aplats vectoriels, pas d'images externes.
  Les dessins doivent être **originaux et propres au sujet** (exigence YouTube « contenu authentique »).
  Éviter le bas de l'écran (sous-titres : ~0,80–0,92 H en 16:9, ~0,70–0,78 H en 9:16).
- `meta_en.json` : `title` (≤ 70 car., curiosité + mot-clé), `short_title` (finir par `#shorts`), `description` (avec `{CHAPITRES}`),
  `chapters` (id de scène → libellé ; chaque chapitre ≥ 10 s, le premier à 00:00), `tags`. Modèle : `episodes/001-lune/meta_en.json`.

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
bash engine/host.sh episodes/NNN-x NNN   # ajoute les fichiers sur la branche durable « backlog » et affiche les 3 URL publiques
```
(Les « releases » GitHub sont interdites depuis les sessions : ne pas les utiliser.)

### 6. Publier via Zapier (action YouTube « Upload Video »)
Vidéo longue : `title`, `description` (= build/description.txt), `tags`, `video` = URL, `privacy_status` = `config.privacy_first`,
`made_for_kids` = false, `category_id` = "27" (Éducation), `default_language` = en, `default_audio_language` = en, `notify_subscribers` = true.
**Ne pas passer `thumbnail` dans l'upload** (s'il échoue, la vidéo est quand même créée → risque de doublon).
Après chaque upload, vérifier avec GET `search?part=snippet&forMine=true&type=video` que la vidéo existe une seule fois.
Puis action « Update Video Thumbnail » (`video_id`, `thumbnail` = URL miniature). Si refus « permissions… thumbnails »
(normalement résolu : téléphone vérifié le 2026-11-04) : continuer sans, noter `"thumbnail_set": false`, le signaler dans l'e-mail.
Lors de l'étape 1, réessayer la miniature des épisodes avec `"thumbnail_set": false` (fichier : régénérer avec `render.py thumb` puis `host.sh`, ou ignorer si impossible).
Short : `short_title`, description courte (anglais) avec le lien `https://youtu.be/<long_id>` + hashtags, sans miniature, `notify_subscribers` = false.
Si l'upload échoue pour limite de mises en ligne : ne pas réessayer ; ajouter l'épisode avec `"status": "attente_youtube"` et `urls` (celles de host.sh), continuer avec TikTok.
Ajouter l'épisode dans `published.json` (`episode`, `topic`, `dir`, `date`, `long_id`, `short_id`, `status`, `thumbnail_set`).
Cocher le sujet dans `topics.md` (date + numéro). `git add -A && git commit && git push origin main`.

### 6 bis. Publier le Short sur TikTok (via Buffer, Zapier)
Action Zapier Buffer « Add to Queue » (selected_api BufferCLIAPI, action « update », tool_name « buffer_add_to_queue »),
avec le `connection_id`, l'`organizationId` et le `channelId` TikTok donnés dans le message de la tâche planifiée.
Paramètres : `method` = "share_now", `attachment` = "video", `video` = URL du Short (celle de host.sh), `scheduling_type` = "direct",
`text` (en anglais) = accroche (1–2 phrases) + « Full video on YouTube: @factoraofficiel » + « Synthetic voice, original illustrations. »
+ 5–6 hashtags (#science #whatif #learnontiktok #factora + sujet). ≤ 2 200 caractères.
Le Short est publié sur TikTok **dès cette exécution** (pas d'étape « non répertorié » sur TikTok).
Noter dans `published.json` : `"tiktok_buffer_id"` (champ `id` de la réponse) et `"tiktok": "envoye"`.
Si Buffer échoue : ne pas bloquer YouTube ; noter `"tiktok": "echec"` et le signaler dans l'e-mail.

### 7. Prévenir Nazik
E-mail via Zapier Gmail à l'adresse donnée dans le message de la tâche planifiée, objet « Factora — épisode NNN en ligne (non répertorié) » :
titre, liens des 2 vidéos YouTube, statut TikTok, rappel : « Elle passera en public automatiquement à la prochaine exécution.
Pour l'empêcher : mettez-la en Privé dans YouTube Studio. » En cas d'échec à une étape : e-mail « Factora — échec épisode NNN » avec l'erreur.

## Règles
- Jamais de contenu « conçu pour les enfants ». Jamais de copie d'une œuvre existante. Jamais de visage ou de voix d'une personne réelle.
- Une seule publication par exécution. Ne jamais republier un sujet déjà coché.
- Ne jamais écrire sur YouTube si le garde-fou chaîne échoue.
- Ne pas committer `build/` (vidéos lourdes) : elles vivent dans les releases du dépôt d'hébergement.
