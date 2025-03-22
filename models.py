from datetime import datetime
from flask_login import UserMixin
from extensions import db

# today = date.today()

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    # date = db.Column(db.Date, default=datetime.utcnow().date)
    # date = db.Column(db.String(12) , date =datetime.utcnow)
    

    def __repr__(self):
        return '<Expense %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(
        db.String(256), nullable=False
    )  # Тут має бути хеш пароля

    def __repr__(self):
        return f"<User {self.username}>"