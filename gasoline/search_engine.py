# -*- coding: utf-8 -*-

import os.path
from whoosh.fields import SchemaClass
from whoosh.fields import TEXT, KEYWORD, ID, DATETIME, NGRAM, NGRAMWORDS
from whoosh.analysis import StemmingAnalyzer
from whoosh.filedb.filestore import FileStorage
from whoosh import scoring
from whoosh.qparser import MultifieldParser

__all__ = ['Indexer', 'MainSchema', 'NGramSchema']


class MainSchema(SchemaClass):
    """Whoosh schema for global indexer"""
    id = ID(stored=True, unique=True)
    doc_type = KEYWORD(stored=True)
    title = TEXT()
    space = KEYWORD()
    content = TEXT(analyzer=StemmingAnalyzer())
    last_author = KEYWORD()
    author = KEYWORD()
    creation = DATETIME()
    last_update = DATETIME()


class NGramSchema(SchemaClass):
    """Whoosh schema for N-Gram indexer"""
    id = ID(stored=True, unique=True)
    doc_type = KEYWORD(stored=True)
    title = NGRAM(minsize=2, maxsize=10, stored=True)
    space = NGRAMWORDS(minsize=2, maxsize=10, stored=True)
    tag = NGRAMWORDS(minsize=2, maxsize=10, stored=True)


class Indexer(object):
    """Whoosh Indexer"""
    ix = None
    ngram_ix = None

    def __init__(self):
        """init Indexer"""
        super(Indexer, self).__init__()

    def _open_indexes(self, app):
        """open storage and open indexes"""
        if not os.path.exists("index"):
            os.mkdir("index")
        storage = FileStorage("index")

        # open or initialise main index
        if not storage.index_exists(indexname='MAIN'):
            self.ix = storage.\
                create_index(MainSchema, indexname='MAIN')
        self.ix = storage.open_index(indexname='MAIN')

        # open or initialise ngram index
        if not storage.index_exists(indexname='ngram'):
            self.ngram_ix = storage.\
                create_index(NGramSchema, indexname='ngram')
        self.ngram_ix = storage.open_index(indexname='ngram')

    def init_app(self, app):
        """intialise indexer with flask configuration"""
        self._open_indexes(app)

    def index_document(self, document):
        """update or add index for document"""
        # update or add to main index
        with self.ix.writer() as w:
            w.update_document(id=unicode(document.id),
                              title=document.title,
                              space=document.space,
                              content=document.content,
                              last_author=document.last_author,
                              author=document.author,
                              last_update=document.last_update,
                              creation=document.creation)
        # update or add to ngram index
        with self.ngram_ix.writer() as w:
            w.update_document(id=unicode(document.id),
                              title=document.title,
                              space=document.space,
                              tag=None)

    def search(self, query):
        """search on main index"""
        with self.ix.\
                searcher(weighting=scoring.BM25F(title_B=2)) as searcher:
            qp = MultifieldParser(['title', 'space', 'content'],
                                  schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=25)
            print 'results %r' % results
            results_list = []
            for i, r in enumerate(results):
                print r, i, results.score(i)
                results_list.append({'res': r, 'score': results.score(i)})
            return results, results_list

    def ngram_search(self, query):
        """search on ngram index"""
        with self.ngram_ix.\
                searcher(weighting=scoring.BM25F(title_B=2)) as searcher:
            qp = MultifieldParser(['title', 'space', 'tag'],
                                  schema=self.ngram_ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=25)
            print 'results %r' % results
            results_list = []
            for i, r in enumerate(results):
                print r, i, results.score(i)
                results_list.append({'res': r, 'score': results.score(i)})
            return results, results_list

indexer = Indexer()
