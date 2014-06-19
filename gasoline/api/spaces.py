# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, Response
from flask.views import MethodView
# from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    get_json, to_json, from_json, update_from_json)
# from gasoline.services import acl_service as acl
from gasoline.models import Space
from gasoline.models.space import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

blueprint_api_spaces = Blueprint('api.spaces', __name__)
route = blueprint_api_spaces.route

logger = logging.getLogger('gasoline')


class SpacesAPI(MethodView):
    # decorators = [login_required]

    # @acl.acl('read')
    def get(self, name):
        if name is None:
            spaces = Space.objects().all()
            resp = to_json(json_schema_collection, spaces=spaces)
        else:
            space = Space.objects(name=name).first()
            if space is None:
                abort(404, 'Space not found')
            resp = to_json(json_schema_collection, spaces=[space])
        return Response(response=resp, status=200,
                        mimetype='application/json')

    def post(self):
        # get json from request
        json = get_json()

        # create space from json
        space = from_json(json, Space,
                          json_schema_resource)

        # create space
        resp = to_json(json_schema_collection, spaces=[space])
        return Response(response=resp, status=201,
                        mimetype='application/json',
                        headers={'location': space.uri})

    def put(self, name):
        # get space
        space = Space.objects(name=name).first()

        # check if space exists
        if space is None:
            logger.debug('space update failed: space not found')
            abort(404, _('Space not found.'))

        # get json from request
        json = get_json()

        if 'name' in json and json['name'] != name:
            abort(422, _('Update space name denied.'))

        # update space
        update_from_json(json, space, json_schema_resource)

        resp = to_json(json_schema_collection, spaces=[space])
        return Response(response=resp, status=200,
                        mimetype='application/json')

    patch = put

    def delete(self, name):
        # get space
        space = Space.objects(name=name).first()

        # check if space exists
        if space is None:
            logger.debug('space update failed: space not found')
            abort(404, _('Space not found.'))

        # delete space
        try:
            space.delete()
        except:
            logger.debug('space delete failed: database error')
            abort(422, _('Error while deleting space.'))

        return Response(status=204, mimetype='application/json')

spaces_view = SpacesAPI.as_view('spaces')
blueprint_api_spaces.\
    add_url_rule(rest_uri_collection, defaults={'name': None},
                 view_func=spaces_view,
                 methods=['GET'])
blueprint_api_spaces.\
    add_url_rule(rest_uri_collection,
                 view_func=spaces_view,
                 methods=['POST'])
blueprint_api_spaces.\
    add_url_rule(rest_uri_resource,
                 view_func=spaces_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
