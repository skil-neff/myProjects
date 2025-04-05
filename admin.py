from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, Select2Widget
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import StringField

from config import Config
from models import Expenses, Category, User, db


# Кастомна головна сторінка адмінки
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return super().index()


# Обмежений доступ до адмінки
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class UserAdmin(AdminModelView):
    column_list = ["id", "username"]
    column_labels = {"username": "Логін"}
    can_edit = False  # Вимикаємо можливість редагування
    can_create = False  # Вимикаємо можливість створення нових користувачів
    can_view_details = True  # Дозволяємо перегляд користувача

class CategoryAdmin(AdminModelView):
    column_labels = {"name": "Назва"}
    form_columns = ["name"]  # тільки поле для вводу назви категорії
    form_overrides = {
        "name": StringField
    }

# Обираємо категорію для товару
class ExpensesAdmin(AdminModelView):
    column_list = ( "category", "title", "value", "date")
    column_labels = {
        "category": "Категорія",
        "title": "Назва",
        "value": "Сума",
        "description": "Опис витрати",
        "date": "Дата додавання",
    }
    form_columns = ["category", "title", "value", "picture", "description", "date"]
    form_overrides = {"category": QuerySelectField,"picture": FileUploadField}
    form_args = {
        "category": {
            "query_factory": lambda: Category.query.all(),
            "get_label": "name",
            "allow_blank": False,
            "widget": Select2Widget(),
        },
        "picture": {
            "label": "Зображення",
            "base_path": Config.UPLOAD_FOLDER,
            "allowed_extensions": {"png", "jpg", "jpeg", "gif"},
        },
        "event_date": {
            "format": "%Y-%m-%d %H:%M:%S",
            "label": "Дата додавання",
            "description": "Введіть дату та чат у форматі YYYY-MM-DD HH:MM:SS"
        }
    }


# Створюємо об'єкт адмінки
admin = Admin(
    name="Адмінка витрат",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
)

admin.add_link(MenuLink(name="🏠 Повернутися до витрат", url="/"))
admin.add_link(MenuLink(name="🚪 Вийти", url="/logout"))
# Додаємо моделі в адмінку
admin.add_view(CategoryAdmin(Category, db.session, name="Категорії"))
admin.add_view(ExpensesAdmin(Expenses, db.session, name="Витрати"))
admin.add_view(UserAdmin(User, db.session, name="Користувачі"))