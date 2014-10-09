# -*- coding: utf-8 -*-

import json
from random import randint

from gasoline.models.space import (
    rest_uri_collection, rest_uri_resource,
    json_schema_collection as json_schema_spaces)
from tests import suite, GasolineTestCase


class SpacesAPITestCaseMixin(object):
    headers = [('Content-Type', 'application/json')]
    json_space = {
        'name': 'unittest_space',
        'description': 'space created by unittest',
    }
    json_spaces = {'spaces': [json_space]}

    # helpers
    def get_spaces(self):
        return self.app.get(rest_uri_collection, follow_redirects=True)

    def post_space(self, space, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_space
            data['name'] = space
            for key, value in kwargs.iteritems():
                data[key] = value
        return self.app.post(rest_uri_collection, data=json.dumps(data),
                             headers=self.headers, follow_redirects=True)

    def get_space(self, space):
        return self.app.get(rest_uri_resource.replace('<space>', space),
                            follow_redirects=True)

    def put_space(self, space, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = self.json_space
            data['name'] = space
            for key, value in kwargs.iteritems():
                data[key] = value
        return self.app.put(rest_uri_resource.replace('<space>', space),
                            data=json.dumps(data),
                            headers=self.headers, follow_redirects=True)

    def delete_space(self, space):
        return self.app.delete(rest_uri_resource.replace('<space>', space),
                               headers=self.headers,
                               follow_redirects=True)


class SpacesAPITestCase(GasolineTestCase, SpacesAPITestCaseMixin):

    @classmethod
    def setUpClass(cls):
        super(SpacesAPITestCase, cls).setUpClass()
        cls.json_space['name'] = suite.space
        cls.space = 'unittest_space_{}'.format(randint(0, 1000))

    def test_crud_space(self):
        """Create, read, update and delete space."""
        # create space
        rv = self.post_space(self.space)
        self.asserts_valid(rv, 201)

        # get space
        self.asserts_valid(
            self.get_space(self.space), 200, json_schema_spaces)

        # update space
        rv = self.put_space(self.space, description='updated by unittest')
        json_data = self.asserts_valid(rv, 200, json_schema_spaces)
        self.assertEqual(json_data['spaces'][0]['description'],
                         'updated by unittest')

        # delete space
        self.asserts_valid(self.delete_space(self.space), 204)

    def test_get_space(self):
        """Testing GET space for all cases."""
        for key, value in suite.cases.iteritems():
            rv = self.get_space(value['space'])
            if self.asserts_acl(rv, 'read', value['can']):
                self.asserts_valid(rv, 200, json_schema_spaces)

    def test_put_space(self):
        """Testing PUT space for all cases."""
        for key, value in suite.cases.iteritems():
            rv = self.put_space(value['space'],
                                description='updated by unittest')
            if self.asserts_acl(rv, 'write', value['can']):
                json_data = self.asserts_valid(rv, 200, json_schema_spaces)
                self.assertEqual(json_data['spaces'][0]['description'],
                                 'updated by unittest')

    # undefined space
    def test_get_undefined_space(self):
        """Testing GET space with undefined space."""
        self.asserts_error(self.get_space('undefined'), 404)

    def test_put_undefined_space(self):
        """Testing PUT space with undefined space."""
        self.asserts_error(
            self.put_space('undefined', description='new description'), 404)

    def test_delete_undefined_space(self):
        """Testing DELETE space with undefined space."""
        self.asserts_error(self.delete_space('undefined'), 404)

    # wrong json input
    def test_post_wrong_json_space(self):
        """Testing POST space with wrong json input."""
        self.asserts_error(self.post_space(suite.space, data='wrong'), 400)

    def test_put_wrong_json_space(self):
        """Testing PUT space with wrong json input."""
        self.asserts_error(
            self.put_space(suite.space, data='wrong'), 400)

    # wront input
    def test_put_wrong_space(self):
        """Testing PUT space with wrong space name."""
        self.asserts_error(
            self.put_space(suite.space, name='undef', description='desc'), 422)

    def test_get_spaces(self):
        """Get list of spaces."""
        self.asserts_valid(self.get_spaces(), 200, json_schema_spaces)
