from app.database.models import User
from app.utils.forms import EditUserForm, DeleteUserForm

from flask import (
    Flask, 
    Blueprint, 
    render_template, 
    flash,
    url_for,
    redirect,
    request, 
)
from flask_login import logout_user, login_required, current_user 

from sqlalchemy import delete
from sqlalchemy.orm import Session


blueprint = Blueprint("profile", __name__, url_prefix='/profile')

@blueprint.route("/")
@login_required
def index():
    
    return render_template("profile.html")


@blueprint.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():

    form = EditUserForm(obj=current_user)

    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Редактирование профиля', 
            form=form,
        )

    session: Session = request.environ['session']
    
    user = session.get(User, current_user.id)
    
    user.username = form.username.data
    user.update_password(form.password.data)

    session.commit()

    flash('Профиль успешно обновлен!', 'success')
    return redirect(url_for("profile.index"))


@blueprint.route("/delete", methods=['GET', 'POST'])
@login_required
def delete_user():

    form = DeleteUserForm()

    if not form.validate_on_submit():

        return render_template(
            "form.html", 
            title='Вы уверены?', 
            form=form,
        )

    if form.cancel.data:

        flash('Удаление отменено', 'info')
        return redirect(url_for("profile.index"))

    session: Session = request.environ['session']
    session.execute(
        delete(User)
        .where(User.id == current_user.id)
    )
    session.commit()  
      
    logout_user()

    flash('Профиль успешно удален!', 'success')
    return redirect(url_for("news.index"))


def setup(app: Flask):
    """
    Setup all the views for home.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
