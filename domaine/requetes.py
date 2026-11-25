"""Requêtes de lecture du domaine.

Toute lecture affichée par l'application passe par ici : une vue ne compte
jamais les lignes elle-même.
"""

from domaine.ports.depots import DepotComptes


def compter_comptes(depot: DepotComptes) -> int:
    """Nombre de comptes enregistrés, lu via le port."""
    return depot.compter()
