# Revue par parcours — Story 1.1 « Socle et première page »

Cible : commit `21891db593a3dc4b2e4edeb2a270050bb2047c54` (branche `story-1-1-socle`, 36 fichiers, 1 101 insertions).

- [x] **Bloc 1 — Intention** *(accepté)*
- [x] **Bloc 2 — Vue d'ensemble** *(accepté)*
- [x] **Bloc 3 — Tranche : le domaine, paquet pur** *(accepté)*
- [x] **Bloc 4 — Tranche : la page d'accueil de bout en bout** *(accepté)*
- [x] **Bloc 5 — Tranche : réglages et refus rapide** *(accepté)*
- [x] **Bloc 6 — Tranche : CI et base locale** *(accepté)*
- [x] **Bloc 7 — Périphérie** *(accepté)*

---

## Bloc 1 — Intention

*Extrait verbatim de la section `## Intent` du plan de la story (bloc gelé après approbation) : `tickets/epic-comptes-permissions/tickets/story-socle-et-premiere-page-en-production-plan.md`, sous `_bmad-output/initiative-escamanager/`.*

**Problem:** le dépôt ne contient aucun code : rien ne prouve que la chaîne domaine → dépôt ORM → MySQL → page fonctionne, et les huit stories de l'épic n'ont pas de socle pour livrer.

**Approach:** balle traceuse de bout en bout : pyproject installable, paquet pur `domaine/` portant sa première lecture, projet Django minimal (`config` + `comptes`) servant la page d'accueil depuis MySQL, CI GitHub Actions en deux jobs (domaine sans base, application sur MySQL, garde d'imports). Exécution strictement locale pendant les premières phases du développement : le code reste déployable sans modification (WSGI standard, configuration exclusive par variables d'environnement, AD-15) et la mise en production est différée. Seul le dépôt GitHub public (nécessaire à la CI) relève d'une étape humaine.

**Decision (2026-11-15):** la première lecture du domaine est le décompte des comptes — requête `compter_comptes` sur l'entité `Compte` (app `comptes`, catalogue AD-9), servie par la page d'accueil.

**Decision (2026-11-15, renégociation humaine) :** pour réduire les coûts, rien n'est hébergé pendant les premières phases — l'application s'exécute en local uniquement ; la mise en production Scalingo (compte, application, addon MySQL, prix du petit conteneur) et le compte Brevo sont reportés au registre du travail différé.

## Bloc 2 — Vue d'ensemble

Le commit pose le socle entier d'un coup : un dépôt Python installable, une bibliothèque de domaine pure, une application Django minimale qui la sert, et la CI qui en prouve les propriétés. Cinq points d'entrée suffisent à comprendre le mécanisme :

1. [pyproject.toml](../../../pyproject.toml) — le dépôt installable : paquets `domaine*` et `application*`, dépendances, extra `dev`, configuration pytest.
2. [application/config/settings.py](../../../application/config/settings.py) — les réglages, pilotés par variables d'environnement seules, avec refus français au démarrage si quelque chose manque.
3. [application/comptes/vues.py](../../../application/comptes/vues.py) — la vue `accueil`, la seule page du site.
4. [application/config/composition.py](../../../application/config/composition.py) — le câblage port → adaptateur, le seul endroit où le domaine rencontre la persistance (AD-10).
5. [.github/workflows/ci.yml](../../../.github/workflows/ci.yml) — la CI en deux jobs : domaine sans base, application sur MySQL (AD-8).

## Bloc 3 — Tranche : le domaine, paquet pur

Le domaine ne connaît ni Django ni MySQL : il porte une entité, un port et une requête de lecture, rien d'autre. Sa pureté (AD-1) n'est pas un souhait mais une propriété vérifiée : une garde parcourt tous ses fichiers par AST et n'autorise que la bibliothèque standard ; le décompte se teste avec un faux dépôt en mémoire, sans aucune base.

- [domaine/entites/compte.py](../../../domaine/entites/compte.py) — l'entité `Compte`, dataclass figée, réduite au courriel (la story 1.2 l'étendra).
- [domaine/ports/depots.py](../../../domaine/ports/depots.py) — le port `DepotComptes`, interface de lecture `compter()`.
- [domaine/requetes.py](../../../domaine/requetes.py) — la requête `compter_comptes(depot)` : toute lecture passe par le domaine (AD-2).
- [tests/test_imports_domaine.py](../../../tests/test_imports_domaine.py) — la garde AST, avec son chemin en échec : une violation nomme fichier et module.
- [tests/domaine/test_compter_comptes.py](../../../tests/domaine/test_compter_comptes.py) — le décompte testé sans base, sur un faux dépôt.

## Bloc 4 — Tranche : la page d'accueil de bout en bout

La route `/` mène à la vue `accueil`, qui demande le décompte au domaine ; le dépôt Django implémente le port sur l'ORM ; le modèle `CompteDjango` porte la table des comptes (courriel unique), créée par la migration initiale ; le gabarit affiche le résultat en français, responsive, sans une ligne de JavaScript (AD-6). C'est la balle traceuse : chaque maillon de la chaîne existe et fonctionne.

- [application/config/urls.py](../../../application/config/urls.py) — la route `/` vers `accueil`.
- [application/comptes/vues.py](../../../application/comptes/vues.py) — la vue : `compter_comptes(depot_comptes())` puis rendu.
- [application/config/composition.py](../../../application/config/composition.py) — la fabrique `depot_comptes()`, câblage unique en `config` (AD-10).
- [application/comptes/depots.py](../../../application/comptes/depots.py) — `DepotComptesDjango` : le port implémenté sur l'ORM.
- [application/comptes/modeles.py](../../../application/comptes/modeles.py) et [migrations/0001_initial.py](../../../application/comptes/migrations/0001_initial.py) — la table `comptes_compte`, aucune règle métier (AD-2), schéma par migration seule (AD-7).
- [application/gabarits/base.html](../../../application/gabarits/base.html), [accueil.html](../../../application/gabarits/accueil.html) et [accueil.css](../../../application/static/css/accueil.css) — la maquette française, mobile d'abord.
- [tests/application/test_accueil.py](../../../tests/application/test_accueil.py) — la page prouvée sur MySQL : base vide, base peuplée, base injoignable (500 journalisée).

## Bloc 5 — Tranche : réglages et refus rapide

Toute la configuration vient de variables d'environnement, rien d'autre (AD-15) : le `.env` local est chargé en `utf-8-sig` sans jamais écraser l'existant ; `SECRET_KEY` et `DATABASE_URL` sont obligatoires et leur absence refuse le démarrage en français ; un `DATABASE_URL` qui ne désigne pas MySQL est refusé nommément (schéma inconnu ou moteur reçu) ; utf8mb4 est imposé à la connexion et à la base de test ; fuseau Europe/Paris, courriels en backend console. `manage.py` et le point d'entrée WSGI standard complètent l'image.

- [application/config/settings.py](../../../application/config/settings.py) — le chargeur `.env`, les variables obligatoires, la garde moteur MySQL, utf8mb4, INSTALLED_APPS volontairement minimale (ni auth, ni sessions, ni admin — la story 1.2 tranche `AUTH_USER_MODEL` avant sa première migration).
- [manage.py](../../../manage.py) et [application/config/wsgi.py](../../../application/config/wsgi.py) — les commandes de développement et l'entrée WSGI déployable partout.
- [tests/application/test_demarrage.py](../../../tests/application/test_demarrage.py) — le refus de démarrer prouvé en sous-processus : variable absente, ou URL sqlite refusée moteur nommé.

## Bloc 6 — Tranche : CI et base locale

La CI (AD-8) coupe la suite en deux : « Domaine — sans base » exécute la garde et les tests du domaine sans aucun service ; « Application — sur MySQL » démarre un service `mysql:8.4`, attend sa disponibilité, vérifie qu'aucune migration ne manque (`makemigrations --check`), puis exécute les tests de l'application sur la base. En local, la même MySQL 8.4 se lève par Docker Compose — jamais SQLite, même en local (AD-7).

- [.github/workflows/ci.yml](../../../.github/workflows/ci.yml) — les deux jobs, valeurs factices pour charger les réglages sans base, service MySQL avec compte racine éphémère.
- [docker-compose.yml](../../../docker-compose.yml) — la MySQL locale, healthcheck et volume persistant.

## Bloc 7 — Périphérie

- [README.md](../../../README.md) — installation locale, variables d'environnement documentées, tests, CI, note « déploiement différé ».
- [Procfile](../../../Procfile) — prêt pour le jour du déploiement (`web` gunicorn, `release` migrate) ; inerte tant que l'exécution est locale.
- [.gitignore](../../../.gitignore) — artefacts Python, `.env` jamais suivi, statiques collectés ; conserve `_bmad/render/`.
- [deferred-work.md](../deferred-work.md) — le registre du travail différé : mise en production Scalingo et compte Brevo, reportés par décision du 15/11/2026.
- [story-socle-et-premiere-page-en-production-plan.md](../tickets/epic-comptes-permissions/tickets/story-socle-et-premiere-page-en-production-plan.md) — le plan de la story, statut `built`, avec ses journaux d'implémentation et de revue.
