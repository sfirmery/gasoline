# -*- coding: utf-8 -*-

import logging

from flask import current_app, request
from flask import json
from bson.objectid import ObjectId
import datetime
import mongoengine
from types import ModuleType
from collections import Iterable

logger = logging.getLogger('gasoline')


def encode_model(obj, recursive=False):
    if obj is None:
        return obj
    if isinstance(obj, (mongoengine.Document, mongoengine.EmbeddedDocument)):
        out = dict()
        for field_name in obj:
            value = obj._data.get(field_name, None)
            field = obj._fields.get(field_name)
            if field is None and obj._dynamic:
                field = obj._dynamic_fields.get(field_name)

            if value is not None:
                if isinstance(value, Iterable) and len(value) == 0:
                    value = None
                else:
                    print "iterable not 0"
                    value = encode_model(value)

            # Handle self generating fields
            if value is None and field._auto_gen:
                value = field.generate()
                obj._data[field_name] = value

            if value is not None:
                out[field.db_field] = value

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
        raise TypeError, "Could not JSON-encode type '%s': %s" % (type(obj), str(obj))
    return out


def rest_jsonify(*args, **kwargs):
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] and not request.is_xhr:
        indent = 2
    data = json.dumps(dict(*args, **kwargs), indent=indent,
                      default=encode_model)

    return data
