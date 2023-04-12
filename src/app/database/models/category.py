from app.database import db


class Category(db.Model):
    __tablename__ = 'categories'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    title: db.Mapped[str] = db.mapped_column()
    