# EscaManager — SCB Escalade

Gestion en ligne des adhésions du SCB Escalade, club d'escalade à but non
lucratif de Beaucouzé : comptes, saisons, adhésions et paiement, liste des
adhérents, licences FFME.

Socle technique : Python 3.13, Django 5.2 LTS, MySQL 8.4 — jamais SQLite,
même en local (écarts de collation). Une bibliothèque de domaine pure
(`domaine/`) porte les entités, les ports et les lectures ; une unique
application Django (`application/`) l'adapte au web. Les quinze règles
d'architecture (AD-1 à AD-15) vivent dans
`_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`.

## Installation locale

Prérequis : [Python 3.13](https://www.python.org/) et [Docker](https://www.docker.com/)
(pour la base MySQL locale).

```bash
python -m venv .venv
# Windows : .venv\Scripts\activate — Linux/macOS : source .venv/bin/activate
pip install -e ".[dev]"
docker compose up -d --wait
```

## Variables d'environnement

Toute la configuration passe par des variables d'environnement — aucun
secret dans le code. En local, créez un fichier `.env` à la racine du dépôt
(non suivi par git) ; un petit chargeur de
`application/config/settings.py` le lit automatiquement, sans jamais
écraser les variables déjà présentes.

| Variable | Obligatoire | Défaut | Rôle |
| --- | --- | --- | --- |
| `SECRET_KEY` | oui | — | Clé secrète Django ; l'application refuse de démarrer sans elle |
| `DATABASE_URL` | oui | — | Base MySQL, par ex. `mysql://root:root@127.0.0.1:3306/escamanager` |
| `DEBUG` | non | faux | `1`, `true`, `vrai` ou `oui` pour le mode debug |
| `ALLOWED_HOSTS` | non | `127.0.0.1,localhost` | Hôtes autorisés, séparés par des virgules |

Contenu minimal du `.env` local :

```dotenv
SECRET_KEY=une-cle-longue-et-secrete
DATABASE_URL=mysql://root:root@127.0.0.1:3306/escamanager
```

Sans `SECRET_KEY` ou `DATABASE_URL`, l'application refuse de démarrer avec
un message explicite.

## Démarrer

```bash
python manage.py migrate
python manage.py runserver
```

La page d'accueil <http://127.0.0.1:8000/> affiche le décompte des comptes,
lu dans MySQL par le domaine — y compris sur un écran étroit (≈375 px) et
sans JavaScript.

## Tests

Le domaine se teste sans aucune base ; l'application se teste sur la MySQL
locale.

```bash
pytest tests/test_imports_domaine.py tests/domaine -q   # garde AD-1 + domaine, sans aucune base
docker compose up -d --wait                             # MySQL locale
pytest tests/application -q                             # application, sur MySQL
python manage.py makemigrations --check --dry-run       # aucune migration ne doit manquer
```

## CI (GitHub Actions)

Toute fusion passe par la CI et n'a lieu qu'après CI verte (AD-8) :
`.github/workflows/ci.yml` exécute deux jobs — « Domaine — sans base »
(garde d'imports et tests du domaine, sans service MySQL) et
« Application — sur MySQL » (service MySQL 8.4, `makemigrations --check`,
tests de l'application).

## Déploiement différé

Pendant les premières phases du développement, rien n'est hébergé :
l'application s'exécute en local uniquement. Le code reste prêt pour le
jour J sans modification (AD-15 — neutralité d'hébergement) : point
d'entrée WSGI standard (`application/config/wsgi.py`), `Procfile`
(`web` gunicorn, `release` migrate), configuration exclusive par variables
d'environnement. La mise en production (piste Scalingo, addon MySQL 8.4) et
le compte Brevo sont suivis dans
`_bmad-output/initiative-escamanager/deferred-work.md`.

## Structure du dépôt

```text
domaine/          bibliothèque de domaine — paquet pur (AD-1) : entités, ports, requêtes, services
application/      projet Django — l'unique adaptatrice
  config/         réglages (variables d'environnement seules), URLs, câblage port/adaptateur (AD-10)
  comptes/        épic 1 : comptes — modèle, dépôt ORM, vue d'accueil
  gabarits/       gabarits HTML en français, sans JavaScript
  static/         feuilles de style
tests/            garde d'imports, tests du domaine (sans base), tests de l'application (MySQL)
```
