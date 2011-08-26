import httplib
import os
import urllib
import urllib2


class CachingHTTPHandler(urllib2.HTTPHandler, object):
    def __init__(self, caching_dir):
        super(self.__class__, self).__init__()
        self.nb_calls = 0
        self.caching_dir = caching_dir

    @property
    def current_cache_path(self):
        return os.path.join(self.caching_dir, "%d.cache" % self.nb_calls)

    def http_open(self, request):
        self.nb_calls += 1

        if isinstance(request, basestring):
            url = request
        else:
            url = request.get_full_url()

        self.parent.urls_called.append(url)

        if 'LIBALBUM_ART_TEST_ONLINE' in os.environ:
            return super(self.__class__, self).http_open(request)

        self.cache_request(request, self.current_cache_path)

        if os.path.exists(self.current_cache_path):
            return self.uncache_response(url, self.current_cache_path)
        else:
            response = super(self.__class__, self).http_open(request)
            self.cache_response(response, self.current_cache_path)
            return response

    def cache_request(self, request, path):
        with open("%s.request" % path, 'w') as fp:
            fp.write('%s %s\n' % (
                'GET' if not request.data else 'POST',
                request.get_full_url()))
            fp.write("Host: %s\n" % request.host)

            for v in sorted(request.headers.items()):
                fp.write("%s: %s\n" % v)

            if request.data:
                fp.write("\n%s\n" % request.data)

    def cache_response(self, response, path):
        with open("%s.headers" % path, 'w') as fp:
            for header, value in response.headers.items():
                fp.write("%s: %s\n" % (header, value))

        fp = open(path, 'w')
        def read():
            data = response.old_read()
            fp.write(data)
            return data

        response.old_read = response.read
        response.read = read

    def uncache_response(self, url, path):
        return urllib.addinfourl(
            open(path),
            httplib.HTTPMessage(open(path + ".headers")),
            url)


class CachingOpener(urllib2.OpenerDirector):
    def __init__(self, caching_dir, *args, **kwargs):
        urllib2.OpenerDirector.__init__(self, *args, **kwargs)

        self.caching_dir = caching_dir

        # May be cleared by the tests
        self.urls_called = []

        self.add_handler(CachingHTTPHandler(caching_dir))
