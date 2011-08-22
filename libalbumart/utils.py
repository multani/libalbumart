import urllib


class LazyURLsOpener(object):
    """Lazy open a list of URLs, on demand

    This is basically an iterator over a list of URLs, which are opened only
    when the URL is request during the iteration.
    """

    def __init__(self, urls, url_opener=None):
        self.urls = urls
        if url_opener is None:
            self.opener = urllib.FancyURLopener()
        else:
            self.opener = url_opener

    def __len__(self):
        return len(self.urls)

    def __iter__(self):
        for url in self.urls:
            yield self.opener.open(url)
