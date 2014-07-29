# -*- coding: utf-8 -*-

import json
from random import randint

from gasoline.models.document import (
    rest_uri_collection, rest_uri_resource,
    json_schema_collection as json_schema_documents)
from tests import suite, GasolineTestCase


class DocumentsAPITestCaseMixin(object):

    headers = [('Content-Type', 'application/json')]
    json_resource = {
        'title': 'unittest_document',
        'space': 'unittest_space',
        'content': 'document created by unittest',
        'author': 'unittest_user',
    }
    json_collection = {'documents': [json_resource]}

    # helpers
    def get_documents(self, space_id):
        uri = rest_uri_collection.replace('<space>', space_id)
        return self.app.get(uri, follow_redirects=True)

    def post_document(self, space_id, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_resource
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_collection.replace('<space>', space_id)
        return self.app.post(uri, data=json.dumps(data),
                             headers=self.headers, follow_redirects=True)

    def get_document(self, space_id, document_id):
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', document_id)
        return self.app.get(uri, follow_redirects=True)

    def put_document(self, space_id, document_id, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_resource
            data['id'] = document_id
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', document_id)
        return self.app.put(uri, data=json.dumps(data),
                            headers=self.headers, follow_redirects=True)

    def delete_document(self, space_id, document_id):
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', document_id)
        return self.app.delete(uri, headers=self.headers,
                               follow_redirects=True)


class DocumentsAPITestCase(GasolineTestCase, DocumentsAPITestCaseMixin):

    @classmethod
    def setUpClass(cls):
        super(DocumentsAPITestCase, cls).setUpClass()
        cls.json_resource['author'] = suite.user
        cls.doc_id = suite.doc_id
        cls.title = 'unittest_document_{}'.format(randint(0, 1000))

    def test_crud_document(self):
        """Testing create, read, update and delete document for all cases."""
        for key, value in suite.cases.iteritems():
            # create document
            rv = self.post_document(value['space'],
                                    space=value['space'], title=self.title)
            documents = None
            if self.asserts_acl(rv, 'write', value['can']):
                documents = self.asserts_valid(rv, 201, json_schema_documents)

            if documents is not None and 'documents'in documents:
                for document in documents['documents']:
                    # get document
                    rv = self.get_document(value['space'], document['id'])
                    if self.asserts_acl(rv, 'read', value['can']):
                        self.asserts_valid(rv, 200, json_schema_documents)

                    # update document
                    rv = self.put_document(value['space'], document['id'],
                                           content='updated by unittest',
                                           title=document['title'],
                                           space=value['space'])
                    if self.asserts_acl(rv, 'write', value['can']):
                        json_data = self.asserts_valid(
                            rv, 200, json_schema_documents)
                        self.assertEqual(json_data['documents'][0]['content'],
                                         'updated by unittest')

                    # delete document
                    rv = self.delete_document(value['space'], document['id'])
                    if self.asserts_acl(rv, 'write', value['can']):
                        self.asserts_valid(rv, 204)

    def test_get_document(self):
        """Testing GET document for all cases."""
        for key, value in suite.cases.iteritems():
            for doc, doc_value in value['documents'].iteritems():
                rv = self.get_document(value['space'], doc_value['id'])
                if self.asserts_acl(rv, 'read', value['can']):
                    self.asserts_valid(rv, 200, json_schema_documents)

    def test_put_document(self):
        """Testing PUT document for all cases."""
        for key, value in suite.cases.iteritems():
            for doc, doc_value in value['documents'].iteritems():
                rv = self.put_document(value['space'], doc_value['id'],
                                       content='updated by unittest',
                                       title=doc, space=value['space'])

                if self.asserts_acl(rv, 'write', value['can']):
                    json_data = self.asserts_valid(
                        rv, 200, json_schema_documents)
                    self.assertEqual(json_data['documents'][0]['content'],
                                     'updated by unittest')

    # undefined document
    def test_get_undefined_document(self):
        """Testing GET document with undefined document."""
        self.asserts_error(self.get_document(suite.space, 'undefined'), 404)

    def test_put_undefined_document(self):
        """Testing PUT document with undefined document."""
        self.asserts_error(
            self.put_document(suite.space, 'undefined', content='undef'), 404)

    def test_delete_undefined_document(self):
        """Testing DELETE document with undefined document."""
        self.asserts_error(self.delete_document(suite.space, 'undefined'), 404)

    # wrong json input
    def test_POST_wrong_json_document(self):
        """Testing POST document with wrong json input."""
        self.asserts_error(self.post_document(suite.space, data='wrong'), 400)

    def test_PUT_wrong_json_document(self):
        """Testing PUT document with wrong json input."""
        self.asserts_error(
            self.put_document(suite.space, suite.doc_id, data='wrong'), 400)

    def test_get_documents(self):
        """Get list of documents."""
        self.asserts_valid(
            self.get_documents(suite.space), 200, json_schema_documents)
