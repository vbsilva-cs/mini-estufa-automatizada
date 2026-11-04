# Decisões de arquitetura e implementação

1. **Arquitetura monolítica em camadas (Flask)**
   - Motivo: simplicidade compatível com MVP individual.

2. **Dataset simulado determinístico em arquivo JSON**
   - Motivo: reprodutibilidade para validação de regras sem hardware.

3. **Limites em memória**
   - Motivo: evitar prometer persistência histórica antes da fase futura com PostgreSQL.

4. **Regras de alerta no serviço de monitoramento**
   - Motivo: separar domínio/regra da camada de apresentação.

5. **Escopo estritamente informacional**
   - Motivo: não acionar hardware nem comunicar ganhos ambientais ainda não medidos.
