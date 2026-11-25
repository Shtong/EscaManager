"""Compte utilisateur Django, adaptateur de l'entité Compte du domaine.

Le courriel est l'identifiant ; un compte frais est inactif jusqu'à la
confirmation de son adresse. Sans PermissionsMixin : les permissions
vivent dans le domaine, pas dans le mécanisme des permissions de modèle.
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class GestionnaireComptes(BaseUserManager):
    """Gestionnaire du modèle utilisateur : création avec hachage du mot
    de passe, jamais de stockage en clair."""

    def create_user(self, courriel: str, mot_de_passe: str, **champs):
        if not courriel:
            raise ValueError("L'adresse de courriel est obligatoire.")
        compte = self.model(courriel=self.normalize_email(courriel), **champs)
        compte.set_password(mot_de_passe)
        compte.save(using=self._db)
        return compte

    def create_superuser(self, courriel: str, mot_de_passe: str, **champs):
        champs.setdefault("is_active", True)
        return self.create_user(courriel, mot_de_passe, **champs)


class CompteDjango(AbstractBaseUser):
    """Compte persisté, identifié par son adresse de courriel."""

    courriel = models.EmailField("courriel", unique=True)
    is_active = models.BooleanField("actif", default=False)

    objects = GestionnaireComptes()

    USERNAME_FIELD = "courriel"
    # Le courriel est aussi l'adresse de contact : les parcours de
    # réinitialisation de Django cherchent le champ par ce nom.
    EMAIL_FIELD = "courriel"

    class Meta:
        db_table = "comptes_compte"
        verbose_name = "compte"
        verbose_name_plural = "comptes"

    def __str__(self) -> str:
        return self.courriel
