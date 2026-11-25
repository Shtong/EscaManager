"""Formulaires du parcours des comptes.

Libellés, aide et erreurs en français direct. Toute écriture passe par
un service du domaine ; la présence d'un compte se lit par le port.
"""

from typing import ClassVar

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.core.exceptions import ValidationError

from application.config.composition import depot_comptes
from domaine.services.comptes import reinitialiser_mot_de_passe

MESSAGE_COURRIEL_DEJA_UTILISE = "Un compte existe déjà avec cette adresse de courriel."


class FormulaireInscription(forms.Form):
    """Inscription : une adresse et deux fois le mot de passe ; l'erreur
    de doublon vient du service du domaine, attrapée par la vue."""

    courriel = forms.EmailField(
        label="Adresse de courriel",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    mot_de_passe = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    confirmation = forms.CharField(
        label="Confirmez le mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        donnees = super().clean()
        mot_de_passe = donnees.get("mot_de_passe")
        confirmation = donnees.get("confirmation")
        if mot_de_passe and confirmation and mot_de_passe != confirmation:
            self.add_error(
                "confirmation",
                ValidationError(
                    "Les deux mots de passe ne concordent pas.",
                    code="password_mismatch",
                ),
            )
        return donnees


class FormulaireConnexion(AuthenticationForm):
    """Connexion : échec générique sans révéler l'existence d'un compte ;
    un compte inscrit mais non confirmé reçoit une invitation à
    confirmer, sans aucun indice sur le mot de passe."""

    username = forms.EmailField(
        label="Adresse de courriel",
        max_length=254,
        widget=forms.EmailInput(attrs={"autofocus": True, "autocomplete": "email"}),
    )
    password = forms.CharField(
        label="Mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages: ClassVar[dict[str, str]] = {
        "invalid_login": "Adresse de courriel ou mot de passe incorrect.",
        "inactive": (
            "Ce compte n'est pas encore confirmé : ouvrez le courriel reçu à "
            "l'inscription et suivez son lien de confirmation."
        ),
    }

    def clean(self):
        courriel = self.cleaned_data.get("username")
        mot_de_passe = self.cleaned_data.get("password")

        if courriel is not None and mot_de_passe:
            self.user_cache = authenticate(
                self.request, username=courriel, password=mot_de_passe
            )
            if self.user_cache is None:
                # Le refus est générique, sauf pour un compte inscrit mais
                # pas encore confirmé, invité à confirmer quel que soit le
                # mot de passe fourni : aucun indice sur sa validité.
                compte = depot_comptes().trouver(courriel)
                if compte is not None and not compte.actif:
                    raise ValidationError(
                        self.error_messages["inactive"], code="inactive"
                    )
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class FormulaireDemandeReinitialisation(PasswordResetForm):
    """Demande de réinitialisation : la réponse est neutre, l'adresse
    soit connue, soit non."""

    email = forms.EmailField(
        label="Adresse de courriel",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )


class FormulaireNouveauMotDePasse(SetPasswordForm):
    """Choix du nouveau mot de passe : la sauvegarde passe par le service
    du domaine, jamais par l'ORM depuis le formulaire."""

    error_messages: ClassVar[dict[str, str]] = {
        **SetPasswordForm.error_messages,
        "password_mismatch": "Les deux mots de passe ne concordent pas.",
    }
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label="Confirmez le nouveau mot de passe",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def save(self, commit: bool = True):
        """Écriture unique : le service du domaine change le mot de
        passe, dans une transaction portée par le dépôt ; sans commit,
        aucune écriture. Le compte est retourné, contrat du parent."""
        if commit:
            reinitialiser_mot_de_passe(
                depot_comptes(),
                self.user.get_username(),
                self.cleaned_data["new_password1"],
            )
            # Le compte a été chargé par la vue avant l'écriture : le
            # ressynchroniser pour que l'objet en mémoire dise la vérité.
            self.user.refresh_from_db(fields=["password"])
        return self.user
