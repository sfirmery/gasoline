# -*- coding: utf-8 -*-

from .people import blueprint_api_people
from .spaces import blueprint_api_spaces
from .documents import blueprint_api_documents
from .comments import blueprint_api_comments
from .tags import blueprint_api_tags
from .search import blueprint_api_search

__all__ = [
    'blueprint_api_people',
    'blueprint_api_spaces',
    'blueprint_api_documents',
    'blueprint_api_comments',
    'blueprint_api_tags',
    'blueprint_api_search',
]
