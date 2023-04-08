from . import Base

from sqlalchemy.orm import Mapped, mapped_column


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
