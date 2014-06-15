# -*- coding: utf-8 -*-

from werkzeug import generate_password_hash, check_password_hash
from flask import url_for

from gasoline.core.extensions import db

rest_uri_collection = '/api/v1/users'
rest_uri_resource = '{}/<name>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'User resource Schema',
    'anyOf': [
        {
            'type': 'object',
            'required': ['name'],
            'properties': {
                'name': {'type': 'string'},
                'display_name': {'type': 'string'},
                'uri': {'type': 'string'},
            },
        },
        {'type': 'string'}
    ]
}

json_schema_collection = {
    'title': 'Documents collection Schema',
    'type': 'object',
    'required': ['users'],
    'properties': {
        'users': {
            'type': 'array',
            'minItems': 1,
            'items': json_schema_resource,
        },
    },
}


class User(db.Document):
    name = db.StringField(primary_key=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.name)

    @property
    def uri(self):
        return rest_uri_resource.\
            replace("<name>", self.name)

    @property
    def display_name(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % (self.name)
