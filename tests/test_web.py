from app.routes.web import monitoring_service


def test_rf01_exibe_leituras_simuladas(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "temperatura_c" in body
    assert "umidade_pct" in body
    assert "luminosidade_lux" in body
    assert "Dataset simulado" in body


def test_rf02_permite_editar_limites_validos(client):
    response = client.post(
        "/limites",
        data={
            "temperatura_c_minimo": "19",
            "temperatura_c_maximo": "29",
            "umidade_pct_minimo": "50",
            "umidade_pct_maximo": "80",
            "luminosidade_lux_minimo": "7000",
            "luminosidade_lux_maximo": "28000",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert monitoring_service.limites["temperatura_c"].minimo == 19
    assert monitoring_service.limites["temperatura_c"].maximo == 29


def test_rnf03_rejeita_minimo_maior_ou_igual_maximo(client):
    response = client.post(
        "/limites",
        data={
            "temperatura_c_minimo": "30",
            "temperatura_c_maximo": "20",
            "umidade_pct_minimo": "55",
            "umidade_pct_maximo": "85",
            "luminosidade_lux_minimo": "8000",
            "luminosidade_lux_maximo": "30000",
        },
    )

    assert response.status_code == 400
    assert "mínimo deve ser menor" in response.data.decode("utf-8")


def test_rf03_exibe_alerta_visual_para_fora_do_limite(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "ATENÇÃO" in body
    assert "fora do limite" in body
