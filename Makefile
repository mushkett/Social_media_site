.DEFAULT_GOAL := help

PYTHON = .venv/bin/python
PIP    = .venv/bin/pip
PYTEST = .venv/bin/pytest
PYLINT = .venv/bin/pylint

.PHONY: help dev lint check test coverage migrate migrations shell install db

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies (including dev) into .venv
	python3 -m venv .venv
	$(PIP) install -r requirements-dev.txt

dev: ## Run development server
	$(PYTHON) manage.py runserver

lint: ## Run pylint
	$(PYLINT) accounts groups posts social_media

check: ## Run Django system checks
	$(PYTHON) manage.py check

test: ## Run tests
	$(PYTEST)

coverage: ## Run tests with coverage report
	$(PYTEST) --cov=. --cov-report=html --cov-report=term-missing

migrate: ## Apply migrations
	$(PYTHON) manage.py migrate

migrations: ## Create new migrations
	$(PYTHON) manage.py makemigrations

shell: ## Open Django shell
	$(PYTHON) manage.py shell_plus

db: ## Start PostgreSQL via Docker
	docker compose up -d db
