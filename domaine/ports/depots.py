"""Ports de persistance : les seules interfaces par lesquelles le domaine
voit les données.

L'app Django en fournit les implémentations ; le domaine n'en connaît que
la forme. Le mot de passe voyage en clair au seul moment de l'appel du
port : c'est l'adaptateur qui le hache avant de le stocker.
"""

from abc import ABC, abstractmethod

from domaine.entites.compte import Compte


class DepotComptes(ABC):
    """Port des comptes : lectures et écritures."""

    @abstractmethod
    def compter(self) -> int:
        """Nombre de comptes enregistrés."""
        raise NotImplementedError

    @abstractmethod
    def creer(self, courriel: str, mot_de_passe: str) -> Compte:
        """Crée un compte inactif ; le mot de passe est haché par
        l'adaptateur, jamais persisté en clair."""
        raise NotImplementedError

    @abstractmethod
    def trouver(self, courriel: str) -> Compte | None:
        """Compte portant cette adresse, ou None s'il n'en existe pas."""
        raise NotImplementedError

    @abstractmethod
    def activer(self, courriel: str) -> None:
        """Marque le compte comme actif."""
        raise NotImplementedError

    @abstractmethod
    def changer_mot_de_passe(self, courriel: str, mot_de_passe: str) -> None:
        """Remplace le mot de passe du compte ; le hachage vit dans
        l'adaptateur."""
        raise NotImplementedError
