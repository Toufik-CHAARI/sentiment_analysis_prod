.PHONY: test test-unit test-integration test-coverage install-test clean

# Variables
PYTHON = python
PIP = pip
PYTEST = python -m pytest

# Installation des dépendances de test
install-test:
	$(PIP) install -r requirements-test.txt

# Exécution de tous les tests
test: install-test
	$(PYTEST) tests/ -v

# Tests unitaires uniquement
test-unit: install-test
	$(PYTEST) tests/unit/ -v

# Tests d'intégration uniquement
test-integration: install-test
	$(PYTEST) tests/integration/ -v

# Tests avec couverture de code
test-coverage: install-test
	$(PYTEST) tests/ --cov=app --cov-report=html --cov-report=term

# Tests avec couverture détaillée
test-coverage-detail: install-test
	$(PYTEST) tests/ --cov=app --cov-report=html --cov-report=term --cov-report=xml

# Tests de performance uniquement
test-performance: install-test
	$(PYTEST) tests/unit/test_performance.py -v

# Tests de validation des schémas
test-schemas: install-test
	$(PYTEST) tests/unit/test_schemas.py -v

# Tests du service
test-service: install-test
	$(PYTEST) tests/unit/test_sentiment_service.py -v

# Tests d'erreurs
test-errors: install-test
	$(PYTEST) tests/unit/test_error_handling.py -v

# Tests des endpoints
test-endpoints: install-test
	$(PYTEST) tests/integration/test_endpoints.py -v

# Nettoyage des fichiers de test
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Aide
help:
	@echo "Commandes disponibles:"
	@echo "  make test              - Exécuter tous les tests"
	@echo "  make test-unit         - Tests unitaires uniquement"
	@echo "  make test-integration  - Tests d'intégration uniquement"
	@echo "  make test-coverage     - Tests avec couverture de code"
	@echo "  make test-performance  - Tests de performance"
	@echo "  make test-schemas      - Tests des schémas"
	@echo "  make test-service      - Tests du service"
	@echo "  make test-errors       - Tests de gestion d'erreurs"
	@echo "  make test-endpoints    - Tests des endpoints"
	@echo "  make install-test      - Installer les dépendances de test"
	@echo "  make clean             - Nettoyer les fichiers de test"
	@echo "  make help              - Afficher cette aide" 