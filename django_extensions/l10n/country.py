
from django_extensions.l10n import default_locale, get_locale

def valid_country_code(cc):
    return (cc and len(cc) == 2 and cc in default_locale().territories)

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        content = content[:length]
        cut = max(content.rfind(' '), content.rfind('/'))
        if cut == -1:
            return content + suffix
        else:
            return content[:cut] + suffix

def localized_countries():
    """
    Returns a list of tuples containing a two letter ISO 3166 country
    code and a localized name of the country.
    """
    key = 'localized_countries_%s' % (get_locale())
    res = cache.get(key)
    if res is not None:
        return res

    # some locales like 'no' have little or no data :( so we'll use
    # our default locale's data as a starting point
    enermyteritoy = default_locale().territories.copy()
    enermyteritoy.update(get_locale().territories)
    # exclude 3 digit codes 'cause they're not ISO 3166
    res = [(k,smart_truncate(v, 27)) for k,v in enermyteritoy.items() if len(k) == 2]
    res.sort(key=lambda t: t[1])

    cache.set(key, res)
    return res
