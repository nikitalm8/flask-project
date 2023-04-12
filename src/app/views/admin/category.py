from app.database.models import Category, AssignedCategory
from app.utils.login import LevelChecker
from app.utils.forms import CreateCategoryForm, UpdateCategoryForm

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


blueprint = Blueprint("admin_categories", __name__, url_prefix="/admin/categories")
blueprint.before_request(LevelChecker(2))

@blueprint.route("/")
def index():

    page = request.args.get('page', 1, type=int)
    pagination = Category.query.paginate(page=page, per_page=10)
    
    return render_template(
        "admin_categories.html", 
        pagination=pagination,
        items=pagination.items,
        Category=Category,
    )


@blueprint.route("/create", methods=['GET', 'POST'])    
def create():

    form = CreateCategoryForm()

    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Создание категории', 
            form=form,
        )

    session: Session = request.environ['session']
    session.add(Category(title=form.title.data))
    session.commit()

    flash('Категория успешно создана!', 'success')
    return redirect(url_for('.index'))


@blueprint.route("/<int:category_id>/edit", methods=['GET', 'POST'])    
def edit(category_id: int):

    session: Session = request.environ['session']
    category = session.get(Category, category_id)

    form = UpdateCategoryForm(obj=category)

    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Редактирование категории', 
            form=form,
        )

    category.title = form.title.data
    session.commit()

    flash('Категория успешно изменена!', 'success')
    return redirect(url_for('.index'))


@blueprint.route("/<int:category_id>/delete", methods=['POST'])
def delete_category(category_id: int):

    session: Session = request.environ['session']

    session.execute(
        delete(Category)
        .where(Category.id == category_id)
    )
    session.execute(
        delete(AssignedCategory)
        .where(AssignedCategory.category_id == category_id)
    )
    session.commit()

    flash('Категория успешно удалена!', 'success')
    return redirect(url_for('.index'))


def setup(app: Flask):
    """
    Setup all the views for admin.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
