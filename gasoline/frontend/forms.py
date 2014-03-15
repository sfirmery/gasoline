# -*- coding: utf-8 -*-

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required


class BaseDocumentForm(Form):
    title = TextField(_('Title'),
                      description=_(u'Title'),
                      validators=[Required()])
    content = TextAreaField(_('Content'),
                            description=_(u'Content'),
                            validators=[Required()])


class SearchForm(Form):
    query = TextField(_('Search'),
                      description=_(u'Search'), validators=[Required()])
