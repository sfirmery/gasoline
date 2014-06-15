# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort
from flask import request, Response
from flask.views import MethodView
# from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    rest_jsonify, get_json, to_json, from_json, update_from_json)
from gasoline.services import acl_service as acl
from gasoline.models import BaseDocument
from gasoline.models.document import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

# from gasoline.services.activity import Activity

blueprint_api_documents = Blueprint('api.documents', __name__)
route = blueprint_api_documents.route

logger = logging.getLogger('gasoline')


class DocumentsAPI(MethodView):
    # decorators = [login_required]

    @acl.acl('read')
    def get(self, space, doc_id):
        if doc_id is not None:
            doc = BaseDocument.objects(space=space, id=doc_id).first()
            # print doc.comments[0]
            # print doc.comments[1]

            resp = to_json(json_schema_collection, documents=[doc])
        else:
            if request.args.get('full') is not None:
                docs = BaseDocument.objects(space=space).limit(10)
            else:
                docs = BaseDocument.objects(space=space).\
                    only('space', 'title', 'creation', 'last_update',
                         'author', 'last_author', 'current_revision', 'tags').\
                    limit(10)
            resp = to_json(json_schema_collection, documents=docs)

        return Response(response=resp, status=200,
                        mimetype='application/json')

    def post(self, space):
        # get json from request
        json = get_json()

        # reject request for adding more than one document
        if len(json['documents']) > 1:
            logger.debug('document creation failed: too many documents')
            abort(400, _('Too many document objects.'))

        # check if document already exists
        if BaseDocument.objects(name=json['documents'][0]['title']).\
                first() is not None:
            logger.debug('document creation failed: already exists')
            abort(422, _('Document already exists.'))

        # create document
        document = from_json(json['documents'][0], BaseDocument,
                             json_schema_resource)

        try:
            document.save()
        except:
            logger.exception('')
            logger.debug('document creation failed: database error')
            abort(422, _('Error while creating document.'))

        return Response(response=rest_jsonify(documents=[document]),
                        status=201, mimetype='application/json',
                        headers={'location': document.uri})

    def put(self, space, doc_id):
        # get document
        try:
            doc = BaseDocument.objects(id=doc_id).first()
            # check if document exists
            if doc is None:
                raise
        except:
            logger.debug('document update failed: document not found')
            abort(404, _('Document not found.'))

        # get json from request
        json = get_json()

        print doc.__dict__
        # update document
        doc = update_from_json(json, doc, json_schema_resource)

        try:
            print doc.__dict__
            doc.save()
        except:
            logger.exception('')
            logger.debug('document update failed: database error')
            abort(422, _('Error while updating document.'))

        return Response(response=rest_jsonify(documents=[doc]), status=200,
                        mimetype='application/json')

    patch = put

    def delete(self, space, doc_id):
        # get document
        try:
            doc = BaseDocument.objects(id=doc_id).first()
            # check if document exists
            if doc is None:
                raise
        except:
            logger.debug('document update failed: document not found')
            abort(404, _('Document not found.'))

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
