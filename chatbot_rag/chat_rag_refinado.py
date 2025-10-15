import boto3
import json
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ============================================
# CONEXÃO COM BANCO DE DADOS
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
# FUNÇÃO PARA CONFIGURAR MODELO (refinamento de parâmetros)
# ============================================
def configurar_modelo(client, max_tokens=300, temperature=0.5, top_p=0.9):
    """
    Configura parâmetros do modelo para respostas mais precisas
    
    Parâmetros:
    - max_tokens: Limite de tokens na resposta (300 = ~225 palavras)
    - temperature: Criatividade (0.5 = balanceado)
    - top_p: Nucleus sampling (0.9 = diversidade controlada)
    """
    def _invocar_com_parametros(messages):
        """Invoca modelo com parâmetros personalizados"""
        if isinstance(messages, dict):
            entrada = messages.get('product_name', messages.get('input', ''))
        elif isinstance(messages, list):
            entrada = str(messages[-1].content if hasattr(messages[-1], 'content') else messages[-1])
        else:
            entrada = str(messages)
        
        config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "system": """Você é um assistente virtual especializado em moda para e-commerce.
            
SUAS RESPONSABILIDADES:
- Fornecer informações precisas sobre produtos de vestuário
- Responder apenas perguntas relacionadas a moda, roupas e acessórios
- Basear-se SEMPRE nos dados do banco de dados fornecidos
- Ser conciso e útil (máximo 300 caracteres)

REGRAS IMPORTANTES:
- Se a pergunta não for sobre moda: redirecione gentilmente
- Se não houver produtos no banco: sugira termos de busca alternativos
- Nunca invente informações sobre produtos
- Sempre mencione preço e quantidade quando disponíveis""",
            "messages": [{"role": "user", "content": entrada}]
        }
        
        response = client.invoke_model(
            body=json.dumps(config),
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )
        
        resposta = json.loads(response['body'].read().decode('utf-8'))
        return resposta.get('content', [{}])[0].get('text', 'Erro')
    
    return RunnableLambda(_invocar_com_parametros)

# ============================================
# CRIAR MODELO COM PARÂMETROS REFINADOS
# ============================================
modelo = configurar_modelo(
    bedrock_client,
    max_tokens=300,    # Respostas concisas
    temperature=0.5,   # Balanceado (nem muito criativo, nem muito rígido)
    top_p=0.9         # Diversidade controlada
)

# ============================================
# HISTÓRICO
# ============================================
historico = []

def get_hist():
    """Retorna histórico concatenado"""
    return "\n".join(historico)

# ============================================
# FUNÇÃO DE CONSULTA AO BANCO
# ============================================
def consulta_produto(nome_produto):
    """
    Consulta produtos no banco de dados usando busca LIKE
    Busca case-insensitive e parcial
    """
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    # Busca em nome E descrição para melhor cobertura
    cursor.execute("""
        SELECT * FROM roupas 
        WHERE nome LIKE ? OR descricao LIKE ?
    """, ('%' + nome_produto + '%', '%' + nome_produto + '%'))
    
    resultado = cursor.fetchall()
    conn.close()
    return resultado

# ============================================
# TEMPLATE DO PROMPT REFINADO
# ============================================
def get_chat_prompt(entrada):
    """
    Define o template de prompt refinado para o LangChain
    Com instruções detalhadas para melhor qualidade de resposta
    """
    template = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente virtual especializado em moda para e-commerce.

DIRETRIZES ESPECÍFICAS:
1. Responda APENAS perguntas sobre roupas, calçados e acessórios de moda
2. Se a pergunta não for sobre moda: redirecione educadamente para temas de moda
3. Base-se EXCLUSIVAMENTE nos dados fornecidos do banco de dados
4. Se não houver produtos: sugira termos alternativos ou peça mais detalhes
5. Sempre mencione preço e quantidade quando disponíveis no banco
6. Seja profissional, amigável e objetivo

FORMATO DE RESPOSTA:
- Máximo 300 caracteres
- Direta e útil
- Com informações concretas (preço, quantidade, características)
- Sem mencionar "banco de dados" ou "prompt" na resposta"""),
        
        ("human", entrada),
        
        ("assistant", """Forneça uma resposta concisa, direta e útil com no máximo 300 caracteres.

SE HOUVER PRODUTOS:
- Mencione nome, preço e quantidade
- Destaque características principais
- Seja entusiasmado mas profissional

SE NÃO HOUVER PRODUTOS:
- Sugira termos de busca alternativos
- Peça mais detalhes sobre o que procura
- Ofereça ajuda para refinar a busca

SE FOR PERGUNTA FORA DO ESCOPO:
- Redirecione educadamente para temas de moda
- Pergunte como pode ajudar com produtos de vestuário

NÃO MENCIONE:
- "Banco de dados"
- "Prompt"
- "Sistema"
- Limitações técnicas""")
    ])
    return template

# ============================================
# INVOCAR MODELO COM RAG REFINADO
# ============================================
def inv_modelo(prompt):
    """
    Invoca o modelo COM consulta refinada ao banco (RAG)
    Inclui melhor formatação e tratamento de casos
    """
    # Guardar prompt original para contexto
    prompt_original = prompt
    
    # Consultar produtos no banco (busca ampliada)
    produtos_encontrados = consulta_produto(prompt)
    
    # Verificar se encontrou produtos
    if produtos_encontrados:
        # Formatar informações dos produtos de forma detalhada
        produtos_info = []
        for p in produtos_encontrados:
            info = f"""
Produto ID {p[0]}:
- Nome: {p[1]}
- Preço: R$ {p[2]:.2f}
- Estoque: {p[3]} unidades
- Descrição: {p[4] if len(p) > 4 else 'N/A'}
"""
            produtos_info.append(info.strip())
        
        produtos_formatados = "\n\n".join(produtos_info)
        
        # Prompt aumentado com contexto rico
        prompt_augmented = f"""PRODUTOS DISPONÍVEIS NO ESTOQUE:
{produtos_formatados}

PERGUNTA DO CLIENTE:
{prompt_original}

INSTRUÇÕES:
Use as informações dos produtos acima para responder de forma precisa e útil.
Mencione preço e disponibilidade.
Seja entusiasmado mas profissional."""
        
    else:
        # Prompt para caso não encontre produtos
        prompt_augmented = f"""SITUAÇÃO: Nenhum produto encontrado no estoque.

BUSCA DO CLIENTE: "{prompt_original}"

INSTRUÇÕES:
1. Informe que não encontrou produtos com esses termos
2. Sugira termos de busca alternativos relacionados a moda
3. Peça mais detalhes sobre o que procura
4. Seja prestativo e ofereça ajuda para refinar a busca
5. NÃO invente produtos ou informações"""
    
    # Criar e executar chain
    chain = get_chat_prompt(prompt_augmented).pipe(modelo)
    response = chain.invoke({"product_name": prompt_augmented})
    return response

# ============================================
# MENSAGEM INICIAL
# ============================================
print("=" * 80)
print("🛍️  METEORA - ASSISTENTE VIRTUAL REFINADO")
print("=" * 80)
print("✨ Chatbot com RAG + Prompt Engineering + Parâmetros Otimizados")
print("=" * 80)
print("\nAssistente: Olá! Sou seu Assistente Virtual da Meteora. 😊")
print("Especializado em moda e vestuário.")
print("\nEm que posso ajudar hoje?")
print("\n💡 Dicas:")
print("   • Pergunte sobre roupas, calçados e acessórios")
print("   • Digite 'sair' para encerrar")
print("   • Digite 'produtos' para ver catálogo\n")
print("-" * 80 + "\n")

# ============================================
# COMANDOS ESPECIAIS
# ============================================
def listar_produtos():
    """Lista todos os produtos disponíveis"""
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco, quantidade FROM roupas ORDER BY nome")
    produtos = cursor.fetchall()
    conn.close()
    
    print("\n" + "=" * 80)
    print("📦 CATÁLOGO DE PRODUTOS")
    print("=" * 80)
    for p in produtos:
        print(f"• {p[0]:30} → R$ {p[1]:6.2f} | Estoque: {p[2]:3} un.")
    print("=" * 80 + "\n")

# ============================================
# LOOP PRINCIPAL
# ============================================
while True:
    try:
        entrada = input("User: ").strip()
        
        # Comandos especiais
        if entrada.lower() == "sair":
            print("\nAssistente: Foi um prazer ajudá-lo(a)!")
            print("Volte sempre à Meteora! 👋✨\n")
            break
        
        if entrada.lower() == "produtos":
            listar_produtos()
            continue
        
        if not entrada:
            continue
        
        # Adicionar ao histórico
        historico.append(f"Human: {entrada}")
        
        # Processar com RAG
        print("\n⏳ Consultando catálogo...", end="\r")
        response = inv_modelo(entrada)
        
        # Formatar e exibir resposta
        resposta_formatada = f"Assistente:\n{response}\n"
        historico.append(f"Assistant: {resposta_formatada}")
        
        print(" " * 50, end="\r")  # Limpar "Consultando..."
        print(resposta_formatada)
        print("-" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nAssistente: Até logo! 👋\n")
        break
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        # Remover última mensagem do histórico se falhou
        if historico and historico[-1].startswith("Human:"):
            historico.pop()