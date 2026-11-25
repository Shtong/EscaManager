# EscaManager, SCB Escalade

Gestion en ligne des adhésions du SCB Escalade, club d'escalade à but non
lucratif de Beaucouzé : comptes, saisons, adhésions et paiement, liste des
adhérents, licences FFME.

## Installation locale

Prérequis : [Python 3.13](https://www.python.org/) et [Docker](https://www.docker.com/)
(pour la base MySQL locale).

```bash
python -m venv .venv
# ou pour Windows : .venv\Scripts\activate
# ou pour Linux/macOS : source .venv/bin/activate
pip install -e ".[dev]"
docker compose up -d --wait
```

## Variables d'environnement

Toute la configuration passe par des variables d'environnement.
En local, créez un fichier `.env` à la racine du dépôt (non suivi par git).
Il sera chargé au démarrage, sans pour autant écraser les variables d'environnement déjà existantes.

| Variable | Obligatoire | Défaut | Rôle |
| --- | --- | --- | --- |
| `SECRET_KEY` | oui | (aucun) | Clé secrète Django ; l'application refuse de démarrer sans elle |
| `DATABASE_URL` | oui | (aucun) | Base MySQL, par ex. `mysql://root:root@127.0.0.1:3306/escamanager` |
| `DEBUG` | non | faux | `1`, `true`, `vrai` ou `oui` pour le mode debug |
| `ALLOWED_HOSTS` | non | `127.0.0.1,localhost` | Hôtes autorisés, séparés par des virgules |
| `DEFAULT_FROM_EMAIL` | non | `ne-pas-repondre@escaladescb.fr` | Expéditeur des courriels de confirmation et de réinitialisation |

Contenu minimal du `.env` local :

```dotenv
SECRET_KEY=une-cle-longue-et-secrete
DATABASE_URL=mysql://root:root@127.0.0.1:3306/escamanager
```

## Démarrer l'application en local

```bash
python manage.py migrate
python manage.py runserver
```

## Parcours des comptes en local

L'inscription, la connexion et la réinitialisation du mot de passe sont
ouvertes sous `/comptes/` : inscription, courriel de confirmation,
confirmation par lien valable 72 heures, connexion, espace personnel,
déconnexion.

En local, aucun courriel ne part vraiment : le backend console écrit
chaque message dans la console de `runserver`, lien de confirmation ou
de réinitialisation compris ; ouvrez-le depuis la console pour
poursuivre le parcours. L'envoi réel par Brevo est différé au registre
du travail ; l'expéditeur affiché vient de `DEFAULT_FROM_EMAIL`.

## Tests

Les gardes et les tests du domaine tournent sans aucune base ; le `.env`
local fournit les variables que les réglages exigent :

```bash
pytest tests/test_imports_domaine.py tests/test_imports_apps.py tests/test_typographie.py tests/domaine -q --cov=domaine --cov-report=term-missing
```

Les tests de l'application exigent la base MySQL locale :

```bash
docker compose up -d --wait
pytest tests/application -q
```

Aucune migration ne doit manquer au dépôt :

```bash
python manage.py makemigrations --check --dry-run
```

## CI (GitHub Actions)

Chaque fusion traverse la CI, et seulement après CI verte. Deux jobs :

- Domaine et qualité, sans base : lint et format (`ruff check .` puis
  `ruff format --check .`), typage strict du domaine (`mypy`), gardes
  d'imports et de typographie, tests du domaine couverts au seuil de
  90 pour cent.
- Application, sur MySQL 8.4 comme en production (jamais SQLite) :
  vérification qu'aucune migration ne manque, puis tests de
  l'application.

## Structure du dépôt

```text
domaine/          bibliothèque de domaine, paquet pur (AD-1) : entités, ports, requêtes, services
application/      projet Django, l'unique adaptatrice
  config/         réglages (variables d'environnement seules), URLs, câblage port/adaptateur (AD-10)
  comptes/        épic 1 : comptes, modèle utilisateur, dépôt ORM, jetons, formulaires, parcours
  gabarits/       gabarits HTML en français, sans JavaScript
  static/         feuilles de style
tests/            gardes d'imports (AD-1, AD-3), tests du domaine (sans base), tests de l'application (MySQL)
```

## Stack technique

Socle technique :
- Python 3.13
- Django 5.2
- MySQL 8.4

Une bibliothèque de domaine pure (`domaine/`) contient les entités, et définit les opérations de données disponibles.
Une unique application Django (`application/`) l'adapte au web. Les quinze règles d'architecture (AD-1 à AD-15) vivent dans
`_bmad-output/initiative-escamanager/architecture-escamanager/architecture-escamanager.md`.
