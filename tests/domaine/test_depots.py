"""Tests du contrat du port DepotComptes, sans aucune
base : un port est une interface, seule l'application l'implémente.
"""

import pytest

from domaine.entites.compte import Compte
from domaine.ports.depots import DepotComptes


def test_le_port_ne_peut_pas_etre_instancie() -> None:
    """Un port est abstrait : le domaine ne fournit aucune implémentation,
    seule l'application câble un dépôt concret."""
    with pytest.raises(TypeError):
        DepotComptes()


class DepotNu(DepotComptes):
    """Dépôt factice qui délègue chaque méthode à la base du port."""

    def compter(self) -> int:
        return super().compter()

    def creer(self, courriel: str, mot_de_passe: str) -> Compte:
        return super().creer(courriel, mot_de_passe)

    def trouver(self, courriel: str) -> Compte | None:
        return super().trouver(courriel)

    def activer(self, courriel: str) -> None:
        super().activer(courriel)

    def changer_mot_de_passe(self, courriel: str, mot_de_passe: str) -> None:
        super().changer_mot_de_passe(courriel, mot_de_passe)


def test_les_methodes_du_port_refusent_tout_appel_residuel() -> None:
    """Contrat du port : une implémentation doit fournir chaque méthode ;
    la méthode de base refuse tout appel résiduel plutôt que de mentir
    sur un décompte ou une écriture."""
    depot = DepotNu()

    with pytest.raises(NotImplementedError):
        depot.compter()
    with pytest.raises(NotImplementedError):
        depot.creer("adherent@scb-escalade.fr", "mot-de-passe")
    with pytest.raises(NotImplementedError):
        depot.trouver("adherent@scb-escalade.fr")
    with pytest.raises(NotImplementedError):
        depot.activer("adherent@scb-escalade.fr")
    with pytest.raises(NotImplementedError):
        depot.changer_mot_de_passe("adherent@scb-escalade.fr", "mot-de-passe")
