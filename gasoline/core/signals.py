# -*- coding: utf-8 -*-
"""Gasoline signals."""

from flask.signals import Namespace

__all__ = ['event']

signals = Namespace()

# used to notify various events
event = signals.signal('event')
