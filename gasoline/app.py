# -*- coding: utf-8 -*-
"""initialise flask application"""
import logging
from functools import partial

from babel import Locale

# flask
from flask import Flask, render_template, request, g
from flask.ext.login import current_user
from flask.ext.assets import Bundle
from werkzeug.datastructures import ImmutableDict

from gasoline.config import DefaultConfig
from gasoline.core import extensions, signals
from gasoline.models import User
from gasoline.views import (
    blueprint_search, blueprint_document, blueprint_user, blueprint_index,
    blueprint_urlshortener)
from gasoline.services import (
    acl_service, indexer_service, event_service, urlshortener_service)

logger = logging.getLogger('gasoline')

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
    plugins = []
    _blueprints = [blueprint_index,
                   blueprint_document,
                   blueprint_user,
                   blueprint_search,
                   blueprint_urlshortener]

    def __init__(self, name=None, config=None, *args, **kwargs):
        name = name or __name__
        super(Application, self).__init__(name, *args, **kwargs)

        if config:
            self.config.from_object(config)

        # setup logging
        self.setup_logging()

        self._assets_bundles = {
            'css': {'options': dict(filters='cssmin',
                                    output='css/style-%(version)s.min.css')},
            'js-top': {'options': dict(output='js/top-%(version)s.min.js')},
            'js': {'options': dict(output='js/app-%(version)s.min.js')},
        }

        # for http_error_code in (403, 404, 500):
        #   self.install_default_handler(http_error_code)

        self.init_extensions()

        self.register_services()
        # load services
        self.start_services()

        # TODO: register plugins ###
        self.register_plugins()
        signals.plugins_registered.send(self)

        self.register_blueprints()

        @self.before_request
        def before_request():
            from gasoline.forms import SearchForm
            if current_user.is_authenticated():
                g.search_form = SearchForm()

        # request_started.connect(self._setup_breadcrumbs)

    def init_extensions(self):
        """
        Initializes flask extensions, helpers and services.
        """

        # load flask-mongoengine extension
        extensions.db.init_app(self)

        # init flask-cache
        # extensions.cache.init_app(self)
        extensions.cache.init_app(self, config={'CACHE_TYPE': 'null'})
        # extensions.cache.init_app(app, config={'CACHE_TYPE': 'simple'})

        # init flask-login
        extensions.lm.login_view = 'user.login'
        extensions.lm.login_message_category = "info"

        @extensions.lm.user_loader
        def load_user(id):
            return User.objects(name=id).first()
        extensions.lm.setup_app(self)

        # extensions.mail.init_app(self)

        #  DeferredJS
        # DeferredJS(self)

        extensions.assets.init_app(self)
        self._assets_bundles['js']['files'] = [
            'vendors/jquery/jquery.js',
            'vendors/bootstrap/js/bootstrap.js',
            'vendors/bootstrap-datepicker/js/bootstrap-datepicker.js',
            'vendors/select2/select2.js']
        self._assets_bundles['css']['files'] = [
            'vendors/bootstrap/css/bootstrap.css',
            'vendors/bootstrap-datepicker/css/datepicker3.css',
            'vendors/font-awesome/css/font-awesome.css',
            'vendors/select2/select2.css']

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
            negociated = Locale.\
                negotiate(request.accept_languages.values(), accept_languages)
            if negociated is None:
                negociated = Locale.\
                    negotiate(request.accept_languages.values(),
                              accept_languages, sep='-')
            return negociated

        # # CSRF by default
        # if self.config.get('CSRF_ENABLED'):
        #     extensions.csrf.init_app(self)
        #     self.extensions['csrf'] = extensions.csrf

        # define errors handlers
        for http_error_code in (403, 404, 410, 500):
            handler = partial(self.handle_http_error, http_error_code)
            self.errorhandler(http_error_code)(handler)

    def setup_logging(self):
        """logging initialisation"""
        self.logger  # force flask to create application logger before logging
                     # configuration; else, flask will overwrite our settings
        # logger = logging.getLogger(__name__)

        # define logging level
        if self.debug or self.testing:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.setLevel(logging.DEBUG)

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

    def register_services(self):
        """Register Gasoline services"""
        # Gasoline services
        acl_service.init_app(self)
        indexer_service.init_app(self)
        event_service.init_app(self)
        urlshortener_service.init_app(self)

    def start_services(self):
        """Start registred services"""
        for svc in self.services.values():
            svc.start()

    def stop_services(self):
        """Stop registred services"""
        for svc in self.services.values():
            svc.stop()

    def register_plugins(self):
        """register plugins"""
        pass

    def register_blueprints(self):
        """register flask blueprints"""
        for blueprint in self._blueprints:
            self.register_blueprint(blueprint)

    def handle_http_error(self, code, error):
        """error handler"""
        template = 'errors/error{:d}.html'.format(code)
        return render_template(template, error=error), code


def create_app(config=DefaultConfig):
    return Application(config=config)
