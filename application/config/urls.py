"""Routage d'EscaManager : la composition des parcours vit ici."""

from django.urls import path

from application.comptes.views import (
    Connexion,
    Deconnexion,
    DemandeReinitialisation,
    NouveauMotDePasse,
    ReinitialisationEnvoyee,
    ReinitialisationTerminee,
    accueil,
    confirmer_inscription,
    espace,
    inscription,
    inscription_envoyee,
)

urlpatterns = [
    path("", accueil, name="accueil"),
    path("comptes/inscription/", inscription, name="inscription"),
    path(
        "comptes/inscription/envoyee/",
        inscription_envoyee,
        name="inscription_envoyee",
    ),
    path(
        "comptes/confirmer/<str:jeton>/",
        confirmer_inscription,
        name="confirmer_inscription",
    ),
    path("comptes/connexion/", Connexion.as_view(), name="connexion"),
    path("comptes/deconnexion/", Deconnexion.as_view(), name="deconnexion"),
    path("comptes/espace/", espace, name="espace"),
    path(
        "comptes/reinitialisation/",
        DemandeReinitialisation.as_view(),
        name="reinitialisation_demande",
    ),
    path(
        "comptes/reinitialisation/envoyee/",
        ReinitialisationEnvoyee.as_view(),
        name="reinitialisation_envoyee",
    ),
    path(
        "comptes/reinitialisation/terminee/",
        ReinitialisationTerminee.as_view(),
        name="reinitialisation_terminee",
    ),
    path(
        "comptes/reinitialisation/<uidb64>/<token>/",
        NouveauMotDePasse.as_view(),
        name="reinitialisation_nouveau_mot_de_passe",
    ),
]
