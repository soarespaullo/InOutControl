import os

# Caminho absoluto da pasta onde este arquivo está
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "troque-esta-chave"

    # Torna o BASE_DIR acessível via current_app.config["BASE_DIR"]
    BASE_DIR = BASE_DIR

    # Caminho do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'inoutcontrol.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload de imagens das peças
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
