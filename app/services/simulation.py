import json
from pathlib import Path

from app.domain.entities import Leitura


DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "simulated" / "leituras.json"


def load_dataset() -> list[Leitura]:
    with DATASET_PATH.open(encoding="utf-8") as file:
        payload = json.load(file)

    return [
        Leitura(
            instante=item["instante"],
            temperatura_c=float(item["temperatura_c"]),
            umidade_pct=float(item["umidade_pct"]),
            luminosidade_lux=float(item["luminosidade_lux"]),
        )
        for item in payload
    ]
