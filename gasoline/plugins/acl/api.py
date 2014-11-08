# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, Response
from flask.views import MethodView
from flask.ext.babel import gettext as _

from gasoline.core.api import get_json, to_json, from_json
from gasoline.services import acl_service as acl

from gasoline.services.acl.models import ACE
from gasoline.services.acl.models import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

from gasoline.api.documents import DocumentsAPIMixin

blueprint_api_plugin_acl = Blueprint('api.acl', __name__)
route = blueprint_api_plugin_acl.route

logger = logging.getLogger('gasoline')


class AclAPI(MethodView, DocumentsAPIMixin):

    def get_acl(self, doc, predicate):
        """Get document and apply acl"""
        try:
            return doc.get_acl(predicate)
        except:
            abort(404, _('ACE not found.'))

    @acl.acl('read')
    def get(self, space, doc_id, predicate):
        # get document
        doc = self.get_document(doc_id, 'read')

        acl = self.get_acl(doc, predicate)
        resp = to_json(json_schema_collection, array=acl)

        return Response(response=resp, status=200,
                        mimetype='application/json')

    @acl.acl('write')
    def post(self, space, doc_id):
        # get document
        doc = self.get_document(doc_id, 'write')

        # get json from request
        json = get_json()

        # create ace from json
        ace = from_json(json, ACE, json_schema_resource, save=False)

        # add ace to document
        try:
            doc.add_ace(ace)
        except:
            abort(422, _('Error while adding ace.'))

        resp = to_json(json_schema_resource, object=ace)
        return Response(response=resp, status=201,
                        mimetype='application/json')

    @acl.acl('write')
    def put(self, space, doc_id, predicate):
        # get document
        doc = self.get_document(doc_id, 'write')

        # get json from request
        json = get_json()

        # create ace from json
        ace = from_json(json, ACE, json_schema_resource, save=False)

        # check ace predicate
        if predicate != ace.predicate:
            abort(422, _('Wrong predicate in json content.'))

        # update ace on document
        try:
            doc.update_ace(ace)
        except:
            logger.exception('')
            logger.debug('ace update failed: database error')
            abort(422, _('Error while updating ace.'))

        resp = to_json(json_schema_resource, object=ace)
        return Response(response=resp, status=200,
                        mimetype='application/json')

    patch = put

    @acl.acl('write')
    def delete(self, space, doc_id, predicate):
        # get document
        doc = self.get_document(doc_id, 'write')

        # check if ace exists
        ace = self.get_acl(doc, predicate)

        # delete ace
        try:
            doc.delete_ace(ace[0])
        except:
            logger.exception('')
            logger.debug('ace delete failed: database error')
            abort(422, _('Error while deleting ace.'))

        return Response(status=204, mimetype='application/json')

acl_view = AclAPI.as_view('acl')
blueprint_api_plugin_acl.\
    add_url_rule(rest_uri_collection,
                 defaults={'predicate': None},
                 view_func=acl_view,
                 methods=['GET'])
blueprint_api_plugin_acl.\
    add_url_rule(rest_uri_collection,
                 view_func=acl_view,
                 methods=['POST'])
blueprint_api_plugin_acl.\
    add_url_rule(rest_uri_resource,
                 view_func=acl_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
