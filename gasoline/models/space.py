# -*- coding: utf-8 -*-

from gasoline.core.extensions import db
from gasoline.services.acl import ACE

rest_uri_collection = '/api/v1/spaces'
rest_uri_resource = '{}/<space>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Space resource Schema',
    'type': 'object',
    'required': ['name'],
    'properties': {
        '_id': {'type': 'string'},
        'name': {'type': 'string'},
        'display_name': {'type': 'string'},
        'description': {'type': 'string'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Spaces collection Schema',
    'required': ['spaces'],
    'type': 'array',
    'minItems': 1,
    'items': json_schema_resource,
}

DEFAULT_ACE = ACE(predicate='ANY',
                  permission={'read': 'ALLOW', 'write': 'ALLOW'})


class Space(db.Document):
    name = db.StringField(primary_key=True)
    display_name = db.StringField()
    description = db.StringField(default='')
    acl = db.ListField(db.EmbeddedDocumentField(ACE), default=[DEFAULT_ACE])

    @property
    def uri(self):
        return rest_uri_resource.\
            replace("<space>", self.name)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.name

        return super(Space, self).save(*args, **kwargs)

    def __repr__(self):
        return '<Space name=%s>' % (self.name)
