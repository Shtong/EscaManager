"""Tests de démarrage — matrice « Variable obligatoire absente » et garde
du moteur MySQL (AD-7 : jamais SQLite, même en local).

Sans ``SECRET_KEY`` ou ``DATABASE_URL``, l'application refuse de démarrer
avec un message français explicite (échec rapide au lancement) ; une
``DATABASE_URL`` qui ne désigne pas MySQL est refusée de la même façon.
L'import des réglages est rejoué dans un processus neuf : c'est bien le
comportement « l'application refuse de démarrer » qui est vérifié, sans
toucher aux réglages déjà chargés par la session de tests.
"""

import os
import subprocess
import sys

import pytest

IMPORTER_REGLAGES = "import application.config.settings"


def _sous_processus(environnement: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", IMPORTER_REGLAGES],
        check=False,
        env=environnement,
        capture_output=True,
        text=True,
        timeout=120,
    )


@pytest.mark.parametrize("variable", ["SECRET_KEY", "DATABASE_URL"])
def test_sans_variable_obligatoire_le_demarrage_est_refuse(variable: str) -> None:
    """La variable testée est présente mais vide, l'autre renseignée —
    présente mais vide suffit : le chargeur .env n'écrase jamais une
    variable déjà dans l'environnement."""
    autre = "DATABASE_URL" if variable == "SECRET_KEY" else "SECRET_KEY"
    environnement = dict(os.environ)
    environnement["SECRET_KEY"] = ""
    environnement["DATABASE_URL"] = ""
    environnement[autre] = "valeur-de-remplacement"

    resultat = _sous_processus(environnement)

    assert resultat.returncode != 0, "le démarrage devait être refusé"
    assert variable in resultat.stderr
    assert "obligatoire" in resultat.stderr
    assert "avant de démarrer" in resultat.stderr


def test_refuse_de_demarrer_avec_sqlite() -> None:
    """Un DATABASE_URL sqlite doit être refusé, moteur nommé, en français."""
    environnement = dict(os.environ)
    environnement["SECRET_KEY"] = "cle-factice-pour-le-test"
    environnement["DATABASE_URL"] = "sqlite://"

    resultat = _sous_processus(environnement)

    sortie = resultat.stdout + resultat.stderr
    assert resultat.returncode != 0, "l'import des réglages devait être refusé"
    assert "ImproperlyConfigured" in sortie
    assert "django.db.backends.sqlite3" in sortie, "le moteur reçu doit être nommé"
    assert "MySQL" in sortie and "moteur" in sortie
