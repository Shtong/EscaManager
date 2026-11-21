---
title: 'Contrôles continus de l'ossature — ruff, mypy strict, pytest-cov, garde d'imports apps (AD-8, maj 21/11/2026)'
type: feature
ticket: ''
created: '2026-11-21'
status: built
baseline_revision: c32fe1bca17e595e74aa435834a13d5bd37e52e4
route: full
route_source: auto
risk: low
review: quick
review_source: pinned
lenses_ran: [quick]
review_loop_iteration: 0
context:
  - _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
  - _bmad-output/initiative-escamanager/architecture-escamanager/reviews/review-verification-web-maj.md
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** AD-8 amendé (21/11/2026) promet quatre contrôles continus — ruff lint+format, mypy strict sur `domaine/`, pytest-cov au seuil sur le domaine, garde des imports croisés entre apps (AD-3) — que ni `pyproject.toml` ni la CI n'instancient (écart principal de la revue de vérification web du 21/11).

**Approach:** Instancier les contrôles dans `pyproject.toml` et le job sans base de la CI ; écrire la garde apps au patron de la garde AD-1 ; compléter les tests du domaine (entité à 0 %, port à 80 % mesurés) ; passer `ruff format` sur les 3 fichiers non conformes.

## Boundaries & Constraints

**Always:** AD-1 à AD-15 (AD-3 : le code par le test d'imports, les migrations par la revue de fusion ; AD-8 : la CI est l'autorité, aucun hook local) ; français partout ; planchers du journal pour mypy (`>=2.4`) et pytest-cov (`>=7.1`), ruff épinglé `==0.17.6` avec son jeu de règles par défaut — renégociation humaine du 21/11/2026, choix prévu par le constat C5 de la revue règle ; le seuil vit dans `pyproject.toml` seul ; deux jobs, `pip install -e ".[dev]"` uniforme ; nouveaux tests au patron des existants. Décisions du 21/11/2026 : seuil de couverture du domaine fixé à 90 (relevable au fil des épics) ; mysqlclient reste `==2.3.0` — la montée 2.3.2 attendra une passe d'ossature.

**Never:** ne pas modifier `_bmad-output/` ni `AGENTS.md` ; ne pas élargir la garde au-delà du texte adopté (FK par chaîne et gabarits = correctif A3, décision d'ossature future) ; ne pas changer les versions de la Stack hors décision ; pas de seuil sur `application/` (A8 non adopté) ; pas de hook pre-commit ; aucun SQL, aucun changement de schéma ni de comportement.

## I/O & Edge-Case Matrix

| Scénario | Entrée / État | Attendu | Erreur |
|---|---|---|---|
| Import croisé (direct ou dynamique littéral) | fichier d'une app important `application.<autre_app>…` (nœud AST, `importlib`, `__import__`) | garde échoue, fichier + module nommés | nominatif |
| Imports licites | soi-même, `domaine`, Django, stdlib ; `config` → apps (AD-10) | la garde passe | — |
| App future | dossier `application/<app>/` avec `__init__.py` | couverte automatiquement (dérivation du système de fichiers) | — |
| Couverture < seuil | total `domaine/` < `fail_under` | pytest échoue avec rapport | CI visible |
| Format / imports / typage | écart ruff ou mypy strict | l'outil échoue en nommant le fichier | idem |

</frozen-after-approval>

## Code Map

- `pyproject.toml` — extra dev actuel : `pytest>=8.0`, `pytest-django>=4.9` ; aucune section ruff/mypy/coverage ; tout s'écrit ici, le seuil n'existe qu'ici
- `.github/workflows/ci.yml` — job `domaine` (env factices) à renommer/étendre ; job `application` inchangé
- `tests/test_imports_domaine.py` — garde AD-1, patron à imiter (AST, échec nominatif, matrice `tmp_path`) ; sera reformatée
- `tests/test_imports_apps.py` — NOUVEAU : garde AD-3
- `tests/domaine/test_compter_comptes.py` — patron des tests du domaine (faux dépôt en mémoire)
- `tests/domaine/test_compte.py`, `tests/domaine/test_depots.py` — NOUVEAUX
- `domaine/entites/compte.py` (frozen dataclass, 0 %), `domaine/ports/depots.py` (ABC, ligne 17 non couverte) — cibles des tests, à ne pas modifier
- `tests/application/test_accueil.py` — écart I001 à corriger
- `application/comptes/migrations/0001_initial.py`, `manage.py` — reformatage cosmétique
- `README.md` — sections Tests et CI à mettre à jour
- `AGENTS.md` — ne pas toucher (bmad-project-context)

## Tasks & Acceptance

**Execution:**
- [x] `pyproject.toml` — ajouter à l'extra dev `pytest-cov>=7.1`, `ruff>=0.17`, `mypy>=2.4` ; `[tool.ruff]` : `target-version = "py313"`, `extend-exclude` (`_bmad`, `.agents`, `_bmad-output`) ; `[tool.ruff.lint]` : `select = ["E4", "E7", "E9", "F", "I"]` ; `[tool.mypy]` : `files = ["domaine"]`, `python_version = "3.13"`, `strict = true` ; `[tool.coverage.report]` : `fail_under = 90`, `show_missing = true`
- [x] `tests/test_imports_apps.py` — garde AD-3 au patron de la garde AD-1 : apps = dossiers de `application/` portant `__init__.py`, hors `config` ; parcours AST des fichiers des apps ; échec nominatif fichier + module sur tout import enraciné sur `application.<autre_app>`, y compris `importlib.import_module` / `__import__` à chaîne constante ; matrice du chemin en échec (apps factices dans `tmp_path`)
- [x] `tests/domaine/test_compte.py` — `Compte` : construction, gel (affectation refusée), égalité
- [x] `tests/domaine/test_depots.py` — contrat du port : instanciation de l'ABC refusée (`TypeError`) ; appel de la méthode de base → `NotImplementedError`
- [x] `tests/application/test_accueil.py` — corriger l'ordre des imports (I001)
- [x] racine — `ruff format` : trois fichiers seulement (la migration, `manage.py`, la garde AD-1)
- [x] `.github/workflows/ci.yml` — job sans base renommé « Domaine et qualité — sans base » ; avant le pytest : « Lint et format (ruff) » → `ruff check .` puis `ruff format --check .` ; « Typage strict du domaine (mypy) » → `mypy` ; le pytest devient `pytest tests/test_imports_domaine.py tests/test_imports_apps.py tests/domaine -q --cov=domaine --cov-report=term-missing` ; en-tête mis à jour
- [x] `README.md` — Tests et CI : commandes des contrôles pour les bénévoles, description à jour des deux jobs

**Acceptance Criteria:**
- Given le dépôt, when `ruff check .` puis `ruff format --check .`, then zéro constat, rien à reformatter.
- Given `domaine/` annoté, when `mypy`, then succès sans erreur.
- Given les tests du domaine complétés, when le pytest du job avec `--cov=domaine`, then tout passe et la couverture totale de `domaine/` tient le seuil sans exclusion ni pragma.
- Given une app important une autre app (arbre factice), when la garde s'exécute, then l'échec nomme fichier et module.
- Given la migration reformatée, when `python manage.py makemigrations --check --dry-run`, then aucune migration manquante.
- Given toutes les commandes vertes localement, when la branche est poussée, then la PR passe la CI verte avant fusion (jamais de poussée sur main).

## Implementation Notes

- 21/11/2026 — Interprétation validée : la garde attrape aussi « from application import <app> » et les imports relatifs inter-apps (« from ..comptes import … ») — même import, autre syntaxe ; l'exemption « relatif » de la garde AD-1 ne se justifie que dans le domaine, d'où un relatif n'en sort jamais. FK par chaîne et gabarits restent à la revue de fusion (A3 hors périmètre).
- 21/11/2026 — `.coverage` (binaire de couverture) ajouté à la section « Outils de test » de `.gitignore` : artefact créé par chaque exécution locale du nouveau contrôle pytest-cov.
- 21/11/2026 — Le sabotage « seuil + 1 » supposait une couverture entre 90 et 100 ; les tests demandés portent le domaine à 100 %, donc 91 passe aussi. Mécanisme prouvé autrement : une exécution des seules gardes mesure 0 % et échoue (« Coverage failure… fail-under=90 », code de sortie 1), sans aucun drapeau CI.
- 21/11/2026 — Vérifications rejouées par l'orchestrateur : `pip install -e ".[dev]"` (planchers exacts résolus), `ruff check .`, `ruff format --check .`, `mypy`, pytest des gardes et du domaine (15 passed, 100 % ≥ 90), pytest de l'application sur MySQL (6 passed), `makemigrations --check` après reformatage (« No changes detected »).
- 21/11/2026 — Renégociation du bloc figéré par l'humain : ruff basculé sur son jeu par défaut, épinglé `==0.17.6` ; exemption RUF012 pour `**/migrations/*` (idiome des migrations Django générées) ; `check=False` explicite dans `test_demarrage.py` (les 3 tests rejoués verts — ils attendent un code non nul, le drapeau explicite est le comportement réel). Vérification complète rejouée après bascule.

## Plan Change Log

- 21/11/2026 — Renégociation humaine (revue du diff avant poussée) : ruff passe du jeu minimal épinglé (E4/E7/E9/F + I, plancher `>=0.17`) au **jeu de règles par défaut**, version épinglée `==0.17.6`. Déclencheur : l'humain conteste le jeu minimal — le pin de version suffit à figer la dérive, le défaut est compatible formateur (vérifié : aucune règle de mise en page dans le jeu activé), et normaliser quel que soit le niveau est l'intention même d'AD-8. Amendé : ligne Always du bloc figéré (ruff épinglé, renégociation humaine), `pyproject.toml` (pin + `per-file-ignores` RUF012 pour `**/migrations/*`), `tests/application/test_demarrage.py` (`check=False` explicite). État évité : un jeu minimal qui normalise moins que l'ossature ne le promet, défendu par un argument anti-dérive plus faible que le pin (le plancher laissait quand même les familles E/F/I s'enrichir en silence). KEEP : le patron AD-1 de la garde apps (dérivation du système de fichiers, échec nominatif, matrice `tmp_path`), les planchers mypy/pytest-cov, le seuil dans `pyproject.toml` seul, les deux jobs et l'installation uniforme.

## Review Triage Log

- Passe 1 (lens `quick`, 21/11/2026) — 0 high / 0 medium / 1 low / 0 false / 0 maybe-false.
- **low** — rejeté (règle : un correctif qui édite le plan de ce build est rejeté) — `_bmad-output/initiative-escamanager/plan-controles-continus-ossature.md`, section Verification : la ligne « saborder `fail_under` (seuil + 1) doit faire échouer » promet un échec que l'état livré ne peut plus produire (les tests demandés portent le domaine à 100 %, donc 91 passe) ; vérifié réel par l'orchestrateur ; le mécanisme de seuil est prouvé par substitution (gardes seules → 0 % mesuré → échec, code 1) et la substitution est consignée dans Implementation Notes ; aucun impact code, CI ni utilisateurs.

## Design Notes

- Garde fidèle au texte adopté : AD-3 confie le code au test d'imports, les migrations à la revue de fusion ; élargir aux FK par chaîne et gabarits (A3) exige d'abord un resserrement d'ossature (bmad-architecture) — hors périmètre. Les imports dynamiques littéraux restent : le journal veut une « garde honnête ».
- Planchers `>=` (journal : « plancher retenu ») pour mypy et pytest-cov ; ruff épinglé `==0.17.6` sur son jeu de règles par défaut — renégociation humaine du 21/11/2026 : le défaut 0.17 est curaté (bandit : 3 règles à haut signal), compatible formateur (aucune règle de mise en page dans le jeu activé) et ne produit que 3 constats sur le dépôt (RUF012 ×2 sur la migration générée → exemption ciblée ; PLW1510 → `check=False` explicite). Le pin fige le jeu avec la version : l'autorité ne change que par un diff relu, et le choix `==0.17.6` était explicitement prévu par le constat C5 de la revue règle.
- Le seuil vit dans `[tool.coverage.report] fail_under` (Outillage : « valeur dans pyproject.toml et relevable ») ; pytest-cov l'honore sans drapeau CI.
- Domaine seul mesuré (A8 non adopté) ; deux jobs conservés, extra dev unique (décisions du walkthrough 1.1 et du journal).

## Verification

**Commands:**
- `pip install -e ".[dev]"` — ruff, mypy, pytest-cov installés
- `ruff check .` puis `ruff format --check .` — zéro constat, rien à reformatter
- `mypy` — succès sur `domaine/`
- `pytest tests/test_imports_domaine.py tests/test_imports_apps.py tests/domaine -q --cov=domaine --cov-report=term-missing` (env factices) — tout passe, couverture ≥ seuil ; saborder `fail_under` (seuil + 1) doit faire échouer la commande
- `pytest tests/application -q` (MySQL locale, `docker compose up -d --wait`) — suite application toujours verte
- `python manage.py makemigrations --check --dry-run` — aucune migration manquante
