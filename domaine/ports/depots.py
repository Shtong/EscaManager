"""Ports de persistance — les seules interfaces par lesquelles le domaine
voit les données (AD-2, AD-5).

L'app Django en fournit les implémentations ; le domaine n'en connaît que
la forme.
"""

from abc import ABC, abstractmethod


class DepotComptes(ABC):
    """Port de lecture des comptes."""

    @abstractmethod
    def compter(self) -> int:
        """Nombre de comptes enregistrés."""
        raise NotImplementedError
