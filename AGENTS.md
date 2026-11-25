<!-- bmad:context -->
<!-- Verified 2026-11-21 against 87a457d. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## EscaManager

Gestion en ligne des adhésions du SCB Escalade, club d'escalade à but non lucratif de Beaucouzé : comptes, saisons, adhésions et paiement, liste des adhérents, licences FFME. Première partie d'un ensemble plus large : un site web responsif en Python 3.13 / Django 5.2 LTS / MySQL 8.4, porté par une bibliothèque de domaine (`domaine/`, paquet pur) consommée par une unique application Django (`application/`). La planification vit dans `_bmad-output/initiative-escamanager/`.

## Politique

- Ne jamais pousser sur `main` : PR obligatoire, fusion après CI verte et revue humaine.
- Ne jamais modifier `_bmad-output/` à la main : initiative, épics, ossature et glossaire ne changent que par les skills BMad dédiés.
- Secrets exclusivement en variables d'environnement ; jamais dans le code ni les fichiers suivis.
- Toute nouvelle dépendance est open-source et gratuite, sans engagement commercial.
- Données personnelles (RGPD) : minimisation à la collecte, consentement enregistré comme donnée.

## Où trouver quoi

- Règles d'architecture AD-1 à AD-15 : `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`. Les lire avant tout travail sur le socle ; une règle s'y change d'abord (les identifiants AD ne se renumérotent jamais), puis dans le code.
- Exigences produit : `initiative-escamanager.md` ; travail à construire : épics et stories dans `tickets/` (même dossier).
- Termes du club : `glossaire.md`. Une saison est une année sportive (par ex. 2026/2027), jamais l'année civile.
- Écrire un client externe (HelloAsso, FFME) : l'interface est un port déclaré dans `domaine/ports/` ; le protocole ne vit que dans l'adaptateur de `application/` (AD-5).
- Guide court du repreneur bénévole : `architecture-escamanager/prise-en-main-benevole.md`.

## Exécuter et vérifier

- Installer : `pip install -e ".[dev]"` (pytest, pytest-django, pytest-cov, mypy, ruff épinglé 0.17.6).
- Tests du domaine, sans aucune base : `pytest tests/test_imports_domaine.py tests/test_imports_apps.py tests/test_typographie.py tests/domaine -q --cov=domaine --cov-report=term-missing`. Exige `SECRET_KEY` et `DATABASE_URL` définies (fictives suffisent) : sans elles, les réglages refusent de charger.
- Tests de l'application : `docker compose up -d --wait` d'abord, puis `pytest tests/application -q` ; jamais SQLite, même en local (écarts de collation).
- La CI exécute en plus `ruff check .`, `ruff format --check .`, `mypy` (strict, `domaine/`), la garde de typographie et `python manage.py makemigrations --check --dry-run` : tout doit être vert avant fusion.
- EXE001 (ruff, jeu par défaut) ne peut pas échouer sous Windows : tout fichier suivi portant un shebang doit être exécutable dans git (`git update-index --chmod=+x <fichier>`), sinon seule la CI Linux le verra.
- Versions décidées : Python 3.13, Django 5.2 LTS, MySQL 8.4 LTS (cible), mysqlclient 2.3.0, ruff 0.17.6.

## Conventions qui divergent des défauts

- Symboles, apps Django et URLs en français, snake_case : apps `comptes`, `saisons`, `adhesions`, `membres`, `federation` ; textes de l'interface en français direct, sans catalogue i18n.
- `domaine/` n'importe que la bibliothèque standard Python : aucun import Django, HTTP, SQL ou client externe (garde d'imports en CI, AD-1).
- Les apps de `application/` ne s'importent jamais entre elles : le partage passe par `domaine/`, la composition par `application/config/` (garde d'imports en CI, AD-3, AD-10).
- Toute écriture d'une entité passe par un service du domaine en transaction ; modèles et vues Django ne portent aucune règle métier.
- Montants en `Decimal`, jamais float ; dates ISO en interne, fuseau Europe/Paris explicite, affichage en français.
- Chaque page fonctionne sans JavaScript ; le JS appelant des endpoints complète le rendu serveur, jamais ne le remplace.
- Permissions = identifiants stables déclarés dans le domaine ; les rôles nommés du club sont des données, jamais codés en dur (AD-14).
- Schéma de données uniquement par migrations Django ; aucun SQL brut propre à un moteur ; charset utf8mb4 (AD-7).
- Pas de tiret cadratin (caractère U+2014) nulle part : code, commentaires, docstrings, documents ; reformuler avec deux-points, virgule ou parenthèse (garde de typographie en CI).
- Pas de guillemets typographiques français (U+00AB, U+00BB) dans le code, les chaînes ou les commentaires : guillemets droits seulement (garde de typographie en CI).
- Pas de références AD-x dans les commentaires de code : les règles d'architecture vivent dans l'ossature.
- Les fichiers de code décrivent l'état présent : aucun commentaire sur le passé ou le futur ; l'historique et le programme vivent dans la documentation projet.

<!-- /bmad:context -->
