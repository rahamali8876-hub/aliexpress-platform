# -------------------------------
# Global config
# -------------------------------
COMPOSE=docker compose
SERVICE_API=api

.DEFAULT_GOAL := help
.PHONY: help up down restart logs shell \
        migrate makemigrations \
        test unit integration saga chaos contract \
        test-products test-orders test-payments \
        coverage lint format clean reset-db ci

# -------------------------------
# Help
# -------------------------------
help:
	@echo ""
	@echo "🚀 AliExpress Platform – Make Commands"
	@echo ""
	@echo "Infrastructure:"
	@echo "  make observe         Start all services with observability"
	@echo "  make up              Start all services"
	@echo "  make up-build        Start all services with build"
	@echo "  make down            Stop and remove containers + volumes"
	@echo "  make restart         Restart services"
	@echo "  make logs            Follow API logs"
	@echo "  make shell           Enter API container shell"
	@echo ""
	@echo "Django:"
	@echo "  make migrate         Apply migrations"
	@echo "  make makemigrations  Create migrations"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make unit            Run unit tests"
	@echo "  make integration     Run integration tests"
	@echo "  make saga            Run saga tests"
	@echo "  make chaos           Run chaos tests"
	@echo "  make contract        Run contract tests"
	@echo ""
	@echo "Domain-specific tests:"
	@echo "  make test-products"
	@echo "  make test-orders"
	@echo "  make test-payments"
	@echo ""
	@echo "Quality:"
	@echo "  make coverage        Run tests with coverage"
	@echo "  make lint            Run lint checks"
	@echo "  make format          Auto-format code"
	@echo ""
	@echo "CI:"
	@echo "  make ci              CI pipeline command"
	@echo ""

# -------------------------------
# Infrastructure
# -------------------------------
observe:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml up -d --build

up:
	$(COMPOSE) up -d

up-build:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) down -v

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d --build

logs:
	$(COMPOSE) logs -f $(SERVICE_API)

shell:
	$(COMPOSE) exec $(SERVICE_API) bash

# -------------------------------
# Django
# -------------------------------
migrate:
	$(COMPOSE) exec $(SERVICE_API) python manage.py migrate

makemigrations:
	$(COMPOSE) exec $(SERVICE_API) python manage.py makemigrations

# -------------------------------
# Testing (global)
# -------------------------------
test:
	$(COMPOSE) exec $(SERVICE_API) pytest -vv

unit:
	$(COMPOSE) exec $(SERVICE_API) pytest -m unit -vv

integration:
	$(COMPOSE) exec $(SERVICE_API) pytest -m integration -vv

saga:
	$(COMPOSE) exec $(SERVICE_API) pytest -m saga -vv

chaos:
	$(COMPOSE) exec $(SERVICE_API) pytest -m chaos -vv

contract:
	$(COMPOSE) exec $(SERVICE_API) pytest -m contract -vv

# -------------------------------
# Domain-specific testing
# -------------------------------
test-products:
	$(COMPOSE) exec $(SERVICE_API) pytest core/domains/products -vv

test-orders:
	$(COMPOSE) exec $(SERVICE_API) pytest core/domains/orders -vv

test-payments:
	$(COMPOSE) exec $(SERVICE_API) pytest core/domains/payments -vv

# -------------------------------
# Quality
# -------------------------------
coverage:
	$(COMPOSE) exec $(SERVICE_API) pytest --cov=core --cov-report=term-missing

lint:
	$(COMPOSE) exec $(SERVICE_API) flake8 core

format:
	$(COMPOSE) exec $(SERVICE_API) black core

# -------------------------------
# Database
# -------------------------------
reset-db:
	$(COMPOSE) down -v
	$(COMPOSE) up -d --build
	$(COMPOSE) exec $(SERVICE_API) python manage.py migrate

# -------------------------------
# CI Pipeline
# -------------------------------
ci:
	make unit
	make integration
	make saga
	make contract
	make coverage
