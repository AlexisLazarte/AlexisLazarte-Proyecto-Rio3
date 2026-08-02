"""
============================================================
RÍO 3 — Construcción en Seco
settings.py — Configuración principal de Django
============================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ============================================================
# RUTAS BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# SEGURIDAD
# ============================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'clave-insegura-solo-para-desarrollo')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

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
    'whitenoise.middleware.WhiteNoiseMiddleware',   # archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ============================================================
# URLS
# ============================================================

ROOT_URLCONF = 'rio3.urls'


# ============================================================
# TEMPLATES
# ============================================================

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
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = 'rio3.wsgi.application'


# ============================================================
# BASE DE DATOS (PostgreSQL)
# ============================================================
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.getenv('DB_NAME',     'rio3_db'),
        'USER':     os.getenv('DB_USER',     'rio3_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST':     os.getenv('DB_HOST',     'localhost'),
        'PORT':     os.getenv('DB_PORT',     '5432'),
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
# ARCHIVOS ESTÁTICOS (CSS, JS, imágenes del sitio)
# ============================================================

STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'    # donde collectstatic pone todo
STATICFILES_DIRS = [BASE_DIR / 'static']  # donde Django busca los archivos

# WhiteNoise: compresión y caché de archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ============================================================
# ARCHIVOS MEDIA (fotos subidas por el admin)
# ============================================================

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ============================================================
# EMAIL — para formulario de contacto
# ============================================================

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = os.getenv('EMAIL_HOST',      'smtp.gmail.com')
"""
EMAIL_PORT          = int(os.getenv('EMAIL_PORT',  '587'))
"""
EMAIL_PORT = int(os.getenv('EMAIL_PORT') or '587')
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS',   'True') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER',  '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_DESTINATARIO  = os.getenv('EMAIL_DESTINATARIO', '')

# En desarrollo: los emails se imprimen en la consola
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# ============================================================
# CRISPY FORMS (formularios con Bootstrap 5)
# ============================================================

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'


# ============================================================
# CONFIGURACIÓN DE LOGIN
# ============================================================

LOGIN_URL          = '/admin-rio3/login/'
LOGIN_REDIRECT_URL = '/admin-rio3/'
LOGOUT_REDIRECT_URL = '/'


# ============================================================
# CAMPO POR DEFECTO PARA CLAVES PRIMARIAS
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ============================================================
# SEGURIDAD EN PRODUCCIÓN
# ============================================================

if not DEBUG:
    SECURE_BROWSER_XSS_FILTER       = True
    SECURE_CONTENT_TYPE_NOSNIFF     = True
    X_FRAME_OPTIONS                 = 'DENY'
    SECURE_SSL_REDIRECT             = True
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True
    SECURE_HSTS_SECONDS             = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
    SECURE_HSTS_PRELOAD             = True
