from app.database.models import Film, Review
from app.utils.login import AdminChecker
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
from werkzeug.utils import secure_filename


blueprint = Blueprint("admin", __name__, url_prefix="/admin")
blueprint.before_request(AdminChecker())


@blueprint.route("/")
def index():

    page = request.args.get('page', 1, type=int)
    pagination = Film.query.order_by(Film.created_at.desc()).paginate(page=page, per_page=10)

    return render_template(
        "admin_films.html", 
        pagination=pagination,
        items=pagination.items,
        Film=Film,
    )


@blueprint.route("/create", methods=["GET", "POST"])
def create():

    form = CreateForm()
    
    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Создание поста', 
            form=form,
        )

    filename = '/images/' + secure_filename(form.image.data.filename)
    form.image.data.save('app/static' + filename)

    session: Session = request.environ['session']
    session.add(
        Film(
            title=request.form['title'],
            text=request.form['text'],
            image=filename,
        )
    )
    session.commit()
    
    return redirect(url_for(".index"))


@blueprint.route("/<int:film_id>/edit", methods=["GET", "POST"])
def edit(film_id: int):

    session: Session = request.environ['session']
    film = session.get(Film, film_id)

    if not film:

        flash('Фильм не найден!', 'danger')
        return redirect(url_for(".index"))

    form = UpdateForm(
        title=film.title,
        text=film.text,
    )
    if not form.validate_on_submit():

        return render_template(
            "form.html",
            title='Редактирование поста',
            form=form,
        )

    film.title = request.form['title']
    film.text = request.form['text']

    if form.image.data:

        filename = '/images/' + secure_filename(form.image.data.filename)
        form.image.data.save('app/static' + filename)
        film.image = filename
    
    session.commit()

    flash('Пост обновлен!', 'success')
    return redirect(url_for(".index"))


@blueprint.route("<int:film_id>/delete", methods=["POST"])
def delete_film(film_id: int):

    session: Session = request.environ['session']

    session.execute(
        delete(Film)
        .where(Film.id == film_id)
    )
    session.execute(
        delete(Review)
        .where(Review.film_id == film_id)
    )
    session.commit()

    flash('Фильм удален!', 'success')
    return redirect(url_for(".index"))


def setup(app: Flask):

    app.register_blueprint(blueprint)
