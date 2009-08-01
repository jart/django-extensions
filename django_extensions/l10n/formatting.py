
from decimal import Decimal
from babel import numbers, dates
from django.conf import settings
from django_extensions.l10n import get_locale
from django_extensions.l10n.timezone import localize_timezone

def format_number(number):
    return numbers.format_number(int(str(number)), locale=get_locale())

def format_percent(number):
    return numbers.format_percent(Decimal(str(number)), locale=get_locale())

def format_decimal(decimal, precision=None):
    if precision:
        fmt = '#,##0.%s;-#,##0.%s' % ('0' * precision, '0' * precision)
        return numbers.format_decimal(decimal, fmt, locale=get_locale())
    else:
        return numbers.format_decimal(decimal, locale=get_locale())

def format_datetime(dt, format='short', tz=None):
    if not tz:
        tz = settings.DEFAULT_TIMEZONE
    return dates.format_datetime(localize_timezone(dt, tz), format, locale=get_locale())

def format_date(dt, format='short', tz=None):
    """Dates are only in UTC currently"""
    if not tz:
        tz = settings.DEFAULT_TIMEZONE
    return dates.format_date(dt, format, locale=get_locale())

def format_currency(amount, currency, precision=None):
    if not amount:
        return None
    if precision:
        format = u'#,##0.%s \xa4\xa4;-#,##0.%s \xa4\xa4' % ('0' * precision, '0' * precision)
        return numbers.format_currency(amount, currency, format, locale=get_locale())
    else:
        return numbers.format_currency(amount, currency, locale=get_locale())
