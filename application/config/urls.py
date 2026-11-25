"""Routage d'EscaManager"""

from django.urls import path

from application.comptes.vues import accueil

urlpatterns = [
    path("", accueil, name="accueil"),
]
