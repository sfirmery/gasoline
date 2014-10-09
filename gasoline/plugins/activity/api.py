# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, Response
from flask.views import MethodView

from gasoline.core.api import to_json
from gasoline.services import acl_service as acl
from gasoline.services.activity.models import Activity
from gasoline.services.activity.models import (
    json_schema_collection, rest_uri_collection)

blueprint_api_plugin_activity = Blueprint('api.services.activity', __name__)
route = blueprint_api_plugin_activity.route

logger = logging.getLogger('gasoline')


class ActivityAPI(MethodView):

    @acl.acl('read')
    def get(self, space=None):
        if space is None:
            # get global activities
            activity = Activity.objects.order_by('-published').limit(50)
            resp = to_json(json_schema_collection, array=activity)
        else:
            # get space activities
            activity = Activity.objects.order_by('-published').limit(50)
            resp = to_json(json_schema_collection, array=activity)
        return Response(response=resp, status=200,
                        mimetype='application/json')

activity_view = ActivityAPI.as_view('activity')
blueprint_api_plugin_activity.\
    add_url_rule(rest_uri_collection, defaults={'space': None},
                 view_func=activity_view,
                 methods=['GET'])
