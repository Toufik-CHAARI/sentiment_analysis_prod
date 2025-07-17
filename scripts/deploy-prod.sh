#!/bin/bash

# Production Deployment Script for Sentiment Analysis API
# This script builds and pushes the latest production image to Docker Hub

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

# Check if we're on main/master branch
check_branch() {
    CURRENT_BRANCH=$(git branch --show-current)
    if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
        print_warning "You're not on main/master branch (current: $CURRENT_BRANCH)"
        read -p "Do you want to continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Check if working directory is clean
check_git_status() {
    if [[ -n $(git status --porcelain) ]]; then
        print_warning "Working directory is not clean. You have uncommitted changes."
        git status --short
        read -p "Do you want to continue anyway? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
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

# Run tests before deployment
run_tests() {
    print_status "Running tests before deployment..."
    
    # Run unit tests
    if ! python -m pytest tests/unit/ -v --tb=short; then
        print_error "Unit tests failed"
        exit 1
    fi
    
    # Run integration tests
    if ! python -m pytest tests/integration/ -v --tb=short; then
        print_error "Integration tests failed"
        exit 1
    fi
    
    print_success "All tests passed"
}

# Build the production Docker image
build_production_image() {
    print_status "Building production Docker image: ${FULL_IMAGE_NAME}"
    
    # Build with no cache to ensure fresh build
    docker build \
        --no-cache \
        --tag "${FULL_IMAGE_NAME}" \
        --file Dockerfile \
        .
    
    # Also tag as latest
    docker tag "${FULL_IMAGE_NAME}" "${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
    
    print_success "Production image built successfully"
}

# Test the production image
test_production_image() {
    print_status "Testing production image..."
    
    # Run the container in background
    CONTAINER_ID=$(docker run -d -p 8000:8000 "${FULL_IMAGE_NAME}")
    
    # Wait for container to start
    sleep 15
    
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
    
    print_success "Production image test passed"
}

# Push the image to Docker Hub
push_to_docker_hub() {
    print_status "Pushing production image to Docker Hub: ${FULL_IMAGE_NAME}"
    
    # Push the versioned tag
    docker push "${FULL_IMAGE_NAME}"
    
    # Push the latest tag
    docker push "${DOCKER_HUB_USERNAME}/${IMAGE_NAME}:latest"
    
    print_success "Production image pushed successfully to Docker Hub"
}

# Create deployment summary
create_deployment_summary() {
    print_status "Creating deployment summary..."
    
    cat > deployment-summary.md << EOF
# Production Deployment Summary

## Deployment Details
- **Image**: ${FULL_IMAGE_NAME}
- **Version**: ${VERSION}
- **Timestamp**: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Git Commit**: $(git rev-parse HEAD)
- **Branch**: $(git branch --show-current)

## Quick Start
\`\`\`bash
# Pull the latest production image
docker pull ${FULL_IMAGE_NAME}

# Run the API
docker run -p 8000:8000 ${FULL_IMAGE_NAME}

# Test the API
curl -X POST http://localhost:8000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"text": "I love this product!"}'
\`\`\`

## Docker Hub URL
https://hub.docker.com/r/${DOCKER_HUB_USERNAME}/${IMAGE_NAME}

## Health Check
\`\`\`bash
curl http://localhost:8000/health
\`\`\`

## API Documentation
http://localhost:8000/docs
EOF

    print_success "Deployment summary created: deployment-summary.md"
}

# Main deployment function
main() {
    echo "🚀 Production Deployment Script"
    echo "================================"
    echo ""
    
    # Pre-deployment checks
    check_branch
    check_git_status
    check_docker
    check_docker_login
    
    # Run tests
    run_tests
    
    # Build and test production image
    build_production_image
    test_production_image
    
    # Ask for confirmation before pushing
    echo ""
    print_warning "About to push production image to Docker Hub: ${FULL_IMAGE_NAME}"
    print_warning "This will update the production environment!"
    read -p "Do you want to continue? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        push_to_docker_hub
        create_deployment_summary
        echo ""
        print_success "🎉 Production deployment successful!"
        echo ""
        echo "📋 Summary:"
        echo "  - Image: ${FULL_IMAGE_NAME}"
        echo "  - Docker Hub: https://hub.docker.com/r/${DOCKER_HUB_USERNAME}/${IMAGE_NAME}"
        echo "  - Health Check: curl http://localhost:8000/health"
        echo "  - API Docs: http://localhost:8000/docs"
        echo ""
        echo "📄 Deployment summary saved to: deployment-summary.md"
        echo ""
        echo "🚀 Your sentiment analysis API is now live in production!"
    else
        print_status "Production deployment cancelled"
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
        echo "  $0                    # Deploy latest"
        echo "  $0 v1.0.0            # Deploy v1.0.0"
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