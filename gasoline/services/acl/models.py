# -*- coding: utf-8 -*-

from gasoline.core.extensions import db

TRUTH = ['DENY', 'ALLOW']


class ACE(db.EmbeddedDocument):
    truth = db.StringField(unique_with=['predicate'],
                           choices=TRUTH, default=TRUTH[0])
    predicate = db.StringField()
    permission = db.ListField(db.StringField())

    def __repr__(self):
        return '<ACE "%s %s %s">' % (
            self.truth, self.predicate, self.permission)
