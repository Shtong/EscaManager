"""Implémentation du port DepotComptes sur l'ORM Django.

Le domaine déclare l'interface dans ``domaine/ports/depots.py``.
"""

from application.comptes.modeles import CompteDjango
from domaine.ports.depots import DepotComptes


class DepotComptesDjango(DepotComptes):
    def compter(self) -> int:
        return CompteDjango.objects.count()
