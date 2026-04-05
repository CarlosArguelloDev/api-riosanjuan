import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope="session")
def app():
    """Crea una instancia de la app configurada para tests (SQLite en memoria)."""
    application = create_app("testing")
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Cliente de test de Flask."""
    return app.test_client()


@pytest.fixture(scope="function")
def db(app):
    """Provee la sesión de DB; hace rollback después de cada test."""
    with app.app_context():
        yield _db
        _db.session.rollback()
