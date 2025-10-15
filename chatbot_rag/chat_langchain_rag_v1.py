import boto3
import json
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ============================================
# CONEXÃO COM BANCO DE DADOS (novo!)
# ============================================
conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

# ============================================
# CONFIGURAÇÃO BEDROCK
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
    if isinstance(messages, dict):
        entrada = messages.get('product_name', messages.get('input', ''))
    elif isinstance(messages, list):
        entrada = str(messages[-1].content if hasattr(messages[-1], 'content') else messages[-1])
    else:
        entrada = str(messages)
    
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
# CRIAR MODELO (igual à aula)
# ============================================
modelo = RunnableLambda(_invocar_bedrock)

# ============================================
# HISTÓRICO (igual à aula)
# ============================================
historico = []

def get_hist():
    return "\n".join(historico)

# ============================================
# FUNÇÃO DE CONSULTA AO BANCO (novo! igual à aula)
# ============================================
def consulta_produto(nome_produto):
    """
    Consulta produtos no banco de dados
    """
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM roupas WHERE nome LIKE ?", ('%' + nome_produto + '%',))
    resultado = cursor.fetchall()
    
    conn.close()
    return resultado

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
# INVOCAR MODELO COM RAG (modificado! igual à aula)
# ============================================
def inv_modelo(prompt):
    """
    Invoca o modelo COM consulta ao banco (RAG)
    """
    # Consultar produtos no banco
    produtos_encontrados = consulta_produto(prompt)
    
    # Verificar se encontrou produtos
    if produtos_encontrados:
        # Formatar informações dos produtos
        produtos_info = "\n".join([
            f"{p[0]}: {p[1]}, Preço: {p[2]}, Quantidade: {p[3]}" 
            for p in produtos_encontrados
        ])
        prompt = f"Produtos disponíveis:\n{produtos_info}\n\n{prompt}"
    else:
        prompt = f"Nenhum produto encontrado para '{prompt}'.\n{prompt}"
    
    # Criar e executar chain (igual à aula)
    chain = get_chat_prompt(prompt).pipe(modelo)
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
        print("\nAssistente: Até logo! 👋\n")
        break
    
    if not entrada:
        continue
    
    try:
        response = inv_modelo(entrada)
        resposta_formatada = f"Assistente:\n{response}\n"
        historico.append(f"Assistant: {resposta_formatada}")
        print(resposta_formatada)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")