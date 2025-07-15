from pydantic import BaseModel


class SentimentRequest(BaseModel):
    """Schéma pour la requête de prédiction de sentiment"""
    text: str


class SentimentResponse(BaseModel):
    """Schéma pour la réponse de prédiction de sentiment"""
    text: str
    sentiment: str  # "0" pour négatif, "4" pour positif
    confidence: float 