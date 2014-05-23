# -*- coding: utf-8 -*-

from flask.ext.babel import gettext as _
from flask.ext.babel import lazy_gettext as _l


def sizeof_fmt(num):
    for x in [_l('bytes'), _l('KB'), _l('MB'), _l('GB')]:
        if num < 1024.0 and num > -1024.0:
            return "{0:3.1f}{1}".format(num, x)
        num /= 1024.0
    return "{0:3.1f}{1}".format(num, _('TB'))
