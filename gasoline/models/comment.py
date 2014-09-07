# -*- coding: utf-8 -*-

from datetime import datetime
import markdown2

from gasoline.core.extensions import db
from gasoline.core.signals import event, activity
from .user import User, json_schema_resource as json_schema_user

rest_uri_collection = '/api/v1/<space>/documents/<doc_id>/comments'
rest_uri_resource = '{}/<comment_id>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Comment resource Schema',
    'type': 'object',
    'required': ['author', 'content'],
    'properties': {
        'id': {'type': 'string'},
        'author': json_schema_user,
        'date': {'type': 'string'},
        'content': {'type': 'string'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Comments collection Schema',
    'type': 'array',
    'minItems': 0,
    'items': json_schema_resource,
}


class Comment(db.EmbeddedDocument):
    id = db.StringField()
    author = db.ReferenceField(User)
    date = db.DateTimeField(default=datetime.utcnow)
    content = db.StringField()

    reply = db.SortedListField(
        db.EmbeddedDocumentField('Comment'),
        ordering='date')

    def __init__(self, **kwargs):
        # remove date field for new comment
        if '__auto_convert' not in kwargs and 'date' in kwargs:
            kwargs.pop('date')
        super(Comment, self).__init__(**kwargs)

    @property
    def uri(self):
        return rest_uri_resource.\
            replace('<space>', self._instance.space).\
            replace('<doc_id>', unicode(self._instance.id)).\
            replace('<comment_id>', self.id)

    def __repr__(self):
        return '<Comment author=%s>' % self.author
