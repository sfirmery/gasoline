# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, flash, redirect, session
from flask import url_for, request
from flask.ext.babel import gettext as _, ngettext as n_
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required

from gasoline.models import User
from gasoline.forms import LoginForm

blueprint_user = Blueprint('user',
                           __name__,
                           url_prefix='/user')

route = blueprint_user.route


@route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated():
        return redirect(url_for('dashboard.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(name=form.name.data).first()
        if user.check_password(form.password.data):
            session['remember_me'] = form.remember_me.data
            login_user(user, remember=session['remember_me'])
            flash(_('Logged in successfully.'), 'success')
            return redirect(request.args.get("next") or
                            url_for('dashboard.index'))

        flash(_('Logging failed.'), 'danger')
        return redirect(url_for('dashboard.login'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@route('/logout')
def logout():
    logout_user()
    return redirect(url_for('dashboard.index'))


@route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
    user = User.objects(name=name).first()
    if user is None:
        flash(n_('User %(name) not found.', name), 'danger')
        return redirect(url_for('dashboard.index'))
    return render_template('profile.html', **locals())
