# -*- coding: utf-8 -*-
"""initialise flask application"""
import logging

from babel import Locale

# flask
from flask import Flask, request, g
from flask.ext.login import current_user
from flask.ext.assets import Bundle
from werkzeug.datastructures import ImmutableDict

from gasoline.config import DefaultConfig
# from .extensions import db, cache, lm, assets
from gasoline.core import extensions
# from .signals import signals
from gasoline.models import User
from gasoline.views import (
    blueprint_search, blueprint_document, blueprint_user, blueprint_dashboard)
from gasoline.services import indexer_service, event_service


default_config = dict(Flask.default_config)
default_config.update(
    CSRF_ENABLED=True,
    PLUGINS=(),
)
default_config = ImmutableDict(default_config)


class Application(Flask):
    """
    Base application class. Extend it in your own app.
    """
    default_config = default_config

    services = {}

    APP_PLUGINS = ('',)

    def __init__(self, name=None, config=None, *args, **kwargs):
        name = name or __name__
        super(Application, self).__init__(name, *args, **kwargs)

        if config:
            self.config.from_object(config)

        # setup logging
        self.setup_logging()

        # self._jinja_loaders = list()
        # self.register_jinja_loaders(
        #   jinja2.PackageLoader('abilian.web', 'templates'))

        self._assets_bundles = {
            'css': {'options': dict(filters='cssmin, cssrewrite',
                                    output='css/style-%(version)s.min.css')},
            'js-top': {'options': dict(output='js/top-%(version)s.min.js')},
            'js': {'options': dict(output='js/app-%(version)s.min.js')},
        }

        # for http_error_code in (403, 404, 500):
        #   self.install_default_handler(http_error_code)

        self.init_extensions()

        # TODO: register plugins ###
        # self.register_plugins()

        self.register_services()
        self.register_blueprints([blueprint_search,
                                  blueprint_document,
                                  blueprint_user,
                                  blueprint_dashboard])

        @self.before_request
        def before_request():
            from gasoline.forms import SearchForm
            if current_user.is_authenticated():
                    g.search_form = SearchForm()

        # signals.components_registered.send(self)

        # request_started.connect(self._setup_breadcrumbs)

        # load services
        self.start_services()

    def init_extensions(self):
        """
        Initializes flask extensions, helpers and services.
        """

        # load flask-mongoengine extension
        extensions.db.init_app(self)

        # init flask-cache
        extensions.cache.init_app(self)
        # cache.init_app(app, config={'CACHE_TYPE': 'null'})
        # cache.init_app(app, config={'CACHE_TYPE': 'simple'})

        # init flask-login
        extensions.lm.login_view = 'user.login'
        extensions.lm.login_message_category = "info"

        @extensions.lm.user_loader
        def load_user(id):
            return User.objects(name=id).first()
        extensions.lm.setup_app(self)

        # extensions.mail.init_app(self)
        # actions.init_app(self)

        # from abilian.core.jinjaext import DeferredJS
        # DeferredJS(self)

        # # webassets
        # self._setup_asset_extension()
        # self._register_base_assets()

        extensions.assets.init_app(self)
        self._assets_bundles['js']['files'] = [
            'vendors/jquery/jquery.js',
            'vendors/bootstrap/js/bootstrap.js',
            'vendors/bootstrap-datepicker/js/bootstrap-datepicker.js']
        self._assets_bundles['css']['files'] = [
            'vendors/bootstrap/css/bootstrap.css',
            'vendors/bootstrap-datepicker/css/datepicker3.css',
            'vendors/font-awesome/css/font-awesome.css']

        for name, data in self._assets_bundles.items():
            files = data.get('files', [])
            options = data.get('options', {})
            if files:
                extensions.assets.register(name, Bundle(*files, **options))

        # flask-babel
        extensions.babel.init_app(self)

        @extensions.babel.localeselector
        def get_locale():
            accept_languages = self.config.get('ACCEPT_LANGUAGES')
            negociated = Locale.negotiate(request.accept_languages.values(),
                                          accept_languages)
            if negociated is None:
                negociated = Locale.negotiate(request.accept_languages.values(),
                                              accept_languages, sep='-')
            return negociated

        # # CSRF by default
        # if self.config.get('CSRF_ENABLED'):
        #     extensions.csrf.init_app(self)
        #     self.extensions['csrf'] = extensions.csrf

    def setup_logging(self):
        """logging initialisation"""
        self.logger  # force flask to create application logger before logging
                     # configuration; else, flask will overwrite our settings
        # logger = logging.getLogger(__name__)
        # logger = app.logger

        # define logging level
        if self.debug or self.testing:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

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
        self.logger.addHandler(console_handler)

    def register_blueprints(self, blueprints):
        """register flask blueprints"""
        for blueprint in blueprints:
            self.register_blueprint(blueprint)

    def register_services(self):
        """Register Gasoline services"""
        # Gasoline services
        indexer_service.init_app(self)
        event_service.init_app(self)

    def start_services(self):
        """Start registred services"""
        for svc in self.services.values():
            svc.start()

    def stop_services(self):
        """Stop registred services"""
        for svc in self.services.values():
            svc.stop()


def create_app(config=DefaultConfig):
    return Application(config=config)


# def create_app():
#         """create flask app"""
#         app = Flask('gasoline')
#         app.config.from_object(DefaultConfig)

#         # initialise flask extensions
#         init_extensions(app)

#         # initialise search engine
#         init_search_engine(app)

#         # register blueprints
#         register_blueprints(app, [frontend, user])

#         @app.before_request
#         def before_request():
#                 from .frontend.forms import SearchForm
#                 if current_user.is_authenticated():
#                         g.search_form = SearchForm()

#         # load request profiler
#         from werkzeug.contrib.profiler import ProfilerMiddleware
#         app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
#                                                                             restrictions=['gasoline'])

#         event_service = EventService()
#         event_service.init_app(app)
#         event_service.start()

#         indexer_ = IndexerService()
#         indexer_.init_app(app)
#         indexer_.start()

#         # initalialise logging app
#         init_logging(app)

#         return app


# def init_extensions(app):
#     """initialise flask extensions"""
#     # init flask-assets
#     assets.init_app(app)
#     jsasset = Bundle('vendors/jquery/jquery.js',
#                      'vendors/bootstrap/js/bootstrap.js',
#                      'vendors/bootstrap-datepicker/js/bootstrap-datepicker.js',
#                      filters='jsmin', output='js/gasoline.js')
#     assets.register('js_all', jsasset)
#     css = Bundle('vendors/bootstrap/css/bootstrap.css',
#                  'vendors/bootstrap-datepicker/css/datepicker3.css',
#                  'vendors/font-awesome/css/font-awesome.css',
#                  filters='cssmin', output='css/gasoline.css')
#     assets.register('css_all', css)


# def register_blueprints(app, blueprints):
#     """register flask blueprints"""
#     for blueprint in blueprints:
#         app.register_blueprint(blueprint)


# def init_logging(app):
#     """logging initialisation"""
#     # logger = logging.getLogger(__name__)
#     logger = app.logger

#     # define logging level
#     if app.debug or app.testing:
#        logger.setLevel(logging.DEBUG)
#     else:
#         logger.setLevel(logging.INFO)

#     if hasattr(logging, 'captureWarnings'):
#         # New in Python 2.7
#         logging.captureWarnings(True)

#     # define logging handler
#     console_handler = logging.StreamHandler()
#     # console_handler.setLevel(logging.DEBUG)
#     console_format = '%(asctime)s - %(name)s:%(lineno)d(%(funcName)s): \
# %(levelname)s %(message)s'
#     console_formatter = logging.Formatter(console_format, '%b %d %H:%M:%S')
#     console_handler.setFormatter(console_formatter)
#     logger.addHandler(console_handler)
