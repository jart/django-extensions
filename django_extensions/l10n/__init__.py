
from babel import Locale
from django.conf import settings
from django_extensions.middleware.request import PAIN

DEFAULT_LOCALE = Locale.parse(settings.LANGUAGE_CODE, sep='-')

def default_locale():
    return DEFAULT_LOCALE

def get_locale():
    try:
        return PAIN.request.locale
    except AttributeError:
        return default_locale()

def get_country():
    try:
        return PAIN.request.country
    except AttributeError:
        return settings.DEFAULT_COUNTRY

def get_timezone():
    try:
        return PAIN.request.timezone
    except AttributeError:
        return settings.DEFAULT_TIMEZONE
