<!-- bmad:context -->
<!-- Verified 2026-11-15 against 4544700. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## EscaManager

Gestion en ligne des adhésions du SCB Escalade, club d'escalade à but non lucratif de Beaucouzé : comptes, saisons, adhésions et paiement, liste des adhérents, licences FFME. Première partie d'un ensemble plus large : un site web responsif en Python 3.13 / Django 5.2 LTS / MySQL 8.4, porté par une bibliothèque de domaine (`domaine/`, paquet pur) consommée par une unique application Django (`application/`). La planification vit dans `_bmad-output/initiative-escamanager/`.

## Politique

- Ne jamais pousser sur `main` : PR obligatoire, fusion après CI verte et revue humaine.
- Ne jamais modifier `_bmad-output/` à la main — initiative, épics, ossature et glossaire ne changent que par les skills BMad dédiés.
- Secrets exclusivement en variables d'environnement ; jamais dans le code ni les fichiers suivis.
- Toute nouvelle dépendance est open-source et gratuite, sans engagement commercial.
- Données personnelles (RGPD) : minimisation à la collecte, consentement enregistré comme donnée.

## Où trouver quoi

- Règles d'architecture AD-1 à AD-15 : `_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md` — les lire avant tout travail sur le socle ; une règle s'y change d'abord (les identifiants AD ne se renumérotent jamais), puis dans le code.
- Exigences produit : `initiative-escamanager.md` ; travail à construire : épics et stories dans `tickets/` (même dossier).
- Termes du club : `glossaire.md` — « saison » = année sportive (par ex. 2026/2027), jamais l'année civile.
- Écrire un client externe (HelloAsso, FFME) ? L'interface est un port déclaré dans `domaine/ports/` ; le protocole ne vit que dans l'adaptateur de `application/` (AD-5).
- Guide court du repreneur bénévole : `architecture-escamanager/prise-en-main-benevole.md`.

## Exécuter et vérifier

- Le socle n'existe pas encore (story 1 de l'épic comptes) : aucune commande de test ni de dépendance n'est établie — ne pas deviner d'invocation ; la story socle crée `pyproject.toml` et la CI GitHub Actions.
- Quand les tests existeront : domaine sans base, application sur MySQL — jamais SQLite, même en local (écarts de collation).
- Versions décidées : Python 3.13, Django 5.2 LTS, MySQL 8.4 LTS (cible), mysqlclient 2.3.0.

## Conventions qui divergent des défauts

- Symboles, apps Django et URLs en français, snake_case — apps : `comptes`, `saisons`, `adhesions`, `membres`, `federation` ; textes de l'interface en français direct, sans catalogue i18n.
- `domaine/` n'importe que la bibliothèque standard Python — aucun import Django, HTTP, SQL ou client externe (AD-1 ; un test d'imports en CI est prévu dès la story socle).
- Les apps de `application/` ne s'importent jamais entre elles : le partage passe par `domaine/`, la composition par `application/config/` (AD-3, AD-10).
- Toute écriture d'une entité passe par un service du domaine en transaction ; modèles et vues Django ne portent aucune règle métier (AD-2, AD-4).
- Montants en `Decimal`, jamais float ; dates ISO en interne, fuseau Europe/Paris explicite, affichage en français.
- Chaque page fonctionne sans JavaScript ; le JS appelant des endpoints complète le rendu serveur, jamais ne le remplace (AD-6).
- Permissions = identifiants stables déclarés dans le domaine ; les rôles nommés du club sont des données, jamais codés en dur ni référencés dans le code (AD-14).
- Schéma de données uniquement par migrations Django ; aucun SQL brut propre à un moteur ; charset utf8mb4 (AD-7).

<!-- /bmad:context -->
