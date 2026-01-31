#!/usr/bin/env make

.PHONY: help install-deps setup-playwright install clean test

# Variáveis
PYTHON := python3
PIP := pip
VENV_DIR := venv

# Cores para output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Mostra esta ajuda
	@echo "$(GREEN)scriptLattes Makefile$(NC)"
	@echo ""
	@echo "$(YELLOW)Comandos disponíveis:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: setup-venv install-deps setup-playwright ## Instalação completa (ambiente virtual + dependências + Playwright)
	@echo "$(GREEN)✓ Instalação completa concluída!$(NC)"
	@echo ""
	@echo "$(YELLOW)Para usar o scriptLattes:$(NC)"
	@echo "  source $(VENV_DIR)/bin/activate"
	@echo "  python3 scriptLattes.py exemplo/teste-01.config"

setup-venv: ## Cria e configura o ambiente virtual Python
	@echo "$(YELLOW)Criando ambiente virtual...$(NC)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✓ Ambiente virtual criado em $(VENV_DIR)$(NC)"

install-deps: ## Instala as dependências Python
	@echo "$(YELLOW)Instalando dependências Python...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Ambiente virtual não encontrado. Execute 'make setup-venv' primeiro.$(NC)"; \
		exit 1; \
	fi
	$(VENV_DIR)/bin/$(PIP) install --upgrade pip
	$(VENV_DIR)/bin/$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependências instaladas$(NC)"

setup-playwright: ## Instala os browsers do Playwright
	@echo "$(YELLOW)Instalando browsers do Playwright...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Ambiente virtual não encontrado. Execute 'make setup-venv' primeiro.$(NC)"; \
		exit 1; \
	fi
	$(VENV_DIR)/bin/playwright install chromium
	@echo "$(GREEN)✓ Playwright browsers instalados$(NC)"

test: ## Executa o exemplo de teste
	@echo "$(YELLOW)Executando teste com exemplo...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Ambiente virtual não encontrado. Execute 'make install' primeiro.$(NC)"; \
		exit 1; \
	fi
	$(VENV_DIR)/bin/$(PYTHON) scriptLattes.py exemplo/teste-01.config

test-unit: ## Executa os testes unitários
	@echo "$(YELLOW)Executando testes unitários...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)❌ Ambiente virtual não encontrado. Execute 'make install' primeiro.$(NC)"; \
		exit 1; \
	fi
	$(VENV_DIR)/bin/$(PYTHON) -m pytest tests/ -v

clean: ## Remove arquivos temporários e cache
	@echo "$(YELLOW)Limpando arquivos temporários...$(NC)"
	rm -rf cache/*
	rm -rf exemplo/teste-01
	@echo "$(GREEN)✓ Cache limpo$(NC)"

clean-all: clean ## Remove tudo (incluindo ambiente virtual)
	@echo "$(YELLOW)Removendo ambiente virtual...$(NC)"
	rm -rf $(VENV_DIR)
	@echo "$(GREEN)✓ Limpeza completa concluída$(NC)"

# Comandos para desenvolvimento
dev-install: install ## Alias para install (desenvolvimento)

lint: ## Executa verificações de linting
	@echo "$(YELLOW)Executando linting...$(NC)"
	$(VENV_DIR)/bin/black --check scriptLattes/
	$(VENV_DIR)/bin/flake8 scriptLattes/
	$(VENV_DIR)/bin/isort --check scriptLattes/
	@echo "$(GREEN)✓ Linting OK$(NC)"

format: ## Formata o código
	@echo "$(YELLOW)Formatando código...$(NC)"
	$(VENV_DIR)/bin/black scriptLattes/
	$(VENV_DIR)/bin/isort scriptLattes/
	@echo "$(GREEN)✓ Código formatado$(NC)"

status: ## Mostra o status da instalação
	@echo "$(YELLOW)Status da instalação:$(NC)"
	@echo -n "Ambiente virtual: "
	@if [ -d "$(VENV_DIR)" ]; then echo "$(GREEN)✓ Instalado$(NC)"; else echo "$(RED)❌ Não instalado$(NC)"; fi
	@echo -n "Playwright: "
	@if [ -f "$(VENV_DIR)/bin/playwright" ]; then echo "$(GREEN)✓ Instalado$(NC)"; else echo "$(RED)❌ Não instalado$(NC)"; fi