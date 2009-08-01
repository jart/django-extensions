"""
Hack: We use the __deepcopy__ method to set field attributes that that
need to be refreshed for each visitor.  Maybe we should just write our
own widget.
"""

from babel import numbers, dates
from django import forms
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import SafeString
from django_extensions.l10n import get_timezone, get_country
from django_extensions.l10n.timezone import localized_timezones, valid_timezone
from django_extensions.l10n.contry import localized_countries, valid_country_code
from django_extensions.l10n.phonenumber import parse_pstn_number, parse_caller_id, \
    e164_format, e164_to_nanp

class IntegerField(forms.IntegerField):
    def clean(self, value):
        locale = get_request().locale
        value = value.replace(numbers.get_group_symbol(locale), '')
        return forms.IntegerField(self, value)

class DecimalInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        value = str(format_decimal(force_unicode(value)))
        return forms.TextInput.render(self, name, value, attrs)

class DecimalField(forms.DecimalField):
    widget = DecimalInput

    def clean(self, value):
        locale = get_request().locale
        value = value.\
            replace(numbers.get_group_symbol(locale), '').\
            replace(numbers.get_decimal_symbol(locale), '.')
        return forms.DecimalField(self, value)

class CountryField(forms.ChoiceField):
    def __deepcopy__(self, memo):
        res = forms.ChoiceField.__deepcopy__(self, memo)
        res.choices = localized_countries()
        if not res.initial:
            res.initial = get_country()
        return res

    def clean(self, value):
        if not valid_country_code(value):
            raise forms.ValidationError("Invalid Timezone")
        return value

class TimeZoneField(forms.ChoiceField):
    def __deepcopy__(self, memo):
        res = forms.ChoiceField.__deepcopy__(self, memo)
        res.choices = localized_timezones()
        if not res.initial:
            res.initial = get_timezone()
        return res

    def clean(self, value):
        if not value:
            raise forms.ValidationError(_("Please select a timezone"))
        if not valid_timezone(value):
            raise forms.ValidationError(_("Invalid Timezone"))
        return value

class MonthField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.width = kwargs.pop('width', 'abbreviated')
        forms.ChoiceField.__init__(self, *args, **kwargs)

    def __deepcopy__(self, memo):
        res = forms.ChoiceField.__deepcopy__(self, memo)
        res.choices = dates.get_month_names(
            width=self.width, locale=get_request().locale).items()
        return res

    def clean(self, value):
        return int(forms.ChoiceField.clean(self, value))

class PhoneInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        if not value:
            value = u''
        country = get_country()
        try:
            value = e164_format(parse_pstn_number(value, country), country)
        except ValueError:
            value = ''
        return forms.TextInput.render(self, name, value, attrs)

class PhoneNumberField(forms.CharField):
    widget = PhoneInput
    def __init__(self, *args, **kwargs):
        self.is_cid = kwargs.pop('is_cid', False)
        kwargs['max_length'] = 25
        kwargs['min_length'] = 5
        forms.CharField.__init__(self, *args, **kwargs)

    def clean(self, value):
        if not value:
            if not self.required:
                return ''
            else:
                raise forms.ValidationError(_("This field is required"))
        if self.is_cid:
            if value.strip().lower() in ('', 'unavailable', 'anonymous'):
                return ''
        try:
            return e164_to_nanp(parse_pstn_number(value, get_country()))
        except ValueError:
            raise forms.ValidationError(_("Invalid phone number"))
