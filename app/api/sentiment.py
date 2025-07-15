from fastapi import APIRouter, HTTPException
from app.schemas import SentimentRequest, SentimentResponse
from app.services.sentiment_service import SentimentService

router = APIRouter(prefix="/predict-sentiment", tags=["sentiment"])

# Instance singleton du service de sentiment
_sentiment_service = None

def get_sentiment_service():
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = SentimentService()
    return _sentiment_service


@router.post("/", response_model=SentimentResponse)
async def predict_sentiment(request: SentimentRequest):
    """
    Prédit le sentiment d'un texte (0 = négatif, 4 = positif)
    """
    try:
        sentiment_service = get_sentiment_service()
        label, confidence = sentiment_service.predict_sentiment(request.text)
        
        return SentimentResponse(
            text=request.text,
            sentiment=label,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        ) 