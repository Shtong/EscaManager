"""Point d'entrée WSGI standard."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.config.settings")

application = get_wsgi_application()
