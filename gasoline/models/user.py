# -*- coding: utf-8 -*-

from werkzeug import generate_password_hash, check_password_hash

from gasoline.core.extensions import db


class User(db.Document):
    name = db.StringField(primary_key=True)
    password = db.StringField()

    def __repr__(self):
        return '<User %r>' % (self.name)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.name)
