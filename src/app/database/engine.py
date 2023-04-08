from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def load_user(user_id: int):
    
    from app.database.models.user import User
    return db.session.get(User, user_id)
