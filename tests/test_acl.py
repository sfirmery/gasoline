# # -*- coding: utf-8 -*-

# # import json
# # from random import randint

# from gasoline.models.space import (
#     json_schema_collection as json_schema_spaces)
# from gasoline.models.comment import (
#     json_schema_collection as json_schema_comments)
# from gasoline.models.document import (
#     json_schema_collection as json_schema_documents)

# from tests import suite, GasolineTestCase
# from test_api_spaces import SpacesAPITestCaseMixin
# from test_api_comments import CommentsAPITestCaseMixin


# class ACLTestCase(GasolineTestCase, SpacesAPITestCaseMixin,
#                   CommentsAPITestCaseMixin):

#     @classmethod
#     def setUpClass(cls):
#         super(ACLTestCase, cls).setUpClass()
#         # cls.space = suite.space
#         # cls.json_resource['author'] = suite.user
#         # cls.doc_id = suite.doc_id
#         # cls.title = 'unittest_document_{}'.format(randint(0, 1000))

#     # Spaces API tests
#     def test_acl_api_spaces(self):
#         """Test ACL on API spaces: list spaces."""
#         json_data = self.asserts_valid(
#             self.get_spaces(), 200, json_schema_spaces)
#         space_names = [space['name'] for space in json_data['spaces']]
#         self.assertIn('main', space_names)

#     def test_get_space(self):
#         """Test ACL on API spaces: get one space."""
#         for key, value in suite.cases.iteritems():
#             rv = self.get_space(value['space'])
#             self.asserts_acl(rv, 'read', value['can'])
            
#     # Comments API tests
#     def test_get_comments(self):
#         """Test ACL on API comments: list comments."""
#         for key, value in suite.cases.iteritems():
#             for doc, meta in value['documents'].iteritems():
#                 rv = self.get_comments(value['space'],
#                                        meta['id'])
#                 if meta['can']['read'] is True:
#                     self.asserts_valid(rv, 200, json_schema_comments)
#                 elif meta['can']['read'] is False:
#                     # print 'cannot read {}.{} ({})'.format(
#                     #     value['space'], doc, meta['id'])
#                     self.asserts_error(rv, 403)

#     # TODO: insert comment in documents
#     # def test_get_comment(self):
#     #     """Test ACL on API comments: get one comment."""
#     #     self.asserts_valid(
#     #         self.get_comment(suite.comment_id), 200, json_schema_comments)
