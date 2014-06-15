# -*- coding: utf-8 -*-

from gasoline.core.extensions import db
from gasoline.services.acl import ACE

rest_uri_collection = '/api/v1/spaces'
rest_uri_resource = '{}/<name>'.format(rest_uri_collection)

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


class Space(db.Document):
    name = db.StringField(primary_key=True)
    description = db.StringField(default='')
    acl = db.ListField(db.EmbeddedDocumentField(ACE))

    @property
    def uri(self):
        return rest_uri_resource.\
            replace("<name>", self.name)

    # def update_from_rest(self, rest):
    #     if 'name' in rest and rest['name'] != self.name:
    #         # update id (delete and recreate document)
    #         self.delete()
    #         self.name = rest['name']
    #         self._created = True

    # def to_rest(self):
    #     """return space in rest friendly format"""
    #     rest = dict()
    #     rest['name'] = self.name
    #     rest['uri'] = self.uri
    #     return rest

    # @classmethod
    # def from_rest(cls, rest):
    #     """create instance from a JSON rest input"""
    #     data = dict(("%s" % key, value) for key, value in rest.iteritems())
    #     errors_dict = {}

    #     fields = cls._fields
    #     for field_name, field in fields.iteritems():
    #         if field.db_field in data:
    #             value = data[field.db_field]
    #             try:
    #                 data[field_name] = (value if value is None
    #                                     else field.to_python(value))
    #                 if field_name != field.db_field:
    #                     del data[field.db_field]
    #             except (AttributeError, ValueError), e:
    #                 errors_dict[field_name] = e

    #     if errors_dict:
    #         errors = "\n".join(["%s - %s" % (k, v)
    #                  for k, v in errors_dict.items()])
    #         msg = ("Invalid data to create a `%s` instance.\n%s"
    #                % (cls._class_name, errors))
    #         raise InvalidDocumentError(msg)

    #     obj = cls(**data)
    #     return obj

    # def update_from_rest(self, rest):
    #     if 'name' in rest and rest['name'] != self.name:
    #         # update id (delete and recreate document)
    #         self.delete()
    #         self.name = rest['name']
    #         self._created = True

    def __repr__(self):
        return '<Space name=%s>' % (self.name)
