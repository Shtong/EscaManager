---
type: architecture-review
lens: adversarial
target: _bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md
units: epic-comptes-permissions, epic-saisons, epic-adhesions-paiement, epic-liste-adherents, epic-federation
date: 2026-11-04
status: final
---

# Revue adverse — ossature EscaManager, première partie

## Verdict

L'ossature empêche efficacement les écarts de *discipline* (imports, couches, SQL, CI) mais rien ne régit les *contrats entre unités* : huit trous constructibles, dont trois critiques, tous fermables par six AD nouveaux et deux resserrages — à faire avant le raffinement des épics 3, 4 et 5.

## Méthode

Entités du domaine énumérées depuis l'ossature, l'initiative et les tickets : **Compte**, **Permission**, **Saison**, **Option**, **Adhesion**, **Paiement** (implicite, R6), **Adherent** (majeur titulaire ou mineur de R9), **Licence**, plus la relation *représentant légal de*. Les dix paires d'épics ont été testées systématiquement ; pour chacune, j'ai cherché deux unités qui obéissent à la lettre aux huit AD et produisent pourtant des formes de données, des propriétaires ou des chemins de mutation incompatibles. Les paires sans trou propre sont nommées en fin de revue.

---

## Trous

### T1 — L'entité `Adherent` est citée par le seed et n'appartient à personne (critique)

**Paire divergente :** epic-comptes-permissions ↔ epic-adhesions-paiement ↔ epic-liste-adherents.

**Scénario.** Le seed structurel liste `Adherent` dans `domaine/entites/`, mais la Capability Map ne l'attribue à aucune app (elle ne nomme que Compte, Permission, Saison, Option, Adhesion, Licence). AD-4 énonce « une entité, un propriétaire » sans jamais fixer le catalogue : l'AD est inapplicable faute de destinateur. Or trois épics ont un besoin légitime et disjoint :

- l'épic comptes construit `Compte` avec des données personnelles (R2) — pour elle, la personne existe dès le compte, une ligne = un utilisateur ;
- l'épic adhésions doit représenter l'adhérent *mineur de R9, qui n'a pas de compte* — pour elle, la personne existe dès la souscription, rattachée au compte du représentant ;
- l'épic membres doit afficher « la liste des adhérents » (R7) — pour elle, une ligne = une personne.

Chaque épic obéit à la lettre : sa persistance dans sa propre app (AD-4), tout accès par des services du domaine (AD-2), aucun import croisé (AD-3). Résultat : deux tables et deux formes de la même personne physique, aucune n'étant interdite. Aggravations : R2 fait du titulaire un correcteur de ses données (app comptes) et R7 de l'équipe un correcteur de la liste (app membres) — deux chemins de mutation des mêmes données personnelles, sans maison commune ; et le mineur de 2026/2027 devenu majeur crée un compte en 2027/2028 — deux enregistrements du même individu, aucune clé de dédoublonnage régie, alors même que la FFME (R10) raisonne, elle, en « personne déjà licenciée ».

**AD-9 proposé (nouveau) — Catalogue des entités et de leurs propriétaires.**

- **Binds :** tous — `domaine/entites/`, les cinq apps.
- **Prevents :** deux définitions ou deux tables de la même personne physique ; entité citée dans l'ossature sans propriétaire ; corrections de la même donnée par deux apps.
- **Rule :** le catalogue des entités et de l'app propriétaire de leur persistance est tenu dans l'ossature et à jour (proposition : Compte, Permission → comptes ; Saison, Option → saisons ; Adherent, Adhesion, Paiement → adhesions ; Licence → federation) ; les données personnelles d'un adhérent vivent uniquement dans `Adherent`, `Compte` ne porte que l'authentification et la relation représentant→adhérents ; une app non propriétaire accède à une entité uniquement par les ports de lecture du domaine ; un individu physique n'a qu'une entité personne, quelle que soit l'année.

### T2 — Le parcours d'adhésion doit porter la licence, mais l'adaptateur FFME vit dans l'app `federation` (critique)

**Paire divergente :** epic-adhesions-paiement ↔ epic-federation.

**Scénario.** L'épic fédération promet « pour chaque adhésion, l'état de la licence est connu » — la vérification s'insère donc *dans* le parcours d'adhésion. Mais le parcours appartient à l'app `adhesions` (livrée en production par l'épic 3, avec boundary explicite « parcours sans licence »), tandis que la Capability Map place R10 dans `application/federation`. Les deux épics obéissent à la lettre : l'épic 3 n'importe rien et ne touche pas à la licence ; l'épic 5 met port dans `domaine/ports/` et adaptateur dans son app (AD-5). L'incompatibilité est structurelle : pour que la vue d'adhésion obtienne l'adaptateur qui vit dans `federation`, il faut un import croisé qu'AD-3 interdit ; l'alternative observée en pratique est que l'épic 5 aille réécrire des vues et des gabarits de l'app `adhesions` — l'épic écrit alors dans une app qui n'est pas la sienne et la Capability Map ment. L'ossature n'a ni racine de composition (qui instancie et injecte les adaptateurs ?) ni point d'accroche nommé dans le parcours (où la licence s'insère-t-elle sans réécrire le parcours ?).

**AD-10 proposé (nouveau) — Racine de composition unique.**

- **Binds :** R5, R9, R10 — `application/config`, `adhesions`, `federation`.
- **Prevents :** import croisé pour câbler un adaptateur ; réécriture du parcours d'adhésion par l'épic fédération ; bouchon câblé en dur dans une vue.
- **Rule :** `application/config` est la racine de composition — le seul endroit qui instancie les adaptateurs (HelloAsso, FFME) et les injecte dans les services du domaine ; aucune vue ni service d'app n'instancie d'adaptateur ni n'importe une autre app projet ; le parcours d'adhésion livré par l'épic 3 expose un point d'accroche nommé (service de domaine + bloc de gabarit) où la vérification de licence s'insère à l'épic 5 sans toucher au reste du parcours.

### T3 — L'effacement RGPD traverse trois propriétaires et se heurte à une inscription fédérale irréversible (critique)

**Paire divergente :** epic-comptes-permissions ↔ epic-adhesions-paiement ↔ epic-federation.

**Scénario.** L'épic comptes implémente R2 « effacer mes données » comme effacement du `Compte` — un service du domaine, une transaction : AD-4 obéi à la lettre. L'épic adhésions persiste `Adherent`, `Adhesion`, `Paiement` — des données personnelles du même individu chez un autre propriétaire, mutées par d'autres services. L'épic fédération a enregistré le licencié auprès de la FFME (R10) — fait externe irréversible. Trois incompatibilités : (a) l'effacement du compte laisse intactes, ou rend orphelines, les données portées par l'autre app — l'app comptes ne peut pas composer la transaction transverse sans import interdit par AD-3 ; (b) l'obligation financière (paiement enregistré « avec son moyen », reçu HelloAsso) milite pour conservation/anonymisation, que personne n'a le mandat de décider ; (c) le critère d'acceptation de R2 (« effacement effectif ») est structurellement inhonorisable pour la part fédérale — sans AD, la réponse sera un mensonge de conformité ou un refus improvisé. Cas mineurs non régi au passage : qui peut demander l'effacement des données d'un mineur, et jusqu'à quand ?

**AD-11 proposé (nouveau) — Mutations transverses et périmètre d'effacement.**

- **Binds :** R2, R9, R10 — comptes, adhesions, federation.
- **Prevents :** effacement partiel silencieux ; promesse RGPD inhonorisable ; mutation multi-propriétaires impossible à composer.
- **Rule :** toute mutation qui traverse plusieurs entités possédées par des apps différentes passe par un unique service orchestrateur du domaine (p. ex. `effacer_donnees_personnelles`) qui coordonne les dépôts de chaque app via `domaine/ports/` ; la politique d'effacement est définie une fois pour toutes : anonymisation des adhésions et paiements conservés pour obligation financière, effacement des données du mineur à la demande du représentant, mention affichée à l'utilisateur que la licence enregistrée auprès de la FFME est irréversible et hors du périmètre d'effacement ; la demande d'effacement d'un compte entraîne celle des adhérents qui lui sont rattachés.

### T4 — Le bouchon FFME et le vrai client : le contrat du port n'est régí par personne (haute)

**Paire divergente :** epic-comptes-permissions (socle qui crée le port et son bouchon) ↔ epic-federation (qui découvre l'API réelle) — avec epic-adhesions-paiement comme tierce liée via la forme de `Adherent`.

**Scénario.** AD-5 dit « le port FFME vit avec un bouchon jusqu'à la recherche API », mais ne dit ni qui écrit le bouchon, ni ce qu'il simule, ni ce qui gèle le contrat. Le socle (épic 1) crée le port ; personne ne le consomme avant l'épic 5 (boundary « parcours sans licence ») ; le bouchon encode donc la sémantique que son auteur imagine. À l'épic 5, la deep-recon découvre l'API réelle. Divergences toutes légitimes au regard des AD : (a) le bouchon renvoie un booléen « déjà licencié », l'API réelle distingue *pas de licence / licence expirée / licence dans un autre club / licence active ici* — l'adaptateur « traduit » en booléen et perd l'information : refus à tort d'un adhérent ou doublon enregistré auprès de la fédération ; (b) la clé de vérification : le bouchon prend (nom, prénom), l'API exige l'état civil complet — or la clé provient de l'entité `Adherent`, possédée par l'épic 3 (T1) : l'épic 5 doit faire migrer une entité qui n'est pas à elle ; (c) le bouchon ne simule ni erreur ni délai — le parcours n'a jamais été testé en échec avant la production fédérale. Chaque unité respecte AD-5 (port dans `domaine/ports/`, adaptateur seul à connaître le protocole) ; ce qui diverge, c'est le contrat lui-même.

**AD-5 resserré (proposition).**

- **Rule (ajout) :** chaque port externe est accompagné d'un contrat écrit dans le dépôt — états de retour nommés (jamais un booléen), clé d'identification requise, erreurs et délais simulables — *avant* sa première consommation ; le bouchon implémente le contrat en entier, chemins d'échec compris ; la recherche API de l'épic 5 peut réécrire l'adaptateur librement, mais ne change le port que par décision d'architecture enregistrée ; si l'API réelle exige des champs absents d'une entité existante, l'ajout est une décision prise avec l'app propriétaire de l'entité, jamais une migration silencieuse.

### T5 — La « ligne adhérent » n'a pas de maison, et « corriger la liste » ouvre un second chemin d'écriture (haute)

**Paire divergente :** epic-liste-adherents ↔ epic-adhesions-paiement (epic-comptes-permissions en tiers via R2).

**Scénario.** R7 exige une liste qui « reflète les adhésions enregistrées » et se *corrige* ; R8 un export tableur. L'épic membres obéit : pages et export lisent via des services du domaine (AD-2), sans importer `adhesions` (AD-3). Mais deux constructions restent ouvertes : la liste est-elle une liste d'*adhésions* (le panier du représentant : options, paiements, mineurs dedans) ou d'*adhérents* (une ligne par personne, le mineur séparé, le représentant en colonne — lecture littérale de R9) ? Le mappage adhésion→ligne est une règle métier ; si elle vit dans un sérialiseur ou un gabarit de l'app membres, elle contourne AD-2 *en pratique* — AD-2 régit les lectures/écritures d'entités, pas la définition des projections. L'export, lui, fige de facto LA forme canonique de « la liste des adhérents » du club, décidée seul par l'épic 4. Deuxième fissure : « corriger la liste » (R7) et « corriger ses données » (R2) sont deux chemins de mutation des mêmes données personnelles — AD-4 régit la persistance, pas la pluralité des chemins d'écriture via services du domaine ; qui arbitre si l'équipe corrige le nom du mineur et que le représentant corrige autrement ? Troisième tentation : filtrer/trier/paginer peut pousser l'épic 4 à matérialiser une table dénormalisée — l'épic 3 écrit sans pouvoir la prévenir (AD-3 interdit l'import) : deux formes persistées de la même donnée, synchronisation non régie, exactement le « deux rédacteurs » qu'AD-4 croit interdire mais qui n'est couvert que pour les entités, pas pour les projections.

**AD-12 proposé (nouveau) — Requêtes de lecture nommées et projections.**

- **Binds :** R7, R8 — membres ; toute lecture inter-apps.
- **Prevents :** forme canonique de la « ligne adhérent » définie dans une vue, un gabarit ou un sérialiseur ; copie dénormalisée divergente ; corrections concurrentes non réconciliées.
- **Rule :** toute donnée lue par une app non propriétaire passe par une requête nommée du domaine ; la projection « ligne d'adhérent » (une ligne par adhérent, mineur séparé, représentant en colonne, options et paiements agrégés) est définie une fois dans `domaine/` et sert à la fois la page et l'export — l'export n'est qu'un rendu de la même projection ; « corriger la liste » et « corriger ses données » empruntent le même service du domaine, seule règle de conciliation ; aucune app ne persiste une copie d'une donnée possédée par une autre app (ni table dénormalisée ni cache écrit) dans cette première partie.

### T6 — « Saison à venir ou en cours » et le prix : règles dérivées duplicables, photo tarifaire non tranchée (moyenne)

**Paire divergente :** epic-saisons ↔ epic-adhesions-paiement (epic-liste-adherents en tiers pour l'export).

**Scénario.** Trois unités affichent l'état d'une saison et son offre : la page de consultation de l'épic saisons (R4 : « la configuration s'observe dans ce que voit un adhérent »), le parcours de souscription de l'épic adhésions (R5 : « adhère à une saison à venir ou en cours »), la liste de l'épic membres (R7 : « n'importe quelle saison »). L'épic adhésions, ne pouvant importer l'app `saisons` (AD-3), écrit son propre service du domaine pour décider quelles saisons proposer — chaque service passe par le domaine (AD-2 obéi à la lettre), mais rien n'interdit deux services du domaine qui tranchent différemment la même question : bordure d'éligibilité (strictement entre bornes ? créneau d'ouverture ?), et surtout l'instant de bascule — « dates ISO en interne » ne fixe pas le fuseau, minuit UTC et minuit Europe/Paris décalent la bascule d'une heure : le soir du 31 août, la page de l'épic 2 peut montrer la saison N+1 « en cours » pendant que le parcours de l'épic 3 la montre « à venir ». Même fissure sur le prix : R4 permet de corriger les prix en cours de saison ; l'adhésion de septembre affiche-t-elle le prix payé ou le prix courant de l'option ? L'épic 3 veut figer (montant dû), l'épic 2 veut refléter la config, l'épic 4 exporte l'un ou l'autre — aucune AD sur la photo tarifaire.

**AD-13 proposé (nouveau) — Une règle dérivée, un service, une vérité.**

- **Binds :** R4, R5, R6, R7 — saisons, adhesions, membres.
- **Prevents :** deux services du domaine qui décident différemment de la même question ; prix d'adhésion ambigu après correction de la saison.
- **Rule :** toute règle dérivée d'une entité (état d'une saison, éligibilité à la souscription, prix d'un panier) n'existe que dans un seul service du domaine, nommé dans l'ossature et appelé par tous les consommateurs ; les instants de bascule sont calculés dans un fuseau unique fixé une fois pour toutes ; une adhésion fige à la souscription sa photo tarifaire (options choisies et montant) — les corrections ultérieures de la saison ne réécrivent jamais une adhésion enregistrée.

### T7 — Trois chemins concurrents confirment le même paiement, aucune règle d'idempotence (moyenne)

**Paire divergente :** stories de epic-adhesions-paiement (retour de redirection HelloAsso, notification HelloAsso, saisie manuelle hors ligne) ↔ epic-liste-adherents (lecteur du résultat).

**Scénario.** R6 : « chaque paiement abouti est enregistré avec son moyen » ; le détail du flux HelloAsso est Deferred, donc trois stories arriveront séparément : confirmation synchrone au retour de redirection, notification asynchrone, enregistrement manuel. Chaque story obéit à AD-4 à la lettre : un service du domaine, une transaction. L'incompatibilité est *entre* les chemins, pas dans les unités : retour + notification confirment le même encaissement → deux `Paiement` pour un paiement réel ; une saisie manuelle (chèque) suivie d'une notification tardive d'un paiement carte → adhésion payée deux fois, ou deux vérités concurrentes que la liste (T5) affichera selon son humeur. AD-4 régit l'atomicité d'une mutation, ni l'idempotence ni la concurrence entre mutations — l'ossature est le seul endroit où poser la règle avant la découpe de l'épic 3.

**AD-4 resserré (proposition).**

- **Rule (ajout) :** tout service du domaine qui enregistre un fait déclenché depuis l'extérieur est idempotent sous une clé d'unicité fonctionnelle (identifiant de paiement HelloAsso, référence de saisie manuelle) ; un paiement abouti n'est confirmé qu'une fois, quel que soit le chemin d'arrivée ; les écritures concurrentes sur une même adhésion convergent — contrainte d'unicité en base et un seul service de confirmation.

### T8 — Le mécanisme de vérification des permissions est unique, le catalogue ne l'est pas (moyenne)

**Paire divergente :** epic-comptes-permissions ↔ toutes les autres (chaque app protège ses pages).

**Scénario.** La convention dit « permissions vérifiées par un mécanisme unique » ; l'épic comptes livre le mécanisme et l'entité `Permission` (R3 : rôles = ensembles, jamais codés en dur). Les épics 2 à 5 obéissent : chacune protège ses pages par le mécanisme. Mais aucune AD ne dit qui *déclare* les codes de permission, dans quel espace de noms, ni où ils sont recensés : l'épic 4 peut déclarer `consulter_liste` pendant que l'épic 3 déclare `lister_adherents` pour une intention voisine, ou deux codes pour la même action — les rôles nommés du club (président, trésorier…) deviennent inassemblables proprement, et le critère R3 (« refus opposé à un compte dépourvu de la permission requise ») se vérifie permission par permission sans que personne garantisse unicité ni couverture.

**AD-14 proposé (nouveau) — Espace de noms des permissions.**

- **Binds :** R3 — comptes + toute app qui protège une action.
- **Prevents :** codes dupliqués ou incohérents entre épics ; rôles nommés impossibles à composer ; vérification contournée.
- **Rule :** chaque permission porte un code préfixé par son app (`comptes.`, `saisons.`, `adhesions.`, `membres.`, `federation.`), déclaré uniquement dans les migrations de son app et recensé dans l'ossature ; attribution, vérification et composition des rôles passent uniquement par le mécanisme de comptes ; une action protégée correspond à exactement une permission.

---

## Paires testées sans trou propre

- **comptes ↔ saisons** : aucune entité partagée ; seul point de contact = les permissions (T8). Pas de divergence de forme de données constructible.
- **comptes ↔ membres** : entièrement absorbé par T1 (forme de la personne) et T5 (projection, corrections).
- **comptes ↔ fédération** : la vérification « personne déjà licenciée » repose sur l'identité de la personne — couvert par T1 (forme) et T3 (effacement). Rien d'autre : la licence ne touche pas au compte.
- **saisons ↔ membres** : la liste lit `Saison` (R7 « n'importe quelle saison ») — couvert par AD-12 (requêtes nommées) et T6 (état de saison). Pas de trou propre.
- **saisons ↔ fédération** : dans la réalité fédérale, une licence est annuelle et calée sur la saison sportive ; ni R10 ni l'ossature ne relient `Licence` à `Saison`. Si l'épic 5 veut dater une licence par saison, c'est une lecture croisée de `Saison` — couvert par AD-12. Sinon, pas de collision.
- **membres ↔ fédération** : tranché par la décision du 26/10 (« liste et export sans état de licence ») — mais c'est une *décision d'initiative*, pas un AD, avec re-découpe explicitement anticipée si le club la veut à l'export. Le jour de la re-découpe, le trou T2 (racine de composition) s'y propage : l'app membres devra, elle aussi, obtenir l'adaptateur FFME sans import croisé. Fragilité notée, pas un trou nouveau.

## Bilan

Les huit trous sont d'une même famille : les AD actuels régissent chaque unité prise isolément — app, entité, couche, fusion — et la structure statique qui en résulte est solide. Rien ne régit les **contrats entre unités** : le catalogue des entités et de leurs propriétaires (T1), le câblage des adaptateurs entre apps et l'accroche du parcours (T2), la composition des mutations transverses avec le cas RGPD (T3), la sémantique des ports et de leurs bouchons (T4), les projections de lecture et l'unicité des chemins d'écriture (T5), les règles dérivées partagées et la photo tarifaire (T6), l'idempotence entre chemins concurrents (T7), le catalogue des permissions (T8). Ordre de fermeture recommandé : **T1 d'abord** (il conditionne la découpe des épics 3 et 4 et le contrat FFME), **T2 et T3 avant le raffinement de l'épic 3** (l'épic 3 doit livrer son point d'accroche et savoir où vivent les données personnelles qu'on lui demandera d'effacer), puis T4 à T8 avant le raffinement des épics 4 et 5.
