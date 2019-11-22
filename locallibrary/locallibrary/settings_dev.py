# settings_dev.py
#
# settings.py (used for production) is completely agnostic to the fact that any
# other environments even exist.
#
#  To see the difference between prod and dev you just look into a
# single location - settings_dev.py. No need to gather configurations
# scattered across settings_prod.py, settings_dev.py and settings_shared.py.
#
# If someone adds a setting to your prod config after troubleshooting a
# production issue you can rest assured that it will appear in your dev
# config as well (unless explicitly overridden). Thus the divergence
# between different config files will be minimized.

# On a dev machine run your Django app with:
# DJANGO_SETTINGS_MODULE=<your_app_name>.settings_dev python3 manage.py runserver

from .settings import *

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'NAME': 'library',
        'USER': 'test',
        'PASSWORD': 'test',
    }
}
