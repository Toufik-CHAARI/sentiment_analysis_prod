# Application FastAPI Simple

Une application FastAPI simple avec des endpoints basiques pour gérer des items et des utilisateurs.

## Installation

1. Créer un environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Sur macOS/Linux
# ou
env\Scripts\activate  # Sur Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
python app.py
```

Ou avec uvicorn directement :
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

L'application sera accessible sur : http://localhost:8000

## Documentation automatique

- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## Endpoints disponibles

### Endpoints de base
- `GET /` - Message de bienvenue
- `GET /health` - Vérification de santé
- `GET /info` - Informations de l'API

### Gestion des items
- `GET /items` - Liste tous les items
- `POST /items` - Créer un nouvel item
- `GET /items/{item_id}` - Obtenir un item spécifique
- `GET /search?name=...&min_price=...` - Rechercher des items

### Gestion des utilisateurs
- `GET /users` - Liste tous les utilisateurs
- `POST /users` - Créer un nouvel utilisateur

## Exemples d'utilisation

### Créer un item
```bash
curl -X POST "http://localhost:8000/items" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Ordinateur",
       "description": "Ordinateur portable",
       "price": 999.99,
       "is_available": true
     }'
```

### Créer un utilisateur
```bash
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "age": 30
     }'
```

### Rechercher des items
```bash
curl "http://localhost:8000/search?name=ordinateur&min_price=500"
```

## Structure du projet

```
.
├── app.py              # Application FastAPI principale
├── requirements.txt    # Dépendances Python
├── README.md          # Ce fichier
└── env/               # Environnement virtuel (créé automatiquement)
```