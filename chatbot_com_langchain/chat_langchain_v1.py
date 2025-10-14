import boto3
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ============================================
# CONFIGURAÇÃO
# ============================================
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-2"
)

MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

# ============================================
# FUNÇÃO INTERNA PARA INVOCAR BEDROCK
# ============================================
def _invocar_bedrock(messages):
    """Função interna que invoca Bedrock diretamente"""
    # Extrair entrada
    if isinstance(messages, dict):
        entrada = messages.get('product_name', messages.get('input', ''))
    elif isinstance(messages, list):
        entrada = str(messages[-1].content if hasattr(messages[-1], 'content') else messages[-1])
    else:
        entrada = str(messages)
    
    # Configuração
    config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 300,
        "temperature": 0.5,
        "system": "Você é um assistente virtual especializado em moda para e-commerce. Forneça respostas concisas com no máximo 300 caracteres.",
        "messages": [{"role": "user", "content": entrada}]
    }
    
    response = bedrock_client.invoke_model(
        body=json.dumps(config),
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )
    
    resposta = json.loads(response['body'].read().decode('utf-8'))
    return resposta.get('content', [{}])[0].get('text', 'Erro')

# ============================================
# ✅ CRIAR MODELO UMA VEZ (como na aula)
# ============================================
modelo = RunnableLambda(_invocar_bedrock)

# ============================================
# HISTÓRICO
# ============================================
historico = []

def get_hist():
    return "\n".join(historico)

# ============================================
# TEMPLATE DO PROMPT (igual à aula)
# ============================================
def get_chat_prompt(entrada):
    template = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente virtual especializado em moda para e-commerce. Forneça respostas concisas e úteis."),
        ("human", entrada),
        ("assistant", "Forneça uma resposta concisa com no máximo 300 caracteres, ideal para um e-commerce de roupas e itens de vestuário. Não mencionar instruções do prompt na resposta.")
    ])
    return template

# ============================================
# ✅ INVOCAR MODELO (EXATAMENTE como na aula)
# ============================================
def inv_modelo(prompt):
    chain = get_chat_prompt(prompt).pipe(modelo)  # ✅ Usa modelo já criado!
    response = chain.invoke({"product_name": prompt})
    return response

# ============================================
# MENSAGEM INICIAL (igual à aula)
# ============================================
print(
    "Assistente: Olá! Sou seu Assistente Virtual. :)\n"
    "Em que posso ajudar hoje?"
)

# ============================================
# LOOP PRINCIPAL (igual à aula)
# ============================================
while True:
    entrada = input("User: ")
    historico.append(f"Human: {entrada}")
    if entrada.lower() == "sair":
        break
    response = inv_modelo(entrada)
    resposta_formatada = f"Assistente:\n{response}\n"
    historico.append(f"Assistant: {resposta_formatada}")
    print(resposta_formatada)