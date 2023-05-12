from functools import wraps

from flask import (
    redirect,
    url_for, 
    flash, 
    current_app, 
)
from flask_login import current_user


class AdminChecker(object):

    def __call__(self):

        return check()


def check():
    
    if not current_user.is_authenticated:
        
        return current_app.login_manager.unauthorized()
    
    if not current_user.is_admin:

        flash('У вас недостаточно прав для просмотра этой страницы!', 'danger')
        return redirect(url_for("films.index"))


def execute(func, *args, **kwargs):

    if callable(getattr(current_app, "ensure_sync", None)):
        
        return current_app.ensure_sync(func)(*args, **kwargs)
        
    return func(*args, **kwargs)


def is_admin(func):
    
    @wraps(func)
    def decorated_view(*args, **kwargs):

        return (
            check()
            or execute(func, *args, **kwargs)
        )

    return decorated_view
