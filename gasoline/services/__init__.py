"""
Modules that provide services.
"""

from flask import current_app

from .base import Service
# from .audit import audit_service
from .indexer import IndexerService
from .event import EventService

__all__ = ['Service', 'get_service', 'indexer_service', 'event_service']

indexer_service = IndexerService()
event_service = EventService()


def get_service(service):
    return current_app.services.get(service)
