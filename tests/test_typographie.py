"""Garde de typographie : les fichiers du club ne contiennent ni tiret
cadratin (U+2014) ni guillemets typographiques français (U+00AB, U+00BB).

Le périmètre est le code du club : 'domaine/', 'application/', 'tests/',
'.github/' et les fichiers de racine listés plus bas. L'archive de
planification '_bmad-output/' et l'outillage des agents ('_bmad/',
'.agents/') restent hors du parcours. En cas d'écart, l'échec nomme
précisément le fichier, la ligne et le caractère.
"""

from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]

INTERDITS = {
    chr(0x2014): "tiret cadratin",
    chr(0x00AB): "guillemet ouvrant",
    chr(0x00BB): "guillemet fermant",
}

RACINES_A_PARCOURIR = ["domaine", "application", "tests", ".github"]
FICHIERS_A_LA_RACINE = [
    "AGENTS.md",
    "README.md",
    ".gitignore",
    "Procfile",
    "docker-compose.yml",
    "manage.py",
    "pyproject.toml",
]
DOSSIERS_EXCLUS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def _fichiers_du_club(racine: Path) -> list[Path]:
    """Fichiers du club à parcourir : dossiers du code et fichiers de
    racine ; rien d'autre n'est lu."""
    trouves: list[Path] = []
    for nom in RACINES_A_PARCOURIR:
        dossier = racine / nom
        if not dossier.is_dir():
            continue
        for fichier in dossier.rglob("*"):
            if not fichier.is_file():
                continue
            if DOSSIERS_EXCLUS.intersection(fichier.parts):
                continue
            trouves.append(fichier)
    for nom in FICHIERS_A_LA_RACINE:
        fichier = racine / nom
        if fichier.is_file():
            trouves.append(fichier)
    return sorted(trouves)


def test_les_fichiers_du_club_evitent_les_caracteres_interdits() -> None:
    fichiers = _fichiers_du_club(RACINE)
    assert fichiers, "aucun fichier à parcourir : la garde ne protège rien"

    violations: list[str] = []
    for fichier in fichiers:
        relatif = fichier.relative_to(RACINE)
        try:
            lignes = fichier.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            violations.append(f"{relatif} : fichier illisible en UTF-8")
            continue
        for numero, ligne in enumerate(lignes, 1):
            for caractere, nom in INTERDITS.items():
                if caractere in ligne:
                    violations.append(f"{relatif}:{numero} : {nom}")

    assert not violations, (
        "Typographie interdite présente (tiret cadratin, guillemets "
        "typographiques français) : " + " ; ".join(violations)
    )


def test_une_violation_est_nommee_fichier_ligne_et_caractere(
    tmp_path, monkeypatch
) -> None:
    """Chemin en échec : un dossier factice contenant les caractères
    interdits fait échouer la garde en nommant le fichier, la ligne et le
    caractère."""
    (tmp_path / "application").mkdir()
    (tmp_path / "application" / "vues.py").write_text(
        "note" + chr(0x2014) + "ici\n" + chr(0x00AB) + "texte" + chr(0x00BB) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(f"{__name__}.RACINE", tmp_path)

    with pytest.raises(AssertionError) as erreur:
        test_les_fichiers_du_club_evitent_les_caracteres_interdits()

    message = str(erreur.value)
    assert "vues.py:1 : tiret cadratin" in message
    assert "vues.py:2 : guillemet ouvrant" in message
    assert "vues.py:2 : guillemet fermant" in message
