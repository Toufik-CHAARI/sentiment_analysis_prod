"""
Tests d'intégration pour les endpoints API
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app


class TestHealthEndpoints:
    """Tests pour les endpoints de santé"""
    
    def test_root_endpoint(self, client):
        """Test de l'endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "actif"
    
    def test_health_endpoint(self, client):
        """Test de l'endpoint de santé"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "model_status" in data
        assert data["status"] == "healthy"
        assert data["service"] == "sentiment-analysis-api"
    
    def test_info_endpoint(self, client):
        """Test de l'endpoint d'informations"""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "nom" in data
        assert "version" in data
        assert "description" in data
        assert "endpoints_disponibles" in data
        assert isinstance(data["endpoints_disponibles"], list)


class TestSentimentEndpoints:
    """Tests pour les endpoints de sentiment"""
    
    def test_predict_sentiment_success(self, client, mock_sentiment_service):
        """Test de prédiction de sentiment réussie"""
        with patch('app.api.sentiment.get_sentiment_service', return_value=mock_sentiment_service):
            response = client.post(
                "/predict-sentiment/",
                json={"text": "I really enjoyed this movie!"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "text" in data
            assert "sentiment" in data
            assert "confidence" in data
            assert data["text"] == "I really enjoyed this movie!"
            assert data["sentiment"] == "4"
            assert data["confidence"] == 0.95
    
    def test_predict_sentiment_negative(self, client, mock_sentiment_service):
        """Test de prédiction de sentiment négatif"""
        # Modifier le mock pour retourner un sentiment négatif
        mock_sentiment_service.predict_sentiment.return_value = ("0", 0.85)
        
        with patch('app.api.sentiment.get_sentiment_service', return_value=mock_sentiment_service):
            response = client.post(
                "/predict-sentiment/",
                json={"text": "I hate this movie!"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["sentiment"] == "0"
            assert data["confidence"] == 0.85
    
    def test_predict_sentiment_empty_text(self, client, mock_sentiment_service):
        """Test avec texte vide"""
        with patch('app.api.sentiment.get_sentiment_service', return_value=mock_sentiment_service):
            response = client.post(
                "/predict-sentiment/",
                json={"text": ""}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["text"] == ""
    
    def test_predict_sentiment_missing_text(self, client):
        """Test avec texte manquant"""
        response = client.post(
            "/predict-sentiment/",
            json={}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_sentiment_invalid_json(self, client):
        """Test avec JSON invalide"""
        response = client.post(
            "/predict-sentiment/",
            data="invalid json"
        )
        
        assert response.status_code == 422
    
    def test_predict_sentiment_service_error(self, client, mock_sentiment_service):
        """Test avec erreur du service"""
        mock_sentiment_service.predict_sentiment.side_effect = Exception("Model error")
        
        with patch('app.api.sentiment.get_sentiment_service', return_value=mock_sentiment_service):
            response = client.post(
                "/predict-sentiment/",
                json={"text": "I love this movie!"}
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data
            assert "Erreur lors de la prédiction" in data["detail"]


class TestAPIStructure:
    """Tests pour la structure de l'API"""
    
    def test_openapi_schema(self, client):
        """Test du schéma OpenAPI"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
    
    def test_docs_endpoint(self, client):
        """Test de l'endpoint de documentation"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self, client):
        """Test de l'endpoint ReDoc"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_nonexistent_endpoint(self, client):
        """Test d'un endpoint inexistant"""
        response = client.get("/nonexistent")
        assert response.status_code == 404 