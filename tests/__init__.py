# -*- coding: utf-8 -*-

import unittest
from mongoengine.errors import NotUniqueError
import json
from jsonschema import validate

from gasoline import create_app
from gasoline.core.api import json_schema_error
from gasoline.core.utils import genid
from gasoline.config import BaseConfig
from gasoline.models import User, Space, BaseDocument, Comment
from gasoline.services.acl import ACE


class TestingConfig(BaseConfig):

    DEBUG = True
    TESTING = True
    CSRF_ENABLED = False

    # flask-mongoengine
    MONGODB_SETTINGS = {'DB': 'gasoline_tests'}

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'Europe/Paris'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    # CACHE_TYPE = 'simple'
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 60

    INDEX_PATH = 'indexdir_tests'

    ASSETS_DEBUG = True


class gasolineTestSuite(object):

    ace_deny_all_any = ACE(
        truth='DENY', predicate='ANY', permission=['read', 'write'])
    ace_deny_read_any = ACE(
        truth='DENY', predicate='ANY', permission=['read'])
    ace_deny_write_any = ACE(
        truth='DENY', predicate='ANY', permission=['write'])

    default_acl = {
        'read': True,
        'write': True,
    }

    cases = {
        'none': {
            'can': {'read': None, 'write': None},
            'acl': [],
        },

        # DENY ANY
        'deny_all_any': {
            'can': {'read': False, 'write': False},
            'acl': [ace_deny_all_any],
        },
        'deny_read_any': {
            'can': {'read': False, 'write': None},
            'acl': [ace_deny_read_any],
        },
        'deny_write_any': {
            'can': {'read': None, 'write': False},
            'acl': [ace_deny_write_any],
        },
        # ALLOW ANY
        'allow_all_any': {
            'can': {'read': True, 'write': True},
            'acl': [ACE(
                truth='ALLOW', predicate='ANY', permission=['read', 'write'])],
        },
        'allow_read_any': {
            'can': {'read': True, 'write': None},
            'acl': [ACE(
                truth='ALLOW', predicate='ANY', permission=['read'])],
        },
        'allow_write_any': {
            'can': {'read': None, 'write': True},
            'acl': [ACE(
                truth='ALLOW', predicate='ANY', permission=['write'])],
        },
        # ALLOW unittest_user
        'allow_all_unittest_user': {
            'can': {'read': True, 'write': True},
            'acl': [ACE(
                truth='ALLOW', predicate='u:unittest_user',
                permission=['read', 'write'])],
        },
        'allow_read_unittest_user': {
            'can': {'read': True, 'write': None},
            'acl': [ACE(
                truth='ALLOW', predicate='u:unittest_user',
                permission=['read'])],
        },
        'allow_write_unittest_user': {
            'can': {'read': None, 'write': True},
            'acl': [ACE(
                truth='ALLOW', predicate='u:unittest_user',
                permission=['write'])],
        },
        # DENY unittest_user
        'deny_all_unittest_user': {
            'can': {'read': True, 'write': True},
            'acl': [ACE(
                truth='DENY', predicate='u:unittest_user',
                permission=['read', 'write'])],
        },
        'deny_read_unittest_user': {
            'can': {'read': True, 'write': None},
            'acl': [ACE(
                truth='DENY', predicate='u:unittest_user',
                permission=['read'])],
        },
        'deny_write_unittest_user': {
            'can': {'read': None, 'write': True},
            'acl': [ACE(
                truth='DENY', predicate='u:unittest_user',
                permission=['write'])],
        },
        # ALLOW doe
        'allow_all_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='ALLOW', predicate='u:doe',
                permission=['read', 'write'])],
        },
        'allow_read_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='ALLOW', predicate='u:doe',
                permission=['read'])],
        },
        'allow_write_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='ALLOW', predicate='u:doe',
                permission=['write'])],
        },
        # DENY doe
        'deny_all_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='DENY', predicate='u:doe',
                permission=['read', 'write'])],
        },
        'deny_read_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='DENY', predicate='u:doe',
                permission=['read'])],
        },
        'deny_write_doe': {
            'can': {'read': None, 'write': None},
            'acl': [ACE(
                truth='DENY', predicate='u:doe',
                permission=['write'])],
        },
    }

    def setUpSuite(self):
        with app.test_request_context():

            Space.drop_collection()
            BaseDocument.drop_collection()
            Comment.drop_collection()
            User.drop_collection()

            user = User(name=u'unittest_user', password=u'test').save()
            self.user = user.name
            self.user_obj = user

            space_main = Space(name=u'main', description='main space').save()
            space = Space(name=u'unittest_space').save()
            self.space = space.name

            try:
                document = BaseDocument(
                    space=self.space,
                    title=u'unittest_document',
                    author=user,
                    tags=['unittest'])
                document.save()
            except NotUniqueError:
                document = BaseDocument.objects(
                    space=self.space,
                    title=u'unittest_document',
                    author=user).first()

            # ace = ACE(thruth='DENY', predicate='ANY', permission=['read', 'write'])
            # document.update(push__acl=ace)
            self.doc_id = unicode(document.id)

            comment = Comment(author=user, content='unittest comment', doc=document)
            # self.comment_id = genid(key=123456789)
            # comment.id = self.comment_id
            # document.update(push__comments=comment)
            comment.save()
            comment.reload()
            self.comment_id = unicode(comment.id)

            # create spaces
            spaces = []
            for key, value in self.cases.iteritems():
                space_name = u'unittest_space_{}'.format(key)
                space = Space(name=space_name)
                if len(self.cases[key]['acl']) > 0:
                    space.acl = self.cases[key]['acl']
                space.validate(clean=True)
                spaces.append(space)
                self.cases[key]['space'] = space_name
            try:
                Space.objects.insert(spaces)
            except:
                pass

            # create documents
            documents = []
            for key, value in self.cases.iteritems():
                space_name = u'unittest_space_{}'.format(key)
                self.cases[key]['documents'] = {}
                for doc_key, doc_value in self.cases.iteritems():
                    document_name = u'unittest_document_{}'.format(doc_key)
                    document = BaseDocument(
                        space=space_name, title=document_name,
                        author=suite.user_obj,
                        tags=['unittest'])
                    if len(self.cases[key]['acl']) > 0:
                        document.acl = self.cases[key]['acl']

                    document.validate(clean=True)
                    documents.append(document)
                    self.cases[key]['documents'][document_name] = {
                        'can': self.cases[key]['can'],
                    }

            try:
                documents = BaseDocument.objects.insert(documents)
            except:
                pass

            comments = []
            for doc in documents:
                key = doc.space.replace('unittest_space_', '')

                comment = Comment(
                    author=user, content=(
                        'unittest comment for {}'.format(key)),
                    doc=doc)
                # comment.id = self.comment_id
                # document.comments.append(comment)
                comment.validate(clean=True)
                comments.append(comment)
                comment.save()
                comment.reload()

                self.cases[key]['documents'][doc.title]['id'] = str(doc.id)
                self.cases[key]['documents'][doc.title]['comment'] = str(comment.id)

            # comments = Comment.objects.insert(comments)

    def tearDownSuite(self):
        pass


class GasolineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def asserts_error(self, rv, code):
        """Validate error return."""
        self.assertEqual(rv.status_code, code)
        json_data = json.loads(rv.data)
        self.assertIsNone(validate(json_data, json_schema_error))
        self.assertEqual(json_data['status'], code)

    def asserts_valid(self, rv, code, json_schema=None):
        """Validate success return."""
        self.assertEqual(rv.status_code, code)
        if json_schema is not None:
            json_data = json.loads(rv.data)
            self.assertIsNone(validate(json_data, json_schema))
            return json_data

    def asserts_acl(self, rv, method, space_can, document_can=None):
        def check_acl(can):
            if (can is not None
                    and (method in can and can[method] is not bool)):
                if can[method] is False:
                    self.asserts_error(rv, 403)
                    return False
                elif can[method] is True:
                    self.assertLess(rv.status_code, 400)
                    self.assertGreaterEqual(rv.status_code, 200)
                    return True
            return None

        # ACL at document and space level
        for can in [check_acl(space_can), check_acl(document_can)]:
            if can is not None:
                return can
        # ACL default
        return check_acl(suite.default_acl)

app = create_app(config=TestingConfig)
suite = gasolineTestSuite()
test_loader = unittest.TestLoader()
