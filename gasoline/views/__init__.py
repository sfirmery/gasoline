# -*- coding: utf-8 -*-

from .index import blueprint_index
from .document import blueprint_document
from .search import blueprint_search
from .user import blueprint_user
from .urlshortener import blueprint_urlshortener

__all__ = ['blueprint_index',
           'blueprint_document',
           'blueprint_search',
           'blueprint_user',
           'blueprint_urlshortener']
