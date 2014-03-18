# -*- coding: utf-8 -*-


class Service(object):
    """Base class for services."""

    # service running ?
    running = False

    # service name in app.services
    name = None

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.services[self.name] = self

    def start(self):
        """Starts the service."""
        self.running = True

    def stop(self):
        """Stops the service."""
        self.running = False
