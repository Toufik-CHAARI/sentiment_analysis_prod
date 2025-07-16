"""
Tests unitaires pour les schémas Pydantic
"""

import pytest
from pydantic import ValidationError

from app.schemas.sentiment import SentimentRequest, SentimentResponse


class TestSentimentRequest:
    """Tests pour SentimentRequest"""

    def test_valid_request(self):
        """Test avec des données valides"""
        data = {"text": "I love this movie!"}
        request = SentimentRequest(**data)
        assert request.text == "I love this movie!"

    def test_empty_text(self):
        """Test avec un texte vide"""
        data = {"text": ""}
        request = SentimentRequest(**data)
        assert request.text == ""

    def test_missing_text(self):
        """Test avec texte manquant"""
        with pytest.raises(ValidationError):
            SentimentRequest()

    def test_invalid_type(self):
        """Test avec type invalide"""
        with pytest.raises(ValidationError):
            SentimentRequest(text=123)


class TestSentimentResponse:
    """Tests pour SentimentResponse"""

    def test_valid_response(self):
        """Test avec des données valides"""
        data = {"text": "I love this movie!", "sentiment": "4", "confidence": 0.95}
        response = SentimentResponse(**data)
        assert response.text == "I love this movie!"
        assert response.sentiment == "4"
        assert response.confidence == 0.95

    def test_negative_sentiment(self):
        """Test avec sentiment négatif"""
        data = {"text": "I hate this movie!", "sentiment": "0", "confidence": 0.85}
        response = SentimentResponse(**data)
        assert response.sentiment == "0"

    def test_confidence_range(self):
        """Test avec différents niveaux de confiance"""
        data = {"text": "Test", "sentiment": "4", "confidence": 0.0}
        response = SentimentResponse(**data)
        assert response.confidence == 0.0

        data["confidence"] = 1.0
        response = SentimentResponse(**data)
        assert response.confidence == 1.0

    def test_missing_fields(self):
        """Test avec champs manquants"""
        with pytest.raises(ValidationError):
            SentimentResponse(text="test")

        with pytest.raises(ValidationError):
            SentimentResponse(sentiment="4", confidence=0.5)

    def test_invalid_confidence_type(self):
        """Test avec type de confiance invalide"""
        with pytest.raises(ValidationError):
            SentimentResponse(text="test", sentiment="4", confidence="high")
