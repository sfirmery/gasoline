# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect
from flask import url_for, request, current_app
from flask.ext.login import login_required

from gasoline.models import BaseDocument


blueprint_dashboard = Blueprint('dashboard', __name__)
route = blueprint_dashboard.route


@route('/')
def index():
    """redirect to default dashboard"""
    return redirect(url_for('.dashboard'))


@route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    docs = BaseDocument.objects.limit(50)
    return render_template('dashboard.html', **locals())


@route('/search')
@route('/search/<query>')
@login_required
def search(query=None):
    if query is None:
        query = request.args.get('query', '')
    results, results_list = current_app.services['indexer'].search(query)
    return render_template('search_results.html', **locals())
