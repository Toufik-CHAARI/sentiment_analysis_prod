import pathlib
import pickle
import os
from typing import Tuple

import tensorflow as tf
from transformers import AutoTokenizer

# Set cache directory for transformers to writable location in Lambda
os.environ['TRANSFORMERS_CACHE'] = '/tmp/transformers_cache'
os.environ['HF_HOME'] = '/tmp/huggingface_cache'


class SentimentService:
    """Service pour l'analyse de sentiment avec DistilBERT"""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.label_encoder = None
        self.model_path = pathlib.Path("models/bert_curriculum_HF_last_version")
        self.model_name = "distilbert-base-uncased"
        self._is_loaded = False

    def _load_model(self):
        """Charge le modèle DistilBERT et les composants nécessaires"""
        try:
            print(f"🔍 Début du chargement du modèle...")
            print(f"📁 Répertoire de travail: {os.getcwd()}")
            print(f"📁 Cache directory: {os.environ.get('TRANSFORMERS_CACHE', 'Non défini')}")
            
            # Chemin vers le modèle SavedModel
            model_dir = self.model_path / "distilbert_HF_2000k"
            print(f"📁 Chemin du modèle: {model_dir}")

            if not model_dir.exists():
                raise FileNotFoundError(f"Dossier du modèle non trouvé: {model_dir}")

            print("🔄 Chargement du modèle TensorFlow...")
            # Charger le modèle avec tf.saved_model.load (plus compatible)
            self.model = tf.saved_model.load(str(model_dir))

            print("🔄 Chargement du tokenizer...")
            # Charger le tokenizer avec cache directory
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir='/tmp/transformers_cache'
            )

            print("🔄 Chargement du label encoder...")
            # Charger le label encoder
            le_path = self.model_path / "label_encoder.pkl"
            with open(le_path, "rb") as f:
                self.label_encoder = pickle.load(f)

            print("✅ Modèle DistilBERT chargé avec succès!")

        except Exception as e:
            print(f"❌ Erreur lors du chargement du modèle: {e}")
            import traceback
            print(f"📋 Stack trace: {traceback.format_exc()}")
            raise

    def predict_sentiment(self, text: str) -> Tuple[str, float]:
        """
        Prédit le sentiment d'un texte

        Args:
            text: Le texte à analyser

        Returns:
            Tuple[str, float]: (sentiment, confidence)
                - sentiment: "0" pour négatif, "4" pour positif
                - confidence: Score de confiance entre 0 et 1
        """
        if not self._is_loaded:
            self._load_model()
            self._is_loaded = True

        # Tokeniser le texte
        toks = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=128,
            return_tensors="tf",
        )

        # Faire la prédiction avec tf.saved_model.load
        # Le modèle attend une liste [ids, mask]
        prediction = self.model(
            [toks["input_ids"], toks["attention_mask"]], training=False
        )

        # Extraire la probabilité
        if isinstance(prediction, dict):
            proba = prediction.get("dense", None)
        else:
            proba = prediction

        if proba is None:
            raise ValueError("Impossible d'extraire la prédiction du modèle")

        proba_value = proba.numpy()[0, 0]
        label_idx = int(proba_value >= 0.5)  # 0 = négatif, 1 = positif
        label = self.label_encoder.inverse_transform([label_idx])[0]

        return str(label), float(proba_value)

    def is_model_loaded(self) -> bool:
        """Vérifie si le modèle est chargé"""
        return self._is_loaded
