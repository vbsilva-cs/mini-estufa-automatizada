VENV := venv

# Instala dependências
install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

# Executa testes com pytest e gera relatório de cobertura
test:
	$(VENV)/bin/pytest --maxfail=1 --disable-warnings -v

# Limpa arquivos temporários
clean:
	rm -rf $(VENV) __pycache__ .pytest_cache

# Target padrão
all: install test
