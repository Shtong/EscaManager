"""Réglages Django d'EscaManager, pilotés exclusivement par des variables
d'environnement : aucun secret dans le code, aucun réglage propre
à un hébergeur.

En local, un petit chargeur stdlib lit le fichier ".env" à la racine du
dépôt s'il existe, sans jamais écraser les variables déjà présentes.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Racine du dépôt : application/config/settings.py → deux niveaux au-dessus.
BASE_DIR = Path(__file__).resolve().parents[2]


def _charger_env(chemin: Path) -> None:
    """Charge un fichier ".env" s'il existe, sans écraser l'environnement."""
    if not chemin.is_file():
        return
    # utf-8-sig : un éventuel BOM en tête de fichier ne doit pas polluer la
    # première clé (U+FEFF survit à strip()).
    for ligne in chemin.read_text(encoding="utf-8-sig").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, _, valeur = ligne.partition("=")
        cle = cle.strip()
        valeur = valeur.strip().strip('"').strip("'")
        if cle and cle not in os.environ:
            os.environ[cle] = valeur


_charger_env(BASE_DIR / ".env")


def _variable_obligatoire(nom: str) -> str:
    """Lit une variable obligatoire, déclenche une erreur en cas d'absence"""
    valeur = os.environ.get(nom, "").strip()
    if not valeur:
        raise ImproperlyConfigured(
            f"La variable d'environnement {nom} est obligatoire : renseignez-la "
            "(par exemple dans un fichier .env local, voir README.md) avant de démarrer."
        )
    return valeur


# Sécurité -----------------------------------------------------------------

SECRET_KEY = _variable_obligatoire("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "").strip().lower() in {"1", "true", "vrai", "oui"}

_hotes = os.environ.get("ALLOWED_HOSTS", "").strip()
ALLOWED_HOSTS = [hote.strip() for hote in _hotes.split(",") if hote.strip()] or [
    "127.0.0.1",
    "localhost",
]

# Applications et middleware ------------------------------------------------

INSTALLED_APPS = [
    # Volontairement minimale : ni auth, ni sessions, ni admin.
    "django.contrib.staticfiles",
    "application.comptes",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "application.config.urls"
WSGI_APPLICATION = "application.config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "application" / "gabarits"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

# Base de données -------------------------------------------------------------

_variable_obligatoire("DATABASE_URL")
try:
    DATABASES = {"default": dj_database_url.config(env="DATABASE_URL", conn_max_age=60)}
except dj_database_url.UnknownSchemeError as exc:
    raise ImproperlyConfigured(
        "La variable d'environnement DATABASE_URL doit désigner une base MySQL "
        f"(schéma inconnu : '{exc}')."
    ) from exc
if DATABASES["default"]["ENGINE"] != "django.db.backends.mysql":
    moteur_recu = DATABASES["default"]["ENGINE"]
    raise ImproperlyConfigured(
        "La variable d'environnement DATABASE_URL doit désigner une base MySQL "
        f"(moteur reçu : '{moteur_recu}')."
    )
DATABASES["default"]["OPTIONS"] = {
    **DATABASES["default"].get("OPTIONS", {}),
    "charset": "utf8mb4",
}
DATABASES["default"]["TEST"] = {
    **DATABASES["default"].get("TEST", {}),
    "CHARSET": "utf8mb4",
}

# Fichiers statiques -----------------------------------------------------------
# WhiteNoise sert les fichiers statiques sans dépendre d'un hébergeur

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "statique"
STATICFILES_DIRS = [BASE_DIR / "application" / "static"]
WHITENOISE_USE_FINDERS = True

# Langue et fuseau ---------------------------------------------------------------

LANGUAGE_CODE = "fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# Courriels ----------------------------------------------------------------------
# Backend console : aucun envoi réel pour l'instant

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Divers ---------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Journalisation standard : tout à la console.

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
