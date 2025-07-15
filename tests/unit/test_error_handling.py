"""
Tests pour la gestion d'erreurs
"""
import pytest
from unittest.mock import patch, Mock
import tensorflow as tf

from app.services.sentiment_service import SentimentService


class TestErrorHandling:
    """Tests pour la gestion d'erreurs"""
    
    def test_model_loading_error(self):
        """Test d'erreur lors du chargement du modèle"""
        with patch('app.services.sentiment_service.tf.saved_model.load') as mock_load:
            mock_load.side_effect = FileNotFoundError("Model not found")
            
            service = SentimentService()
            
            with pytest.raises(FileNotFoundError):
                service._load_model()
    
    def test_tokenizer_loading_error(self):
        """Test d'erreur lors du chargement du tokenizer"""
        with patch('app.services.sentiment_service.AutoTokenizer.from_pretrained') as mock_tokenizer:
            mock_tokenizer.side_effect = Exception("Tokenizer error")
            
            service = SentimentService()
            
            with pytest.raises(Exception):
                service._load_tokenizer()
    
    def test_label_encoder_loading_error(self):
        """Test d'erreur lors du chargement du label encoder"""
        with patch('builtins.open') as mock_open:
            mock_open.side_effect = FileNotFoundError("Label encoder not found")
            
            service = SentimentService()
            
            with pytest.raises(FileNotFoundError):
                service._load_model()  # Cette méthode charge aussi le label encoder
    
    @patch('app.services.sentiment_service.tf.saved_model.load')
    @patch('app.services.sentiment_service.AutoTokenizer.from_pretrained')
    @patch('builtins.open')
    @patch('app.services.sentiment_service.pickle.load')
    def test_prediction_with_empty_text(self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model):
        """Test de prédiction avec texte vide"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()
        
        # Mock des tokens pour texte vide
        mock_tokens = {
            "input_ids": tf.constant([[1, 2]]),
            "attention_mask": tf.constant([[1, 1]])
        }
        mock_tokenizer_instance.return_value = mock_tokens
        
        # Mock de la prédiction
        mock_prediction = tf.constant([[0.6]])
        mock_model.return_value = mock_prediction
        
        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["4"]
        
        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder
        
        # Test
        service = SentimentService()
        label, confidence = service.predict_sentiment("")
        
        assert label == "4"
        # Utiliser pytest.approx pour la comparaison de float
        assert confidence == pytest.approx(0.6, rel=1e-6)
    
    @patch('app.services.sentiment_service.tf.saved_model.load')
    @patch('app.services.sentiment_service.AutoTokenizer.from_pretrained')
    @patch('builtins.open')
    @patch('app.services.sentiment_service.pickle.load')
    def test_prediction_with_very_long_text(self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model):
        """Test de prédiction avec texte très long"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()
        
        # Mock des tokens pour texte long
        mock_tokens = {
            "input_ids": tf.constant([[1] + [2] * 500 + [3]]),
            "attention_mask": tf.constant([[1] + [1] * 500 + [1]])
        }
        mock_tokenizer_instance.return_value = mock_tokens
        
        # Mock de la prédiction
        mock_prediction = tf.constant([[0.7]])
        mock_model.return_value = mock_prediction
        
        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["4"]
        
        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder
        
        # Test
        service = SentimentService()
        long_text = "This is a very long text " * 100
        label, confidence = service.predict_sentiment(long_text)
        
        assert label == "4"
        assert confidence == pytest.approx(0.7, rel=1e-6)
    
    @patch('app.services.sentiment_service.tf.saved_model.load')
    @patch('app.services.sentiment_service.AutoTokenizer.from_pretrained')
    @patch('builtins.open')
    @patch('app.services.sentiment_service.pickle.load')
    def test_prediction_with_special_characters(self, mock_pickle_load, mock_open, mock_tokenizer, mock_load_model):
        """Test de prédiction avec caractères spéciaux"""
        # Mock des composants
        mock_model = Mock()
        mock_tokenizer_instance = Mock()
        mock_label_encoder = Mock()
        
        # Mock des tokens
        mock_tokens = {
            "input_ids": tf.constant([[1, 2, 3, 4, 5]]),
            "attention_mask": tf.constant([[1, 1, 1, 1, 1]])
        }
        mock_tokenizer_instance.return_value = mock_tokens
        
        # Mock de la prédiction
        mock_prediction = tf.constant([[0.5]])
        mock_model.return_value = mock_prediction
        
        # Mock du label encoder
        mock_label_encoder.inverse_transform.return_value = ["0"]
        
        # Configuration des mocks
        mock_load_model.return_value = mock_model
        mock_tokenizer.return_value = mock_tokenizer_instance
        mock_pickle_load.return_value = mock_label_encoder
        
        # Test
        service = SentimentService()
        special_text = "This is a test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        label, confidence = service.predict_sentiment(special_text)
        
        assert label == "0"
        assert confidence == pytest.approx(0.5, rel=1e-6)
    
    def test_model_not_loaded_error(self):
        """Test d'erreur quand le modèle n'est pas chargé"""
        service = SentimentService()
        service._is_loaded = False
        service.model = None
        
        # Le modèle se charge automatiquement lors de la première prédiction
        # donc on ne peut pas tester cette erreur directement
        # On teste plutôt que le modèle se charge correctement
        with patch('app.services.sentiment_service.tf.saved_model.load') as mock_load:
            mock_load.side_effect = FileNotFoundError("Model not found")
            
            with pytest.raises(FileNotFoundError):
                service.predict_sentiment("test") 