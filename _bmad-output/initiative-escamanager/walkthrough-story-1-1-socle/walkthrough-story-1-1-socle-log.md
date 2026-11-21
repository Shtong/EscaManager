# Review log: walkthrough-story-1-1-socle

Target: commit 21891db593a3dc4b2e4edeb2a270050bb2047c54 (branche story-1-1-socle, story 1.1 « Socle et première page »)

## 1 — orientation — démarrage de la revue

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:00:03+01:00

- Action: cible confirmée depuis la session de construction (pas de question utilisateur nécessaire) ; plan de la story déjà lu intégralement en contexte ; gabarit de journal lu ; slug vérifié libre.
- Result: revue ouverte sur le commit de la story 1.1 ; narration créée en 7 blocs (intention, vue d'ensemble, 4 tranches, périphérie), tous non visités, bloc courant = 1.
- Evidence: ../tickets/epic-comptes-permissions/tickets/story-socle-et-premiere-page-en-production-plan.md
- Open: aucun

## 2 — bloc 1 (intention) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:09:51+01:00

- Action: bloc 1 (intention) présenté verbatim depuis le plan gelé ; l'utilisateur a dit « fait » sans modification.
- Result: bloc 1 accepté tel quel ; bloc courant = 2 (vue d'ensemble).
- Evidence: walkthrough-story-1-1-socle.md (blocs 1 et 2)
- Open: arbre sale (dossier walkthrough non suivi) — commit proposé à l'utilisateur

## 3 — bloc 2 (vue d'ensemble) — question sur la CI

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:24:10+01:00

- Action: question utilisateur : pourquoi le job « Domaine — sans base » installe-t-il des paquets MySQL ? Vérification de ci.yml, pyproject.toml et des fichiers publiés de mysqlclient 2.3.0 sur PyPI.
- Result: le job domaine n'a aucun serveur MySQL (service mysql:8.4 uniquement dans le job application) ; apt installe default-libmysqlclient-dev + pkg-config, en-têtes C du client nécessaires pour COMPILER le pilote mysqlclient (2.3.0 ne publie que des roues Windows + sdist, vérifié sur PyPI). Le pilote vient de `pip install -e ".[dev]"` (dépendance runtime de la distribution unique) mais n'est jamais importé dans ce job — variables factices uniquement pour charger les réglages. Variante allégée (--no-deps + sous-ensemble) proposée, compromis uniformité/dérive expliqué.
- Evidence: .github/workflows/ci.yml:19-20,27,29,38 ; pyproject.toml:15 ; https://pypi.org/pypi/mysqlclient/2.3.0/json
- Open: décision utilisateur — garder l'installation uniforme ou alléger le job domaine

## 4 — bloc 2 (vue d'ensemble) — décision : installation uniforme conservée

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:34:32+01:00

- Action: décision utilisateur clôturant l'ouverture de l'entrée 3.
- Result: l'installation uniforme `pip install -e ".[dev]"` est conservée dans les deux jobs — le compromis uniformité/temps CI est assumé, le job domaine n'est pas allégé, rien à changer au commit.
- Evidence: .github/workflows/ci.yml:27-29
- Open: aucun (bloc 2 toujours en cours)

## 5 — bloc 2 (vue d'ensemble) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:35:29+01:00

- Action: bloc 2 présenté ; question CI résolue en cours de bloc (entrée 4) ; l'utilisateur a dit « fait ».
- Result: bloc 2 accepté ; bloc courant = 3 (tranche : le domaine, paquet pur).
- Evidence: walkthrough-story-1-1-socle.md (bloc 2)
- Open: question du commit du dossier walkthrough restée sans réponse — reportée à la clôture de la revue

## 6 — bloc 3 (domaine) — question de découpage des requêtes à l'échelle

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:39:53+01:00

- Action: question utilisateur : requetes.py deviendra-t-il un point de convergence à 10-20 pages ? Principes de découpage de l'interface UI.
- Result: explication fondée sur l'ossature — requetes.py est la forme minimale de la balle traceuse ; découpage prévu par propriétaire d'entité (AD-9) en paquet domaine/requetes/ quand les lectures d'un second propriétaire arrivent (épic 2 saisons) ; une requête = une forme de données affichée, déclarée une seule fois (AD-12) ; les vues ne composent jamais entre apps, la composition multi-fournisseurs vit dans config (AD-10) ; requêtes = fonctions pures sur ports (testées par faux dépôts). Pas de changement demandé à ce stade.
- Evidence: domaine/requetes.py:10 ; application/comptes/vues.py:15 ; architecture-escamanager.md (AD-2, AD-9, AD-10, AD-12)
- Open: aucun — split à faire dans la story qui amène les lectures du second propriétaire

## 7 — bloc 3 (domaine) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:44:26+01:00

- Action: bloc 3 présenté ; question de découpage des requêtes résolue en cours de bloc (entrée 6) ; l'utilisateur a dit « fait ».
- Result: bloc 3 accepté ; bloc courant = 4 (tranche : la page d'accueil de bout en bout).
- Evidence: walkthrough-story-1-1-socle.md (bloc 3)
- Open: commit du dossier walkthrough reporté à la clôture

## 8 — bloc 4 (page d'accueil) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:46:02+01:00

- Action: bloc 4 présenté ; l'utilisateur a dit « fait » sans coup intermédiaire.
- Result: bloc 4 accepté ; bloc courant = 5 (tranche : réglages et refus rapide).
- Evidence: walkthrough-story-1-1-socle.md (bloc 4)
- Open: commit du dossier walkthrough reporté à la clôture

## 9 — bloc 5 (réglages) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:47:18+01:00

- Action: bloc 5 présenté (avec note sur l'origine « correctifs de revue » de la garde moteur et du message français) ; l'utilisateur a dit « fait » sans coup intermédiaire.
- Result: bloc 5 accepté ; bloc courant = 6 (tranche : CI et base locale).
- Evidence: walkthrough-story-1-1-socle.md (bloc 5)
- Open: commit du dossier walkthrough reporté à la clôture

## 10 — bloc 6 (CI) — bloc accepté

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:47:53+01:00

- Action: bloc 6 présenté (renvoi à la discussion CI du bloc 2, entrées 3-4) ; l'utilisateur a dit « fait ».
- Result: bloc 6 accepté ; bloc courant = 7 (périphérie, dernier bloc).
- Evidence: walkthrough-story-1-1-socle.md (bloc 6)
- Open: commit du dossier walkthrough reporté à la clôture

## 11 — bloc 7 (périphérie) — bloc accepté, revue complète

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:49:48+01:00

- Action: bloc 7 présenté ; l'utilisateur a dit « fait ».
- Result: les 7 blocs sont acceptés — revue par parcours complète du commit 21891db. Clôture proposée à l'utilisateur.
- Evidence: walkthrough-story-1-1-socle.md (tous blocs cochés)
- Open: commit du dossier walkthrough ; suite naturelle = étape humaine H1 (dépôt GitHub public, remote, PR)

## 12 — clôture — revue terminée

Session: ses_e20aa9482ffeBYFHPXq5CmNQeB · Timestamp: 2026-11-21T15:50:47+01:00

- Action: clôture proposée (commit du dossier de revue + étape H1) ; décision utilisateur : commiter maintenant, H1 plus tard.
- Result: revue close — 7/7 blocs acceptés, aucun constat ouvert (question CI résolue entrée 4, découpage des requêtes entrée 6) ; dossier walkthrough commité sur la branche story-1-1-socle.
- Evidence: git (commit du dossier walkthrough-story-1-1-socle)
- Open: étape humaine H1 différée par l'utilisateur (dépôt GitHub public, remote, pousser main + branche, PR, protection de branche) — dernier critère d'acceptation de la story encore à démontrer
