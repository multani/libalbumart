import os
try:
    # Python < 2.7
    import unittest2 as unittest
except ImportError:
    import unittest

from libalbumart.tests.utils import CachingOpener


HERE = os.path.dirname(os.path.abspath(__file__))


class LastFMTestCase(unittest.TestCase):

    fixtures_dir = os.path.join(HERE, 'fixtures', 'lastfm')

    def setUp(self):
        self.opener = CachingOpener(self.fixtures_dir)

    def _makeCtx(self):
        from libalbumart.plugins.lastfm import LastFM
        return LastFM(self.opener)

    def test_find_cover(self):
        ctx = self._makeCtx()

        covers = ctx.find_covers("Iron Maiden",
                                 "Somewhere In Time",
                                 "Caught Somewhere In Time")

        self.assertEqual(['http://ws.audioscrobbler.com/2.0/?album=Somewhere+In+Time&api_key=166213f4a8ec2e428923dbd9ea9c87b7&method=album.search'],
                         self.opener.urls_called)
        self.opener.urls_called = []

        from libalbumart.utils import LazyURLsOpener
        self.assertTrue(isinstance(covers, LazyURLsOpener))
        self.assertEqual(1, len(covers))

        item = iter(covers).next()
        self.assertEqual(['http://userserve-ak.last.fm/serve/300x300/62429725.png'],
                        self.opener.urls_called)
        self.assertTrue(hasattr(item, 'read'))
