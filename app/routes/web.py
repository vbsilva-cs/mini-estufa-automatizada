from flask import Blueprint, render_template

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def home():
    try:
        html = render_template("index.html")
        return html
    except:
        return {"mensagem": "[ERRO] Servico indisponivel"}, 500

    