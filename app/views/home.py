import aiofiles
import random

from flask import Flask, Blueprint


blueprint = Blueprint("home", __name__)

@blueprint.route("/")
async def index():

    return "Hello, World!"


@blueprint.route("/random")
async def random_saying():
    
    async with aiofiles.open("app/static/random.txt") as file:
        
        lines = await file.readlines()
        return random.choice(lines)


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
