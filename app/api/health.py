from fastapi import APIRouter
from app.services.sentiment_service import SentimentService

router = APIRouter(tags=["health"])

# Instance singleton du service de sentiment
_sentiment_service = None

def get_sentiment_service():
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = SentimentService()
    return _sentiment_service


@router.get("/")
async def root():
    """Endpoint racine avec message de bienvenue"""
    return {
        "message": "Bienvenue sur mon API FastAPI!", 
        "status": "actif"
    }


@router.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    sentiment_service = get_sentiment_service()
    model_status = "healthy" if sentiment_service.is_model_loaded() else "unhealthy"
    
    return {
        "status": "healthy",
        "service": "sentiment-analysis-api",
        "model_status": model_status
    }


@router.get("/info")
async def get_info():
    """Informations sur l'API et ses endpoints"""
    return {
        "nom": "Mon API Simple",
        "version": "1.0.0",
        "description": "Une application FastAPI simple avec analyse de sentiment",
        "endpoints_disponibles": [
            "GET / - Message de bienvenue",
            "GET /health - Vérification de santé",
            "GET /info - Informations de l'API",
            "GET /items - Liste des items",
            "POST /items - Créer un item",
            "GET /items/{id} - Obtenir un item spécifique",
            "GET /items/search - Rechercher des items",
            "GET /users - Liste des utilisateurs",
            "POST /users - Créer un utilisateur",
            "POST /predict-sentiment - Prédire le sentiment d'un texte (0=négatif, 4=positif)"
        ]
    } 