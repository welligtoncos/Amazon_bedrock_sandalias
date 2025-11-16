#!/bin/bash
# scripts/run.sh

echo "🚀 Running Catalogo RAG Chatbot..."
echo "===================================="

# Verificar variáveis de ambiente AWS
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "❌ Erro: Credenciais AWS não configuradas!"
  echo ""
  echo "Configure com:"
  echo "  export AWS_ACCESS_KEY_ID=seu-access-key"
  echo "  export AWS_SECRET_ACCESS_KEY=seu-secret-key"
  exit 1
fi

# Executar container
docker run -it --rm \
  --name catalogo-rag \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_REGION=us-east-1 \
  -v $(pwd)/data:/app/data \
  catalogo-rag:latest