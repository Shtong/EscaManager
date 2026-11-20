"""Entité « Compte » — première entité du catalogue AD-9, propriété de l'app
« comptes ».

Volontairement minimale : un compte y est identifié par son adresse de
courriel, sans aucune logique d'authentification — celle-ci appartient aux
stories suivantes de l'épic comptes.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Compte:
    """Compte d'une personne du club, identifié par son adresse de courriel."""

    courriel: str
