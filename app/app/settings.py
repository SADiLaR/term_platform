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
]

# Add django-extensions to the installed apps if DEBUG is True
if DEBUG:
    INSTALLED_APPS += [
        "django_extensions",
        "debug_toolbar",
    ]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

# Add debug toolbar middleware
if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

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
    }
}

# toolbar settings
if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "IS_RUNNING_TESTS": False,
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
    }

    INTERNAL_IPS = [
        "host.docker.internal",
    ]

# Check if the application is under testing
if "test" in sys.argv or "test_coverage" in sys.argv:  # Covers regular testing and django-coverage
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"

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

LOGGING_FOLDER_DEFAULT = os.path.abspath(os.path.join("/logging/"))

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
                "filename": os.path.join(
                    LOGGING_FOLDER_DEFAULT, os.environ.get("LOGGING_FILE", "debug.log")
                ),
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
