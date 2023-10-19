"""
Django settings for manga_reader project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailBackend",
]
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-gy-p5d*#$fso0fl!9&^e_=e^!8+%n*l-$d6r!$!3pcxrd^2ow%"
MEDIA_ROOT = "./imgs"
MEDIA_URL = "imgs/"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =False

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login"
LOGOUT_URL = "logout"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
# LOGGING = {
#     "version": 1,
#     "handlers": {"console": {"class": "logging.StreamHandler"}},
#     "loggers": {"django.db.backends": {"handlers": ["console"], "level": "DEBUG"}},
# }
ALLOWED_HOSTS = ["MangaLove.info.gf"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reader.apps.ReaderConfig",
    "rosetta",
    "parler",
    "cachalot",
    "django.contrib.humanize",
    "account.apps.AccountConfig",
    "user_actions.apps.UserActionsConfig",
]

PARLER_LANGUAGES = {
 None: (
 {'code': 'en'},
 {'code': 'ru'},
 ),
 'default': {
 'fallback': 'ru',
 'hide_untranslated': False,
 }
}
CACHES = {
    "default": {
        "BACKEND": 'django_redis.cache.RedisCache',
        "LOCATION": "redis://127.0.0.1:6379",
    }
}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "manga_reader.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "manga_reader.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "manga_project",
        # "NAME": "manga_project1",
        "USER": "lumberjack",
        "PASSWORD": "h*99IgJdEc8*",
        "HOST": "localhost",
        "PORT": "",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"
from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
LOGIN_REDIRECT_URL = "/"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'alanuldashev@gmail.com'
EMAIL_HOST_PASSWORD = 'duxunbifpdtkfpog'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
LOGIN_URL = "login"
LOGOUT_URL = "logout"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_ROOT = "./static"
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "imgs",
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
