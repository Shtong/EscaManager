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

## Structure du dépôt

```text
domaine/          bibliothèque de domaine, paquet pur (AD-1) : entités, ports, requêtes, services
application/      projet Django, l'unique adaptatrice
  config/         réglages (variables d'environnement seules), URLs, câblage port/adaptateur (AD-10)
  comptes/        épic 1 : comptes, modèle, dépôt ORM, vue d'accueil
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
