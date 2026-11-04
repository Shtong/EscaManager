---
type: review
reviewer: verification-web (contexte frais)
scope: architecture-escamanager.md — chaque décision engagée de l'ossature a-t-elle été recherchée sur le web ou confrontée au réel ?
date: '2026-11-04'
inputs:
  - _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
  - _bmad-output/initiative-escamanager/architecture-escamanager/.memlog.md
  - _bmad-output/initiative-escamanager/initiative-escamanager.md
---

# Revue de vérification web — ossature EscaManager (première partie)

## Verdict

L'ossature est globalement saine et fraîche — le socle vérifié au journal (Django 5.2 LTS, Python 3.13, compatibilité MySQL/MariaDB, mysqlclient) tient toujours mot pour mot — mais **trois énoncés affirment des propriétés que le réel dément en novembre 2026** : les bornes de versions de base de données (séries au plancher mortes), le tableau idéalisé du candidat PythonAnywhere (base MySQL 8.0 en fin de vie, bases créées en latin1, sauvegardes manuelles), et la mention « sauvegardes quotidiennes » fausse pour un des trois candidats. De plus, deux briques fondatrices — HelloAsso et GitHub Actions — n'avaient jamais été vérifiées nulle part : cette revue les confirme, et apporte une découverte (la passerelle officielle HelloAsso→myFFME de la FFME) qui change la donne du futur deep-recon de l'épic fédération. Rien de bloquant : tout est corrigeable en quelques lignes avant l'épic 1.

## Méthode

Lecture intégrale de l'ossature, du journal (.memlog.md) et du billet d'initiative. Le journal enregistre des vérifications datées du 26/10/2026 (Django, Python, Node, PostgreSQL, hébergeurs, compatibilité MySQL/MariaDB via doc Django) et du 04/11/2026 (mysqlclient). Cette revue n'a pas refait ce qui était frais et sourcé ; elle a vérifié sur le web, le 04/11/2026, tout ce qui était affirmé sans vérification : HelloAsso, GitHub Actions, gunicorn, WhiteNoise, état de vie réel des séries MySQL/MariaDB, calendrier Django, PythonAnywhere en détail, Scalingo, Clever Cloud, FFME.

Sources consultées le 04/11/2026 : endoflife.date (API django, mysql, mariadb, python), djangoproject.com/download, docs.djangoproject.com/fr/5.2/ref/databases, PyPI (mysqlclient, whitenoise, gunicorn), docs.github.com (« About billing for GitHub Actions »), pythonanywhere.com/pricing, help.pythonanywhere.com (UsingMySQL, DatabaseCharacterSets), forum PythonAnywhere (thread 36691), scalingo.com/pricing, scalingo.com/databases/mysql, doc.scalingo.com/databases/mysql, clever-cloud.com/pricing, info.helloasso.com/modele-economique, centredaide.helloasso.com, dev.helloasso.com / api.helloasso.com (Swagger v5), ffme.fr (rentrée des clubs 2025-2026 et 2026-2027).

## Constats

### C1 — Bornes de versions de base de données : le plancher de compatibilité Django est confondu avec une cible de déploiement, et les séries au plancher sont mortes — **haute**

- **Constat.** AD-7 et la table Stack écrivent « MySQL 8.0.11+ ou MariaDB 10.5+ (InnoDB, utf8mb4) ». Ces bornes sont exactes comme *plancher de compatibilité Django 5.2* — mais l'ossature les présente comme la spec de la base, sans distinguer plancher de test et version à déployer.
- **Vérifié (04/11/2026).** endoflife.date/api/mysql : la série MySQL 8.0 est **EOL depuis le 30/04/2026** (dernier patch 8.0.46, 07/04/2026) ; les versions vivantes sont 8.4 LTS (support étendu 2032) et 9.7 LTS (2034). endoflife.date/api/mariadb : MariaDB 10.5 est **EOL depuis le 24/06/2025** et 10.6 depuis le 06/07/2026 ; les LTS vivantes sont 11.4 (05/2029), 11.8 (06/2028) et 12.3 (06/2029). Le journal (26/10) avait vérifié la compatibilité via la doc Django, jamais l'état de vie des séries elles-mêmes — non couvert. Chez les PaaS candidats : doc.scalingo.com montre des guides « Upgrading to MySQL 8.0 » **et « Upgrading to MySQL 8.4 »** (8.4 disponible chez Scalingo) ; **aucun des trois candidats (Scalingo, Clever Cloud, PythonAnywhere) n'offre MariaDB** — la moitié « MariaDB » de la fourchette n'a pas de candidat PaaS dans la liste de l'ossature.
- **Non vérifié.** Version MySQL exacte offerte par Clever Cloud (page produit sans version).
- **Action.** Corriger AD-7/Stack : plancher de compatibilité (Django) ≠ cible de déploiement — viser MySQL 8.4 LTS chez le PaaS (ou MariaDB 11.4+/12.3 en local/CI si MariaDB), et ne pas faire tourner la CI sur `mysql:8.0`/`mariadb:10.5`, qui sont des versions en fin de vie.

### C2 — PythonAnywhere : le candidat « le moins cher » cache une base MySQL 8.0 en fin de vie, un charset par défaut latin1 contraire à AD-7, et des sauvegardes manuelles — **haute**

- **Constat.** Le journal motive la bascule MySQL en partie par l'« économie réelle sur PythonAnywhere (MySQL incluse au plan 10 $) », et le Structural Seed affirme « base managée MySQL/MariaDB, sauvegardes quotidiennes ». Trois propriétés fines n'avaient jamais été vérifiées et sont démenties ou contredites aujourd'hui.
- **Vérifié (04/11/2026).**
  - Prix : pythonanywhere.com/pricing — Developer toujours **10 $/mois**, 1 app, domaine personnalisé, MySQL incluse, ~150 000 hits/jour, internet sortant non restreint (offre gratuite toujours non pertinente : MySQL désormais réservée aux comptes payants — help.pythonanywhere.com/pages/UsingMySQL).
  - Version : forum PythonAnywhere, thread « When will PythonAnywhere support MySQL 8.4? (8.0 reaches EOL this month) » (20/04/2026) — le staff confirme que le serveur actuel est **MySQL 8.0** et que 8.4 est « on our roadmap… no ETA » (avril) puis « actively testing » (août 2026). Or 8.0 est EOL upstream depuis avril 2026 (cf. C1) : la base « incluse » est une série en fin de vie, sans correctifs upstream.
  - Charset : help.pythonanywhere.com/pages/DatabaseCharacterSets — les bases y sont **créées par défaut en latin1/latin1_swedish_ci** ; l'exigence AD-7 (utf8mb4) n'y est pas satisfaite sans `ALTER DATABASE` préalable (la doc PA illustre même avec `utf8`, pas `utf8mb4`).
  - Sauvegardes : help.pythonanywhere.com/pages/UsingMySQL renvoie les sauvegardes vers **mysqldump manuel** — pas de sauvegarde quotidienne automatisée documentée, contrairement au Structural Seed.
- **Non vérifié.** Date de disponibilité de MySQL 8.4 chez PythonAnywhere ; affirmation d'un utilisateur du forum (non confirmée par une source Django officielle) selon laquelle Django 6.1 abandonnerait MySQL 8.0 — sans impact sur le pin 5.2, à surveiller pour la migration 6.2.
- **Action.** À l'épic 1, re-peser PythonAnywhere avec ces données réelles (base EOL + latin1 + sauvegardes manuelles) face à Scalingo (MySQL 8.4, sauvegardes quotidiennes, Let's Encrypt, chiffrement au repos — vérifiés) ; si PythonAnywhere est retenu, documenter dans l'épic 1 le `ALTER DATABASE … utf8mb4` avant `migrate` et une stratégie de sauvegarde manuelle planifiée, et corriger le Structural Seed (« sauvegardes quotidiennes » n'est pas acquis chez tous les candidats).

### C3 — FFME : pas d'API publique trouvée, mais une passerelle officielle HelloAsso→myFFME existe et est active pour la saison 2026-2027 — **moyenne**

- **Constat.** L'ossature gère correctement l'incertitude (port FFME en bouchon, AD-5 ; recherche `bmad-deep-recon` avant l'épic 5 ; question ouverte dans l'initiative). Mais la recherche de cette revue apporte une information que le journal ne contient pas et qui oriente le deep-recon.
- **Vérifié (04/11/2026).** ffme.fr, « Rentrée des clubs 2025-2026 » : la FFME annonce « **API MYFFME - HELLOASSO** : une passerelle mise en place pour synchroniser les inscriptions de vos adhérents sur myFFME et les transformer en licencié sur myFFME », avec un formulaire FFME type sur HelloAsso ; myFFME gère saisie de licences, renouvellement en série et import CSV (« licences Helloasso » inclus). ffme.fr, « Préparation de la rentrée des clubs 2026-2027 » (01/09/2026) : « Guide d'utilisation du formulaire HelloAsso 2026-2027 » — la passerelle est toujours d'actualité cette saison. Aucune API publique documentée pour des tiers (vérification de licence existante, enregistrement direct) n'est apparue.
- **Non vérifié.** Modalités précises de la passerelle (champs transmis, délais, erreurs) ; existence d'un accès API myFFME pour clubs ; possibilité de *vérifier* une licence existante autrement qu'en lisant myFFME.
- **Action.** Consigner au journal ; orienter le deep-recon de l'épic 5 vers la piste « passerelle officielle HelloAsso/myFFME » (l'enregistrement de licenciés de R10 pourrait passer par le parcours HelloAsso déjà choisi, sans API fédérale directe) et traiter la vérification d'état de licence comme le risque résiduel numéro un.

### C4 — HelloAsso : contrainte fondatrice jamais vérifiée au journal — confirmée intégralement par cette revue — **moyenne (risque résiduel nul, gap de journal)**

- **Constat.** « HelloAsso, gratuit pour les associations » est une contrainte fondatrice (initiative, décision 24/10) reprise par l'ossature (AD-5, épic 3, R6) — sans aucune vérification web datée dans le journal. C'était le plus grand trou de vérification de l'ossature ; il est comblé et le résultat est favorable.
- **Vérifié (04/11/2026).** info.helloasso.com/modele-economique et centredaide.helloasso.com : services **« 100 % gratuits pour les associations, sans frais ni commission »**, financement uniquement par contributions volontaires des payeurs (optionnelles, refusables) ; ESUS, établissement de paiement agréé ACPR (n° 17678Q) ; 450 000 associations, ~4 Md€ collectés depuis 2009 « intégralement reversés » ; plateforme très vivante (actualités d'octobre 2026). Outil « Adhésion » dédié, adapté au cas du club. dev.helloasso.com / api.helloasso.com : **API v5 publique vivante** — OAuth2 client credentials (tokens 30 min + refresh), sandbox dédiée, notifications/webhooks (paiement autorisé, commande créée, remboursement, contestation…), modèles Organization/Form/Order/Payment (les campagnes « recueillent des adhésions »), HelloAsso Checkout intégrable, SDK Python officiel (HelloAsso/HaApiV5), doc mise à jour (août 2026) ; clé API obtenue directement depuis le compte de l'association (Mon compte > Intégration et API).
- **Non vérifié.** Détail du flux adhésion (redirection, webhooks, reçu) — explicitement différé au raffinement de l'épic 3 par l'ossature, ce qui reste juste.
- **Action.** Consigner la vérification au journal ; rien à changer dans l'ossature (AD-5 et le différé épic 3 restent valables ; l'existence du SDK Python et de la sandbox est un bonus pour l'épic 3).

### C5 — GitHub Actions : gratuit confirmé à cette échelle, mais l'ossature ne dit pas si le dépôt est privé et le modèle de gratuité a changé de forme — **moyenne**

- **Constat.** AD-8 repose sur GitHub Actions sans qu'aucune vérification de gratuité ne figure au journal, et sans préciser dépôt privé ou public.
- **Vérifié (04/11/2026).** docs.github.com (« About billing for GitHub Actions ») : les runners standard dans les **dépôts publics restent gratuits** ; pour un **dépôt privé**, GitHub Free inclut **12 $/mois de compute** (Linux standard à 0,006 $/min ≈ 2 000 min/mois ; runner Linux 1-core à 0,002 $/min ≈ 6 000 min). Une CI Django + service MySQL de quelques minutes par push tient très largement dans ce quota à l'échelle d'un club. Sans moyen de paiement enregistré, l'usage est **bloqué** au-delà du quota (pas de fuite de coût, mais un risque d'arrêt de CI).
- **Non vérifié.** Rien d'essentiel ; noter que le quota est désormais exprimé en dollars de compute, plus en « minutes » — toute doc qui énoncerait « 2 000 minutes gratuites » est périmée.
- **Action.** Préciser dans l'ossature/le journal : dépôt privé (recommandé pour un club) + GitHub Free suffit ; prévoir le moyen de paiement du compte propriétaire pour éviter la coupure de CI.

### C6 — mysqlclient 2.3.0 : pin confirmé (journal à jour), mais un détail de déploiement n'y figure pas : pas de roues Linux — **basse**

- **Vérifié (04/11/2026).** PyPI : 2.3.0 (14/09/2026) toujours la version courante, Production/Stable, Python 3.10-3.15 — le journal du 04/11 est exact. Complément : la release 2.3.0 ne publie que des **roues Windows** (x86-64 et ARM64, cp310-cp315) — le poste de développement du club (Windows) est donc couvert sans compilation ; en revanche, sur Linux (runners GitHub Actions, build PaaS), mysqlclient **se compile depuis les sources** (paquets `python3-dev`, `default-libmysqlclient-dev`, `pkg-config`, `build-essential` ou équivalent buildpack). Doc Django 5.2 reconfirmée : mysqlclient est le pilote **recommandé** (≥ 1.4.3 requis). Support free-threading expérimental (sans impact ici).
- **Non vérifié.** Rien de bloquant.
- **Action.** Prévoir l'étape de compilation dans la CI et le déploiement dès l'épic 1 (une ligne de workflow/apt) ; noter les roues Windows comme facilitateur du dev local.

### C7 — gunicorn et WhiteNoise : affirmés sans version ni vérification — vérifiés maintenant, courants et sains — **basse**

- **Vérifié (04/11/2026).** PyPI : **gunicorn 26.2.0** (24/08/2026 ; versionnement passé au format annuel — 23.0.0 datait de 2024, 24.0.0 en janvier 2026) ; toujours le serveur WSGI de référence, UNIX uniquement (utilisation en production ; `runserver` en local — cohérent). **WhiteNoise 6.12.0** (27/02/2026), Production/Stable, Python 3.10+, classifiers Django 4.2-6.0 (5.2 couvert). Let's Encrypt : inclus et automatique chez **Scalingo** (scalingo.com/pricing, 03/11/2026) ; « free SSL support » sur tous les comptes **PythonAnywhere** (page pricing) ; non relu explicitement chez Clever Cloud.
- **Non vérifié.** Let's Encrypt chez Clever Cloud (affirmé par le journal, pas reconfirméré par cette revue).
- **Action.** Ajouter les pins à la table Stack (gunicorn 26.x, WhiteNoise 6.12.x) ; noter que WhiteNoise ne sert que les statiques — les médias téléversés sont hors périmètre de la première partie, à revoir si des fichiers membres apparaissent.

### C8 — Django 5.2 LTS reconfirmée courante ; horizon 6.2 LTS en avril 2027 puis nouveau calendrier annuel — **basse (contexte)**

- **Vérifié (04/11/2026).** endoflife.date/api/django : 5.2 LTS toujours **la** LTS (5.2.19 sortie le 03/11/2026 ; support étendu jusqu'au 30/04/2028 ; Python 3.10-3.14 — le pin 3.13 est couvert). djangoproject.com/download : la roadmap place **Django 6.2 LTS en avril 2027** (support étendu 04/2030) puis change de politique — « Django 2028 » (janvier 2028), versions annuelles, trois ans de support pour toutes. La prochaine LTS arrive donc *avant* la fin de support de 5.2 : le pin actuel est le bon choix, et la migration 6.2 en 2027 est le plan naturel.
- **Non vérifié.** Plancher MySQL/Python exact de 6.2 (le pin 5.2 n'en dépend pas).
- **Action.** Consigner au journal (date 6.2 + nouveau calendrier) pour la prochaine passe de version.

### C9 — Python 3.13 : reconfirmé raisonnable — **basse**

- **Vérifié (04/11/2026).** endoflife.date/api/python : 3.13.18 (25/10/2026), EOL 31/10/2029 — identique au journal (26/10) ; 3.15 est sortie (09/10/2026) mais le pin 3.13 garde ~3 ans de piste et la maturité voulue. Rien à changer.

### C10 — Greenfield sans starter externe : le risque « défauts du starter » est nul par construction — **basse (positive)**

- **Constat.** L'ossature ne s'appuie sur **aucun starter** (pas de cookiecutter-django ou équivalent) : l'arborescence du Structural Seed est maison (`domaine/` + `application/`). Il n'y a donc pas de défauts de starter à traquer ; en échange, l'épic 1 devra écrire réglages, CI et déploiement à la main — cohérent avec le paradigme hexagonal léger et la contrainte de maintenabilité par des repreneurs peu techniques. Les composants du socle que cette « graine » mobilise (Django, gunicorn, WhiteNoise, mysqlclient) sont tous vérifiés ci-dessus.
- **Action.** Aucune — le point est à conserver comme choix implicite, désormais documenté.

## Couverture des décisions engagées

| Décision de l'ossature | Statut | Source / date |
| --- | --- | --- |
| Django 5.2 LTS | Confirmé (journal 26/10 + reconfirmation 04/11) | endoflife.date, djangoproject.com/download |
| Python 3.13 | Confirmé (journal 26/10 + reconfirmation 04/11) | endoflife.date/api/python |
| MySQL 8.0.11+ / MariaDB 10.5+ (AD-7) | Compatibilité confirmée ; **bornes déployables invalidées** (C1) | docs.djangoproject.com/fr/5.2 ; endoflife.date mysql/mariadb |
| mysqlclient 2.3.0 | Confirmé (journal 04/11) ; complément roues/compilation (C6) | PyPI |
| HelloAsso | **Vérifié pour la première fois — confirmé** (C4) | info.helloasso.com, dev.helloasso.com |
| GitHub Actions (AD-8) | **Vérifié pour la première fois — confirmé, à préciser** (C5) | docs.github.com |
| gunicorn + WhiteNoise | **Vérifiés pour la première fois — confirmés** (C7) | PyPI |
| PythonAnywhere 10 $/mois | Prix confirmé ; propriétés BDD démenties (C2) | pythonanywhere.com, help PA, forum PA |
| Scalingo | Actif, MySQL 8.4, sauvegardes quotidiennes, Let's Encrypt ; prix exact non lisible | scalingo.com, doc.scalingo.com |
| Clever Cloud | Actif, Python + MySQL managé ; versions/prix non confirmés | clever-cloud.com |
| FFME (port bouchon, AD-5) | Incertitude correctement différée ; passerelle HelloAsso→myFFME découverte (C3) | ffme.fr |
| PostgreSQL 17/18, Node 24 (journal) | Sans objet depuis la bascule MySQL et le choix Django | — |

## Ce qui reste non vérifié

- Prix exacts des petits conteneurs Scalingo et Clever Cloud (estimateurs interactifs illisibles en fetch) — déjà noté au journal, différé à l'épic 1.
- Version MySQL proposée par Clever Cloud (et sauvegardes quotidiennes MySQL chez Clever, explicites seulement pour PostgreSQL).
- Disponibilité effective de MySQL 8.4 chez PythonAnywhere (« actively testing » en août 2026, sans date).
- La rumeur « Django 6.1+ abandonne MySQL 8.0 » (utilisateur du forum PA) — à confirmer côté release notes Django avant la migration 6.2.
- Modalités précises de la passerelle myFFME–HelloAsso (champs, erreurs) et tout accès API myFFME pour clubs — objet du deep-recon épic 5.
- Détail du flux HelloAsso (redirection, webhooks, reçu) — différé au raffinement de l'épic 3, conformément à l'ossature.

## Actions recommandées (par ordre)

1. **Corriger AD-7 et la table Stack** (C1) : distinguer plancher de compatibilité Django et cible de déploiement (MySQL 8.4 LTS chez le PaaS ; MariaDB 11.4+/12.3 en local/CI le cas échéant) ; noter que MariaDB n'est offert par aucun des trois PaaS candidats.
2. **Corriger le Structural Seed** (C2) : « sauvegardes quotidiennes » n'est garanti ni chez PythonAnywhere ni (à confirmer) chez Clever — en faire un critère de choix plutôt qu'une propriété acquise.
3. **Alimenter le journal** avec les vérifications de cette revue : HelloAsso (C4), GitHub Actions (C5), gunicorn/WhiteNoise (C7), EOL MySQL/MariaDB (C1), détails PythonAnywhere (C2), passerelle FFME–HelloAsso (C3), horizon Django 6.2 (C8).
4. **Préciser le mode du dépôt GitHub** (privé recommandé) et le compte payeur de la CI (C5).
5. **Orienter le deep-recon épic 5** vers la passerelle officielle HelloAsso→myFFME, en gardant la vérification d'état de licence comme risque résiduel principal (C3).
