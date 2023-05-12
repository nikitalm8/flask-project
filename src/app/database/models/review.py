from app.database import db

from datetime import datetime


class Review(db.Model):
    __tablename__ = 'reviews'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    
    user_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('users.id', on_delete='CASCADE'))
    film_id: db.Mapped[int] = db.mapped_column(db.ForeignKey('films.id', on_delete='CASCADE'))
    
    text: db.Mapped[str]
    rating: db.Mapped[int]

    created_at: db.Mapped[datetime] = db.mapped_column(default=datetime.now)
    
    author = db.relationship(
        "User",
        back_populates="reviews",
        uselist=False,
    )
