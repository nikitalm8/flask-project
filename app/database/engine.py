import logging

from app.database.models import Base

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Database(object):

    def __init__(self, database_url: str):

        logger = logging.getLogger('database.engine')
        
        if 'sqlite' in database_url:

            logger.warning(
                "Using SQLite database in production is not recommended",
            )

        self.engine = create_async_engine(
            database_url, future=True, 
        )

    async def create_tables(self):

        async with self.engine.begin() as conn:
                
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def setup(cls, database_url: str) -> async_sessionmaker:

        instance = cls(database_url)
        await instance.create_tables()

        return async_sessionmaker(
            instance.engine, 
            expire_on_commit=False,
        )


async def create_sessionmaker(database_url: str) -> async_sessionmaker:
    """
    Creates all tables and returns an async_sessionmaker

    :param str database_url: SQLAlchemy database url
    :return async_sessionmaker: Async Sessionmaker
    """

    return await Database.setup(database_url)
