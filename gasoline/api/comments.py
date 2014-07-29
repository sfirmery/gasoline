# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, Response
from flask.views import MethodView
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    get_json, to_json, from_json, update_from_json)
from gasoline.services import acl_service as acl
from gasoline.models import Comment
from gasoline.models.comment import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)
from gasoline.api.documents import DocumentsAPIMixin

blueprint_api_comments = Blueprint('api.comments', __name__)
route = blueprint_api_comments.route

logger = logging.getLogger('gasoline')


class CommentsAPI(MethodView, DocumentsAPIMixin):

    def get_comment(self, comments, comment_id):
        """Get document and apply acl"""
        try:
            return comments[comment_id]
        except:
            abort(404, _('Comment not found.'))

    @acl.acl('read')
    def get(self, space, doc_id, comment_id):
        # get document
        doc = self.get_document(space, doc_id, 'read')

        if comment_id is None:
            resp = to_json(json_schema_collection, comments=doc.comments)
        else:
            comment = self.get_comment(doc.comments, comment_id)
            resp = to_json(json_schema_collection,
                           comments={comment_id: comment})
        return Response(response=resp, status=200,
                        mimetype='application/json')

    @acl.acl('write')
    def post(self, space, doc_id):
        # get document
        doc = self.get_document(space, doc_id, 'write')

        # get json from request
        json = get_json()

        # create comment from json
        comment = from_json(json, Comment,
                            json_schema_resource)

        # add comment to document
        comment_id = doc.add_comment(comment)
        doc.reload()
        comment = doc.comments[comment_id]

        resp = to_json(json_schema_collection, comments={comment_id: comment})
        return Response(response=resp, status=201,
                        mimetype='application/json',
                        headers={'location': comment.uri})

    @acl.acl('write')
    def put(self, space, doc_id, comment_id):
        # get document
        doc = self.get_document(space, doc_id, 'write')

        # get json from request
        json = get_json()

        # check if comment exists
        comment = self.get_comment(doc.comments, comment_id)

        # update comment object from json
        if 'comments' in json:
            json = json['comments'][0]
        comment = update_from_json(json, comment,
                                   json_schema_resource)

        # update comment on document
        doc.update_comment(comment)
        doc.reload()
        comment = doc.comments[comment_id]

        resp = to_json(json_schema_collection, comments={comment_id: comment})
        return Response(response=resp, status=200,
                        mimetype='application/json',
                        headers={'location': comment.uri})

    patch = put

    @acl.acl('write')
    def delete(self, space, doc_id, comment_id):
        # get document
        doc = self.get_document(space, doc_id, 'write')

        # check if comment exists
        comment = self.get_comment(doc.comments, comment_id)

        # delete comment
        try:
            doc.delete_comment(comment)
        except:
            logger.debug('comment delete failed: database error')
            abort(422, _('Error while deleting comment.'))

        return Response(status=204, mimetype='application/json')

comments_view = CommentsAPI.as_view('comments')
blueprint_api_comments.\
    add_url_rule(rest_uri_collection, defaults={'comment_id': None},
                 view_func=comments_view,
                 methods=['GET'])
blueprint_api_comments.\
    add_url_rule(rest_uri_collection,
                 view_func=comments_view,
                 methods=['POST'])
blueprint_api_comments.\
    add_url_rule(rest_uri_resource,
                 view_func=comments_view,
                 methods=['GET', 'PUT', 'PATCH', 'DELETE'])
