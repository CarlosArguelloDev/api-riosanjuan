from flask import Flask
from app.utils.responses import fail


def register_error_handlers(app: Flask) -> None:
    """Registra handlers globales de errores HTTP."""

    @app.errorhandler(400)
    def bad_request(e):
        return fail("Solicitud incorrecta", 400, str(e))

    @app.errorhandler(404)
    def not_found(e):
        return fail("Recurso no encontrado", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return fail("Método no permitido", 405)

    @app.errorhandler(500)
    def internal_error(e):
        return fail("Error interno del servidor", 500)
