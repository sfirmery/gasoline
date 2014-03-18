# -*- coding: utf-8 -*-

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

__all__ = ['BaseDocumentForm']


class BaseDocumentForm(Form):
    title = TextField(_('Title'),
                      description=_(u'Title'),
                      validators=[Required()])
    content = TextAreaField(_('Content'),
                            description=_(u'Content'),
                            validators=[Required()])
