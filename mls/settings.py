import os

from pathlib import Path

from cosmogo.utils.settings import env, configure_sentry, setdefault

BASE_DIR = Path(__file__).parents[1]

ENVIRONMENT = env('ENVIRONMENT', 'default')

RELEASE = env('RELEASE')

if SENTRY_DSN := env('SENTRY_DSN'):
    configure_sentry(SENTRY_DSN, ENVIRONMENT, RELEASE, celery=True, send_default_pii=True)

DEBUG = env('DEBUG', ENVIRONMENT == 'develop')

SECRET_KEY = env('SECRET_KEY', 'not-a-secret-key' if DEBUG else None)

if ALLOWED_HOST := env('ALLOWED_HOST'):
    ALLOWED_HOSTS = [ALLOWED_HOST]
elif DEBUG:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'mls',
    'cosmogo',
    'rest_framework',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_USE_SESSIONS = False

ROOT_URLCONF = 'mls.urls'

DJANGO_TEMPLATES = {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
        ],
    },
}

TEMPLATES = [DJANGO_TEMPLATES]

WSGI_APPLICATION = 'mls.wsgi.application'

DATABASES = {}

USE_I18N = True
LANGUAGE_CODE = 'en-us'

USE_TZ = True
TIME_ZONE = 'Europe/Berlin'

STATIC_URL = 'static/'
STATIC_ROOT = env('STATIC_ROOT', BASE_DIR / 'public' / 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

DATA_DIR = env('DATA_DIR', BASE_DIR / 'data')

LARGE_LANGUAGE_MODEL_NAME = 'intfloat/multilingual-e5-large'
SMALL_LANGUAGE_MODEL_NAME = 'intfloat/multilingual-e5-small'

EMBEDDING_MODEL_NAME = env('EMBEDDING_MODEL_NAME', SMALL_LANGUAGE_MODEL_NAME)
EMBEDDING_MODEL_CACHE_DIR = env('EMBEDDING_MODEL_CACHE_DIR', DATA_DIR / 'embedding')

NLTK_DATA_DIR = setdefault('NLTK_DATA', DATA_DIR / 'nltk')

FASTEMBED_MODEL_NAME = env('FASTEMBED_MODEL_NAME', LARGE_LANGUAGE_MODEL_NAME)
FASTEMBED_MODEL_CACHE_DIR = env('FASTEMBED_MODEL_CACHE_DIR', EMBEDDING_MODEL_CACHE_DIR)

SENTENCE_TRANSFORMERS_MODEL_NAME = env('SENTENCE_TRANSFORMERS_MODEL_NAME', EMBEDDING_MODEL_NAME)
SENTENCE_TRANSFORMERS_HOME = setdefault('SENTENCE_TRANSFORMERS_HOME', EMBEDDING_MODEL_CACHE_DIR)

TOKENIZERS_PARALLELISM = setdefault('TOKENIZERS_PARALLELISM', True, 'true')

EMBEDDING_LIBRARY = env('EMBEDDING_LIBRARY', 'sbert')
