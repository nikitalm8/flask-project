from app.database.models import News
from app.utils.login import is_admin
from app.utils.forms import CreateForm, UpdateForm

from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    flash,
    url_for,
    redirect,
    request, 
)

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.future import select


blueprint = Blueprint("news", __name__)

@blueprint.route("/")
def index():

    page = request.args.get('page', 1, type=int)
    pagination = News.query.paginate(page=page, per_page=10)
    
    return render_template(
        "pagination.html", 
        pagination=pagination,
        items=pagination.items,
        News=News,
    )


@blueprint.route("/news/<int:news_id>")
def news(news_id: int):

    session: Session = request.environ['session']
    news = session.scalar(
        select(News)
        .where(News.id == news_id)
    )

    return render_template(
        "news.html", 
        news=news, 
    )


@blueprint.route("/create", methods=["GET", "POST"])
@is_admin
async def create():

    form = CreateForm()

    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Создание поста', 
            form=CreateForm(),
        )

    session: Session = request.environ['session']
    session.add(
        News(
            title=request.form['title'],
            text=request.form['text'],
        )
    )
    session.commit()
    
    return redirect(url_for("news.index"))


@blueprint.route("/edit/<int:id>") 
@is_admin
async def edit(id: int):

    session: Session = request.environ['session']
    news = session.get(News, id)

    if not news:

        flash('Пост не найден!', 'danger')
        return redirect(url_for("news.index"))

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
@is_admin
async def edit_post(id: int):

    session: Session = request.environ['session']
    news = session.get(News, id)

    if not news:

        flash('Пост не найден!', 'danger')
        return redirect(url_for("news.index"))

    news.title = request.form['title']
    news.text = request.form['text']
    session.commit()

    flash('Пост обновлен!', 'success')
    return redirect(url_for("news.index"))


@blueprint.route("/delete/<int:id>", methods=["POST"])
@is_admin
async def delete_news(id: int):

    session: Session = request.environ['session']

    session.execute(
        delete(News)
        .where(News.id == id)
    )
    session.commit()

    flash('Пост удален!', 'success')
    return redirect(url_for("news.index"))


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
