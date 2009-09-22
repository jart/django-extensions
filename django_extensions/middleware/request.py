
try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

PAIN = local()

def global_request():
    return PAIN.request

class GlobalRequestMiddleware(object):
    def process_request(self, request):
        PAIN.request = request
