# -*- coding: utf-8 -*-

from gasoline.core.extensions import db

rest_uri_collection = '/api/v1/documents/<space>/<doc_id>/acl'
rest_uri_resource = '{}/<predicate>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Document resource Schema',
    'type': 'object',
    'required': ['predicate', 'truth', 'permission'],
    'properties': {
        'predicate': {'type': 'string'},
        'truth': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': 'true',
            },
        },
    },
}

json_schema_collection = {
    'title': 'ACL Schema',
    'type': 'array',
    'minItems': 1,
    'items': json_schema_resource,
}

TRUTH = ['DENY', 'ALLOW']


class ACE(db.EmbeddedDocument):
    # truth = db.StringField(unique_with=['predicate'],
    #                        choices=TRUTH, default=TRUTH[0])
    predicate = db.StringField()
    # permission = db.ListField(db.StringField())
    truth = db.DictField()

    def __repr__(self):
        return '<ACE "%s %s">' % (self.predicate, self.truth)
