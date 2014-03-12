# -*- coding: utf-8 -*-
"""initialise flask application"""
import logging

from babel import Locale

# flask
from flask import Flask, request
from flask import g
from flask.ext.assets import Bundle
from flask.ext.login import current_user
from flask.ext.babel import Babel

from .config import DefaultConfig
from .extensions import db, cache, lm, assets
from .user import User, user
from .frontend import frontend


def create_app():
    """create flask app"""
    app = Flask('gasoline')
    app.config.from_object(DefaultConfig)

    init_extensions(app)

    register_blueprints(app, [frontend, user])

    @app.before_request
    def before_request():
        from .frontend.forms import SearchForm
        if current_user.is_authenticated():
            g.search_form = SearchForm()

    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                                      restrictions=['gasoline'])

    init_logging(app)

    return app


def init_extensions(app):
    """initialise flask extensions"""

    # init flask-mongoengine
    db.init_app(app)

    # init flask-cache
    cache.init_app(app)
    # cache.init_app(app, config={'CACHE_TYPE': 'null'})
    # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    # init flask-login
    lm.login_view = 'user.login'
    lm.login_message_category = "info"

    @lm.user_loader
    def load_user(id):
        return User.objects(name=id).first()
    lm.setup_app(app)

    # flask-babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('ACCEPT_LANGUAGES')
        negociated = Locale.negotiate(request.accept_languages.values(),
                                      accept_languages)
        if negociated is None:
            negociated = Locale.negotiate(request.accept_languages.values(),
                                          accept_languages, sep='-')
        return negociated

    # init flask-assets
    assets.init_app(app)
    jsasset = Bundle('vendors/jquery/jquery.js',
                     'vendors/bootstrap/js/bootstrap.js',
                     'vendors/bootstrap-datepicker/js/bootstrap-datepicker.js',
                     filters='jsmin', output='js/gasoline.js')
    assets.register('js_all', jsasset)
    css = Bundle('vendors/bootstrap/css/bootstrap.css',
                 'vendors/bootstrap-datepicker/css/datepicker3.css',
                 'vendors/font-awesome/css/font-awesome.css',
                 filters='cssmin', output='css/gasoline.css')
    assets.register('css_all', css)


def register_blueprints(app, blueprints):
    """register flask blueprints"""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def init_logging(app):
    """logging initialisation"""
    # logger = logging.getLogger(__name__)
    logger = app.logger

    # define logging level
    if app.debug or app.testing:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if hasattr(logging, 'captureWarnings'):
        # New in Python 2.7
        logging.captureWarnings(True)

    # define logging handler
    console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)
    console_format = '%(asctime)s - %(name)s:%(lineno)d(%(funcName)s): \
%(levelname)s %(message)s'
    console_formatter = logging.Formatter(console_format, '%b %d %H:%M:%S')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
