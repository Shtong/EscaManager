"""Bibliothèque de domaine d'EscaManager — paquet pur (AD-1).

Elle n'importe que la bibliothèque standard Python : aucun import Django,
HTTP, SQL ou client externe n'y est toléré. La garde
``tests/test_imports_domaine.py`` le vérifie en CI sur chaque fichier.
"""
