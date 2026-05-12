"""NavbatHub uchun ASGI konfiguratsiyasi."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navbat_hub.settings')
application = get_asgi_application()
