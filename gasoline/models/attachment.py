# -*- coding: utf-8 -*-

from datetime import datetime
# from mongoengine.fields import GridFSProxy

from gasoline.core.extensions import db
from gasoline.core.utils import sizeof_fmt
# from gasoline.core.signals import event, activity
from .user import User, json_schema_resource as json_schema_user

rest_uri_collection = '/api/v1/<space>/documents/<doc_id>/attachments'
rest_uri_resource = '{}/<attachment_id>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Attachment resource Schema',
    'type': 'object',
    'required': ['author', 'filename'],
    'properties': {
        # '_id': {'type': 'string'},
        'date': {'type': 'string'},
        'author': json_schema_user,
        'comment': {'type': 'string'},
        'filename': {'type': 'string'},
        'size': {'type': 'string'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Attachments collection Schema',
    'type': 'object',
    'required': ['attachments'],
    'properties': {
        'attachments': {
            'type': 'array',
            'minItems': 1,
            'items': json_schema_resource,
        },
    },
}


class Attachment(db.EmbeddedDocument):
    filename = db.StringField(primary_key=True)
    attachment = db.FileField()

    _date = db.DateTimeField(db_field='date', default=datetime.utcnow)
    author = db.ReferenceField(User)
    comment = db.StringField()

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def uri(self):
        return rest_uri_resource.\
            replace("<space>", self._instance.space).\
            replace("<doc_id>", unicode(self._instance.id)).\
            replace("<attachment_id>", '1')

    @property
    def size(self):
        return sizeof_fmt(self.attachment.length)

    def __repr__(self):
        return '<Attachment filename=%r>' % self.filename
