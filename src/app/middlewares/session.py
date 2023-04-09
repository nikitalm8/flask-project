from flask_sqlalchemy import SQLAlchemy


class SessionMiddleware(object):


    def __init__(self, app: callable, db: SQLAlchemy):

        self.app = app
        self.db = db


    def __call__(self, context: dict, handler: callable):
        
        context['session'] = self.db.session
        return self.app(context, handler)
