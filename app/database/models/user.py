from app.database import db

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: db.Mapped[int] = db.mapped_column(primary_key=True, autoincrement=True)
    
    username: db.Mapped[str] = db.mapped_column(unique=True)
    password: db.Mapped[str] = db.mapped_column(nullable=False)
    
    created_at: db.Mapped[datetime] = db.mapped_column(default=datetime.utcnow)
    admin_level: db.Mapped[int] = db.mapped_column(default=0)

    def update_password(self, password: str):
        
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:

        return check_password_hash(self.password, password)
