---
type: spine-review
lens: règle — liste de contrôle « bonne ossature », contrôle de la mise à jour du 21/11/2026
target: _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
ticket: _bmad-output/initiative-escamanager/initiative-escamanager.md
journal: _bmad-output/initiative-escamanager/architecture-escamanager/.memlog.md
code: pyproject.toml, .github/workflows/ci.yml, tests/test_imports_domaine.py, git log (PR #1 fusionnée le 21/11/2026)
contexte: revoyeur frais, sans participation à la rédaction ; socle déjà fusionné (story 1.1, PR #1) — la séquence « l'ossature change d'abord, le code ensuite » est assumée par le projet pour les contrôles qualité ; les versions d'outils ont été re-vérifiées le jour même sur PyPI
date: 2026-11-21
---

# Revue « bonne ossature » — mise à jour du 21/11/2026

Revue de l'ossature complète (pas seulement des amendements du 21/11) contre la liste de contrôle « bonne ossature », point par point, avec la réalité du code comme témoin : le socle existe (story 1.1 fusionnée par PR #1 le 21/11, dépôt GitHub public avec protection de branche, CI verte), ce qui permet de vérifier la ratification en plus des intentions. Les technologies nommées par la mise à jour (ruff, mypy, pytest-cov) ont été re-vérifiées le jour même sur PyPI. Chaque constat porte une sévérité — critique / haute / moyenne / basse — et, quand elle est évidente, sa correction mécanique.

## Verdict

Ossature toujours solide, et mise à jour du 21/11 propre et cohérente : identifiants stables (AD-3 et AD-8 amendés en place), énumération d'AD-8 alignée avec les lignes Outillage/Stack et les deux nouveaux Deferred, versions exactes (re-vérifiées le jour même), dernière dimension silencieuse — la qualité de code entre contributeurs — désormais décidée ; aucun constat critique ni haut, deux retards de ratification de la réalité postérieurs au 04/11 (Deferred périmé sur deux items ; seed contredit par le code fusionné sur l'emplacement des requêtes de lecture) et quatre accrocs de netteté (basses) à régler à la prochaine passe.

## Constats (sévérité décroissante)

### C1 — [moyenne] Deux items du Deferred sont périmés : tranchés ou reportés par des décisions postérieures au 04/11, non ratifiés

- **« Le mode du dépôt GitHub (public ou privé) — épic 1 »** : la question est close. Décision « dépôt public » consignée dans l'épic 1 le 15/11 (commit 4544700 : « depot public »), exécutée le 21/11 : le dépôt public `Shtong/EscaManager` existe, la PR #1 y a été fusionnée après CI verte, avec un ruleset « Protection main » (commit d02cd38). Le Deferred continue de présenter comme ouverte une décision déjà exécutée.
- **« Le plan exact chez Scalingo… prix du petit conteneur à confirmer à la story socle »** : la condition de reprise est dépassée et remplacée. La story socle (1.1) est fusionnée (done le 21/11) sans que le prix soit confirmé ; par décision humaine du 15/11 au checkpoint du plan, la mise en production Scalingo — compte, application, addon MySQL, confirmation du prix — et le compte Brevo sont reportés au registre du travail différé (`deferred-work.md` à la racine de l'initiative, lu et vérifié). L'échéance « story socle » n'existe plus.

**Justification (points 3 et 5 de la liste) :** aucun de ces deux items ne peut laisser deux unités diverger — une seule unité, l'épic 1, décide, et elle a déjà décidé. Mais l'ossature affirme une ouverture factuelle close, alors que sa mise à jour du 21/11 est contemporaine (ou postérieure) de toutes ces décisions et touche précisément le Deferred. Le risque réel est la dépense d'un repreneur : un agent ou un bénévole qui lit le Deferred peut rouvrir une question tranchée — re-discuter public/privé, re-chercher le prix pour une échéance disparue, voire recréer un second dépôt. C'est la définition même d'un différé dont la condition de reprise n'est plus honnête.

**Correction mécanique :** deux lignes ajustées — « dépôt GitHub public — créé et protégé (PR #1 fusionnée, CI verte, protection main), 21/11/2026 » ; « mise en production Scalingo et compte Brevo — reportés au registre du travail différé (décision humaine du 15/11), prix du petit conteneur à confirmer au jour du déploiement ».

### C2 — [moyenne] Le Structural Seed contredit le code fusionné sur l'emplacement des requêtes de lecture

Le seed commente `ports/` ainsi : « dépôts, requêtes de lecture et clients externes (interfaces uniquement) ». Le code fusionné (story 1.1, PR #1) pose la première requête de lecture ailleurs : `domaine/requetes.py`, à la racine du paquet — précédent pris en pleine connaissance du seed (le plan de la story cite l'ossature et choisit explicitement `domaine/requetes.py`). Or AD-12, qui régira la « requête ligne adhérent » de l'épic 4, ne tranche pas l'emplacement : il dit seulement « une requête de lecture déclarée dans `domaine/` ». L'épic 4 lira donc soit le seed (→ `domaine/ports/`), soit le précédent (→ `domaine/requetes.py`) : deux maisons possibles pour le même type d'objet, précisément la graine de divergence structurelle qu'un seed doit prévenir — et l'épic 4 est l'une des deux épics construites en parallèle.

**Justification (points 5 et 1) :** impact borné — les deux placements respectent AD-1 (domaine pur) et AD-12 (déclaré dans `domaine/`) ; c'est un placement de fichier, pas une fuite hors du domaine. Mais l'ossature a été touchée le 21/11, après la fusion du code, sans ratifier le précédent ; la seule phrase du document qui précise l'emplacement des requêtes de lecture est contredite par la réalité. Un lecteur de confiance ne peut plus savoir laquelle des deux indications fait foi.

**Correction mécanique :** ajuster le commentaire du seed (« dépôts et clients externes ; les requêtes de lecture vivent à la racine du paquet — `requetes.py` »), ou à l'inverse resserrer AD-12 (« requête de lecture déclarée dans `domaine/ports/` ») et faire migrer `requetes.py` au build suivant — la règle du projet veut l'ossature corrigée d'abord, le code ensuite ; les deux voies sont conformes, il faut en choisir une.

### C3 — [basse] Les restes des constats C6/C7 de la revue du 04/11 n'ont pas été épuisés par les mises à jour du 09/11 et du 21/11

Quatre sous-points, aucun ne peut laisser deux unités diverger :

- le libellé d'altitude diverge toujours — memlog de l'ossature : « altitude: initiative » ; spine : « altitude: feature » ;
- le glossaire (compagnon du billet, correspondance FR/EN — cinq équipes nommeront des symboles français) reste absent des sources de la spine ;
- AD-6 n'a toujours pas de garde nommé — applicable en revue seulement, conforme au point 2 de la liste, mais l'inégalité de vérifiabilité relevée au 04/11 persiste ;
- le champ `updated` du frontmatter du memlog de l'ossature affiche toujours `2026-10-26T21:52` alors que son contenu va jusqu'au 21/11.

Un point connexe, acceptable celui-là : le « mécanisme unique » de vérification des permissions reste non nommé — mais il est désormais correctement renvoyé à la story 1.3 par la décision du 15/11 (« ensembles de permissions écrits à la volée dans la story 3 ») ; c'est du suivi d'épic, pas un manque de l'ossature.

**Justification :** étiquetage et traçabilité documentaire. Deux mises à jour se sont succédé sans que ces petites dettes soient payées ; à ce rythme, elles s'accumulent à chaque passe. Basse car sans risque structurel.

**Correction mécanique :** aligner le libellé d'altitude du memlog, ajouter `glossaire.md` aux sources de la spine, relever le champ `updated` du memlog ; pour AD-6, nommer un garde au moment où les pages se multiplieront (épic 3) — un test fonctionnel sans JavaScript par parcours suffit.

### C4 — [basse] L'écart volontaire entre AD-8 (sept contrôles) et la CI réelle (quatre) n'est tracé nulle part dans la spine

La CI fusionnée exécute : garde d'imports du domaine (AD-1 — vérifiée dans `tests/test_imports_domaine.py`, parcours AST sur `sys.stdlib_module_names`), tests du domaine sans base, tests de l'application sur MySQL 8.4, `makemigrations --check`. AD-8 énumère en plus : la garde des imports croisés apps (AD-3), lint et format ruff, mypy strict, pytest-cov au seuil. Le `pyproject.toml` réel n'a encore ni ruff, ni mypy, ni pytest-cov (extra dev = pytest, pytest-django). C'est la séquence prévue « l'ossature change d'abord, le code ensuite » — le memlog la documente (« point de gouvernance qualité avec l'utilisateur avant la reprise des stories ») — et ce n'est pas une contradiction ; le build suivant implémentera les contrôles. Mais la spine elle-même ne dit nulle part que sa cible est en attente d'implémentation : un repreneur qui compare AD-8 et `.github/workflows/ci.yml` voit un écart sans explication dans le document, et AD-3 promet un test d'imports « apps » qui n'existe pas encore.

**Justification :** la séquence est saine et correctement tenue ; c'est sa lisibilité depuis l'extérieur qui manque. Basse.

**Correction mécanique :** une ligne en Deferred — « mise en œuvre des quatre contrôles qualité du 21/11 dans la CI et pyproject (garde apps AD-3, ruff, mypy strict, pytest-cov au seuil) — build en cours après la story socle ».

### C5 — [basse] La ligne « Qualité (dev) » du Stack affiche des planchers comme si c'étaient des pins

Le memlog dit explicitement « plancher retenu » pour ruff 0.17 (courant vérifié : 0.17.6, du 19/11/2026), mypy 2.4 (courant 2.4.1, du 28/10/2026) et pytest-cov 7.1 (courant 7.1.0, du 21/03/2026). Le tableau Stack, lui, mêle sans distinction de lecture : un pin exact (mysqlclient 2.3.0 — et le `pyproject.toml` réel épingle bien `==2.3.0`), des gammes (Python 3.13, Django 5.2 LTS) et ces planchers (ruff 0.17 · mypy 2.4 · pytest-cov 7.1). Le build suivant devra choisir `>=0.17` ou `==0.17.6` sans que le document le dise ; deux unités (la CI et le pyproject local d'un bénévole) pourraient sinon épingler différemment.

**Justification :** netteté, pas divergence — la CI est l'autorité (ligne Outillage) et les bornes vivront dans pyproject. Basse.

**Correction mécanique :** écrire les planchers comme des planchers (« ruff ≥ 0.17 · mypy ≥ 2.4 · pytest-cov ≥ 7.1 ») ou une note de lecture sous le tableau (« versions de la colonne : pins pour la production, planchers pour l'outillage dev »).

### C6 — [basse] La liste des rôles d'AD-14 (cinq) est datée par rapport à la réalité de l'épic 1 (six)

AD-14 : « les rôles nommés du club (président, trésorier, secrétaire, membre du CA, adhérent)… ». L'épic 1, raffinée le même 04/11, sème six rôles au premier démarrage — l'administrateur technique en plus — et la story 1.3 écrira leurs ensembles de permissions. La règle elle-même (identifiants stables dans le domaine, ensembles de permissions en données, jamais codés en dur) est saine, ratifiée et sans divergence possible ; seule la liste entre parenthèses, héritée de la décision du 24/10, se lit comme exhaustive alors que la réalité du club ajoute des rôles au démarrage. Le qualificatif « du club » joue en sa faveur (l'administrateur technique n'est pas un rôle associatif), mais un lecteur pressé y verra un inventaire complet.

**Justification :** ratification légère, sans effet structurel — AD-14 ne dépend pas de l'exhaustivité de la liste. Basse.

**Correction mécanique :** « (président, trésorier, secrétaire, membre du CA, adhérent, administrateur technique — et tout rôle semé au démarrage) » ou un simple « notamment ».

## Passage de la liste de contrôle, point par point

### 1. Les vrais points de divergence pour les cinq épics — rien de manqué ?

Couverts, épics par épics : frontières entre apps (AD-3, garde nommée le 21/11 — le point le plus aigu, `membres` et `federation` étant construites en parallèle après l'épic 3), chemin d'écriture et idempotence des paiements (AD-4), intégrations externes et bouchon FFME (AD-5), rendu serveur (AD-6), dialecte SQL et migrations (AD-7), seuil de fusion et qualité (AD-8), catalogue des entités et propriétaires (AD-9), composition dans `config/` (AD-10), mutations multi-propriétaires et RGPD (AD-11), ligne adhérent partagée (AD-12), concepts saison/prix (AD-13), permissions et rôles (AD-14), hébergement (AD-15), courriels (Brevo, Stack). La mise à jour du 21/11 ferme le seul angle mort structurel restant depuis le 04/11 : la dérive de style, de typage et de discipline de tests entre cinq unités construites séparément par des contributeurs hétérogènes (bénévoles comme agents) — divergence réelle à cette altitude, correctement hissée du niveau story au niveau ossature. Les épics citent l'ossature comme compagnon (vérifié dans les cinq fichiers d'épic). Restes de netteté seulement : le placement des requêtes de lecture (C2), et le Deferred périmé (C1).

### 2. Chaque Rule est-elle applicable et prévient-elle réellement sa divergence ?

- **Mécaniques** : AD-1 (garde AST réelle, lue dans `tests/test_imports_domaine.py`, y compris le chemin en échec nommant fichier et module), AD-3 (garde promis, extension à écrire — séquence doc-d'abord), AD-7 (utf8mb4 par configuration de connexion, `makemigrations --check` réel dans la CI), AD-8 (sept contrôles mécaniques), AD-14 (identifiants stables vérifiables par grep).
- **Par relecture** : AD-2, AD-4 (idempotence testable), AD-5, AD-6, AD-9, AD-10, AD-11, AD-12, AD-13, AD-15.
- Aucune Rule invérifiable ; aucune ne prévient mal ce qu'elle énonce. Le recouvrement AD-2/AD-4 reste bénin. Les deux AD amendés sont bien formés : AD-3 (Binds R1–R10, Prevents couplage croisé des épics parallèles, Rule avec garde nommé) et AD-8 (Prevents enrichi le 21/11 — « style, typage et couverture compris » — pour couvrir exactement les nouveaux contrôles, Rule qui énumère). AD-6 reste le seul sans garde nommé (C3) — applicable en revue, conforme à la liste.

### 3. Rien sous Deferred ne peut laisser deux unités diverger

Vérifié item par item. Anodins ou munis d'une condition de reprise : outillage du rendu (épic 1, après `bmad-ux`), flux HelloAsso (épic 3 seule, mono-épic), API FFME (recherche `bmad-deep-recon` avant l'épic 5, bouchon en attendant — le meilleur item du lot), ensembles de permissions (épic 1, déjà consignés par sa décision du 15/11), sauvegarde au-delà de l'hébergeur / supervision au-delà du socle / plein-texte (hors périmètre explicite), mypy sur `application/` (condition : besoin ressenti ; sans danger car la partie partagée entre épics — le domaine et ses ports — est stricte dès maintenant, et les apps cloisonnées par AD-3 ne peuvent pas se contaminer par leurs annotations), hook pre-commit (la CI reste l'autorité). Deux items seulement ont une condition de reprise périmée — dépôt GitHub et plan Scalingo (C1) : ils ne peuvent pas non plus créer de divergence, mais ils affichent une ouverture close et demandent ratification.

### 4. Technologies d'actualité — re-vérifiées le 21/11/2026, pas affirmées

| Nom (spine) | Vérification du jour (PyPI) | Statut |
| --- | --- | --- |
| ruff 0.17 (plancher) | PyPI : 0.17.6 du 19/11/2026, MIT, lint et format en un seul outil, roues py3.13, compatible jusqu'à Python 3.15 | ✓ exact — le memlog du 21/11 est fidèle |
| mypy 2.4 (plancher) | PyPI : 2.4.1 du 28/10/2026, MIT, Production/Stable, Python ≥ 3.10 | ✓ exact |
| pytest-cov 7.1 (plancher) | PyPI : 7.1.0 du 21/03/2026, MIT, requiert coverage ≥ 7.10.6 et pytest ≥ 7 — compatible avec le dev actuel (`pytest>=8.0`, vérifié dans pyproject) | ✓ exact |
| Python 3.13, Django 5.2 LTS, MySQL 8.4, mysqlclient 2.3.0 | vérifiés le 26/10 et le 04/11 (memlog), confirmés par la revue « vérification web » du 04/11 ; le pyproject réel écrit bien `requires-python >=3.13`, `Django>=5.2,<5.3`, `mysqlclient==2.3.0` | ✓ conformes, ratifiés par le code |
| HelloAsso API v5, passerelle myFFME 2026-2027 | vérifiées le 04/11 (memlog, sourcé) ; pas re-vérifiées aujourd'hui — rien n'indique de changement, l'épic 3 les re-vérifiera à son raffinement | ✓ traçables |

Les affirmations du memlog du 21/11 (lignes 61-63) sont confirmées à la lettre. Seule réserve : l'ambiguïté plancher/pin de la ligne Stack (C5). Le choix « plancher » plutôt que pin est le bon pour des outils de dev — il évite de pourrir les PR de dépendances sans enjeu.

### 5. Ratifie la réalité du code existant plutôt que de la contredire

Ratifié partout où le code existe : AD-1 (garde AST réelle, fusionnée), AD-7 (utf8mb4 dans les réglages, `makemigrations --check` dans la CI, docker-compose MySQL 8.4), AD-8 dans son mécanisme (fusion via PR #1 après CI verte, ruleset « Protection main » consigné le 21/11 — la promesse « fusion seulement après CI verte » est matériellement tenue), AD-15 (WSGI standard, variables d'environnement seules, Procfile inerte), Brevo intégré à la Stack dès le 12/11. L'écart CI (quatre contrôles réels sur sept énumérés) est la séquence doc-d'abord prévue, assumée au memlog (C4 : à tracer dans la spine pour lisibilité). Trois retards de ratification : le Deferred dépôt/Scalingo (C1), le seed contredit par `domaine/requetes.py` (C2), la liste des rôles d'AD-14 face aux six rôles de l'épic 1 (C6). Aucune contradiction frontale avec le code fusionné hors ces trois points — remarquable pour un document touché trois fois en dix-sept jours.

### 6. Chaque dimension possédée par l'altitude est décidée, différée ou ouverte

- **Décidées** : paradigme, frontières et dépendances, mutations et transactions, intégrations externes, rendu, persistance et dialecte, seuil de fusion, déploiement et environnements, nommage et formats, fuseau, secrets, i18n (résolu au 04/11 : français direct, sans catalogues), courriels (Brevo), dépendances, tests — et, depuis le 21/11, **qualité de code** (ruff, mypy strict sur le domaine, couverture au seuil) : c'était la dernière dimension entière passée sous silence, la mise à jour la ferme avec ses lignes Outillage et Stack.
- **Différées avec échéance** : fournisseur PaaS (via le registre du travail différé depuis le 15/11 — échéance à corriger, C1), outillage du rendu (épic 1), flux HelloAsso (épic 3), API FFME (recherche puis épic 5), ensembles de permissions (story 1.3), mypy application/ (besoin ressenti), pre-commit (facultatif).
- **Ouverte** : durées de conservation des lignes anonymisées (épic 1, avec la trésorerie — question ouverte de l'épic, le mécanisme étant fixé par AD-11 et la politique générale tranchée le 04/11 : compte supprimé, historique anonymisé).
- **Silencieuse** : aucune dimension entière. Restes intra-dimensions seulement (placement des requêtes — C2 ; planchers — C5).

### 7. Identifiants stables, amendements en place

AD-1 à AD-15 présents, dans l'ordre, sans trou ni doublon ; AD-3 et AD-8 amendés en place le 21/11 (textes vérifiés : AD-3 porte désormais « — vérifié par le test d'imports de la CI, comme AD-1 » ; AD-8 porte l'énumération complète), AD-9 à AD-14 intacts depuis le 04/11, AD-15 en fin depuis le 09/11 — aucune renumérotation sur trois mises à jour, la promesse de stabilité est tenue. Le frontmatter de la spine (`updated: '2026-11-21'`) est correct ; seul le champ `updated` du memlog traîne (C3).

### 8. Cohérence des textes amendés du 21/11

Croisements vérifiés un à un :

- **AD-8 ↔ ligne Outillage** : l'énumération (garde AD-1/AD-3, tests domaine sans base, tests application MySQL, migrations, ruff, mypy strict, pytest-cov au seuil) est reprise et précisée par la ligne Outillage (où vit la valeur du seuil : `pyproject.toml`, relevable ; qui fait autorité : la CI, aucun hook exigé) — complémentaires, pas contradictoires.
- **AD-8 ↔ ligne Stack « Qualité (dev) »** : ruff 0.17, mypy 2.4 strict `domaine/`, pytest-cov 7.1 — versions conformes au memlog, le libellé « (dev) » isolant proprement l'outillage des dépendances de production.
- **AD-3 ↔ AD-8** : se citent mutuellement exactement (« garde d'imports du domaine et des apps (AD-1, AD-3) ») ; aucun doublon contradictoire — la redondance AD-8 ↔ lignes Outillage/Tests est de l'énoncé versus la précision.
- **Nouveaux Deferred ↔ reste du document** : mypy application/ s'accorde avec « typage du domaine (mypy strict) » ; pre-commit s'accorde avec « la CI est l'autorité » de la ligne Outillage et avec AD-8 ; les deux portent leur date (21/11/2026).
- **Binds/Prevents/Rule** : présents et bien formés sur les deux AD amendés (voir point 2) ; le Prevent d'AD-8 a été correctement élargi pour couvrir ce que les nouveaux contrôles préviennent (dérive de style, typage et couverture entre contributeurs).
- Seul accroc : l'ambiguïté plancher/pin de la ligne Stack (C5) ; la ligne Outillage omet de citer la garde d'imports et la vérification des migrations, sans gravité — elles vivent dans AD-1/AD-3/AD-8 et la CI réelle les exécute déjà.

## Points forts

- La mise à jour du 21/11 ferme exactement la bonne brèche, au bon niveau : la dérive de qualité de code entre unités construites séparément par des contributeurs hétérogènes est une divergence réelle de cette altitude, la seule dimension entière encore silencieuse depuis le 04/11 — elle est désormais décidée, avec un mécanisme (CI) et non une exhortation.
- « La CI est l'autorité, aucun hook local n'est exigé » : cohérent avec AD-15 (neutralité), avec l'équipe cible (bénévoles peu techniques) et avec le Deferred pre-commit — trois textes qui se renforcent au lieu de se contredire.
- Les trois versions nommées sont exactes (re-vérifiées le jour même sur PyPI) et le choix « plancher » plutôt que pin est le bon pour l'outillage de développement.
- La séquence « l'ossature change d'abord, le code ensuite » est réellement respectée — l'ossature a changé avant le build qui implémentera les contrôles, et le memlog en garde la trace datée.
- La promesse de stabilité des identifiants est tenue sur trois mises à jour successives : AD-3 et AD-8 amendés en place, AD-15 ajouté en fin, aucune renumérotation.

## Récapitulatif des actions

| # | Sévérité | Action |
| --- | --- | --- |
| C1 | moyenne | Ratifier dans le Deferred : dépôt GitHub public (décidé le 15/11, exécuté le 21/11) ; mise en production Scalingo et Brevo reportés au registre du travail différé (15/11), échéance « story socle » remplacée |
| C2 | moyenne | Trancher l'emplacement des requêtes de lecture : ajuster le commentaire du seed (`requetes.py` à la racine) ou resserrer AD-12 vers `domaine/ports/` et migrer au build suivant |
| C3 | basse | Épuiser les restes C6/C7 du 04/11 : libellé d'altitude du memlog, glossaire dans les sources de la spine, champ `updated` du memlog ; garde AD-6 à nommer quand les pages se multiplieront |
| C4 | basse | Une ligne en Deferred : mise en œuvre des quatre contrôles qualité du 21/11 (garde apps AD-3, ruff, mypy, pytest-cov) dans la CI et pyproject — build en cours |
| C5 | basse | Écrire les planchers comme des planchers dans la ligne « Qualité (dev) » (ruff ≥ 0.17, mypy ≥ 2.4, pytest-cov ≥ 7.1) ou noter la convention de lecture du tableau Stack |
| C6 | basse | « Notamment » ou sixième rôle (administrateur technique) dans la liste des rôles d'AD-14 |

## Remarque hors périmètre (consignée pour la traçabilité)

`AGENTS.md` (vérifié contre le commit 4544700 du 15/11) dit encore « le socle n'existe pas encore… la story socle crée pyproject.toml et la CI » — périmé depuis la fusion de la story 1.1 (21/11) : pyproject, CI en deux jobs et garde d'imports existent. Ce fichier est géré par `bmad-project-context`, pas par l'ossature : à rafraîchir à la prochaine passe de ce skill, idéalement avec les commandes de vérification désormais établies (`pip install -e ".[dev]"`, `pytest tests/test_imports_domaine.py tests/domaine -q`, `pytest tests/application -q`, `python manage.py makemigrations --check --dry-run`).
