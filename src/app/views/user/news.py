from app.utils.forms import CategorySelectForm
from app.database.models import News, AssignedCategory, Category

from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    redirect,
    url_for,
    request, 
)

from sqlalchemy.orm import Session
from sqlalchemy.future import select


blueprint = Blueprint("news", __name__)

@blueprint.route("/")
def index():

    query = News.query.order_by(News.created_at.desc())

    if categories := request.args.getlist('categories', type=int):

        query = query.filter(News.id.in_(
            select(AssignedCategory.news_id)
            .where(AssignedCategory.category_id.in_(categories))
        ))

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=10)

    category_form = CategorySelectForm(
        categories=request.args.getlist('categories', type=int)
    )
    category_form.categories.choices = [
        (category.id, category.title) 
        for category in Category.query.all()
    ]
    
    return render_template(
        "pagination.html", 
        pagination=pagination,
        items=pagination.items,
        form=category_form,
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


@blueprint.route("/categories", methods=['POST'])
def category():

    categories = request.form.getlist('categories', type=int)
    return redirect(
        url_for('news.index', categories=categories, page=1),
    )


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
