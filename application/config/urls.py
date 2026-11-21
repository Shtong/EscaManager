"""Routage d'EscaManager — URLs françaises (AD-3, AD-10)."""

from django.urls import path

from application.comptes.vues import accueil

urlpatterns = [
    path("", accueil, name="accueil"),
]
