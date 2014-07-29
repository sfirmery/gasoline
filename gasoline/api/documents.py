# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort
from flask import request, Response
from flask.views import MethodView
from flask.ext.login import login_required
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    get_json, to_json, from_json, update_from_json)
from gasoline.services import acl_service as acl
from gasoline.models import BaseDocument
from gasoline.models.document import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

# from gasoline.services.activity import Activity

blueprint_api_documents = Blueprint('api.documents', __name__)
route = blueprint_api_documents.route

logger = logging.getLogger('gasoline')


class DocumentsAPIMixin(object):

    def get_document(self, space, doc_id, right):
        """Get document and apply acl"""
        try:
            doc = BaseDocument.objects(id=doc_id, space=space).first()
        except:
            doc = None
        if doc is None:
            logger.info('document not found %r', doc_id)
            abort(404, _('document not found'))

        # check acl for document
        acl.apply(right, doc.acl, _('document'))
        return doc


class DocumentsAPI(MethodView, DocumentsAPIMixin):
    decorators = [login_required]

    @acl.acl('read')
    def get(self, space, doc_id):
        if doc_id is not None:
            doc = self.get_document(space, doc_id, 'read')
            resp = to_json(json_schema_collection, array=[doc])
        else:
            if request.args.get('full') is not None:
                docs = BaseDocument.objects(space=space).limit(10)
            else:
                docs = BaseDocument.objects(space=space).\
                    only('space', 'title', 'creation', 'last_update',
                         'author', 'last_author', 'current_revision', 'tags').\
                    limit(10)
            resp = to_json(json_schema_collection, array=docs)

        return Response(response=resp, status=200,
                        mimetype='application/json')

    @acl.acl('write')
    def post(self, space):
        # get json from request
        json = get_json()

        # create document
        document = from_json(json, BaseDocument, json_schema_resource)

        resp = to_json(json_schema_collection, array=[document])
        return Response(response=resp, status=201, mimetype='application/json',
                        headers={'location': document.uri})

    @acl.acl('write')
    def put(self, space, doc_id):
        # get document
        doc = self.get_document(space, doc_id, 'write')

        # get json from request
        json = get_json()

        # update document
        document = update_from_json(json, doc, json_schema_resource)

        resp = to_json(json_schema_collection, array=[document])
        return Response(response=resp, status=200, mimetype='application/json')

    patch = put

    @acl.acl('write')
    def delete(self, space, doc_id):
        # get document
        doc = self.get_document(space, doc_id, 'write')

        # delete document
        try:
            doc.delete()
        except:
            logger.debug('document delete failed: database error')
            abort(422, _('Error while deleting document.'))

        return Response(status=204, mimetype='application/json')

documents_view = DocumentsAPI.as_view('documents')
blueprint_api_documents.\
    add_url_rule(rest_uri_collection, defaults={'doc_id': None},
                 view_func=documents_view,
                 methods=['GET'])
blueprint_api_documents.\
    add_url_rule(rest_uri_collection,
                 view_func=documents_view,
                 methods=['POST'])
blueprint_api_documents.\
    add_url_rule(rest_uri_resource,
                 view_func=documents_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
