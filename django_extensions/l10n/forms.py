"""
Hack: We use the __deepcopy__ method to set field attributes that that
need to be refreshed for each visitor.  Maybe we should just write our
own widget.
"""

from babel import numbers, dates
from django import forms
from django.conf import settings
from django.http import get_request
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.utils.safestring import SafeString
from django_extensions.l10n.timezone import localized_timezones, valid_timezone
from django_extensions.l10n.contry import localized_countries, valid_country_code

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
            res.initial = settings.DEFAULT_COUNTRY
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
        if not res.initial:
            res.initial = settings.DEFAULT_TIMEZONE
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
