from datetime import datetime
from flask_login import UserMixin
from extensions import db

# today = date.today()

class Expenses(db.Model):

    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False
    )

    category = db.relationship(
        'Category', back_populates='expenses', lazy='joined'
    )    

    def __repr__(self):
        return '<Expense %r>' % self.id

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Зв'язок з витратами, один тип категорії може бути у декількох витрат
    expenses = db.relationship('Expenses', back_populates='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(
        db.String(256), nullable=False
    )  # Тут має бути хеш пароля

    def __repr__(self):
        return f'<User {self.username}>'