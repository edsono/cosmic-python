##
# Makefile
#

include .env

# Detect Operational System
# https://stackoverflow.com/questions/714100/os-detecting-makefile
ifeq ($(OS),Windows_NT)
	COPY    := copy
	PYTHON  := .\.venv\Scripts\python
	PIP-SYNC  := .\.venv\Scripts\pip-sync
	PIP-COMPILE  := .\.venv\Scripts\pip-compile
	OPEN_COV_HTML := PowerShell -Command "start chrome .\htmlcov\index.html"
else
	COPY  := cp
	SHELL := /bin/bash
	PYTHON  := .venv/bin/python3
	PIP-SYNC  := .venv/bin/pip-sync
	PIP-COMPILE  := .venv/bin/pip-compile
    UNAME_S := $(shell uname -s)
    ifeq ($(UNAME_S),Darwin)
		OPEN_COV_HTML := open htmlcov/index.html
		BROWSER := open
    endif
    ifeq ($(UNAME_S),Linux)
		OPEN_COV_HTML := google-chrome htmlcov/index.html
    endif
endif


.PHONY: help
help:
	@echo init     - inicializa o ambiente de desenvolvimento
	@echo sync     - sincroniza pacotes do pip e tabelas do sgbd
	@echo test     - teste automatizado de todo o sistema
	@echo coverage - test calculando a cobertura dos testes
	@echo -----
	@echo clean    - limpa todos os arquivos temporários
	@echo deploy   - contrói, sobe o código para o controle de versão e implanta


# Why you really need to upgrade pip:
# https://pythonspeed.com/articles/upgrade-pip/
.PHONY: init
init:
	@echo ---------------------------------------------------------------
	@echo Inicializando ambiente
	@echo ---------------------------------------------------------------
ifeq ($(OS),Windows_NT)
	PowerShell -Command "if (!(test-path -path .venv)) {py -m venv .venv}"
else
	[ -d .venv ] || $(PYTHON) -m venv .venv
endif
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pip-tools
	@echo ::: Ambiente inicializado!


.PHONY: pip-compile
pip-compile: .venv pyproject.toml
	@echo ---------------------------------------------------------------
	@echo Compilando os pacotes de pré-requisitos
	@echo ---------------------------------------------------------------
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pip-tools toml
	$(PYTHON) -c "import toml; c = toml.load('pyproject.toml');open('requirements.in', 'w').write('\n'.join(c['build-system']['requires']))"
	$(PYTHON) -c "import toml; c = toml.load('pyproject.toml');open('dev-requirements.in', 'w').write('\n'.join(c['project']['optional-dependencies']['requires']))"
	$(PIP-COMPILE) -o requirements.txt requirements.in
	$(PIP-COMPILE) -o dev-requirements.txt dev-requirements.in
	@echo ::: Ok


.PHONY: pip-sync
pip-sync: .venv requirements.txt dev-requirements.txt
	@echo ---------------------------------------------------------------
	@echo Checando o sistema
	@echo ---------------------------------------------------------------
	$(PIP-SYNC) requirements.txt dev-requirements.txt
	@echo ::: Ok


.PHONY: clean
clean:
ifeq ($(OS),Windows_NT)
	PowerShell -Command "Get-ChildItem -Include *~ -Recurse | Remove-Item -Force -Recurse"
	PowerShell -Command "Get-ChildItem -Include *.py[co] -Recurse | Remove-Item -Force -Recurse"
	PowerShell -Command "Get-ChildItem -Include __pycache__ -Recurse | Remove-Item -Force -Recurse"
else
	find . -name '*~' -exec rm -f {} +
	find . -name '*.py[co]' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
endif
	@echo ::: Ok

.PHONY: test
test:
	$(PYTHON) -m pytest -x

.PHONY: coverage
coverage: .venv
	$(PYTHON) -m pytest -x --cov-report html --cov='.'
	$(OPEN_COV_HTML)

test_all: clean test

.PHONY: deploy
deploy: .venv clean test_all
	@echo ">>>"
	@echo ">>> Deploying..."
	@echo ">>>"
	git diff-index --quiet HEAD
	$(PYTHON) -c 'v=open("VERSION").read().split(".");v[-1]=str(int(v[-1])+1);open("VERSION", "w").write(".".join(v))'
	$(PYTHON) -m build -nwx
	git add VERSION
ifeq ($(OS),Windows_NT)
	PowerShell -Command '$$env:VERSION=(gc VERSION.txt); git commit -m "v$$env:VERSION"'
	PowerShell -Command '$$env:VERSION=(gc VERSION.txt); git tag $$env:VERSION'
else
	git push origin main --tags
	git commit -m "Atualiza VERSION"
endif
	git tag "$(<VERSION)"
	@echo ::: Ok
