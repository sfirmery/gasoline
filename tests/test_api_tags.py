# -*- coding: utf-8 -*-

import json

from gasoline.models.tag import (
    rest_uri_collection, rest_uri_resource,
    json_schema_resource as json_schema_tag)
from tests import suite, GasolineTestCase


class TagsAPITestCaseMixin(object):
    headers = [('Content-Type', 'application/json')]
    tag = 'tag created by unittest'
    json_tag = {
        'tag': 'tag created by unittest',
    }
    json_tags = {'tags': [json_tag]}

    # helpers
    def get_tags(self, space_id=suite.space, doc_id=suite.doc_id):
        uri = rest_uri_collection.\
            replace('<space>', space_id).\
            replace('<doc_id>', doc_id)
        return self.app.get(uri, follow_redirects=True)

    def post_tag(self, space_id=suite.space, doc_id=suite.doc_id,
                 **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_tag
            for key, value in kwargs.iteritems():
                data[key] = value
        uri = rest_uri_collection.\
            replace('<space>', space_id).\
            replace('<doc_id>', doc_id)
        return self.app.post(uri, data=json.dumps(data),
                             headers=self.headers, follow_redirects=True)

    def get_tag(self, tag_id, space_id=suite.space,
                doc_id=suite.doc_id):
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', doc_id).\
            replace('<tag_id>', tag_id)
        return self.app.get(uri, follow_redirects=True)

    def put_tag(self, tag_id, space_id=suite.space,
                doc_id=suite.doc_id, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = {'tag': kwargs.pop('tag')}
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', doc_id).\
            replace('<tag_id>', tag_id)
        return self.app.put(uri, data=json.dumps(data),
                            headers=self.headers, follow_redirects=True)

    def delete_tag(self, tag_id,
                   space_id=suite.space, doc_id=suite.doc_id):
        uri = rest_uri_resource.\
            replace('<space>', space_id).\
            replace('<doc_id>', doc_id).\
            replace('<tag_id>', tag_id)
        return self.app.delete(uri, headers=self.headers,
                               follow_redirects=True)


class TagsAPITestCase(GasolineTestCase, TagsAPITestCaseMixin):

    @classmethod
    def setUpClass(cls):
        super(TagsAPITestCase, cls).setUpClass()

    def test_crud_tag(self):
        """Create, read, update and delete tag."""
        for key, value in suite.cases.iteritems():
            for doc, doc_value in value['documents'].iteritems():
                rv = self.post_tag(value['space'], doc_value['id'])
                if self.asserts_acl(rv, 'write', value['can'],
                                    doc_value['can']):
                    tag = self.asserts_valid(rv, 201, json_schema_tag)

                    # update tag
                    json_data = self.asserts_valid(
                        self.put_tag(tag['tag'], value['space'],
                                     doc_value['id'],
                                     tag='tag updated by unittest'),
                        200, json_schema_tag)
                    self.assertEqual(json_data['tag'],
                                     'tag updated by unittest')

                    # delete tag
                    self.asserts_valid(
                        self.delete_tag('tag updated by unittest',
                                        value['space'], doc_value['id']), 204)

    # undefined tag
    def test_delete_undefined_tag(self):
        """Testing DELETE tag with undefined tag."""
        self.asserts_error(self.delete_tag('undefined'), 404)

    # wrong json input
    def test_POST_wrong_json_tag(self):
        """Testing POST tag with wrong json input."""
        self.asserts_error(self.post_tag(data='wrong'), 400)

    def test_PUT_wrong_json_tag(self):
        """Testing PUT tag with wrong json input."""
        self.asserts_error(
            self.put_tag(self.tag, data='wrong'), 400)
