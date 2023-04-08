from . import (
    admin,
    home,
)

from flask import Flask


def setup(app: Flask):
    """
    Setup all the views for the app.

    :param Flask app: Flask app instance
    """

    admin.setup(app)
    home.setup(app)
