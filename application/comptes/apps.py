"""Configuration de l'app comptes."""

from importlib import import_module

from django.apps import AppConfig
from django.utils.module_loading import module_has_submodule


class ComptesConfig(AppConfig):
    name = "application.comptes"
    label = "comptes"
    verbose_name = "Comptes"

    def import_models(self) -> None:
        """Charge les modèles depuis 'modeles.py', leur nom français :
        Django ne cherche que 'models.py', sans ce chargement le
        registre ignorerait l'app et makemigrations resterait aveugle
        à ses changements de schéma."""
        self.models = self.apps.all_models[self.label]
        if self.models_module is None and module_has_submodule(self.module, "modeles"):
            self.models_module = import_module(f"{self.name}.modeles")
