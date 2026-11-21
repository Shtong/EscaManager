"""Tests du domaine, sans aucune base : un faux dépôt suffit."""

import pytest

from domaine.requetes import compter_comptes


class FauxDepotComptes:
    """Dépôt en mémoire : le domaine se teste sans MySQL."""

    def __init__(self, nombre: int) -> None:
        self._nombre = nombre

    def compter(self) -> int:
        return self._nombre


@pytest.mark.parametrize("nombre", [0, 1, 2, 13])
def test_compter_comptes_renvoye_le_decompte_du_depot(nombre: int) -> None:
    assert compter_comptes(FauxDepotComptes(nombre)) == nombre
