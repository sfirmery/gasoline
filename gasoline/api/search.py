# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, Response, abort, request
from flask import current_app
from flask.views import MethodView
# from flask.ext.login import login_required, current_user

from gasoline.core.api import to_json
from gasoline.services import acl_service as acl

# from gasoline.services.indexer.model import SearchResults
from gasoline.services.indexer.model import (
    json_schema_collection, rest_uri_collection)

blueprint_api_search = Blueprint('api.search', __name__)
route = blueprint_api_search.route

logger = logging.getLogger('gasoline')


class SearchAPI(MethodView):
    # decorators = [login_required]

    @acl.acl('read')
    def get(self):
        if 'q' not in request.args:
            abort(400, 'need a query: "q"')

        query = request.args.get('q', '')

        results = current_app.services['indexer'].search(query)

        from time import sleep
        sleep(1)

        resp = to_json(json_schema_collection, object=results)
        return Response(response=resp, status=200,
                        mimetype='application/json')

search_view = SearchAPI.as_view('search')
blueprint_api_search.\
    add_url_rule(rest_uri_collection,
                 view_func=search_view,
                 methods=['GET'])
