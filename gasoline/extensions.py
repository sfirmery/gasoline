# -*- coding: utf-8 -*-
"""load flask extensions"""

from flask.ext.mongoengine import MongoEngine
db = MongoEngine()

from flask.ext.cache import Cache
cache = Cache()

from flask.ext.login import LoginManager
lm = LoginManager()

from flask.ext.assets import Environment
assets = Environment()
