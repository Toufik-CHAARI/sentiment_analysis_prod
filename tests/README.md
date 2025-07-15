# Tests pour l'API d'Analyse de Sentiment

Ce dossier contient tous les tests unitaires et d'intégration pour l'API d'analyse de sentiment.

## Structure des Tests

```
tests/
├── __init__.py
├── conftest.py              # Configuration pytest et fixtures communes
├── run_tests.py             # Script pour exécuter les tests
├── unit/                    # Tests unitaires
│   ├── __init__.py
│   ├── test_schemas.py      # Tests des schémas Pydantic
│   ├── test_sentiment_service.py  # Tests du service de sentiment
│   ├── test_error_handling.py     # Tests de gestion d'erreurs
│   └── test_performance.py        # Tests de performance
└── integration/             # Tests d'intégration
    ├── __init__.py
    └── test_endpoints.py    # Tests des endpoints API
```

## Types de Tests

### Tests Unitaires (`tests/unit/`)

- **`test_schemas.py`** : Validation des modèles Pydantic
  - Tests de validation des données d'entrée
  - Tests de validation des réponses
  - Tests des cas d'erreur de validation

- **`test_sentiment_service.py`** : Tests du service de sentiment
  - Tests d'initialisation du service
  - Tests de prédiction de sentiment
  - Tests de chargement du modèle
  - Tests de gestion d'erreurs

- **`test_error_handling.py`** : Tests de gestion d'erreurs
  - Tests d'erreurs de chargement de modèle
  - Tests d'erreurs de tokenizer
  - Tests avec différents types de texte (vide, long, caractères spéciaux)

- **`test_performance.py`** : Tests de performance
  - Tests de vitesse de prédiction
  - Tests de prédictions multiples
  - Tests d'utilisation mémoire

### Tests d'Intégration (`tests/integration/`)

- **`test_endpoints.py`** : Tests des endpoints API
  - Tests des endpoints de santé (`/`, `/health`, `/info`)
  - Tests de l'endpoint de prédiction (`/predict-sentiment/`)
  - Tests de validation des requêtes
  - Tests de gestion d'erreurs HTTP
  - Tests de la structure de l'API (OpenAPI, docs)

## Fixtures Communes (`conftest.py`)

- `client` : Client de test FastAPI
- `mock_sentiment_service` : Service de sentiment mocké
- `sample_text` : Texte d'exemple pour les tests
- `negative_text` : Texte négatif d'exemple
- `sentiment_request_data` : Données de requête pour les tests
- `sentiment_response_data` : Données de réponse pour les tests

## Exécution des Tests

### Tous les tests
```bash
python -m pytest tests/
```

### Tests unitaires uniquement
```bash
python -m pytest tests/unit/
```

### Tests d'intégration uniquement
```bash
python -m pytest tests/integration/
```

### Avec couverture de code
```bash
python -m pytest tests/ --cov=app --cov-report=html --cov-report=term
```

### Utilisation du script personnalisé
```bash
# Tous les tests
python tests/run_tests.py

# Tests unitaires
python tests/run_tests.py --type unit

# Tests d'intégration
python tests/run_tests.py --type integration

# Avec couverture
python tests/run_tests.py --coverage
```

## Couverture de Code

La couverture actuelle est de **94%** avec :
- **100%** pour les schémas et les endpoints de santé
- **82%** pour l'endpoint de sentiment (gestion d'erreurs non testée)
- **93%** pour le service de sentiment (chargement initial non testé)

## Marqueurs Pytest

- `@pytest.mark.unit` : Tests unitaires
- `@pytest.mark.integration` : Tests d'intégration
- `@pytest.mark.slow` : Tests lents (performance)

## Bonnes Pratiques

1. **Mocking** : Utilisation extensive de `unittest.mock` pour isoler les tests
2. **Fixtures** : Réutilisation des fixtures communes via `conftest.py`
3. **Validation** : Tests de validation des schémas Pydantic
4. **Gestion d'erreurs** : Tests des cas d'erreur et exceptions
5. **Performance** : Tests de temps de réponse et d'utilisation mémoire
6. **Couverture** : Objectif de maintenir une couverture > 90%

## Dépendances de Test

Les dépendances de test sont dans `requirements-test.txt` :
- `pytest` : Framework de test
- `pytest-cov` : Couverture de code
- `pytest-mock` : Support avancé pour le mocking
- `httpx` : Client HTTP pour les tests d'intégration 