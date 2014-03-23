# -*- coding: utf-8 -*-

from flask.ext.babel import lazy_gettext as _l
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

from gasoline.models import User


class LoginForm(Form):
    name = TextField(_l(u'Username'),
                     description=_l(u'Username'), validators=[Required()])
    password = PasswordField(_l(u'Password'),
                             description=_l(u'Password'),
                             validators=[Required()])
    remember_me = BooleanField(_l(u'Remember me'),
                               description=_l(u'Remember me'), default=False)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.objects(name=self.name.data).first()
        if user is None:
            self.name.errors.append(_l(u'Username or password mismatch.'))
            return False
        return True
