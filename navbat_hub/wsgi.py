"""NavbatHub uchun WSGI konfiguratsiyasi."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navbat_hub.settings')
application = get_wsgi_application()
