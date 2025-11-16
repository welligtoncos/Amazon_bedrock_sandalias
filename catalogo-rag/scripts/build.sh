#!/bin/bash
# scripts/build.sh

echo "🐳 Building Docker Image..."
echo "=============================="

# Build image
docker build \
  --build-arg AWS_REGION=us-east-1 \
  -t catalogo-rag:latest \
  -t catalogo-rag:$(git rev-parse --short HEAD) \
  .

echo ""
echo "✅ Build concluído!"
echo ""
echo "🚀 Para executar:"
echo "   docker run -it --rm catalogo-rag:latest"