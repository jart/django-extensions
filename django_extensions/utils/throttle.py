"""
Useful for rate limiting login attempts, payments, and more.
"""

from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache

def throttle_is_over_limit(ip, class_name, limit):
    if ip in settings.INTERNAL_IPS or settings.DEBUG:
        return False
    k = "throttle_%s" % (ip)
    data = cache.get(k)
    if data is None:
        return False
    if data['expires'] < datetime.now():
        cache.delete(k)
        return False
    return (data.get(class_name, 0) >= limit)

def throttle_increment(ip, class_name, delta=1):
    if ip in settings.INTERNAL_IPS or settings.DEBUG:
        return
    k = "throttle_%s" % (ip)
    data = cache.get(k)
    if data is None or datetime.now() > data['expires']:
        # we need to specify a date in both places as the age of the
        # object in memcached resets each time it's accessed
        cache.set(k, {'expires': datetime.now() + timedelta(days=1),
                      class_name: delta},
                  60 * 60 * 24)
    else:
        data[class_name] = data.get(class_name, 0) + delta
        cache.set(k, data, (data['expires'] - datetime.now()).seconds)
