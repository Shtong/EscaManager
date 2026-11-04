# Prise en main d'EscaManager — guide du repreneur bénévole

Mis à jour : 04/11/2026. Ce guide est court et veut le rester : il ne remplace pas l'ossature d'architecture (`architecture-escamanager.md`), qui fait autorité — il vous met en selle. Si le code contredit ce guide, on corrige le guide d'abord.

## Ce que c'est

EscaManager gère les adhésions du SCB Escalade (club d'escalade de Beaucouzé) : comptes des membres, saisons et leurs options, adhésions avec paiement (HelloAsso en ligne, paiements hors ligne enregistrés à la main), liste des adhérents avec export tableur, et licences FFME. C'est la première partie du projet ; les exigences exactes vivent dans l'initiative (`../initiative-escamanager.md`).

## Comment c'est construit

Deux morceaux :

- **`domaine/`** — le cœur : les entités du club (Compte, Permission, Saison, Option, Adhesion, Paiement, Adherent, Licence), les règles métier, et des « ports » (interfaces de lecture/écriture et d'accès aux services extérieurs). Du Python pur : il ne connaît ni le web, ni la base de données. Il se teste sans base.
- **`application/`** — le projet Django, unique consommatrice du domaine : pages, formulaires, admin, accès à la base (MySQL via l'ORM), clients HelloAsso et FFME. Une app par périmètre : `comptes`, `saisons`, `adhesions`, `membres`, `federation` ; leur composition (routage, câblage) vit dans `config/`.

Les règles en une phrase : **le métier vit dans `domaine/`, le web vit dans `application/`, et jamais l'un ne contourne l'autre** ; une app n'importe jamais une autre ; toute écriture passe par un service du domaine ; chaque page marche sans JavaScript ; tout changement passe la CI avant fusion. Les quatorze règles complètes (AD-1 à AD-14) sont dans l'ossature.

## La pile

Python 3.13 · Django 5.2 LTS · MySQL 8.4 · mysqlclient · GitHub + GitHub Actions · hébergé sur un PaaS (un conteneur, gunicorn, fichiers statiques servis par l'application).

## Pour travailler dessus

1. Cloner le dépôt ; installer Python 3.13 et l'outil de gestion des dépendances du projet (voir `pyproject.toml`).
2. Récupérer les variables d'environnement nécessaires (jamais de secret dans le code) ; lancer le serveur local depuis `application/`.
3. Lancer les tests : le domaine sans base, l'application sur MySQL.
4. Modifier, tester, pousser : GitHub Actions vérifie tests et migrations ; on ne fusionne que CI verte.

## Pour entretenir

- **Correctifs** : rester sur la branche Django 5.2 LTS, prendre les versions de sécurité — la CI vous protège.
- **Schéma de données** : uniquement par migrations Django, jamais à la main dans la base.
- **Une règle d'architecture à changer** : la changer d'abord dans l'ossature (les identifiants AD ne se renumérotent jamais), puis dans le code ; le `.memlog.md` adjacent garde le pourquoi de chaque décision.

## Où trouver quoi

- Les exigences du produit : `../initiative-escamanager.md` et les épics dans `../tickets/`.
- Les décisions d'architecture et leur historique : `architecture-escamanager.md` et `.memlog.md`.
- Les termes du club (adhésion, saison, licence…) : `../glossaire.md`.

## En cas de pépin

- **Le site ne répond plus** : la console du PaaS (logs) et l'état du dernier déploiement dans GitHub Actions.
- **Une adhésion payée n'apparaît pas** : regarder les logs de l'adaptateur HelloAsso (webhooks) ; les paiements sont idempotents — rejouer une notification ne duplique rien.
- **Une licence FFME reste inconnue** : l'adaptateur vit dans `application/federation/` avec un bouchon si l'API n'est pas encore branchée.
