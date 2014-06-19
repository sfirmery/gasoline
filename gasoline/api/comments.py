# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, abort, Response
from flask.views import MethodView
# from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _

from gasoline.core.api import (
    get_json, to_json, from_json, update_from_json)
# from gasoline.services import acl_service as acl
from gasoline.models import BaseDocument, Comment
from gasoline.models.comment import (
    json_schema_collection, json_schema_resource,
    rest_uri_collection, rest_uri_resource)

blueprint_api_comments = Blueprint('api.comments', __name__)
route = blueprint_api_comments.route

logger = logging.getLogger('gasoline')


class CommentsAPI(MethodView):
    # decorators = [login_required]

    # @acl.acl('read')
    def get(self, space, doc_id, comment_id):
        if comment_id is None:
            try:
                doc = BaseDocument.objects(space=space, id=doc_id).first()
                comments = doc.comments
            except:
                abort(404, _('Comment not found'))
            resp = to_json(json_schema_collection, comments=comments)
        else:
            try:
                doc = BaseDocument.objects(space=space, id=doc_id).first()
                comment = doc.comments[comment_id]
            except:
                abort(404, _('Comment not found'))
            resp = to_json(json_schema_collection,
                           comments={comment_id: comment})
        return Response(response=resp, status=200,
                        mimetype='application/json')

    def post(self, space, doc_id):
        # get json from request
        json = get_json()

        # get document
        try:
            doc = BaseDocument.objects(space=space, id=doc_id).first()
            # check if document exists
            if doc is None:
                raise
        except:
            logger.debug('post comment failed: document not found')
            abort(404, _('Document not found.'))

        # create comment from json
        comment = from_json(json, Comment,
                            json_schema_resource)

        # print 'doc dict before: {}'.format(doc.__dict__)
        comment_id = doc.add_comment(comment)
        doc.reload()
        # print 'doc dict after: {}'.format(doc.__dict__)
        comment = doc.comments[comment_id]

        resp = to_json(json_schema_collection, comments={comment_id: comment})
        return Response(response=resp, status=201,
                        mimetype='application/json',
                        headers={'location': comment.uri})

    def put(self, space, doc_id, comment_id):
        # get json from request
        json = get_json()

        # get document
        try:
            doc = BaseDocument.objects(space=space, id=doc_id).first()
            # check if document exists
            if doc is None:
                raise
        except:
            logger.debug('post comment failed: document not found')
            abort(404, _('Document not found.'))

        # check if comment exists
        try:
            comment = doc.comments[comment_id]
        except:
            logger.debug('comment update failed: comment not found')
            abort(404, _('Comment not found.'))

        # update comment from json
        if 'comments' in json:
            json = json['comments'][0]
        comment = update_from_json(json, comment,
                                   json_schema_resource)

        # print 'doc dict before: {}'.format(doc.__dict__)
        doc.update_comment(comment)
        doc.reload()
        # print 'doc dict after: {}'.format(doc.__dict__)
        comment = doc.comments[comment_id]

        resp = to_json(json_schema_collection, comments={comment_id: comment})
        return Response(response=resp, status=200,
                        mimetype='application/json',
                        headers={'location': comment.uri})

    patch = put

    def delete(self, space, doc_id, comment_id):
        # get document
        try:
            doc = BaseDocument.objects(space=space, id=doc_id).first()
            # check if document exists
            if doc is None:
                raise
        except:
            logger.debug('post comment failed: document not found')
            abort(404, _('Document not found.'))

        # # check if comment exists
        # if comment_id not in doc.comments:
        #     logger.debug('comment update failed: comment not found')
        #     abort(404, _('Comment not found.'))
        try:
            comment = doc.comments[comment_id]
        except:
            logger.debug('comment update failed: comment not found')
            abort(404, _('Comment not found.'))

        # delete comment
        try:
            doc.delete_comment(comment)
        except:
            logger.exception('')
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
