# -*- coding: utf-8 -*-

# from .search import blueprint_api_search
from .users import blueprint_api_users
from .spaces import blueprint_api_spaces
from .documents import blueprint_api_documents
from .comments import blueprint_api_comments
from .tags import blueprint_api_tags

__all__ = [
    'blueprint_api_users',
    'blueprint_api_spaces',
    'blueprint_api_documents',
    'blueprint_api_comments',
    'blueprint_api_tags',
]
