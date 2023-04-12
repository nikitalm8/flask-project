from . import auth, news, profile

from flask import Flask


def setup(app: Flask):
    
    auth.setup(app)
    news.setup(app)
    profile.setup(app)
