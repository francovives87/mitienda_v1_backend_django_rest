from pathlib import Path

import os

import datetime


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-prkeel1h%)7oyki1!=#jh&a0*1+p-+-%a@ar3uvn_0k!fez@(c'


#User model
AUTH_USER_MODEL = 'users.User'

FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework_gis',
    'drf_yasg',
    'corsheaders',
    'django_cleanup.apps.CleanupConfig',
    'channels',
    'django.contrib.gis',
]

LOCAL_APPS = [
    'apps.users',
    'apps.tiendas',
    'apps.products',
    'apps.blog',
    'apps.orders',
    'apps.realtime',
    'apps.services',
    'apps.estadisticas',
    
]

THIRD_APPS = [

]


INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

REST_FRAMEWORK = {
      'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M:%S",
    'TIME_FORMAT': "%H:%M",
    'DATE_FORMAT': "%Y-%m-%d",
    #["%d-%m-%Y"]
    "DATE_INPUT_FORMATS": ["%Y-%m-%d"],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=365),
}

CORS_ALLOWED_ORIGINS = [
    "https://45.15.24.205",
    "https://minegocio.me",
    "http://localhost",
    "https://localhost",
    "https://127.0.0.1",
    "http://127.0.0.1",
    'http://localhost',
    'http://127.0.0.1:8080',
    'http://localhost:8080',
    'http://mitienda.app',
    'https://mitienda.app',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'mitienda.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mitienda.wsgi.application'
ASGI_APPLICATION = 'mitienda.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


