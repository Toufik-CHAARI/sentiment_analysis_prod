"""
Tests de performance pour le service de sentiment
"""

import time
from unittest.mock import Mock, patch

import pytest
import tensorflow as tf

from app.services.sentiment_service import SentimentService


class TestPerformance:
    """Tests de performance"""

    @patch("app.services.sentiment_service.tf.saved_model.load")
    @patch("app.services.sentiment_service.AutoTokenizer.from_pretrained")
    @patch("builtins.open")
    @patch("app.services.sentiment_service.pickle.load")
    def test_prediction_speed(
        self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model
    ):
        """Test de la vitesse de prédiction"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()

        # Mock des tokens
        mock_tokens = {
            "input_ids": tf.constant([[1, 2, 3, 4, 5]]),
            "attention_mask": tf.constant([[1, 1, 1, 1, 1]]),
        }
        mock_tokenizer_instance.return_value = mock_tokens

        # Mock de la prédiction
        mock_prediction = tf.constant([[0.8]])
        mock_model.return_value = mock_prediction

        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["4"]

        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder

        # Test
        service = SentimentService()

        # Mesurer le temps de prédiction
        start_time = time.time()
        label, confidence = service.predict_sentiment("I love this movie!")
        end_time = time.time()

        prediction_time = end_time - start_time

        # Vérifier que la prédiction est rapide (< 1 seconde)
        assert prediction_time < 1.0
        assert label == "4"
        assert confidence == pytest.approx(0.8, rel=1e-6)

    @patch("app.services.sentiment_service.tf.saved_model.load")
    @patch("app.services.sentiment_service.AutoTokenizer.from_pretrained")
    @patch("builtins.open")
    @patch("app.services.sentiment_service.pickle.load")
    def test_multiple_predictions(
        self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model
    ):
        """Test de prédictions multiples"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()

        # Mock des tokens
        mock_tokens = {
            "input_ids": tf.constant([[1, 2, 3, 4, 5]]),
            "attention_mask": tf.constant([[1, 1, 1, 1, 1]]),
        }
        mock_tokenizer_instance.return_value = mock_tokens

        # Mock de la prédiction
        mock_prediction = tf.constant([[0.8]])
        mock_model.return_value = mock_prediction

        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["4"]

        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder

        # Test
        service = SentimentService()

        texts = [
            "I love this movie!",
            "This is amazing!",
            "Great film!",
            "Excellent work!",
            "Fantastic!",
        ]

        start_time = time.time()
        results = []
        for text in texts:
            label, confidence = service.predict_sentiment(text)
            results.append((label, confidence))
        end_time = time.time()

        total_time = end_time - start_time

        # Vérifier que toutes les prédictions sont correctes
        assert len(results) == 5
        for label, confidence in results:
            assert label == "4"
            assert confidence == pytest.approx(0.8, rel=1e-6)

        # Vérifier que le temps total est raisonnable (< 5 secondes)
        assert total_time < 5.0

    def test_memory_usage(self):
        """Test d'utilisation mémoire (simulation)"""
        # Ce test simule une vérification d'utilisation mémoire
        # En pratique, on utiliserait psutil ou memory_profiler

        service = SentimentService()

        # Vérifier que l'objet est créé sans erreur
        assert service is not None
        assert hasattr(service, "model")
        assert hasattr(service, "tokenizer")
        assert hasattr(service, "label_encoder")
