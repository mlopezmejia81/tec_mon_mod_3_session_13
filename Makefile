.PHONY: install test lint format clean train predict api help

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala las dependencias
	poetry install

test: ## Ejecuta todas las pruebas
	poetry run pytest

test-unit: ## Ejecuta solo las pruebas unitarias
	poetry run pytest tests/unit/

test-integration: ## Ejecuta solo las pruebas de integración
	poetry run pytest tests/integration/

test-functional: ## Ejecuta solo las pruebas funcionales
	poetry run pytest tests/functional/

test-cov: ## Ejecuta pruebas con cobertura
	poetry run pytest --cov=src/iris_ml --cov-report=html --cov-report=term-missing

lint: ## Ejecuta todos los linters
	poetry run pycodestyle src/ tests/
	poetry run pydocstyle src/ || true
	poetry run mypy src/ || true

format: ## Formatea el código con Black
	poetry run black src/ tests/

format-check: ## Verifica el formato sin cambiar archivos
	poetry run black --check src/ tests/

train: ## Entrena el modelo
	poetry run iris-train

predict: ## Realiza una predicción de ejemplo
	poetry run iris-predict

api: ## Inicia el servidor de la API
	poetry run iris-api

clean: ## Limpia archivos generados
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml dist/ build/

all: format lint test ## Ejecuta formato, linting y pruebas
