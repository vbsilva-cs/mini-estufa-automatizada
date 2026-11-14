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

    # Verifica se o retorno é JSON válido
    json_data = response.get_json()
    assert json_data is not None

    # Verifica o conteúdo da resposta
    assert json_data["mensagem"] == "Mini estufa automatizada."