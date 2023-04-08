import aiofiles
import random

from app.database.models import News

from flask import Flask, Blueprint, request, render_template, url_for

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


blueprint = Blueprint("home", __name__)

@blueprint.route("/")
async def index():

    return "Hello, World!"


@blueprint.route("/random")
async def random_saying():
    
    async with aiofiles.open("app/static/random.txt") as file:
        
        lines = await file.readlines()
        return random.choice(lines)


@blueprint.route("/news")
async def news():

    session: AsyncSession = request.environ['session']
    posts = await session.scalars(select(News))

    return render_template("list.html", news_list=posts)


@blueprint.route("/news/<int:id>")
async def post(id):

    session: AsyncSession = request.environ['session']
    post = await session.get(News, id)

    if not post:

        return "Post not found", 404

    return render_template("news.html", news=post)


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
