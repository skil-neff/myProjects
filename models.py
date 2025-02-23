from datetime import datetime, timezone, date
from flask_sqlalchemy import SQLAlchemy
today = date.today()
db = SQLAlchemy()

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Integer)
    # date = db.Column(db.Date)
    # date = db.Column(db.Date, default=datetime.utcnow().date)
    # date = db.Column(db.String(12) , date =datetime.utcnow)
    

    # def __repr__(self):
    #     return '<Expense %r>' % self.id

