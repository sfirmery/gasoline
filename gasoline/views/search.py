# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from flask import request, current_app
from flask.ext.login import login_required

blueprint_search = Blueprint('search', __name__)
route = blueprint_search.route


@route('/search')
@route('/search/<query>')
@login_required
def search(query=None):
    if query is None:
        query = request.args.get('query', '')
    results, results_list = current_app.services['indexer'].search(query)
    return render_template('search_results.html', **locals())
