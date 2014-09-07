# -*- coding: utf-8 -*-

import json

from gasoline.models.comment import (
    rest_uri_collection, rest_uri_resource,
    json_schema_collection as json_schema_comments)
from tests import suite, GasolineTestCase


class CommentsAPITestCaseMixin(object):
    headers = [('Content-Type', 'application/json')]
    json_comment = {
        'author': suite.user,
        'content': 'comment created by unittest',
    }
    json_comments = {'comments': [json_comment]}

    # helpers
    def get_comments(self, space=suite.space, doc_id=suite.doc_id):
        uri = rest_uri_collection.\
            replace('<space>', space).\
            replace('<doc_id>', doc_id)
        return self.app.get(uri, follow_redirects=True)

    def post_comment(self, space=suite.space, doc_id=suite.doc_id, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_comment
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_collection.\
            replace('<space>', space).\
            replace('<doc_id>', doc_id)
        return self.app.post(uri, data=json.dumps(data),
                             headers=self.headers, follow_redirects=True)

    def get_comment(self, comment_id, space=suite.space, doc_id=suite.doc_id):
        uri = rest_uri_resource.\
            replace('<space>', space).\
            replace('<doc_id>', doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.get(uri, follow_redirects=True)

    def put_comment(self, comment_id, space=suite.space, doc_id=suite.doc_id,
                    **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_comment
            data['id'] = comment_id
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_resource.\
            replace('<space>', space).\
            replace('<doc_id>', doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.put(uri, data=json.dumps(data),
                            headers=self.headers, follow_redirects=True)

    def delete_comment(self, comment_id,
                       space=suite.space, doc_id=suite.doc_id):
        uri = rest_uri_resource.\
            replace('<space>', space).\
            replace('<doc_id>', doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.delete(uri, headers=self.headers,
                               follow_redirects=True)


class CommentsAPITestCase(GasolineTestCase, CommentsAPITestCaseMixin):

    @classmethod
    def setUpClass(cls):
        super(CommentsAPITestCase, cls).setUpClass()

    def test_crud_comment(self):
        """Create, read, update and delete comment."""
        # create comment
        comments = self.asserts_valid(
            self.post_comment(), 201, json_schema_comments)

        for comment in comments:
            # get comment
            self.asserts_valid(
                self.get_comment(comment['id']), 200, json_schema_comments)
            # update comment
            json_data = self.asserts_valid(
                self.put_comment(comment['id'],
                                 content='comment updated by unittest'),
                200, json_schema_comments)
            self.assertEqual(json_data[0]['content'],
                             'comment updated by unittest')

            # delete comment
            self.asserts_valid(self.delete_comment(comment['id']), 204)

    def test_get_comment(self):
        """Testing GET comment for all cases."""
        for key, value in suite.cases.iteritems():
            for doc, doc_value in value['documents'].iteritems():
                rv = self.get_comment(
                    suite.comment_id, value['space'], doc_value['id'])
                try:
                    if self.asserts_acl(rv, 'read', value['can']):
                        self.asserts_valid(rv, 200, json_schema_comments)
                except:
                    print '{}.{}'.format(value['space'], doc)
                    print doc_value['id']
                    print rv
                    print rv.data
                    print json_schema_comments

    # undefined comment
    def test_get_undefined_comment(self):
        """Testing GET comment with undefined comment."""
        self.asserts_error(self.get_comment('undefined'), 404)

    def test_put_undefined_comment(self):
        """Testing PUT comment with undefined comment."""
        self.asserts_error(self.put_comment('undefined', content='undef'), 404)

    def test_delete_undefined_comment(self):
        """Testing DELETE comment with undefined comment."""
        self.asserts_error(self.delete_comment('undefined'), 404)

    # wrong json input
    def test_POST_wrong_json_comment(self):
        """Testing POST comment with wrong json input."""
        self.asserts_error(self.post_comment(data='wrong'), 400)

    def test_PUT_wrong_json_comment(self):
        """Testing PUT comment with wrong json input."""
        self.asserts_error(
            self.put_comment(suite.comment_id, data='wrong'), 400)

    def test_get_comments(self):
        """Get list of comments."""
        self.asserts_valid(self.get_comments(), 200, json_schema_comments)
