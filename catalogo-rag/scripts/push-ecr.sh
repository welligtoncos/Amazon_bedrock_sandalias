#!/bin/bash
# scripts/push-ecr.sh

echo "📤 Pushing to AWS ECR..."
echo "========================="

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPOSITORY="catalogo-rag"
IMAGE_TAG="latest"

# Criar repositório ECR se não existir
aws ecr describe-repositories --repository-names $ECR_REPOSITORY --region $AWS_REGION || \
  aws ecr create-repository --repository-name $ECR_REPOSITORY --region $AWS_REGION

# Login no ECR
aws ecr get-login-password --region $AWS_REGION | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag image
docker tag catalogo-rag:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

# Push
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG

echo ""
echo "✅ Push concluído!"
echo "📦 Image: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPOSITORY:$IMAGE_TAG"