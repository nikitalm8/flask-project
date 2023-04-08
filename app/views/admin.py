from app.database.models import News

from flask import Flask, Blueprint, request, render_template, redirect, flash
from flask_wtf import FlaskForm
from wtforms import fields, validators

from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class NewsForm(FlaskForm):

    title = fields.StringField(label='Название статьи', validators=[validators.DataRequired()])
    text = fields.TextAreaField(label='Текст статьи', validators=[validators.DataRequired()])

class CreateForm(NewsForm):

    submit = fields.SubmitField(label='Создать')

class UpdateForm(NewsForm):

    submit = fields.SubmitField(label='Обновить')


blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
async def index():

    session: AsyncSession = request.environ['session']
    page = request.args.get('page', 1, type=int)

    pagination = await News.paginate(session, page, 10)
    
    return render_template(
        "pagination.html", 
        pagination=pagination,
        items=pagination.items,
        News=News,
    )


@blueprint.route("/create")
async def create():

    return render_template(
        "form.html", 
        title='Создание поста', 
        form=CreateForm(),
    )


@blueprint.route("/create", methods=["POST"])
async def create_post():

    session: AsyncSession = request.environ['session']

    session.add(
        News(
            title=request.form['title'],
            text=request.form['text'],
        )
    )
    await session.commit()
    
    return redirect("/admin")


@blueprint.route("/edit/<int:id>")  
async def edit(id: int):

    session: AsyncSession = request.environ['session']
    news = await session.get(News, id)

    if not news:

        flash('Пост не найден!', 'danger')
        return redirect("/admin")

    form = UpdateForm(
        title=news.title,
        text=news.text,
    )
    return render_template(
        "form.html",
        title='Редактирование поста',
        form=form,
    )


@blueprint.route("/edit/<int:id>", methods=["POST"])
async def edit_post(id: int):

    session: AsyncSession = request.environ['session']
    news = await session.get(News, id)

    if not news:

        flash('Пост не найден!', 'danger')
        return redirect("/admin")

    news.title = request.form['title']
    news.text = request.form['text']
    await session.commit()

    flash('Пост обновлен!', 'success')
    return redirect("/admin")


@blueprint.route("/delete/<int:id>", methods=["POST"])
async def delete_get(id: int):

    session: AsyncSession = request.environ['session']

    await session.execute(
        delete(News)
        .where(News.id == id)
    )
    await session.commit()

    flash('Пост удален!', 'success')
    return redirect("/admin")


def setup(app: Flask):
    """
    Setup all the views for admin.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
