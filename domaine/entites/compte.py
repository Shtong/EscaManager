"""Entité Compte, propriété de l'app comptes.

Volontairement minimale : un compte y est identifié par son adresse de
courriel, avec son état d'activation ; le mot de passe n'entre jamais
dans l'entité, il ne vit que dans l'adaptateur, haché.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Compte:
    """Compte d'une personne du club, identifié par son adresse de courriel.

    Un compte frais est inactif : il ne devient actif qu'après la
    confirmation de son adresse de courriel.
    """

    courriel: str
    actif: bool = False
