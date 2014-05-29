# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, redirect, abort
from flask import flash, url_for, request, Response
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from gasoline.core.api import rest_jsonify
from gasoline.services import acl_service as acl
from gasoline.forms import BaseDocumentForm, CommentForm
from gasoline.models import BaseDocument, DocumentHistory, Comment
from gasoline.services.activity import Activity

blueprint_api_document = Blueprint('api.document',
                                   __name__,
                                   url_prefix='/api/v1/<space>')
route = blueprint_api_document.route

logger = logging.getLogger('gasoline')


class DocumentsListAPI(MethodView):
    decorators = [login_required]

    def get(self, space='main'):
        docs = BaseDocument.objects(space=space).\
            only('space', 'title', 'creation', 'last_update',
                 'author', 'last_author', 'current_revision', 'tags').\
            limit(1)

        return Response(response=rest_jsonify(documents_list=docs), status=200,
                        mimetype='application/json')


class DocumentAPI(MethodView):
    decorators = [login_required]

    def get(self, space='main'):
        pass


documents_list_view = DocumentsListAPI.as_view('documents_list_api')
blueprint_api_document.\
    add_url_rule('/documents_list', view_func=documents_list_view,
                 methods=['GET'])

document_view = DocumentAPI.as_view('document_api')
blueprint_api_document.\
    add_url_rule('/document', view_func=document_view,
                 methods=['GET'])
blueprint_api_document.\
    add_url_rule('/document', view_func=document_view,
                 methods=['POST'])
blueprint_api_document.\
    add_url_rule('/document/<int:doc_id>', view_func=document_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])

