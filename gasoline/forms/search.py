# -*- coding: utf-8 -*-

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required

__all__ = ['SearchForm']


class SearchForm(Form):
    query = TextField(_('Search'),
                      description=_(u'Search'), validators=[Required()])
