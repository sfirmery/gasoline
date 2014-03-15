# -*- coding: utf-8 -*-

from flask.ext.babel import lazy_gettext as _
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required, Length

from .models import User


class LoginForm(Form):
    name = TextField(_(u'Username'),
                     description=_(u'Username'), validators=[Required()])
    password = PasswordField(_(u'Password'),
                             description=_(u'Password'), validators=[Required()])
    remember_me = BooleanField(_(u'Remember me'),
                               description=_(u'Remember me'), default=False)

    def validate(self):
        if not Form.validate(self):
            return False
        user = User.objects(name=self.name.data).first()
        if user is None:
            self.name.errors.append(_('Username or password mismatch.'))
            return False
        return True
