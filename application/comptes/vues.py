"""Vues de l'app « comptes » — la page d'accueil, nourrie par le domaine.

Tant qu'un seul app nourrit la page d'accueil, la vue vit ici ; le câblage
du dépôt reste dans ``application/config/composition.py`` (AD-10).
"""

from django.shortcuts import render

from application.config.composition import depot_comptes
from domaine.requetes import compter_comptes


def accueil(requete):
    """Page d'accueil : décompte des comptes, lu par le domaine (AD-2)."""
    nombre = compter_comptes(depot_comptes())
    return render(requete, "accueil.html", {"nombre_comptes": nombre})
