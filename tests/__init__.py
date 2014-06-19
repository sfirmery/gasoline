# -*- coding: utf-8 -*-

import unittest
from mongoengine.errors import NotUniqueError
import json
from jsonschema import validate

from gasoline import create_app
from gasoline.core.api import json_schema_error
from gasoline.config import BaseConfig
from gasoline.models import User, Space, BaseDocument, Comment
from gasoline.core.utils import genid


class TestingConfig(BaseConfig):

    DEBUG = False
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


class gasolineTestSuite(unittest.TestSuite):
    def setUpSuite(self):
        user = User(name=u'unittest_user', password=u'test').save()
        self.user = user.name

        space_main = Space(name=u'main').save()
        space = Space(name=u'unittest_space').save()
        self.space = space.name

        try:
            document = BaseDocument(
                space=self.space,
                title=u'unittest_document',
                author=user)
            document.save()
            print 'document: {}'.format(document)
        except NotUniqueError:
            document = BaseDocument.objects(
                space=self.space,
                title=u'unittest_document',
                author=user).first()
            # document.reload()
        self.doc_id = unicode(document.id)

        comment = Comment(author=user, content='unittest comment')
        self.comment_id = genid(key=123456789)
        comment.id = self.comment_id
        document.update(**{'set__comments__' + self.comment_id: comment})

    def tearDownSuite(self):
        pass

    def run(self, result):
        self.setUpSuite()
        super(gasolineTestSuite, self).run(result)
        self.tearDownSuite()


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

app = create_app(config=TestingConfig)
suite = gasolineTestSuite()
