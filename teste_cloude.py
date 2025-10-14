import boto3
import json

client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

# Claude Sonnet 4.5 (MAIS RECENTE) ⭐
claude_model_id = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'

# Configuração corrigida - apenas temperature (SEM top_p e top_k)
claude_config = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 300,
    "temperature": 0.5,  # Use APENAS temperature OU top_p, nunca os dois
    "messages": [
        {
            "role": "user",
            "content": "Quais são as melhores opções de sandálias para uma caminhada na praia? Forneça uma resposta concisa com no máximo 300 caracteres, ideal para um e-commerce de roupas e itens de vestuário."
        }
    ]
})

response = client.invoke_model(
    body=claude_config,
    modelId=claude_model_id,
    accept="application/json",
    contentType="application/json"
)

resposta_json = json.loads(response['body'].read().decode('utf-8'))
texto_resposta = resposta_json['content'][0]['text']

print("Resposta:")
print(texto_resposta)
print(f"\n✅ Modelo usado: {claude_model_id}")