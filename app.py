from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
# from datetime import datetime, timezone, date

from admin import admin
from models import Expenses, User
from config import Config
from extensions import db, login_manager
from forms import LoginForm, RegistrationForm



# Створення Flask-додатку
app = Flask(__name__)
app.config.from_object(Config)

# Ініціалізація розширень
db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)

# Створення таблиць, якщо їх ще немає
with app.app_context():
    db.create_all() # Створення таблиць


# Функція завантаження користувача
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    expenses = Expenses.query.all()
    return render_template("index.html", expenses=expenses)

@app.route("/expense/<int:id>")
def expense_detail(id):
    expense = Expenses.query.get_or_404(id)
    return render_template("expense.html", expense=expense)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Перевіряємо, чи існує користувач з таким логіном
        existing_user = User.query.filter_by(
            username=form.username.data
        ).first()
        if existing_user:
            flash("Користувач з таким ім'ям вже існує!", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Реєстрація пройшла успішно!", "success")
        login_user(user)
        return redirect(url_for("admin.index"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Успішний вхід!", "success")
            return redirect(url_for("admin.index"))

        flash("Невірний логін або пароль", "danger")

    return render_template("login.html", form=form)


# Сторінка виходу
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
