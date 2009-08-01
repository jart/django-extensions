
from math import ceil
from datetime import datetime
from django import template
from django.template import Node, Variable, Template, Context
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext as _p
from django_extensions.l10n import get_locale
from django_extensions.l10n.formatting import format_currency, format_datetime, \
    format_date, format_percent, format_number, format_decimal

register = template.Library()

@register.filter
def currency(amount, currency="USD"):
    if not amount:
        return None
    return format_currency(amount, currency)

@register.tag
def currency(parser, token):
    class CurrencyNode(Node):
        def __init__(self, amount, currency, *extra):
            self.amount = Variable(amount)
            self.currency = Variable(currency)
            if len(extra) >= 1:
                self.precision = int(extra[0])
            else:
                self.precision = None

        def render(self, context):
            amount = self.amount.resolve(context)
            currency = self.currency.resolve(context)
            return format_currency(amount, currency, precision=self.precision)

    bits = token.split_contents()[1:]
    if len(bits) < 2:
        raise TemplateSyntaxError("{% currency <amount> <currency> [precision] %}")
    return CurrencyNode(*bits)

@register.tag
def lang_name(parser, token):
    class LangNameNode(Node):
        def __init__(self, lang):
            self.lang = Variable(lang)

        def render(self, context):
            lang = self.lang.resolve(context)
            return get_locale().languages[lang]

    bits = token.split_contents()[1:]
    if len(bits) != 1:
        raise TemplateSyntaxError("{% lang_name <lang> %}")
    return LangNameNode(*bits)

@register.filter
def number(number):
    return format_number(number)

@register.filter
def percent(number): # 0.34 -> 34%
    return format_percent(number)

@register.filter
def decimal(number, precision=None):
    if precision == '' or precision is None:
        return format_decimal(number)
    else:
        return format_decimal(number, int(precision))

@register.filter
def decimal_shift(number): # 0.34 -> 34.0
    return Decimal(str(number)).shift(Decimal(str(number)))

@register.filter
def date_short(dt):
    if not dt: return '?'
    return format_date(dt, 'short')

@register.filter
def datetime_short(dt):
    if not dt: return '?'
    return format_datetime(dt, 'short')
register.filter('datetime', datetime_short)

@register.filter
def datetime_medium(dt):
    if not dt: return '?'
    return format_datetime(dt, 'medium')

@register.filter
def datetime_long(dt):
    if not dt: return '?'
    return format_datetime(dt, 'long')

@register.tag
def current_time_in_zone(parser, token):
    class CurrentTimeInZoneNode(Node):
        def __init__(self, zone):
            self.zone = Variable(zone)
        def render(self, context):
            return format_datetime(datetime.now(), 'long', self.zone.resolve(context))
    bits = token.split_contents()[1:]
    if len(bits) < 1:
        raise TemplateSyntaxError("'current_time_in_zone' statement requires an argument")
    return CurrentTimeInZoneNode(bits[0])

@register.filter
def countryname(code):
    if not code:
        return u'None'
    return get_locale().territories[code]

@register.filter
def timespan(seconds):
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "?"
    if seconds <= 60 * 2:
        return _("%(seconds)d sec") % {'seconds': seconds}
    elif seconds <= 60 * 60 * 2:
        return _("%(minutes)d min") % {'minutes': int(ceil(seconds / 60.0))}
    elif seconds <= 60 * 60 * 24 * 2:
        return _("%(hours)d hours %(minutes)d min") % {'hours': int(round(seconds / 60 / 60)),
                                                       'minutes': int(seconds / 60) % 60}
    elif seconds <= 60 * 60 * 24 * 30:
        return _("%(days)d days") % {'days': int(round(seconds / 60 / 60 / 24))}
    else:
        return _("~%(months)d months") % {'months': int(round(seconds / 60 / 60 / 24 / 30))}

@register.filter
def billing_timespan(seconds):
    """More verbose version for describing a timespan when they get
    billed by the minute"""
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "?"
    if seconds < 60:
        return _p("%(seconds)d Second", "%(seconds)d Seconds", seconds) % {'seconds': seconds}
    elif seconds == 60:
        return _p("%(minutes)d Minute", "%(minutes)d Minutes", 1) % {'minutes': 1}
    else:
        minutes = int(seconds / 60.0)
        seconds = seconds % 60
        return _("%(thing1)s and %(thing2)s" % {
                'thing1': _p("%(minutes)d Minute", "%(minutes)d Minutes", minutes) % {'minutes': minutes},
                'thing2': _p("%(seconds)d Second", "%(seconds)d Seconds", seconds) % {'seconds': seconds}})
