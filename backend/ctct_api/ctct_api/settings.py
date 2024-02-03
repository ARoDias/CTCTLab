# settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment-specific settings
ENVIRONMENT = os.getenv('DJANGO_ENV', 'dev')

if ENVIRONMENT == 'prod':
    from .settings_prod import *
else:
    from .settings_dev import *

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'rest_framework_simplejwt',

    'users',
    'questions',
    'analytics',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR.parent.parent / 'frontend' / 'public'],
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

ROOT_URLCONF = 'ctct_api.urls'
WSGI_APPLICATION = 'ctct_api.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'users.validators.CustomUserAttributeSimilarityValidator',
    },
    {
        'NAME': 'users.validators.CustomMinimumLengthValidator',
    },
    {
        'NAME': 'users.validators.CustomCommonPasswordValidator',
    },
    {
        'NAME': 'users.validators.CustomNumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'pt-pt'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent.parent / 'frontend' / 'dist']
STATIC_ROOT = BASE_DIR.parent.parent / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
   'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=120),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
