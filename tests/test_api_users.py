# -*- coding: utf-8 -*-

from gasoline.models.user import (
    rest_uri_collection, rest_uri_resource,
    json_schema_collection as json_schema_users)
from tests import suite, GasolineTestCase


class UsersAPITestCase(GasolineTestCase):

    headers = [('Content-Type', 'application/json')]
    json_resource = {
        'name': 'unittest_user',
        'description': 'user created by unittest',
    }
    json_collection = {'users': json_resource}

    @classmethod
    def setUpClass(cls):
        super(UsersAPITestCase, cls).setUpClass()
        cls.json_resource['name'] = suite.user

    # helpers
    def get_users(self):
        return self.app.get(rest_uri_collection, follow_redirects=True)

    # def post_user(self, user, **kwargs):
    #     data = self.json_collection
    #     data['spaces'][0]['name'] = user
    #     for key, value in kwargs.iteritems():
    #         data['spaces'][0][key] = value
    #     return self.app.post(rest_uri_collection, data=json.dumps(data),
    #                          headers=self.headers, follow_redirects=True)

    def get_user(self, user):
        return self.app.get(rest_uri_resource.replace('<name>', user),
                            follow_redirects=True)

    # def put_user(self, user, description, rest_uri_user=None, data=None):
    #     headers = [('Content-Type', 'application/json')]
    #     if rest_uri_user is None:
    #         rest_uri_user = user
    #     if data is None:
    #         data = self.json_resource.format(rest_uri_user, description)
    #     return self.app.put(rest_uri_resource.replace('<name>', user),
    #                         data=data, headers=headers, follow_redirects=True)

    # def delete_user(self, user):
    #     headers = [('Content-Type', 'application/json')]
    #     return self.app.delete(rest_uri_resource.replace('<name>', user),
    #                            headers=headers,
    #                            follow_redirects=True)

    def test_get_user(self):
        """Get unittest_user."""
        self.asserts_valid(self.get_user(suite.user), 200, json_schema_users)

    def test_get_undefined_user(self):
        """Get undefined user."""
        self.asserts_error(self.get_user('undefined_user'), 404)

    def test_get_users(self):
        """Get list of users."""
        self.asserts_valid(self.get_users(), 200, json_schema_users)
