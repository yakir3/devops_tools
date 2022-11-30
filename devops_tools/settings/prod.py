from .base import *
from os import environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DB_ADDRESS = environ.get('DB_ADDRESS', '172.17.0.3')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'uatproxy',
        'USER': 'root',
        'PASSWORD': '123qwe123',
        'HOST': DB_ADDRESS,
        'PORT': '3306',
    }
}

TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False
