# -*- coding: utf-8 -*-
"""initialise flask application"""
import logging
from functools import partial

from babel import Locale

# flask
from flask import Flask, render_template, request, g
from flask.ext.assets import Bundle
from flask.ext.babel import (
    format_date, format_datetime, format_time, get_locale as babel_get_locale)
from werkzeug.datastructures import ImmutableDict, Headers

from gasoline.config import DefaultConfig
from gasoline.core import extensions, signals
from gasoline.core.api import api_error_handler
from gasoline.models import User
from gasoline.views import blueprint_index, blueprint_urlshortener
from gasoline.api import (
    blueprint_api_people, blueprint_api_spaces,
    blueprint_api_documents, blueprint_api_comments, blueprint_api_tags)
from gasoline.services import (
    acl_service, indexer_service, activity_service, urlshortener_service)
from gasoline.plugins.activity import blueprint_api_plugin_activity
from gasoline.plugins.acl import blueprint_api_plugin_acl

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
    plugins = {}
    _blueprints = [
        blueprint_index,
        blueprint_urlshortener,
        blueprint_api_people,
        blueprint_api_spaces,
        blueprint_api_documents,
        blueprint_api_comments,
        blueprint_api_tags,
    ]

    def __init__(self, name=None, config=None, *args, **kwargs):
        name = name or __name__
        super(Application, self).__init__(name, *args, **kwargs)

        if config:
            self.config.from_object(config)

        # setup logging
        self.setup_logging()

        self._assets_bundles = {
            'css': {
                'options': dict(
                    # filters='cssmin',
                    output='assets/style-%(version)s.min.css')
            },
            'js-top': {
                'options': dict(output='assets/top-%(version)s.min.js')},
            'js': {
                'options': dict(output='assets/app-%(version)s.min.js')},
        }

        self._assets_locales = {
            'locales': ['fr'],
            'output': 'assets/app-%(version)s.min.',
        }

        self._assets_jst = {
            'locales': ['en', 'fr'],
            'output': 'assets/jst-%(version)s.',
            'options': dict(filters='jinja2,jst'),
        }

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
            g.locale = babel_get_locale()

        # request_started.connect(self._setup_breadcrumbs)

        # # load request profiler
        # from werkzeug.contrib.profiler import ProfilerMiddleware
        # self.wsgi_app = ProfilerMiddleware(self.wsgi_app,
        #                                    restrictions=['gasoline'])
        # # self.wsgi_app = ProfilerMiddleware(self.wsgi_app)

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

        @extensions.babel.timezoneselector
        def get_timezone():
            return

        @self.template_filter('date')
        def _jinja2_filter_date(date):
            return format_date(date)

        @self.template_filter('time')
        def _jinja2_filter_time(date):
            return format_time(date)

        @self.template_filter('datetime')
        def _jinja2_filter_datetime(date):
            return format_datetime(date)

        extensions.assets.init_app(self)

        self._assets_bundles['js']['files'] = [
            'vendors/jquery/js/jquery.js',
            'vendors/bootstrap/js/bootstrap.js',
            'vendors/bootstrap-datepicker/js/bootstrap-datepicker.js',
            'vendors/jquery-timeago/js/jquery.timeago.js',
            'vendors/bootstrap-tags/js/bootstrap-tags.js',
            'vendors/underscore/js/underscore.js',
            'vendors/backbone/js/backbone.js',
            'vendors/backbone.marionette/js/backbone.marionette.js',
            'vendors/backbone.babysitter/js/backbone.babysitter.js',
            'vendors/backbone.wreqr/js/backbone.wreqr.js',
            'vendors/backbone.validation/js/backbone-validation.js',
            'vendors/backbone.syphon/js/backbone.syphon.js',
            'js/config/**/*.js',
            'js/backbone/app.js',
            'js/backbone/lib/entities/**/*.js',
            'js/backbone/lib/utilities/**/*.js',
            'js/backbone/lib/views/**/*.js',
            'js/backbone/lib/controllers/**/*.js',
            'js/backbone/lib/regions/**/*.js',
            'js/backbone/lib/components/**/*.js',
            'js/backbone/entities/**/*.js',
            'js/backbone/apps/**/*.js',
        ]
        self._assets_bundles['js']['files'].append('js/gasoline.js')

        self._assets_bundles['css']['files'] = [
            'vendors/bootstrap/css/bootstrap.css',
            'vendors/bootstrap-datepicker/css/datepicker3.css',
            'vendors/font-awesome/css/font-awesome.css',
            'vendors/*bootstrap-tags/css/bootstrap-tags.css',
        ]
        self._assets_bundles['css']['files'].append('css/gasoline.css')

        self._assets_locales['files'] = [
            'vendors/bootstrap-datepicker/js/locales/bootstrap-datepicker.',
            'vendors/jquery-timeago/js/locales/jquery.timeago.',
        ]

        self._assets_jst['files'] = [
            'js/backbone/apps/**/*.jst',
            'js/backbone/lib/**/*.jst',
        ]

        for name, data in self._assets_bundles.items():
            files = data.get('files', [])
            options = data.get('options', {})
            if files:
                extensions.assets.register(name, Bundle(*files, **options))

        for locale in self._assets_locales['locales']:
            files = self._assets_locales.get('files', [])
            files = [file + locale + '.js' for file in files]
            options = self._assets_locales.get('options', {})
            output = self._assets_locales.get('output', {})
            options['output'] = output + locale + '.js'
            if files:
                extensions.assets.register('js-' + locale,
                                           Bundle(*files, **options))

        # for each locales, create translated jst
        for locale in self._assets_jst['locales']:
            # create dummy context with locale
            with self.test_request_context(
                    headers=Headers([('Accept-Language', locale)])):
                files = self._assets_jst.get('files', [])
                options = self._assets_jst.get('options', {})
                output = self._assets_jst.get('output', {})
                options['output'] = output + locale + '.jst'
                if files:
                    extensions.assets.register('jst-' + locale,
                                               Bundle(*files, **options))

        # # CSRF by default
        # if self.config.get('CSRF_ENABLED'):
        #     extensions.csrf.init_app(self)
        #     self.extensions['csrf'] = extensions.csrf

        # define errors handlers
        for http_error_code in (400, 401, 403, 404, 405, 410, 415, 422, 429,
                                500):
            handler = partial(self.handle_http_error, http_error_code)
            self.errorhandler(http_error_code)(handler)

    def setup_logging(self):
        """logging initialisation"""
        self.logger  # force flask to create application logger before logging
                     # configuration; else, flask will overwrite our settings
        # logger = logging.getLogger(__name__)

        # define logging level
        # if self.debug:
        #     logger.setLevel(logging.DEBUG)
        # else:
        #     logger.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)

        if hasattr(logging, 'captureWarnings'):
            # New in Python 2.7
            logging.captureWarnings(True)

        # define logging handler
        console_handler = logging.StreamHandler()
        if self.debug:
            console_handler.setLevel(logging.DEBUG)
        console_format = '%(asctime)s - %(name)s:%(lineno)d:%(filename)s(%(funcName)s): \
    %(levelname)s %(message)s'
        console_formatter = logging.Formatter(console_format, '%b %d %H:%M:%S')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    def register_services(self):
        """Register Gasoline services"""
        # Gasoline services
        acl_service.init_app(self)
        indexer_service.init_app(self)
        activity_service.init_app(self)
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
        self.plugins['activity'] = {'blueprint': blueprint_api_plugin_activity}
        self.plugins['acl'] = {'blueprint': blueprint_api_plugin_acl}

    def register_blueprints(self):
        """register flask blueprints"""
        # register plugins blueprints
        for plugin in self.plugins.values():
            if 'blueprint' in plugin:
                self.register_blueprint(plugin['blueprint'])
        # register blueprints
        for blueprint in self._blueprints:
            self.register_blueprint(blueprint)

    def handle_http_error(self, code, error):
        """error handler"""
        template = 'errors/error{:d}.html.jinja2'.format(code)
        # return api error handler for URI starting with /api/
        if str(request.url_rule).startswith('/api/'):
            return api_error_handler(code, error)
        else:
            try:
                return render_template(template, error=error), code
            except:
                return render_template('errors/error_generic.html.jinja2',
                                       error=error), code


def create_app(config=DefaultConfig):
    return Application(config=config)
