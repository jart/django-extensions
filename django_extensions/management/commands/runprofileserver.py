"""
runprofileserver.py

Starts a lightweight Web server with profiling enabled.  Produces output
for CacheGrind.

Debian/Ubuntu Users:

sudo apt-get install kcachegrind kcachegrind-converters

To Use:

$ ./manage.py --nomedia --prof-path=profiles

*go crazy visiting pages like /blog/love/*

$ ls profiles
blog.love_000050ms_2009-08-07T13:28:56.649857.prof
blog.love_000002ms_2009-08-07T13:29:00.643459.prof

Why did the first request take 50 milliseconds?  :(

$ kcachegrind blog.love_000050ms_2009-08-07T13:28:56.649857.prof

The rest is totally amazing.
"""

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from datetime import datetime
import os
import sys
import time
import thread

def label(code):
    if isinstance(code, str):
        return ('~', 0, code)    # built-in functions ('~' sorts at the end)
    else:
        return '%s %s:%d' % (code.co_name,
                             code.co_filename,
                             code.co_firstlineno)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noreload', action='store_false', dest='use_reloader', default=True,
            help='Tells Django to NOT use the auto-reloader.'),
        make_option('--adminmedia', dest='admin_media_path', default='',
            help='Specifies the directory from which to serve admin media.'),
        make_option('--prof-path', dest='prof_path', default='/tmp',
            help='Specifies the directory which to save profile information in.'),
        make_option('--nomedia', action='store_true', dest='no_media', default=False,
            help='Do not profile MEDIA_URL and ADMIN_MEDIA_URL'),
    )
    help = "Starts a lightweight Web server with profiling enabled."
    args = '[optional port number, or ipaddr:port]'

    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False

    def handle(self, addrport='', *args, **options):
        import django
        from django.core.servers.basehttp import run, AdminMediaHandler, WSGIServerException
        from django.core.handlers.wsgi import WSGIHandler
        if args:
            raise CommandError('Usage is runserver %s' % self.args)
        if not addrport:
            addr = ''
            port = '8000'
        else:
            try:
                addr, port = addrport.split(':')
            except ValueError:
                addr, port = '', addrport
        if not addr:
            addr = '127.0.0.1'

        if not port.isdigit():
            raise CommandError("%r is not a valid port number." % port)

        use_reloader = options.get('use_reloader', True)
        admin_media_path = options.get('admin_media_path', '')
        shutdown_message = options.get('shutdown_message', '')
        no_media = options.get('no_media', False)
        quit_command = (sys.platform == 'win32') and 'CTRL-BREAK' or 'CONTROL-C'

        def inner_run():
            from django.conf import settings

            import hotshot, time, os
            prof_path = options.get('prof_path', '/tmp')
            def make_profiler_handler(inner_handler):
                def handler(environ, start_response):
                    path_info = environ['PATH_INFO']
                    # normally /media/ is MEDIA_URL, but in case still check it in case it's differently
                    # should be hardly a penalty since it's an OR expression.
                    # TODO: fix this to check the configuration settings and not make assumpsions about where media are on the url
                    if no_media and (path_info.startswith('/media') or path_info.startswith(settings.MEDIA_URL)):
                        return inner_handler(environ, start_response)
                    path_name = path_info.strip("/").replace('/', '.') or "root"
                    profname = "%s.%s.prof" % (path_name, datetime.now().isoformat())
                    profname = os.path.join(prof_path, profname)
                    prof = hotshot.Profile(profname)
                    start = datetime.now()
                    try:
                        return prof.runcall(inner_handler, environ, start_response)
                    finally:
                        # seeing how long the request took is important!
                        elap = datetime.now() - start
                        elapms = elap.seconds * 1000.0 + elap.microseconds / 1000.0
                        prof.close()
                        profname2 = "%s_%06dms_%s.prof" % (path_name, elapms, datetime.now().isoformat())
                        profname2 = os.path.join(prof_path, profname2)
                        def lawl():
                            time.sleep(0.2)
                            os.spawnlp(os.P_WAIT, "hotshot2calltree", "hotshot2calltree",
                                       profname, '-o', profname2)
                            os.unlink(profname)
                        thread.start_new_thread(lawl, ())
                return handler

            print "Validating models..."
            self.validate(display_num_errors=True)
            print "\nDjango version %s, using settings %r" % (django.get_version(), settings.SETTINGS_MODULE)
            print "Development server is running at http://%s:%s/" % (addr, port)
            print "Quit the server with %s." % quit_command
            try:
                path = admin_media_path or django.__path__[0] + '/contrib/admin/media'
                handler = make_profiler_handler(AdminMediaHandler(WSGIHandler(), path))
                run(addr, int(port), handler)
            except WSGIServerException, e:
                # Use helpful error messages instead of ugly tracebacks.
                ERRORS = {
                    13: "You don't have permission to access that port.",
                    98: "That port is already in use.",
                    99: "That IP address can't be assigned-to.",
                }
                try:
                    error_text = ERRORS[e.args[0].args[0]]
                except (AttributeError, KeyError):
                    error_text = str(e)
                sys.stderr.write(self.style.ERROR("Error: %s" % error_text) + '\n')
                # Need to use an OS exit because sys.exit doesn't work in a thread
                os._exit(1)
            except KeyboardInterrupt:
                if shutdown_message:
                    print shutdown_message
                sys.exit(0)
        if use_reloader:
            from django.utils import autoreload
            autoreload.main(inner_run)
        else:
            inner_run()
