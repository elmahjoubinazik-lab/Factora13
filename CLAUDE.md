# Factora — production et publication automatiques

Chaîne YouTube **Factora (@factoraofficiel, id UCzFd6_4jKV184oZtqr06ueA)** — ne pas publier sur @factora13 (UCYxSS4wKZUa3kmLnTYiGmuw), autre chaîne : vidéos éducatives sans visage, en français, sur des thèmes variés
(« What if…? », « How does … work? », « Why…? »). **Toutes les vidéos sont en ANGLAIS** (décision de Nazik, 2026-11-04) ; `config.json → langue` = "en". Une vidéo longue (**7–10 min** depuis le 2026-11-06 : seules les vidéos longues comptent pour les 4 000 h de visionnage de la monétisation, 16:9) + un Short (≤ 60 s, 9:16) par épisode, et **un récap hebdomadaire de ~8 min le samedi** (voir « Récap du samedi »).
Propriétaire : Nazik EL MAHJOUBI. Toute la communication avec elle se fait **en français**.

Paramètres : `config.json` (chaîne cible, dépôt d'hébergement des fichiers, rythme). Le dépôt est **public** : n'y écrire aucune donnée personnelle ni identifiant.

## Procédure de publication (exécution planifiée 5 jours par semaine — mardi, jeudi, vendredi, samedi, dimanche — à **23h47 heure suisse** (depuis le 2026-11-07, décision de Nazik : publication YouTube vers 18h30 à New York, début de soirée US ; TikTok/Instagram à 19h30 New York), sans intervention humaine ; pas de production le lundi ni le mercredi, décision de Nazik du 2026-11-06 pour économiser les tokens)

### 0. Préparation
**Exécutions sautées (décision de Nazik)** : 2026-11-08 (dimanche soir — laisser le Short de la paille faire effet). Si la date d'aujourd'hui (heure suisse) figure ici : ne rien produire ni publier, aucun appel Zapier, aucune notification ; terminer par une ligne de message.
**Garde-fou « un épisode par jour » :** si `published.json` contient déjà un épisode (hors `"format": "short_seul"`) dont la `date` est celle d'aujourd'hui (heure suisse), ne rien produire : terminer par un court message à Nazik (sans notification).
**Mode « Shorts seuls » (décision de Nazik, 2026-11-07 : plan de 30 jours, objectif +1 000 abonnés) — toutes les exécutions du dimanche 8 novembre au dimanche 6 décembre 2026 inclus (même rythme 5/7) :** ne produire **que le Short** (règle « Short seul » plus bas : `format` = "short_seul", pas de vidéo longue ni de miniature, **25–35 s**, accroche forte dès la 1re seconde) sur le premier sujet non coché de `topics.md` marqué **[SHORT]**. Ajouter `"auto": true` à l'entrée de `published.json` ; pendant ce mode, le garde-fou ci-dessus compte aussi les épisodes `"auto": true` du jour. Description du Short : lien vers la vidéo longue de la chaîne la plus proche du sujet (s'il y en a une). Publier Short + commentaire + TikTok + Instagram comme d'habitude.
- **Trois familles** (répartition de test) : quotidien surprenant ≈ 50 %, illusions / paradoxes ≈ 30 %, « ton corps si… » ≈ 20 % ; ne pas enchaîner 2 fois la même famille.
- **Apprendre des chiffres :** la lecture groupée de l'état YouTube (étape 0) inclut les `short_id` des 10 derniers Shorts ; le **dimanche**, remonter en tête des [SHORT] un sujet de la famille dont les Shorts ont la meilleure moyenne de vues (repère : 2× la médiane = succès) et noter ce classement dans le résumé.
- S'il reste moins de 6 sujets [SHORT] non cochés, en ajouter 10 (mêmes règles, faits vérifiables, familles ci-dessus).
- À partir du 22 novembre : regrouper par mini-séries reconnaissables (même formule de titre, ex. « Everyday mysteries #1, #2, #3 »).
- Le récap du samedi continue (seule vidéo longue de la période ; il réutilise les scènes des Shorts).
- Le résumé final indique le nombre de Shorts restants dans le plan (fin : dimanche 6 décembre ; ensuite, demander à Nazik la suite).
```bash
bash engine/setup.sh            # dépendances + voix Kokoro (≈1 min)
```
Toutes les actions YouTube Zapier se font avec `connection_id` donné dans le message de la tâche planifiée (non stocké ici : dépôt public).
Charger les outils : ToolSearch « select:mcp__Zapier__execute_zapier_read_action,mcp__Zapier__execute_zapier_write_action,PushNotification ».
**Économie d'appels (décision de Nazik, 2026-11-07) :** aucun appel `inspect_zapier_actions` ni `discover_zapier_actions`, sauf si un appel échoue (utiliser la « Référence des appels Zapier » ci-dessous) ; **un seul** garde-fou chaîne par exécution ; **une seule** lecture groupée de l'état YouTube (un GET `videos?part=status,statistics&id=<tous les ids utiles, séparés par des virgules>`) ; **une seule** lecture Buffer, et seulement si nécessaire ; **plus d'e-mail** : Nazik est prévenue par notification push (`PushNotification`).

**Garde-fou chaîne — obligatoire avant toute écriture YouTube :** appeler l'action YouTube « Make API GET Request »
sur `https://www.googleapis.com/youtube/v3/channels?part=snippet&mine=true`. Si l'`id` renvoyé n'est pas
`config.json → youtube_channel_id`, **NE RIEN PUBLIER** : envoyer une notification push d'alerte et s'arrêter.

### 1. Passer en public l'épisode précédent
(Depuis le 2026-11-06, les nouveaux épisodes sont publiés **directement en public** : cette étape ne concerne plus que d'éventuelles anciennes entrées « unlisted ».)
Pour chaque entrée de `published.json` avec `"status": "unlisted"` (les statuts `attente_youtube` / `attente_short` relèvent de l'étape 1 bis) : lire son statut réel (GET `videos?part=status&id=…`).
- s'il est **encore « unlisted »** → PUT `videos?part=status` avec `{"id": …, "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": false, "embeddable": true, "publicStatsViewable": true, "license": "youtube"}}` (**toujours ces 5 champs** : un PUT qui les omet désactive l'intégration et les statistiques publiques) `` ; noter `"status": "public"` ;
- s'il est « private » ou supprimé → Nazik l'a retiré : noter `"status": "retire"`, ne rien toucher.
Faire de même pour le Short associé.
Si l'entrée a un champ `remplace_ids` et vient d'être passée en public : supprimer ces anciennes vidéos (DELETE `videos?id=…`), puis retirer le champ.

### 1 bis. Écouler la file d'attente YouTube
YouTube limite le nombre de mises en ligne (≈ 10 par 24 h avant la vérification d'identité ; limite nettement relevée depuis la vérification du 2026-11-06 : 18 envois acceptés en 2 h 30). **Toujours garder 2 envois pour le nouvel épisode du jour** : au maximum 8 envois de file d'attente par exécution. Les épisodes de `published.json` avec `"status": "attente_youtube"`
(déjà publiés sur TikTok, fichiers hébergés dans `urls`) sont mis en ligne **avant** le nouvel épisode, dans l'ordre des numéros.
**Priorité aux vidéos longues** (ce sont elles qui rapportent) : d'abord toutes les vidéos longues en attente, puis les Shorts.
Un épisode dont la longue est en ligne mais pas le Short garde `"status": "attente_short"`. Pour chacun :
vidéo longue en **public** directement (contenu déjà validé), miniature, puis Short en public
(description avec le lien `https://youtu.be/<long_id>`). Remplir `long_id`, `short_id`, `thumbnail_set`, `"status": "public"`.
Si YouTube répond « exceeded the number of videos they may upload » : **arrêter les envois YouTube pour cette exécution**
(ne pas réessayer), garder le reste en attente, et continuer la procédure (le nouvel épisode ira lui aussi en attente, voir étape 6).

### 2. Choisir le sujet
Premier sujet non coché de `topics.md` (pour un épisode long, ignorer les sujets marqués [SHORT]). **S'il reste moins de 10 sujets non cochés**, en ajouter 20 nouveaux à la fin (mêmes règles : intemporels, vérifiables, variés — science, corps humain, histoire, économie, nature, technologie ; jamais un sujet déjà traité). Créer `episodes/NNN-mot-cle/` (NNN = numéro suivant sur 3 chiffres).

### 3. Écrire l'épisode
- `script_en.json` (langue de la chaîne ; `script.json` = ancien français, ne plus l'utiliser) : liste de segments `{"scene": "id", "text": ["phrase", …]}`. Modèle : `episodes/001-lune/script_en.json`. Rédiger directement en anglais naturel (américain), pas une traduction.
  - **1 000–1 400 mots, 14–20 segments** (≈ 7–10 min) ; accroche forte en 2 phrases ; promesse tenue dans les 10 premières secondes ;
    structure en 3–5 « chapitres » avec une relance de curiosité toutes les ~60 s (« But here's where it gets strange… ») pour garder le public jusqu'au bout ;
    exemples concrets, comparaisons à l'échelle humaine, une anecdote historique, une idée reçue corrigée ;
  - nombres écrits en toutes lettres (la voix les lit mieux) ; phrases courtes ;
  - **public américain (77 % des vues, Studio 2026-11-08)** : unités US d'abord (feet, miles, pounds, °F, gallons ; métrique éventuellement entre parenthèses à l'écran), comparaisons américaines (football field, school bus, Statue of Liberty, Empire State Building), orthographe et vocabulaire US (color, gas, fall, trash), exemples du quotidien US (dryer, garbage disposal, Thanksgiving…) quand c'est naturel ; titres et hashtags avec les mots que tapent les Américains.
  - textes dessinés à l'écran : écrire directement en anglais dans `scenes.py` (ou clé française + dictionnaire `TR["en"]` comme l'épisode 001) ;
  - **uniquement des faits établis** (NASA, ESA, CNRS, INSERM, OMS, Banque de France, encyclopédies…). Pas de chiffre douteux ;
    en cas de doute, formuler prudemment (« selon plusieurs études ») ou retirer. Lister les sources dans `meta.json` ;
  - fin : question au public + « And subscribe to Factora, so you never miss a fascinating fact. » (ne jamais citer de fréquence de publication : elle peut changer)
- `scenes.py` : une fonction de dessin par scène `sc_xxx(ctx, t, d)` (t = temps local, d = durée), le dict `SCENES`,
  la liste `SHORT_SCENES` (segments gardés pour le Short : **viser 25 à 35 s, jamais plus de 45 s** — vérifier avec build/timeline.json ; données Studio du 2026-11-07 : nos Shorts de 53–59 s ne sont regardés qu’en moyenne 10 à 19 s (18–36 %) → plus courts, la réponse complète avant 30 s, une 2e surprise au milieu, une dernière image qui relance la boucle ; commencer par l'accroche, finir par l'outro),
  et `thumbnail(c)` (1280×720, utiliser `thumb_text(c, ligne1, ligne2, bandeau)`).
  Modèle complet : `episodes/001-lune/scenes.py`. Style maison : fond bleu nuit, accents or, aplats vectoriels, pas d'images externes.
  **Qualité graphique exigée (2026-11-06)** — le moteur ajoute déjà halo lumineux, vignette, grain, sous-titres animés et 1440p ; les scènes doivent suivre :
  - **remplir le cadre** : le sujet principal occupe ≥ 60 % de la largeur en 16:9 et ≥ 75 % en 9:16 (Short) — jamais un petit objet au milieu d'un grand fond vide ;
  - **profondeur** : 3 plans par scène (fond en dégradé + éléments lointains estompés, sujet, premier plan / particules), dégradés plutôt qu'aplats unis, `glow()` sur les éléments importants ;
  - **mouvement permanent** : quelque chose bouge à chaque instant (particules, rotation, flux, rebond d'apparition `ease`) ; les éléments entrent en animation, jamais d'un coup ;
  - **chiffres-clés en grand** : quand le texte cite un nombre marquant (« 100,000 tons »), l'afficher en très gros (≥ 120 px en 16:9) avec un compteur qui défile ;
  - détails qui rendent l'objet reconnaissable (hublots, rivets, reflets, ombres portées), pas de silhouettes trop schématiques ;
  - varier les couleurs d'accent d'une scène à l'autre sur le fond bleu nuit ;
  - **couleurs vives (demande de Nazik, 2026-11-08)** : utiliser la palette saturée du moteur (`GOLD`, `CORAL`, `CYAN`, `GREEN`, `PINK`, `PURPLE`) — ne pas redéfinir de versions ternes dans `scenes.py` ; de grandes surfaces colorées (objets en dégradé de couleur, halos `glow()` colorés à 0,3–0,5), pas seulement des traits fins ; teinter le fond de certaines scènes (dégradé navy → violet ou navy → bleu-vert profond) ; le moteur ajoute à la finition +75 % de saturation, vibrance, fond tiré vers le bleu électrique (2026-11-08) ; les Shorts sont rendus nativement en 1440×2560, sans grain, avec un léger piqué (demande de Nazik 2026-11-08 : image plus fine) — écrire toutes les tailles en multiples de `U`, jamais en pixels bruts.
  - **CTA final obligatoire** : la scène `outro` (vidéo longue ET Short) appelle `cta(ctx, t, d, "<question de fin courte>")` du moteur (bouton SUBSCRIBE qui claque, clic, SUBSCRIBED, cloche, confettis), éventuellement par-dessus un rappel animé du sujet en fond estompé ; pas de bouton maison. Durée de la scène `outro` ≥ 4 s pour que l'animation aille au bout. Texte parlé du Short : question de fin + **appel à commenter ou partager adapté au sujet** (décision de Nazik, 2026-11-08 : 0 partage sur TikTok, peu d'interactions sur IG) + « Subscribe for more things you never noticed. » (vidéo longue : phrase habituelle).
  - **Appel à l'engagement** (une phrase courte, ≤ 10 mots, aussi affichée à l'écran via `cta(…, line2="<même phrase en MAJUSCULES>")`) : paradoxe / énigme → « Did you spot it? Comment your answer. » ; quotidien → « Send this to someone who <fait l'habitude du sujet>. » / « Tag someone who… » ; corps → « Comment if this happens to you. ». Reprendre la même phrase dans le commentaire publié (`meta.comment`) et dans la légende TikTok/Instagram.
  Les dessins doivent être **originaux et propres au sujet** (exigence YouTube « contenu authentique »).
  Éviter le bas de l'écran (sous-titres : ~0,80–0,92 H en 16:9, ~0,70–0,78 H en 9:16).
- `meta_en.json` : `hook_text` (question courte, ≤ 8 mots, affichée en grand dès la 1re image du Short ; ex. « WHAT IF THE SUN WENT OUT? »), `playlist` (`what_if`, `how` ou `why`), `comment` (question au public, 1 phrase + emoji, publiée sous la vidéo), `title` (≤ 70 car., curiosité + mot-clé), `short_title` (question courte + 1 emoji, finir par `#shorts`), `description` (avec `{CHAPITRES}`),
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
Contrôles finaux : **extraire 3 images de chaque vidéo finale** (`ffmpeg -ss T -i build/video_X.mp4 -frames:v 1 …png`) et les regarder (couleurs, sous-titres nets, pas de dédoublement) — les captures `still_*` ne passent pas par la finition ffmpeg ; taille de la vidéo longue < 95 Mo ; `ffprobe` (durée Short ≤ 60 s), volume (`volumedetect` : moyenne entre −24 et −16 dB), miniature lisible.
Construire la description : `python3 engine/description.py episodes/NNN-x` (→ `build/description.txt`, chapitres calculés).

### 5. Héberger les fichiers (lien public pour Zapier)
```bash
bash engine/host.sh episodes/NNN-x NNN   # ajoute les fichiers sur la branche durable « backlog » et affiche les 3 URL publiques
```
(Les « releases » GitHub sont interdites depuis les sessions : ne pas les utiliser.)

### 6. Publier via Zapier (action YouTube « Upload Video »)
Vidéo longue : `title`, `description` (= build/description.txt), `tags`, `video` = URL, `privacy_status` = `config.privacy_first` (= "public" depuis le 2026-11-06 : publication directe, Nazik contrôle a posteriori),
`made_for_kids` = false, `category_id` = "27" (Éducation), `default_language` = en-US, `default_audio_language` = en-US, `notify_subscribers` = true.
**Ne pas passer `thumbnail` dans l'upload** (s'il échoue, la vidéo est quand même créée → risque de doublon).
**Pas de vérification de doublons** (supprimée le 2026-11-07 pour économiser les tasks Zapier) : ne jamais relancer un upload qui a renvoyé un `id`.
Puis action « Update Video Thumbnail » (`video_id`, `thumbnail` = URL miniature). Si refus « permissions… thumbnails »
(normalement résolu : téléphone vérifié le 2026-11-04) : continuer sans, noter `"thumbnail_set": false`, le signaler dans le résumé final.
Lors de l'étape 1, réessayer la miniature des épisodes avec `"thumbnail_set": false` (fichier : régénérer avec `render.py thumb` puis `host.sh`, ou ignorer si impossible).
Short : `short_title`, description courte (anglais) avec le lien `https://youtu.be/<long_id>` + hashtags, sans miniature, `notify_subscribers` = false.
Ensuite, pour la vidéo longue : **pas d'ajout automatique en playlist** (supprimé le 2026-11-07 pour économiser les tasks ; Nazik le fait dans Studio si elle veut, la playlist conseillée = `meta.playlist`, à rappeler dans le résumé final) ;
publier le commentaire `meta.comment` (POST `commentThreads?part=snippet` avec `{"snippet":{"channelId":…,"videoId":…,"topLevelComment":{"snippet":{"textOriginal":…}}}}`).
Le commentaire ne peut pas être épinglé par l'API : le rappeler à Nazik dans le résumé final. Un 429 de Zapier : attendre 60 s et réessayer une fois.
Si l'upload échoue pour limite de mises en ligne : ne pas réessayer ; ajouter l'épisode avec `"status": "attente_youtube"` et `urls` (celles de host.sh), continuer avec TikTok.
Ajouter l'épisode dans `published.json` (`episode`, `topic`, `dir`, `date`, `long_id`, `short_id`, `status`, `thumbnail_set`).
Cocher le sujet dans `topics.md` (date + numéro). `git add -A && git commit && git push origin main`.

### 6 bis. Publier le Short sur TikTok (via Buffer, Zapier)
Action Zapier Buffer « Add to Queue » (selected_api BufferCLIAPI, action « update », tool_name « buffer_add_to_queue »),
avec le `connection_id`, l'`organizationId` et le `channelId` TikTok donnés dans le message de la tâche planifiée.
Paramètres : `method` = "schedule", `scheduled_at` = aujourd'hui 19:30 heure de New York (heure de pointe US) — calculer avec
`python3 -c "from datetime import datetime;from zoneinfo import ZoneInfo as Z;n=datetime.now(Z('America/New_York'));t=n.replace(hour=19,minute=30,second=0,microsecond=0);print((t if t>n else n.replace(second=0,microsecond=0)).isoformat())"`
(si 19:30 est déjà passé à New York : `method` = "share_now"), `attachment` = "video", `video` = URL du Short (celle de host.sh), `scheduling_type` = "direct",
`text` (en anglais) = accroche (1–2 phrases) + « Full video on YouTube: @factoraofficiel » + « Synthetic voice, original illustrations. »
+ 5–6 hashtags (#sciencetok #didyouknow #learnontiktok #factora + 1–2 du sujet). Mettre dans la 1re phrase les mots-clés que les gens taperaient dans la recherche TikTok. ≤ 2 200 caractères.
Le Short est programmé sur TikTok dès cette exécution (pas d'étape « non répertorié » sur TikTok).
Noter dans `published.json` : `"tiktok_buffer_id"` (champ `id` de la réponse) et `"tiktok": "envoye"`.
Si Buffer échoue : ne pas bloquer YouTube ; noter `"tiktok": "echec"` et le signaler dans le résumé final.

### 6 ter. Publier le Short en Reel Instagram (via Buffer, Zapier) — depuis le 2026-11-07
Même action Buffer que 6 bis, avec le `channelId` **Instagram** donné dans le message de la tâche planifiée (compte @factora132).
`dynamic_properties` : `ig_post_type` = "reels", `ig_share_to_feed` = "true", `video` = URL du Short, `scheduling_type` = "direct",
`scheduled_at` = même heure que TikTok (19:30 New York ; sinon `method` = "share_now"),
`text` (anglais) = accroche + « Full videos on YouTube: Factora (link in bio) » (**pas** « @factoraofficiel » : sur Instagram ce @ pointe vers un autre compte)
+ « Synthetic voice, original illustrations. » + 5–6 hashtags (#science #didyouknow #learnoninstagram #factora + 1–2 du sujet).
**Buffer gratuit : 10 publications en attente maximum par compte** (erreur « 10 scheduled post limit ») : dans ce cas, réessayer quelques minutes plus tard ou utiliser `share_now`. Tous les anciens Shorts (001–014) ont été publiés en Reels le 2026-11-07.
Noter dans `published.json` : `"instagram_buffer_id"` et `"instagram": "envoye"` (ou `"echec"`, signalé dans le résumé final, sans bloquer le reste).

### 7. Prévenir Nazik
**Notification push** (`PushNotification`, < 200 caractères, une seule ligne) : « Factora : <titre court> en ligne — https://youtu.be/<long_id> ».
En cas d'échec bloquant : notification « Factora — échec épisode NNN : <erreur en quelques mots> ».
Terminer par un court résumé en français (liens des 2 vidéos, statuts TikTok/Instagram, rappel d'épingler le commentaire et de relier le Short à la vidéo longue dans Studio). Plus aucun e-mail.

## Référence des appels Zapier (à utiliser tels quels, sans `inspect`)
Tous les appels YouTube : `selected_api` = "YouTubeV4CLIAPI", `connection_id` = celui de la tâche planifiée.
- **GET** : `execute_zapier_read_action`, action "_zap_raw_request", tool_name "youtube_make_api_get_request",
  params `{"url": "https://www.googleapis.com/youtube/v3/<ressource>", "querystring": {…}, "fail_on_errors": "false"}` (**jamais** de `?…` dans l'URL : erreur 400).
  Garde-fou : ressource `channels`, querystring `{"part": "id", "mine": "true"}`.
- **POST / PUT / DELETE** : `execute_zapier_write_action`, action "_zap_raw_request", tool_name "youtube_make_api_mutating_request",
  params `{"url": …, "method": "POST"|"PUT"|"DELETE", "querystring": {"part": "snippet"|"status"}, "body": "<JSON en texte>", "fail_on_errors": "false"}`.
- **Upload** : `execute_zapier_write_action`, action "upload_video", tool_name "youtube_upload_video", params `title`, `description`, `tags` (liste), `video` (URL), `privacy_status`, `made_for_kids` "false", `category_id` "27", `default_language` "en-US", `default_audio_language` "en-US", `notify_subscribers` "true"|"false".
- **Miniature** : action "upload_video_thumbnail", tool_name "youtube_update_video_thumbnail", params `video_id`, `thumbnail` (URL).
- **Buffer** : `selected_api` "BufferCLIAPI", action "update", tool_name "buffer_add_to_queue", `connection_id`, params
  `{"method": "schedule"|"share_now", "channelId": …, "organizationId": …, "dynamic_properties": {…}}`.
  TikTok : `dynamic_properties` = `text`, `attachment` "video", `video`, `scheduling_type` "direct", `scheduled_at`.
  Instagram : `dynamic_properties` = `ig_post_type` "reels", `ig_share_to_feed` "true", `text`, `video`, `scheduling_type` "direct", `scheduled_at`.
- **Playlists** (`config.json → playlists`) : what_if, how, why, recap.

## Récap du samedi (tâche planifiée séparée, samedi soir heure de New York)
Même garde-fou chaîne (étape 0) avant toute écriture YouTube.
1. Épisodes à résumer : ceux de `published.json` en `"status": "public"` (ou unlisted) qui ne figurent dans aucune entrée de `recaps.json`. S'il y en a plus de 7, garder les 7 qui ont le plus de vues (GET `videos?part=statistics&id=…` sur `long_id` + `short_id`) ; les autres restent pour un prochain récap. Moins de 3 épisodes : ne rien publier, prévenir Nazik.
2. Créer `episodes/recap-AAAA-MM-JJ/` :
   - `script_en.json` : **≈ 1 100–1 200 mots (≈ 8 min)**, narration NEUVE (pas un copier-coller des scripts) : intro accrocheuse (« This week on Factora: … »), puis ~1 min par épisode (le fait le plus surprenant, l'explication essentielle), du plus fort au moins fort, transitions entre sujets, fin : « Which one surprised you most? Tell us in the comments. » + appel à l'abonnement. Mêmes règles de faits établis.
   - `scenes.py` : réutiliser les illustrations des épisodes avec `episode_scenes("episodes/NNN-x")` (fonction du moteur) :
     `A = episode_scenes("episodes/005-airplane"); SCENES = {"intro": sc_intro, "e005_wing": A["wing"], …}` — choisir des scènes sans étiquette numérotée hors contexte ; ajouter une scène d'intro et une carte titre par sujet (dessinées dans ce fichier), `SHORT_SCENES = []`, `thumbnail(c)` (mosaïque des sujets + « THIS WEEK'S MOST FASCINATING FACTS »).
   - `meta_en.json` : `title` du type « 7 Mind-Blowing Facts From This Week: … » (≤ 70 car.), description avec `{CHAPITRES}` (un chapitre par sujet) et liens `https://youtu.be/<long_id>` de chaque épisode, `playlist` = `recap` si elle existe dans config.json sinon aucune, `comment`, `tags`.
3. `tts.py`, captures de contrôle (Read), `render.py long` (> 5 min 30 → 1080p automatiquement, fichier < 100 Mo), `render.py thumb`, `description.py`, `host.sh episodes/recap-… recap-AAAA-MM-JJ`.
4. Upload YouTube **public directement** (contenu déjà validé), `notify_subscribers` = true, miniature, commentaire (pas de vérification de doublons ni d'ajout en playlist : économie de tasks). Pas de Short ni de TikTok pour le récap.
5. Ajouter `{"date", "dir", "video_id", "episodes": [numéros]}` à `recaps.json`, commit + push, **notification push** « Factora : récap de la semaine en ligne — https://youtu.be/<id> » (pas d'e-mail). Statistiques de l'étape 1 : **un seul** GET groupé sur tous les ids.

## Sujets d'actualité / politiques
Strictement **neutres et factuels** : expliquer les règles et mécanismes (institutions, chiffres officiels), présenter chaque scénario avec ses effets sans jugement ni préférence, temps de parole égal pour chaque camp, aucun pronostic, aucun qualificatif partisan, aucune personne politique caricaturée ou dessinée. Ne citer un résultat électoral que s'il est vérifié à la date de production (AP, sources officielles) ; sinon rester sur les mécanismes. Exemples illustrés avec un projet de loi **fictif** et des partis représentés par des couleurs neutres (pas rouge/bleu : utiliser or et cyan avec une légende « Party A / Party B »).

## Règles
- **Short seul** (`meta_en.json → format = "short_seul"`) : à la demande de Nazik pour un sujet qui ne justifie pas 8 min. Pas de vidéo longue ni de miniature (`host.sh` n'héberge que les fichiers présents), Short public + commentaire + TikTok. Dans `published.json` : `"format": "short_seul"`, `long_id` null. Le récap du samedi peut l'inclure (statistiques sur `short_id`, scènes réutilisables).
- Jamais de contenu « conçu pour les enfants ». Jamais de copie d'une œuvre existante. Jamais de visage ou de voix d'une personne réelle.
- Une seule publication par exécution. Ne jamais republier un sujet déjà coché.
- Ne jamais écrire sur YouTube si le garde-fou chaîne échoue.
- Ne pas committer `build/` (vidéos lourdes) : elles vivent dans les releases du dépôt d'hébergement.
