from dataclasses import dataclass


@dataclass(frozen=True)
class Leitura:
    instante: str
    temperatura_c: float
    umidade_pct: float
    luminosidade_lux: float


@dataclass(frozen=True)
class Limite:
    parametro: str
    minimo: float
    maximo: float
    ativo: bool = True


@dataclass(frozen=True)
class Alerta:
    parametro: str
    valor: float
    mensagem: str
    instante: str
