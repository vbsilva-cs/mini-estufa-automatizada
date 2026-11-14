import pytest
from app import app


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste para a aplicação Flask."""
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Testa a rota principal."""
    response = client.get("/")

    # Verifica se o status HTTP é 200
    assert response.status_code == 200

    # Verifica se payload contém "mini-estufa-automatizada"
    body = response.data.decode("utf-8")
    assert "mini-estufa-automatizada" in body