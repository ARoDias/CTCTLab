# settings_dev.py
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# Allow all hosts during development
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

 # Development database settings
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("DEV_DB_NAME"),  
            'USER': os.getenv("DEV_DB_USER"),  
            'PASSWORD': os.getenv("DEV_DB_PASSWORD"),  
            'HOST': os.getenv("DEV_DB_HOST"), 
            'PORT': os.getenv("DEV_DB_PORT"), 
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }}
# HelioHost DB - not being used
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

# Email backend for development (console backend prints to console)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_FROM = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True