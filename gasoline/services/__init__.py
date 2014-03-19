# -*- coding: utf-8 -*-
"""Modules that provide services"""

from flask import current_app

from .base import Service
# from .audit import audit_service
from .indexer import IndexerService
from .event import EventService
from .urlshortener import URLShortenerService

__all__ = [
    'Service',
    'get_service',
    'indexer_service',
    'event_service',
    'urlshortener_service']

indexer_service = IndexerService()
event_service = EventService()
urlshortener_service = URLShortenerService()


def get_service(service):
    return current_app.services.get(service)
