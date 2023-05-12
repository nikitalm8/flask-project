from app.database import db

from datetime import date
from flask import url_for


class Film(db.Model):
    __tablename__ = 'films'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    
    title: db.Mapped[str]
    text: db.Mapped[str]
    image: db.Mapped[str]
    
    created_at: db.Mapped[date] = db.mapped_column(default=date.today)

    reviews = db.relationship(
        "Review",
        uselist=True,
    )

    @property
    def url(self) -> str:
        
        return url_for("films.film", film_id=self.id)

    @property
    def href(self) -> str:
        
        return '<a href="%s">%s</a>' % (self.url, self.title)

    @property
    def avg(self) -> float:

        return sum([
            review.rating
            for review in self.reviews
        ]) / (len(self.reviews) or 1)
        
    @property
    def review_count(self) -> float:

        return len(self.reviews)
