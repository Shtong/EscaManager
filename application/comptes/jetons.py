"""Jetons signés du parcours des comptes.

Confirmation d'inscription : l'identifiant du compte (son courriel) est
signé avec un sel dédié, valable 72 heures. Aucune table supplémentaire,
aucune dépendance nouvelle. La réinitialisation du mot de passe, elle,
s'appuie sur le générateur de jetons standard de Django, éprouvé et
branché sur la clé secrète des réglages.
"""

from datetime import timedelta

from django.core.signing import BadSignature, TimestampSigner

SEL_CONFIRMATION = "confirmation-compte"
VALIDITE_CONFIRMATION = timedelta(hours=72)


def fabriquer_jeton_confirmation(courriel: str) -> str:
    """Signe le courriel du compte frais ; le jeton embarque sa date."""
    return TimestampSigner(salt=SEL_CONFIRMATION).sign(courriel)


def lire_jeton_confirmation(jeton: str) -> str | None:
    """Retourne le courriel signé par le jeton, ou None si le jeton est
    altéré, inconnu ou expiré (plus de 72 heures)."""
    signeur = TimestampSigner(salt=SEL_CONFIRMATION)
    try:
        return signeur.unsign(jeton, max_age=VALIDITE_CONFIRMATION)
    except BadSignature:
        return None
