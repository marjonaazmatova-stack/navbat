"""
NavbatHub uchun Django sozlamalari.
Production'ga tayyor — barcha sezgir ma'lumotlar muhit o'zgaruvchilaridan o'qiladi.
"""
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# XAVFSIZLIK
# ============================================================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-CHANGE-ME-IN-PRODUCTION-x7k9m2p4q8w3e6r5t1y'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,.railway.app,.onrender.com,.fly.dev,.pythonanywhere.com'
).split(',')

CSRF_TRUSTED_ORIGINS = [
    f'https://{host.lstrip(".")}' for host in ALLOWED_HOSTS if '.' in host
]

# ============================================================
# ILOVALAR
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Loyiha ilovalari
    'apps.accounts',
    'apps.queue',
    'apps.operator',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static fayllar uchun
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'navbat_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.queue.context_processors.site_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'navbat_hub.wsgi.application'

# ============================================================
# MA'LUMOTLAR BAZASI
# ============================================================
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR}/db.sqlite3',
        conn_max_age=600,
    )
}

# ============================================================
# AUTENTIFIKATSIYA
# ============================================================
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/cabinet/'
LOGOUT_REDIRECT_URL = '/'

# ============================================================
# XALQARO SOZLAMALAR
# ============================================================
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('uz', "O'zbekcha"),
    ('ru', 'Русский'),
    ('en', 'English'),
]

# ============================================================
# STATIK VA MEDIA FAYLLAR
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# SAYT SOZLAMALARI
# ============================================================
SITE_NAME = 'NavbatHub'
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# XABARLAR (Django messages)
# ============================================================
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'bg-slate-100 text-slate-800 border-slate-300',
    messages.INFO: 'bg-blue-50 text-blue-800 border-blue-300',
    messages.SUCCESS: 'bg-emerald-50 text-emerald-800 border-emerald-300',
    messages.WARNING: 'bg-amber-50 text-amber-800 border-amber-300',
    messages.ERROR: 'bg-rose-50 text-rose-800 border-rose-300',
}

# ============================================================
# PRODUCTION XAVFSIZLIK
# ============================================================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Login URL'ni qayta o'rnatish
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 kun
