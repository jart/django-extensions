
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

PAIN = local()

def global_request():
    if hasattr(REQUEST_LOCAL, 'request'):
        return PAIN.request
    else:
        return None

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        PAIN.request = request
