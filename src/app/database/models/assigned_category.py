from app.database import db
from app.database.models import News, Category


class AssignedCategory(db.Model):
    __tablename__ = 'assigned_categories'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    
    category_id: db.Mapped[int] = db.mapped_column()
    news_id: db.Mapped[int] = db.mapped_column()
