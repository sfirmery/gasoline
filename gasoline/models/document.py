# -*- coding: utf-8 -*-

from datetime import datetime
import markdown2
import mediawiki

from gasoline.core.extensions import db
from gasoline.core.signals import event
from gasoline.core.diff import Diff

from .user import User


class DocumentRevision(db.EmbeddedDocument):
    number = db.IntField(primary_key=True, default=0)
    title_diff = db.StringField(default=None)
    space_diff = db.StringField(default=None)
    content_diff = db.StringField(default=None)
    date = db.DateTimeField()

    def __repr__(self):
        return '<DocumentVersion number=%s>' % (self.number)


class BaseDocument(db.DynamicDocument):
    _title = db.StringField(db_field='title', unique_with='_space')
    _space = db.StringField(db_field='space', default=u'root')
    _content = db.StringField(db_field='content')

    # document Metadata
    creation = db.DateTimeField(default=datetime.utcnow)
    last_update = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField(User)
    last_author = db.ReferenceField(User)
    current_revision = db.IntField(default=0)
    markup = db.StringField(default=u'xhtml')

    meta = {
        'indexes': ['title', 'space']
    }

    _history = None
    _next_revision = None
    _diff = None

    def _get_history(self):
        # get history document or create it
        if self._history is None:
            self._history = DocumentHistory.objects(document=self.id)
            if len(self._history) == 0:
                history = DocumentHistory(document=self)
                history.save()
                self._history = DocumentHistory.objects(document=self)

    def _get_next_revision(self):
        # create new revision if not exist
        if self._next_revision is None:
            self._next_revision = DocumentRevision()
            self._next_revision.date = self.last_update
            self._next_revision.number = self.current_revision

    def _get_diff(self):
        # get diff object
        if self._diff is None:
            self._diff = Diff()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if self._title is not None:
            self._get_next_revision()
            self._get_diff()

            # compute title diff
            title_patches = self._diff.patch_make(title, self.title)
            if len(title_patches) > 0:
                self._next_revision.\
                    title_diff = self._diff.patch_toText(title_patches)
        self._title = title

    @property
    def space(self):
        return self._space

    @space.setter
    def space(self, space):
        if self._space is not None:
            self._get_next_revision()
            self._get_diff()

            # compute space diff
            space_patches = self._diff.patch_make(space, self.space)
            if len(space_patches) > 0:
                self._next_revision.\
                    space_diff = self._diff.patch_toText(space_patches)
        self._space = space

    @property
    def content_html(self):
        if self.markup == 'xhtml':
            return self.content
        elif self.markup == 'mediawiki':
            return mediawiki.wiki2html(self.content, True)
        else:
            return markdown2.markdown(self.content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if self._content is not None:
            self._get_next_revision()
            self._get_diff()

            # compute content diff
            content_patches = self._diff.patch_make(content, self.content)
            if len(content_patches) > 0:
                self._next_revision.\
                    content_diff = self._diff.patch_toText(content_patches)
        self._content = content

    def get_revision(self, revision_number):
        self._get_diff()
        self._get_history()
        history = self._history.first()
        # patch content for each revisions
        for revision in reversed(history.revisions):
            # break if requested revision
            if revision.number < revision_number:
                break
            # apply title patch
            if revision.title_diff is not None:
                title_patches = self._diff.\
                    patch_fromText(revision.title_diff)
                self._title = self._diff.\
                    patch_apply(title_patches, self.title)[0]
            # apply space patch
            if revision.space_diff is not None:
                space_patches = self._diff.\
                    patch_fromText(revision.space_diff)
                self._space = self._diff.\
                    patch_apply(space_patches, self.space)[0]
            # apply content patch
            if revision.content_diff is not None:
                content_patches = self._diff.\
                    patch_fromText(revision.content_diff)
                self._content = self._diff.\
                    patch_apply(content_patches, self.content)[0]
            self.current_revision = revision.number
            self.last_update = revision.date

    def save(self):
        # append revision to history
        if self._next_revision is not None:
            self._get_history()
            self._history.update_one(push__revisions=self._next_revision)
            self.current_revision = self.current_revision + 1

        # update metadata
        self.last_update = datetime.utcnow()

        super(BaseDocument, self).save()

        # send document update evetn
        event.send('document', document=self)

    def __repr__(self):
        return '<BaseDocument id=%s name=%s>' % (self.id, self.title)


class DocumentHistory(db.Document):
    document = db.ReferenceField(BaseDocument)
    revisions = db.SortedListField(db.EmbeddedDocumentField(DocumentRevision))

    meta = {
        'indexes': ['document', 'revisions._id']
    }

    @property
    def reverse_revisions(self):
        return reversed(self.revisions)

    def __repr__(self):
        return '<DocumentHistory document=%r>' % (self.document)
