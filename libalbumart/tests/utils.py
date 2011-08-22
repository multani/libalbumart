import os
import urllib


class CachingOpener(urllib.FancyURLopener):
    def __init__(self, caching_dir, *args, **kwargs):
        urllib.FancyURLopener.__init__(self, *args, **kwargs)

        self.caching_dir = caching_dir
        self.nb_calls = 0

        # May be cleared by the tests
        self.urls_called = []

    def open(self, url, data=None):
        self.urls_called.append(url)
        self.nb_calls += 1

        if 'LIBALBUM_ART_TEST_ONLINE' in os.environ:
            return urllib.FancyURLopener.open(self, url, data)

        cache_path = os.path.join(self.caching_dir,
                                  "%d.cache" % self.nb_calls)

        try:
            # XXX not an actual urllib.urlopen() object
            return open(cache_path)
        except IOError:
            result = urllib.FancyURLopener.open(self, url, data)
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
