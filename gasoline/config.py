# -*- coding: utf-8 -*-

import os

# from utils import make_dir, INSTANCE_FOLDER_PATH


class BaseConfig(object):

    PROJECT = "Gasoline"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ['youremail@yourdomain.com']

    SECRET_KEY = 'you-will-never-guess'
    CSRF_ENABLED = True


class DefaultConfig(BaseConfig):

    DEBUG = True

    # flask-mongoengine
    MONGODB_SETTINGS = {'DB': 'gasoline'}

    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['fr']
    BABEL_DEFAULT_LOCALE = 'en'

    # Flask-cache: http://pythonhosted.org/Flask-Cache/
    # CACHE_TYPE = 'simple'
    CACHE_TYPE = 'null'
    CACHE_DEFAULT_TIMEOUT = 60

    INDEX_PATH = 'indexdir'
