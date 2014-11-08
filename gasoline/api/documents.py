# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort
from flask import request, Response
from flask.views import MethodView
from flask.ext.login import login_required
from flask.ext.babel import gettext as _

from gasoline.core.api import (get_json, to_json, from_json, update_from_json)
from gasoline.services import acl_service as acl
from gasoline.models import BaseDocument, Space
from gasoline.models.document import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

# from gasoline.services.activity import Activity

blueprint_api_documents = Blueprint('api.documents', __name__)
route = blueprint_api_documents.route

logger = logging.getLogger('gasoline')


class DocumentsAPIMixin(object):

    def get_document(self, doc_id, right, filter=None):
        """Get document and apply acl"""
        try:
            if filter is not None:
                doc = BaseDocument.objects(id=doc_id)\
                    .filter(**filter).first()
            else:
                doc = BaseDocument.objects(id=doc_id).first()
        except:
            doc = None
        if doc is not None:
            # check acl for space
            space = Space.objects(name=doc.space).first()
            acl.apply(right, space.acl, _('space'))
        else:
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
            document = self.get_document(doc_id, 'read')
            resp = to_json(json_schema_resource, object=document)
        else:
            query = {'space': space}
            if request.args.get('details') == 'true':
                docs = BaseDocument.objects(**query).limit(10)
            else:
                docs = BaseDocument.objects(**query).\
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

        # check acl for space
        if 'space' in json:
            space = Space.objects(name=json['space']).first()
            acl.apply('write', space.acl, _('space'))
        else:
            abort(400, _('Invalid JSON format.'))

        # create document
        document = from_json(json, BaseDocument, json_schema_resource)

        resp = to_json(json_schema_resource, object=document)
        return Response(response=resp, status=201, mimetype='application/json',
                        headers={'location': document.uri})

    @acl.acl('write')
    def put(self, space, doc_id):
        # get document
        doc = self.get_document(doc_id, 'write')

        # get json from request
        json = get_json()

        # update document
        document = update_from_json(json, doc, json_schema_resource)

        resp = to_json(json_schema_resource, object=document)
        return Response(response=resp, status=200, mimetype='application/json')

    patch = put

    @acl.acl('write')
    def delete(self, space, doc_id):
        # get document
        doc = self.get_document(doc_id, 'write')

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
