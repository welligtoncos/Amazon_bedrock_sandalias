# Dockerfile

# Base image
FROM python:3.11-slim

# Metadata
LABEL maintainer="seu-email@example.com"
LABEL description="RAG Chatbot - Catálogo de Produtos"

# Argumentos de build
ARG AWS_REGION=us-east-1
ARG BEDROCK_MODEL=anthropic.claude-3-sonnet-20240229-v1:0

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    AWS_REGION=${AWS_REGION} \
    BEDROCK_MODEL_ID=${BEDROCK_MODEL}

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório de dados
RUN mkdir -p data

# Verificar se o banco existe, se não, criar
RUN python criar_catalogo.py || echo "Banco já existe"

# Expor porta (para versão web)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sqlite3; conn = sqlite3.connect('data/catalogo.db'); conn.close()" || exit 1

# Comando padrão
CMD ["python", "app.py"]