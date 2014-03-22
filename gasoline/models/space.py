# -*- coding: utf-8 -*-

from gasoline.core.extensions import db
from gasoline.services.acl import ACE


class Space(db.Document):
    name = db.StringField(primary_key=True)
    acl = db.ListField(db.EmbeddedDocumentField(ACE))

    def __repr__(self):
        return '<Space name=%s>' % (self.name)
