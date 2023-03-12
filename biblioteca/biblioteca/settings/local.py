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



BASE_DIRE = os.path.dirname(os.path.abspath(__file__))

# STATICFILES_DIRS = (
#         os.path.join(BASE_DIRE, 'static'),
#     )

STATIC_URL = '/static/'

static = BASE_DIR.child('static')
css = static.child('css')
img = static.child('img')
js = static.child('js')

STATICFILES_DIRS = [static, css,img, js,]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



MEDIA_URL = '/media/'


MEDIA_ROOT =BASE_DIR.child('media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

