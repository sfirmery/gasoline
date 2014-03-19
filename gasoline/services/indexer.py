# -*- coding: utf-8 -*-

import os.path
import logging
from whoosh.fields import SchemaClass
from whoosh.fields import TEXT, KEYWORD, ID, DATETIME, NGRAM, NGRAMWORDS
from whoosh.analysis import StemmingAnalyzer
from whoosh.filedb.filestore import FileStorage
from whoosh import scoring
from whoosh.qparser import MultifieldParser
from whoosh.writing import AsyncWriter, CLEAR

from gasoline.core.signals import event, plugins_registered
from gasoline.services.base import Service

logger = logging.getLogger('gasoline')

__all__ = ['IndexerService', 'MainSchema', 'NGramSchema']


class MainSchema(SchemaClass):
    """Whoosh schema for global indexer"""
    id = ID(stored=True, unique=True)
    doc_id = ID(stored=True)
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

    _plugins_fields_main = {'dyn_1': TEXT(stored=True)}
    _plugins_fields_ngram = {}

    def __init__(self):
        self.schema = MainSchema()
        self.ngram_schema = NGramSchema()
        super(IndexerService, self).__init__()

    def init_app(self, app):
        """intialise indexer with flask configuration"""
        self._open_indexes()
        # update index schema
        self._update_schemas()
        super(IndexerService, self).init_app(app)

    def start(self):
        event.connect(self.index_document_callback, 'document')
        plugins_registered.connect(self.plugins_registered_callback)
        super(IndexerService, self).start()

    def stop(self):
        event.disconnect(self.index_document_callback)
        plugins_registered.disconnect(self.plugins_registered_callback)
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

    def add_plugin_field(self, name, field, searchable=False):
        """add plugin field in main index schema and search field"""
        if name not in self._plugins_fields_main:
            self._plugins_fields_main[name] = field
        if name not in self.search_field and searchable:
            self.search_field.append(name)

    def add_plugin_ngram_field(self, name, field, searchable=False):
        """add plugin field in ngram index schema and ngram search field"""
        if name not in self._plugins_fields_ngram:
            self._plugins_fields_ngram[name] = field
        if name not in self.ngram_search_field and searchable:
            self.ngram_search_field.append(name)

    def _update_schemas(self):
        """update main and ngram schema"""
        # update main schema
        with AsyncWriter(self.ix) as writer:
            for name, field in self.schema.items():
                if name not in self.ix.schema:
                    writer.add_field(name, field)
                    logger.info('field %r added to main index', name)
                elif self.ix.schema[name] != field:
                    logger.error(
                        'field %r exists in main index but is incorrect', name)
            for name, field in self._plugins_fields_main.items():
                if name not in self.ix.schema:
                    writer.add_field(name, field)
                    logger.info('field %r added to main index', name)
                elif self.ix.schema[name] != field:
                    logger.error(
                        'field %r exists in main index but is incorrect', name)
                if name not in self.schema:
                    logger.info('field %r added to main schema', name)
                    self.schema.add(name, field)
        # update ngram schema
        with AsyncWriter(self.ngram_ix) as ngram_writer:
            for name, field in self.ngram_schema.items():
                if name not in self.ngram_ix.schema:
                    writer.add_field(name, field)
                    logger.info('field %r added to ngram index', name)
                elif self.ngram_ix.schema[name] != field:
                    logger.error(
                        'field %r exists in ngram index but is incorrect', name)
            for name, field in self._plugins_fields_ngram.items():
                if name not in self.ngram_ix.schema:
                    logger.info('field %r added to ngram index', name)
                    ngram_writer.add_field(name, field)
                elif self.ngram_ix.schema[name] != field:
                    logger.info('field %r not correct in ngram index', name)
                if name not in self.ngram_schema:
                    logger.info('field %r added to ngram schema', name)
                    self.schema.add(name, field)

    def _update_index(self, document, writer, ngram_writer):
        """update or add document"""
        # update or add in main index
        writer.update_document(id=unicode(document.id),
                               doc_id=unicode(document.id),
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
        """signals callback for indexing document"""
        if 'document' in extra:
            self.index_document(extra['document'])

    def plugins_registered_callback(self, sender, **extra):
        """signals callback for updating schemas when all plugins are
        registered"""
        self._update_schemas()
