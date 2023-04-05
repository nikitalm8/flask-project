from . import (
    home,
)

from flask import Flask


def setup(app: Flask):
    """
    Setup all the views for the app.

    :param Flask app: Flask app instance
    """

    home.setup(app)
