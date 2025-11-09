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
# CONFIGURACIÓN DE SEGURIDAD
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
# Las variables de entorno son la mejor práctica aquí
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Permitir todo en DEBUG=True

if not DEBUG:
    # En producción (DEBUG=False), solo permitir orígenes específicos (ej. Render)
    CORS_ALLOWED_ORIGINS = [
        # La URL de tu servicio web en Render (ej. https://feature-selection-api.onrender.com)
        os.environ.get("CORS_ORIGIN_URL", "https://127.0.0.1")
    ]
    # Configuraciones de seguridad obligatorias en producción
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Habilitar el proxy seguro para Render
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# =======================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y WHITENOISE (CORREGIDO)
# =======================================================

# 1. Rutas (Igual para Dev/Prod)
STATIC_URL = "static/"
# El directorio donde 'collectstatic' reunirá todos los archivos. ¡Crucial para WhiteNoise!
STATIC_ROOT = BASE_DIR / "staticfiles"
# 2. Directorios donde Django buscará archivos estáticos
# *SOLO* incluimos la carpeta 'static' de la raíz si estamos en desarrollo.
# WhiteNoise maneja el servir desde STATIC_ROOT.
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Directorio para tus archivos estáticos en la raíz
]
# 3. Configuración de WhiteNoise (Usando el nuevo ajuste STORAGES)
if not DEBUG:
    # Usamos la nueva forma de configurar el Storage Backend para WhiteNoise
    # Esto reemplaza WHITENOISE_STORAGE y WHITENOISE_MANIFEST_HETERS
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    # ELIMINAR: WHITENOISE_MANIFEST_HETERS y WHITENOISE_STORAGE son obsoletos con STORAGES

# =======================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
