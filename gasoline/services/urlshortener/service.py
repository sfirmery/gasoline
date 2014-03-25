# -*- coding: utf-8 -*-
"""Based on https://pypi.python.org/pypi/short_url"""

from gasoline.services.base import Service
from .models import ShortURL

__all__ = ['URLShortenerService']

MIN_LENGTH = 5


class URLShortenerService(Service):
    name = 'urlshortener'

    alphabet = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    base = len(alphabet)
    block_size = 32
    mask = (1 << block_size) - 1
    mapping = range(block_size)

    last_id = 0

    def init_app(self, app):
        """initialise url shortener service with flask configuration"""
        last_url = ShortURL.objects.order_by('-id').first()
        if last_url is not None:
            self.last_id = last_url.id
        super(URLShortenerService, self).init_app(app)

    def shorten(self, url):
        """shorten an url and save it to database"""
        url_id = self.last_id + 1
        short_url = ShortURL(id=url_id, url=url)
        short_url.save()
        self.last_id += 1
        return self.encode_url(url_id)

    def extend(self, short_url):
        """search an url in database"""
        if short_url is None:
            return None
        url = ShortURL.objects(id=self.decode_url(short_url)).first()
        if url is None:
            return None
        return url.url

    def encode_url(self, n, min_length=MIN_LENGTH):
        return self.enbase(self.encode(n), min_length)

    def decode_url(self, n):
        return self.decode(self.debase(n))

    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)

    def _encode(self, n):
        result = 0
        for i, b in enumerate(reversed(self.mapping)):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)

    def _decode(self, n):
        result = 0
        for i, b in enumerate(reversed(self.mapping)):
            if n & (1 << b):
                result |= (1 << i)
        return result

    def enbase(self, x, min_length=MIN_LENGTH):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)

    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(int(x / n)) + self.alphabet[int(x % n)]

    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result
