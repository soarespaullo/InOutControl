import os
from flask import Flask
from config import Config
from extensions import db
from dashboard.routes import dashboard_bp
from users.routes import users_bp
from parts.routes import parts_bp
from movements import movements_bp 
from backup import backup_bp

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )
    app.config.from_object(Config)

    db.init_app(app)

    # Registrando blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp, url_prefix="/usuarios")
    app.register_blueprint(parts_bp, url_prefix="/pecas")
    app.register_blueprint(movements_bp, url_prefix="/movimentacoes")
    app.register_blueprint(backup_bp, url_prefix="/backup")
    
    return app
