from . import films

from flask import Flask


def setup(app: Flask):

    films.setup(app)
