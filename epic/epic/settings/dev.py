from .base import *  # noqa type:ignore
from .base import MIDDLEWARE, INSTALLED_APPS, BASE_DIR

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ceciestmasecretkeymouahahh"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "epic_dev",
        "USER": "epic",
        "PASSWORD": "EPIC_PASSWORD",
        "HOST": "localhost",
        "PORT": "45432",
    }
}

MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
INSTALLED_APPS += ("debug_toolbar",)  # and other apps for local development


INTERNAL_IPS = [
    "127.0.0.1",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "../static/media/"
