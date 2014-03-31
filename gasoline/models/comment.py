# -*- coding: utf-8 -*-

from datetime import datetime
import markdown2

from gasoline.core.extensions import db
from gasoline.core.signals import event, activity
from .user import User


class Comment(db.EmbeddedDocument):
    author = db.ReferenceField(User)
    date = db.DateTimeField(default=datetime.utcnow)
    content = db.StringField()

    reply = db.ListField(db.EmbeddedDocumentField("Comment"))

    def __repr__(self):
        return '<Comment author=%s>' % self.author
