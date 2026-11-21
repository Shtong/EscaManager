"""Tests du contrat du port DepotComptes, sans aucune
base : un port est une interface, seule l'application l'implémente.
"""

import pytest

from domaine.ports.depots import DepotComptes


def test_le_port_ne_peut_pas_etre_instancie() -> None:
    """Un port est abstrait : le domaine ne fournit aucune implémentation,
    seule l'application câble un dépôt concret (AD-10)."""
    with pytest.raises(TypeError):
        DepotComptes()


def test_la_methode_du_port_n_est_pas_implementee() -> None:
    """Contrat du port : une implémentation doit fournir 'compter', la
    méthode de base refuse tout appel résiduel plutôt que de mentir sur
    le décompte."""

    class DepotNu(DepotComptes):
        """Dépôt factice qui délègue à la méthode de base du port."""

        def compter(self) -> int:
            return super().compter()

    with pytest.raises(NotImplementedError):
        DepotNu().compter()
