from . import (
    admin,
    auth,
    news,
    user,
)

from flask import Flask


def setup(app: Flask):
    """
    Setup all the views for the app.

    :param Flask app: Flask app instance
    """

    admin.setup(app)
    auth.setup(app)
    news.setup(app)
    user.setup(app)
