---
type: spine-review
lens: règle — liste de contrôle « bonne ossature »
target: _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
ticket: _bmad-output/initiative-escamanager/initiative-escamanager.md
journal: _bmad-output/initiative-escamanager/architecture-escamanager/.memlog.md
contexte: revueuse fraîche, sans participation à la rédaction ; greenfield ; altitude feature (cinq épics)
date: 2026-11-04
---

# Revue « bonne ossature » — EscaManager, première partie

Revue de l'ossature `architecture-escamanager.md` contre la liste de contrôle « bonne ossature », point par point. Les technologies nommées ont été re-vérifiées le jour de la revue (sources en section 4). Chaque constat porte une sévérité — critique / haute / moyenne / basse — et, quand elle est évidente, sa correction mécanique.

## Verdict

Ossature solide et honnête — paradigme nommé et porté par huit AD applicables, enveloppe opérationnelle présente, Deferred propre — utilisable pour découper les cinq épics après correction d'un manque haut (la politique d'effacement des données personnelles, transversale à trois épics, n'est ni décidée ni différée ni posée) et de deux manques moyens (propriétaire non assigné pour l'entité `Adherent` ; versions de base de données affichées comme cibles alors qu'elles sont des moteurs en fin de vie).

## Constats (sévérité décroissante)

### C1 — [haute] La politique d'effacement des données personnelles (R2) n'est ni décidée, ni différée, ni question ouverte

R2 exige un effacement « sans intervention technique ». Cet effacement ne reste pas dans l'épic comptes : il touche ce que les autres épics stockent — l'épic 3 (identité des adhérents, données des mineurs via R9), l'épic 4 (les listes qui « reflètent les adhésions enregistrées », R7). La tension est directe et non tranchée : après effacement, la liste d'une saison passée montre-t-elle un trou (suppression physique) ou une ligne anonymisée ? Deux épics peuvent y répondre de façon incompatible, et la séquence de livraison rend l'oubli silencieux : l'épic 1 sera raffinée avant que l'entité `Adhesion` existe ; si elle implémente l'effacement pour le seul `Compte`, l'épic 3 créera des tables de données personnelles hors de portée de l'effacement — R2 cassée sans que rien ne le détecte.

**Correction mécanique :** une question ouverte dans le memlog puis dans la spine — « effacement RGPD : anonymisation des entités liées (`Adherent`, `Adhesion`…) vs suppression — à trancher avant le raffinement de l'épic 3 » — ou un AD court si la réponse est déjà évidente pour le club (l'anonymisation en préservant les listes historiques est le schéma usuel, mais c'est une décision métier).

### C2 — [moyenne] AD-4 dit « une entité, un propriétaire », mais l'entité la plus partagée n'a pas de propriétaire assigné

La Capability Map assigne `Compte`/`Permission`, `Saison`/`Option`, `Adhesion` — pas `Adherent` (ni `Paiement`, ni `Licence`). Or quatre exigences traversent `Adherent` : R5 (création, épic 3), R7 (« consulter **et corriger** » — une mutation, épic 4), R9 (rattachement au représentant, épic 3), R10 (licence, épic 5) — dont les épics 4 et 5, construites en parallèle. Sans assignation, le raffinement de l'épic 4 peut légitimement croire que « corriger la liste » lui donne la persistance des adhérents : deux dépôts d'écriture pour la même entité, précisément la divergence qu'AD-4 énonce sans la fermer.

**Correction mécanique :** une ligne par entité partagée dans la Capability Map (lecture naturelle : `adhesions` possède `Adherent` et `Paiement`, `federation` possède `Licence`, `membres` ne possède que ses vues et son export) — ou question ouverte si l'assignation est un vrai trade-off.

### C3 — [moyenne] Versions de base de données : la cible affichée est aujourd'hui deux moteurs en fin de vie

Le tableau Stack affiche « MySQL 8.0.11+ ou MariaDB 10.5+ » comme version de la base. Ce sont exactement les planchers de compatibilité du backend Django 5.2 (doc officielle vérifiée ce jour), pas des versions à déployer : vérifié le 04/11/2026, MySQL 8.0 est en fin de support étendu depuis le 30/04/2026 et MariaDB 10.5 depuis le 24/06/2025. Toujours vivantes : MySQL 8.4 LTS (support jusqu'en 2032) et 9.x LTS ; MariaDB 10.11 LTS, 11.4 LTS, 11.8 LTS. La CI devant « tester sur MySQL/MariaDB comme en production », un pin lu comme « 8.0/10.5 » peut faire tourner la prod sur un moteur sans correctifs de sécurité — pour une application qui stocke des données personnelles.

**Correction mécanique :** dissocier dans le tableau Stack la cible de déploiement (« MySQL 8.4 LTS+ ou MariaDB 11.4 LTS+, version concrète fixée avec le choix PaaS à l'épic 1 ») du plancher de compatibilité backend (MySQL 8.0.11+ / MariaDB 10.5+), qui reste seul dans AD-7.

### C4 — [moyenne] Exploitation : la restauration des sauvegardes et la supervision de production sont silencieuses

L'enveloppe opérationnelle est présente et correcte — conteneur unique gunicorn + WhiteNoise, environnements local/production, base managée avec sauvegardes quotidiennes, TLS, CI fidèle à la production — c'est mieux que ce qu'une ossature focalisée domaine offre habituellement. Restent deux angles ni décidés, ni différés, ni question ouverte :

- **Restauration** : les sauvegardes quotidiennes sont citées, jamais la capacité à restaurer ni son test. Une sauvegarde jamais restaurée n'en est pas une, et chaque épic livrée en production accumule des données d'adhérents.
- **Supervision** : rien sur l'alerte de disponibilité ou d'erreur. Une panne entre deux livraisons passera inaperçue pour un club tenu par des bénévoles ; les échecs des appels externes (webhooks HelloAsso, API FFME) seront invisibles.

**Correction mécanique :** deux lignes en Deferred — « procédure de restauration testée une fois — épic 1 » et « sonde de disponibilité (sonde HTTP native du PaaS ou service externe gratuit) — épic 1 ».

### C5 — [basse] La mécanique i18n n'est pas décidée

La contrainte « interface intégralement en français » est couverte par les conventions (symboles, apps et URLs en français ; « erreurs présentées en français »), mais rien ne dit si l'i18n de Django est activée (gettext) ou si les textes sont en français en dur. Deux épics peuvent choisir différemment — divergence stylistique à faible impact (site unilingue), mais vérifiable et fixable en une ligne.

**Correction mécanique :** une ligne en conventions, p. ex. « textes français en dur dans les gabarits et les chaînes ; framework de traduction non activé » (ou l'inverse).

### C6 — [basse] Vérifiabilité inégale : certains AD ont un garde, d'autres n'en ont pas

AD-1 nomme son garde (test d'imports en CI — exemplaire) et AD-8 est entièrement mécanique. AD-3 est vérifiable par le même test d'imports mais ne le dit pas ; AD-2 (contournement du domaine) et AD-6 (page fonctionnelle sans JS) n'ont aucun garde nommé et ne restent applicables qu'en revue. La convention « permissions vérifiées par un mécanisme unique » est dans le même cas : le mécanisme n'est pas nommé, donc « unique » reste à interpréter tant que l'épic 1 ne l'a pas posé.

**Correction mécanique :** étendre le garde de l'AD-1 en « tests d'architecture (AD-1, AD-3) » ; nommer un garde pour AD-6 (ex. un test fonctionnel sans JS par page) ; nommer le mécanisme de permissions à l'épic 1 (un seul mixin/décorateur Django).

### C7 — [basse] Étiquetage et liaisons

- Le memlog dit « altitude: initiative », la spine « altitude: feature » — même niveau réel (celui qui tient les cinq épics), mais les épics citeront l'un ou l'autre : aligner le libellé.
- Le glossaire FR/EN, compagnon du billet, n'est pas référencé par la spine alors que cinq équipes nommeront des symboles en français — l'app de la liste s'appelle `membres`, l'entité `Adherent` : une ligne dans les sources de la spine prévient la dérive de vocabulaire.

## Passage de la liste de contrôle, point par point

### 1. Les vrais points de divergence pour les cinq épics — rien de manqué ?

Couverts : structure et pureté du domaine (AD-1, AD-2), frontières entre apps (AD-3, le point le plus aigu vu que `membres` et `federation` sont construites en parallèle), chemin d'écriture et transactions (AD-4), intégrations externes (AD-5), style de rendu (AD-6), dialecte SQL et migrations (AD-7), seuil de fusion (AD-8), contrôle d'accès (convention « mécanisme unique »), formats transverses (Decimal, dates ISO), nommage français. Deux points de divergence réels ne sont pas fixés : la politique de données personnelles (C1) et la propriété de `Adherent` (C2). Structurellement complet ; data-métier, deux manques.

### 2. Chaque AD est-il applicable et prévient-il réellement sa divergence ?

- **AD-1** : règle binaire (imports interdits) avec garde nommé en CI. Oui, pleinement.
- **AD-2** : applicable en revue (aucune lecture/écriture d'entité hors service ou port) ; prévient l'éparpillement ; garde non mécanique (C6).
- **AD-3** : trivialement vérifiable ; garde à rattacher au test d'imports (C6) ; prévient le couplage croisé.
- **AD-4** : la règle est applicable (un propriétaire, une mutation = un service en transaction) mais incomplète sans assignation des entités partagées (C2).
- **AD-5** : applicable (interfaces dans `domaine/ports/`, protocole confiné aux adaptateurs — couvert en amont par AD-1 côté domaine) ; le bouchon FFME prévient réellement le blocage de l'épic 5 par l'incertitude API.
- **AD-6** : applicable (testable fonctionnellement) ; prévient la bifurcation monopage ; garde non nommé (C6).
- **AD-7** : applicable (backend unique dans les réglages, absence de SQL de dialecte, migrations seules) ; prévient le verrouillage ; nuance de versions → C3.
- **AD-8** : entièrement mécanique ; prévient le code non testé et la dérive entre contributeurs.

Aucun AD dont la règle serait invérifiable ou qui ne préviendrait pas sa divergence déclarée. Le recouvrement AD-2/AD-4 sur « mutation = service » est bénin.

### 3. Rien sous Deferred ne peut laisser deux unités diverger

Vérifié item par item : chaque différé est soit mono-épic (flux HelloAsso → épic 3 seule ; API FFME → épic 5 seule, derrière le bouchon), soit un socle posé par l'épic 1 dont les épics suivantes héritent (fournisseur PaaS, outillage du rendu, ensembles de permissions), soit hors périmètre explicite (sauvegarde au-delà du quotidien, plein-texte). Les deux seules unités parallèles (épics 4 et 5) héritent du rendu posé en 1 et du bouchon FFME. Rien à déplacer. Point fort.

### 4. Technologies d'actualité — vérifiées le 04/11/2026, pas affirmées

| Nom (spine) | Vérification du jour | Statut |
| --- | --- | --- |
| Django 5.2 LTS | endoflife.date : LTS courante, sécurité jusqu'au 30/04/2028, dernière 5.2.19 (03/11/2026) ; supporte Python 3.10–3.14 | ✓ à jour, runway long |
| Python 3.13 | endoflife.date : sécurité jusqu'au 31/10/2029 (active support clos le 01/10/2026) ; pin « maturité + runway » documenté au memlog | ✓ défendable |
| mysqlclient 2.3.0 | PyPI : 2.3.0 du 14/09/2026, production/stable, Python ≥ 3.10, wheels cp313 ; pilote recommandé par la doc Django | ✓ à jour |
| MySQL 8.0.11+ / MariaDB 10.5+ | doc Django 5.2 : planchers de compatibilité exacts — mais endoflife.date : MySQL 8.0 EOL 30/04/2026, MariaDB 10.5 EOL 24/06/2025 | △ voir C3 |
| GitHub Actions | service omniprésent, pas de pin de version requis | ✓ |
| PythonAnywhere 10 $/mois | page pricing du jour : Developer 10 $/mois, une web app, domaine personnalisé, ~150 000 hits/jour, MySQL incluse | ✓ conforme au memlog |
| WhiteNoise, gunicorn | nommés sans version dans le diagramme de déploiement ; standards vivants de l'écosystème Django | ✓ |

Les affirmations du memlog (vérifications datées du 26/10 et 04/11) sont confirmées à un détail près : Django est passé de 5.2.18 à 5.2.19 entre-temps — sans importance. Scalingo et Clever Cloud restent marqués « à confirmer » dans la spine : honnête, la vérification est correctement différée au moment du choix. Une seule réserve réelle : C3.

### 5. Chaque exigence du billet est couverte

- R1, R4, R5, R8, R9, R10 : couvertes nominativement par la Capability Map, avec la bonne altitude (le détail — format d'export, structure du rattachement mineur — correctement laissé aux épics).
- R2 : couverte nominativement (`comptes`), mais l'invariant transversal manque → C1.
- R3 : mécanique RBAC fixée par le billet et la convention ; ensembles concrets différés à l'épic 1 ✓ ; mécanisme unique à nommer (C6).
- R6 : port HelloAsso + flux différé à l'épic 3 (mono-épic, sûr) — mais l'entité `Paiement` (« chaque paiement abouti enregistré avec son moyen ») n'apparaît ni dans le seed ni dans la map : à rattacher à C2.
- R7 : la correction de liste est une mutation → C2.
- Contraintes : responsivité (AD-6 + Deferred outillage) ✓ ; open-source/gratuit « autant que possible » ✓ (stack 100 % open-source, seuls hébergement et base managé sont payants) ; disponibilité chez les hébergeurs courants ✓ ; backend en deux parties, une seule application consommatrice (paradigme + AD-1/AD-2, « Must not change » respecté) ✓ ; interface en française ✓-ish (C5) ; documentation/code en français — héritée du billet, correctement non re-décidée ; RGPD → C1 ; identité visuelle du club (Deferred + passage `bmad-ux`) ✓ ; HelloAsso (AD-5) ✓.

Couverture nominative complète ; deux angles morts structurels (C1, et `Paiement`/`Adherent` via C2).

### 6. Chaque dimension possédée par l'altitude est décidée, différée ou ouverte

- **Décidées** : paradigme, frontières et dépendances, mutations et transactions, intégrations externes, rendu, persistance et dialecte, seuil de fusion, déploiement et environnements (local/production, conteneur unique, base managée, TLS), nommage et formats, secrets en variables d'environnement.
- **Différées avec échéance** : fournisseur PaaS (épic 1), outillage du rendu (épic 1), flux HelloAsso (épic 3), API FFME (épic 5), ensembles de permissions (épic 1).
- **Question ouverte** : l'API FFME (au billet et dans Deferred, avec recherche `bmad-deep-recon` prévue).
- **Silencieuses** : politique de données personnelles (C1 — la plus lourde), restauration et supervision (C4), mécanique i18n (C5).

L'enveloppe opérationnelle — le piège classique d'un draft focalisé domaine — est ici présente et correcte ; il ne manque que les deux angles de C4. Le fuseau horaire (`USE_TZ`/Europe/Paris) n'est pas décidé mais reste un réglage global du socle épic 1, sans risque de divergence entre épics : remarque, pas constat.

## Points forts

- Le paradigme est nommé et porté partout : les AD se renforcent mutuellement (AD-1 rend AD-5 presque gratuit ; AD-3 + AD-4 ensemble ferment le couplage croisé).
- Le traitement de l'incertitude FFME — port dans le domaine, bouchon, recherche différée avant l'épic 5 — est exactement le bon geste : il découple l'épic 5 du risque de recherche.
- L'enveloppe opérationnelle est posée avec un niveau de détail supérieur à ce que cette altitude offre habituellement.
- Le Deferred est propre : chaque item a une échéance et un décideur identifiable.
- Le memlog est tenu avec vérifications datées et sourcées — l'autorité est traçable, et mes re-vérifications du jour le confirment.

## Récapitulatif des actions

| # | Sévérité | Action |
| --- | --- | --- |
| C1 | haute | Question ouverte (ou AD court) sur l'effacement RGPD — anonymisation vs suppression — avant le raffinement de l'épic 3 |
| C2 | moyenne | Assigner le propriétaire de persistance de `Adherent`, `Paiement`, `Licence` dans la Capability Map |
| C3 | moyenne | Dissocier cible de déploiement (8.4 LTS / 11.4 LTS+) et plancher de compatibilité (8.0.11+ / 10.5+) dans le tableau Stack |
| C4 | moyenne | Ajouter en Deferred : restauration testée, sonde de disponibilité — épic 1 |
| C5 | basse | Décider la mécanique i18n en une ligne de conventions |
| C6 | basse | Étendre les tests d'architecture à AD-3, nommer un garde pour AD-6 et le mécanisme de permissions |
| C7 | basse | Aligner le libellé d'altitude memlog/spine ; référencer le glossaire dans les sources de la spine |
