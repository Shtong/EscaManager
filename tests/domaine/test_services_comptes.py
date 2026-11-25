"""Tests des services d'écriture des comptes, sans aucune base : un
faux dépôt en mémoire suffit.

Le faux dépôt garde le mot de passe tel qu'il arrive au port : le
service doit le transporter en clair jusqu'ici, et uniquement
jusqu'ici.
"""

import pytest

from domaine.entites.compte import Compte
from domaine.ports.depots import DepotComptes
from domaine.services.comptes import (
    CompteInconnu,
    CourrielDejaUtilise,
    confirmer_compte,
    inscrire_compte,
    reinitialiser_mot_de_passe,
)


class FauxDepotComptes(DepotComptes):
    """Dépôt en mémoire : comptes par courriel, mots de passe reçus,
    activations jouées."""

    def __init__(self) -> None:
        self.comptes: dict[str, Compte] = {}
        self.mots_de_passe: dict[str, str] = {}
        self.activations: list[str] = []

    def compter(self) -> int:
        return len(self.comptes)

    def creer(self, courriel: str, mot_de_passe: str) -> Compte:
        compte = Compte(courriel=courriel)
        self.comptes[courriel] = compte
        self.mots_de_passe[courriel] = mot_de_passe
        return compte

    def trouver(self, courriel: str) -> Compte | None:
        return self.comptes.get(courriel)

    def activer(self, courriel: str) -> None:
        self.activations.append(courriel)
        ancien = self.comptes[courriel]
        self.comptes[courriel] = Compte(courriel=ancien.courriel, actif=True)

    def changer_mot_de_passe(self, courriel: str, mot_de_passe: str) -> None:
        self.mots_de_passe[courriel] = mot_de_passe


def test_l_inscription_cree_un_compte_inactif() -> None:
    """Un compte inscrit est inactif : la confirmation l'activera ; le
    mot de passe transite en clair jusqu'au port, sans détour."""
    depot = FauxDepotComptes()

    compte = inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")

    assert compte.courriel == "adherent@scb-escalade.fr"
    assert compte.actif is False
    assert depot.mots_de_passe["adherent@scb-escalade.fr"] == "mot-de-passe"


def test_l_inscription_refuse_un_courriel_deja_utilise() -> None:
    """Une adresse portée par un compte confirmé : refus, aucun
    doublon n'est créé."""
    depot = FauxDepotComptes()
    inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")
    confirmer_compte(depot, "adherent@scb-escalade.fr")

    with pytest.raises(CourrielDejaUtilise):
        inscrire_compte(depot, "adherent@scb-escalade.fr", "autre")

    assert depot.compter() == 1
    assert depot.mots_de_passe["adherent@scb-escalade.fr"] == "mot-de-passe"


def test_la_reinscription_d_un_compte_non_confirme_remplace_le_mot_de_passe() -> None:
    """Une adresse inscrite mais jamais confirmée : la ré-inscription
    remplace le mot de passe, retourne le compte inactif pour le renvoi
    du courriel, ne crée aucun doublon."""
    depot = FauxDepotComptes()
    inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")

    compte = inscrire_compte(depot, "adherent@scb-escalade.fr", "autre")

    assert depot.compter() == 1
    assert compte.courriel == "adherent@scb-escalade.fr"
    assert compte.actif is False
    assert depot.mots_de_passe["adherent@scb-escalade.fr"] == "autre"
    assert depot.activations == []


def test_la_confirmation_active_un_compte_neuf() -> None:
    """La confirmation active le compte inscrit, une seule fois."""
    depot = FauxDepotComptes()
    inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")

    confirmer_compte(depot, "adherent@scb-escalade.fr")

    assert depot.trouver("adherent@scb-escalade.fr").actif is True
    assert depot.activations == ["adherent@scb-escalade.fr"]


def test_la_confirmation_est_idempotente() -> None:
    """Un compte déjà actif ne change pas : rejouer le lien de
    confirmation ne refait aucune écriture."""
    depot = FauxDepotComptes()
    inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")
    confirmer_compte(depot, "adherent@scb-escalade.fr")

    confirmer_compte(depot, "adherent@scb-escalade.fr")

    assert depot.trouver("adherent@scb-escalade.fr").actif is True
    assert depot.activations == ["adherent@scb-escalade.fr"]


def test_la_confirmation_refuse_un_compte_inconnu() -> None:
    """Confirmer une adresse sans compte : refus explicite, aucune
    écriture silencieuse."""
    depot = FauxDepotComptes()

    with pytest.raises(CompteInconnu):
        confirmer_compte(depot, "inconnu@scb-escalade.fr")

    assert depot.activations == []


def test_la_reinitialisation_change_le_mot_de_passe() -> None:
    """La réinitialisation remplace le mot de passe du compte connu."""
    depot = FauxDepotComptes()
    inscrire_compte(depot, "adherent@scb-escalade.fr", "mot-de-passe")

    reinitialiser_mot_de_passe(
        depot, "adherent@scb-escalade.fr", "nouveau-mot-de-passe"
    )

    assert depot.mots_de_passe["adherent@scb-escalade.fr"] == "nouveau-mot-de-passe"


def test_la_reinitialisation_refuse_un_compte_inconnu() -> None:
    """Réinitialiser une adresse sans compte : refus explicite."""
    depot = FauxDepotComptes()

    with pytest.raises(CompteInconnu):
        reinitialiser_mot_de_passe(
            depot, "inconnu@scb-escalade.fr", "nouveau-mot-de-passe"
        )

    assert depot.mots_de_passe == {}
