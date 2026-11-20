"""Persistance des comptes — adaptateur de l'entité « Compte » du domaine.

Aucune règle métier ici (AD-2) : les modèles ne portent que les données ;
les lectures passent par le domaine, les écritures passeront par ses
services.
"""

from django.db import models


class CompteDjango(models.Model):
    """Compte persisté, identifié par son adresse de courriel."""

    courriel = models.EmailField("courriel", unique=True)

    class Meta:
        db_table = "comptes_compte"
        verbose_name = "compte"
        verbose_name_plural = "comptes"

    def __str__(self) -> str:
        return self.courriel
