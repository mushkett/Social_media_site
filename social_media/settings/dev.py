from decouple import config

from .base import *

# Development settings
INSTALLED_APPS = INSTALLED_APPS + ['django_extensions']
SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Use PostgreSQL in development (via Docker)
# Override DATABASE_URL in .env if needed
# DATABASE_URL=postgres://postgres:postgres@localhost:5432/social_media

# Disable manifest storage for development/testing (no collectstatic needed)
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}
