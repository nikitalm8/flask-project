import yaml
import asyncio

from app import views, middlewares, utils
from app.database import create_sessionmaker

from flask import Flask
from flask_wtf import CSRFProtect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy


async def main():
    
    app = Flask(__name__, static_url_path='')
    app.secret_key = 'secret'
    app.config = yaml.safe_load(open('config.yaml'))
    
    bootstrap = Bootstrap5(app)
    csrf = CSRFProtect(app)
    
    with app.app_context():
        
        db = SQLAlchemy(app)
        db.create_all()
    
    app.static_folder = 'app/static'
    app.template_folder = 'app/templates'

    views.setup(app)
    middlewares.setup(app, sessionmaker)

    app.run(port=1488)


if __name__ == '__main__':
    
    asyncio.run(main())
