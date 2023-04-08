from .session import SessionMiddleware

from flask import Flask

from sqlalchemy.orm import sessionmaker


def setup(app: Flask, sessionmaker: sessionmaker):
    """
    Setup all the middleware for the app.
    :param Flask app: Flask app instance
    """

    app.wsgi_app = SessionMiddleware(app.wsgi_app, sessionmaker)
