# -*- coding: utf-8 -*-

from random import random
from time import time

from flask.ext.babel import gettext as _
from flask.ext.babel import lazy_gettext as _l


def sizeof_fmt(num):
    for x in [_l('bytes'), _l('KB'), _l('MB'), _l('GB')]:
        if num < 1024.0 and num > -1024.0:
            return "{0:3.1f}{1}".format(num, x)
        num /= 1024.0
    return "{0:3.1f}{1}".format(num, _('TB'))


def genid(key=None):
    alphabet = "23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"
    base = len(alphabet)
    block_size = 32
    mask = (1 << block_size) - 1
    mapping = range(block_size)

    def encode(n):
        return (n & ~mask) | _encode(n & mask)

    def _encode(n):
        result = 0
        for i, b in enumerate(reversed(mapping)):
            if n & (1 << i):
                result |= (1 << b)
        return result

    def enbase(x, min_length=6):
        result = _enbase(x)
        padding = alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)

    def _enbase(x):
        n = len(alphabet)
        if x < n:
            return alphabet[x]
        return _enbase(int(x / n)) + alphabet[int(x % n)]

    if key is None:
        key = int(int(time() * 1000) * random())

    return enbase(encode(key))
