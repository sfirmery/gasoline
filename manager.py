# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.script import Manager

from gasoline import create_app
from gasoline.core import extensions

app = create_app()
manager = Manager(app)


@manager.command
def run(debug=False):
    """run app"""
    app.run(debug=debug, host='0.0.0.0')


@manager.command
def initdb():
    from gasoline.frontend import BaseDocument
    from gasoline.user import User

    user = User(name='doe')
    user.set_password('pass')
    user.save()

    import wikipedia

    for article in ['Wiki', 'Collaboration', 'Team']:
        article = wikipedia.page(article)
        new_doc = BaseDocument(title=article.title,
                               content=article.content)
        new_doc.save()


@manager.command
def reindex(clear=False):
    """Reindex documents"""
    from gasoline.frontend.models import BaseDocument

    indexer = current_app.services['indexer']
    documents = BaseDocument.objects.all()

    if clear:
        print "*" * 80
        print "WILL CLEAR INDEX BEFORE REINDEXING"
        print "*" * 80
    indexer.index_documents(documents, clear)


def _make_context():
    return dict(app=app, db=extensions.db)

from flask.ext.script import Shell
manager.add_command("shell", Shell(make_context=_make_context))

from flask.ext.assets import ManageAssets
manager.add_command("assets", ManageAssets())

if __name__ == '__main__':
    manager.run()
