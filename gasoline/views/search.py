# -*- coding: utf-8 -*-

from time import sleep
from flask import Blueprint, render_template
from flask import request, current_app, g
from flask.ext.login import login_required

blueprint_search = Blueprint('search', __name__)
route = blueprint_search.route


@route('/search')
@route('/search/<query>')
@login_required
def search(query=None):
    if query is None:
        query = request.args.get('query', '')
    g.search_form.query.data = query
    results = current_app.services['indexer'].search(query)
    return render_template('search_results.html', results=results)

from flask import jsonify


@route('/api/search')
@login_required
def api_search(query=None):
    if query is None:
        query = request.args.get('query', '')
    g.search_form.query.data = query
    results = current_app.services['indexer'].search(query)
    return jsonify(results=results)


@route('/api/quick_search')
@login_required
def api_quick_search(query=None):
    if query is None:
        query = request.args.get('query', '')
    g.search_form.query.data = query
    results = current_app.services['indexer'].live_search(query)
    sleep(1)
    return jsonify(results=results)
