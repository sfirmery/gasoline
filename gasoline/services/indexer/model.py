# -*- coding: utf-8 -*-

rest_uri_collection = '/api/v1/search'
# rest_uri_resource = '{}/<path:query>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Search result resource Schema',
    'type': 'object',
    'required': ['predicate', 'permissions'],
    'properties': {
        'id': {'type': 'string'},
        'space': {'type': 'string'},
        'title': {'type': 'string'},
        'rank': {'type': 'string'},
        'score': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Search results Schema',
    'type': 'object',
    'required': ['results'],
    'properties': {
        'estimated_length': {'type': 'int'},
        'scored_length': {'type': 'int'},
        'runtime': {'type': 'float'},
        'results': {
            'type': 'array',
            'minItems': 0,
            'items': json_schema_resource,
        }
    },
}


class SearchResult(object):

    def __init__(self, id, space, title, rank, score, *args, **kwargs):
        self.id = id
        self.space = space
        self.title = title
        self.rank = rank
        self.score = score

    def __repr__(self):
        return '<SearchResult "{}.{}" {}>'.format(
            self.space, self.title, self.rank)


class SearchResults(object):

    def __init__(self, results, *args, **kwargs):
        self.estimated_length = results.estimated_length()
        self.scored_length = results.scored_length()
        self.runtime = results.runtime

        self.results = []
        for i, r in enumerate(results):
            self.results.append(SearchResult(**{
                'id': r.get('id', ''),
                'space': r.get('space', ''),
                'title': r.get('title', ''),
                'rank': r.rank,
                'score': results.score(i)
            }))

    def __repr__(self):
        return '<SearchResults {} entries>'.format(self.scored_length)
