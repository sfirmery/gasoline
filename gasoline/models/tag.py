# -*- coding: utf-8 -*-

rest_uri_collection = '/api/v1/documents/<space>/<doc_id>/tags'
rest_uri_resource = '{}/<tag_id>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Tag resource Schema',
    'type': 'object',
    'required': ['tag'],
    'properties': {
        'tag': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Tags collection Schema',
    'type': 'array',
    'minItems': 0,
    'items': json_schema_resource,
}
