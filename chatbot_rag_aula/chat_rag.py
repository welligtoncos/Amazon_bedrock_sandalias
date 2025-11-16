import boto3
import sqlite3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import re
import unicodedata

# Caminho do banco
DB_PATH = r'C:\rsm_projects-inteligencia-artificial\Amazon_bedrock_sandalias\chatbot_rag_aula\produtos.db'

# Cliente Bedrock
bedrock_client = boto3.client(service_name='bedrock-runtime', region_name="us-east-1")

# Histórico
historico = []

def configurar_modelo(client, max_tokens=300, temperature=0.5, top_p=0.9):
    """Configura o modelo com parâmetros personalizados"""
    return ChatBedrock(
        model_id='anthropic.claude-3-sonnet-20240229-v1:0',
        client=client,
        model_kwargs={
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }
    )

# Configurar modelo
modelo = configurar_modelo(bedrock_client)

def get_hist():
    """Retorna histórico formatado"""
    return "\n".join(historico[-6:])

def remover_acentos(texto):
    """Remove acentos do texto"""
    nfkd = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def singular(palavra):
    """Converte palavra para singular"""
    if palavra.endswith('s') and len(palavra) > 3:
        return palavra[:-1]
    return palavra

def extrair_palavras_chave(texto):
    """Extrai palavras relevantes removendo stop words"""
    texto_limpo = remover_acentos(texto.lower())
    texto_limpo = re.sub(r'[^\w\s]', ' ', texto_limpo)
    
    stop_words = {
        'o', 'a', 'de', 'da', 'do', 'em', 'para', 'com', 'os', 'as', 
        'um', 'uma', 'e', 'eh', 'que', 'na', 'no', 'tem', 'tem', 'ter',
        'qual', 'quais', 'voce', 'voces', 'possui', 'ha', 'cor', 'cores',
        'quanto', 'custa', 'custam', 'preco', 'precos', 'valor', 'valores',
        'quero', 'comprar', 'procuro', 'busco'
    }
    
    palavras = texto_limpo.split()
    palavras_filtradas = []
    
    for p in palavras:
        if p not in stop_words and len(p) > 2:
            p_singular = singular(p)
            palavras_filtradas.append(p_singular)
    
    if not palavras_filtradas:
        palavras_filtradas = [p for p in palavras if len(p) > 3]
    
    return palavras_filtradas

def consulta_produto(texto_busca):
    """RETRIEVAL - Busca produtos relevantes no banco"""
    palavras_chave = extrair_palavras_chave(texto_busca)
    print(f"🔑 Palavras-chave: {palavras_chave}")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    resultados_ids = set()
    todos_resultados = []
    
    if not palavras_chave:
        cursor.execute("SELECT * FROM roupas LIMIT 10")
        todos_resultados = cursor.fetchall()
    else:
        for palavra in palavras_chave:
            cursor.execute("""
                SELECT * FROM roupas 
                WHERE LOWER(REPLACE(REPLACE(REPLACE(REPLACE(nome, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) LIKE LOWER(?)
                OR LOWER(REPLACE(REPLACE(REPLACE(REPLACE(descricao, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) LIKE LOWER(?)
            """, ('%' + palavra + '%', '%' + palavra + '%'))
            
            resultados = cursor.fetchall()
            print(f"   → '{palavra}': {len(resultados)} produto(s)")
            
            for r in resultados:
                if r[0] not in resultados_ids:
                    resultados_ids.add(r[0])
                    todos_resultados.append(r)
    
    print(f"✅ Total encontrado: {len(todos_resultados)}")
    
    conn.close()
    return todos_resultados

def inv_modelo(prompt_usuario):
    """Invoca modelo com contexto recuperado (RAG)"""
    
    print(f"\n🔍 Processando: '{prompt_usuario}'")
    
    # RETRIEVAL: Buscar produtos
    produtos_encontrados = consulta_produto(prompt_usuario)
    
    # AUGMENTED: Formatar contexto
    if produtos_encontrados:
        info_produtos = "Produtos disponíveis:\n\n"
        for produto in produtos_encontrados:
            info_produtos += f"""• {produto[1]} - R$ {produto[2]:.2f}
  Estoque: {produto[3]} unidades
  {produto[4]}

"""
    else:
        info_produtos = "Nenhum produto encontrado para essa busca."
    
    print(f"\n📦 Produtos para o modelo:\n{info_produtos[:200]}...")
    
    # Criar prompt SIMPLES (sem template complexo)
    system_message = f"""Você é um assistente virtual especializado em moda.
Responda APENAS perguntas sobre roupas e acessórios.
Use APENAS os produtos abaixo para responder.
Seja objetivo e amigável.

{info_produtos}

Histórico:
{get_hist()}"""
    
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt_usuario)
    ]
    
    print("\n🤖 Chamando modelo...")
    
    try:
        # GENERATION: Gerar resposta
        resposta = modelo.invoke(messages)
        
        print(f"✅ Resposta recebida: tipo={type(resposta)}")
        print(f"   Conteúdo: {resposta}")
        
        # Tentar diferentes formas de extrair o texto
        if hasattr(resposta, 'content'):
            resposta_texto = resposta.content
        elif isinstance(resposta, str):
            resposta_texto = resposta
        else:
            resposta_texto = str(resposta)
        
        print(f"📝 Texto extraído: '{resposta_texto[:100]}...'")
        
        # Salvar histórico
        historico.append(f"Usuário: {prompt_usuario}")
        historico.append(f"Assistente: {resposta_texto}")
        
        return resposta_texto
        
    except Exception as e:
        print(f"\n❌ ERRO ao chamar modelo: {e}")
        import traceback
        traceback.print_exc()
        return f"Desculpe, houve um erro: {e}"

# Loop principal
if __name__ == "__main__":
    print("=" * 60)
    print("🛍️  CHATBOT ZOOP - ASSISTENTE VIRTUAL DE MODA")
    print("=" * 60)
    print("\nOlá! Sou seu Assistente Virtual. :)")
    print("Em que posso ajudar hoje?\n")
    print("(Digite 'sair' para encerrar)")
    print("-" * 60)
    
    while True:
        pergunta = input("\nUser: ")
        
        if pergunta.lower() in ['sair', 'exit', 'quit']:
            print("\n👋 Obrigado por visitar a Zoop! Até logo!")
            break
        
        try:
            resposta = inv_modelo(pergunta)
            print(f"\nAssistente: {resposta}\n")
            print("-" * 60)
        except Exception as e:
            print(f"\n❌ Erro geral: {e}")
            import traceback
            traceback.print_exc()