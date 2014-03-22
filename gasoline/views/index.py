# -*- coding: utf-8 -*-

from flask import Blueprint, redirect
from flask import url_for
from flask.ext.login import login_required


blueprint_index = Blueprint('index', __name__)
route = blueprint_index.route


@route('/')
@login_required
def index():
    """redirect to default dashboard"""
    return redirect(url_for('document.dashboard', space='main'))
