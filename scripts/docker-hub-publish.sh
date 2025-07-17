#!/bin/bash

# Docker Hub Publishing Script for Sentiment Analysis API
# This script builds and publishes your Docker image to Docker Hub

set -e

# Configuration
DOCKER_HUB_USERNAME=${DOCKER_HUB_USERNAME:-"your-username"}
IMAGE_NAME="sentiment-analysis-api"
VERSION=${VERSION:-"latest"}
FULL_IMAGE_NAME="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if user is logged in to Docker Hub
check_docker_login() {
    if ! docker info | grep -q "Username"; then
        print_warning "You are not logged in to Docker Hub"
        print_status "Please run: docker login"
        print_status "Or set DOCKER_HUB_USERNAME environment variable"
        read -p "Do you want to login now? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker login
        else
            print_error "Login required to publish to Docker Hub"
            exit 1
        fi
    fi
    print_success "Logged in to Docker Hub"
}

# Build the Docker image
build_image() {
    print_status "Building Docker image: ${FULL_IMAGE_NAME}"
    
    # Build with no cache to ensure fresh build
    docker build \
        --no-cache \
        --tag "${FULL_IMAGE_NAME}" \
        --file Dockerfile \
        .
    
    print_success "Image built successfully"
}

# Test the Docker image
test_image() {
    print_status "Testing Docker image..."
    
    # Run the container in background
    CONTAINER_ID=$(docker run -d -p 8000:8000 "${FULL_IMAGE_NAME}")
    
    # Wait for container to start
    sleep 10
    
    # Test health endpoint
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Health check passed"
    else
        print_error "Health check failed"
        docker logs "${CONTAINER_ID}"
        docker stop "${CONTAINER_ID}" > /dev/null 2>&1
        exit 1
    fi
    
    # Test sentiment endpoint
    if curl -f -X POST http://localhost:8000/predict \
        -H "Content-Type: application/json" \
        -d '{"text": "I love this product!"}' > /dev/null 2>&1; then
        print_success "API endpoint test passed"
    else
        print_error "API endpoint test failed"
        docker logs "${CONTAINER_ID}"
        docker stop "${CONTAINER_ID}" > /dev/null 2>&1
        exit 1
    fi
    
    # Stop the test container
    docker stop "${CONTAINER_ID}" > /dev/null 2>&1
    docker rm "${CONTAINER_ID}" > /dev/null 2>&1
    
    print_success "All tests passed"
}

# Push the image to Docker Hub
push_image() {
    print_status "Pushing image to Docker Hub: ${FULL_IMAGE_NAME}"
    
    docker push "${FULL_IMAGE_NAME}"
    
    print_success "Image pushed successfully to Docker Hub"
}

# Create Docker Hub README
create_dockerhub_readme() {
    print_status "Creating Docker Hub README..."
    
    cat > dockerhub-readme.md << 'EOF'
# Sentiment Analysis API

A production-ready sentiment analysis API built with FastAPI and BERT models.

## Quick Start

```bash
# Pull the image
docker pull your-username/sentiment-analysis-api:latest

# Run the API
docker run -p 8000:8000 your-username/sentiment-analysis-api:latest

# Test the API
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Predict sentiment
- `GET /docs` - Interactive API documentation

## Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `WORKERS` - Number of workers (default: 4)
- `LOG_LEVEL` - Logging level (default: info)

## Example Usage

```python
import requests

# Predict sentiment
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "This is amazing!"}
)
result = response.json()
print(result["sentiment"])  # "positive"
```

## Docker Compose

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
```

## Features

- ✅ FastAPI with automatic documentation
- ✅ BERT-based sentiment analysis
- ✅ Production-ready with health checks
- ✅ Docker optimized
- ✅ AWS Lambda compatible
- ✅ Comprehensive testing

## License

MIT License
EOF

    print_success "Docker Hub README created"
}

# Main execution
main() {
    echo "🐳 Docker Hub Publishing Script"
    echo "================================"
    echo ""
    
    # Check prerequisites
    check_docker
    check_docker_login
    
    # Build and test
    build_image
    test_image
    
    # Ask for confirmation before pushing
    echo ""
    print_warning "About to push image to Docker Hub: ${FULL_IMAGE_NAME}"
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        push_image
        create_dockerhub_readme
        echo ""
        print_success "🎉 Image successfully published to Docker Hub!"
        echo ""
        echo "Next steps:"
        echo "1. Update your Docker Hub repository description"
        echo "2. Add the README content to your repository"
        echo "3. Share your image: docker pull ${FULL_IMAGE_NAME}"
        echo ""
        echo "Your API is now available at: https://hub.docker.com/r/${DOCKER_HUB_USERNAME}/${IMAGE_NAME}"
    else
        print_status "Publishing cancelled"
    fi
}

# Handle command line arguments
case "${1:-}" in
    --help|-h)
        echo "Usage: $0 [VERSION]"
        echo ""
        echo "Environment variables:"
        echo "  DOCKER_HUB_USERNAME - Your Docker Hub username"
        echo "  VERSION             - Image version (default: latest)"
        echo ""
        echo "Examples:"
        echo "  $0                    # Build and publish latest"
        echo "  $0 v1.0.0            # Build and publish v1.0.0"
        echo "  VERSION=v1.0.0 $0    # Same as above"
        exit 0
        ;;
    *)
        if [ -n "$1" ]; then
            VERSION="$1"
            FULL_IMAGE_NAME="${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:${VERSION}"
        fi
        main
        ;;
esac 