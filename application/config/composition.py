"""Composition : câblage des ports du domaine vers leurs adaptateurs.

C'est ici, que le domaine rencontre la persistance : les vues demandent un
repository via cette factory, jamais directement l'ORM.
"""

from application.comptes.depots import DepotComptesDjango
from domaine.ports.depots import DepotComptes


def depot_comptes() -> DepotComptes:
    """Retourne le repository des comptes, câblé sur l'ORM Django."""
    return DepotComptesDjango()
