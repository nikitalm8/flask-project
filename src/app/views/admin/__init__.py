from . import category, users, news

from flask import Flask


def setup(app: Flask):
    
    users.setup(app)
    category.setup(app)
    news.setup(app)
