"""
Application FastAPI principale - Version refactorisée
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    sentiment_router,
    health_router
)

# Créer l'instance FastAPI
app = FastAPI(
    title="API d'Analyse de Sentiment",
    description="Une application FastAPI moderne avec analyse de sentiment DistilBERT",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(health_router)
app.include_router(sentiment_router)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage du serveur FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000) 