from math import ceil
from functools import cached_property

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class Pagination(object):

    def __init__(self, page: int, per_page: int, total: int, items: list):
        """
        Pagination object.

        :param int page: Current page
        :param int per_page: Results per page
        :param int total: Total results
        :param list items: Items
        """

        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @cached_property
    def pages(self) -> int:
        """
        Total pages.

        :return: Total pages
        """

        return ceil(self.total / self.per_page)

    @property
    def has_next(self) -> bool:
        """
        Has next page.

        :return: True if has next page
        """

        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        """
        Has previous page.

        :return: True if has previous page
        """

        return self.page > 1

    def iter_pages(self):

        return range(1, self.pages + 1)


class Base(DeclarativeBase):

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int, per_page: int):
        """
        Paginate results.

        :param AsyncSession session: AsyncSession instance
        :param int page: Current page
        :param int per_page: Results per page
        """

        results = await session.scalars(
            select(cls)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        results = results.all()

        if not results:

            raise ValueError

        if page == 1 and len(results) < per_page:

            return Pagination(1, 10, len(results), results)

        total = await session.scalar(
            select(func.count(cls.id))
        )
        return Pagination(page, per_page, total, results)
