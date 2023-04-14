from app.database.models import News, Category, AssignedCategory
from app.utils.login import LevelChecker
from app.utils.forms import UpdateForm, CreateForm

from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    redirect, 
    flash,
    url_for,
    request, 
)

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.future import select


blueprint = Blueprint("admin_news", __name__, url_prefix="/admin/news")
blueprint.before_request(LevelChecker(1))


@blueprint.route("/")
def index():

    page = request.args.get('page', 1, type=int)
    pagination = News.query.order_by(News.created_at.desc()).paginate(page=page, per_page=10)

    return render_template(
        "admin_news.html", 
        pagination=pagination,
        items=pagination.items,
        News=News,
    )


@blueprint.route("/create", methods=["GET", "POST"])
def create():

    form = CreateForm()
    form.categories.choices = [
        (category.id, category.title) 
        for category in Category.query.all()
    ]
    
    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Создание поста', 
            form=form,
        )

    session: Session = request.environ['session']
    session.add(
        News(
            title=request.form['title'],
            text=request.form['text'],
        )
    )
    session.commit()
    
    return redirect(url_for(".index"))


@blueprint.route("/<int:news_id>/edit", methods=["GET", "POST"])
def edit(news_id: int):

    session: Session = request.environ['session']
    news = session.get(News, news_id)
    categories = [
        category[0] for category in
        session.execute(
            select(AssignedCategory.category_id)
            .where(AssignedCategory.news_id == news_id)
        ).all()
    ]

    if not news:

        flash('Пост не найден!', 'danger')
        return redirect(url_for(".index"))

    form = UpdateForm(
        title=news.title,
        text=news.text,
        categories=categories,
    )
    form.categories.choices = [
        (category.id, category.title) 
        for category in Category.query.all()
    ]

    if not form.validate_on_submit():

        return render_template(
            "form.html",
            title='Редактирование поста',
            form=form,
        )
        
    session.execute(
        delete(AssignedCategory)
        .where(AssignedCategory.news_id == news_id)
    )
        
    for category_id in request.form.getlist('categories', type=int):

        session.add(
            AssignedCategory(
                news_id=news_id,
                category_id=category_id,
            )
        )

    news.title = request.form['title']
    news.text = request.form['text']
    session.commit()

    flash('Пост обновлен!', 'success')
    return redirect(url_for(".index"))


@blueprint.route("<int:news_id>/delete", methods=["POST"])
def delete_news(news_id: int):

    session: Session = request.environ['session']

    session.execute(
        delete(News)
        .where(News.id == news_id)
    )
    session.execute(
        delete(AssignedCategory)
        .where(AssignedCategory.news_id == news_id)
    )
    session.commit()

    flash('Пост удален!', 'success')
    return redirect(url_for(".index"))


def setup(app: Flask):

    app.register_blueprint(blueprint)
