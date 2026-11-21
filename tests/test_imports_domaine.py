"""Garde AD-1 : le domaine n'importe que la bibliothèque standard Python.

Le parcours se fait par AST — aucun code du domaine n'est exécuté — sur
tous les fichiers Python de « domaine/ ». La liste blanche est
``sys.stdlib_module_names`` : aucune liste codée à la main à maintenir.
En cas d'import interdit, l'échec nomme précisément le fichier et le module.
"""

import ast
import sys
from pathlib import Path

import pytest

RACINE_DOMAINE = Path(__file__).resolve().parents[1] / "domaine"

# Le domaine peut s'importer lui-même ; c'est sa seule tolérance.
PAQUETS_AUTORISES = {"domaine"}


def _imports_de(fichier: Path) -> list[str]:
    """Modules importés par un fichier, en absolu — un import relatif reste
    dans le domaine et n'est pas concerné."""
    arbre = ast.parse(fichier.read_text(encoding="utf-8"))
    modules: list[str] = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            modules.extend(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.level == 0 and noeud.module:
            modules.append(noeud.module)
    return modules


def test_le_domaine_n_importe_que_la_bibliotheque_standard() -> None:
    fichiers = sorted(RACINE_DOMAINE.rglob("*.py"))
    assert fichiers, "aucun fichier Python trouvé sous domaine/ — la garde ne protège rien"

    violations: list[str] = []
    for fichier in fichiers:
        for module in _imports_de(fichier):
            racine = module.split(".")[0]
            if racine not in sys.stdlib_module_names and racine not in PAQUETS_AUTORISES:
                violations.append(
                    f"{fichier.relative_to(RACINE_DOMAINE.parent)} importe « {module} »"
                )

    assert not violations, (
        "AD-1 violé — le domaine n'importe que la bibliothèque standard : "
        + " ; ".join(violations)
    )


def test_une_violation_est_nommee_fichier_et_module(
    tmp_path, monkeypatch
) -> None:
    """Matrice « Garde d'imports », chemin en échec : un domaine factice
    contenant un import interdit fait échouer la garde en nommant
    précisément le fichier et le module."""
    domaine_factice = tmp_path / "domaine"
    domaine_factice.mkdir()
    (domaine_factice / "entites.py").write_text(
        "import django.db\n", encoding="utf-8"
    )
    monkeypatch.setattr(f"{__name__}.RACINE_DOMAINE", domaine_factice)

    with pytest.raises(AssertionError) as erreur:
        test_le_domaine_n_importe_que_la_bibliotheque_standard()

    message = str(erreur.value)
    assert "entites.py" in message
    assert "django.db" in message
