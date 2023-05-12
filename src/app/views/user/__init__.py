from . import auth, film

from flask import Flask


def setup(app: Flask):
    
    auth.setup(app)
    film.setup(app)
