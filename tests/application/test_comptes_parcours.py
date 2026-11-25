"""Parcours complet des comptes, sur MySQL : inscription, courriel de
confirmation, confirmation, connexion, espace, déconnexion,
réinitialisation.

Le backend locmem capture les courriels : aucun envoi réel, et la
sortie des tests reste propre (jamais le backend console).
"""

import re

import pytest
from django.conf import settings
from django.core import mail
from django.test import Client
from django.urls import reverse

from application.comptes.jetons import fabriquer_jeton_confirmation
from application.comptes.modeles import CompteDjango
from application.config.composition import depot_comptes
from domaine.services.comptes import confirmer_compte, inscrire_compte

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def courriels_en_memoire(settings):
    """Backend locmem : les courriels du parcours sont capturés, aucun
    n'atterrit dans la console des tests."""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


COURRIEL = "adherent@scb-escalade.fr"
MOT_DE_PASSE = "mot-de-passe-du-club"


def _compte_actif(
    courriel: str = COURRIEL, mot_de_passe: str = MOT_DE_PASSE
) -> CompteDjango:
    """Compte actif par le chemin du domaine : inscription puis
    confirmation, jamais d'écriture directe."""
    inscrire_compte(depot_comptes(), courriel, mot_de_passe)
    confirmer_compte(depot_comptes(), courriel)
    return CompteDjango.objects.get(courriel=courriel)


def _contenu(reponse) -> str:
    return reponse.content.decode("utf-8")


def _lien_dans(courriel, motif: str) -> str:
    """Lien extrait du corps du courriel, avec son message d'échec."""
    trouve = re.search(motif, courriel.body)
    assert trouve, f"lien introuvable dans le courriel : {courriel.body}"
    return trouve.group(0)


def _jeton_csrf(contenu: str) -> str:
    """Jeton CSRF extrait d'une page rendue, avec son message d'échec."""
    trouve = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', contenu)
    assert trouve, f"jeton CSRF introuvable dans la page : {contenu[:200]}"
    return trouve.group(1)


def test_parcours_complet_inscription_connexion_espace_deconnexion(client) -> None:
    """De l'inscription à la déconnexion : le compte se crée inactif,
    le courriel porte un lien, la confirmation l'active, la connexion
    ouvre la session, l'espace s'affiche, la déconnexion la ferme."""
    reponse = client.post(
        reverse("inscription"),
        {
            "courriel": COURRIEL,
            "mot_de_passe": MOT_DE_PASSE,
            "confirmation": MOT_DE_PASSE,
        },
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("inscription_envoyee")

    compte = CompteDjango.objects.get(courriel=COURRIEL)
    assert compte.is_active is False
    assert compte.check_password(MOT_DE_PASSE)
    assert compte.password != MOT_DE_PASSE

    assert len(mail.outbox) == 1
    courriel_envoye = mail.outbox[0]
    assert courriel_envoye.to == [COURRIEL]
    assert courriel_envoye.from_email == settings.DEFAULT_FROM_EMAIL
    assert "72 heures" in courriel_envoye.body

    lien = _lien_dans(courriel_envoye, r"/comptes/confirmer/[^/\s]+/")
    reponse = client.get(lien)
    assert reponse.status_code == 302
    assert reponse.url == reverse("connexion")

    compte.refresh_from_db()
    assert compte.is_active is True

    suivi = client.get(reponse.url)
    assert "confirmé" in _contenu(suivi)

    reponse = client.post(
        reverse("connexion"),
        {"username": COURRIEL, "password": MOT_DE_PASSE},
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("espace")

    reponse = client.get(reverse("espace"))
    assert reponse.status_code == 200
    assert COURRIEL in _contenu(reponse)

    reponse = client.post(reverse("deconnexion"))
    assert reponse.status_code == 302
    assert reponse.url == reverse("accueil")

    reponse = client.get(reverse("espace"))
    assert reponse.status_code == 302
    assert reponse.url.startswith(reverse("connexion"))


def test_inscription_doublon_refusee_sur_le_champ_courriel(client) -> None:
    """Un courriel déjà en base : formulaire re-rendu, erreur sur le
    champ courriel, aucun compte de plus."""
    _compte_actif()

    reponse = client.post(
        reverse("inscription"),
        {
            "courriel": COURRIEL,
            "mot_de_passe": "autre-mot-de-passe",
            "confirmation": "autre-mot-de-passe",
        },
    )

    assert reponse.status_code == 200
    assert "Un compte existe déjà avec cette adresse de courriel." in _contenu(reponse)
    assert CompteDjango.objects.count() == 1
    assert not mail.outbox, "aucun courriel ne devait partir pour un doublon"


def test_reinscription_d_un_compte_non_confirme_renvvoie_le_courriel(client) -> None:
    """Adresse inscrite mais jamais confirmée, jeton perdu ou expiré :
    la re-inscription ne crée pas de doublon, remplace le mot de passe
    saisi, renvoie un courriel de confirmation, et la réponse est
    identique à une inscription neuve."""
    inscrire_compte(depot_comptes(), COURRIEL, MOT_DE_PASSE)
    mail.outbox.clear()

    reponse = client.post(
        reverse("inscription"),
        {
            "courriel": COURRIEL,
            "mot_de_passe": "mot-de-passe-remplace",
            "confirmation": "mot-de-passe-remplace",
        },
    )

    assert reponse.status_code == 302
    assert reponse.url == reverse("inscription_envoyee")
    assert CompteDjango.objects.count() == 1
    assert len(mail.outbox) == 1

    compte = CompteDjango.objects.get(courriel=COURRIEL)
    assert compte.is_active is False
    assert compte.check_password("mot-de-passe-remplace")
    assert not compte.check_password(MOT_DE_PASSE)

    lien = _lien_dans(mail.outbox[0], r"/comptes/confirmer/[^/\s]+/")
    reponse = client.get(lien)
    assert reponse.status_code == 302
    assert reponse.url == reverse("connexion")

    reponse = client.post(
        reverse("connexion"),
        {"username": COURRIEL, "password": "mot-de-passe-remplace"},
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("espace")


def test_connexion_refusee_avant_confirmation_sans_indice(client) -> None:
    """Compte inscrit mais non confirmé : refus avec invitation à
    confirmer, identique que le mot de passe soit bon ou faux, aucun
    indice sur sa validité, aucune session ouverte."""
    inscrire_compte(depot_comptes(), COURRIEL, MOT_DE_PASSE)

    for mot_de_passe in (MOT_DE_PASSE, "faux-mot-de-passe"):
        reponse = client.post(
            reverse("connexion"),
            {"username": COURRIEL, "password": mot_de_passe},
        )
        assert reponse.status_code == 200
        contenu = _contenu(reponse)
        assert "pas encore confirmé" in contenu
        assert "incorrect" not in contenu

    assert client.get(reverse("espace")).status_code == 302


def test_connexion_identifiants_faux_message_generique(client) -> None:
    """Courriel inconnu ou mot de passe erroné : même message générique,
    sans jamais révéler l'existence du compte."""
    _compte_actif()

    pour_inconnu = client.post(
        reverse("connexion"),
        {"username": "inconnu@scb-escalade.fr", "password": "peu-importe"},
    )
    pour_faux = client.post(
        reverse("connexion"),
        {"username": COURRIEL, "password": "faux-mot-de-passe"},
    )

    for reponse in (pour_inconnu, pour_faux):
        assert reponse.status_code == 200
        contenu = _contenu(reponse)
        assert "Adresse de courriel ou mot de passe incorrect." in contenu
        assert "pas encore confirmé" not in contenu


def test_confirmation_invalide_page_echec(client) -> None:
    """Jeton altéré, ou bien signé mais sans compte : page d'échec avec
    les liens vers la connexion et l'inscription, jamais d'exception."""
    pour_jeton_factice = client.get("/comptes/confirmer/jeton-factice/")
    jeton_sans_compte = fabriquer_jeton_confirmation("parti@scb-escalade.fr")
    pour_compte_disparu = client.get(f"/comptes/confirmer/{jeton_sans_compte}/")

    for reponse in (pour_jeton_factice, pour_compte_disparu):
        assert reponse.status_code == 200
        contenu = _contenu(reponse)
        assert "Ce lien ne fonctionne pas" in contenu
        assert reverse("connexion") in contenu
        assert reverse("inscription") in contenu


def test_espace_sans_session_redirige_vers_connexion(client) -> None:
    """L'espace est réservé aux connectés : sans session, retour à la
    connexion."""
    reponse = client.get(reverse("espace"))

    assert reponse.status_code == 302
    assert reverse("connexion") in reponse.url


def test_deconnexion_n_accepte_que_post(client) -> None:
    """La déconnexion se fait par un formulaire en POST : un GET direct
    est refusé."""
    _compte_actif()
    client.post(reverse("connexion"), {"username": COURRIEL, "password": MOT_DE_PASSE})

    reponse = client.get(reverse("deconnexion"))

    assert reponse.status_code == 405


def test_le_parcours_tient_sans_contournement_csrf() -> None:
    """Un navigateur réel ne contourne pas la protection CSRF : le jeton
    suit la rotation opérée par la connexion, du formulaire de connexion
    jusqu'au bouton de déconnexion, sinon la déconnexion est rejetée
    avec un 403 en conditions réelles."""
    _compte_actif()
    navigateur = Client(enforce_csrf_checks=True)

    page_connexion = navigateur.get(reverse("connexion"))
    reponse = navigateur.post(
        reverse("connexion"),
        {
            "username": COURRIEL,
            "password": MOT_DE_PASSE,
            "csrfmiddlewaretoken": _jeton_csrf(_contenu(page_connexion)),
        },
    )
    assert reponse.status_code == 302

    page_espace = navigateur.get(reverse("espace"))
    reponse = navigateur.post(
        reverse("deconnexion"),
        {"csrfmiddlewaretoken": _jeton_csrf(_contenu(page_espace))},
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("accueil")

    assert navigateur.get(reverse("espace")).status_code == 302


def test_reinitialisation_de_bout_en_bout(client) -> None:
    """Demande, courriel, choix du nouveau mot de passe : l'ancien est
    refusé, le nouveau fonctionne, la redirection mène au succès."""
    _compte_actif()

    reponse = client.post(reverse("reinitialisation_demande"), {"email": COURRIEL})
    assert reponse.status_code == 302
    assert reponse.url == reverse("reinitialisation_envoyee")

    assert len(mail.outbox) == 1
    lien = _lien_dans(mail.outbox[0], r"/comptes/reinitialisation/[^/\s]+/[^/\s]+/")

    # Lien valide : redirection standard vers l'URL de saisie, le jeton
    # ne reste pas dans l'adresse du navigateur.
    reponse = client.get(lien, follow=True)
    assert reponse.status_code == 200
    assert "nouveau mot de passe" in _contenu(reponse)
    lien_final = reponse.request["PATH_INFO"]

    nouveau = "nouveau-mot-de-passe-du-club"
    reponse = client.post(
        lien_final, {"new_password1": nouveau, "new_password2": nouveau}
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("reinitialisation_terminee")

    compte = CompteDjango.objects.get(courriel=COURRIEL)
    assert compte.check_password(nouveau)

    reponse = client.post(
        reverse("connexion"),
        {"username": COURRIEL, "password": MOT_DE_PASSE},
    )
    assert "incorrect" in _contenu(reponse)

    reponse = client.post(
        reverse("connexion"),
        {"username": COURRIEL, "password": nouveau},
    )
    assert reponse.status_code == 302
    assert reponse.url == reverse("espace")


def test_lien_de_reinitialisation_invalide(client) -> None:
    """Lien de réinitialisation altéré ou déjà utilisé : page d'échec,
    jamais d'exception, invitation à redemander un courriel."""
    reponse = client.get(
        reverse("reinitialisation_nouveau_mot_de_passe", args=["bogus", "bogus"])
    )

    assert reponse.status_code == 200
    contenu = _contenu(reponse)
    assert "Ce lien ne fonctionne pas" in contenu
    assert reverse("reinitialisation_demande") in contenu


def test_demande_de_reinitialisation_neutre(client) -> None:
    """Adresse connue ou inconnue : même redirection, même page, un
    seul courriel et il ne part que pour le compte connu."""

    _compte_actif()

    pour_connue = client.post(reverse("reinitialisation_demande"), {"email": COURRIEL})
    pour_inconnue = client.post(
        reverse("reinitialisation_demande"), {"email": "inconnu@scb-escalade.fr"}
    )

    assert pour_connue.status_code == 302
    assert pour_inconnue.status_code == 302
    assert pour_inconnue.url == pour_connue.url

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [COURRIEL]

    page = client.get(reverse("reinitialisation_envoyee"))
    contenu = _contenu(page)
    assert "Si un compte actif existe avec cette adresse" in contenu
    assert COURRIEL not in contenu
    assert "inconnu@scb-escalade.fr" not in contenu


def test_demande_de_reinitialisation_inscrite_non_confirmee_neutre(client) -> None:
    """Une adresse inscrite mais non confirmée : même réponse neutre
    qu'une adresse confirmée, et aucun courriel ne part."""
    _compte_actif()
    inscrire_compte(depot_comptes(), "en-attente@scb-escalade.fr", MOT_DE_PASSE)

    pour_confirmee = client.post(
        reverse("reinitialisation_demande"), {"email": COURRIEL}
    )
    pour_non_confirmee = client.post(
        reverse("reinitialisation_demande"), {"email": "en-attente@scb-escalade.fr"}
    )

    assert pour_confirmee.status_code == 302
    assert pour_non_confirmee.status_code == 302
    assert pour_non_confirmee.url == pour_confirmee.url

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [COURRIEL]
