"""Tests de la page d'accueil — sur MySQL, jamais SQLite (AD-7).

Prouvent la chaîne complète : page → domaine → dépôt → ORM → MySQL.
"""

import pytest

from application.comptes.depots import DepotComptesDjango
from application.comptes.modeles import CompteDjango
from django.db.utils import OperationalError


@pytest.mark.django_db
def test_accueil_base_vide_affiche_zero(client) -> None:
    reponse = client.get("/")

    assert reponse.status_code == 200
    assert "Aucun compte" in reponse.content.decode("utf-8")


@pytest.mark.django_db
def test_accueil_affiche_le_decompte_depuis_mysql(client) -> None:
    CompteDjango.objects.create(courriel="presidente@scb-escalade.fr")
    CompteDjango.objects.create(courriel="secretaire@scb-escalade.fr")

    reponse = client.get("/")

    assert reponse.status_code == 200
    assert "2 comptes sont enregistrés" in reponse.content.decode("utf-8")


def _compter_base_injoignable(self) -> int:
    """Ce que l'ORM lève quand MySQL est absente (erreur 2003)."""
    raise OperationalError(2003, "Can't connect to MySQL server on '127.0.0.1' (111)")


def test_accueil_base_injoignable_repond_500_journalisee(
    client, monkeypatch, caplog
) -> None:
    """Matrice « Base injoignable » : une erreur de connexion remonte du
    port ; la page rend une erreur 500 standard Django, journalisée —
    jamais d'exception avalée."""
    monkeypatch.setattr(DepotComptesDjango, "compter", _compter_base_injoignable)
    # Attribut du client (pas un paramètre d'appel) : sans lui, l'exception
    # serait relancée dans le test au lieu de rendre la 500.
    client.raise_request_exception = False

    reponse = client.get("/")

    assert reponse.status_code == 500
    erreurs = [
        journal
        for journal in caplog.records
        if journal.name == "django.request" and journal.levelname == "ERROR"
    ]
    assert erreurs, "l'erreur devait être journalisée via django.request"
