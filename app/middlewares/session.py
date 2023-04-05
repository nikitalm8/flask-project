import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionMiddleware(object):
    

    def __init__(self, app, sessionmaker: async_sessionmaker):

        self.app = app
        self.sessionmaker = sessionmaker


    def __call__(self, context: dict, handler: callable):

        session: AsyncSession = self.sessionmaker()
        context['session'] = session
        
        response = self.app(context, handler)
        asyncio.run(session.close())

        return response
