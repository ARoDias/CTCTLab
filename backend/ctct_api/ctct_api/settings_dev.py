# settings_dev.py
import os
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# Allow all hosts during development
ALLOWED_HOSTS = ['*']

# Database configuration for development
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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
