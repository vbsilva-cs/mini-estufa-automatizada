# mini-estufa-automatizada

<img width="1920" height="868" alt="Tela Principal" src="https://github.com/user-attachments/assets/2bdf9b96-fb3b-4ee7-b740-757d7ea0caf6" />

## Sobre

Aplicação web responsiva para monitoramento **simulado** de miniestufa.

## Objetivo

Validar o fluxo informacional do MVP (leitura → validação → comparação → alerta) antes de qualquer investimento em hardware.

## Problema e público-alvo

O público-alvo é o produtor-operador de minifúndio. O problema atual é a dispersão de leituras e limites, dificultando análise rápida de condições fora do padrão.

## Funcionalidades incluídas

- Exibição de `leitura` simulada com `temperatura_c`, `umidade_pct` e `luminosidade_lux`.
- Atualização dinâmica da leitura atual por requisição manual e autoatualização a cada 30 segundos.
- Estado da estufa: **normal** ou **atenção**.
- Edição de `limite` (`minimo`, `maximo`, `ativo`) em memória.
- Exibição de `alerta` visual para valor fora do limite.
- Lista de alertas com filtro por parâmetro.

## Limitações e fora do escopo

- Sem sensores físicos, ou microcontrolador.
- Sem relés, bombas, ventiladores ou iluminação.
- Sem acionamento automático.
- Sem notificações externas (WhatsApp/SMS/e-mail/push).
- Sem autenticação/permissões de produção.
- Sem persistência histórica em banco no MVP.
- Sem uso de dados meteorológicos externos como leitura interna da estufa.

## Aviso importante

Os dados utilizados são **simulados, determinísticos e reproduzíveis**.

## Arquitetura

Arquitetura monolítica em camadas:

- `app/domain`: entidades de domínio (`leitura`, `limite`, `alerta`).
- `app/services`: validação, comparação e geração de alertas.
- `app/routes`: rotas HTTP Flask.
- `app/templates`: páginas HTML.
- `app/static`: estilos CSS.
- `data/simulated`: dataset fictício.

## Estrutura de pastas

```text
mini-estufa-automatizada/
├── app/
│   ├── domain/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
├── data/simulated/
├── docs/
├── tests/
├── run.py
└── requirements.txt
```

## Instalação e execução

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py run
```

## Execução dos testes

```bash
pytest
```

## Fluxo funcional

1. Carregar dataset simulado (`leitura`).
2. Validar atualização de `limite` (`minimo < maximo`).
3. Comparar leitura com limites ativos.
4. Gerar `alerta` visual quando houver violação.
5. Classificar estado:
   - **estado normal**: todas as leituras dentro dos limites;
   - **estado de atenção**: ao menos uma leitura fora dos limites.

## Segurança e privacidade (limitações)

- MVP sem autenticação/autorização.
- Dados são fictícios e não sensíveis.
- Sem integração externa de mensagens ou sensores.
- Não usar este protótipo como sistema de produção.

## Evolução futura (não implementada)

- Integração com microcontrolador e sensores reais.
- Persistência histórica com PostgreSQL.

## Relação com ODS

- **ODS 12**: base para decisões de consumo/produção responsáveis.
- **ODS 6**: suporte futuro à irrigação mais precisa.
- **ODS 13**: apoio a decisões de expansão orientadas por evidências.

Este MVP **não** alega impacto medido de economia de água, energia ou redução de perdas.
