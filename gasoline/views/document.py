# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, render_template, redirect, abort
from flask import flash, url_for
from flask.ext.login import login_required
from flask.ext.babel import gettext as _

from gasoline.services import acl_service as acl
from gasoline.forms import BaseDocumentForm
from gasoline.models import BaseDocument, DocumentHistory, Space

blueprint_document = Blueprint('document',
                               __name__,
                               url_prefix='/document')
route = blueprint_document.route

logger = logging.getLogger('gasoline')


@route('/<space>/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard(space='main'):
    docs = BaseDocument.objects.limit(50)
    return render_template('dashboard.html', **locals())


@route('/<space>/view/<doc_id>', methods=['GET', 'POST'])
@route('/<space>/revision/<doc_id>/<int:revision>', methods=['GET', 'POST'])
@login_required
def view(space='main', doc_id=None, revision=None):
    if not acl.can('read', space=Space.objects(name=space).first()):
        abort(403)
    try:
        doc = BaseDocument.objects(id=doc_id, space=space).first()
        print 'doc %r' % doc
        history = DocumentHistory.objects(document=doc.id).first()
    except:
        logger.info('document not found %r', doc_id)
        abort(404)
    if revision is not None:
        doc.get_revision(revision)
    return render_template('view_document.html', **locals())


@route('/<space>/new', methods=['GET', 'POST'])
@route('/<space>/edit/<doc_id>', methods=['GET', 'POST'])
@login_required
def edit(space='main', doc_id=None):
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
        return redirect(url_for('.view', space=space, doc_id=doc.id))
    return render_template('edit_document.html', **locals())
