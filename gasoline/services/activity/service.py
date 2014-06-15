# -*- coding: utf-8 -*-
""""""

import logging
from flask import url_for
from flask.ext.login import current_user

from gasoline.core.signals import activity
from gasoline.services.base import Service

from .models import Activity, DocumentObject

__all__ = ['ActivityService']

logger = logging.getLogger('gasoline')


class ActivityService(Service):
    """activity service"""
    name = 'activity'

    def init_app(self, app):
        """initialise activity service with flask configuration"""
        super(ActivityService, self).init_app(app)

    def start(self):
        activity.connect(self.activity_callback)
        super(ActivityService, self).start()

    def stop(self):
        activity.disconnect(self.activity_callback)
        super(ActivityService, self).stop()

    def activity_callback(self, sender, verb, object, object_type, **extra):
        """signals callback for activity"""
        logger.debug('new activity from %r with %r', sender, extra)

        activity = Activity(verb=verb,
                            actor=current_user.get_id(),
                            target=object.space)
        activity.object = DocumentObject(
            object_type=object_type,
            id=str(object.id),
            display_name=object.title,
            url=url_for('document.view', space=object.space,
                        doc_id=str(object.id))
        )
        print 'activity %r' % activity
        activity.save()
