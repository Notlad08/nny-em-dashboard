# Development & Deployment Scripts
# Usage: make [target]
# Example: make start-dev

.PHONY: all init dev setup db migrate start-dev start-prod clean

all: dev

# Initialize project
init:
	pip install -r requirements.txt
	mkdir -p logs models
	touch .env

# Development environment
dev:
	docker-compose up -d api ingestion transcription pg redis
	docker-compose exec api python app/main.py

# Production environment
prod:
	docker-compose -f docker-compose.prod.yml up -d

# Database setup
db:
	docker-compose exec pg psql -U postgres -d nny_em_dashboard -c "CREATE EXTENSION IF NOT EXISTS timescale;"

# Database migrations
migrate:
	docker-compose exec api python app/core/run_migrations.py

# Start services
start-dev:
	docker-compose up -d

start-prod:
	docker-compose -f docker-compose.prod.yml up -d

# Clean up
clean:
	docker-compose down -v
	rm -rf venv/ .venv/ env/

# Build images
build:
	docker-compose build
	docker-compose -f docker-compose.prod.yml build

# Test
test:
	pytest

# Lint
lint:
	flake8 api/ ingestion/ transcription/
	isort api/ ingestion/ transcription/
	black api/ ingestion/ transcription/

# Format
format:
	black api/ ingestion/ transcription/
	isort api/ ingestion/ transcription/

# Health check
health:
	docker-compose exec api python app/core/health_check.py

# Help
help:
	@echo "Development & Deployment Scripts"
	@echo "================================"
	@echo "make init              - Initialize project (install deps, create dirs)"
	@echo "make dev               - Start development environment"
	@echo "make prod              - Start production environment"
	@echo "make db                - Set up database (create Timescale extension)"
	@echo "make migrate           - Run database migrations"
	@echo "make start-dev         - Alias for make dev"
	@echo "make start-prod        - Alias for make prod with prod config"
	@echo "make clean             - Stop containers and remove volumes"
	@echo "make build             - Build all Docker images"
	@echo "make test              - Run pytest tests"
	@echo "make lint              - Run flake8, isort, black"
	@echo "make format            - Run black and isort formatting"
	@echo "make health            - Run health check on all services"
