# -*- coding: utf-8 -*-

from flask.ext.babel import gettext as _
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required


class BaseDocumentForm(Form):
    title = TextField(_('Title'), validators=[Required()])
    content = TextAreaField(_('Content'), validators=[Required()])


class SearchForm(Form):
    search = TextField('Search',
                       description=_(u'Search'), validators=[Required()])
