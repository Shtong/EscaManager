---
type: architecture-review
lens: adversarial — attaque de la mise à jour du 21/11/2026
target: _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
units: epic-comptes-permissions (stories 1–8), epic-saisons, epic-adhesions-paiement, epic-liste-adherents, epic-federation
date: 2026-11-21
status: final
---

# Revue adverse — ossature EscaManager, mise à jour du 21/11/2026

## Verdict

Les contrôles continus du 21/11 disciplinent chaque unité prise isolée — style, typage du noyau, couverture du noyau, garde d'imports — mais aucun d'eux ne mesure un **contrat entre unités** : huit attaques tiennent, dont une critique et quatre hautes, toutes montrant deux unités construites séparément, chacune conforme à la lettre des quinze AD, qui produisent pourtant un double encaissement, un schéma secrètement croisé entre apps, une frontière port↔adaptateur jamais vérifiée ou une non-conformité RGPD — **avec CI verte** ; de surcroît, trois clauses proposées par la revue du 04/11 n'ont pas survécu à l'adoption et rouvrent les angles qu'elles fermaient.

## Méthode

Lecture intégrale de l'ossature (version du 21/11/2026), du journal `.memlog.md`, de la revue adverse du 04/11 (pour ne pas réinventer ses trous), des trois autres revues, de l'initiative, des cinq épics et des huit stories planifiées de l'épic comptes. Conformément au mandat, j'ai d'abord vérifié ce que AD-9, AD-11, AD-12, AD-13 et AD-14 ferment réellement — en comparant chaque AD **adoptée** à la proposition de la revue du 04/11 (section suivante) : trois clauses proposées n'ont pas été reprises, et mes attaques exploitent d'abord ces angles rouverts. J'ai ensuite testé systématiquement les paires d'unités au niveau le plus fin où le bâtisseur change (story contre story quand les stories existent — épic 1 ; story anticipée contre story anticipée, ou épic contre épic, sinon), en cherchant à chaque fois deux unités qui obéissent à la lettre à toutes les AD. Enfin j'ai attaqué directement les quatre contrôles du 21/11 (mypy strict sur `domaine/` seul, garde d'imports, seuil pytest-cov sur le domaine seul, CI comme autorité) en demandant : quelles divergences cette mesure ne voit-elle pas ?

## Vérification préalable : ce que AD-9, AD-11, AD-12, AD-13, AD-14 ferment — et ce qu'elles ne ferment pas

**Clauses proposées le 04/11 et perdues à l'adoption** (constat de cette revue, exploité ci-dessous) :

1. AD-9 proposée disait « un individu physique n'a qu'une entité personne, quelle que soit l'année », « les données personnelles d'un adhérent vivent uniquement dans `Adherent` » et « une app non propriétaire accède à une entité uniquement par les ports de lecture du domaine » — l'AD-9 adoptée ne contient **aucune** de ces trois phrases : elle catalogue des propriétaires et exige l'entrée au catalogue, point.
2. AD-5 resserrée proposée disait « clé d'identification requise » dans le contrat du port et « si l'API réelle exige des champs absents d'une entité existante, l'ajout est une décision prise avec l'app propriétaire de l'entité, jamais une migration silencieuse » — l'AD-5 adoptée n'a gardé que la sémantique d'états de licence.
3. AD-12 proposée disait « toute donnée lue par une app non propriétaire passe par une requête nommée du domaine » — l'AD-12 adoptée ne le dit que pour la seule ligne adhérent.

Ce que chaque AD ferme néanmoins correctement : AD-9 ferme la double définition d'une même entité et l'entité sans propriétaire ; AD-11 ferme l'effacement partiel silencieux et le chemin d'écriture multi-propriétaires ; AD-12 ferme la double forme de la ligne adhérent et la copie dénormalisée ; AD-13 ferme les deux calculs de « saison en cours » et de prix, et institue la photo tarifaire ; AD-14 ferme le vocabulaire de permissions dupliqué et les rôles codés en dur. Mes attaques ne retouchent pas ces terrains. Ce qui reste ouvert de façon transversale : les **clés** (unicités métier, identité d'une personne à travers les saisons) et les **contrats sémantiques** (contenu des requêtes partagées, contrat d'erreur des ports, liens entre entités de propriétaires différents, raccordements successifs, et le test de tout cela).

---

## Attaques

### A1 — L'unicité « une adhésion par personne et par saison » n'est régie par aucune AD (critique)

**Paire divergente :** stories de l'épic adhesions-paiement — « souscrire en ligne » ↔ « paiement hors ligne enregistré par l'équipe » (l'épic liste en témoin, l'épic fédération en aggravation).

**Scénario.** Le bâtisseur de la souscription crée `Adherent` + `Adhesion` à chaque soumission du parcours — c'est même nécessaire, car le webhook HelloAsso doit rattacher le paiement à une adhésion qui existe. Il obéit à tout : service du domaine en transaction (AD-4), entités au catalogue (AD-9), aucun import croisé (AD-3), permissions (AD-14). Le bâtisseur du paiement hors ligne reçoit un chèque au local du club ; pour l'enregistrer « avec son moyen » (R6), il doit le rattacher à une adhésion — et comme rien ne lui dit qu'une adhésion existe déjà pour cette personne, le chemin naturel de sa story crée l'adhésion au moment de la saisie, par un autre service du domaine, tout aussi conforme. Charles adhère en ligne lundi (paiement HelloAsso encaissé), son chèque perdu dans un sac arrive mercredi : l'équipe l'enregistre → deuxième `Adhesion`, deuxième `Paiement`. AD-4 n'interdit rien : sa clé d'unicité n'est exigée que pour les « mutations nées d'un événement externe » (rejouer un webhook) ; une saisie humaine n'est pas un rejeu, et une double souscription humaine non plus. AD-9 catalogue les entités, aucune AD ne déclare leurs **unicités métier** ; la clause « un individu n'a qu'une entité personne » de la revue du 04/11 n'a pas été adoptée, donc même la clé d'identité de la personne à travers les saisons est sans maison. **Incompatibilité en chaîne :** double encaissement réel (HelloAsso + chèque), liste de l'épic 4 avec deux lignes pour la même personne (AD-12 rend fidèlement ce qui existe), et l'épic 5 enregistre le même mineur **deux fois** comme licencié FFME si la vérification passe entre les deux écritures — la sémantique d'états (AD-5) ne connaît pas « enregistrement déjà en cours ici ». CI verte partout : chaque unité teste ses propres parcours, jamais la collision des deux.

**Sévérité : critique** (argent réel encaissé deux fois, doublon fédéral, liste faussée).

**Correctif :** AD nouvelle (proposition AD-16) — toute entité du catalogue AD-9 déclare ses unicités fonctionnelles dans le domaine et les porte en contraintes de base par migrations ; en particulier une adhésion est unique par (personne, saison) et la clé d'identité d'une personne est déclarée une seule fois dans le domaine ; tout service d'écriture vérifie l'unicité avant création, la contrainte en base restant le filet.

### A2 — AD-12 fixe la maison de la ligne adhérent, pas son contenu (haute)

**Paire divergente :** stories de l'épic adhesions-paiement (« créer l'adhésion », « confirmer le paiement ») ↔ stories liste et export de l'épic liste-adherents.

**Scénario.** L'épic 3 crée l'`Adhesion` **avant** le paiement (état « en attente ») — structurellement obligatoire pour qu'HelloAsso ait quelque chose à confirmer. Chaque écriture est un service du domaine en transaction : conforme. L'épic 4 construit la requête « ligne adhérent » — maison dans le domaine, rendue sans copie, corrections par l'app propriétaire : AD-12 obéie à la lettre. Mais AD-12 ne dit **rien du contenu** : quelles adhésions figurent ? Le bâtisseur de l'épic 4 fabrique ses fixtures en appelant directement les services du domaine — il ne passe jamais par le parcours HelloAsso, il ne sait même pas que l'état « en attente » existe : sa liste inclut toutes les adhésions (ou les filtre, décision seule). L'export tableur (R8) fige ce choix dans le fichier que le club enverra tel quel à la FFME ou à la comptabilité. Trois autres contenus sans maison : (a) quand l'équipe a corrigé un prix de saison après coup (R4 le permet), la photo tarifaire (AD-13) et le montant réellement encaissé par HelloAsso divergent — la ligne affiche lequel ? AD-13 institue la photo, pas la réconciliation ni l'affichage de l'écart ; (b) l'instant exact de la photo (« au moment de l'adhésion ») entre création du panier et confirmation du paiement, deux stories différentes ; (c) l'orchestrateur d'effacement (AD-11) crée un nouvel état de ligne — l'anonymisé — que la requête de l'épic 4 doit régir (trou ? ligne muette ?) : le raccordement AD-11→AD-12 n'est écrit nulle part. Ordre de tri et pagination : non régis.

**Sévérité : haute** (l'export devient LA forme canonique du club sur une décision prise seul par un bâtisseur, et les incompatibilités AD-11/AD-13/AD-12 se rencontrent en silence).

**Correctif :** AD-12 resserrée — chaque requête partagée est déclarée dans le domaine **avec son contrat** : états des entités sources inclus, colonnes, ordre, comportement en cas d'écart photo/encaissé (AD-13 complétée sur ce point unique), traitement des lignes anonymisées ; le contrat s'écrit avant le rendu de la première page.

### A3 — La garde d'imports ne voit pas les chaînes : AD-3 contournée au niveau du schéma (haute)

**Paire divergente :** epic-adhesions-paiement ↔ epic-federation (et épics 4/5 parallèles pour les gabarits).

**Scénario.** La story socle n'a livré qu'une garde pour `domaine/` (`tests/test_imports_domaine.py`, parcours AST des nœuds import) ; la garde des apps promise par l'AD-3 amendée n'existe pas encore et l'ossature n'en fixe pas la spec. Le bâtisseur de l'épic 5 crée `Licence`, qui se vérifie « pour une adhésion » (Done when de son épic). Sans importer `adhesions` — il obéit à AD-3 à la lettre — il écrit le lien le plus naturel en Django : `ForeignKey("adhesions.AdhesionDjango")`. Référence par chaîne : aucun nœud `import`/`from`, un garde AST naïf ne voit rien ; `makemigrations --check` passe ; la CI est verte. Résultats : (a) le lien Adhesion↔Licence, entre deux propriétaires, n'est catalogué nulle part — AD-9 nomme les liens **intra**-`adhesions` (représentant, mineur, consentement) et ignore les liens inter-apps ; (b) le couplage vit désormais dans le schéma : l'épic 3 ne peut plus refactorer sa table sans casser l'épic 5 en silence (aucun test de l'épic 3 ne touche `Licence`), et réciproquement ; (c) « le partage passe par `domaine/` » (AD-3) est contourné en esprit : la donnée elle-même est partagée par clé étrangère. Même famille d'angles morts, tous invisibles à la garde : `importlib.import_module("application.adhesions…")` et `getattr(module, "…")` par chaîne ; gabarits — `{% url "adhesions:etape" %}` ou `{% include "adhesions/extrait.html" %}` dans un gabarit de `membres` crée un couplage réel qu'aucune AD ne régit (et l'épic 3 peut renommer son URL, CI verte chez lui, page cassée chez l'épic 4) ; `application/gabarits/` est un dossier commun sans convention de nommage, et les épics 4 et 5 y écrivent **en parallèle** (deux `detail.html`, résolution par ordre de chargement — une demi-journée perdue par un bénévole) ; réglages — `INSTALLED_APPS`, `TEMPLATES` sont des chaînes, hors de tout garde.

**Sévérité : haute** (AD-3 est la règle structurante du projet et sa garde promise, écrite naïvement, ne ferme que la moitié du couplage).

**Correctif :** AD-3 resserrée (ou AD-17) — aucune dépendance inter-apps par identifiant de chaîne : ni FK de schéma ni clé naturelle (`ForeignKey("app.…")` interdit), ni gabarit ni URL ni réglage ; un lien entre entités de propriétaires différents est déclaré dans le domaine (identifiant porté par l'entité, jointure par requête ou service du domaine) et entre au catalogue AD-9 comme les entités ; la garde apps se spécifie **avant** d'être écrite : AST des imports + scan des chaînes `"app.` dans les modèles et migrations + balises `{% url %}`/`{% include %}` des gabarits + `importlib` ; convention de nommage des gabarits par app.

### A4 — mypy s'arrête à la frontière : les adaptateurs ne sont jamais vérifiés contre leurs ports (haute)

**Paire divergente :** adaptateurs des épics 2 à 5, écrits chacun par sa propre épic — p. ex. dépôt des saisons (épic 2) ↔ dépôt des adhésions (épic 3), tous deux consommés par la requête ligne adhérent (épic 4) et par les services du domaine.

**Scénario.** mypy strict sur `domaine/` garantit la cohérence **interne** du noyau : les entités et les signatures des ports sont typées. Mais l'exécution traverse l'adaptateur, et la décision du 21/11 exclut `application/` du typage (django-stubs différé). Chaque bâtisseur d'adaptateur choisit donc seul ses conventions, toutes conformes : AD-2 (implémente le port via l'ORM, sans règle métier), AD-9 (dans son app), ruff vert, ses tests verts. L'adaptateur de l'épic 2 retourne `None` quand la ligne n'existe pas (le réflexe ORM : `.first()`) ; celui de l'épic 3 lève une exception du domaine ; le domaine, lui, a déclaré **une** signature — aucun outil ne compare l'implémentation au port. Si le port promet une `Saison` et que l'adaptateur rend `None` sur un chemin, c'est un `AttributeError` en production sur un parcours non couvert par les tests de l'épic qui a livré l'adaptateur (parcours d'une autre épic — cf. A8). Deuxième divergence de la même famille : la forme temporelle. « Fuseau Europe/Paris explicite » est une convention, mais **quelle forme** entre dans les services du domaine — `date`, `datetime` naïf, `datetime` conscient ? La conversion vit dans chaque adaptateur, non typée : l'épic 2 appelle « la saison en cours à une date donnée » (AD-13) avec une date pure, l'épic 3 avec un horodatage UTC du webhook converti ou non — une heure d'écart aux bordures, exactement ce que la convention croyait fermer. Troisième : le mapping modèle↔entité (champ oublié, silencieux).

**Sévérité : haute** (c'est la réponse directe à la question du mandat : oui, deux apps peuvent diverger dans `application/` en restant « conformes » — mypy ne le verra jamais).

**Correctif :** chaque port déclaré dans le domaine l'est **avec son contrat d'erreur** (introuvable = exception nommée du domaine, jamais `None`) et sa forme temporelle (une seule) ; vérifier les adaptateurs contre les ports : mypy ciblé sur les seuls fichiers d'adaptateurs (faisable sans django-stubs complet) ou un test de conformité par adaptateur ; à défaut, inscrire au Deferred que la frontière port↔adaptateur est non vérifiée — un risque assumé, pas un confort.

### A5 — Entrer au catalogue est gratuit : recouvrement de champs et raccordement RGPD ne sont contrôlés par personne (haute)

**Paire divergente :** epic-adhesions-paiement (`Adherent` livré, minimisation RGPD) ↔ epic-federation (découverte de l'API réelle au deep-recon).

**Scénario.** `Adherent` porte l'état civil minimal (minimisation, R9). La recherche API de l'épic 5 découvrira presque certainement que la FFME exige des champs qu'`Adherent` n'a pas (une licence fédérale demande l'état civil complet). Le bâtisseur de l'épic 5 ne peut pas importer `adhesions` (AD-3), ne peut pas migrer l'entité d'un autre sans le dire — sauf que rien ne l'interdit non plus : la clause du 04/11 (« décision avec l'app propriétaire, jamais une migration silencieuse ») n'a **pas** été adoptée. Face à sa date de livraison, il a un chemin entièrement conforme : créer une entité nouvelle (`FicheFederation`), la faire entrer au catalogue — AD-9 le permet expressément (« toute nouvelle entité entre au catalogue avant d'être persistée » : l'entrée n'est refusée par personne — la persister dans son app (AD-4 : un propriétaire, `federation`), y accéder par ports du domaine (AD-2, AD-5), traduire le protocole dans son adaptateur (AD-5). CI verte. Résultat : l'état civil de la même personne existe en deux exemplaires chez deux propriétaires ; l'orchestrateur d'effacement (AD-11, livré à l'épic 1) ne connaît pas la nouvelle entité — **aucun texte ne rend le raccordement obligatoire à l'entrée au catalogue** : AD-11 s'applique aux écritures qui traversent, pas à la naissance d'une entité. L'utilisateur qui exerce R2 garde ses données personnelles chez `federation` : non-conformité RGPD, CI verte, et la story 6 de l'épic 1 (« les entités des épics suivantes s'y raccorderont ») est une intention de story, pas une règle.

**Sévérité : haute** (contournement conforme au catalogue d'une protection RGPD déjà annoncée au club).

**Correctif :** AD-9 resserrée — l'entrée au catalogue est un acte contrôlé : (a) recouvrement interdit, une entité nouvelle ne recoupe pas les champs d'une entité existante, et les champs exigés par un système tiers appartiennent à l'entité propriétaire, étendus par décision prise avec elle (reprendre la clause perdue du 04/11) ; (b) toute entité portant des données personnelles est raccordée à l'orchestrateur d'effacement **avant sa première persistance**, raccordement testé (cf. A6).

### A6 — L'accroche et l'orchestrateur n'ont pas de propriétaire de test : CI verte ≠ unités compatibles (haute)

**Paire divergente :** epic-adhesions-paiement ↔ epic-federation pour le point d'accroche licence×parcours ; epic-comptes-permissions (story 6) ↔ épics 3 et 5 pour l'orchestrateur d'effacement.

**Scénario.** AD-10 impose que l'accroche soit déclarée et composée dans `config/` — elle impose **où**, pas **qui teste**. L'épic 3 teste son parcours sans licence : c'est son boundary explicite (« parcours sans licence ») et chaque test vert est fondé. L'épic 5 teste le port FFME et son service, avec le bouchon et ses fixtures à elle. Le câblage dans `config/` — le seul endroit où les deux se rencontrent — n'est testé par aucune des deux unités : chacune peut croire légitimement que l'autre couvre l'intégration. La CI, autorité du 21/11, est verte des deux côtés : elle prouve chaque morceau, jamais l'assemblage. Même structure pour l'orchestrateur : livré à l'épic 1 sur le seul `Compte`, étendu par chaque épic suivante. L'extension du **code du domaine** est à peu près forcée par le seuil de couverture (une branche non testée fait plonger la mesure du paquet) — mais l'**adaptateur ORM** du raccordement (l'anonymisation effective des lignes MySQL) vit dans `application/`, sans seuil ni obligation : un raccordement écrit sans test d'intégration traverse la CI. AD-8 énumère des contrôles par **zone** (domaine sans base, application sur MySQL, migrations) ; aucun contrôle par **contrat**. C'est la démonstration directe demandée par le mandat : la CI verte peut être atteinte par deux unités quand même incompatibles.

**Sévérité : haute** (les mécanismes de protection existent tous — accroche AD-10, orchestrateur AD-11 — mais rien ne prouve jamais qu'ils fonctionnent assemblés).

**Correctif :** AD-8 resserrée — toute story qui introduit ou étend un point d'accroche, un orchestrateur multi-propriétaires ou un câblage de `config/` apporte **dans la même PR** le test d'intégration du contrat complet (parcours avec licence branchée sur le bouchon, effacement avec toutes les entités raccordées, sur MySQL) ; le test d'un contrat transversal appartient à l'unité qui le **complète**, pas à celles qui fournissent les morceaux.

### A7 — Une permission nouvelle n'atteint jamais les rôles semés (moyenne)

**Paire divergente :** story 3 de l'épic comptes (« permissions et six rôles semés ») ↔ toute story d'une épic suivante qui déclare une permission.

**Scénario.** La story 3 sème les six rôles avec les permissions qui existent — celles de `comptes` (décision du 15/11 : « ensembles écrits à la volée dans la story 3, jeu initial simple et modifiable dans l'admin »). L'épic 2 déclare ensuite `saisons.configurer` : identifiant stable dans le domaine, format unique, AD-14 obéie à la lettre. Mais la répartition de cette permission dans les rôles semés — le président doit-il pouvoir configurer les saisons ? — n'est régie par aucune AD : AD-14 fixe le vocabulaire et « rôles en données », pas la **mise à jour** des données au fil des épics. Trois constructions toutes conformes : (a) une migration de données par épic ajoute la permission aux rôles ; (b) un re-seed « au premier démarrage » mal écrit la réinjecte à chaque redémarrage et **écrase les ajustements faits dans l'admin par le club** — la modification dans l'admin est pourtant une décision explicite de l'épic ; (c) personne ne fait rien : la fonctionnalité est livrée, CI verte, et le président découvre un refus à l'écran — et le critère R3 (« le refus opposé à un compte dépourvu ») **passe quand même**, puisque le refus est le comportement par défaut. Une vérification qui réussit sur une fonctionnalité inaccessible à tous : le trou se déguise en succès.

**Sévérité : moyenne** (fonctionnalité livrée mais invisible ; risque d'écrasement silencieux des réglages du club).

**Correctif :** AD-14 resserrée — toute nouvelle permission arrive avec sa répartition initiale dans les rôles semés, par migration de données idempotente qui ne réécrit jamais une attribution existante (semer seulement l'absent) ; le test de la story vérifie qu'un compte portant le rôle cible exerce la fonctionnalité nouvelle.

### A8 — Couverture mesurée sur le domaine seul : l'érosion de `application/` est invisible par construction (moyenne)

**Paire divergente :** dépôt ORM de l'épic 3 (construit et testé avec ses parcours) ↔ requête ligne adhérent de l'épic 4 qui le consomme (et tout consommateur croisé futur : correction via la liste, effacement anonymisant).

**Scénario.** Le seuil pytest-cov ne porte que sur `domaine/` ; les tests du domaine tournent sur des faux dépôts ; la vérité du mapping modèle↔entité, elle, vit dans les adaptateurs de `application/`, mesurés par personne. L'épic 3 teste **ses** parcours (création, paiement HelloAsso, saisie hors ligne) ; les chemins du dépôt que seuls d'autres épics traversent — la lecture agrégée de l'épic 4, la correction, l'anonymisation — n'apparaissent dans aucun décompte : la couverture de `application/` peut descendre à mesure que les épics s'empilent sans qu'aucun chiffre ne le montre. L'érosion se concentre précisément sur les chemins transversaux, ceux qu'aucune épic ne teste deux fois. Combiné à l'exclusion de mypy (A4) : `application/` est une zone sans mesure sémantique — ruff en voit la surface, jamais le sens. C'est la réponse directe à la question du mandat : oui, le seuil sur le seul domaine masque l'érosion côté application, et il la masque au moment exact où elle compte (les contrats transversaux de A2, A5, A6).

**Sévérité : moyenne** (dégradation lente, mais structurelle pour un projet maintenu par des repreneurs bénévoles).

**Correctif :** ligne Outillage resserrée — seuil de couverture bas sur `application/` (p. ex. 60 % au départ, relevable au fil des épics), ciblé d'abord sur les dépôts et adaptateurs ; à défaut, couverture d'`application/` mesurée et rapportée sans seuil, pour que l'érosion au moins se **voie**.

---

## Paires retestées sans trou propre

- **comptes ↔ saisons** : aucune entité partagée ; le seul contact reste les permissions — le trou du lien permission→rôles (A7) vaut pour toutes les épics, sans collision propre à cette paire.
- **comptes ↔ membres** : absorbé par AD-9/AD-11/AD-12 pour la forme et l'effacement ; l'affichage des lignes anonymisées dans la liste historique est couvert par le contrat de requête demandé en A2, pas un trou séparé.
- **saisons ↔ membres** : la lecture de `Saison` par la liste reste couverte par AD-12/AD-13 ; le tri de l'export et l'état d'adhésion inclus sont dans A2.
- **saisons ↔ fédération** : dater une licence par saison reste une lecture croisée — la généralisation « toute lecture inter-apps par requête nommée » proposée le 04/11 n'a pas été adoptée, la paire reste donc dans l'angle mort de A3/A5 ; pas de collision propre autre.
- **membres ↔ fédération** : la décision du 26/10 (« liste et export sans état de licence ») tient toujours ; le jour de la re-découpe anticipée, l'accroche exigera le test d'intégration de A6 — fragilité déjà notée le 04/11, pas un trou neuf.

## Bilan

Fil rouge des huit attaques : les AD du 26/10 régissent les **unités**, celles du 04/11 ont fermé les **formes et les maisons** (catalogue, composition, orchestrateur, requête, calculs uniques), les contrôles du 21/11 mesurent des **zones** (domaine, apps, migrations) — ce qui reste ouvert, ce sont les **clés** (unicités métier, identité d'une personne à travers les saisons) et les **contrats** (contenu sémantique des requêtes, contrat d'erreur des ports, liens entre propriétaires, raccordements successifs, et le test des contrats). Chaque attaque est une CI verte avec deux unités néanmoins incompatibles : l'autorité du 21/11 ne peut pas voir ce qu'aucun de ses contrôles ne compare. Enfin, la protection a rétréci en trois points : les clauses « un individu n'a qu'une entité personne », « clé d'identification requise / décision avec l'app propriétaire » et « toute lecture inter-apps par requête nommée » proposées le 04/11 n'ont pas été reprises dans les AD adoptées — A1, A3 et A5 s'y engouffrent ; les reprendre est la moitié du correctif.

| # | Trou | Sévérité | Correctif proposé |
| --- | --- | --- | --- |
| A1 | Unicité métier personne×saison non régie — double adhésion, double encaissement, double licence | critique | AD-16 nouvelle : unicités fonctionnelles déclarées au catalogue et portées en base |
| A2 | Contenu de la ligne adhérent sans contrat (états inclus, photo vs encaissé, anonymisés, ordre) | haute | AD-12 resserrée (+ AD-13 sur l'écart photo/encaissé) |
| A3 | Dépendances inter-apps par chaîne (FK, gabarits, urls, importlib) invisibles à la garde | haute | AD-3 resserrée + spec de la garde apps avant son écriture |
| A4 | Frontière port↔adaptateur jamais vérifiée (mypy domaine seul) | haute | Contrat d'erreur et forme temporelle des ports + conformité des adaptateurs |
| A5 | Entrée au catalogue sans contrôle de recouvrement ni raccordement RGPD | haute | AD-9 resserrée (reprendre les clauses perdues du 04/11) |
| A6 | Accroches et orchestrateurs sans propriétaire de test | haute | AD-8 resserrée : test d'intégration dans la PR qui complète le contrat |
| A7 | Permission nouvelle sans mise à jour des rôles semés | moyenne | AD-14 resserrée : migration de données idempotente, testée |
| A8 | Couverture d'`application/` non mesurée — érosion invisible | moyenne | Ligne Outillage resserrée : seuil bas sur application/, relevable |

Ordre de fermeture recommandé : **A1 avant le raffinement de l'épic 3** (la clé d'identité et l'unicité conditionnent la découpe des stories souscription, HelloAsso et paiement hors ligne, et le futur contrat FFME) ; **A5 avant le deep-recon de l'épic 5** (l'entité parallèle est le chemin naturel du bâtisseur face à l'API réelle) ; **A3 en même temps que la spec de la garde apps** (promise par l'AD-3 amendée, à écrire avant la story qui l'implémente) ; **A2 avant le raffinement de l'épic 4** ; **A6 dès l'épic 1** (le premier raccordement à l'orchestrateur est la story 6) ; A4, A7, A8 aux raffinements des épics 3 et 4.
