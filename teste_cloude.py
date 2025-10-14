import boto3
import json

# Cliente Bedrock Runtime
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

# Claude Sonnet 4.5 (Inference Profile)
claude_model_id = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

# Configuração da requisição (Messages API)
claude_config = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 500,  # Aumentado para evitar resposta cortada
    "temperature": 0.5,
    "messages": [
        {
            "role": "user",
            "content": "Quais são as melhores opções de sandálias para uma caminhada na praia? Forneça uma resposta detalhada e bem formatada."
        }
    ]
})

# Invocação do modelo
response = client.invoke_model(
    body=claude_config,
    modelId=claude_model_id,
    accept="application/json",
    contentType="application/json"
)

# Tratamento da resposta usando dicionário Python
resposta = json.loads(response['body'].read().decode('utf-8'))

# Extração do texto da resposta (Claude 3+ usa 'content')
completion = resposta.get('content', [{}])[0].get('text', 'Resposta não encontrada')

# Formatação da resposta
resposta_formatada = f"Resposta:\n{completion}\n"

print(resposta_formatada)