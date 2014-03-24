# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, render_template, redirect, abort
from flask import flash, url_for
from flask.ext.login import login_required
from flask.ext.babel import gettext as _

from gasoline.services import acl_service as acl
from gasoline.forms import BaseDocumentForm
from gasoline.models import BaseDocument, DocumentHistory, Space
from gasoline.services.activity import Activity

blueprint_document = Blueprint('document',
                               __name__,
                               url_prefix='/document')
route = blueprint_document.route

logger = logging.getLogger('gasoline')


@route('/<space>/dashboard', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def dashboard(space='main'):
    # check acl for space
    # acl.apply('read', Space.objects(name=space).first().acl, _('space'))
    docs = BaseDocument.objects(space=space).limit(50)
    activity = Activity.objects.limit(50)
    return render_template('dashboard.html', **locals())


@route('/<space>/view/<doc_id>', methods=['GET', 'POST'])
@route('/<space>/revision/<doc_id>/<int:revision>', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def view(space='main', doc_id=None, revision=None):
    # check acl for space
    # acl.apply('read', Space.objects(name=space).first().acl, _('space'))
    try:
        doc = BaseDocument.objects(id=doc_id, space=space).first()
    except:
        doc = None
    if doc is None:
        logger.info('document not found %r', doc_id)
        abort(404, _('document not found'))
    # check acl for document
    acl.apply('read', doc.acl, _('document'))
    history = DocumentHistory.objects(document=doc.id).first()
    if revision is not None:
        doc.get_revision(revision)
    return render_template('view_document.html', **locals())


@route('/<space>/new', methods=['GET', 'POST'])
@route('/<space>/edit/<doc_id>', methods=['GET', 'POST'])
@acl.acl('write')
@login_required
def edit(space='main', doc_id=None):
    # check acl for space
    acl.apply('read', Space.objects(name=space).first().acl, _('space'))
    if doc_id is not None:
        doc = BaseDocument.objects(id=doc_id).first()
        # check acl for document
        acl.apply('write', doc.acl, _('document'))
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
