from datetime import UTC, datetime

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.services.monitoring import MonitoringService
from app.services.reading_stream import ReadingStreamService
from app.services.readings import ReadingCycleService
from app.services.simulation import load_dataset


web_bp = Blueprint("web", __name__)
monitoring_service = MonitoringService()
DATASET = load_dataset()
reading_stream_service = ReadingStreamService(DATASET)
PARAMETROS = {
    "temperatura_c": {"nome": "Temperatura", "unidade": "°C"},
    "umidade_pct": {"nome": "Umidade", "unidade": "%"},
    "luminosidade_lux": {"nome": "Luminosidade", "unidade": "lux"},
}
AUTO_REFRESH_SECONDS = 30
reading_service = ReadingCycleService(DATASET)


@web_bp.get("/")
def dashboard():
    leitura_cursor = session.get("leitura_cursor", 0)
    leitura = reading_stream_service.current(leitura_cursor)
    if request.args.get("atualizar") == "1":
        leitura = reading_service.advance()
    else:
        leitura = reading_service.current

    alertas = monitoring_service.compare_leitura(leitura)
    proxima_acao = "Nenhuma ação imediata necessária."
    descricao_alerta = "Todos os parâmetros estão na faixa esperada."
    if any(alerta.parametro == "umidade_pct" for alerta in alertas):
        proxima_acao = "Verifique o alerta de umidade."
        descricao_alerta = "A umidade está acima da faixa configurada."
    elif alertas:
        descricao_alerta = "Há leituras fora da faixa configurada."

    return render_template(
        "dashboard.html",
        leitura=leitura,
        limites=monitoring_service.limites,
        alertas=alertas,
        estado=monitoring_service.estado(leitura),
        parametros=PARAMETROS,
        ultima_atualizacao=reading_stream_service.elapsed_label(session.get("last_refresh_at")),
        proxima_acao=proxima_acao,
        descricao_alerta=descricao_alerta,
        active_page="dashboard",
        auto_refresh_seconds=AUTO_REFRESH_SECONDS,
        atualizar_url=url_for("web.dashboard", atualizar=1),
    )


@web_bp.post("/atualizar")
def atualizar_leitura():
    leitura_cursor = session.get("leitura_cursor", 0)
    session["leitura_cursor"] = reading_stream_service.next_cursor(leitura_cursor)
    session["last_refresh_at"] = datetime.now(UTC).isoformat()
    return redirect(url_for("web.dashboard"))


@web_bp.route("/limites", methods=["GET", "POST"])
def limites():
    erros = {}
    valores = {
        parametro: {"minimo": limite.minimo, "maximo": limite.maximo}
        for parametro, limite in monitoring_service.limites.items()
    }

    if request.method == "POST":
        limites_novos = {}
        for parametro in monitoring_service.limites:
            minimo_raw = request.form.get(f"{parametro}_minimo", "").strip()
            maximo_raw = request.form.get(f"{parametro}_maximo", "").strip()
            valores[parametro] = {"minimo": minimo_raw, "maximo": maximo_raw}
            erros_antes = len(erros)

            if not minimo_raw:
                erros[f"{parametro}_minimo"] = "Campo obrigatório."
            if not maximo_raw:
                erros[f"{parametro}_maximo"] = "Campo obrigatório."
            if len(erros) > erros_antes:
                continue

            try:
                minimo = float(minimo_raw)
                maximo = float(maximo_raw)
            except ValueError:
                erros[f"{parametro}_maximo"] = "Informe valores numéricos válidos."
                continue

            try:
                monitoring_service.validate_limite(parametro, minimo, maximo)
            except ValueError as exc:
                mensagem = str(exc)
                if "mínimo deve ser menor" in mensagem:
                    erros[f"{parametro}_maximo"] = mensagem
                elif "umidade" in mensagem:
                    erros[f"{parametro}_minimo"] = mensagem
                    erros[f"{parametro}_maximo"] = mensagem
                elif "luminosidade" in mensagem:
                    if minimo < 0:
                        erros[f"{parametro}_minimo"] = mensagem
                    if maximo < 0:
                        erros[f"{parametro}_maximo"] = mensagem
                else:
                    erros[f"{parametro}_maximo"] = mensagem
                continue

            limites_novos[parametro] = (minimo, maximo)

        if not erros:
            for parametro, (minimo, maximo) in limites_novos.items():
                monitoring_service.update_limite(parametro, minimo, maximo)
            return redirect(url_for("web.limites", status="ok"))

    return render_template(
        "limites.html",
        limites=monitoring_service.limites,
        erros=erros,
        valores=valores,
        parametros=PARAMETROS,
        status=request.args.get("status"),
        active_page="limites",
    ), (400 if erros else 200)


@web_bp.get("/alertas")
def alertas():
    parametro = request.args.get("parametro")
    status = request.args.get("status")

    eventos = []
    for leitura in reversed(DATASET):
        for alerta in monitoring_service.compare_leitura(leitura):
            if parametro and alerta.parametro != parametro:
                continue
            alerta_status = "acima" if alerta.valor > monitoring_service.limites[alerta.parametro].maximo else "abaixo"
            if status and alerta_status != status:
                continue
            eventos.append(alerta)

    return render_template(
        "alertas.html",
        alertas=eventos,
        parametro=parametro,
        status=status,
        limites=monitoring_service.limites,
        parametros=PARAMETROS,
        active_page="alertas",
    )