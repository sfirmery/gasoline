# -*- coding: utf-8 -*-

from .document import blueprint_document
from .search import blueprint_search
from .user import blueprint_user
from .dashboard import blueprint_dashboard

__all__ = ['blueprint_document',
           'blueprint_search',
           'blueprint_user',
           'blueprint_dashboard']
