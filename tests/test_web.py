from app.routes.web import monitoring_service


def test_rf01_exibe_leituras_simuladas(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "Dados simulados" in body
    assert "Visão geral" in body
    assert "27,4" in body
    assert "78" in body


def test_rf02_permite_editar_limites_validos(client):
    response = client.post(
        "/limites",
        data={
            "temperatura_c_minimo": "19",
            "temperatura_c_maximo": "30",
            "umidade_pct_minimo": "50",
            "umidade_pct_maximo": "80",
            "luminosidade_lux_minimo": "7000",
            "luminosidade_lux_maximo": "12000",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert monitoring_service.limites["temperatura_c"].minimo == 19
    assert monitoring_service.limites["temperatura_c"].maximo == 30
    assert monitoring_service.limites["umidade_pct"].maximo == 80


def test_rnf03_rejeita_minimo_maior_ou_igual_maximo(client):
    response = client.post(
        "/limites",
        data={
            "temperatura_c_minimo": "30",
            "temperatura_c_maximo": "20",
            "umidade_pct_minimo": "45",
            "umidade_pct_maximo": "75",
            "luminosidade_lux_minimo": "2000",
            "luminosidade_lux_maximo": "12000",
        },
    )

    assert response.status_code == 400
    assert "mínimo deve ser menor" in response.data.decode("utf-8")


def test_rf03_exibe_alerta_visual_para_fora_do_limite(client):
    response = client.get("/")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "Atenção: 1 parâmetro fora do limite" in body
    assert "Há leituras fora da faixa configurada." in body


def test_rnf04_rejeita_umidade_fora_da_faixa(client):
    response = client.post(
        "/limites",
        data={
            "temperatura_c_minimo": "19",
            "temperatura_c_maximo": "29",
            "umidade_pct_minimo": "-1",
            "umidade_pct_maximo": "80",
            "luminosidade_lux_minimo": "2000",
            "luminosidade_lux_maximo": "12000",
        },
    )

    assert response.status_code == 400
    assert "umidade deve ficar entre 0 e 100%" in response.data.decode("utf-8")


def test_rf05_filtra_alertas_por_parametro(client):
    response = client.get("/alertas?parametro=luminosidade_lux&status=")

    assert response.status_code == 200
    body = response.data.decode("utf-8")
    assert "Luminosidade: 32000.0 lux" in body
    assert "Temperatura: 27,4 °C" not in body