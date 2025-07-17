# Docker Hub Setup Guide

This guide will help you set up Docker Hub automation and CI/CD for your sentiment analysis API.

## 🚀 Quick Setup

### 1. Create Docker Hub Account
1. Go to [Docker Hub](https://hub.docker.com)
2. Create an account
3. Note your username (e.g., `your-username`)

### 2. Set Up GitHub Secrets
1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add these secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### 3. Generate Docker Hub Access Token
1. Go to Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Give it a name (e.g., "GitHub Actions")
4. Copy the token and add it to GitHub secrets as `DOCKERHUB_TOKEN`

### 4. Update Configuration
Replace `your-username` with your actual Docker Hub username in:
- `Makefile` (line with `DOCKER_HUB_USERNAME`)
- `scripts/deploy-prod.sh` (line with `DOCKER_HUB_USERNAME`)
- `dockerhub-readme.md` (all instances)

## 🔄 CI/CD Workflow

### Automatic Triggers
- **Push to main/master**: Builds and pushes `latest` tag
- **New version tag**: Builds and pushes versioned tag (e.g., `v1.0.0`)
- **Pull requests**: Builds and tests (no push)

### Manual Deployment
```bash
# Deploy to production
make deploy-prod

# Deploy specific version
make deploy-prod-version

# Force deploy (skip tests)
make deploy-prod-force
```

## 📦 Image Tags

| Tag | Description | Trigger |
|-----|-------------|---------|
| `latest` | Latest stable version | Push to main |
| `v1.0.0` | Specific version | Git tag v1.0.0 |
| `main-abc123` | Branch-specific | Push to main |

## 🧪 Testing

### Local Testing
```bash
# Test the API locally
docker-compose up sentiment-api

# Test with curl
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

### Production Testing
```bash
# Test production image
make docker-hub-prod-test

# Run from Docker Hub
docker run -p 8000:8000 your-username/sentiment-analysis-api:latest
```

## 🔧 Environment Variables

Set these in your deployment environment:
```bash
export DOCKER_HUB_USERNAME="your-username"
export VERSION="v1.0.0"  # Optional
```

## 📊 Monitoring

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

### Docker Hub Metrics
- Pull count
- Star count
- Version tags
- Build status

## 🚨 Troubleshooting

### Common Issues

1. **Docker Hub login failed**
   ```bash
   docker login
   # Enter your Docker Hub credentials
   ```

2. **GitHub Actions failing**
   - Check secrets are set correctly
   - Verify Docker Hub token has write permissions
   - Check repository permissions

3. **Image not building**
   ```bash
   # Build locally to debug
   docker build -t test-image .
   docker run -p 8000:8000 test-image
   ```

4. **Tests failing**
   ```bash
   # Run tests locally
   python -m pytest tests/ -v
   ```

### Debug Commands
```bash
# Check Docker Hub login
docker info | grep Username

# List local images
docker images | grep sentiment-analysis-api

# Check container logs
docker logs <container-id>

# Test API endpoints
curl -v http://localhost:8000/health
curl -v -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'
```

## 📈 Next Steps

1. **Set up monitoring** (Prometheus, Grafana)
2. **Add rate limiting** to your API
3. **Set up alerts** for failed deployments
4. **Add security scanning** (Trivy, Snyk)
5. **Implement blue-green deployments**

## 🎉 Success!

Once set up, your workflow will be:
1. Push code to main branch
2. GitHub Actions automatically builds and tests
3. Image is pushed to Docker Hub
4. Production deployment is updated
5. Your API is live! 🚀

## 📞 Support

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/sentiment-analysis-api/issues)
- 📖 Docs: [API Documentation](http://localhost:8000/docs) 