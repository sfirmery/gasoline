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
from gasoline.services.indexer.model import SearchResults

logger = logging.getLogger('gasoline')

__all__ = ['IndexerService', 'IndexerSchema']


class IndexerSchema(SchemaClass):
    """Whoosh schema for global indexer"""
    id = ID(stored=True, unique=True)
    doc_id = ID(stored=True)
    doc_type = KEYWORD(stored=True)
    title = TEXT(stored=True)
    space = KEYWORD(stored=True)
    content = TEXT(analyzer=StemmingAnalyzer())
    tags = KEYWORD(stored=True)

    # document metadata
    author = KEYWORD()
    last_author = KEYWORD(stored=True)
    creation = DATETIME()
    last_update = DATETIME(stored=True)

    # ngram fields for live search
    ngram_title = NGRAM(minsize=2, maxsize=10)
    ngram_space = NGRAMWORDS(minsize=2, maxsize=10)
    ngram_tags = NGRAMWORDS(minsize=2, maxsize=10)

_default_search_field = ['title', 'space', 'content', 'tags']
_default_live_search_field = ['ngram_title', 'ngram_space', 'ngram_tags']


class IndexerService(Service):
    """Whoosh Indexer service"""
    name = 'indexer'

    ix = None
    schema = None
    search_field = _default_search_field
    live_search_field = _default_live_search_field

    _plugins_fields = {'dyn_1': TEXT(stored=True)}

    def __init__(self):
        self.schema = IndexerSchema()
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

        # open or initialise index
        if not storage.index_exists(indexname='MAIN'):
            self.ix = storage.\
                create_index(IndexerSchema, indexname='MAIN')
        self.ix = storage.open_index(indexname='MAIN')

    def add_plugin_field(self, name, field, searchable=False):
        """add plugin field in main index schema and search field"""
        if name not in self._plugins_fields:
            self._plugins_fields[name] = field
        if name not in self.search_field and searchable:
            self.search_field.append(name)

    def _update_schemas(self, force=False):
        """update indexer schema"""
        # with an async writer
        with AsyncWriter(self.ix) as writer:
            # check index schema
            for name, field in self.schema.items():
                if name not in self.ix.schema:
                    writer.add_field(name, field)
                    logger.info('field %r added to main index', name)
                elif self.ix.schema[name] != field:
                    if force:
                        writer.remove_field(name)
                        writer.add_field(name, field)
                        logger.info('field %r recreated in main index', name)
                    else:
                        logger.error('field %r exists in main index but is\
 incorrect', name)
            # check plugins fields
            for name, field in self._plugins_fields.items():
                if name not in self.ix.schema:
                    writer.add_field(name, field)
                    logger.info('field %r added to main index', name)
                elif self.ix.schema[name] != field:
                    if force:
                        writer.remove_field(name)
                        writer.add_field(name, field)
                        logger.info('field %r recreated in main index', name)
                    else:
                        logger.error('field %r exists in main index but is\
 incorrect', name)
                if name not in self.schema:
                    logger.info('field %r added to main schema', name)
                    self.schema.add(name, field)

    def _update_index(self, document, writer):
        """update or add document"""
        doc_id = unicode(document.id)
        writer.update_document(id=doc_id,
                               doc_id=doc_id,
                               title=document.title,
                               space=document.space,
                               content=document.content,
                               tags=u' '.join(document.tags),
                               last_author=document.last_author.id,
                               author=document.author.id,
                               last_update=document.last_update,
                               creation=document.creation,
                               ngram_title=document.title,
                               ngram_space=document.space,
                               ngram_tags=u' '.join(document.tags))

    def index_document(self, document):
        """index document"""
        with self.ix.writer() as writer:
            self._update_index(document, writer)

    def index_documents(self, documents, clear=False):
        """batch index documents"""
        if clear:
            self._update_schemas(force=True)
        with AsyncWriter(self.ix) as writer:
            if clear:
                writer.mergetype = CLEAR
            for document in documents:
                self._update_index(document, writer)

    def search(self, query):
        """search on main index"""
        with self.ix.\
                searcher(weighting=scoring.BM25F(title_B=2)) as searcher:
            qp = MultifieldParser(self.search_field,
                                  schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=15).copy()

            return SearchResults(results)

    def live_search(self, query):
        """live search on ngram field"""
        with self.ix.\
                searcher(weighting=scoring.BM25F(title_B=2)) as searcher:
            qp = MultifieldParser(self.live_search_field + self.search_field,
                                  schema=self.ix.schema)
            q = qp.parse(query)
            results = searcher.search(q, limit=15).copy()

            return SearchResults(results)

    def index_document_callback(self, sender, **extra):
        """signals callback for indexing document"""
        if 'document' in extra:
            self.index_document(extra['document'])

    def plugins_registered_callback(self, sender, **extra):
        """signals callback for updating schemas when all plugins are
        registered"""
        self._update_schemas()
