"""
Configuration pytest avec fixtures communes
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from main import app
from app.services.sentiment_service import SentimentService


@pytest.fixture
def client():
    """Client de test FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_sentiment_service():
    """Service de sentiment mocké pour les tests"""
    with patch('app.services.sentiment_service.SentimentService') as mock:
        service = Mock(spec=SentimentService)
        service.predict_sentiment.return_value = ("4", 0.95)
        service.is_model_loaded.return_value = True
        mock.return_value = service
        yield service


@pytest.fixture
def sample_text():
    """Texte d'exemple pour les tests"""
    return "I really enjoyed this movie!"


@pytest.fixture
def negative_text():
    """Texte négatif d'exemple"""
    return "This movie was terrible and boring."


@pytest.fixture
def sentiment_request_data():
    """Données de requête pour les tests de sentiment"""
    return {"text": "I really enjoyed this movie!"}


@pytest.fixture
def sentiment_response_data():
    """Données de réponse pour les tests de sentiment"""
    return {
        "text": "I really enjoyed this movie!",
        "sentiment": "4",
        "confidence": 0.95
    } 