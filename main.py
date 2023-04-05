import asyncio

from app import views, middlewares, utils
from app.database import create_sessionmaker

from flask import Flask


async def main():
    
    app = Flask(__name__, static_url_path='')

    config = utils.load_config('config.yaml')
    sessionmaker = await create_sessionmaker(config.database_url)

    app.static_folder = 'app/static'
    app.template_folder = 'app/templates'

    views.setup(app)
    middlewares.setup(app, sessionmaker)

    app.run()



if __name__ == '__main__':
    
    asyncio.run(main())
