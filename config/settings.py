from pathlib import Path
import environ
import os

from keycloak_oidc.default_settings import *

env = environ.Env()

"""
Project Settings
"""

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

DEBUG = env.bool('DJANGO_DEBUG', default=True)

# Allowed Hosts Definition
if DEBUG:
    # If Debug is True, allow all.
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['backend.9735.ru'])

SECRET_KEY = env('DJANGO_SECRET_KEY')

# KEYCLOAK CLIENT SETTINGS
OIDC_RP_CLIENT_ID = env('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = env('OIDC_RP_CLIENT_SECRET')

# KEYKLOAK URLS SETTINGS
OIDC_OP_AUTHORIZATION_ENDPOINT = env('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT = env('OIDC_OP_TOKEN_ENDPOINT')
OIDC_OP_USER_ENDPOINT = env('OIDC_OP_USER_ENDPOINT')
OIDC_OP_JWKS_ENDPOINT = env('OIDC_OP_JWKS_ENDPOINT')
OIDC_OP_LOGOUT_ENDPOINT = env('OIDC_OP_LOGOUT_ENDPOINT')

"""
Project Apps Definitions
Django Apps - Django Internal Apps
Third Party Apps - Apps installed via requirements.txt
Project Apps - Project owned / created apps

Installed Apps = Django Apps + Third Part apps + Projects Apps
"""
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'keycloak_oidc',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.redirects',
]

THIRD_PARTY_APPS = [
    'import_export',
    'django_extensions',
    'rest_framework',
    'storages',
    'corsheaders',
    'djangoql',
]

PROJECT_APPS = [
    'audit',
    'platform_api'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": env("DATABASE_URL")
    }
    DATABASES = {

        'default': {

            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env("DATABASE_NAME"),
            'USER': env("DATABASE_USER"),
            'PASSWORD': env("DATABASE_PASSWORD"),
            'HOST': env("DATABASE_HOST"),
            'PORT': env("DATABASE_PORT"),
        }
    }
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
    DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
AUTHENTICATION_BACKENDS = [
    'keycloak_oidc.auth.OIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Admin URL Definition
ADMIN_URL = env('DJANGO_ADMIN_URL', default='admin/')

# Redis Settings
REDIS_URL = env('REDIS_URL', default=None)

if REDIS_URL:
    CACHES = {
        "default": env.cache('REDIS_URL')
    }
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {  # 'catch all' loggers by referencing it with the empty string
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
# Static And Media Settings
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default=None)
if AWS_STORAGE_BUCKET_NAME:
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default=None) or f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=600'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'djangito.storages.StaticStorage'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'djangito.storages.PublicMediaStorage'

    STATICFILES_DIRS = (
        # os.path.join(BASE_DIR, "static"),
    )
else:
    MIDDLEWARE.insert(2, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
    WHITENOISE_USE_FINDERS = True
    STATIC_HOST = env('DJANGO_STATIC_HOST', default='')
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = STATIC_HOST + '/static/'
    if DEBUG:
        WHITENOISE_AUTOREFRESH = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='test@example.com')
"""
Third Party Settings
"""

# Celery Settings
try:
    from kombu import Queue
    from celery import Celery

    CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='amqp://localhost')
    if CELERY_BROKER_URL:
        CELERYD_TASK_SOFT_TIME_LIMIT = 60
        CELERY_ACCEPT_CONTENT = ['application/json']
        CELERY_TASK_SERIALIZER = 'json'
        CELERY_RESULT_SERIALIZER = 'json'
        CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')
        CELERY_DEFAULT_QUEUE = 'default'
        CELERY_QUEUES = (
            Queue('default'),
        )
        CELERY_CREATE_MISSING_QUEUES = True
except ModuleNotFoundError:
    print("Celery/kombu not installed. Skipping...")

CORS_ALLOWED_ORIGINS = [
    "http://backend.9735.ru:3000"
]

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOW_CREDENTIALS = True
MEDIA_PRIVATE_ROOT = 'import'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # other authentication classes, if needed
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}