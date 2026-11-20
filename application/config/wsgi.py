"""Point d'entrée WSGI standard — déployable sur toute infrastructure qui
exécute Python, sans rien modifier (AD-15).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.config.settings")

application = get_wsgi_application()
