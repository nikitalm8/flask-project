from app.database.models import User
from app.utils.forms import LoginForm, RegisterForm

from flask import (
    Flask, 
    Blueprint, 
    request, 
    render_template, 
    url_for,
    redirect,
    flash,
)

from flask_login import login_user, logout_user

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select



blueprint = Blueprint("auth", __name__)


@blueprint.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if not form.validate_on_submit():

        return render_template(
            'login.html', 
            form=form, 
            title='Войти', 
            url=url_for('auth.register'), 
            href='Зарегистрироваться',
        )

    session: Session = request.environ['session']
    user = session.scalar(
        select(User)
        .where(User.username == form.username.data)
    )

    if user and user.check_password(form.password.data):

        login_user(user, remember=form.remember.data)
        return redirect(url_for('news.index'))

    flash('Неправильный логин или пароль')
    return redirect(url_for('auth.login'))


@blueprint.route("/register", methods=['GET', 'POST'])  
def register():

    form = RegisterForm()

    if not form.validate_on_submit():

        return render_template(
            'login.html', 
            form=form, 
            title='Зарегистрироваться', 
            url=url_for('auth.login'), 
            href='Войти',
        )

    session: Session = request.environ['session']
    
    user = User(username=form.username.data)
    user.update_password(form.password.data)

    try:

        session.add(user)
        session.commit()

    except IntegrityError:

        flash('Пользователь с таким именем уже существует')
        return redirect(url_for('auth.register'))

    login_user(user)
    return redirect(url_for('news.index'))


@blueprint.route("/logout", methods=['GET', 'POST'])  
def logout():

    logout_user()
    return redirect(url_for('news.index'))


def setup(app: Flask):
    """
    Setup all the views for auth.

    :param Flask app: Flask app instance
    """

    app.register_blueprint(blueprint)
