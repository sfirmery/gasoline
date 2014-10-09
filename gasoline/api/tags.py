# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, Response, request
from flask.views import MethodView
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    get_json, to_json, from_json, update_from_json, validate_input)
from gasoline.services import acl_service as acl
from gasoline.models.tag import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)
from gasoline.api.documents import DocumentsAPIMixin

blueprint_api_tags = Blueprint('api.tags', __name__)
route = blueprint_api_tags.route

logger = logging.getLogger('gasoline')


class TagsAPI(MethodView, DocumentsAPIMixin):

    def get_tag(self, doc, tag_id):
        """Get tag"""
        try:
            return doc.get_tag(tag_id)
        except:
            abort(404, _('Tag not found.'))

    @acl.acl('write')
    def post(self, space, doc_id):
        # get document
        doc = self.get_document(doc_id, 'write')

        # get json from request
        json = get_json()

        # validate json
        validate_input(json, json_schema_resource)

        try:
            doc.add_tag(json.get('tag'))
        except:
            logger.exception('')
            abort(422, _('Tag already exists.'))

        resp = to_json(json_schema_resource, object=json)
        return Response(response=resp, status=201,
                        mimetype='application/json')

    @acl.acl('write')
    def put(self, space, doc_id, tag_id):
        # get document
        doc = self.get_document(doc_id, 'write')

        # get json from request
        json = get_json()

        # validate json
        validate_input(json, json_schema_resource)

        # check if tag exists
        if json.get('tag') == self.get_tag(doc, tag_id):
            abort(422, _('Tag not changed.'))

        # update tag
        try:
            doc.update_tag(tag_id, json.get('tag'))
        except:
            logger.exception('')
            logger.debug('tag delete failed: database error')
            abort(422, _('Error while updating tag.'))

        resp = to_json(json_schema_resource, object=json)
        return Response(response=resp, status=200,
                        mimetype='application/json')

    patch = put

    @acl.acl('write')
    def delete(self, space, doc_id, tag_id):
        # get document
        doc = self.get_document(doc_id, 'write')

        # check if tag exists
        self.get_tag(doc, tag_id)

        # delete tag
        try:
            doc.delete_tag(tag_id)
        except:
            logger.exception('')
            logger.debug('tag delete failed: database error')
            abort(422, _('Error while deleting tag.'))

        return Response(status=204, mimetype='application/json')

tags_view = TagsAPI.as_view('tags')
blueprint_api_tags.\
    add_url_rule(rest_uri_collection,
                 view_func=tags_view,
                 methods=['POST'])
blueprint_api_tags.\
    add_url_rule(rest_uri_resource,
                 view_func=tags_view,
                 methods=['PUT', 'PATCH', 'DELETE'])
