#!/usr/bin/env python
"""Outil de développement Django d'EscaManager — commandes à la racine du dépôt.
"""

import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django est introuvable — activez l'environnement virtuel et "
            "installez le dépôt : pip install -e \".[dev]\""
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
