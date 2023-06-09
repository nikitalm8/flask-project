from app.database import db

from datetime import date
from flask import url_for


class News(db.Model):
    __tablename__ = 'news'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    
    title: db.Mapped[str] = db.mapped_column()
    text: db.Mapped[str] = db.mapped_column()
    
    created_at: db.Mapped[date] = db.mapped_column(default=date.today)

    @property
    def url(self) -> str:
        
        return url_for("news.news", news_id=self.id)

    @property
    def href(self) -> str:
        
        return '<a href="%s">%s</a>' % (self.url, self.title)
    