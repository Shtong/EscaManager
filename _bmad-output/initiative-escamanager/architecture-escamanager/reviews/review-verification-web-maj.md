---
type: review
reviewer: verification-web-maj (contexte frais)
scope: architecture-escamanager.md — mise à jour du 21/11/2026 : vérification web des trois outils qualité déclarés (ruff 0.17, mypy 2.4, pytest-cov 7.1), revalidation des techniques déjà liées, et confrontation des affirmations de l'ossature au dépôt réel (pyproject.toml, ci.yml)
date: '2026-11-21'
inputs:
  - _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
  - pyproject.toml
  - .github/workflows/ci.yml
  - _bmad-output/initiative-escamanager/architecture-escamanager/reviews/review-verification-web.md
---

# Revue de vérification web — mise à jour du 21/11/2026 de l'ossature

## Verdict

La mise à jour du 21/11/2026 est **globalement conforme** : les trois affirmations de version du bâtisseur sont exactes au jour près sur PyPI (ruff 0.17.6 du 19/11/2026, mypy 2.4.1 du 28/10/2026, pytest-cov 7.1.0 du 21/03/2026 avec exactement les dépendances annoncées `coverage>=7.10.6` et `pytest>=7`), les socles existants tiennent tous (Django 5.2 LTS en sécurité jusqu'en avril 2028, Python 3.13 jusqu'en octobre 2029, MySQL 8.4 LTS jusqu'en 2032, HelloAsso v5 vivante avec SDK Python officiel confirmé, Brevo gratuit avec relais SMTP confirmé) — **un seul écart de fond, côté dépôt et non côté web** : AD-8 et la ligne Outillage affirment que la CI exécute ruff, mypy strict et pytest-cov au seuil, or ni `pyproject.toml` ni `.github/workflows/ci.yml` ne contiennent le moindre début d'instanciation de cet outillage ; l'ossature décrit l'état cible, pas l'état du dépôt. Trois points à surveiller sans être périmés : Python 3.13 vient de quitter la phase bugfix (octobre 2026), une LTS MySQL plus récente (9.7) existe depuis avril 2026, et mysqlclient 2.3.2 a remplacé le 2.3.0 épinglé.

## Méthode et sources

Lecture intégrale de l'ossature (203 lignes, AD-1 à AD-15, conventions, Stack, Structural Seed, Deferred), du `pyproject.toml` et du `ci.yml` du dépôt, puis vérification web le 21/11/2026 de chaque version et propriété affirmée. La revue du 04/11/2026 (`review-verification-web.md`) a été relue pour ne pas re-vérifier ce qui était déjà frais et pour assurer la continuité des constats (C1 à C6).

Sources consultées le 21/11/2026 :

- **PyPI** : `pypi.org/project/ruff/`, `pypi.org/project/mypy/`, `pypi.org/project/pytest-cov/` (+ JSON `pypi.org/pypi/pytest-cov/7.1.0/json` pour `requires_dist`), `pypi.org/pypi/mysqlclient/2.3.0/json`, `pypi.org/project/mysqlclient/`, `pypi.org/project/pytest-django/`, `pypi.org/project/django-stubs/`, `pypi.org/project/dj-database-url/`, `pypi.org/project/gunicorn/`, `pypi.org/project/whitenoise/`.
- **Sites officiels** : `djangoproject.com/download`, `docs.djangoproject.com/en/5.2/ref/databases/`, `devguide.python.org/versions/`, `dev.mysql.com/doc/refman/8.4/en/mysql-releases.html`.
- **Hébergeurs et modèles de support** : `endoflife.date/mysql` (+ miroir eol.vallis.info, màj 31/10/2026), `doc.scalingo.com/databases/mysql/guides/backing-up` et `/databases/about/backup-policies`, `clever.cloud/fr/product/mysql` et `clever.cloud/developers/doc/deploy/databases/mysql`, `help.pythonanywhere.com/pages/MySQLBackupRestore`.
- **Paiement et courriels** : `dev.helloasso.com` (docs api-overview, sdk, llms.txt), `github.com/HelloAsso/helloasso-python`, `ffme.fr/preparation-de-la-rentree-des-clubs-2026-2027/`, courrier de rentrée 2026-2027 (hdf.ffme.fr, 09/2026), `brevo.com/pricing/` et `brevo.com/pricing.md` (généré le 29/09/2026 depuis l'API tarifaire officielle), `help.brevo.com` (limites du plan Free), `brevo.com/free-smtp-server/`, `developers.brevo.com/docs/smtp-integration`.
- **CI** : `github.com/pricing`, `docs.github.com/en/billing/reference/product-usage-included`, `docs.github.com/en/actions/concepts/billing-and-usage`, annonce « Pricing changes for GitHub Actions » (15/12/2025).

## Tableau récapitulatif

| Élément | Affirmé (ossature, 21/11/2026) | Constaté (21/11/2026) | Verdict |
| --- | --- | --- | --- |
| ruff | 0.17 (lint + format, CI) | 0.17.6, publiée le 19/11/2026, MIT, config `pyproject.toml`, Python 3.13 OK | **conforme** |
| mypy | 2.4 (strict, `domaine/` uniquement) | 2.4.1, publiée le 28/10/2026, MIT, roues cp313 | **conforme** (exclusion d'`application/` cohérente) |
| pytest-cov | 7.1 (seuil sur le domaine) | 7.1.0 du 21/03/2026, MIT, `coverage[toml]>=7.10.6`, `pytest>=7` | **conforme** |
| Django | 5.2 LTS | 5.2.19 ; support étendu jusqu'en avril 2028 | conforme, **à surveiller** |
| Python | 3.13 | phase *security* depuis 10/2026 ; EOL 10/2029 | conforme, **à surveiller** |
| MySQL | 8.4 LTS (cible) | 8.4.13 ; support jusqu'au 30/04/2032 ; LTS plus récente : 9.7 (04/2026) | conforme, **à surveiller** |
| mysqlclient | 2.3.0 | 2.3.0 du 14/09/2026, roues cp313 ; version courante : 2.3.2 (18/11/2026) | conforme, **pin à rafraîchir** |
| HelloAsso | API v5, OAuth2, sandbox, webhooks, SDK Python officiel | doc vivante ; `github.com/HelloAsso/helloasso-python` référencé par la doc officielle | **conforme** |
| Passerelle myFFME | active pour 2026-2027 | confirmée par ffme.fr (01/09/2026) et le courrier de rentrée 2026-2027 | **conforme** |
| Brevo | offre gratuite (relais SMTP) | plan Free : 300 emails/jour, SMTP transactionnel inclus | **conforme** |
| CI outillée (AD-8) | ruff + mypy strict + pytest-cov au seuil dans la CI | `ci.yml` : aucune de ces étapes ; `pyproject.toml` : aucune de ces deps | **non instancié dans le dépôt** (écart principal) |

---

## 1. Les trois outils déclarés le 21/11/2026

### 1.1 ruff 0.17 — **conforme**

- **Affirmation du bâtisseur** : ruff 0.17.6 publié le 19/11/2026, utilisé pour lint + format avec configuration dans `pyproject.toml`.
- **Vérifié (21/11/2026, PyPI `pypi.org/project/ruff/`)** : la dernière version est **0.17.6**, « Released: Nov 19, 2026 » (données PyPI vérifiées le 19/11/2026), publication par *trusted publishing* (uv 0.13.9). L'affirmation est exacte au jour près.
- **Maintenance et licence** : projet Astral, Development Status « 5 - Production/Stable », 4 mainteneurs, licence **MIT**. Roues disponibles pour Windows x86-64/ARM64, Linux, macOS — le poste Windows du club est couvert.
- **Compatibilité projet** :
  - *lint + format* : confirmé — `ruff check` et `ruff format`, parité drop-in avec Flake8/isort/Black annoncée dans le README PyPI ; une action GitHub officielle existe (`astral-sh/ruff-action@v3`).
  - *configuration dans `pyproject.toml`* : confirmé textuellement — « Ruff can be configured through a `pyproject.toml`, `ruff.toml`, or `.ruff.toml` file… each section header should be prefixed with `tool.ruff` ». Rien à installer d'autre.
  - *Python 3.13* : confirmé — classifiers Python 3.7 à 3.15 (le projet vise même la compatibilité 3.15) ; ruff analyse le code *pour* une version cible, qu'il faudra fixer à la story socle (`target-version = "py313"` sous `[tool.ruff]` ; le défaut de la doc est `py311`).
- **Remarque** : ruff 0.17.6 remplace ruff 0.17.5 et antérieures ; l'ossature n'épingle pas de version précise, la ligne Stack « ruff 0.17 » est donc correcte en l'état. À la story socle, épingler (ex. `ruff==0.17.6`) pour des builds reproductibles, comme le fait déjà `mysqlclient==2.3.0`.

### 1.2 mypy 2.4 (strict, `domaine/`) — **conforme**, et l'exclusion d'`application/` est cohérente

- **Affirmation du bâtisseur** : mypy 2.4.1 publié le 28/10/2026, typage strict du paquet de domaine uniquement.
- **Vérifié (21/11/2026, PyPI `pypi.org/project/mypy/`)** : la dernière version est **2.4.1**, « Released: Oct 28, 2026 » — exact au jour près. Licence **MIT**, Development Status « 5 - Production/Stable », 12 mainteneurs, requires-python `>=3.10`.
- **Compatibilité Python 3.13** : confirmée — roues cp313 Windows/Linux/macOS (y compris cp313t *free-threading*). mypy 2.4.1 s'exécute donc directement sur l'interpréteur 3.13 de la CI.
- **Typage strict d'un paquet pur stdlib** : cohérent et immédiat — `domaine/` n'importe que la bibliothèque standard (AD-1), donc aucun stub externe n'est requis pour le passer en strict. C'est précisément le sous-ensemble où mypy strict coûte le moins et rapporte le plus.
- **L'exclusion d'`application/` est-elle cohérente avec ce que django-stubs imposerait ? Oui.** Vérifié le 21/11/2026 sur PyPI `pypi.org/project/django-stubs/` (version courante **6.1.2**, publiée le 05/10/2026, MIT) :
  - django-stubs exige son **plugin mypy** pour tout code Django (« This package contains type stubs and a custom mypy plugin… it does not make any sense to use this project without mypy ») : sans plugin, les modèles, managers, `QuerySet` et relations inversées produisent des erreurs massives en mode strict. Typer `application/` en strict *sans* django-stubs serait donc ingérable ; typer *avec* django-stubs est possible mais apporte une dépendance et une configuration supplémentaires (`plugins = ["mypy_django_plugin.main"]`, `django_settings_module`).
  - Matrice de compatibilité publiée par django-stubs : **6.1.2 accepte mypy 1.13 à 2.4**, mais avec Django 6.1 en cible et **Django 5.2 en « support partiel »** ; les versions de django-stubs qui supportent *complètement* Django 5.2 (série 5.2.x, dernière 5.2.9 du 20/01/2026) n'acceptent que mypy 1.13–1.19 — incompatible avec le mypy 2.4 retenu.
  - Conclusion : le couple mypy 2.4 + Django 5.2 n'a aujourd'hui qu'un support *partiel* du côté de django-stubs. Le choix de l'ossature — strict sur `domaine/` maintenant, typage de `application/` avec django-stubs **différé** (dernier point du Deferred) — est donc non seulement cohérent avec la pratique recommandée, mais c'est aussi le seul qui ne force pas à rétrograder mypy. À re-vérifier si le club demande un jour le typage de `application/` : d'ici là, django-stubs 6.x aura probablement consolidé le support 5.2/6.x.

### 1.3 pytest-cov 7.1 — **conforme**, seuil `--cov-fail-under` fonctionnel en CI

- **Affirmation du bâtisseur** : pytest-cov 7.1.0 publié le 21/03/2026, requiert `coverage >= 7.10.6` et `pytest >= 7`.
- **Vérifié (21/11/2026, PyPI + JSON `requires_dist` de 7.1.0)** : la dernière version est **7.1.0**, publiée le 21/03/2026 — exact. `requires_dist` lu directement : **`coverage[toml]>=7.10.6`**, **`pluggy>=1.2`**, **`pytest>=7`** — l'affirmation du bâtisseur est exacte, y compris le plancher coverage. Licence **MIT**, mainteneur Ionel Cristian Mărieș, requires-python `>=3.9`, classifiers 3.9–3.14.
- **Compatibilité pytest 8.x** : oui — le plancher est `pytest>=7`, donc 8.x est dedans ; le changelog 6.2.0/6.2.1 (juin 2025) corrige d'ailleurs spécifiquement les interactions avec **pytest 8.4** (`filterwarnings=error`). Le `pyproject.toml` du club exige `pytest>=8.0` : compatible.
- **Compatibilité pytest-django 4.9** : oui — vérifié le 21/11/2026 sur PyPI : pytest-django est aujourd'hui en **4.14.0** (10/08/2026, BSD-3) et déclare « Django: 5.2, 6.0… pytest: >=7.0 », classifiers Django 5.2 et Python 3.13/3.14. La borne du dépôt `pytest-django>=4.9` résout vers 4.14.0, qui supporte Django 5.2. (La 4.9.0 seule, du 02/09/2024, prédatait Django 5.2 — c'est bien la résolution de borne `>=4.9` qui compte, et elle est saine.)
- **`--cov-fail-under` en CI** : fonctionnel — l'option existe depuis pytest-cov 2.0.0, respecte la précision de la configuration coverage depuis 6.0.0, et **7.1.0 corrige un défaut de cohérence du total** (« Fixed total coverage computation to always be consistent, regardless of reporting settings… can make --cov-fail-under behave different depending on reporting options », issue #641) : le seuil en CI est donc plus fiable qu'il ne l'a jamais été. Utilisable tel quel : `pytest --cov=domaine --cov-fail-under=SEUIL`.
- **À noter** (sans incidence ici) : pytest-cov 7.0.0 (09/09/2025) a **supprimé la mesure des sous-processus** par fichier `.pth` — remplacée par l'option `patch = subprocess` de coverage. Le projet teste le domaine sans base ni sous-processus : aucun impact.

---

## 2. Revalidation des techniques déjà liées avant cette mise à jour

### 2.1 Django 5.2 LTS — **conforme, à surveiller**

- **Vérifié (21/11/2026, `djangoproject.com/download`)** : 5.2 LTS en est à **5.2.19** ; fin de support *mainstream* le 03/12/2025 (passée), **fin de support étendu (sécurité) en avril 2028**. Les versions courantes sont 6.0.10 et 6.1.3 ; la prochaine LTS est **6.2 (avril 2027)** — Django changera ensuite de modèle (versions calendaires « 2028 », « 2029 »…, chaque version recevant trois ans de support).
- Donc au 21/11/2026 : Django 5.2 est **toujours la LTS courante** (la seule série LTS supportée jusqu'en 2028), et le pin du dépôt `Django>=5.2,<5.3` est cohérent. Nuance honnête : depuis décembre 2025, 5.2 ne reçoit plus que des correctifs de sécurité et de perte de données — pour un produit dont la première saison pleine sera 2027/2028, la fenêtre couvre l'horizon, mais la migration 6.2 LTS (avril 2027 → avril 2030) est à inscrire à l'horizon 2027.
- **Plancher MySQL/MariaDB (AD-7) fondé** — vérifié (21/11/2026, `docs.djangoproject.com/en/5.2/ref/databases/`) : « Django supports MySQL 8.0.11 and higher », « Django supports MariaDB 10.5 and higher », mysqlclient est « the recommended choice » (≥ 1.4.3 requis), et la création de base recommandée est `CHARACTER SET utf8mb4`. Chaque affirmation technique d'AD-7 sur le backend est confirmée mot pour mot par la doc officielle.

### 2.2 Python 3.13 — **conforme, à surveiller**

- **Vérifié (21/11/2026, `devguide.python.org/versions`)** : Python 3.13 (release 07/10/2024, PEP 719) est en phase **security** — la phase bugfix (deux ans depuis PEP 719, contre 18 mois avant 3.13) s'est achevée en **octobre 2026** ; fin de vie **octobre 2029**. Les versions en maintenance active sont 3.14 (bugfix, EOL 10/2030) et 3.15 (release du 09/10/2026, bugfix, EOL 10/2031).
- Verdict : 3.13 reste **pleinement supporté** (correctifs de sécurité jusqu'en octobre 2029) et tout l'outillage vérifié le couvre (roues cp313 de mypy/mysqlclient, classifiers 3.13 de ruff/pytest-cov/gunicorn/whitenoise/pytest-django). La CI (`python-version: "3.13"`) et `requires-python = ">=3.13"` sont cohérents. Mais un projet qui démarre aujourd'hui peut légitimement viser **3.14** (bugfix jusqu'en octobre 2027, EOL octobre 2030) pour trois années de maintenance complète. Décision à arbitrer à la story socle — aucune urgence, les deux tiennent la fenêtre 2026-2029.

### 2.3 MySQL 8.4 LTS — **conforme, à surveiller**

- **Vérifié (21/11/2026, `endoflife.date/mysql` màj 31/10/2026, doc MySQL refman 8.4, guides PaaS)** :
  - MySQL **8.4 LTS** : GA le 30/04/2024, dernier patch **8.4.13** (20/10/2026), Premier support jusqu'au **30/04/2029**, Extended support jusqu'au **30/04/2032**. La cible de l'ossature est donc une LTS vivante et stable — la série ne reçoit que des correctifs, sans retrait de fonctionnalités ni changement de format.
  - **Fait nouveau depuis la rédaction initiale de l'ossature** : la LTS suivante, **MySQL 9.7 LTS**, est sortie le **21/04/2026** (dernier patch 9.7.4 du 20/10/2026, Extended jusqu'au 30/04/2034) ; MySQL est ensuite passé aux versions calendaires (innovation 26.7, 26.10). MySQL 8.0 est EOL depuis le 30/04/2026 (8.0.46, déjà relevé par C1 de la revue du 04/11).
  - La doc MySQL précise que la montée de version se fait **une LTS à la fois** (8.4 → 9.7, sans saut) : la cible 8.4 n'induit aucun verrouillage.
- **Côté PaaS (vérifié le 21/11/2026)** : Clever Cloud propose MySQL **8.4.10** et **9.7.1** (8.0.46 marqué EOL dans leur doc — cohérent) ; Scalingo documente les mises à niveau en un clic vers 8.4. La phrase AD-7 « la version 8.x LTS proposée par l'hébergeur » reste exacte. À surveiller : à l'horizon Premier 2029, le choix 8.4 vs 9.7 se reposera ; l'épic 1 (choix d'hébergeur) est le bon moment pour le re-peser.

### 2.4 mysqlclient 2.3.0 — **conforme, pin à rafraîchir**

- **Vérifié (21/11/2026, PyPI + JSON de la release 2.3.0)** :
  - **2.3.0 existe et date bien du 14/09/2026** (`upload_time` 2026-09-14T15:38), requires-python `>=3.10`, Development Status « 5 - Production/Stable », mainteneur Inada Naoki, licence **GPL-2.0-or-later**.
  - **Compatible Python 3.13** : la release publie des roues cp310 à cp315 pour Windows (x86-64 et ARM64), dont `mysqlclient-2.3.0-cp313-cp313-win_amd64.whl` — le poste de développement Windows du club est couvert sans compilation ; sur Linux (CI, PaaS), compilation depuis les sources avec `default-libmysqlclient-dev` + `pkg-config`, déjà prévue dans le `ci.yml` (étape apt identique dans les deux jobs).
  - **Nouveauté depuis la vérification du 04/11** : la version courante est désormais **2.3.2** (18/11/2026, publication avec *full provenance*, roues cp310-cp315 Windows). Le pin `mysqlclient==2.3.0` du `pyproject.toml` reste fonctionnel ; deux correctifs mineurs sont disponibles.
  - **Licence** : GPL-2.0-or-later — open-source et gratuite, donc conforme à la règle « toute dépendance nouvelle est open-source et gratuite » ; copyleft sans incidence pratique pour un service web hébergé (pas de redistribution binaire), mais le fait mérite une ligne dans le guide du repreneur bénévole.
- **Verdict** : conforme (affirmation exacte), action mineure : passer le pin à 2.3.2 à la story socle après lecture du changelog.

### 2.5 HelloAsso — API v5 — **conforme** (vivante, documentée, SDK Python officiel confirmé)

- **Vérifié (21/11/2026, `dev.helloasso.com`)** : la documentation de l'**API v5** est en ligne et fraîche — page « API Overview » : base `https://api.helloasso.com/v5`, sandbox `https://api.helloasso-sandbox.com/v5` (organisation de test sur helloasso-sandbox.com, cartes bancaires virtuelles), **OAuth 2.0** (`client_credentials` puis `refresh_token`, jeton d'accès 30 min, refresh 1 mois), **Checkout** (`POST …/checkout-intents`, `redirectUrl` valide 15 min, `returnUrl`, `metadata` jusqu'à 20 000 caractères), **webhooks** (« Configure webhook notifications for Order and Payment events »), pagination par `continuationToken`. Le `llms.txt` du site montre une référence complète (Checkout, formulaires, commandes, paiements).
- **« SDK Python officiel » (AD-5) — confirmé** : la page officielle `dev.helloasso.com/docs/sdk` (mise à jour 24/10/2025) liste trois kits officiels, dont **PYTHON : `github.com/HelloAsso/helloasso-python`** — dépôt sous l'organisation GitHub HelloAsso, dernière activité le 19/02/2026. L'affirmation d'AD-5 (« OAuth2, webhooks, bac à sable, SDK Python officiel — vérifiée le 04/11/2026 ») est donc toujours exacte et mieux sourcée qu'au 04/11.
- **Passerelle myFFME (Deferred, épic 5) — confirmée active pour 2026-2027** : ffme.fr « Préparation de la rentrée des clubs 2026-2027 » (01/09/2026) : « Guide d'utilisation du formulaire HelloAsso 2026-2027 : la nouvelle version est disponible sur vos comptes HelloAsso » ; courrier de rentrée 2026-2027 (sept. 2026) : « Une passerelle sera mise en place pendant le mois de juin 2026 pour synchroniser les inscriptions de vos adhérents sur myFFME et les transformer en licencié ». Le Q&R du webinaire myFFME 2025-2026 confirme : « Concernant l'API, est-ce qu'il est possible de l'utiliser dans un autre cadre que HelloAsso ? Non, ce n'est pas possible » — ce qui renforce la prémisse d'AD-5 et du Deferred (« aucune API publique tierce ») : la passerelle HelloAsso→myFFME reste la seule voie automatisée fédérée.

### 2.6 Brevo — **conforme** (offre gratuite transactionnelle toujours disponible)

- **Vérifié (21/11/2026, `brevo.com/pricing/`, `brevo.com/pricing.md`, `help.brevo.com`, `developers.brevo.com`)** :
  - Le plan **Free** existe toujours : « Free forever, no credit card needed » ; dans le `pricing.md` généré le 29/09/2026 depuis l'API tarifaire officielle, le plan `marketing-plan-free` apparaît « Included » dans toutes les devises.
  - **Quota** : « The Free plan includes 300 email sends per day » (FAQ Brevo), non cumulatif ; au-delà, jusqu'à 1 000 emails *transactionnels* sont mis en file d'attente de réessai. Ce volume convient à l'échelle du club.
  - **Relais SMTP inclus dans le plan gratuit** : confirmé explicitement — page « Free SMTP server » : « Try SMTP on our forever free plan with a sending limit of 300 emails a day » ; tableau comparatif des offres : « Transactional email (API/SMTP)… Included » sur la colonne Free ; `developers.brevo.com/docs/smtp-integration` documente le branchement (ports 587/2525/465, clé SMTP dédiée).
- L'affirmation de la Stack « Brevo — offre gratuite (relais SMTP) » est donc **conforme en chaque mot**, avec le quota de 300/jour comme unique paramètre à garder en tête.

---

## 3. Affirmations non tenues par le dépôt, ou à nuancer

### 3.1 AD-8, Outillage et Stack déclarent un outillage que le dépôt n'a pas encore — **écart principal (haute)**

- **Constat.** Trois endroits de l'ossature affirment que la qualité est exécutée par la CI : AD-8 (« chaque fusion traverse GitHub Actions — … lint et format (ruff), typage du domaine (mypy strict), couverture du domaine au seuil (pytest-cov) »), la ligne Outillage des conventions (« ruff… et mypy… s'exécutent dans la CI ; couverture mesurée par pytest-cov avec un seuil minimal sur le domaine, valeur dans `pyproject.toml` et relevable »), et la Stack (« ruff 0.17 · mypy 2.4 · pytest-cov 7.1 »).
- **Confrontation au dépôt (lu le 21/11/2026)** :
  - `pyproject.toml` — dépendances dev : `pytest>=8.0`, `pytest-django>=4.9`, **et c'est tout**. Ni ruff, ni mypy, ni pytest-cov. Aucune section `[tool.ruff]`, `[tool.mypy]`, ni `[tool.coverage.report]` avec un seuil `fail_under`.
  - `.github/workflows/ci.yml` — deux jobs : `domaine` (garde d'imports + tests, sans base) et `application` (MySQL 8.4 + `makemigrations --check --dry-run` + tests). **Aucune étape ruff, aucune étape mypy, aucun drapeau `--cov`/`--cov-fail-under`.**
- **Interprétation.** Ce n'est pas du *périmé*, c'est de l'*en avance* : l'ossature du 21/11/2026 décrit l'état cible que le dépôt n'a pas encore rejoint. Mais au jour où AD-8 dit « la CI est l'autorité, chaque fusion traverse lint, typage et couverture », la moitié de cette phrase n'est vraie d'aucun fichier du dépôt. À noter que la véracité du reste d'AD-8 est confirmée : garde d'imports (AD-1/AD-3) et tests du domaine sans base, tests de l'application sur MySQL 8.4 (cohérent avec la cible AD-7), vérification des migrations via `--check --dry-run` — tout cela est bien dans le `ci.yml`.
- **Action.** À la story socle (AGENTS.md : « la story socle crée `pyproject.toml` et la CI » — les deux fichiers existent déjà, il faut donc les *compléter*) : ajouter `ruff`, `mypy`, `pytest-cov` aux dépendances dev ; instancier `[tool.ruff]` (avec `target-version = "py313"`), `[tool.mypy]` (strict, périmètre `domaine/`), et un seuil `[tool.coverage.report] fail_under` ; ajouter au `ci.yml` les étapes `ruff check` + `ruff format --check`, `mypy domaine/`, et `pytest tests/domaine --cov=domaine --cov-fail-under=…`. D'ici là, traiter la ligne Stack comme une déclaration d'intention.

### 3.2 Sauvegardes PaaS — exact, mais réservé aux plans payants — **moyenne**

- **Vérifié (21/11/2026)** :
  - **Scalingo** (`doc.scalingo.com`) : « Starter and Business plans of Scalingo for MySQL® include automated and managed backups », quotidiens (« Periodic backups are done on a daily basis », rétention 7 jours + 4 semaines en Starter) ; le blog Scalingo précise que « les sauvegardes périodiques ne s'appliquent pas aux plans Gratuit/Sandbox ». L'affirmation du Structural Seed (« quotidiennes et incluses chez Scalingo ») est donc exacte **pour les plans payants** — le club devra prendre au minimum un Starter.
  - **Clever Cloud** (`clever.cloud/fr/product/mysql` et doc developers) : « une sauvegarde gratuite est effectuée chaque nuit par défaut, avec une rétention de sept jours » ; mais « DEV plan is free, for testing purposes only. It has… **no backups**… nor SLA ». Même nuance : quotidien et inclus **hors plan DEV gratuit**. (Au passage, la doc confirme les versions proposées : MySQL 8.4.10 et 9.7.1 — cohérent avec la cible 8.4 LTS.)
  - **PythonAnywhere** (`help.pythonanywhere.com/pages/MySQLBackupRestore`) : la sauvegarde se fait **manuellement par `mysqldump`** (ou via une tâche planifiée configurée à la main) — l'affirmation « manuelles (mysqldump) sur PythonAnywhere » est **exacte**.
- **Action.** Préciser dans le Structural Seed « sauvegardes quotidiennes incluses (plans payants uniquement) » pour que le choix d'épic 1 pèse cette donnée — le différé actuel (« ce fait pèse dans le choix de l'épic 1 ») reste valable.

### 3.3 « GitHub Actions est gratuit dans les deux cas » — exact en pratique, avec un quota sur privé — **basse**

- **Vérifié (21/11/2026, `github.com/pricing`, docs GitHub billing)** : dépôt **public** → runners standard gratuits, sans plafond. Dépôt **privé** → GitHub Free inclut **12 $/mois de compute** (soit ~2 000 minutes de runner Linux standard à 0,006 $/min, ~6 000 minutes en Linux 1-core) ; l'usage se déduit de cette enveloppe et la CI est bloquée (pas facturée) au-delà sans moyen de paiement. Les prix des runners ont en outre baissé jusqu'à -39 % au 01/01/2026 (annonce du 15/12/2025). Une CI à deux jobs courts avec service MySQL tient très largement dans l'enveloppe : l'affirmation du Deferred est donc **exacte en pratique**, à condition de noter (comme la revue du 04/11, C5) que le quota privé est exprimé en dollars de compute depuis le 28/10/2026, plus en « minutes ».

### 3.4 Formulation ambiguë d'AD-7 — **basse**

- « plancher de compatibilité Django 8.0.11+ / MariaDB 10.5+ » : le fond est confirmé par la doc Django 5.2 (MySQL 8.0.11+, MariaDB 10.5+), mais « Django 8.0.11 » se lit comme une version de Django. Reformuler en « plancher de compatibilité (exigences du backend Django) : MySQL 8.0.11+ / MariaDB 10.5+ ». Cosmétique, mais l'ossature est le document de référence des bénévoles.

### 3.5 Dépendances mineures du `pyproject.toml` — **conformes**

- Vérifié le 21/11/2026 sur PyPI : `gunicorn>=23.0` → courant **27.0.1** (12/11/2026, MIT, Python 3.13, WSGI toujours au cœur, ASGI/HTTP-2 en bêta) ; `whitenoise>=6.7` → courant **6.12.0** (27/02/2026, MIT, classifiers Django 5.2, Python 3.13) ; `dj-database-url>=2.2` → courant **3.1.2** (19/02/2026, BSD-3, classifiers Django 5.2/6, Python 3.13). Les bornes souples résolvent toutes vers des versions compatibles Django 5.2 + Python 3.13. Aucune affirmation de version précise dans l'ossature : rien à corriger. Seule réserve : gunicorn a changé trois fois de majeure depuis 23.0 — au moment du verrouillage (story socle), épingler et lire le changelog.

### 3.6 Points restant volontairement non vérifiés — **conformes à leur statut « différé »**

- Le prix du petit conteneur Scalingo et le mode public/privé du dépôt sont déclarés « à confirmer » par l'ossature : rien à vérifier aujourd'hui, la revue du 04/11 (C5) et la présente nuance (3.3) fournissent les données pour l'épic 1.
- Le détail du flux HelloAsso (redirection, webhooks, reçu, sandbox) : l'API Overview vérifiée confirme que tous ces éléments existent et sont documentés ; l'ossature a raison de différer leur assemblage au raffinement de l'épic 3.
- La licence GPL de mysqlclient est conforme à la règle « open-source et gratuite » (2.4) — à documenter pour le repreneur, pas à changer.

---

## Actions recommandées

1. **Story socle (prioritaire, débloque AD-8)** : instancier l'outillage déclaré — deps dev `ruff`/`mypy`/`pytest-cov`, sections `[tool.ruff]` (`target-version = "py313"`), `[tool.mypy]` (strict, `domaine/`), seuil `[tool.coverage.report] fail_under`, et les trois étapes correspondantes dans `ci.yml` (`ruff check` + `ruff format --check`, `mypy domaine/`, `pytest … --cov=domaine --cov-fail-under=…`).
2. Passer le pin `mysqlclient==2.3.0` à `==2.3.2` (18/11/2026) après lecture du changelog.
3. Arbitrer Python 3.13 (security jusqu'en 10/2029) vs 3.14 (bugfix jusqu'en 10/2027, EOL 10/2030) à la story socle — les deux tiennent la fenêtre du projet.
4. Noter dans l'horizon : MySQL 9.7 LTS (04/2026, support 2034) existe ; montée obligatoirement 8.4 → 9.7, sans saut ; Django 6.2 LTS attendue en avril 2027 — inscrire ces jalons dans la revue d'épic 1 sans changer les cibles actuelles.
5. Préciser le Structural Seed : « sauvegardes quotidiennes incluses chez Scalingo et Clever Cloud (plans payants uniquement ; pas de sauvegarde sur les plans DEV/Sandbox gratuits) » ; reformuler le plancher AD-7 (3.4).
6. Consigner au journal : ruff 0.17.6 (19/11/2026), mypy 2.4.1 (28/10/2026), pytest-cov 7.1.0 (21/03/2026, `coverage>=7.10.6`, `pytest>=7`), SDK Python officiel HelloAsso confirmé, passerelle myFFME active 2026-2027, Brevo Free 300 emails/jour avec SMTP transactionnel inclus.
