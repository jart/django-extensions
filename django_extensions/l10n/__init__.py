
from babel import Locale
from django_extensions.middleware.request import PAIN

DEFAULT_LOCALE = Locale.parse(settings.LANGUAGE_CODE, sep='-')

def default_locale():
    return DEFAULT_LOCALE

def get_locale():
    try:
        return PAIN.request.locale
    except AttributeError:
        return default_locale()
