from flask import Flask


def register_blueprints(app: Flask) -> None:
    """Registra todos los Blueprints de la aplicación."""
    from app.routes.health import bp as health_bp
    from app.routes.estaciones import bp as estaciones_bp
    from app.routes.sensores import bp as sensores_bp
    from app.routes.mediciones import bp as mediciones_bp
    from app.routes.predicciones import bp as predicciones_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(estaciones_bp)
    app.register_blueprint(sensores_bp)
    app.register_blueprint(mediciones_bp)
    app.register_blueprint(predicciones_bp)
