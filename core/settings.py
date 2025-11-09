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
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# --- ALLOWED_HOSTS CORREGIDO PARA RENDER ---
# Definimos una lista base que contiene hosts locales.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Si la variable de entorno DJANGO_ALLOWED_HOSTS existe, añadimos sus valores.
env_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
if env_hosts:
    # Extendemos la lista con los hosts definidos en la variable de entorno
    ALLOWED_HOSTS.extend(env_hosts.split(","))

if not DEBUG:
    # 1. Añadimos el comodín de Render
    if ".onrender.com" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(".onrender.com")
    
    # 2. Aseguramos que la URL específica esté allí, resolviendo el DisallowedHost.
    RENDER_HOST = "api-tecnicas-seleccion-features.onrender.com"
    if RENDER_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOST)
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
    "whitenoise.middleware.WhiteNoiseMiddleware", # <-- WhiteNoise
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
# CONFIGURACIÓN CORS Y SEGURIDAD EN PRODUCCIÓN
# =======================================================
CORS_ALLOW_ALL_ORIGINS = DEBUG  

if not DEBUG:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get("CORS_ORIGIN_URL", "https://127.0.0.1")
    ]
    # Configuraciones de seguridad obligatorias
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Habilitar el proxy seguro para Render
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# =======================================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS Y WHITENOISE
# =======================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Directorio donde Django buscará archivos estáticos creados por ti
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Configuración de WhiteNoise (Usando el nuevo ajuste STORAGES)
if not DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

# =======================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"