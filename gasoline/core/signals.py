# -*- coding: utf-8 -*-
"""Gasoline signals."""

from flask.signals import Namespace

__all__ = ['event']

signals = Namespace()

# used to notify various events
event = signals.signal('event')

# used to notify activity
activity = signals.signal('activity')

# triggered at application initialization when all plugins have been loaded
plugins_registered = signals.signal('plugins_registered')
