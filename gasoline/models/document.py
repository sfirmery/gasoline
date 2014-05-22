# -*- coding: utf-8 -*-

from datetime import datetime
import markdown2
import mediawiki
from mongoengine.fields import GridFSProxy

from gasoline.core.extensions import db
from gasoline.core.signals import event, activity
from gasoline.core.diff import Diff
from gasoline.services.acl import ACE
from .user import User
from .comment import Comment
from .attachment import Attachment


class DocumentRevision(db.EmbeddedDocument):
    number = db.IntField(primary_key=True, default=1)
    title_diff = db.StringField(default=None)
    space_diff = db.StringField(default=None)
    content_diff = db.StringField(default=None)
    date = db.DateTimeField()
    author = db.ReferenceField(User)

    def __repr__(self):
        return '<DocumentVersion number=%r>' % self.number


class BaseDocument(db.DynamicDocument):
    _title = db.StringField(db_field='title', unique_with='_space')
    _space = db.StringField(db_field='space', default=u'main')
    _content = db.StringField(db_field='content')
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    attachments = db.ListField(db.EmbeddedDocumentField(Attachment))

    acl = db.ListField(db.EmbeddedDocumentField(ACE))

    # document Metadata
    creation = db.DateTimeField(default=datetime.utcnow)
    last_update = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField(User)
    last_author = db.ReferenceField(User)
    current_revision = db.IntField(default=1)
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
            self._next_revision.author = self.last_author

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

    def add_comment(self, comment):
        self.update(push__comments=comment)
        # send activity event
        activity.send(verb='add', object=self, object_type='comment')

    def get_attachment(self, filename):
        """get attached file"""
        # get attachment if exist
        for idx, attachment in enumerate(self.attachments):
            if filename == attachment.filename:
                return attachment.attachment
        # if filename in self.attachments:
        #     print filename
        raise

    def add_attachment(self, file, filename, content_type, user):
        """attach file to document"""
        # update file if already exists
        for idx, attachment in enumerate(self.attachments):
            if filename == attachment.filename:
                # update file in gridfs
                file_ = GridFSProxy(attachment.attachment.grid_id)
                file_.replace(file.read(), content_type=content_type,
                              filename=filename)
                attachment.attachment = file_
                attachment.date = datetime.utcnow
                attachment.author = user
                # update document with new id
                self.update(**({'set__attachments__%s' % idx: attachment}))

                # send activity event
                activity.send(verb='update', object=self, object_type='file')
                return

        # add new file
        file_ = GridFSProxy()
        file_.put(file.read(), content_type=content_type,
                  filename=filename)
        # add file id in document
        attachment = Attachment(filename=filename, attachment=file_,
                                author=user,
                                comment='')
        self.update(push__attachments=attachment)

        # send activity event
        activity.send(verb='attach', object=self, object_type='file')

    def delete_attachment(self, filename):
        """delete attached file from document"""
        for idx, attachment in enumerate(self.attachments):
            if filename == attachment.filename:
                # delete file in gridfs
                file_ = GridFSProxy(attachment.attachment.grid_id)
                file_.delete()
                # delete file in document
                self.update(pull__attachments=attachment)

                # send activity event
                activity.send(verb='delete', object=self, object_type='file')

    def save(self):
        # append revision to history
        if self._next_revision is not None:
            self._get_history()
            self._history.update_one(push__revisions=self._next_revision)
            self.current_revision += 1

        # update metadata
        self.last_update = datetime.utcnow()

        # is a new document ?
        verb = 'update'
        if self.id is None:
            verb = 'create'

        super(BaseDocument, self).save()

        # send document update event
        event.send('document', document=self)

        # send activity event
        activity.send(verb=verb, object=self, object_type='page')

    def __repr__(self):
        return '<BaseDocument id=%s name=%r>' % (self.id, self.title)


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
