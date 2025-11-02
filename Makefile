.PHONY: help install test clean run format lint docker-build docker-run

help:
	@echo "NEO: Neural Executive Operator - Makefile Commands"
	@echo "=================================================="
	@echo "install        Install NEO and dependencies"
	@echo "test           Run test suite"
	@echo "test-cov       Run tests with coverage report"
	@echo "run            Run NEO in interactive mode"
	@echo "format         Format code with black"
	@echo "lint           Run linters (flake8)"
	@echo "clean          Remove build artifacts and cache"
	@echo "docker-build   Build Docker image"
	@echo "docker-run     Run NEO in Docker"
	@echo "docs           Build documentation"

install:
	@echo "Installing NEO..."
	chmod +x scripts/*.sh
	./scripts/install.sh

test:
	@echo "Running tests..."
	python -m pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	python -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

run:
	@echo "Starting NEO..."
	python -m src.main --mode interactive

format:
	@echo "Formatting code..."
	black src/ tests/ config/
	@echo "Code formatted!"

lint:
	@echo "Running linters..."
	flake8 src/ tests/ --max-line-length=120
	@echo "Linting complete!"

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf build/ dist/ htmlcov/
	@echo "Cleanup complete!"

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-run:
	@echo "Running NEO in Docker..."
	docker-compose up -d
	docker exec -it neo-assistant python -m src.main --mode interactive

docs:
	@echo "Building documentation..."
	cd docs && make html
	@echo "Documentation built: docs/_build/html/index.html"

.DEFAULT_GOAL := help
