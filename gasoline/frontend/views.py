# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect
from flask import url_for, flash
from flask.ext.login import login_required

from .models import BaseDocument, DocumentHistory
from .forms import BaseDocumentForm
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


@route('/document/edit/<doc_id>', methods=['GET', 'POST'])
@login_required
def edit_document(doc_id=None):
    doc = BaseDocument.objects(id=doc_id).first()
    form = BaseDocumentForm(obj=doc)
    if form.validate_on_submit():
        updated = False
        if form.title.data != doc.title:
            doc.title = form.title.data
            updated = True
        if form.content.data != doc.content:
            doc.content = form.content.data
            updated = True
        # if updated:
        if True:
            doc.save()
        else:
            flash("no modification", 'warning')

        return redirect(url_for('.view_document', doc_id=doc_id))

    return render_template('edit_document.html', **locals())


@route('/search')
def search():
    return redirect(url_for('.index'))
