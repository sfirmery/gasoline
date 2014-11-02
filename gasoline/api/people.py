# -*- coding: utf-8 -*-

from flask import Blueprint, abort, Response
from flask.views import MethodView
from flask.ext.babel import gettext as _, ngettext as _n
from flask.ext.login import current_user, login_required

from gasoline.core.api import get_json
from gasoline.core.api import (
    to_json, from_json, update_from_json)
from gasoline.models import User
from gasoline.models.user import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

blueprint_api_people = Blueprint('api.people', __name__)
route = blueprint_api_people.route


class PeopleAPI(MethodView):
    # decorators = [login_required]

    def get(self, uid):
        if uid is None:
            people = User.objects().all()
            resp = to_json(json_schema_collection, array=people)
        else:
            user = User.objects(name=uid).first()
            if user is None:
                abort(404, 'Unknown user')
            resp = to_json(json_schema_resource, object=user)

        return Response(response=resp, status=200,
                        mimetype='application/json')

    def post(self):
        # get json from request
        json = get_json()

        # create document
        user = from_json(json, User, json_schema_resource)

        resp = to_json(json_schema_resource, object=user)
        return Response(response=resp, status=201, mimetype='application/json',
                        headers={'location': user.uri})

    def put(self, uid):
        # get user
        user = User.objects(name=uid).first()
        if user is None:
            abort(404, 'Unknown user')

        # get json from request
        json = get_json()

        # update user
        user = update_from_json(json, user, json_schema_resource)

        resp = to_json(json_schema_resource, object=user)
        return Response(response=resp, status=200, mimetype='application/json')

    patch = put

    def delete(self, uid):
        # get user
        user = User.objects(name=uid).first()
        if user is None:
            abort(404, 'Unknown user')

        # delete space
        try:
            user.delete()
        except:
            abort(422, _('Error while deleting user.'))

        return Response(status=204, mimetype='application/json')

people_view = PeopleAPI.as_view('people')
blueprint_api_people.\
    add_url_rule(rest_uri_collection, defaults={'uid': None},
                 view_func=people_view, methods=['GET'])
blueprint_api_people.\
    add_url_rule(rest_uri_collection,
                 view_func=people_view, methods=['POST'])
blueprint_api_people.\
    add_url_rule(rest_uri_resource,
                 view_func=people_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
