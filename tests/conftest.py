import pytest

from app import create_app
from app.routes.web import reading_service


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_reading_service():
    reading_service.reset()
