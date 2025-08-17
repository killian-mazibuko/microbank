import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("JWT_SECRET", "changeme")
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'corsheaders',
    "drf_spectacular",
    "users",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "users.middleware.InternalTokenMiddleware",
]


CORS_ALLOWED_ORIGINS = [
    "http://20.63.49.65:3000"
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/data/db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
# Static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.environ.get("ANON_THROTTLE_RATE", "20/min"),
        "user": os.environ.get("USER_THROTTLE_RATE", "60/min"),
        "login": os.environ.get("LOGIN_THROTTLE_RATE", "10/min"),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Client Service API",
    "DESCRIPTION": "Registration, authentication, profile, admin blacklisting",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

JWT_SECRET = os.environ.get("JWT_SECRET", "changeme")
INTERNAL_TOKEN = os.environ.get("INTERNAL_TOKEN", "changeme")
RABBITMQ = {
    "HOST": os.environ.get("RABBITMQ_HOST", "rabbitmq"),
    "USER": os.environ.get("RABBITMQ_USER", "guest"),
    "PASS": os.environ.get("RABBITMQ_PASS", "guest"),
    "VHOST": os.environ.get("RABBITMQ_VHOST", "/"),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"
