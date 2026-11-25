"""Services d'écriture des comptes : une mutation = un service.

Chaque service exécute dans la transaction ouverte par l'adaptateur au
moment de l'appel du port. Le mot de passe transite en clair jusqu'au
port, jamais au-delà : l'adaptateur le hache.
"""

from domaine.entites.compte import Compte
from domaine.ports.depots import DepotComptes


class CourrielDejaUtilise(Exception):
    """L'adresse de courriel est déjà rattachée à un compte."""


class CompteInconnu(Exception):
    """Aucun compte ne porte cette adresse de courriel."""


def inscrire_compte(depot: DepotComptes, courriel: str, mot_de_passe: str) -> Compte:
    """Inscrit un compte frais, inactif tant que l'adresse n'est pas
    confirmée, ou relance une inscription jamais confirmée.

    Adresse portée par un compte actif : refus. Adresse portée par un
    compte inactif : le mot de passe saisi remplace l'ancien et le
    compte inactif est retourné, pour que l'appelant renvoie le
    courriel de confirmation. Adresse inconnue : création. Deux
    chemins d'écriture ne créent jamais deux fois le même compte.
    """
    compte = depot.trouver(courriel)
    if compte is None:
        return depot.creer(courriel, mot_de_passe)
    if compte.actif:
        raise CourrielDejaUtilise(f"Un compte existe déjà avec l'adresse {courriel}.")
    depot.changer_mot_de_passe(courriel, mot_de_passe)
    return compte


def confirmer_compte(depot: DepotComptes, courriel: str) -> None:
    """Active le compte portant cette adresse.

    Idempotent : un compte déjà actif ne change pas, rejouer le lien de
    confirmation ne fait rien. Un compte inconnu est refusé.
    """
    compte = depot.trouver(courriel)
    if compte is None:
        raise CompteInconnu(f"Aucun compte ne porte l'adresse {courriel}.")
    if not compte.actif:
        depot.activer(courriel)


def reinitialiser_mot_de_passe(
    depot: DepotComptes, courriel: str, mot_de_passe: str
) -> None:
    """Remplace le mot de passe du compte portant cette adresse.

    Un compte inconnu est refusé : aucun changement silencieux.
    """
    if depot.trouver(courriel) is None:
        raise CompteInconnu(f"Aucun compte ne porte l'adresse {courriel}.")
    depot.changer_mot_de_passe(courriel, mot_de_passe)
