# Sentiment Analysis API

A production-ready sentiment analysis API built with FastAPI and BERT models. This API provides real-time sentiment analysis for text input with high accuracy and low latency.

## 🚀 Quick Start

```bash
# Pull the latest image
docker pull your-username/sentiment-analysis-api:latest

# Run the API
docker run -p 8000:8000 your-username/sentiment-analysis-api:latest

# Test the API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check endpoint |
| `/predict` | POST | Predict sentiment for text |
| `/docs` | GET | Interactive API documentation |
| `/redoc` | GET | Alternative API documentation |

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server host address |
| `PORT` | `8000` | Server port |
| `WORKERS` | `4` | Number of worker processes |
| `LOG_LEVEL` | `info` | Logging level |

## 📝 Example Usage

### Python
```python
import requests

# Predict sentiment
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "This is amazing!"}
)
result = response.json()
print(result["sentiment"])  # "positive"
print(result["confidence"])  # 0.95
```

### JavaScript
```javascript
// Predict sentiment
const response = await fetch('http://localhost:8000/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: "I love this product!"
    })
});

const result = await response.json();
console.log(result.sentiment); // "positive"
```

### cURL
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is terrible!"}'
```

## 🐳 Docker Compose

```yaml
version: '3.8'
services:
  sentiment-api:
    image: your-username/sentiment-analysis-api:latest
    ports:
      - "8000:8000"
    environment:
      - WORKERS=2
      - LOG_LEVEL=info
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
```

## 🏗️ Production Deployment

### AWS ECS
```yaml
# task-definition.json
{
  "family": "sentiment-api",
  "containerDefinitions": [
    {
      "name": "sentiment-api",
      "image": "your-username/sentiment-analysis-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WORKERS",
          "value": "4"
        }
      ]
    }
  ]
}
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentiment-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentiment-api
  template:
    metadata:
      labels:
        app: sentiment-api
    spec:
      containers:
      - name: sentiment-api
        image: your-username/sentiment-analysis-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: WORKERS
          value: "4"
```

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test sentiment prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'

# Expected response
{
  "sentiment": "positive",
  "confidence": 0.95,
  "text": "I love this product!"
}
```

## 📊 Performance

- **Response Time**: < 100ms average
- **Throughput**: 1000+ requests/second
- **Memory Usage**: ~2GB RAM
- **CPU Usage**: Optimized for multi-core

## 🔒 Security

- ✅ Non-root user execution
- ✅ Minimal attack surface
- ✅ Health checks
- ✅ Input validation
- ✅ Rate limiting ready

## 🛠️ Development

### Build locally
```bash
# Clone the repository
git clone https://github.com/your-username/sentiment-analysis-api.git
cd sentiment-analysis-api

# Build the image
docker build -t sentiment-analysis-api .

# Run locally
docker run -p 8000:8000 sentiment-analysis-api
```

### Run tests
```bash
# Run unit tests
docker-compose up sentiment-api-test

# Run integration tests
docker-compose up sentiment-api-integration
```

## 📈 Monitoring

### Health Checks
```bash
# Check API health
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Metrics
- Request count
- Response time
- Error rate
- Memory usage
- CPU usage

## 🔄 CI/CD

This image is automatically built and pushed to Docker Hub on:
- ✅ Push to main/master branch
- ✅ New version tags (v1.0.0, v1.1.0, etc.)
- ✅ Pull requests (build only)

## 📦 Image Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest stable version |
| `v1.0.0` | Specific version |
| `main-abc123` | Branch-specific builds |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/sentiment-analysis-api/issues)
- 📖 Documentation: [API Docs](http://localhost:8000/docs)

---

**Made with ❤️ using FastAPI and BERT** 