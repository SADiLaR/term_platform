"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import sys
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", ""))
DEBUG_TOOLBAR = DEBUG  # to toggle separately if we want to

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split()
USE_X_FORWARDED_HOST = bool(os.getenv("USE_X_FORWARDED_HOST", ""))
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split()

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "users",
    "general",
    "simple_history",
    "accounts",
    "django_filters",
    "django_htmx",
]
if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
    ]
    if DEBUG_TOOLBAR:
        INSTALLED_APPS += [
            "debug_toolbar",
        ]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # DebugToolbarMiddleware should go here if enabled. Done below. See
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#add-the-middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

if DEBUG and DEBUG_TOOLBAR:
    MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

WSGI_APPLICATION = "app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "TEST": {"NAME": "test_db"},
        "CONN_MAX_AGE": None,
        "CONN_HEALTH_CHECKS": True,
    }
}

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
        "UPDATE_ON_FETCH": True,
    }

    # Some things rely on the setting INTERNAL_IPS:
    #  - debug_toolbar.middleware.show_toolbar
    #  - django.template.context_processors.debug
    # See https://docs.djangoproject.com/en/stable/ref/settings/#internal-ips
    # Inside a docker container, it isn't trivial to get the IP address of the
    # Docker host that will appear in REMOTE_ADDR. The following seems to work
    # for now to add support for a range of IP addresses without having to put
    # a huge list in INTERNAL_IPS, e.g. with
    #    map(str, ipaddress.ip_network('172.0.0.0/24'))
    # If this can't resolve the name "host.docker.internal", we assume that the
    # browser will contact localhost.
    import socket

    try:
        host_ip = socket.gethostbyname("host.docker.internal")
    except socket.gaierror:
        # presumably not in docker
        host_ip = None

    import ipaddress

    # Based on https://code.djangoproject.com/ticket/3237#comment:12
    class CIDRList(list):
        def __init__(self, addresses):
            """Create a new ip_network object for each address range provided."""
            self.networks = [ipaddress.ip_network(address, strict=False) for address in addresses]

        def __contains__(self, address):
            """Check if the given address is contained in any of the networks."""
            return any([ipaddress.ip_address(address) in network for network in self.networks])

    if host_ip:
        INTERNAL_IPS = CIDRList([f"{host_ip}/8"])
    else:
        INTERNAL_IPS = ["127.0.0.1"]


# Email settings
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")

email_backend_env = os.environ.get("EMAIL_BACKEND_CONSOLE", "False").lower() in ["true", "1", "yes"]

if DEBUG and email_backend_env:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Johannesburg"

USE_I18N = True

USE_TZ = True

# Media files (uploads)

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "media/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files (CSS, JavaScript, Images)
if DEBUG:
    _STATICFILES_BACKEND = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    _STATICFILES_BACKEND = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "static_files"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": _STATICFILES_BACKEND,
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING_DIR = Path("/logging")

# Internationalization

USE_I18N = True

LANGUAGES = [
    ("af", "Afrikaans"),
    ("en", "English"),
]

LANGUAGE_CODE = "en"

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# Check if the application is under testing
if "test" in sys.argv:
    DEBUG = False

# Logging configuration
if DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }
else:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": os.environ.get("LOGGING_HANDLERS_LEVEL", "WARNING"),
                "class": "logging.FileHandler",
                "filename": LOGGING_DIR / os.environ.get("LOGGING_FILE", "debug.log"),
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": os.environ.get("LOGGING_LOGGERS_LEVEL", "WARNING"),
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": os.environ.get("LOGGING_LOGGERS_DJANGO_LEVEL", "WARNING"),
                "propagate": True,
            },
        },
        "formatters": {
            "verbose": {
                "format": "{asctime} {levelname}  - {name} {module}.py (line: {lineno:d}). - {message}",
                "style": "{",
            },
        },
    }
