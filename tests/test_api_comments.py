# -*- coding: utf-8 -*-

import json

from gasoline.models.comment import (
    rest_uri_collection, rest_uri_resource,
    json_schema_collection as json_schema_comments)
from tests import suite, GasolineTestCase


class CommentsAPITestCase(GasolineTestCase):

    headers = [('Content-Type', 'application/json')]
    json_resource = {
        'author': 'unittest_user',
        'content': 'comment created by unittest',
    }
    json_collection = {'comments': [json_resource]}

    @classmethod
    def setUpClass(cls):
        super(CommentsAPITestCase, cls).setUpClass()
        cls.space = suite.space
        cls.json_resource['author'] = suite.user
        cls.doc_id = suite.doc_id

    # helpers
    def get_comments(self):
        uri = rest_uri_collection.\
            replace('<space>', self.space).\
            replace('<doc_id>', self.doc_id)
        return self.app.get(uri, follow_redirects=True)

    def post_comment(self, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_resource
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_collection.\
            replace('<space>', self.space).\
            replace('<doc_id>', self.doc_id)
        return self.app.post(uri, data=json.dumps(data),
                             headers=self.headers, follow_redirects=True)

    def get_comment(self, comment_id):
        uri = rest_uri_resource.\
            replace('<space>', self.space).\
            replace('<doc_id>', self.doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.get(uri, follow_redirects=True)

    def put_comment(self, comment_id, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_resource
            data['id'] = comment_id
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_resource.\
            replace('<space>', self.space).\
            replace('<doc_id>', self.doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.put(uri, data=json.dumps(data),
                            headers=self.headers, follow_redirects=True)

    def delete_comment(self, comment_id):
        uri = rest_uri_resource.\
            replace('<space>', self.space).\
            replace('<doc_id>', self.doc_id).\
            replace('<comment_id>', comment_id)
        return self.app.delete(uri, headers=self.headers,
                               follow_redirects=True)

    def test_crud_comment(self):
        """Create, read, update and delete comment."""
        # create comment
        comments = self.asserts_valid(
            self.post_comment(), 201, json_schema_comments)

        for key, value in comments['comments'].iteritems():
            # get comment
            self.asserts_valid(
                self.get_comment(key), 200, json_schema_comments)
            # update comment
            json_data = self.asserts_valid(
                self.put_comment(key, content='comment updated by unittest'),
                200, json_schema_comments)
            self.assertEqual(json_data['comments'][key]['content'],
                             'comment updated by unittest')

            # delete comment
            self.asserts_valid(self.delete_comment(key), 204)

    def test_get_comment(self):
        """Get document comment."""
        self.asserts_valid(
            self.get_comment(suite.comment_id), 200, json_schema_comments)

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
