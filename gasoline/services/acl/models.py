# -*- coding: utf-8 -*-

from gasoline.core.extensions import db

rest_uri_collection = '/api/v1/documents/<space>/<doc_id>/acl'
rest_uri_resource = '{}/<predicate>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Document resource Schema',
    'type': 'object',
    'required': ['predicate', 'permissions'],
    'properties': {
        'id': {'type': 'string'},
        'predicate': {'type': 'string'},
        'permissions': {
            'type': 'object',
            'additionalProperties': True,
        },
    },
}

json_schema_collection = {
    'title': 'ACL Schema',
    'type': 'array',
    'minItems': 1,
    'items': json_schema_resource,
}

ORDER = {
    'read': 1,
    'write': 2,
}


class ACE(db.EmbeddedDocument):
    predicate = db.StringField()
    permissions = db.DictField()

    @property
    def id(self):
        return unicode(self.predicate)

    def __repr__(self):
        return '<ACE "%s %s">' % (self.predicate, self.permissions)
