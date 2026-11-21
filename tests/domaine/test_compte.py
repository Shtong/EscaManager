"""Tests de l'entité « Compte » — première entité du catalogue (AD-9).

Sans aucune base : le domaine est un paquet pur (AD-1), l'entité se teste
telle quelle.
"""

import dataclasses

import pytest

from domaine.entites.compte import Compte


def test_un_compte_porte_le_courriel_donne() -> None:
    """Construction : le courriel passé au compte y reste."""
    compte = Compte(courriel="presidente@scb-escalade.fr")

    assert compte.courriel == "presidente@scb-escalade.fr"


def test_un_compte_refuse_toute_affectation() -> None:
    """Gel : l'entité est figée à la construction — une écriture directe
    d'attribut est refusée ; les mutations à venir passeront par un
    service du domaine (AD-4)."""
    compte = Compte(courriel="secretaire@scb-escalade.fr")

    with pytest.raises(dataclasses.FrozenInstanceError):
        compte.courriel = "autre@scb-escalade.fr"


def test_deux_comptes_de_meme_courriel_sont_egaux() -> None:
    """Égalité : deux comptes portant le même courriel sont le même
    compte, quel que soit le chemin qui les a construits."""
    premier = Compte(courriel="adherent@scb-escalade.fr")
    second = Compte(courriel="adherent@scb-escalade.fr")

    assert premier == second


def test_deux_comptes_de_courriels_differents_ne_sont_pas_egaux() -> None:
    """Contre-égalité : deux courriels différents, deux comptes distincts."""
    premier = Compte(courriel="adherent@scb-escalade.fr")
    second = Compte(courriel="presidente@scb-escalade.fr")

    assert premier != second
