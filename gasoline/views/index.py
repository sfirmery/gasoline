# -*- coding: utf-8 -*-

from flask import Blueprint, render_template


blueprint_index = Blueprint('index', __name__)
route = blueprint_index.route


@route('/', defaults={'path': ''})
@route('/<path:path>')
def index(path):
    return render_template('index.html.jinja2')
