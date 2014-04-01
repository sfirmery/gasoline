# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, render_template, redirect, abort
from flask import flash, url_for, request, Response
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext as _
from mongoengine.fields import GridFSProxy

from gasoline.services import acl_service as acl
from gasoline.forms import BaseDocumentForm, CommentForm
from gasoline.models import BaseDocument, DocumentHistory, Comment
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
    docs = BaseDocument.objects(space=space).limit(50)
    activity = Activity.objects.order_by('-published').limit(50)
    return render_template('dashboard.html', **locals())


@route('/<space>/view/<doc_id>', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def view(space='main', doc_id=None):
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

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(author=current_user._get_current_object(),
                          content=comment_form.content.data)
        doc.add_comment(comment)
        flash(_('Comment added successfully.'), 'info')
        return redirect(url_for('.view', space=space, doc_id=doc.id))
    return render_template('document_view.html', **locals())


@route('/<space>/revision/<doc_id>/<int:revision>', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def revision(space='main', doc_id=None, revision=None):
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

    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(author=current_user._get_current_object(),
                          content=comment_form.content.data)
        doc.add_comment(comment)
        flash(_('Comment added successfully.'), 'info')
        return redirect(url_for('.view', space=space, doc_id=doc.id))
    return render_template('document_view.html', **locals())


@route('/<space>/history/<doc_id>', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def history(space='main', doc_id=None):
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
    return render_template('document_history.html', **locals())


@route('/<space>/attachment/<doc_id>/<file>', methods=['GET', 'POST'])
@acl.acl('read')
@login_required
def attachment(space='main', doc_id=None, file=None):
    try:
        doc = BaseDocument.objects(id=doc_id, space=space).first()
    except:
        doc = None
    if doc is None:
        logger.info('attachment not found %r', doc_id)
        abort(404, _('attachment not found'))
    # check acl for document
    acl.apply('read', doc.acl, _('document'))

    # get attachment
    for attachment in doc.attachments:
        if str(attachment.grid_id) == file:
            break

    # iterator for file streaming
    def generate(file):
        while True:
            try:
                # read 256kB
                chunk = file.read(262144)
            except:
                break
            if len(chunk) < 1:
                break
            yield chunk
    # stream file
    return Response(generate(attachment), mimetype=attachment.contentType)


@route('/<space>/new', methods=['GET', 'POST'])
@route('/<space>/edit/<doc_id>', methods=['GET', 'POST'])
@acl.acl('write')
@login_required
def edit(space='main', doc_id=None):
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
        doc.last_author = current_user._get_current_object()
        doc.save()
        flash(_('Document saved successfully.'), 'info')
        return redirect(url_for('.view', space=space, doc_id=doc.id))
    return render_template('document_edit.html', **locals())


@route('/<space>/upload/<doc_id>', methods=['POST'])
@acl.acl('write')
@login_required
def upload(space='main', doc_id=None):
    print 'enter request'
    if doc_id is None:
        redirect(url_for('.dashboard'))
    else:
        doc = BaseDocument.objects(id=doc_id).first()
        # check acl for document
        acl.apply('write', doc.acl, _('document'))

    print request.files

    file = request.files['upload']
    file_ = GridFSProxy()
    file_.put(file.read(), content_type=file.content_type, filename=file.filename)
    doc.attachments.append(file_)
    doc.save()

    flash(_('File uploaded successfully.'), 'info')
    return redirect(url_for('.view', space=space, doc_id=doc.id))
