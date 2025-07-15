# API d'Analyse de Sentiment avec FastAPI

Une API FastAPI moderne pour l'analyse de sentiment utilisant un modèle DistilBERT pré-entraîné.

## 🚀 Fonctionnalités

- **Analyse de sentiment** : Prédiction positive/négative avec score de confiance
- **Architecture modulaire** : Structure claire avec séparation des responsabilités
- **Documentation automatique** : Swagger UI et ReDoc intégrés
- **Tests complets** : Tests unitaires et d'intégration avec 94% de couverture
- **Performance optimisée** : Chargement unique du modèle avec pattern singleton

## 📋 Prérequis

- Python 3.8+
- TensorFlow 2.16+
- Modèle DistilBERT dans le dossier `models/`

## 🛠️ Installation

1. **Cloner le projet** :
```bash
git clone <repository-url>
cd sentiment_analysis_prod
```

2. **Créer un environnement virtuel** :
```bash
python -m venv env
source env/bin/activate  # Sur macOS/Linux
# ou
env\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

4. **Installer les dépendances de test** :
```bash
pip install -r requirements-test.txt
```

## 🚀 Lancement de l'application

```bash
python main.py
```

Ou avec uvicorn directement :
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur : http://localhost:8000

## 📚 Documentation

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
- **OpenAPI Schema** : http://localhost:8000/openapi.json

## 🔌 Endpoints disponibles

### Endpoints de santé
- `GET /` - Message de bienvenue
- `GET /health` - Vérification de santé avec statut du modèle
- `GET /info` - Informations détaillées de l'API

### Endpoint d'analyse de sentiment
- `POST /predict-sentiment/` - Analyser le sentiment d'un texte

## 📖 Exemples d'utilisation

### Analyser un sentiment positif
```bash
curl -X POST "http://localhost:8000/predict-sentiment/" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "I really enjoyed this movie! It was fantastic."
     }'
```

**Réponse** :
```json
{
  "text": "I really enjoyed this movie! It was fantastic.",
  "sentiment": "4",
  "confidence": 0.95
}
```

### Analyser un sentiment négatif
```bash
curl -X POST "http://localhost:8000/predict-sentiment/" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This movie was terrible and boring."
     }'
```

**Réponse** :
```json
{
  "text": "This movie was terrible and boring.",
  "sentiment": "0",
  "confidence": 0.87
}
```

## 🏗️ Structure du projet

```
sentiment_analysis_prod/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py          # Endpoints de santé
│   │   └── sentiment.py       # Endpoint d'analyse de sentiment
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── sentiment.py       # Modèles Pydantic
│   └── services/
│       ├── __init__.py
│       └── sentiment_service.py # Service d'analyse de sentiment
├── models/                     # Modèle DistilBERT
├── tests/                      # Tests unitaires et d'intégration
│   ├── unit/                   # Tests unitaires
│   ├── integration/            # Tests d'intégration
│   ├── conftest.py            # Configuration pytest
│   └── run_tests.py           # Script d'exécution des tests
├── main.py                     # Point d'entrée de l'application
├── requirements.txt            # Dépendances principales
├── requirements-test.txt       # Dépendances de test
├── pytest.ini                 # Configuration pytest
├── Makefile                   # Commandes de test
└── README.md                  # Ce fichier
```

## 🧪 Tests

### Exécution des tests

```bash
# Tous les tests
make test

# Tests unitaires uniquement
make test-unit

# Tests d'intégration uniquement
make test-integration

# Tests avec couverture de code
make test-coverage

# Tests spécifiques
make test-schemas      # Tests des schémas
make test-service      # Tests du service
make test-errors       # Tests de gestion d'erreurs
make test-endpoints    # Tests des endpoints
```

### Couverture de code

La couverture actuelle est de **94%** :
- **100%** pour les schémas et endpoints de santé
- **82%** pour l'endpoint de sentiment
- **93%** pour le service de sentiment

### Types de tests

- **Tests unitaires** : Validation des schémas, service de sentiment, gestion d'erreurs
- **Tests d'intégration** : Endpoints API, validation des requêtes
- **Tests de performance** : Vitesse de prédiction, utilisation mémoire

## 🔧 Configuration

### Variables d'environnement

- `MODEL_PATH` : Chemin vers le modèle (défaut: `models/bert_curriculum_HF_last_version`)
- `MODEL_NAME` : Nom du modèle tokenizer (défaut: `distilbert-base-uncased`)

### Configuration pytest

Le fichier `pytest.ini` configure :
- Chemins de test
- Marqueurs personnalisés
- Options de sortie

## 🚀 Déploiement

### Développement
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 Métriques

- **Temps de réponse** : < 1 seconde par prédiction
- **Couverture de tests** : 94%
- **Endpoints** : 4 endpoints principaux
- **Modèle** : DistilBERT fine-tuné pour l'analyse de sentiment

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

