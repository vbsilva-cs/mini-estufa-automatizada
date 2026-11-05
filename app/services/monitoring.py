from app.domain.entities import Alerta, Leitura, Limite


class MonitoringService:
    def __init__(self) -> None:
        self.limites: dict[str, Limite] = {
            "temperatura_c": Limite("temperatura_c", 18.0, 30.0, True),
            "umidade_pct": Limite("umidade_pct", 45.0, 75.0, True),
            "luminosidade_lux": Limite("luminosidade_lux", 2000.0, 12000.0, True),
        }

    def validate_limite(self, parametro: str, minimo: float, maximo: float) -> None:
        if minimo >= maximo:
            raise ValueError("mínimo deve ser menor que máximo")

        if parametro not in self.limites:
            raise ValueError("parâmetro inválido")

        if parametro == "umidade_pct" and (minimo < 0 or maximo > 100):
            raise ValueError("umidade deve ficar entre 0 e 100%")

        if parametro == "luminosidade_lux" and (minimo < 0 or maximo < 0):
            raise ValueError("luminosidade não pode ser negativa")

    def update_limite(self, parametro: str, minimo: float, maximo: float, ativo: bool = True) -> Limite:
        self.validate_limite(parametro, minimo, maximo)

        self.limites[parametro] = Limite(parametro, minimo, maximo, ativo)
        return self.limites[parametro]

    def compare_leitura(self, leitura: Leitura) -> list[Alerta]:
        alertas: list[Alerta] = []
        for parametro, limite in self.limites.items():
            if not limite.ativo:
                continue

            valor = getattr(leitura, parametro)
            if valor < limite.minimo or valor > limite.maximo:
                alertas.append(
                    Alerta(
                        parametro=parametro,
                        valor=valor,
                        mensagem=f"{parametro} fora do limite ({limite.minimo} - {limite.maximo})",
                        instante=leitura.instante,
                    )
                )

        return alertas

    def estado(self, leitura: Leitura) -> str:
        return "atencao" if self.compare_leitura(leitura) else "normal"
