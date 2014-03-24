# -*- coding: utf-8 -*-

from gasoline.core.extensions import db
from flask.ext.babel import lazy_gettext as _l

ACTIONS = {
    'edit': _l('edit'),
    'new': _l('new'),
    'delete': _l('delete'),
}

ICON = {
    'edit': 'fa fa-edit',
    'new': 'fa fa-plus',
    'delete': 'fa fa-trash-o',
}


class Activity(db.Document):
    date = db.DateTimeField()
    action = db.StringField()
    user = db.ReferenceField('User')
    document = db.ReferenceField('BaseDocument')

    @property
    def action_localized(self):
        return ACTIONS.get(self.action, self.action)

    @property
    def icon(self):
        return ICON.get(self.action, 'fa fa-square-o')

    def __repr__(self):
        return '<Activity date=%r, action=%s document=%s>' % (
            self.date, self.action, self.document)
