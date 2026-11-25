"""Garde d'imports des apps : les apps Django ne s'importent jamais entre
elles.

Le parcours se fait par AST, aucun code de l'application n'est exécuté,
sur tous les fichiers Python des apps : dossiers de 'application/'
portant un '__init__.py', hors 'config', seule habilitée à composer
les apps entre elles. Une app ajoutée est donc couverte
automatiquement, sans liste à maintenir. Sont traqués l'import direct,
l'import relatif qui s'échappe vers une autre app et l'import dynamique
à chaîne constante ('importlib.import_module',
'importlib.util.import_module', '__import__') ; une
app peut s'importer elle-même, importer le domaine, Django ou la
bibliothèque standard. En cas d'import croisé, l'échec nomme précisément
le fichier et le module. Les migrations relèvent de la revue de fusion,
pas de cette garde.
"""

import ast
from pathlib import Path

import pytest

RACINE_APPLICATION = Path(__file__).resolve().parents[1] / "application"


def _apps_de(racine: Path) -> list[str]:
    """Apps Django du projet : dossiers portant un '__init__.py', hors
    'config' qui n'est pas une app, seule elle compose les apps.
    Une app ajoutée est couverte sans toucher à la garde."""
    return sorted(
        dossier.name
        for dossier in racine.iterdir()
        if (
            dossier.is_dir()
            and dossier.name != "config"
            and (dossier / "__init__.py").is_file()
        )
    )


def _est_import_dynamique(noeud: ast.Call) -> bool:
    """Appel 'importlib.import_module(...)',
    'importlib.util.import_module(...)', 'import_module(...)' (après un
    'from importlib import import_module') ou '__import__(...)'."""
    fonction = noeud.func
    if isinstance(fonction, ast.Name):
        return fonction.id in {"import_module", "__import__"}
    if not isinstance(fonction, ast.Attribute) or fonction.attr != "import_module":
        return False
    base = fonction.value
    if isinstance(base, ast.Name):
        return base.id == "importlib"
    return (
        isinstance(base, ast.Attribute)
        and base.attr == "util"
        and isinstance(base.value, ast.Name)
        and base.value.id == "importlib"
    )


def _chaine_constante(noeud: ast.Call) -> str | None:
    """Chaîne littérale du premier argument ou du mot-clé 'name' : un
    module calculé au moment de l'appel échappe à l'AST et n'est pas
    traqué."""
    premier = noeud.args[0] if noeud.args else None
    if isinstance(premier, ast.Constant) and isinstance(premier.value, str):
        return premier.value
    for motcle in noeud.keywords:
        if (
            motcle.arg == "name"
            and isinstance(motcle.value, ast.Constant)
            and isinstance(motcle.value.value, str)
        ):
            return motcle.value.value
    return None


def _imports_croises_de(
    fichier: Path, paquet: list[str], autres_apps: set[str]
) -> list[str]:
    """Modules d'une autre app importés par un fichier : import direct,
    import relatif ou appel dynamique à chaîne constante. 'paquet' est
    le paquet du fichier (par ex. 'application.comptes.migrations'),
    nécessaire pour résoudre les imports relatifs."""
    arbre = ast.parse(fichier.read_text(encoding="utf-8"))
    croises: list[str] = []

    def examiner(module: str) -> None:
        parties = module.split(".")
        if (
            parties[0] == "application"
            and len(parties) > 1
            and parties[1] in autres_apps
        ):
            croises.append(module)

    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            for alias in noeud.names:
                examiner(alias.name)
        elif isinstance(noeud, ast.ImportFrom):
            if noeud.level == 0:
                if noeud.module:
                    examiner(noeud.module)
                    if noeud.module == "application":
                        # 'from application import <app>' importe
                        # 'application.<app>' : même règle, autre syntaxe.
                        for alias in noeud.names:
                            examiner(f"application.{alias.name}")
            else:
                # Import relatif, résolu depuis le paquet du fichier : un
                # 'from ..comptes import ...' écrit depuis une autre app
                # est un import croisé déguisé, pas un détail de syntaxe.
                base = paquet[: max(0, len(paquet) - (noeud.level - 1))]
                cible = base + (noeud.module.split(".") if noeud.module else [])
                if noeud.module:
                    examiner(".".join(cible))
                else:
                    for alias in noeud.names:
                        examiner(".".join([*cible, alias.name]))
        elif isinstance(noeud, ast.Call) and _est_import_dynamique(noeud):
            chaine = _chaine_constante(noeud)
            if chaine is not None:
                examiner(chaine)

    return croises


def test_les_apps_ne_s_importent_pas_entre_elles() -> None:
    apps = _apps_de(RACINE_APPLICATION)
    assert apps, "aucune app trouvée sous application/ : la garde ne protège rien"

    violations: list[str] = []
    for app in apps:
        autres_apps = set(apps) - {app}
        dossier_app = RACINE_APPLICATION / app
        for fichier in sorted(dossier_app.rglob("*.py")):
            sous_dossiers = fichier.relative_to(dossier_app).parts[:-1]
            paquet = ["application", app, *sous_dossiers]
            chemin = fichier.relative_to(RACINE_APPLICATION.parent)
            for module in _imports_croises_de(fichier, paquet, autres_apps):
                violations.append(f"{chemin} importe '{module}'")

    assert not violations, "Les apps ne s'importent jamais entre elles : " + " ; ".join(
        violations
    )


def test_un_import_croise_est_nomme_fichier_et_module(tmp_path, monkeypatch) -> None:
    """Chemin en échec : des apps factices, dont 'saisons', absente du
    dépôt, dont l'une importe l'autre, directement, en relatif ou par un
    appel dynamique à chaîne constante, font échouer la garde en nommant
    précisément le fichier et le module."""
    application_factice = tmp_path / "application"
    for app in ("comptes", "saisons"):
        dossier = application_factice / app
        dossier.mkdir(parents=True)
        (dossier / "__init__.py").write_text("", encoding="utf-8")

    (application_factice / "saisons" / "views.py").write_text(
        "import application.comptes.models\n"
        "import importlib\n"
        "import importlib.util\n"
        "from application import comptes\n"
        "from ..comptes import services\n"
        "from importlib import import_module\n"
        'importlib.import_module("application.comptes.depots")\n'
        'importlib.util.import_module("application.comptes.requetes")\n'
        'import_module(name="application.comptes.views")\n'
        '__import__("application.comptes.services")\n',
        encoding="utf-8",
    )

    monkeypatch.setattr(f"{__name__}.RACINE_APPLICATION", application_factice)

    with pytest.raises(AssertionError) as erreur:
        test_les_apps_ne_s_importent_pas_entre_elles()

    message = str(erreur.value)
    assert "views.py" in message
    assert "application.comptes.models" in message
    assert "application.comptes.depots" in message
    assert "application.comptes.requetes" in message
    assert "application.comptes.views" in message
    assert "application.comptes.services" in message
    assert "'application.comptes'" in message


def test_les_imports_licites_passent(tmp_path, monkeypatch) -> None:
    """Imports licites : une app peut s'importer elle-même,
    importer le domaine, Django ou la bibliothèque standard, en direct ou
    en relatif ; seule 'config' compose les apps, la garde
    reste verte."""
    application_factice = tmp_path / "application"
    for app in ("comptes", "saisons"):
        dossier = application_factice / app
        dossier.mkdir(parents=True)
        (dossier / "__init__.py").write_text("", encoding="utf-8")

    (application_factice / "saisons" / "views.py").write_text(
        "import json\n"
        "import importlib\n"
        "import importlib.util\n"
        "from django.shortcuts import render\n"
        "from application.saisons.models import Saison\n"
        "from domaine.requetes import compter_comptes\n"
        "from . import vues_locales\n"
        "from ..config import composition\n"
        "from importlib import import_module\n"
        'importlib.import_module("application.saisons.depots")\n'
        'importlib.util.import_module("application.saisons.requetes")\n'
        'import_module(name="application.saisons.vues")\n',
        encoding="utf-8",
    )
    config = application_factice / "config"
    config.mkdir()
    (config / "__init__.py").write_text(
        "from application.comptes.depots import DepotComptesDjango\n"
        "from application.saisons.vues import accueil\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(f"{__name__}.RACINE_APPLICATION", application_factice)

    # Ne doit pas lever : aucun de ces imports n'est un import croisé d'app.
    test_les_apps_ne_s_importent_pas_entre_elles()
