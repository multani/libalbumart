import logging
from urllib import urlencode
import urllib2
from xml.etree import ElementTree as ETree

from libalbumart.utils import LazyURLsOpener


class LastFM(object):
    """Retrieve covers from Last.fm

    This plugin is largely inspired by the Last.fm plugin found in Exaile,
    updated to fit into this library. Thanks for the original authors Adam Olsen
    and Johannes Schwarz!
    """

    url = "http://ws.audioscrobbler.com/2.0/"
    url_params = {
        'method': 'type.search',
        'type': None,
        'api_key': None,
    }


    # API Key used for internal purpose (test) of the lib
    # Please please please, get your own key on http://last.fm/api if you want
    # to use this plugin in an application, thanks!
    API_KEY = "166213f4a8ec2e428923dbd9ea9c87b7"

    def __init__(self, url_opener=None):
        self.logger = logging.getLogger("libalbumart.plugins.lastfm")

        if url_opener is None:
            self.opener = urllib2.build_opener()
        else:
            self.opener = url_opener

    def find_covers(self, artist, album, title):
        self.logger.info(
            "Searching cover with artist %r, album %r and title %r",
            artist, album, title)

        for type, value in [('album', album), ('track', title)]:
            params = {
                'method': '%s.search' % type,
                type: value.encode('utf-8'),
                'api_key': self.API_KEY,
            }
            url = "%s?%s" % (self.url, urlencode(params))

            self.logger.debug("Calling URL: %s", url)

            try:
                data = self.opener.open(url).read()
            except IOError:
                continue

            xml = ETree.fromstring(data)

            for element in xml.getiterator(type):
                if element.find('artist').text == artist.encode("utf-8"):
                    for sub_element in element.findall('image'):
                        if sub_element.attrib['size'] == 'extralarge':
                            url = sub_element.text
                            if url:
                                return LazyURLsOpener([url], self.opener)

        return []
