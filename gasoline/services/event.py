# -*- coding: utf-8 -*-

from gasoline.core.signals import event
from gasoline.services.base import Service

__all__ = ['EventService']


class EventService(Service):
    name = 'event'

    def start(self):
        event.connect(self.event_callback)
        super(EventService, self).start()

    def stop(self):
        event.disconnect(self.event_callback)
        super(EventService, self).stop()

    def event_callback(self, sender, **extra):
        print "event revieved from callback !!!"
