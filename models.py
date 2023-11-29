"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Users Table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, default = 'https://tinyurl.com/4vzvrrx3')

    def get_full_name(self):
        """Put together first/last name"""
        full_name = f'{self.first_name} {self.last_name}'

        return full_name