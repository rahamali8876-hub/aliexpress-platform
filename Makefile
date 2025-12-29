# -------------------------------
# Global config
# -------------------------------
DOCKER=docker
COMPOSE=docker compose
SERVICE_API=api
SERVICE_DB=db

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
	@echo "  make observe-up-build Start all services with observability and build"
	@echo "  make observe         Start all services with observability"
	@echo "  make up              Start all services"
	@echo "  make up-build        Start all services with build"
	@echo "  make down            Stop and remove containers + volumes"
	@echo "  make restart         Restart services"
	@echo "  make logs-api        Follow API logs"
	@echo "  make logs-db         Follow DB logs"
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
# 	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml up -d
	$(COMPOSE) -f docker-compose.yml up -d

observe-up-build:
# 	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml up -d --build
	$(COMPOSE) -f docker-compose.yml up -d --build

ps:
	$(COMPOSE) ps

ps-stoped:
	$(COMPOSE) ps -a

up:
	$(COMPOSE) up -d

up-build:
	$(COMPOSE) up -d --build

down:
	$(COMPOSE) -f docker-compose.yml down -v
# 	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml down -v

restart:
	$(COMPOSE) down
	$(COMPOSE) -f docker-compose.yml up -d --build
# 	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml up -d --build

stop:
	$(COMPOSE) -f docker-compose.yml -f docker-compose.observability.yml stop

stop-api:
	$(DOCKER) stop api

stop-es:
	$(DOCKER) stop aliexpress_elasticsearch

stop-prometheus:
	$(DOCKER) stop aliexpress_prometheus

restart-prometheus:
	$(DOCKER) restart aliexpress_prometheus	

restart-api:
	$(DOCKER) restart api

logs-api:
	$(COMPOSE) logs -f $(SERVICE_API)

logs-db:
	$(COMPOSE) logs -f $(SERVICE_DB)

shell:
	$(COMPOSE) exec $(SERVICE_API) bash

python-shell:
	docker exec -it aliexpress_api python manage.py runserver
	
# -------------------------------
# Django
# -------------------------------

# -------------------------------
# restart python app inside the container
# -------------------------------

# docker compose restart api
restart-api:
	$(COMPOSE) restart $(SERVICE_API)

superuser:
	$(COMPOSE) exec $(SERVICE_API) python manage.py createsuperuser

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
