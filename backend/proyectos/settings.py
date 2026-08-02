"""
============================================================
RÍO 3 — Construcción en Seco
settings.py — Configuración principal de Django
============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURIDAD
# ============================================================

SECRET_KEY    = os.getenv('SECRET_KEY', 'clave-insegura-solo-para-desarrollo')
DEBUG         = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# ============================================================
# APLICACIONES INSTALADAS
# ============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps propias
    'proyectos',
    'contacto',
    # Terceros
    'crispy_forms',
    'crispy_bootstrap5',
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rio3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':    [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rio3.wsgi.application'


# ============================================================
# BASE DE DATOS
# Usa SQLite en desarrollo (si DB_NAME está vacío)
# Usa PostgreSQL en producción (cuando DB_NAME está definido en .env)
# ============================================================

_db_name = os.getenv('DB_NAME', '')

if _db_name:
    # Producción — PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql',
            'NAME':     _db_name,
            'USER':     os.getenv('DB_USER',     'rio3_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST':     os.getenv('DB_HOST',     'localhost'),
            'PORT':     os.getenv('DB_PORT',     '5432'),
        }
    }
else:
    # Desarrollo local — SQLite (no requiere instalación)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME':   BASE_DIR / 'db.sqlite3',
        }
    }


# ============================================================
# VALIDACIÓN DE CONTRASEÑAS
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ============================================================
# INTERNACIONALIZACIÓN
# ============================================================

LANGUAGE_CODE = 'es-ar'
TIME_ZONE     = 'America/Argentina/Cordoba'
USE_I18N      = True
USE_TZ        = True


# ============================================================
# ARCHIVOS ESTÁTICOS
# ============================================================

STATIC_URL       = '/static/'
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================================
# ARCHIVOS MEDIA (fotos subidas por el admin)
# ============================================================

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# EMAIL
# En desarrollo: se imprime en consola (no envía emails reales)
# En producción: configura Gmail en el .env
# ============================================================

_email_port = os.getenv('EMAIL_PORT', '').strip()

EMAIL_HOST          = os.getenv('EMAIL_HOST',          'smtp.gmail.com')
EMAIL_PORT          = int(_email_port) if _email_port.isdigit() else 587
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS',       'True') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER',     '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_DESTINATARIO  = os.getenv('EMAIL_DESTINATARIO',  '')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# ============================================================
# CRISPY FORMS
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'


# ============================================================
# LOGIN
# ============================================================

LOGIN_URL           = '/admin-rio3/login/'
LOGIN_REDIRECT_URL  = '/admin-rio3/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# SEGURIDAD EN PRODUCCIÓN
# ============================================================

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER      = True
    SECURE_CONTENT_TYPE_NOSNIFF    = True
    X_FRAME_OPTIONS                = 'DENY'
    SECURE_SSL_REDIRECT            = True
    SESSION_COOKIE_SECURE          = True
    CSRF_COOKIE_SECURE             = True
    SECURE_HSTS_SECONDS            = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD            = True
