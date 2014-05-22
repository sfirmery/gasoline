# -*- coding: utf-8 -*-

from datetime import datetime
# from mongoengine.fields import GridFSProxy

from gasoline.core.extensions import db
# from gasoline.core.signals import event, activity
from .user import User


class Attachment(db.EmbeddedDocument):
    filename = db.StringField(primary_key=True)
    attachment = db.FileField()

    date = db.DateTimeField(default=datetime.utcnow)
    author = db.ReferenceField(User)
    comment = db.StringField()

    def __repr__(self):
        return '<Attachment filename=%r>' % self.filename
