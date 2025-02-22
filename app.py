from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from models import db, Expenses
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route("/")
def index():
    expenses = Expenses.query.all()
    return render_template("index.html", expenses=expenses)

@app.route("/add", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    if title:
        new_expense = Expenses(title=title)
        db.session.add(new_expense)
        db.session.commit()
    return redirect(url_for("index"))

# @app.route("/complete/<int:task_id>")
# def complete_task(task_id):
#     task = Task.query.get(task_id)
#     if task:
#         task.completed = True
#         db.session.commit()
#     return redirect(url_for("index"))
#
@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expenses.query.get(expense_id)
    if expense and request.method == "POST":
        expense.title = request.form.get("title", "").strip()
        if expense.title:
            db.session.commit()
            return redirect(url_for("index"))
    return render_template("edit.html", expense=expense)
