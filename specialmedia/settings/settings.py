import os
from specialmedia.settings.local_settings import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'rk445853nr+y3hr&gov$sf7&$n%#=e(l@jhr4cq7=&z8&&$4qi'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'specialmedia',
    'specialGmail'
)

MIDDLEWARE_CLASSES = (
)

ROOT_URLCONF = 'specialmedia.urls'

WSGI_APPLICATION = 'specialmedia.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
