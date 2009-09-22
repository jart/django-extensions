
import re
import pytz
import babel
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from django_extensions.l10n import get_locale

def linux_timezones():
    """
    Returns the names of all timezones in Linux's zone.tab file.
    """
    import os.path
    if not os.path.exists('/usr/share/zoneinfo/zone.tab'):
        return
    for line in open('/usr/share/zoneinfo/zone.tab'):
        if not line or line.startswith('#'):
            continue
        yield line.split('\t')[2].strip()

def supported_timezones():
    """
    Returns the names of all timezones supported by linux, pytz AND
    babel.
    """
    res = set(babel.core.get_global('meta_zones')).\
        intersection(set(pytz.all_timezones))
    linux_zones = set(linux_timezones())
    if linux_zones:
        return res.intersection(linux_zones)
    else:
        return res

SYSTEMZONE = pytz.timezone(settings.TIME_ZONE)
SUPPORTED_TIMEZONES = supported_timezones()

def valid_timezone(tzname):
    return (tzname in SUPPORTED_TIMEZONES)

def localize_timezone(dt, localzone):
    if not isinstance(localzone, tzinfo):
        localzone = pytz.timezone(localzone)
    dt = dt.replace(tzinfo=SYSTEMZONE)
    #return localzone.normalize(dt.astimezone(localzone))
    return dt.astimezone(localzone)

def localized_timezones(group=False, truncate=True):
    """
    This function is a doozy.  Returns a list of timezones
    translated to your locale.  Usually used for displaying on an
    HTML form in a select box.
    """
    locale = get_locale()
    key = 'localized_timezones_%s%s%s' % (
        locale, ['', '_grouped'][group], ['', '_truncated'][group])
    zones = cache.get(key)
    if zones is not None:
        zones.sort(key=lambda t: t[1])
        return zones

    if group:
        zones = {}
    else:
        zones = []
    dups = {}
    # certain locales like en_US will assign the same name to a whole
    # bunch of different zones.  dups detects duplicate names so we
    # can append extra data to differentiate the duplicated zones
    for tzname in SUPPORTED_TIMEZONES:
        name = dates.get_timezone_name(pytz.timezone(tzname), locale=locale)
        if name in dups:
            dups[name] += 1
        else:
            dups[name] = 0
    for tzname in SUPPORTED_TIMEZONES:
        # utc offsets change so feed in current date
        tz = pytz.timezone(tzname)
        dt = datetime.now(tz=tz)
        gmt = dates.get_timezone_gmt(dt, locale=locale)
        try:
            name = dates.get_timezone_name(tz, locale=locale)
        except KeyError:
            # ceratin locales like 'no' will raise "KeyError: 'ZZ'"
            # because they don't have any zone information at the moment
            name = dates.get_timezone_name(dt, locale=DEFAULT_LOCALE)
        if dups[name]:
            name = "%s (%s)" % (name, tzname[tzname.index('/')+1:].replace('_', ' '))
        if group:
            if gmt not in zones:
                zones[gmt] = []
            if truncate:
                zones[gmt].append((tzname, smart_truncate(name, 35)))
            else:
                zones[gmt].append((tzname, name))
        else:
            if truncate:
                zones.append((tzname, smart_truncate("%s - %s" % (gmt, name), 45)))
            else:
                zones.append((tzname, "%s - %s" % (gmt, name)))
    if group:
        zones = zones.items()
        zones.sort(key=lambda t: t[0])
        for k, v in zones:
            v.sort(key=lambda t: t[1])
    else:
        zones.sort(key=lambda t: t[1])

    cache.set(key, zones)
    return zones
