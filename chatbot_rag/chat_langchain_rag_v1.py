import boto3
import json
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

# ============================================
# CONFIGURAÇÃO BEDROCK
# ============================================
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-2"
)

MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

# ============================================
# FUNÇÃO PARA CONFIGURAR MODELO
# ============================================
def configurar_modelo(client, max_tokens=300, temperature=0.5, top_p=0.9):
    """Configura parâmetros do modelo"""
    def _invocar_com_parametros(messages):
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
            "system": """Você é um assistente virtual especializado em moda para e-commerce da Meteora.

SUAS RESPONSABILIDADES:
- Fornecer informações precisas sobre produtos de vestuário
- Responder apenas perguntas relacionadas a moda, roupas e acessórios
- Basear-se SEMPRE nos dados do banco de dados fornecidos
- Ser conciso e útil (máximo 300 caracteres)

REGRAS:
- Se a pergunta não for sobre moda: redirecione gentilmente
- Se não houver produtos: sugira termos de busca alternativos
- Sempre mencione preço e quantidade quando disponíveis
- Nunca invente informações""",
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

modelo = configurar_modelo(bedrock_client)

# ============================================
# HISTÓRICO
# ============================================
historico = []

def get_hist():
    return "\n".join(historico)

# ============================================
# FUNÇÃO DE CONSULTA CORRIGIDA
# ============================================
def consulta_produto(nome_produto):
    """
    Consulta produtos no banco - VERSÃO CORRIGIDA
    """
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    # 🔧 CORREÇÃO: Busca apenas em NOME (mais confiável)
    # Remove acentos e converte para minúsculas para melhor match
    termos_busca = nome_produto.lower().split()
    
    # Lista para armazenar todos os produtos encontrados
    produtos_encontrados = []
    
    # Buscar por cada termo
    for termo in termos_busca:
        cursor.execute("""
            SELECT * FROM roupas 
            WHERE LOWER(nome) LIKE ?
        """, ('%' + termo + '%',))
        
        resultados = cursor.fetchall()
        produtos_encontrados.extend(resultados)
    
    conn.close()
    
    # Remover duplicatas mantendo ordem
    produtos_unicos = []
    ids_vistos = set()
    for p in produtos_encontrados:
        if p[0] not in ids_vistos:
            produtos_unicos.append(p)
            ids_vistos.add(p[0])
    
    return produtos_unicos

# ============================================
# TEMPLATE DO PROMPT
# ============================================
def get_chat_prompt(entrada):
    template = ChatPromptTemplate.from_messages([
        ("system", """Você é assistente virtual da Meteora especializado em moda.

DIRETRIZES:
1. Responda APENAS sobre moda, roupas, calçados e acessórios
2. Use EXCLUSIVAMENTE dados fornecidos do banco
3. Se não houver produtos: sugira termos alternativos
4. Sempre mencione preço e quantidade quando disponível
5. Seja profissional, amigável e conciso (máximo 300 caracteres)

FORMATO:
- Direto e útil
- Com informações concretas (preço, quantidade)
- Sem mencionar "banco de dados" ou limitações técnicas"""),
        
        ("human", entrada),
        
        ("assistant", """Forneça resposta concisa (máximo 300 caracteres).

SE HOUVER PRODUTOS:
- Mencione nome, preço e quantidade
- Destaque características principais

SE NÃO HOUVER PRODUTOS:
- Sugira termos de busca alternativos
- Peça mais detalhes

SE PERGUNTA FORA DO ESCOPO:
- Redirecione educadamente para moda
- Pergunte como pode ajudar com vestuário""")
    ])
    return template

# ============================================
# INVOCAR MODELO COM RAG
# ============================================
def inv_modelo(prompt):
    """Invoca modelo COM RAG"""
    prompt_original = prompt
    
    # 🔍 DEBUG: Mostrar o que está buscando
    print(f"  🔍 Buscando: '{prompt}'", end="\r")
    
    # Consultar produtos
    produtos_encontrados = consulta_produto(prompt)
    
    # 🔍 DEBUG: Mostrar quantos encontrou
    print(f"  📦 Encontrados: {len(produtos_encontrados)} produto(s)    ", end="\r")
    
    if produtos_encontrados:
        produtos_info = []
        for p in produtos_encontrados:
            # Estrutura: ID, Nome, Preço, Quantidade, (Descrição se existir)
            info = f"""Produto ID {p[0]}:
- Nome: {p[1]}
- Preço: R$ {p[2]:.2f}
- Estoque: {p[3]} unidades"""
            
            # Adicionar descrição se existir (índice 4)
            if len(p) > 4 and p[4]:
                info += f"\n- Descrição: {p[4]}"
            
            produtos_info.append(info.strip())
        
        produtos_formatados = "\n\n".join(produtos_info)
        
        prompt_augmented = f"""PRODUTOS DISPONÍVEIS:
{produtos_formatados}

PERGUNTA: {prompt_original}

INSTRUÇÕES: Use as informações acima para responder com preço e disponibilidade."""
        
    else:
        prompt_augmented = f"""SITUAÇÃO: Nenhum produto encontrado.

BUSCA: "{prompt_original}"

INSTRUÇÕES:
1. Informe que não encontrou com esses termos
2. Sugira termos alternativos de moda
3. Peça mais detalhes
4. NÃO invente informações"""
    
    chain = get_chat_prompt(prompt_augmented).pipe(modelo)
    response = chain.invoke({"product_name": prompt_augmented})
    return response

# ============================================
# COMANDOS ESPECIAIS
# ============================================
def listar_produtos():
    """Lista catálogo completo"""
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, preco, quantidade FROM roupas ORDER BY nome")
    produtos = cursor.fetchall()
    conn.close()
    
    print("\n" + "=" * 80)
    print("📦 CATÁLOGO METEORA")
    print("=" * 80)
    for i, p in enumerate(produtos, 1):
        print(f"{i}. {p[0]:30} → R$ {p[1]:6.2f} | {p[2]:3} un.")
    print("=" * 80 + "\n")

# ============================================
# MENSAGEM INICIAL
# ============================================
print("=" * 80)
print("🛍️  METEORA - ASSISTENTE VIRTUAL")
print("=" * 80)
print("\nAssistente: Olá! Sou seu Assistente Virtual da Meteora. 😊")
print("Especializado em moda e vestuário.\n")
print("💡 Comandos:")
print("   • 'produtos' = ver catálogo completo")
print("   • 'sair' = encerrar\n")
print("-" * 80 + "\n")

# ============================================
# LOOP PRINCIPAL
# ============================================
while True:
    try:
        entrada = input("User: ").strip()
        
        if entrada.lower() == "sair":
            print("\nAssistente: Até logo! Volte sempre! 👋✨\n")
            break
        
        if entrada.lower() == "produtos":
            listar_produtos()
            continue
        
        if not entrada:
            continue
        
        historico.append(f"Human: {entrada}")
        
        # Processar com RAG
        response = inv_modelo(entrada)
        
        resposta_formatada = f"\nAssistente:\n{response}\n"
        historico.append(f"Assistant: {resposta_formatada}")
        
        print(resposta_formatada)
        print("-" * 80 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nAssistente: Até logo! 👋\n")
        break
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")
        if historico and historico[-1].startswith("Human:"):
            historico.pop()