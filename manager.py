# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from gasoline import create_app
from gasoline.extensions import db, cache, lm, assets

app = create_app()
manager = Manager(app)


@manager.command
def run(debug=False):
    """run app"""
    app.run(debug=debug)


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


def _make_context():
    return dict(app=app, db=db)

from flask.ext.script import Shell
manager.add_command("shell", Shell(make_context=_make_context))

from flask.ext.assets import ManageAssets
manager.add_command("assets", ManageAssets())

if __name__ == '__main__':
    manager.run()
