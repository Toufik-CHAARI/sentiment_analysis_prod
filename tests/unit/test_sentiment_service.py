"""
Tests unitaires pour le service de sentiment
"""

from unittest.mock import Mock, patch

import pytest
import tensorflow as tf

from app.services.sentiment_service import SentimentService


class TestSentimentService:
    """Tests pour SentimentService"""

    @patch("app.services.sentiment_service.tf.saved_model.load")
    @patch("app.services.sentiment_service.AutoTokenizer.from_pretrained")
    @patch("builtins.open")
    @patch("app.services.sentiment_service.pickle.load")
    def test_init_success(
        self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model
    ):
        """Test d'initialisation réussie"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()

        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder

        # Test
        service = SentimentService()

        assert service.model is None  # Pas chargé au début
        assert service.tokenizer is None
        assert service.label_encoder is None
        assert service._is_loaded is False

    @patch("app.services.sentiment_service.tf.saved_model.load")
    @patch("app.services.sentiment_service.AutoTokenizer.from_pretrained")
    @patch("builtins.open")
    @patch("app.services.sentiment_service.pickle.load")
    def test_predict_sentiment_success(
        self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model
    ):
        """Test de prédiction réussie"""
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
        label, confidence = service.predict_sentiment("I love this movie!")

        assert label == "4"
        assert confidence == pytest.approx(0.8, rel=1e-6)
        assert service._is_loaded is True

    @patch("app.services.sentiment_service.tf.saved_model.load")
    @patch("app.services.sentiment_service.AutoTokenizer.from_pretrained")
    @patch("builtins.open")
    @patch("app.services.sentiment_service.pickle.load")
    def test_predict_sentiment_negative(
        self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model
    ):
        """Test de prédiction négative"""
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

        # Mock de la prédiction (probabilité < 0.5)
        mock_prediction = tf.constant([[0.3]])
        mock_model.return_value = mock_prediction

        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["0"]

        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder

        # Test
        service = SentimentService()
        label, confidence = service.predict_sentiment("I hate this movie!")

        assert label == "0"
        assert confidence == pytest.approx(0.3, rel=1e-6)

    def test_predict_sentiment_model_not_loaded(self):
        """Test avec modèle non chargé"""
        service = SentimentService()
        service._is_loaded = False
        service.model = None

        # Le modèle se charge automatiquement lors de la première prédiction
        # donc on teste plutôt une erreur de chargement
        with patch("app.services.sentiment_service.tf.saved_model.load") as mock_load:
            mock_load.side_effect = FileNotFoundError("Model not found")

            with pytest.raises(FileNotFoundError):
                service.predict_sentiment("test")

    @patch("app.services.sentiment_service.tf.saved_model.load")
    def test_load_model_file_not_found(self, mock_load_model):
        """Test avec fichier modèle non trouvé"""
        mock_load_model.side_effect = FileNotFoundError("Model not found")

        with pytest.raises(FileNotFoundError):
            service = SentimentService()
            service._load_model()

    def test_is_model_loaded(self):
        """Test de vérification du chargement du modèle"""
        service = SentimentService()

        # Non chargé
        service._is_loaded = False
        assert service.is_model_loaded() is False

        # Chargé
        service._is_loaded = True
        assert service.is_model_loaded() is True
