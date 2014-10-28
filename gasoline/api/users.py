# -*- coding: utf-8 -*-

from flask import Blueprint, flash, abort, redirect, session
from flask import url_for, request, Response
from flask.views import MethodView
from flask.ext.babel import gettext as _, ngettext as _n
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required

from gasoline.core.api import get_json
from gasoline.core.api import (
    to_json, from_json, update_from_json)
from gasoline.models import User
from gasoline.models.user import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

blueprint_api_users = Blueprint('api.users', __name__)
route = blueprint_api_users.route


class UsersAPI(MethodView):
    # decorators = [login_required]

    def get(self, uid):
        if uid is None:
            users = User.objects().all()
            resp = to_json(json_schema_collection, array=users)
        else:
            user = User.objects(id=uid).first()
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
        user = User.objects(id=uid).first()
        if user is None:
            abort(404, 'Unknown user')

        # get json from request
        json = get_json()

        import time
        time.sleep(10)

        # update document
        user = update_from_json(json, user, json_schema_resource)

        resp = to_json(json_schema_resource, object=user)
        return Response(response=resp, status=200, mimetype='application/json')


users_view = UsersAPI.as_view('users')
blueprint_api_users.\
    add_url_rule(rest_uri_collection, defaults={'uid': None},
                 view_func=users_view, methods=['GET'])
blueprint_api_users.\
    add_url_rule(rest_uri_collection,
                 view_func=users_view, methods=['POST'])
blueprint_api_users.\
    add_url_rule(rest_uri_resource,
                 view_func=users_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
