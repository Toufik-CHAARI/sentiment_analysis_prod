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

# Docker commands
docker-build:
	docker build -t sentiment-analysis-api:latest .

docker-build-test:
	docker build -f Dockerfile.test -t sentiment-analysis-api:test .

docker-run:
	docker run -d --name sentiment-api -p 8000:8000 sentiment-analysis-api:latest

docker-stop:
	docker stop sentiment-api || true
	docker rm sentiment-api || true

docker-test:
	docker run --rm sentiment-analysis-api:test

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

docker-compose-test:
	docker-compose run --rm sentiment-api-test

# Docker Hub commands
docker-hub-login:
	@echo "🔐 Logging in to Docker Hub..."
	docker login

docker-hub-build:
	@echo "🐳 Building Docker image for Docker Hub..."
	docker build --no-cache -t $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION) .
	docker tag $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION) $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest

docker-hub-test:
	@echo "🧪 Testing Docker Hub image..."
	docker run -d --name test-sentiment-api -p 8000:8000 $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)
	@sleep 10
	@curl -f http://localhost:8000/health || (docker logs test-sentiment-api && docker stop test-sentiment-api && docker rm test-sentiment-api && exit 1)
	@docker stop test-sentiment-api && docker rm test-sentiment-api
	@echo "✅ Docker Hub image test passed"

docker-hub-push:
	@echo "📤 Pushing to Docker Hub..."
	docker push $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)
	docker push $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest

docker-hub-publish: docker-hub-login docker-hub-build docker-hub-test docker-hub-push
	@echo "🎉 Successfully published to Docker Hub!"
	@echo "Image: $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)"
	@echo "URL: https://hub.docker.com/r/$(DOCKER_HUB_USERNAME)/sentiment-analysis-api"

docker-hub-run:
	@echo "🚀 Running from Docker Hub..."
	docker run -p 8000:8000 $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)

# Production deployment commands
deploy-prod:
	@echo "🚀 Deploying to production..."
	@./scripts/deploy-prod.sh

deploy-prod-version:
	@echo "🚀 Deploying specific version to production..."
	@read -p "Enter version (e.g., v1.0.0): " version; \
	./scripts/deploy-prod.sh $$version

deploy-prod-force:
	@echo "🚀 Force deploying to production (skip tests)..."
	@DOCKER_HUB_USERNAME=$(DOCKER_HUB_USERNAME) \
	docker build --no-cache -t $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest . && \
	docker push $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest

# Docker Hub production commands
docker-hub-prod-build:
	@echo "🐳 Building production Docker image..."
	docker build --no-cache -t $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest .
	docker tag $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)

docker-hub-prod-test:
	@echo "🧪 Testing production Docker image..."
	docker run -d --name prod-test-api -p 8000:8000 $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest
	@sleep 15
	@curl -f http://localhost:8000/health || (docker logs prod-test-api && docker stop prod-test-api && docker rm prod-test-api && exit 1)
	@curl -f -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text": "I love this product!"}' || (docker logs prod-test-api && docker stop prod-test-api && docker rm prod-test-api && exit 1)
	@docker stop prod-test-api && docker rm prod-test-api
	@echo "✅ Production image test passed"

docker-hub-prod-push:
	@echo "📤 Pushing production image to Docker Hub..."
	docker push $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:latest
	docker push $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)

docker-hub-prod-deploy: docker-hub-prod-build docker-hub-prod-test docker-hub-prod-push
	@echo "🎉 Production deployment successful!"
	@echo "Image: $(DOCKER_HUB_USERNAME)/sentiment-analysis-api:$(VERSION)"
	@echo "URL: https://hub.docker.com/r/$(DOCKER_HUB_USERNAME)/sentiment-analysis-api"

# Linting and formatting
lint:
	flake8 app/ tests/ --max-line-length=88 --extend-ignore=E203,W503

format:
	black app/ tests/
	isort app/ tests/

format-check:
	black --check app/ tests/
	isort --check-only app/ tests/

security-scan:
	bandit -r app/ -f json -o bandit-report.json

# Nettoyage des fichiers de test
clean:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Nettoyage Docker
clean-docker:
	docker system prune -f
	docker image prune -f

# Aide
help:
	@echo "Commandes disponibles:"
	@echo ""
	@echo "Tests:"
	@echo "  make test              - Exécuter tous les tests"
	@echo "  make test-unit         - Tests unitaires uniquement"
	@echo "  make test-integration  - Tests d'intégration uniquement"
	@echo "  make test-coverage     - Tests avec couverture de code"
	@echo "  make test-performance  - Tests de performance"
	@echo "  make test-schemas      - Tests des schémas"
	@echo "  make test-service      - Tests du service"
	@echo "  make test-errors       - Tests de gestion d'erreurs"
	@echo "  make test-endpoints    - Tests des endpoints"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build      - Construire l'image Docker"
	@echo "  make docker-build-test - Construire l'image de test"
	@echo "  make docker-run        - Démarrer le conteneur"
	@echo "  make docker-stop       - Arrêter le conteneur"
	@echo "  make docker-test       - Tester l'image Docker"
	@echo "  make docker-compose-up - Démarrer avec docker-compose"
	@echo "  make docker-compose-down - Arrêter docker-compose"
	@echo "  make docker-compose-test - Tests avec docker-compose"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint              - Vérifier le style de code"
	@echo "  make format            - Formater le code"
	@echo "  make format-check      - Vérifier le formatage"
	@echo "  make security-scan     - Scan de sécurité"
	@echo ""
	@echo "Nettoyage:"
	@echo "  make clean             - Nettoyer les fichiers de test"
	@echo "  make clean-docker      - Nettoyer Docker"
	@echo "  make install-test      - Installer les dépendances de test"
	@echo "  make help              - Afficher cette aide" 