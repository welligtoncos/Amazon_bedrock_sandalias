import boto3
import sqlite3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
import re
import unicodedata

# ==================== CONFIGURAÇÕES ====================

# Caminho do banco de dados
DB_PATH = r'C:\rsm_projects-inteligencia-artificial\Amazon_bedrock_sandalias\chatbot_rag_aula\produtos.db'

# Cliente Bedrock AWS
bedrock_client = boto3.client(
    service_name='bedrock-runtime', 
    region_name="us-east-1"
)

# Histórico da conversa
historico = []

# ==================== CONFIGURAÇÃO DO MODELO ====================

def configurar_modelo(client, max_tokens=300, temperature=0.5, top_p=0.9):
    """
    Configura o modelo Claude com parâmetros otimizados
    
    Args:
        client: Cliente Bedrock
        max_tokens: Número máximo de tokens na resposta
        temperature: Controla criatividade (0.0 a 1.0)
        top_p: Controla diversidade da resposta
    
    Returns:
        Modelo configurado
    """
    return ChatBedrock(
        model_id='anthropic.claude-3-sonnet-20240229-v1:0',
        client=client,
        model_kwargs={
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    )

# Inicializar modelo
modelo = configurar_modelo(bedrock_client)

# ==================== FUNÇÕES AUXILIARES ====================

def get_hist():
    """Retorna as últimas 6 mensagens do histórico (3 interações)"""
    return "\n".join(historico[-6:]) if historico else "Nenhuma conversa anterior."

def remover_acentos(texto):
    """Remove acentos de um texto"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def singular(palavra):
    """Converte palavra para singular (simplificado)"""
    if palavra.endswith('s') and len(palavra) > 3:
        return palavra[:-1]
    return palavra

def extrair_palavras_chave(texto):
    """
    Extrai palavras-chave relevantes do texto removendo stop words
    
    Args:
        texto: Texto de entrada do usuário
    
    Returns:
        Lista de palavras-chave relevantes
    """
    # Normalizar texto
    texto_limpo = remover_acentos(texto.lower())
    texto_limpo = re.sub(r'[^\w\s]', ' ', texto_limpo)
    
    # Stop words em português
    stop_words = {
        'o', 'a', 'de', 'da', 'do', 'em', 'para', 'com', 'os', 'as', 
        'um', 'uma', 'e', 'eh', 'que', 'na', 'no', 'tem', 'tem', 'ter',
        'qual', 'quais', 'voce', 'voces', 'possui', 'ha', 'cor', 'cores',
        'quanto', 'custa', 'custam', 'preco', 'precos', 'valor', 'valores',
        'quero', 'comprar', 'procuro', 'busco', 'gostaria', 'preciso'
    }
    
    # Extrair e filtrar palavras
    palavras = texto_limpo.split()
    palavras_filtradas = []
    
    for palavra in palavras:
        if palavra not in stop_words and len(palavra) > 2:
            palavra_singular = singular(palavra)
            palavras_filtradas.append(palavra_singular)
    
    # Fallback: se não encontrou palavras relevantes
    if not palavras_filtradas:
        palavras_filtradas = [p for p in palavras if len(p) > 3]
    
    return palavras_filtradas

# ==================== RETRIEVAL (RAG) ====================

def consulta_produto(texto_busca):
    """
    Busca produtos no banco de dados (RETRIEVAL)
    
    Args:
        texto_busca: Texto da consulta do usuário
    
    Returns:
        Lista de produtos encontrados
    """
    # Extrair palavras-chave
    palavras_chave = extrair_palavras_chave(texto_busca)
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    resultados_ids = set()
    todos_resultados = []
    
    # Se não há palavras-chave, retornar alguns produtos
    if not palavras_chave:
        cursor.execute("SELECT * FROM roupas LIMIT 10")
        todos_resultados = cursor.fetchall()
    else:
        # Buscar produtos para cada palavra-chave
        for palavra in palavras_chave:
            cursor.execute("""
                SELECT * FROM roupas 
                WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(nome, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) 
                      LIKE LOWER(?)
                OR LOWER(REPLACE(REPLACE(REPLACE(REPLACE(descricao, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) 
                   LIKE LOWER(?)
            """, ('%' + palavra + '%', '%' + palavra + '%'))
            
            resultados = cursor.fetchall()
            
            # Adicionar resultados únicos
            for resultado in resultados:
                if resultado[0] not in resultados_ids:
                    resultados_ids.add(resultado[0])
                    todos_resultados.append(resultado)
    
    conn.close()
    return todos_resultados

# ==================== GERAÇÃO DE RESPOSTA (RAG) ====================

def inv_modelo(prompt_usuario):
    """
    Invoca o modelo Claude com contexto recuperado (AUGMENTED GENERATION)
    
    Args:
        prompt_usuario: Pergunta/mensagem do usuário
    
    Returns:
        Resposta do assistente
    """
    # PASSO 1: RETRIEVAL - Buscar produtos relevantes
    produtos_encontrados = consulta_produto(prompt_usuario)
    
    # PASSO 2: AUGMENTED - Formatar contexto com produtos
    if produtos_encontrados:
        info_produtos = "Produtos disponíveis:\n\n"
        for produto in produtos_encontrados:
            info_produtos += f"""• {produto[1]} - R$ {produto[2]:.2f}
  Estoque: {produto[3]} unidades
  {produto[4]}

"""
    else:
        info_produtos = "Nenhum produto encontrado para essa busca."
    
    # PASSO 3: Criar prompt do sistema
    system_message = f"""Você é um assistente virtual especializado em moda para e-commerce.

REGRAS:
- Responda APENAS perguntas sobre roupas, calçados e acessórios de moda
- Se a pergunta não for sobre moda, redirecione educadamente
- Use APENAS os produtos listados abaixo
- Seja objetivo, amigável e prestativo
- Não mencione que usa banco de dados ou prompts

{info_produtos}

Histórico da conversa:
{get_hist()}"""
    
    # Criar mensagens
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt_usuario)
    ]
    
    # PASSO 4: GENERATION - Gerar resposta com o modelo
    resposta = modelo.invoke(messages)
    resposta_texto = resposta.content
    
    # Salvar no histórico
    historico.append(f"Usuário: {prompt_usuario}")
    historico.append(f"Assistente: {resposta_texto}")
    
    return resposta_texto

# ==================== INTERFACE DO CHATBOT ====================

def main():
    """Função principal do chatbot"""
    print("=" * 60)
    print("🛍️  CHATBOT ZOOP - ASSISTENTE VIRTUAL DE MODA")
    print("=" * 60)
    print("\nOlá! Sou seu Assistente Virtual. 😊")
    print("Posso ajudá-lo a encontrar roupas e acessórios!\n")
    print("Digite 'sair' para encerrar a conversa.")
    print("-" * 60)
    
    while True:
        # Receber entrada do usuário
        pergunta = input("\n👤 Você: ").strip()
        
        # Verificar se quer sair
        if pergunta.lower() in ['sair', 'exit', 'quit', 'tchau']:
            print("\n👋 Obrigado por visitar a Zoop! Até logo!")
            break
        
        # Ignorar entradas vazias
        if not pergunta:
            continue
        
        try:
            # Processar pergunta e obter resposta
            resposta = inv_modelo(pergunta)
            print(f"\n🤖 Assistente: {resposta}")
            
        except Exception as e:
            print(f"\n❌ Desculpe, ocorreu um erro. Tente novamente.")
            print(f"Detalhes: {e}")

if __name__ == "__main__":
    main()