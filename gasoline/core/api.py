# -*- coding: utf-8 -*-

import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from flask import current_app, request, Response, abort
from flask import json as flask_json
from flask.ext.babel import gettext as _
from mongoengine import EmbeddedDocument
from mongoengine.base.datastructures import BaseDict

from bson.objectid import ObjectId
import datetime
import mongoengine
from types import ModuleType

logger = logging.getLogger('gasoline')

json_schema_error = {
    'title': 'Error Schema',
    'type': 'object',
    'required': ['status', 'message'],
    'properties': {
        'status': {'type': 'integer'},
        'code': {'type': 'integer'},
        'message': {'type': 'string'},
    },
}


def api_error_handler(code, error):
    """error handler for API with json response"""
    resp = {
        'status': error.code,
        'code': error.response if error.response is not None else 0,
        'message': error.description,
    }

    return Response(response=rest_jsonify(resp),
                    mimetype='application/json', status=code)


def get_json(schema=None):
    """get json from request"""
    try:
        json = request.get_json()
        if json is None:
            raise
    except:
        abort(400, _('Require JSON encoded data.'))

    return json


def validate_input(json, schema):
    """valide json with schema"""
    title = schema
    if 'title' in schema:
        title = schema['title']
    try:
        validate(json, schema)
        logger.debug('json validation: match "{}"'.format(title))
    except ValidationError as e:
        logger.debug(
            ('json validation: don\'t match "{}" for value "{}" '
             'with error "{}"').format(title, json, e.message))
        abort(400, _('JSON validation error: {}.'.format(e.message)))


def sanitize_input(json, cls, json_schema_resource):
    """sanitize json with class definition"""
    json = dict(("%s" % key, value) for key, value in json.iteritems())
    logger.debug('json before sanitization with {}: {}'.format(cls, json))
    logger.debug('json schema: {}'.format(json_schema_resource['properties']))
    data = {}

    fields = cls._fields
    for field_name, field in fields.iteritems():
        # use mongodb field name if not _id
        if field.db_field != '_id':
            field_name = field.db_field
        # if field in schema and json, add value to sanatized output
        if (field_name in json_schema_resource['properties']
                and field_name in json):
            value = json[field_name]
            try:
                data[field_name] = (value if value is None
                                    else field.to_python(value))
                # print 'field {}, data: {}, orig value: {}'.\
                #     format(field, data[field_name], value)
            except (AttributeError, ValueError), e:
                logger.debug('invalid json input {}'.format(e))
                abort(400, _('Invalid JSON format.'))
            del json[field_name]

    if len(json) > 0:
        for value in json:
            logger.debug('found incorrect field: {}'.format(value))

    logger.debug('json after sanitization with {}: {}'.format(cls, data))
    return data


def encode_model(obj, recursive=False):
    if obj is None:
        return obj
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = encode_model(to_json(obj))
    elif isinstance(obj, mongoengine.queryset.QuerySet):
        out = encode_model(list(obj))
    elif isinstance(obj, ModuleType):
        out = None
    # elif isinstance(obj, groupby):
    #     out = [(g, list(l)) for g, l in obj]
    elif isinstance(obj, (list)):
        out = [encode_model(item) for item in obj]
    elif isinstance(obj, (dict)):
        out = dict([(k, encode_model(v)) for (k, v) in obj.items()])
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        out = str(obj)
    elif isinstance(obj, ObjectId):
        out = str(obj)
    elif isinstance(obj, (str, unicode)):
        out = obj
    elif isinstance(obj, float) or isinstance(obj, int):
        out = str(obj)
    else:
        raise (TypeError,
               "Could not JSON-encode type '%s': %s" % (type(obj), str(obj)))
    return out


def to_json(json_schema, recursive=False, **kwargs):
    """return obj in json with specified schema"""
    # print 'schema: {}'.format(repr(json_schema))
    # print 'kwargs: {}'.format(repr(kwargs))

    # if isinstance(obj, mongoengine.Document):
    #     print "mongoengine.Document !!!"
    # if isinstance(obj, mongoengine.queryset.base.BaseQuerySet):
    #     print "mongoengine.BaseQuerySet !!!"

    data = {}

    def parse_attr(obj=None, key=None, attr=None, schema=None):
        # print 'parse_attr_before - obj: {}, key: {}, attr: {}, schema: {}'.\
        #     format(repr(obj), key, repr(attr), schema)
        # get attribute from obj if no attr
        if attr is None:
            if obj is None or key is None:
                raise BaseException

            if type(obj) in (dict, BaseDict):
                attr = obj[key]
            else:
                attr = getattr(obj, key)
        # print 'parse_attr - obj: {}, key: {}, attr: {}, schema: {}'.\
        #     format(repr(obj), key, repr(attr), schema)

        # if schema has a type, get value
        if 'type' in schema:
            if schema['type'] == 'array':
                array = []
                try:
                    for item in attr:
                        if (hasattr(attr, '_instance')
                                and isinstance(item, EmbeddedDocument)):
                            item._instance = getattr(attr, '_instance')

                        if 'type' not in schema['items']:
                            array.append(
                                parse_attr(attr=item, schema=schema['items']))
                        else:
                            array.append(
                                to_json(schema['items'], True,
                                        **{schema['items']['type']: item}))
                except:
                    logger.exception('')
                    print repr(attr)
                attr = array
            elif schema['type'] == 'object':
                attr = to_json(schema, True, **{'object': attr})
            elif schema['type'] == 'string':
                attr = unicode(attr)
            elif schema['type'] == 'integer':
                pass
        # if schema has a anyOf keyword, use first schema
        elif 'anyOf' in schema:
            # print 'ANYOF with attr {}'.format(repr(attr))
            attr = parse_attr(attr=attr, schema=schema['anyOf'][0])
        else:
            pass
            print 'ERROR: no properties {}'.format(schema)

        # print 'attr {}, value: {}'.format(key, attr)
        return attr

    if 'object' in kwargs:
        obj = kwargs['object']
    else:
        obj = kwargs

    if 'properties' in json_schema:
        # print "properties!!! json_schema: {}, obj: {}".\
        #     format(json_schema, obj)
        for key, value in json_schema['properties'].iteritems():
            if key == '_id':
                key = 'id'

            # print 'properties - item: {}'.format(value)
            data[key] = parse_attr(obj=obj, key=key, schema=value)

    elif 'additionalProperties' in json_schema:
        # print "additionalProperties!!! json_schema: {}, obj: {}".\
        #     format(json_schema, obj)
        for key, value in obj.iteritems():
            # print 'item key: {}, value: {}'.format(key, repr(value))
            data[key] = parse_attr(obj=obj, key=key,
                                   schema=json_schema['additionalProperties'])

    else:
        # print "NON properties!!! json_schema: {}, obj: {}".\
        #     format(json_schema, obj)
        data = parse_attr(obj=obj, key=json_schema['type'], schema=json_schema)

    # print 'validate data: {} with schema {}'.format(data, json_schema)

    # print data
    validate_input(data, json_schema)

    if recursive is False:
        indent = None
        if (current_app.config['JSONIFY_PRETTYPRINT_REGULAR']
                and not request.is_xhr):
            indent = 2
        data = flask_json.dumps(data, indent=indent)

    return data


def from_json(json, cls, json_schema_resource, base_document=None):
    """create object of type cls with json"""
    # validate json
    validate_input(json, json_schema_resource)

    # sanitize json
    json = sanitize_input(json, cls, json_schema_resource)

    if EmbeddedDocument not in cls.__bases__:
        # check if already exists
        if cls.objects(**json).first() is not None:
            logger.debug(
                '{} creation failed: already exists'.format(cls._class_name))
            abort(422, _('{} already exists.'.format(cls._class_name)))

    obj = cls(**json)
    # print 'obj dict: {}'.format(obj.__dict__)

    if EmbeddedDocument not in cls.__bases__:
        # create object
        try:
            obj.save()
        except:
            logger.exception('')
            logger.debug(
                '{} creation failed: database error'.format(cls._class_name))
            abort(
                422, _('{} creation: database error.'.format(cls._class_name)))

    return obj


def update_from_json(json, obj, json_schema_resource):
    """update object with json"""
    # validate json
    validate_input(json, json_schema_resource)

    cls = type(obj)

    # sanitize json
    json = sanitize_input(json, cls, json_schema_resource)

    # update object
    for key, value in json.iteritems():
        setattr(obj, key, value)

    if not isinstance(obj, EmbeddedDocument):
        # save space
        try:
            obj.save()
        except:
            logger.exception('')
            logger.debug(
                '{} update failed: database error'.format(cls._class_name))
            abort(422, _('{} update: database error.'.format(cls._class_name)))

    # return updated object
    return obj


def rest_jsonify(*args, **kwargs):
    indent = None
    if (current_app.config['JSONIFY_PRETTYPRINT_REGULAR']
            and not request.is_xhr):
        indent = 2
    data = flask_json.dumps(dict(*args, **kwargs), indent=indent,
                            default=encode_model)

    return data


def restify():
    pass
