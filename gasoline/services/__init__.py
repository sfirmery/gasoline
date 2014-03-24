# -*- coding: utf-8 -*-
"""Modules that provide services"""

from flask import current_app

from .base import Service
# from .audit import audit_service
from .acl import ACLService
from .indexer import IndexerService
from .activity import ActivityService
from .urlshortener import URLShortenerService

__all__ = [
    'Service',
    'get_service',
    'acl_service',
    'indexer_service',
    'activity_service',
    'urlshortener_service']

acl_service = ACLService()
indexer_service = IndexerService()
activity_service = ActivityService()
urlshortener_service = URLShortenerService()


def get_service(service):
    return current_app.services.get(service)
