import os
from flask import Flask
from app.config import config
from app.extensions import db
from app.routes import register_blueprints
from app.errors.handlers import register_error_handlers


def create_app(config_name: str | None = None) -> Flask:
    """
    Application factory.
    Uso:
        app = create_app()                  # usa la variable de entorno FLASK_ENV
        app = create_app("testing")         # fuerza un entorno concreto
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensiones
    db.init_app(app)

    # Blueprints
    register_blueprints(app)

    # Manejo global de errores
    register_error_handlers(app)

    return app
