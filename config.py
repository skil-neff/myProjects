import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'todo.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "Таємний_Ключ_Захисту_Фласк_2025!")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    