import boto3
import json

# Cliente Bedrock Runtime
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

# Modelo: Claude 3.5 Haiku (custo baixo)
MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

def get_config(prompt: str):
    """
    Configuração da requisição para o modelo Claude 3.5 Haiku
    Usando Messages API (formato moderno)
    """
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.5,
        "system": """Você é um assistente virtual da Meteora, um e-commerce de moda e vestuário.
        Suas respostas devem ser:
        - Concisas (máximo 300 caracteres)
        - Focadas em produtos de moda e vestuário
        - Profissionais e amigáveis
        - Orientadas para ajudar o cliente a encontrar produtos
        - Sem mencionar limitações técnicas""",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

def processar_resposta(response):
    """
    Processa a resposta do modelo e extrai o texto
    """
    try:
        resposta = json.loads(response['body'].read().decode('utf-8'))
        texto = resposta.get('content', [{}])[0].get('text', 'Resposta não encontrada')
        return texto
    except Exception as e:
        return f"Erro ao processar resposta: {e}"

def iniciar_chat():
    """
    Função principal do chatbot
    """
    print("=" * 80)
    print("🛍️  METEORA - ASSISTENTE VIRTUAL")
    print("=" * 80)
    print("\nAssistente: Olá! Sou seu Assistente Virtual da Meteora. 😊")
    print("Em que posso ajudar hoje?")
    print("\n💡 Dica: Digite 'sair' para encerrar\n")
    
    while True:
        # Capturar entrada do usuário
        entrada = input("Você: ").strip()
        
        # Verificar se quer sair
        if entrada.lower() in ['sair', 'exit', 'quit', 'tchau']:
            print("\nAssistente: Foi um prazer ajudá-lo(a)! Até logo! 👋\n")
            break
        
        # Ignorar entradas vazias
        if not entrada:
            continue
        
        try:
            # Enviar requisição ao modelo
            response = client.invoke_model(
                body=get_config(entrada),
                modelId=MODEL_ID,
                accept="application/json",
                contentType="application/json"
            )
            
            # Processar e exibir resposta
            resposta_texto = processar_resposta(response)
            print(f"\nAssistente: {resposta_texto}\n")
            
        except client.exceptions.ThrottlingException:
            print("\n⚠️ Muitas requisições. Aguarde um momento...\n")
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")

# Executar chatbot
if __name__ == "__main__":
    iniciar_chat()