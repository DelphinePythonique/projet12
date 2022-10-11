from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ceciestmasecretkeymouahahh"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_test_epic_test',
        'USER': 'epic',
        'PASSWORD': 'EPIC_PASSWORD',
        'HOST': 'localhost',
        'PORT': '45432',
    }
}
