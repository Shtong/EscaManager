"""Vues du parcours des comptes : inscription, confirmation, connexion,
déconnexion, réinitialisation, espace personnel.

Toute écriture passe par un service du domaine ; le routage et la
composition vivent dans ``application/config``.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from application.comptes.forms import (
    MESSAGE_COURRIEL_DEJA_UTILISE,
    FormulaireConnexion,
    FormulaireDemandeReinitialisation,
    FormulaireInscription,
    FormulaireNouveauMotDePasse,
)
from application.comptes.jetons import (
    VALIDITE_CONFIRMATION,
    fabriquer_jeton_confirmation,
    lire_jeton_confirmation,
)
from application.config.composition import depot_comptes
from domaine.requetes import compter_comptes
from domaine.services.comptes import (
    CompteInconnu,
    CourrielDejaUtilise,
    confirmer_compte,
    inscrire_compte,
)


class VueFormulaireFrancais:
    """Les vues génériques de Django nomment leur formulaire 'form' ;
    les gabarits du club l'attendent sous 'formulaire'."""

    def get_context_data(self, **kwargs):
        contexte = super().get_context_data(**kwargs)
        contexte["formulaire"] = contexte["form"]
        return contexte


def accueil(requete: HttpRequest) -> HttpResponse:
    """Page d'accueil : décompte des comptes"""
    nombre = compter_comptes(depot_comptes())
    return render(requete, "accueil.html", {"nombre_comptes": nombre})


def _envoyer_courriel_confirmation(requete: HttpRequest, courriel: str) -> None:
    """Courriel de confirmation : lien signé valable 72 heures, corps
    rendu depuis le gabarit."""
    jeton = fabriquer_jeton_confirmation(courriel)
    lien = requete.build_absolute_uri(reverse("confirmer_inscription", args=[jeton]))
    corps = render_to_string(
        "courriels/confirmation.html",
        {
            "lien": lien,
            "validite_heures": int(VALIDITE_CONFIRMATION.total_seconds() // 3600),
        },
        requete,
    )
    send_mail(
        "Confirmez votre compte EscaManager, SCB Escalade",
        corps,
        settings.DEFAULT_FROM_EMAIL,
        [courriel],
    )


def inscription(requete: HttpRequest) -> HttpResponse:
    """Inscription : la politique (création, relance d'une inscription
    non confirmée, refus d'un compte confirmé) vit dans le service du
    domaine ; la vue n'en garde que l'erreur de champ sur l'exception
    et l'envoi du courriel de confirmation."""
    if requete.method == "POST":
        formulaire = FormulaireInscription(requete.POST)
        if formulaire.is_valid():
            courriel = formulaire.cleaned_data["courriel"]
            try:
                inscrire_compte(
                    depot_comptes(),
                    courriel,
                    formulaire.cleaned_data["mot_de_passe"],
                )
            except CourrielDejaUtilise:
                formulaire.add_error("courriel", MESSAGE_COURRIEL_DEJA_UTILISE)
            else:
                _envoyer_courriel_confirmation(requete, courriel)
                return redirect("inscription_envoyee")
    else:
        formulaire = FormulaireInscription()
    return render(requete, "comptes/inscription.html", {"formulaire": formulaire})


def inscription_envoyee(requete: HttpRequest) -> HttpResponse:
    """Avis d'envoi du courriel de confirmation."""
    return render(requete, "comptes/inscription_envoyee.html")


def confirmer_inscription(requete: HttpRequest, jeton: str) -> HttpResponse:
    """Confirmation : active le compte si le jeton signé est valide,
    puis message de succès et redirection vers la connexion ; page
    d'échec pour un jeton altéré, expiré ou un compte inconnu."""
    courriel = lire_jeton_confirmation(jeton)
    if courriel is None:
        return render(requete, "comptes/confirmer_echec.html")
    try:
        confirmer_compte(depot_comptes(), courriel)
    except CompteInconnu:
        return render(requete, "comptes/confirmer_echec.html")
    messages.success(requete, "Votre compte est confirmé : connectez-vous.")
    return redirect("connexion")


class Connexion(VueFormulaireFrancais, LoginView):
    """Connexion : refus générique, invitation dédiée aux comptes non
    confirmés."""

    template_name = "comptes/connexion.html"
    form_class = FormulaireConnexion


class Deconnexion(LogoutView):
    """Déconnexion : la classe de base n'accepte que POST et OPTIONS,
    un GET direct reçoit son 405 d'elle-même."""


@login_required
def espace(requete: HttpRequest) -> HttpResponse:
    """Espace personnel minimal : le courriel et les liens de parcours.
    Sans session, la connexion est exigée par le réglage LOGIN_URL."""
    return render(requete, "comptes/espace.html")


class DemandeReinitialisation(VueFormulaireFrancais, PasswordResetView):
    """Demande de réinitialisation : réponse neutre, connue ou non."""

    template_name = "comptes/reinitialisation/demande.html"
    form_class = FormulaireDemandeReinitialisation
    email_template_name = "courriels/reinitialisation.html"
    subject_template_name = "courriels/sujet_reinitialisation.txt"
    success_url = reverse_lazy("reinitialisation_envoyee")


class ReinitialisationEnvoyee(PasswordResetDoneView):
    """Avis d'envoi, identique que l'adresse soit connue ou non."""

    template_name = "comptes/reinitialisation/envoyee.html"


class NouveauMotDePasse(VueFormulaireFrancais, PasswordResetConfirmView):
    """Choix du nouveau mot de passe ; la sauvegarde passe par le
    service du domaine depuis le formulaire."""

    template_name = "comptes/reinitialisation/nouveau_mot_de_passe.html"
    form_class = FormulaireNouveauMotDePasse
    success_url = reverse_lazy("reinitialisation_terminee")


class ReinitialisationTerminee(PasswordResetCompleteView):
    """Fin du parcours : le nouveau mot de passe fonctionne."""

    template_name = "comptes/reinitialisation/terminee.html"
