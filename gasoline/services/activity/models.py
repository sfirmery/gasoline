# -*- coding: utf-8 -*-
"""
Based on:
Activity Stream Specs: http://activitystrea.ms/specs/json/1.0/
"""


from datetime import datetime

from gasoline.core.extensions import db
from flask.ext.babel import gettext as _, lazy_gettext as _l

ACTIONS = {
    'create': {
        'page': _l('create page'),
        'event': _l('create event'),
        'issue': _l('create issue'),
        'task': _l('create task'),
    },
    'update': {
        'page': _l('update page'),
        'file': _l('update file'),
    },
    'remove': {
        'page': _l('remove page'),
    },
    'delete': {
        'file': _l('delete file'),
    },
    'attach': {
        'file': _l('attach file'),
    },
    'add': {
        'comment': _l('comment'),
    },
    'share': {
        'bookmark': _l('share bookmark'),
    },
}

ICONS_MAP = {
    'page': 'fa-file-text-o',
    'comment': 'fa-comments',
    'file': 'fa-paperclip',
    'bookmark': 'fa-bookmark-o',
    'event': 'fa-calender',
    'issue': 'fa-bug',
    'task': 'fa-tasks',
}


class DocumentObject(db.EmbeddedDocument):
    object_type = db.StringField(default='page')
    id = db.StringField()
    display_name = db.StringField()
    url = db.StringField()

    def __repr__(self):
        return '<DocumentObject %s>' % self.display_name


class Activity(db.Document):
    actor = db.ReferenceField('User')
    published = db.DateTimeField(default=datetime.utcnow)
    verb = db.StringField()
    object = db.EmbeddedDocumentField(DocumentObject)
    target = db.StringField()

    @property
    def action(self):
        try:
            action = ACTIONS.get(self.verb).get(self.object.object_type)
        except:
            action = _('$(verb)s on', self.verb)
        return action

    @property
    def icon(self):
        return 'fa ' + ICONS_MAP.get(self.object.object_type) + ' fa-lg'

    def __repr__(self):
        return '<Activity published=%r, verb=%s object=%s>' % (
            self.published, self.verb, self.object)
