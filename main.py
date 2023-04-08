import yaml

from app import views, middlewares
from app.database import db, load_user

from flask import Flask
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

    
app = Flask(__name__, static_url_path='')

app.secret_key = 'secret'
app.static_folder = 'app/static'
app.template_folder = 'app/templates'
app.config.update(
    **yaml.safe_load(open('config.yaml')),
)

bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.user_loader(load_user)
login_manager.login_view = 'auth.login'

with app.app_context():

    db.init_app(app)
    db.create_all()

views.setup(app)
middlewares.setup(app, db)


if __name__ == '__main__':
    
    app.run()
