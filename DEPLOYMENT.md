# Guide de Déploiement - API d'Analyse de Sentiment

Ce guide explique comment déployer l'API d'analyse de sentiment en production avec Docker et GitHub Actions.

## 🚀 Déploiement Local

### Prérequis
- Docker et Docker Compose installés
- Modèle DistilBERT dans le dossier `models/`

### Déploiement avec Docker

#### 1. Construction de l'image
```bash
# Construire l'image de production
make docker-build

# Ou avec le script de déploiement
./scripts/deploy.sh
```

#### 2. Démarrage du conteneur
```bash
# Démarrer le conteneur
make docker-run

# Vérifier que l'API fonctionne
curl http://localhost:8000/health
```

#### 3. Arrêt du conteneur
```bash
make docker-stop
```

### Déploiement avec Docker Compose

```bash
# Démarrer tous les services
make docker-compose-up

# Arrêter tous les services
make docker-compose-down

# Exécuter les tests dans un conteneur
make docker-compose-test
```

## 🔄 Pipeline CI/CD

### GitHub Actions Workflow

Le pipeline CI/CD est configuré dans `.github/workflows/ci-cd.yml` et comprend :

#### 1. **Job de Tests**
- Installation des dépendances
- Linting (flake8, black, isort)
- Tests unitaires et d'intégration
- Couverture de code (seuil 90%)
- Upload des résultats vers Codecov

#### 2. **Job de Build Docker**
- Construction de l'image Docker
- Tests de l'image
- Nettoyage automatique

#### 3. **Job de Sécurité**
- Scan de sécurité avec Bandit
- Upload des résultats

#### 4. **Jobs de Déploiement**
- Déploiement staging (branche `develop`)
- Déploiement production (branche `main`)

### Déclencheurs
- **Push** sur `main` ou `develop`
- **Pull Request** vers `main`

## 🐳 Configuration Docker

### Image de Production (`Dockerfile`)

#### Caractéristiques
- **Multi-stage build** pour optimiser la taille
- **Utilisateur non-root** pour la sécurité
- **Health check** intégré
- **Variables d'environnement** configurables
- **Seulement les fichiers nécessaires** inclus

#### Optimisations
- `.dockerignore` pour exclure les fichiers inutiles
- Cache des dépendances Python
- Image de base minimale (`python:3.12-slim`)

### Image de Test (`Dockerfile.test`)

#### Caractéristiques
- Inclut toutes les dépendances de test
- Optimisé pour l'exécution des tests
- Volume mounting pour le développement

## 🔧 Configuration de Production

### Variables d'Environnement

```bash
# Configuration de base
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info

# Configuration du modèle
MODEL_PATH=models/bert_curriculum_HF_last_version
MODEL_NAME=distilbert-base-uncased
```

### Configuration Uvicorn

```bash
# Démarrage avec uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Health Check

```bash
# Vérification de santé
curl http://localhost:8000/health
```

## 📊 Monitoring et Logs

### Logs
```bash
# Voir les logs du conteneur
docker logs sentiment-api

# Suivre les logs en temps réel
docker logs -f sentiment-api
```

### Métriques
- **Temps de réponse** : < 1 seconde
- **Couverture de tests** : 94%
- **Health check** : Toutes les 30 secondes

## 🔒 Sécurité

### Bonnes Pratiques
- **Utilisateur non-root** dans le conteneur
- **Scan de sécurité** avec Bandit
- **Dépendances minimales** dans l'image
- **Health checks** pour la surveillance

### Variables Sensibles
- Utiliser des secrets GitHub pour les variables sensibles
- Ne pas commiter les clés API dans le code
- Utiliser des variables d'environnement pour la configuration

## 🚀 Déploiement en Production

### 1. Préparation
```bash
# Vérifier que tous les tests passent
make test

# Construire l'image
make docker-build

# Tester l'image
make docker-test
```

### 2. Déploiement
```bash
# Avec le script de déploiement
./scripts/deploy.sh v1.0.0 your-registry.com

# Ou manuellement
docker tag sentiment-analysis-api:latest your-registry.com/sentiment-analysis-api:v1.0.0
docker push your-registry.com/sentiment-analysis-api:v1.0.0
```

### 3. Orchestration
```bash
# Kubernetes
kubectl apply -f k8s/

# Docker Swarm
docker stack deploy -c docker-compose.prod.yml sentiment-api

# Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Troubleshooting

### Problèmes Courants

#### 1. **Modèle non trouvé**
```bash
# Vérifier que le modèle existe
ls -la models/

# Vérifier les permissions
chmod -R 755 models/
```

#### 2. **Port déjà utilisé**
```bash
# Vérifier les conteneurs en cours
docker ps

# Arrêter le conteneur existant
make docker-stop
```

#### 3. **Mémoire insuffisante**
```bash
# Augmenter la mémoire Docker
# Dans Docker Desktop > Settings > Resources > Memory
```

#### 4. **Tests qui échouent**
```bash
# Nettoyer et relancer
make clean
make test

# Vérifier les dépendances
pip install -r requirements-test.txt
```

### Logs de Debug
```bash
# Logs détaillés
docker logs sentiment-api

# Shell dans le conteneur
docker exec -it sentiment-api /bin/bash
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Avec Docker Compose
docker-compose up -d --scale sentiment-api=3

# Avec Kubernetes
kubectl scale deployment sentiment-api --replicas=3
```

### Vertical Scaling
```bash
# Augmenter les workers
docker run -e WORKERS=8 sentiment-analysis-api:latest
```

## 🔄 Rollback

### En cas de problème
```bash
# Revenir à la version précédente
docker tag sentiment-analysis-api:previous sentiment-analysis-api:latest

# Redémarrer le service
make docker-stop
make docker-run
```

## 📋 Checklist de Déploiement

- [ ] Tous les tests passent (`make test`)
- [ ] Couverture de code > 90%
- [ ] Scan de sécurité réussi
- [ ] Image Docker construite avec succès
- [ ] Tests de l'image réussis
- [ ] Health check fonctionne
- [ ] Logs configurés
- [ ] Monitoring en place
- [ ] Rollback planifié 