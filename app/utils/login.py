from functools import wraps

from flask import (
    redirect,
    url_for, 
    flash, 
    current_app, 
)
from flask_login import current_user


class LevelChecker(object):

    def __init__(self, level: int=1):
        
        self.level = level

    def __call__(self):

        return check_level(self.level)


def check_level(level: int=1):
    
    if not current_user.is_authenticated:
        
        return current_app.login_manager.unauthorized()
    
    if current_user.admin_level < level:

        flash('У вас недостаточно прав для просмотра этой страницы!', 'danger')
        return redirect(url_for("news.index"))


def execute(func, *args, **kwargs):

    if callable(getattr(current_app, "ensure_sync", None)):
        
        return current_app.ensure_sync(func)(*args, **kwargs)
        
    return func(*args, **kwargs)


def is_admin(func):
    
    @wraps(func)
    def decorated_view(*args, **kwargs):

        return (
            check_level()
            or execute(func, *args, **kwargs)
        )

    return decorated_view
