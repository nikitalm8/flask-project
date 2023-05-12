from app.utils.forms import ReviewForm
from app.database.models import Film, Review

from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    redirect,
    flash,
    url_for,
    request, 
)
from flask_login import current_user

from sqlalchemy.orm import Session
from sqlalchemy.future import select


blueprint = Blueprint("films", __name__)

@blueprint.route("/")
def index():

    query = Film.query.order_by(Film.created_at.desc())

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=10)
    
    return render_template(
        "pagination.html", 
        pagination=pagination,
        rows=[
            pagination.items[offset: offset + 3]
            for offset in range(0, len(pagination.items), 3)
        ],
        Film=Film,
    )


@blueprint.route("/film/<int:film_id>", methods=['GET', 'POST'])
def film(film_id: int):

    form = ReviewForm()
    session: Session = request.environ['session']
    film = session.scalar(
        select(Film)
        .where(Film.id == film_id)
    )

    if form.validate_on_submit():

        message = None

        if not current_user.is_authenticated:

            message = 'Войдите для того, чтобы оставлять отзывы!'

        else:

            review = session.scalar(
                select(Review)
                .where(Review.film_id == film_id)
                .where(Review.user_id == current_user.id)
            )
            if review:

                message = 'Вы уже оставляли отзыв!'

        if message:

            flash(message, 'error')
            return render_template(
                "film.html", 
                film=film, 
                form=form,
            )

        session.add(
            Review(
                user_id=current_user.id,
                film_id=film.id,
                text=form.text.data,
                rating=form.rating.data,
            )
        )
        session.commit()

    return render_template(
        "film.html", 
        film=film, 
        form=form,
    )


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
