# Rastreabilidade de requisitos

## Requisitos funcionais

- **RF01: exibir leituras simuladas**
  - Código: `app/routes/web.py` (`dashboard`) e `app/templates/dashboard.html`
  - Teste: `tests/test_web.py::test_rf01_exibe_leituras_simuladas`

- **RF02: permitir editar limites válidos**
  - Código: `app/routes/web.py` (`/limites`) e `app/services/monitoring.py::update_limite`
  - Teste: `tests/test_web.py::test_rf02_permite_editar_limites_validos`

- **RF03: exibir alertas para valores fora dos limites**
  - Código: `app/services/monitoring.py::compare_leitura` e `app/templates/dashboard.html`
  - Teste: `tests/test_web.py::test_rf03_exibe_alerta_visual_para_fora_do_limite`

## Requisitos não funcionais

- **RNF01: resposta visual em até 2 segundos no ambiente de teste**
  - Cobertura: requisito declarado para validação manual em execução local; não há benchmark automatizado no MVP.

- **RNF02: interface responsiva, foco visível, navegação por teclado e mensagens que não dependam apenas de cor**
  - Código: `app/static/styles.css` (`:focus-visible`, media query) e templates com textos explícitos de estado.

- **RNF03: rejeitar entradas em que o mínimo seja maior ou igual ao máximo**
  - Código: `app/services/monitoring.py::update_limite`
  - Teste: `tests/test_web.py::test_rnf03_rejeita_minimo_maior_ou_igual_maximo`
