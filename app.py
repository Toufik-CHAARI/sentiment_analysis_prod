from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pathlib
import pickle
import tensorflow as tf
from transformers import AutoTokenizer
from transformers.models.distilbert.modeling_tf_distilbert import (
    TFDistilBertModel, TFDistilBertMainLayer
)

# Créer l'instance FastAPI
app = FastAPI(
    title="Mon API Simple",
    description="Une application FastAPI simple",
    version="1.0.0"
)

# Modèle Pydantic pour les données
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str  # "0" pour négatif, "4" pour positif
    confidence: float

# Configuration du modèle DistilBERT
MODEL_PATH = pathlib.Path("models/bert_curriculum_HF_last_version")
MODEL_NAME = "distilbert-base-uncased"

# Variables globales pour le modèle, tokenizer et label encoder
model = None
tokenizer = None
label_encoder = None

def load_model():
    """Charge le modèle DistilBERT et les composants nécessaires"""
    global model, tokenizer, label_encoder
    
    try:
        # Chemin vers le modèle SavedModel
        model_dir = MODEL_PATH / "distilbert_HF_2000k"
        
        if not model_dir.exists():
            raise FileNotFoundError(f"Dossier du modèle non trouvé: {model_dir}")
        
        # Charger le modèle avec tf.saved_model.load (plus compatible)
        model = tf.saved_model.load(str(model_dir))
        
        # Charger le tokenizer
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        
        # Charger le label encoder
        le_path = MODEL_PATH / "label_encoder.pkl"
        with open(le_path, "rb") as f:
            label_encoder = pickle.load(f)
            
        print("✅ Modèle chargé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle: {e}")
        raise

def predict_sentiment(text: str):
    """Prédit le sentiment d'un texte"""
    global model, tokenizer, label_encoder
    
    if model is None or tokenizer is None or label_encoder is None:
        raise RuntimeError("Le modèle n'est pas chargé")
    
    # Tokeniser le texte
    toks = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors="tf"
    )
    
    # Faire la prédiction avec tf.saved_model.load
    # Le modèle attend un dictionnaire avec les noms des inputs
    prediction = model([toks["input_ids"], toks["attention_mask"]])
    
    # Extraire la probabilité
    if isinstance(prediction, dict):
        proba = prediction.get('dense', None)
    else:
        proba = prediction
    
    if proba is None:
        raise ValueError("Impossible d'extraire la prédiction du modèle")
    
    proba_value = proba.numpy()[0, 0]
    label_idx = int(proba_value >= 0.5)  # 0 = négatif, 1 = positif
    label = label_encoder.inverse_transform([label_idx])[0]
    
    return str(label), float(proba_value)

# Endpoint racine
@app.get("/")
async def root():
    return {"message": "Bienvenue sur mon API FastAPI!", "status": "actif"}

# Endpoint de santé
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mon-api"}

# Endpoint pour obtenir des informations
@app.get("/info")
async def get_info():
    return {
        "nom": "Mon API Simple",
        "version": "1.0.0",
        "endpoints_disponibles": [
            "GET / - Message de bienvenue",
            "GET /health - Vérification de santé",
            "GET /info - Informations de l'API",
            "GET /items - Liste des items",
            "POST /items - Créer un item",
            "GET /users - Liste des utilisateurs",
            "POST /users - Créer un utilisateur",
            "POST /predict-sentiment - Prédire le sentiment d'un texte (0=négatif, 4=positif)"
        ]
    }

# Stockage en mémoire (pour la démo)
items_db = []
users_db = []

# Endpoints pour les items
@app.get("/items")
async def get_items():
    return {"items": items_db}

@app.post("/items")
async def create_item(item: Item):
    items_db.append(item)
    return {"message": "Item créé avec succès", "item": item}

# Endpoints pour les utilisateurs
@app.get("/users")
async def get_users():
    return {"users": users_db}

@app.post("/users")
async def create_user(user: User):
    users_db.append(user)
    return {"message": "Utilisateur créé avec succès", "user": user}

# Endpoint avec paramètre de chemin
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id < len(items_db):
        return {"item": items_db[item_id]}
    return {"error": "Item non trouvé"}

# Endpoint avec paramètres de requête
@app.get("/search")
async def search_items(name: Optional[str] = None, min_price: Optional[float] = None):
    results = items_db
    
    if name:
        results = [item for item in results if name.lower() in item.name.lower()]
    
    if min_price is not None:
        results = [item for item in results if item.price >= min_price]
    
    return {"results": results}

# Endpoint de prédiction de sentiment
@app.post("/predict-sentiment", response_model=SentimentResponse)
async def predict_sentiment_endpoint(request: SentimentRequest):
    """
    Prédit le sentiment d'un texte (0 = négatif, 4 = positif)
    """
    try:
        label, confidence = predict_sentiment(request.text)
        
        return SentimentResponse(
            text=request.text,
            sentiment=label,
            confidence=confidence
        )
        
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    
    # Charger le modèle au démarrage
    print("🔄 Chargement du modèle DistilBERT...")
    load_model()
    print("🚀 Démarrage du serveur FastAPI...")
    
    uvicorn.run(app, host="0.0.0.0", port=8000) 