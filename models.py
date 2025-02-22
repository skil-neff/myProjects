import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # date = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Integer)
