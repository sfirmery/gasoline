# -*- coding: utf-8 -*-

from flask import Blueprint, flash, abort, redirect, session
from flask import url_for, request, Response
from flask.views import MethodView
from flask.ext.babel import gettext as _, ngettext as _n
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required

from gasoline.core.api import rest_jsonify
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

    def get(self, name):
        if name is None:
            users = User.objects().all()
            resp = to_json(json_schema_collection, array=users)
        else:
            user = User.objects(name=name).first()
            if user is None:
                abort(404, 'Unknown user')
            resp = to_json(json_schema_resource, object=user)

        return Response(response=resp, status=200,
                        mimetype='application/json')

users_view = UsersAPI.as_view('users')
blueprint_api_users.\
    add_url_rule(rest_uri_collection, defaults={'name': None},
                 view_func=users_view, methods=['GET'])
blueprint_api_users.\
    add_url_rule(rest_uri_collection,
                 view_func=users_view, methods=['POST'])
blueprint_api_users.\
    add_url_rule(rest_uri_resource,
                 view_func=users_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
