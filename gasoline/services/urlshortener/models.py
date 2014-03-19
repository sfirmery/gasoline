# -*- coding: utf-8 -*-

from gasoline.core.extensions import db


class ShortURL(db.Document):
    id = db.IntField(primary_key=True)
    url = db.StringField(unique=True)

    meta = {
        'collection': 'short_url',
        'indexes': ['url'],
    }

    def __repr__(self):
        return '<ShortURL %r>' % (self.id)
