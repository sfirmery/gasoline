# -*- coding: utf-8 -*-
""""""

import logging
from datetime import datetime
from flask.ext.login import current_user

from gasoline.core.signals import event
from gasoline.services.base import Service

from .models import Activity

__all__ = ['ActivityService']

logger = logging.getLogger('gasoline')


class ActivityService(Service):
    """activity service"""
    name = 'activity'

    def init_app(self, app):
        """intialise activity service with flask configuration"""
        super(ActivityService, self).init_app(app)

    def start(self):
        event.connect(self.activity_callback)
        super(ActivityService, self).start()

    def stop(self):
        event.disconnect(self.activity_callback)
        super(ActivityService, self).stop()

    def activity_callback(self, sender, **extra):
        """signals callback for activity"""
        logger.debug('new activity from %r', sender)
        activity = Activity(date=datetime.utcnow(),
                            action='edit',
                            user=current_user.id,
                            document=extra['document'])
        activity.save()
