# -*- coding: utf-8 -*-
"""
Based on:
Activity Stream Specs: http://activitystrea.ms/specs/json/1.0/
"""

from datetime import datetime

from gasoline.core.extensions import db
from flask.ext.babel import gettext as _, lazy_gettext as _l

from gasoline.models.user import json_schema_resource as json_schema_user

rest_uri_collection = '/api/v1/activity'
rest_uri_resource = '{}/<activity>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Activity resource Schema',
    'type': 'object',
    'required': ['actor', 'published', 'verb', 'object'],
    'properties': {
        'actor': json_schema_user,
        'published': {'type': 'string'},
        'verb': {'type': 'string'},
        'object': {
            'type': 'object',
            'properties': {
                'object_type': {'type': 'string'},
                'id': {'type': 'string'},
                'display_name': {'type': 'string'},
                'url': {'type': 'string'},
            },
        },
        'target': {'type': 'string'},
        'action': {'type': 'string'},
        'icon': {'type': 'string'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Activities collection Schema',
    'type': 'array',
    'minItems': 1,
    'items': json_schema_resource,
}

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
        'tag': _l('remove tag from'),
    },
    'delete': {
        'file': _l('delete file'),
    },
    'attach': {
        'file': _l('attach file'),
    },
    'add': {
        'comment': _l('comment'),
        'tag': _l('add tag on'),
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
    'tag': 'fa-tag',
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
    def uri(self):
        return rest_uri_resource.\
            replace("<activity>", unicode(self.id))

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
