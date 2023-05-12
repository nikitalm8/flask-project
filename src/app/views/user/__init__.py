from . import auth, film#, profile

from flask import Flask


def setup(app: Flask):
    
    auth.setup(app)
    film.setup(app)
    # profile.setup(app)
