"""
Django settings for core project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env (solo para desarrollo local)
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
# =======================================================
# CONFIGURACIÓN DE SEGURIDAD (LEYENDO DE VARIABLES DE ENTORNO)
# =======================================================
# SECRET_KEY: Obligatorio en Render
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "default-insecure-key-para-desarrollo")
# DEBUG: Debe ser False en producción (Render)
DEBUG = (
    os.environ.get("DJANGO_DEBUG", "False") == "True"
)  # ¡Cambiado a False por defecto!
# ALLOWED_HOSTS: Cargando la lista y añadiendo Render
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
if not DEBUG:
    # Render siempre usa *.onrender.com
    ALLOWED_HOSTS.append(".onrender.com")
    # Asegúrate de que DjangoSettingsModule apunte a este archivo
    # Y que Render cargue DJANGO_SETTINGS_MODULE=core.settings
# =======================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    # Whitenoise debe estar justo después de SecurityMiddleware
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # RUTA A LA CARPETA 'templates' en la raíz
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
# SIN BASE DE DATOS
DATABASES = {}
# =======================================================
# CONFIGURACIÓN CORS (Crucial para el frontend)
# =======================================================
if DEBUG:
    # En desarrollo, permitir todo
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # En producción, solo permitir orígenes específicos (ej. Render)
    CORS_ALLOWED_ORIGINS = [
        # La URL de tu servicio web en Render (ej. https://feature-selection-api.onrender.com)
        os.environ.get("CORS_ORIGIN_URL", "https://127.0.0.1")
    ]
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
if DEBUG:
    # Solo en desarrollo, busca archivos estáticos en la carpeta 'static' de la raíz
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]
else:
    # En producción, solo usa STATIC_ROOT
    STATICFILES_DIRS = []
# Configuración adicional para Whitenoise (compresión y encabezados)
if not DEBUG:
    # Esto ayuda a servir archivos con encabezados optimizados para caché
    WHITENOISE_MANIFEST_HETERS = True
    # Esto habilita la compresión de archivos estáticos
    WHITENOISE_STORAGE = (
        "django.contrib.staticfiles.storage.CompressedManifestStaticFilesStorage"
    )
# =======================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
