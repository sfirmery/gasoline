# -*- coding: utf-8 -*-

import os.path
from whoosh.fields import SchemaClass
from whoosh.fields import TEXT, KEYWORD, ID, DATETIME, NGRAM, NGRAMWORDS
from whoosh.analysis import StemmingAnalyzer
from whoosh.filedb.filestore import FileStorage
from whoosh import scoring
from whoosh.qparser import MultifieldParser
from whoosh.writing import AsyncWriter, CLEAR

from gasoline.core.signals import event
from gasoline.services.base import Service

__all__ = ['IndexerService', 'MainSchema', 'NGramSchema']


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

_main_default_search_field = ['title', 'space', 'content']


class NGramSchema(SchemaClass):
    """Whoosh schema for N-Gram indexer"""
    id = ID(stored=True, unique=True)
    doc_type = KEYWORD(stored=True)
    title = NGRAM(minsize=2, maxsize=10, stored=True)
    space = NGRAMWORDS(minsize=2, maxsize=10, stored=True)
    tag = NGRAMWORDS(minsize=2, maxsize=10, stored=True)

_ngram_default_search_field = ['title', 'space', 'tag']


class IndexerService(Service):
    """Whoosh Indexer service"""
    name = 'indexer'

    ix = None
    schema = None
    search_field = _main_default_search_field

    ngram_ix = None
    ngram_schema = None
    ngram_search_field = _ngram_default_search_field

    _plugins_fields_main = {'dyn_1': TEXT()}
    _plugins_fields_ngram = {}

    def __init__(self):
        self.schema = MainSchema()
        self.ngram_schema = NGramSchema()

        self._open_indexes()
        super(IndexerService, self).__init__()

    def init_app(self, app):
        """intialise indexer with flask configuration"""
        super(IndexerService, self).init_app(app)

    def start(self):
        event.connect(self.index_document_callback, 'document')
        super(IndexerService, self).start()

    def stop(self):
        event.disconnect(self.index_document_callback)
        super(IndexerService, self).stop()

    def _open_indexes(self):
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

    def register_main_field(self, name, field):
        """register plugins fields in main index"""
        if name not in self._plugins_fields_main:
            self._plugins_fields_main[name] = field

    def register_ngram_field(self, name, field):
        """register plugins fields in ngram index"""
        if name not in self._plugins_fields_ngram:
            self._plugins_fields_ngram[name] = field

    def _update_fields(self):
        """register dynamics field in index"""
        with self.ix.writer() as writer:
            for name, field in self._plugins_fields_main.items():
                print 'plugin field -> name: %r, field: %r' % (name, field)
                if name not in self.ix.schema:
                    print 'add field in index schema'
                    writer.add_field(name, field)
                if name not in self.schema:
                    print 'add field in schema'
                    self.schema.add(name, field)
        with self.ngram_ix.writer() as ngram_writer:
            for name, field in self._plugins_fields_ngram.items():
                print 'plugin field -> name: %r, field: %r' % (name, field)
                if name not in self.ngram_ix.schema:
                    print 'add field in index schema'
                    ngram_writer.add_field(name, field)
                if name not in self.ngram_schema:
                    print 'add field in schema'
                    self.schema.add(name, field)

    def _update_index(self, document, writer, ngram_writer):
        """update or add document"""
        # update or add in main index
        writer.update_document(id=unicode(document.id),
                               title=document.title,
                               space=document.space,
                               content=document.content,
                               last_author=document.last_author,
                               author=document.author,
                               last_update=document.last_update,
                               creation=document.creation)
        # update or add to ngram index
        ngram_writer.update_document(id=unicode(document.id),
                                     title=document.title,
                                     space=document.space,
                                     tag=None)

    def index_document(self, document):
        """index document"""
        with self.ix.writer() as writer, self.\
                ngram_ix.writer() as ngram_writer:
            self._update_index(document, writer, ngram_writer)

    def index_documents(self, documents, clear=False):
        """batch index documents"""
        with AsyncWriter(self.ix) as w, AsyncWriter(self.ngram_ix) as ngw:
            if clear:
                w.mergetype = CLEAR
                ngw.mergetype = CLEAR
            for document in documents:
                self._update_index(document, w, ngw)

    def search(self, query):
        """search on main index"""
        with self.ix.\
                searcher(weighting=scoring.BM25F(title_B=2)) as searcher:
            qp = MultifieldParser(self.search_field,
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
            qp = MultifieldParser(self.ngram_search_field,
                                  schema=self.ngram_ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=25)
            print 'results %r' % results
            results_list = []
            for i, r in enumerate(results):
                print r, i, results.score(i)
                results_list.append({'res': r, 'score': results.score(i)})
            return results, results_list

    def index_document_callback(self, sender, **extra):
        if 'document' in extra:
            self.index_document(extra['document'])
