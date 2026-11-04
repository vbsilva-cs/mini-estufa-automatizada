from flask import Blueprint, redirect, render_template, request, url_for

from app.services.monitoring import MonitoringService
from app.services.readings import ReadingCycleService
from app.services.simulation import load_dataset


web_bp = Blueprint("web", __name__)
monitoring_service = MonitoringService()
DATASET = load_dataset()
AUTO_REFRESH_SECONDS = 30
reading_service = ReadingCycleService(DATASET)


@web_bp.get("/")
def dashboard():
    if request.args.get("atualizar") == "1":
        leitura = reading_service.advance()
    else:
        leitura = reading_service.current

    alertas = monitoring_service.compare_leitura(leitura)
    return render_template(
        "dashboard.html",
        leitura=leitura,
        limites=monitoring_service.limites,
        alertas=alertas,
        estado=monitoring_service.estado(leitura),
        auto_refresh_seconds=AUTO_REFRESH_SECONDS,
        atualizar_url=url_for("web.dashboard", atualizar=1),
    )


@web_bp.route("/limites", methods=["GET", "POST"])
def limites():
    erro = None

    if request.method == "POST":
        try:
            for parametro in monitoring_service.limites:
                minimo = float(request.form[f"{parametro}_minimo"])
                maximo = float(request.form[f"{parametro}_maximo"])
                monitoring_service.update_limite(parametro, minimo, maximo)
            return redirect(url_for("web.limites", status="ok"))
        except (ValueError, TypeError):
            erro = "Entrada inválida: cada mínimo deve ser menor que o máximo."

    return render_template(
        "limites.html",
        limites=monitoring_service.limites,
        erro=erro,
        status=request.args.get("status"),
    ), (400 if erro else 200)


@web_bp.get("/alertas")
def alertas():
    parametro = request.args.get("parametro")

    eventos = []
    for leitura in DATASET:
        for alerta in monitoring_service.compare_leitura(leitura):
            if parametro and alerta.parametro != parametro:
                continue
            eventos.append(alerta)

    return render_template(
        "alertas.html",
        alertas=eventos,
        parametro=parametro,
    )
