from django.shortcuts import render

from application.config.composition import depot_comptes
from domaine.requetes import compter_comptes


def accueil(requete):
    """Page d'accueil : décompte des comptes"""
    nombre = compter_comptes(depot_comptes())
    return render(requete, "accueil.html", {"nombre_comptes": nombre})
