
import sys
from recaptcha.client import captcha
from django import forms
from django.conf import settings
from django.http import get_request
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_extensions.utils.throttle import throttle_is_over_limit, throttle_increment

class ReCaptchaWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        attrs = self.build_attrs(attrs, name=name)
        ip = get_request().META['REMOTE_ADDR']
        if attrs['do_hiding'] and throttle_is_over_limit(ip, attrs['hide_class'], attrs['hide_for']):
            return u''
        html = []
        html.append("<div id=\"captcha\">")
        html.append("<script>var RecaptchaOptions = {theme : '%s'};</script>" % (attrs.get('theme', 'white')))
        html.append('<script type="text/javascript"')
        html.append('        src="https://api-secure.recaptcha.net/challenge?k=%s">' % (attrs['public_key']))
        html.append('</script>')
        html.append('<noscript>')
        html.append('  <iframe src="https://api-secure.recaptcha.net/noscript?k=%s"' % (attrs['public_key']))
        html.append('          height="300" width="500" frameborder="0"></iframe><br>')
        html.append('  <textarea name="recaptcha_challenge_field" rows="3" cols="40">')
        html.append('  </textarea>')
        html.append('  <input type="hidden" name="recaptcha_response_field" value="manual_challenge">')
        html.append('</noscript>')
        html.append(u"</div>")
        return mark_safe("\n".join(html))

    def value_from_datadict(self, data, files, name):
        return {
            'recaptcha_challenge_field': data.get('recaptcha_challenge_field', None),
            'recaptcha_response_field': data.get('recaptcha_response_field', None),
        }

class ReCaptchaField(forms.Field):
    error_messages = {
        'incorrect-captcha-sol':  _("Invalid entry, please try again."),
        'invalid-site-public-key':  "Invalid public key",
        'invalid-site-private-key':  "Invalid private key",
        'invalid-request-cookie':  "Invalid cookie",
        'verify-params-incorrect':  "The parameters to /verify were incorrect, make sure you are passing all the required parameters.",
        'invalid-referrer':  "Invalid referrer domain",
        'recaptcha-not-reachable':  "Could not contact reCAPTCHA server",
    }

    def __init__(self, *args, **kwargs):
        """
        hiding=(class, count): Keeps a throttle tally under 'class' on
        the client IP and only displays captcha after the form is
        submitted 'count' times.
        """
        self.public_key = kwargs.pop('public_key', settings.RECAPTCHA_PUBLIC)
        self.private_key = kwargs.pop('private_key', settings.RECAPTCHA_PRIVATE)
        if 'hiding' in kwargs:
            self.do_hiding = True
            self.hide_class = 'recaptcha_%s' % (kwargs['hiding'][0])
            self.hide_for = kwargs['hiding'][1]
            del kwargs['hiding']
        else:
            self.do_hiding = False
            self.hide_class = None
            self.hide_for = None
        self.widget = ReCaptchaWidget({'do_hiding': self.do_hiding,
                                       'hide_class': self.hide_class,
                                       'hide_for': self.hide_for,
                                       'public_key': self.public_key})
        forms.Field.__init__(self, *args, **kwargs)

    def clean(self, data):
        ip = get_request().META['REMOTE_ADDR']
        if self.do_hiding and not throttle_is_over_limit(ip, self.hide_class, self.hide_for):
            throttle_increment(ip, self.hide_class)
            return
        try:
            resp = captcha.submit(data.get("recaptcha_challenge_field", None),
                                  data.get("recaptcha_response_field", None),
                                  self.private_key, request.META['REMOTE_ADDR'])
        except Exception, e:
            #sys.stderr.write('Recaptcha failed!  %r\n' % (e))
            pass
        else:
            if not resp.is_valid:
                raise forms.ValidationError(
                    self.error_messages.get(resp.error_code, "Unknown error"))
