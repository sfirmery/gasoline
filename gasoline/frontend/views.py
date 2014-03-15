# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect
from flask import url_for, flash, request
from flask.ext.login import login_required
from flask.ext.babel import gettext as _

from .models import BaseDocument, DocumentHistory
from .forms import BaseDocumentForm
from ..search_engine import indexer

# from .constants import DEFAULT_SPACE

frontend = Blueprint('frontend',
                     __name__,
                     template_folder='templates')
route = frontend.route


@route('/')
def index():
    """redirect to default dashboard"""
    return redirect(url_for('.dashboard'))


@route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    docs = BaseDocument.objects
    return render_template('dashboard.html', **locals())


@route('/document/view/<doc_id>', methods=['GET', 'POST'])
@route('/document/revision/<doc_id>/<int:revision>', methods=['GET', 'POST'])
@login_required
def view_document(doc_id=None, revision=None):
    doc = BaseDocument.objects(id=doc_id).first()
    history = DocumentHistory.objects(document=doc.id).first()
    if revision is not None:
        doc.get_revision(revision)
    return render_template('view_document.html', **locals())


@route('/document/new', methods=['GET', 'POST'])
@route('/document/edit/<doc_id>', methods=['GET', 'POST'])
@login_required
def edit_document(doc_id=None):
    if doc_id is not None:
        doc = BaseDocument.objects(id=doc_id).first()
    else:
        doc = BaseDocument()
    form = BaseDocumentForm(obj=doc)
    if form.validate_on_submit():
        if form.title.data != doc.title:
            doc.title = form.title.data
        if form.content.data != doc.content:
            doc.content = form.content.data
        doc.save()
        flash(_('Document saved successfuly.'), 'info')
        return redirect(url_for('.view_document', doc_id=doc.id))
    return render_template('edit_document.html', **locals())


@login_required
def new_document():
    doc = BaseDocument()
    form = BaseDocumentForm()
    if form.validate_on_submit():
        if form.title.data != doc.title:
            doc.title = form.title.data
        if form.content.data != doc.content:
            doc.content = form.content.data
        doc.save()
        flash(_('Document saved successfuly.'), 'info')
        return redirect(url_for('.view_document', doc_id=doc.id))
    return render_template('edit_document.html', **locals())


@route('/search')
@route('/search/<query>')
@login_required
def search(query=None):
    if query is None:
        query = request.args.get('query', '')
    results, results_list = indexer.search(query)
    return render_template('search_results.html', **locals())
