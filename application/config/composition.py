"""Composition : câblage des ports du domaine vers leurs adaptateurs.

C'est ici que le domaine rencontre la persistance : les vues demandent un
dépôt via cette fabrique, jamais directement l'ORM.
"""

from application.comptes.depots import DepotComptesDjango
from domaine.ports.depots import DepotComptes


def depot_comptes() -> DepotComptes:
    """Retourne le dépôt des comptes, câblé sur l'ORM Django."""
    return DepotComptesDjango()
