---
title: 'Socle et première page en production'
type: 'feature'
ticket: 1
created: '2026-11-15'
status: 'built'
baseline_revision: '1fbf7ba58d2214e6d9a801cce8cd1d2f43f4c010'
route: 'full'
route_source: 'auto'
risk: 'medium'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['H:/EscaManager/_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** le dépôt ne contient aucun code : rien ne prouve que la chaîne domaine → dépôt ORM → MySQL → page fonctionne, et les huit stories de l'épic n'ont pas de socle pour livrer.

**Approach:** balle traceuse de bout en bout : pyproject installable, paquet pur `domaine/` portant sa première lecture, projet Django minimal (`config` + `comptes`) servant la page d'accueil depuis MySQL, CI GitHub Actions en deux jobs (domaine sans base, application sur MySQL, garde d'imports). Exécution strictement locale pendant les premières phases du développement : le code reste déployable sans modification (WSGI standard, configuration exclusive par variables d'environnement, AD-15) et la mise en production est différée. Seul le dépôt GitHub public (nécessaire à la CI) relève d'une étape humaine.

**Decision (2026-11-15):** la première lecture du domaine est le décompte des comptes — requête `compter_comptes` sur l'entité `Compte` (app `comptes`, catalogue AD-9), servie par la page d'accueil.

**Decision (2026-11-15, renégociation humaine) :** pour réduire les coûts, rien n'est hébergé pendant les premières phases — l'application s'exécute en local uniquement ; la mise en production Scalingo (compte, application, addon MySQL, prix du petit conteneur) et le compte Brevo sont reportés au registre du travail différé.

## Boundaries & Constraints

**Always:** règles AD-1 à AD-15 de l'ossature (notamment AD-1 domaine pur vérifié par test d'imports en CI, AD-2 lectures par le domaine, AD-7 MySQL utf8mb4 et migrations seules, AD-8 CI obligatoire avant fusion, AD-15 neutralité d'hébergement) ; symboles, apps et URLs en français snake_case ; textes d'interface en français direct, sans catalogue i18n ; secrets exclusivement en variables d'environnement ; chaque page utilisable sans JavaScript ; versions décidées : Python 3.13, Django 5.2 LTS, MySQL 8.4, mysqlclient 2.3.0.

**Never:** pas de SQLite, même en local ; pas d'authentification, de sessions ni d'admin (stories 1.2 et 1.4) — le modèle User par défaut de Django ne doit pas être migré avant que 1.2 tranche ; pas d'apps `saisons`/`adhesions`/`membres`/`federation` (leurs épics) ; pas de SQL brut ni de dépendance propre à un hébergeur ; pas de mise en production, de compte Scalingo ni de compte Brevo dans cette story (différés au registre du travail) ; pas d'envoi réel de courriel (backend console en local).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Accueil, base vide | GET `/`, zéro ligne | 200, page rendue avec « 0 » | sans erreur |
| Accueil, base peuplée | GET `/`, N lignes | 200, N affiché depuis MySQL | sans erreur |
| Variable obligatoire absente | démarrage sans `SECRET_KEY` ou `DATABASE_URL` | refus de démarrer, message français explicite | échec rapide au lancement |
| Base injoignable | GET `/`, MySQL absente | erreur 500 standard Django, journalisée | jamais d'exception avalée |
| Garde d'imports | import non-stdlib dans `domaine/` | test en échec, fichier et module nommés | liste blanche `sys.stdlib_module_names` |

</frozen-after-approval>

## Code Map

- Terrain vierge : aucun fichier applicatif ; tout est à créer. Structure cible : `domaine/{entites,ports,services}` , `application/{config,comptes,gabarits,static}`, `tests/`.
- `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md` — ossature AD-1 à AD-15, pile, structure : à consulter, jamais modifier.
- `.gitignore` — existe (ignore `_bmad/render/`) : étendre, ne pas retirer cette ligne.
- `_bmad/`, `_bmad-output/`, `AGENTS.md`, `.agents/` — socle BMad : ne pas toucher.
- Épic et decisions : `tickets/epic-comptes-permissions/epic-comptes-permissions.md` (dépôt GitHub public, Scalingo piste, Brevo, balle traceuse).

## Tasks & Acceptance

**Execution:**
- [ ] `pyproject.toml` — créer : paquets `domaine` et `application`, deps (Django>=5.2,<5.3, mysqlclient 2.3.0, gunicorn, whitenoise, dj-database-url), extra `dev` (pytest, pytest-django), config pytest — dépôt installable (`pip install -e .[dev]`)
- [ ] `domaine/entites/compte.py` — entité `Compte` minimale (courriel), sans logique d'auth — première entité du catalogue AD-9
- [ ] `domaine/ports/depots.py` — port `DepotComptes` (interface) avec `compter() -> int` — maison unique des interfaces (AD-2, AD-5)
- [ ] `domaine/requetes.py` — lecture `compter_comptes(depot)` — toute lecture passe par le domaine (AD-2)
- [ ] `application/config/settings.py` — réglages : variables d'environnement seules (petit chargeur `.env` stdlib pour le local), `DATABASE_URL` via dj-database-url + OPTIONS `utf8mb4`, `SECRET_KEY` obligatoire, `DEBUG` faux par défaut, `ALLOWED_HOSTS`, fuseau Europe/Paris, `LANGUAGE_CODE` fr, INSTALLED_APPS minimale (`staticfiles`, `application.comptes`), WhiteNoise, dossiers de gabarits — AD-7, AD-15
- [ ] `application/config/urls.py` — route `/` vers la vue `accueil` (name `accueil`) — URLs françaises
- [ ] `application/config/wsgi.py` et `manage.py` — point d'entrée WSGI standard + `manage.py` à la racine — AD-15 et commandes de développement
- [ ] `application/config/composition.py` — fabrique `depot_comptes()` — câblage port/adaptateur uniquement dans `config` (AD-10)
- [ ] `application/comptes/modeles.py` + `application/comptes/migrations/0001_initial.py` — modèle `CompteDjango` (courriel unique), migration générée par `makemigrations`, aucune règle métier — persistance propriétaire `comptes` (AD-9, AD-2)
- [ ] `application/comptes/depots.py` — `DepotComptesDjango` implémente le port via l'ORM — AD-2
- [ ] `application/comptes/vues.py` — vue `accueil` : `compter_comptes(depot)` puis rendu — lecture par le domaine
- [ ] `application/gabarits/base.html`, `application/gabarits/accueil.html`, `application/static/css/accueil.css` — gabarits français, responsives, sans JavaScript (AD-6) ; maquette minimale en attendant le passage UX
- [ ] `tests/test_imports_domaine.py` — garde AD-1 : parcours AST de `domaine/`, liste blanche `sys.stdlib_module_names`, échec nommant fichier et module — exigence de vérification de la story
- [ ] `tests/domaine/test_compter_comptes.py` — faux dépôt en mémoire, sans base — le domaine se teste sans base
- [ ] `tests/application/test_accueil.py` — sur MySQL : lignes créées, la page affiche le décompte (`django_db`) — la chaîne complète est prouvée
- [ ] `.github/workflows/ci.yml` — job `domaine` (sans service, `SECRET_KEY` factice) ; job `application` (service `mysql:8.4`, `makemigrations --check`, pytest) — AD-8
- [ ] `Procfile` — `web` gunicorn, `release` migrate — prêt pour le jour du déploiement, code neutre (AD-15) ; inerte tant que l'exécution est locale
- [ ] `docker-compose.yml` — MySQL 8.4 locale : la seule base d'exécution pendant les premières phases du développement
- [ ] `README.md` — installation locale, variables d'environnement documentées, CI, note courte « déploiement différé » (`Procfile` et variables déjà prêts) — dépôt vivant pour le repreneur
- [ ] `.gitignore` — étendre (`.venv/`, `.env`, `__pycache__/`, statiques collectés) sans retirer `_bmad/render/`

**Étapes humaines (points d'arrêt, hitl) :**
- H1, avant la PR : créer le dépôt GitHub **public**, ajouter le remote, pousser `main` (nécessaire pour que la CI tourne sur la PR) — gratuit.
- La mise en production Scalingo (compte, application, addon MySQL 8.4, prix du petit conteneur) et le compte Brevo sont différés : voir `deferred-work.md` à la racine de l'initiative.

**Acceptance Criteria:**
- Given le dépôt GitHub public avec la CI en place, when la PR de la story est ouverte, then les deux jobs passent (domaine sans base, application sur MySQL) et la fusion n'a lieu qu'après CI verte.
- Given la base MySQL 8.4 locale lancée (`docker compose up -d`) et le serveur de développement démarré, when on ouvre `http://127.0.0.1:8000/`, then la page d'accueil répond 200 et affiche le décompte lu depuis MySQL.
- Given le code livré, when on cherche une dépendance ou une fonction propre à un hébergeur, then il n'y en a aucune — le déploiement différé se fera sans modifier le code (AD-15).
- Given un import interdit (Django, HTTP, SQL, client externe) dans `domaine/`, when la CI tourne, then le test d'imports échoue en le nommant précisément.
- Given une migration manquante, when le job application tourne, then `makemigrations --check` échoue.
- Given `SECRET_KEY` ou `DATABASE_URL` absente, when l'application démarre, then elle refuse de démarrer avec un message explicite.
- Given un écran étroit (≈375 px) sans JavaScript, when on ouvre la page d'accueil, then elle reste lisible et utilisable.

## Implementation Notes

- 15/11/2026 — écarts d'implémentation rapportés par l'implémentateur, acceptés : la CI installe `default-libmysqlclient-dev` + `pkg-config` (mysqlclient 2.3.0 ne publie pas de roue Linux) ; le job application attend explicitement MySQL et l'utilise avec le compte racine du conteneur éphémère, seul capable de créer la base `test_*`.
- 20/11/2026 — audit matrice (étape 3) : trois lignes n'avaient qu'une vérification manuelle ; tests couvrants ajoutés — `tests/application/test_demarrage.py` (sous-processus, variable obligatoire vide → refus de démarrer, message français nommé), ligne « base injoignable » dans `tests/application/test_accueil.py` (dépôt levant `OperationalError` 2003 → 500 standard, journalisée via `django.request`), et chemin en échec de la garde dans `tests/test_imports_domaine.py` (domaine factice dans `tmp_path` → l'échec nomme fichier et module).
- 20/11/2026 — piège rencontré : `raise_request_exception` est un attribut du client de test Django, pas un paramètre d'appel — en kwarg de `client.get()` il finit en variable WSGI et l'exception est relancée dans le test ; le test positionne donc l'attribut avant la requête.
- 20/11/2026 — vérifications locales : `pytest -q` → 11 passed ; `pytest tests/test_imports_domaine.py tests/domaine -q` → 6 passed sans aucune base ; `python manage.py makemigrations --check --dry-run` → « No changes detected ». La CI GitHub Actions reste à exécuter : elle exige le dépôt distant (étape humaine H1 en attente).
- 20/11/2026 — correctifs de revue appliqués (garde moteur MySQL avec refus français nommant schéma inconnu et moteur reçu ; `.env` lu en `utf-8-sig` ; `yes` retiré du jeu DEBUG) ; piège rencontré : l'implémentateur a réécrit `tests/application/test_demarrage.py` pour le test sqlite et écrasé les deux tests « variable obligatoire absente » exigés par l'audit matrice (suite retombée à 10) — tests restaurés autour du nouveau cas sqlite. Vérifications repassées : 12 passed au total, 6 sans base, migrations propres, `runserver` + GET / → 200 avec décompte.

## Plan Change Log

## Review Triage Log

- 20/11/2026, lentille `quick` (1re passe) — verdicts : 0 high / 2 medium / 2 low / 0 false / 0 maybe-false.
  - `medium` `patch` — `application/config/settings.py` (section base) : `DATABASE_URL` analysé sans validation du moteur. Vérifié : `postgres://` configure le backend postgresql ; `sqlite://` configure sqlite puis échoue à la première connexion en `TypeError: Connection() got an unexpected keyword argument 'charset'` ; un schéma inconnu lève l'exception anglaise `UnknownSchemeError` de dj-database-url. Contredit la convention « erreurs en français » et laisse le Never « pas de SQLite » sans garde structurelle. Correctif automatique envoyé à l'implémentateur.
  - `low` `patch` — `application/config/settings.py` (`_charger_env`) : un `.env` avec BOM UTF-8 garde U+FEFF en tête de la première clé (vérifié : `'\ufeff'.isspace()` → False, `strip()` ne le retire pas) → refus de démarrage trompeur alors que la ligne est visible dans le fichier. Correctif automatique envoyé à l'implémentateur.
  - `low` `patch` — `README.md` vs `application/config/settings.py` : le code accepte aussi `yes` pour `DEBUG`, le README documente `1/true/vrai/oui` seulement — dérive de documentation. Correctif automatique envoyé à l'implémentateur.
  - `medium` `rejeté (hors périmètre, intention)` — critère « CI verte sur la PR » non démontrable à la revue : aucun dépôt distant (vérifié), la CI n'a jamais tourné. L'intention gelée place elle-même le dépôt GitHub public en étape humaine H1 et les règles du workflow interdisent toute opération distante. Reste suivie par l'étape H1 du plan et sera présentée à l'étape 5 — y inclure alors la protection de branche « PR obligatoire » à la création du dépôt, qui matérialise « fusion seulement après CI verte ».

## Design Notes

- INSTALLED_APPS volontairement minimale (ni auth, ni sessions, ni admin) : la story 1.2 doit trancher `AUTH_USER_MODEL` **avant** sa première migration ; migrer le `User` par défaut maintenant le lui interdirait.
- La vue `accueil` vit dans `comptes` tant qu'un seul app nourrit la page ; le câblage, lui, vit déjà dans `config/composition.py` (AD-10) — quand d'autres épics enrichiront l'accueil, la composition y restera.
- Garde d'imports par AST (pas d'exécution du code) sur `sys.stdlib_module_names` — aucune liste codée en main à maintenir.
- Courriels : backend console par défaut en local ; Brevo et ses variables `EMAIL_*` arriveront avec le déploiement différé — aucun envoi réel avant production.
- Déploiement différé mais prêt : WSGI standard, `Procfile`, variables d'environnement — remis en service sans toucher au code (AD-15).
- `dj-database-url` retenu pour `DATABASE_URL` : pur, gratuit, éprouvé sur les formats des PaaS ; moins d'analyse manuelle à se tromper.

## Verification

**Commands:**
- `pip install -e .[dev]` — attendu : installation sans erreur
- `pytest tests/test_imports_domaine.py tests/domaine -q` — attendu : verts sans aucune base
- `docker compose up -d` puis `pytest tests/application -q` (avec `.env`) — attendu : verts sur MySQL
- `python manage.py makemigrations --check --dry-run` — attendu : aucune modification de schéma détectée
- `python manage.py runserver` puis `GET /` — attendu : 200, décompte affiché
- CI verte sur la PR — attendu : les deux jobs passent, fusion seulement après CI verte

**Manual checks (if no CLI):**
- Page d'accueil lisible à ≈375 px et sans JavaScript ; textes et code en français.
