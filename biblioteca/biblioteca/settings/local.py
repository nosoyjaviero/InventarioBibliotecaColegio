from .base import *
from django.apps import AppConfig

DEBUG = True

ALLOWED_HOSTS = []



DB_FILE = BASE_DIR.child('db.sqlite3')
# DB_FILE =os.path.join(BASE_DIR, 'db.sqlite3')


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_FILE,
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS =[BASE_DIR.child('static')]

MEDIA_URL = '/media/'


MEDIA_ROOT =BASE_DIR.child('media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

