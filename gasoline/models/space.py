# -*- coding: utf-8 -*-

from mongoengine import queryset_manager, Q
from gasoline.core.extensions import db
from gasoline.services.acl import ACE

rest_uri_collection = '/api/v1/spaces'
rest_uri_resource = '{}/<space>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Space resource Schema',
    'type': 'object',
    'required': ['name'],
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Spaces collection Schema',
    'type': 'object',
    'required': ['spaces'],
    'properties': {
        'spaces': {
            'type': 'array',
            'minItems': 1,
            'items': json_schema_resource,
        },
    },
}

DEFAULT_ACE = ACE(
    truth='ALLOW', predicate='ANY', permission=['read', 'write'])


class Space(db.Document):
    name = db.StringField(primary_key=True)
    description = db.StringField(default='')
    acl = db.ListField(db.EmbeddedDocumentField(ACE), default=[DEFAULT_ACE])

    @property
    def uri(self):
        return rest_uri_resource.\
            replace("<space>", self.name)

    def __repr__(self):
        return '<Space name=%s>' % (self.name)
