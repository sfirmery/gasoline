# -*- coding: utf-8 -*-

from flask import Blueprint, redirect, url_for, current_app

blueprint_urlshortener = Blueprint('urlshortener', __name__)
route = blueprint_urlshortener.route


@route('/u/<short_url>')
def urlshortener(short_url=None):
    url = current_app.services['urlshortener'].extend(short_url)
    if url is None:
        return redirect(url_for('dashboard.index'))
    print url
    return redirect(url)
