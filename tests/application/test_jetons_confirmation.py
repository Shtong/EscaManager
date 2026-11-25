"""Jeton de confirmation : la validité de 72 heures est réelle, un
jeton périmé est refusé même si sa signature est intacte.
"""

import time

from django.core.signing import Signer, b62_encode

from application.comptes.jetons import (
    SEL_CONFIRMATION,
    fabriquer_jeton_confirmation,
    lire_jeton_confirmation,
)


def test_un_jeton_frais_rend_le_courriel() -> None:
    """Le jeton signé à l'instant rend l'adresse qu'il porte."""
    jeton = fabriquer_jeton_confirmation("adherent@scb-escalade.fr")

    assert lire_jeton_confirmation(jeton) == "adherent@scb-escalade.fr"


def test_un_jeton_expire_est_refuse() -> None:
    """Un jeton de plus de 72 heures est refusé : la signature reste
    valide, seul l'âge du lien le disqualifie."""
    horodatage_passe = b62_encode(int(time.time()) - 73 * 3600)
    jeton_expire = Signer(salt=SEL_CONFIRMATION).sign(
        f"adherent@scb-escalade.fr:{horodatage_passe}"
    )

    assert lire_jeton_confirmation(jeton_expire) is None
