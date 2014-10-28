# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session, redirect
from flask.ext.login import current_user
from flask.ext.login import login_user, logout_user

from gasoline.models import User
from gasoline.forms import LoginForm

blueprint_index = Blueprint('index', __name__)
route = blueprint_index.route


@route('/', defaults={'path': ''})
@route('/<path:path>')
def index(path):
    if current_user is None or not current_user.is_authenticated():
        return redirect('/sign_in')

    return render_template('index.html.jinja2')


@route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user is not None and current_user.is_authenticated():
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(name=form.name.data).first()
        if user.check_password(form.password.data):
            session['remember_me'] = form.remember_me.data
            login_user(user, remember=session['remember_me'])
            return redirect('/')

        return redirect('/sign_in')

    return render_template('sign_in.html.jinja2', form=form)


@route('/sign_out', methods=['GET', 'POST'])
def sign_out():
    if current_user is None or not current_user.is_authenticated():
        return redirect('/sign_in')

    logout_user()

    return redirect('/')
