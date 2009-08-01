
from babel import Locale, UnknownLocaleError
from django.conf import settings

class LocalizationMiddleware(object):
    def process_request(self, request):
        try:
            request.locale = Locale.parse(request.LANGUAGE_CODE, sep='-')
        except (ValueError, UnknownLocaleError):
            pass
