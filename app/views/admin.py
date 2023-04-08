from app.database.models import User
from app.utils.login import LevelChecker
from app.utils.forms import EditUserAdminForm

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

from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select


blueprint = Blueprint("admin", __name__, url_prefix="/admin")
blueprint.before_request(LevelChecker(2))

@blueprint.route("/")
def index():

    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(page=page, per_page=10)
    
    return render_template(
        "users.html", 
        pagination=pagination,
        items=pagination.items,
        User=User,
    )


@blueprint.route("/delete/<int:user_id>", methods=['POST'])
def delete_user(user_id: int):

    session: Session = request.environ['session']

    admin_level = session.scalar(
        select(User.admin_level)
        .where(User.id == user_id)
    )
    if admin_level >= current_user.admin_level:

        flash('Недостаточно прав для удаления данного пользователя!', 'danger')
        return redirect(url_for('admin.index'))
    
    session.execute(
        delete(User)
        .where(User.id == user_id)
    )
    session.commit()

    flash('Пользователь успешно удален!', 'success')
    return redirect(url_for('admin.index'))


@blueprint.route("/edit/<int:user_id>", methods=['GET', 'POST'])
def edit_user(user_id: int):

    session: Session = request.environ['session']
    user = session.scalar(
        select(User)
        .where(User.id == user_id)
    )

    if user.admin_level >= current_user.admin_level:

        flash('Недостаточно прав для редактирования данного пользователя!', 'danger')
        return redirect(url_for('admin.index'))
    
    form = EditUserAdminForm(obj=user)

    if not form.validate_on_submit():
        
        return render_template(
            "form.html",
            title='Редактирование пользователя', 
            form=form,
        )

    if int(form.admin_level.data) >= current_user.admin_level:

        flash('Вы не можете выдать эти привелегии!', 'danger')
        return redirect(url_for('admin.index'))

    user.username = form.username.data
    user.admin_level = int(form.admin_level.data)

    if not user.check_password(form.password.data):

        user.update_password(form.password.data)
    
    session.commit()

    flash('Пользователь успешно отредактирован!', 'success')
    return redirect(url_for('admin.index'))


@blueprint.route("/create", methods=['GET', 'POST'])
def create_user():

    form = EditUserAdminForm()

    if not form.validate_on_submit():

        return render_template(
            "form.html",
            title='Создание пользователя', 
            form=form,
        )

    if int(form.admin_level.data) >= current_user.admin_level:

        flash('Вы не можете выдать эти привелегии!', 'danger')
        return redirect(url_for('admin.index'))

    session: Session = request.environ['session']
    
    user = User(
        username=form.username.data,
        admin_level=int(form.admin_level.data),
    )
    user.update_password(form.password.data)

    try:

        session.add(user)
        session.commit()

    except IntegrityError:

        flash('Пользователь с таким именем уже существует!', 'danger')

    else:

        flash('Пользователь успешно создан!', 'success')
        
    return redirect(url_for('admin.index'))


def setup(app: Flask):
    """
    Setup all the views for admin.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
