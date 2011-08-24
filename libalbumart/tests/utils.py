import os
import urllib2


class CachingOpener(urllib2.OpenerDirector):
    def __init__(self, caching_dir, *args, **kwargs):
        urllib2.OpenerDirector.__init__(self, *args, **kwargs)

        self.caching_dir = caching_dir
        self.nb_calls = 0

        # May be cleared by the tests
        self.urls_called = []

        # From urllib2.build_opener()
        for handler in [urllib2.ProxyHandler, urllib2.UnknownHandler,
                        urllib2.HTTPHandler, urllib2.HTTPDefaultErrorHandler,
                        urllib2.HTTPRedirectHandler, urllib2.FTPHandler,
                        urllib2.FileHandler, urllib2.HTTPErrorProcessor]:
            self.add_handler(handler())

    def open(self, req):
        if isinstance(req, basestring):
            url = req
        else:
            url = req.get_full_url()

        self.urls_called.append(url)
        self.nb_calls += 1

        if 'LIBALBUM_ART_TEST_ONLINE' in os.environ:
            return urllib2.OpenerDirector.open(self, url)

        # XXX maybe there's a better way, using maybe an handler, to do this
        # caching stuff...

        cache_path = os.path.join(self.caching_dir,
                                  "%d.cache" % self.nb_calls)

        try:
            # XXX not an actual urllib2.urlopen() object
            return open(cache_path)
        except IOError:
            result = urllib2.OpenerDirector.open(self, url)
            return CacheSaverResult(result, cache_path)


class CacheSaverResult(object):
    def __init__(self, fp, dest):
        self.fp = fp
        self.dest = dest

    def read(self):
        data = self.fp.read()
        with open(self.dest, 'w') as fp:
            fp.write(data)
        return data
