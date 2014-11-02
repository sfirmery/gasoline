# -*- coding: utf-8 -*-

from datetime import datetime
import markdown2
import mediawiki
from mongoengine.fields import GridFSProxy
from bson.objectid import ObjectId

from gasoline.core.utils import genid
from gasoline.core.extensions import db
from gasoline.core.signals import event, activity
from gasoline.core.diff import Diff
from gasoline.services.acl import ACE
from .space import Space
from .user import User, json_schema_resource as json_schema_user
from .comment import Comment, json_schema_collection as json_schema_comments
from .attachment import (
    Attachment, json_schema_resource as json_schema_attachment)

rest_uri_collection = '/api/v1/documents/<space>'
rest_uri_resource = '{}/<doc_id>'.format(rest_uri_collection)

json_schema_resource = {
    'title': 'Document resource Schema',
    'type': 'object',
    'required': ['space', 'title', 'author'],
    'properties': {
        '_id': {'type': 'string'},
        'title': {'type': 'string'},
        'space': {'type': 'string'},
        'content': {'type': 'string'},
        'tags': {
            'type': 'array',
            'items': {
                'title': 'Tag schema',
                'type': 'string'
            },
        },
        # 'comments': json_schema_comments,
        'attachments': {
            'type': 'array',
            'items': json_schema_attachment,
        },
        'creation': {'type': 'string'},
        'last_update': {'type': 'string'},
        'author': json_schema_user,
        'last_author': json_schema_user,
        'current_revision': {'type': 'integer'},
        'uri': {'type': 'string'},
    },
}

json_schema_collection = {
    'title': 'Documents collection Schema',
    'type': 'array',
    'minItems': 1,
    'items': json_schema_resource,
}


class DocumentRevision(db.EmbeddedDocument):
    number = db.IntField(primary_key=True, default=1)
    title_diff = db.StringField(default=None)
    space_diff = db.StringField(default=None)
    content_diff = db.StringField(default=None)
    date = db.DateTimeField()
    author = db.ReferenceField(User)

    def __repr__(self):
        return '<DocumentVersion number=%r>' % self.number


class BaseDocumentQuerySet(db.QuerySet):

    def get_document(self, doc):
        if ObjectId.is_valid(doc):
            return self.filter(id=doc)
        else:
            return self.filter(title=doc)


class BaseDocument(db.DynamicDocument):
    _title = db.StringField(db_field='title', unique_with='_space')
    _space = db.StringField(db_field='space', default=u'main')
    # _space = db.ReferenceField(Space, db_field='space', default=u'main')
    _content = db.StringField(db_field='content')
    tags = db.ListField(db.StringField())
    # comments = db.DictField(field=db.EmbeddedDocumentField(Comment))
    # comments = db.SortedListField(
    #     db.EmbeddedDocumentField('Comment'),
    #     ordering='date')
    # comments = db.ListField(db.ReferenceField(Comment))
    attachments = db.ListField(db.EmbeddedDocumentField(Attachment))

    acl = db.ListField(db.EmbeddedDocumentField(ACE))

    # document Metadata
    creation = db.DateTimeField(default=datetime.utcnow)
    last_update = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField(User, required=True)
    last_author = db.ReferenceField(User)
    current_revision = db.IntField(default=1)
    markup = db.StringField(default=u'xhtml')

    meta = {
        'indexes': ['title', 'space'],
        'queryset_class': BaseDocumentQuerySet,
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
    def uri(self):
        return rest_uri_resource.\
            replace("<space>", self.space).\
            replace("<doc_id>", unicode(self.id))

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
        # return self._content
        if self.markup == 'xhtml':
            return self._content
        elif self.markup == 'mediawiki':
            return mediawiki.wiki2html(self._content, True)
        else:
            return markdown2.markdown(self._content)

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

    @property
    def comments(self):
        return Comment.objects().all()

    def get_comment(self, comment_id):
        # for i, comment in enumerate(self.comments):
        #     if comment.id == comment_id:
        #         return self.comments[i]
        # raise
        return Comment.objects(doc=self, id=comment_id).first()

    def get_comments(self):
        return Comment.objects(doc=self).all()

    def add_comment(self, comment):
        comment.doc = self
        comment.save()

        # # send activity event
        # activity.send(verb='add', object=self, object_type='comment')

    def update_comment(self, comment):
        comment.doc = self
        comment.save()

        # # send activity event
        # activity.send(verb='edit', object=self, object_type='comment')

    def delete_comment(self, comment):
        comment.delete()

        # # send activity event
        # activity.send(verb='delete', object=self, object_type='comment')

    def get_attachment(self, filename):
        """get attached file"""
        # get attachment if exist
        for idx, attachment in enumerate(self.attachments):
            if filename == attachment.filename:
                return attachment.attachment
        # if filename in self.attachments:
        #     print filename
        raise BaseException

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
                return
        raise BaseException

    def get_tag(self, tag):
        """update tag"""
        if tag in self.tags:
            return tag
        raise BaseException

    def add_tag(self, tag):
        """add tag if necessary"""
        if tag not in self.tags:
            self.update(push__tags=tag)
            # send document update event
            event.send('document', document=self)
            # send activity event
            activity.send(verb='add', object=self, object_type='tag')
        else:
            raise BaseException

    def update_tag(self, old_tag, new_tag):
        """update tag"""
        self.delete_tag(old_tag)
        self.add_tag(new_tag)

    def delete_tag(self, tag):
        """remove tag"""
        if tag in self.tags:
            self.update(pull__tags=tag)
            # send document update event
            event.send('document', document=self)
            # send activity event
            activity.send(verb='remove', object=self, object_type='tag')
        else:
            raise BaseException

    def clean(self):
        # append revision to history
        if self._next_revision is not None:
            self._get_history()
            self._history.update_one(push__revisions=self._next_revision)
            self.current_revision += 1

        # update metadata
        self.last_update = datetime.utcnow()

        if self.last_author is None:
            self.last_author = self.author

    def save(self, *args, **kwargs):
        # is a new document ?
        verb = 'update'
        if self.id is None:
            verb = 'create'

        super(BaseDocument, self).save(*args, **kwargs)

        # # send document update event
        # event.send('document', document=self)
        # # send activity event
        # activity.send(verb=verb, object=self, object_type='page')

    def to_rest(self):
        """return document in rest friendly format"""
        rest = dict()
        rest['_id'] = self.id
        rest['space'] = self.space
        rest['title'] = self.title
        if self._content is not None:
            rest['content'] = self.content_html
        if len(self.tags) > 0:
            rest['tags'] = self.tags
        if len(self.comments) > 0:
            rest['comments'] = self.comments
        if len(self.attachments) > 0:
            rest['attachments'] = self.attachments
        rest['creation'] = self.creation
        rest['last_update'] = self.last_update
        rest['author'] = self.author
        rest['last_author'] = self.last_author
        rest['current_revision'] = self.current_revision
        rest['uri'] = self.uri
        return rest

    def __repr__(self):
        return '<BaseDocument id=%s name=%r>' % (self.id, self.title)

    def __str__(self):
        return unicode(self.id)


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
