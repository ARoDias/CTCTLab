# settings_prod.py
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allowed hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': os.getenv("DB_NAME", "default_db_name"),  
        'USER': os.getenv("DB_USER", "root"),  
        'PASSWORD': os.getenv("DB_PASSWORD", ""),  
        'HOST': os.getenv("DB_HOST", "localhost"), 
        'PORT': os.getenv("DB_PORT", "3306"), 
          'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Email configuration for production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

