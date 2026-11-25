"""Implémentation du port DepotComptes sur l'ORM Django.

Le domaine déclare l'interface dans ``domaine/ports/depots.py`` ; chaque
écriture s'exécute dans une transaction, et le mot de passe, transporté
en clair jusqu'ici, est haché avant toute persistance. Les exceptions
de l'ORM sont traduites ici en exceptions du domaine : une contrainte
d'unicité qui saute est un courriel déjà utilisé, une ligne disparue
entre deux lectures est un compte inconnu.
"""

from django.db import IntegrityError, transaction

from application.comptes.models import CompteDjango
from domaine.entites.compte import Compte
from domaine.ports.depots import DepotComptes
from domaine.services.comptes import CompteInconnu, CourrielDejaUtilise


def _vers_entite(compte: CompteDjango) -> Compte:
    """Projection du modèle Django vers l'entité du domaine."""
    return Compte(courriel=compte.courriel, actif=compte.is_active)


class DepotComptesDjango(DepotComptes):
    def compter(self) -> int:
        return CompteDjango.objects.count()

    def creer(self, courriel: str, mot_de_passe: str) -> Compte:
        try:
            with transaction.atomic():
                compte = CompteDjango.objects.create_user(courriel, mot_de_passe)
        except IntegrityError as exc:
            # Double soumission simultanée : la contrainte d'unicité de
            # la base parle, en français du domaine.
            raise CourrielDejaUtilise(
                f"Un compte existe déjà avec l'adresse {courriel}."
            ) from exc
        return _vers_entite(compte)

    def trouver(self, courriel: str) -> Compte | None:
        compte = CompteDjango.objects.filter(courriel__iexact=courriel).first()
        if compte is None:
            return None
        return _vers_entite(compte)

    def activer(self, courriel: str) -> None:
        with transaction.atomic():
            CompteDjango.objects.filter(courriel__iexact=courriel).update(
                is_active=True
            )

    def changer_mot_de_passe(self, courriel: str, mot_de_passe: str) -> None:
        try:
            with transaction.atomic():
                compte = CompteDjango.objects.get(courriel__iexact=courriel)
                compte.set_password(mot_de_passe)
                compte.save()
        except CompteDjango.DoesNotExist as exc:
            # La ligne a disparu entre la lecture du service et
            # l'écriture.
            raise CompteInconnu(f"Aucun compte ne porte l'adresse {courriel}.") from exc
