"""
Django settings for ctct_api project.
Generated by 'django-admin startproject' using Django 5.0.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

# Base directory where the manage.py exists
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Never expose this in your repository.
SECRET_KEY = os.getenv("SECRET_KEY")

# Debug mode should be False in Production
DEBUG = bool(os.getenv("DEBUG", True))

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
    # ... other apps
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.getenv("DB_NAME", "ctctboosterDB"),  
        'USER': os.getenv("DB_USER", "root"),  
        'PASSWORD': os.getenv("DB_PASSWORD", "C2T0C2T4_admin"),  
        'HOST': os.getenv("DB_HOST", "localhost"), 
        'PORT': os.getenv("DB_PORT", "3306"), 
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_ALL_TABLES'",
        },      
    }
}

# database on HelioHost:
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ctctlab_db1',  
        'USER': 'ctctlab_user',  
        'PASSWORD': 'Eskec1da',  
        'HOST': 'localhost', 
        'PORT': '3306',
    }
} """

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = 'ctctbooster@gmail.com'
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "default_email_user")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "default_email_password")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
PASSWORD_RESET_TIMEOUT = 14400  # 4 hours

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

ALLOWED_HOSTS = ['167.71.56.116','127.0.0.1', '192.168.1.18', 'localhost', 'throbbing-river-82258.pktriot.net','c99b-2a01-14-8020-7e20-4149-3c30-a6b3-baa8.ngrok-free.app']
#ALLOWED_HOSTS = ['ctctlab.helioho.st','127.0.0.1','192.168.1.18','localhost','1308-193-136-124-214.ngrok-free.app']

CSRF_TRUSTED_ORIGINS = ['https://throbbing-river-82258.pktriot.net', 'https://c99b-2a01-14-8020-7e20-4149-3c30-a6b3-baa8.ngrok-free.app']

""" CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8081",
    "https://c99b-2a01-14-8020-7e20-4149-3c30-a6b3-baa8.ngrok-free.app",
] """

CORS_ALLOWED_ORIGINS = [
    "https://c99b-2a01-14-8020-7e20-4149-3c30-a6b3-baa8.ngrok-free.app",
    "http://localhost:8080",
    "https://throbbing-river-82258.pktriot.net",
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
