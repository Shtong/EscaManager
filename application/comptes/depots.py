"""Adaptateur du port « DepotComptes » sur l'ORM Django (AD-2).

Le domaine déclare l'interface dans ``domaine/ports/depots.py`` ; seule
l'application connaît la persistance.
"""

from application.comptes.modeles import CompteDjango
from domaine.ports.depots import DepotComptes


class DepotComptesDjango(DepotComptes):
    """Décompte des comptes lu dans MySQL via l'ORM."""

    def compter(self) -> int:
        return CompteDjango.objects.count()
