# AWS Lambda Container Deployment Guide - Sentiment Analysis API

This guide explains how to deploy your FastAPI sentiment analysis application to AWS Lambda using Docker containers for MVP deployment.

## 🚀 Why Lambda Container for MVP?

**AWS Lambda Container is PERFECT for your MVP** because:

- ✅ **Your Docker setup**: Uses your existing Dockerfile
- ✅ **Pay-per-request**: Only pay when used (150 requests = ~$0.50/month)
- ✅ **Free tier**: 1M requests/month free
- ✅ **Zero idle costs**: No charges when not in use
- ✅ **Auto-scaling**: Handles traffic spikes automatically
- ✅ **Easy to unpublish**: Just delete the stack

## 📋 Prerequisites

### 1. AWS CLI Setup
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure AWS credentials
aws configure
```

### 2. Docker Setup
```bash
# Install Docker Desktop
# Download from https://www.docker.com/products/docker-desktop

# Verify Docker is running
docker --version
```

### 3. Required AWS Permissions
Your AWS user/role needs these permissions:
- `Lambda:*` (Lambda Functions)
- `ApiGateway:*` (API Gateway)
- `IAM:*` (Identity and Access Management)
- `CloudFormation:*` (Infrastructure as Code)
- `CloudWatch:*` (Logs and Metrics)
- `ECR:*` (Elastic Container Registry)

## 🚀 Quick Deployment

### Deploy to Lambda Container
```bash
# Deploy MVP
./aws/deploy-lambda-container.sh mvp eu-west-3

# Deploy staging
./aws/deploy-lambda-container.sh staging us-east-1
```

## 🔧 Infrastructure Components

### 1. **Lambda Function (Container)**
- Runs your Docker container
- Auto-scaling based on requests
- Pay-per-request pricing

### 2. **ECR Repository**
- Stores your Docker images
- Automatic image scanning
- Lifecycle policies

### 3. **API Gateway**
- HTTP endpoint for your API
- Built-in HTTPS
- Request routing

### 4. **CloudWatch**
- Logs and metrics
- Performance monitoring
- Error tracking

## 📊 Cost Analysis for MVP (150 requests)

### Monthly Cost Breakdown
- **Lambda**: $0.00 (Free tier: 1M requests/month)
- **API Gateway**: $0.00 (Free tier: 1M requests/month)
- **ECR**: ~$0.50 (storage)
- **Data Transfer**: ~$0.10
- **Total**: ~$0.60/month

### Cost Comparison
| Service | Monthly Cost | Best For |
|---------|-------------|----------|
| **Lambda Container** | **~$0.60** | ✅ **Your MVP** |
| AWS ECS | ~$75 | Production |
| AWS App Runner | ~$45 | Medium traffic |

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-api-gateway-url/health
```

### 2. API Documentation
```bash
# Open in browser
https://your-api-gateway-url/docs
```

### 3. Sentiment Analysis Test
```bash
curl -X POST "https://your-api-gateway-url/predict-sentiment/" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "I really enjoyed this movie! It was fantastic."
     }'
```

## 📈 Performance Characteristics

### Lambda Container Performance
- **Cold Start**: 3-5 seconds (first request, includes container startup)
- **Warm Start**: ~200ms (subsequent requests)
- **Concurrent**: Up to 1000 requests simultaneously
- **Timeout**: 30 seconds (configurable)

### Auto-Scaling
- **Automatic**: Scales from 0 to 1000+ requests
- **No Configuration**: Handles traffic spikes automatically
- **Cost Efficient**: Only pay for actual usage

## 🔄 CI/CD Pipeline

### GitHub Actions Setup
See `setup-github-secrets.md` for detailed instructions.

### Environment Strategy
- **`main` branch**: Deploy to production
- **`develop` branch**: Deploy to staging
- **Pull Requests**: Run tests only

## 🛠️ Files in This Directory

### Core Deployment Files
- **`lambda-container-deployment.yml`** - CloudFormation template for Lambda Container
- **`deploy-lambda-container.sh`** - Automated deployment script
- **`mvp-pricing-guide.md`** - Detailed cost analysis

### Documentation
- **`README.md`** - This deployment guide
- **`setup-github-secrets.md`** - GitHub Actions setup

## 🚀 Deployment Steps

### 1. Set up AWS credentials
```bash
aws configure
```

### 2. Deploy to Lambda Container
```bash
./aws/deploy-lambda-container.sh mvp eu-west-3
```

### 3. Get your API URL
```
Output: https://abc123.execute-api.eu-west-3.amazonaws.com/mvp
```

### 4. Test your API
```bash
curl -X POST "https://abc123.execute-api.eu-west-3.amazonaws.com/mvp/predict-sentiment/" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really enjoyed this movie!"}'
```

## 🔒 Security Features

### Built-in Security
- **HTTPS**: Automatic SSL/TLS encryption
- **IAM Integration**: Fine-grained access control
- **VPC Support**: Network isolation (if needed)
- **API Keys**: Request authentication (optional)
- **ECR Security**: Image scanning and lifecycle policies

## 🛠️ Troubleshooting

### Common Issues

#### 1. **Container Build Issues**
```bash
# Test Docker build locally
docker build -f Dockerfile.lambda -t test-lambda .

# Check container size
docker images test-lambda
```

#### 2. **Cold Start Too Slow**
```bash
# Consider Lambda provisioned concurrency
aws lambda put-provisioned-concurrency-config \
    --function-name mvp-sentiment-analysis-api \
    --qualifier $LATEST \
    --provisioned-concurrent-executions 1
```

#### 3. **Memory Issues**
```bash
# Increase Lambda memory (up to 10GB)
aws lambda update-function-configuration \
    --function-name mvp-sentiment-analysis-api \
    --memory-size 2048
```

#### 4. **Timeout Issues**
```bash
# Increase timeout (up to 15 minutes)
aws lambda update-function-configuration \
    --function-name mvp-sentiment-analysis-api \
    --timeout 60
```

## 🗑️ Cleanup

### Delete the entire stack
```bash
aws cloudformation delete-stack --stack-name sentiment-analysis-lambda-container-mvp
```

### Clean up ECR images
```bash
aws ecr batch-delete-image \
    --repository-name mvp-sentiment-analysis-api \
    --image-ids imageTag=latest
``` 