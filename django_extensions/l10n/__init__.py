
from django_extensions.middleware.request import PAIN

def default_locale():
    from babel import Locale
    DEFAULT_LOCALE = Locale.parse(settings.LANGUAGE_CODE, sep='-')
    return DEFAULT_LOCALE

def get_locale():
    try:
        return PAIN.request.locale
    except AttributeError:
        return default_locale()

def get_country():
    from django.conf import settings
    try:
        return PAIN.request.country
    except AttributeError:
        try:
            return settings.DEFAULT_COUNTRY
        except AttributeError:
            return 'US'

def get_timezone():
    from django.conf import settings
    try:
        return PAIN.request.timezone
    except AttributeError:
        return settings.DEFAULT_TIMEZONE
