# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, render_template
from flask import url_for
from flask.ext.login import login_required


blueprint_index = Blueprint('index', __name__)
route = blueprint_index.route


@route('/')
@login_required
def index():
    """redirect to default dashboard"""
    return redirect(url_for('document.dashboard', space='main'))


@route('/frontend', defaults={'path': ''})
@route('/frontend/', defaults={'path': ''})
@route('/frontend/<path:path>')
def frontend(path):
    return render_template('frontend.html.jinja2')


@route('/marionette', defaults={'path': ''})
@route('/marionette/', defaults={'path': ''})
@route('/marionette/<path:path>')
def marionette(path):
    return render_template('marionette.html.jinja2')
