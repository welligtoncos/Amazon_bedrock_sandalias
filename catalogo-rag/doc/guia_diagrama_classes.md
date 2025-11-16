# 📘 GUIA DE ENTENDIMENTO - DIAGRAMA DE CLASSES

## 🎯 Visão Geral do Sistema

O sistema implementa um **assistente virtual de produtos** usando a arquitetura **RAG (Retrieval-Augmented Generation)** com Claude da Anthropic via AWS Bedrock.

---

## 🏗️ ARQUITETURA DO DIAGRAMA DE CLASSES

### 1. CLASSE PRINCIPAL: CatalogoRAG

```
┌─────────────────────────────┐
│      CatalogoRAG            │
├─────────────────────────────┤
│ - retriever                 │  → ProductRetriever
│ - augmenter                 │  → ContextAugmenter
│ - generator                 │  → ResponseGenerator
│ - db                        │  → DatabaseManager
├─────────────────────────────┤
│ + processar_consulta()      │
│ + mostrar_estatisticas()    │
└─────────────────────────────┘
```

**O QUE FAZ:**
- É a **classe orquestradora** do sistema
- Gerencia o pipeline RAG completo
- Coordena todas as outras classes

**RESPONSABILIDADES:**
1. Receber consultas do usuário
2. Executar o pipeline RAG (Retrieve → Augment → Generate)
3. Retornar respostas ao usuário
4. Exibir estatísticas do catálogo

**COMO FUNCIONA:**
```python
app = CatalogoRAG()
resposta = app.processar_consulta("Quero tênis Nike")

# Internamente executa:
# 1. retriever.retrieve() → busca produtos
# 2. augmenter.augment() → formata contexto
# 3. generator.generate() → gera resposta com IA
```

---

### 2. RETRIEVAL: ProductRetriever

```
┌─────────────────────────────┐
│     ProductRetriever        │
├─────────────────────────────┤
│ - db: DatabaseManager       │
│ - processor: TextProcessor  │
├─────────────────────────────┤
│ + retrieve(query, limit)    │
└─────────────────────────────┘
```

**O QUE FAZ:**
- **Primeira etapa do RAG**: Recuperação de informações
- Busca produtos relevantes no banco de dados
- Processa a consulta do usuário

**RESPONSABILIDADES:**
1. Extrair palavras-chave da pergunta do usuário
2. Identificar filtros (categoria, preço, etc)
3. Buscar produtos relevantes no banco
4. Retornar lista de produtos encontrados

**FLUXO DE TRABALHO:**
```
Entrada: "Quero tênis Nike até R$ 500"
   ↓
1. TextProcessor extrai:
   - Palavras-chave: ["tenis", "nike"]
   - Filtros: {categoria: "calçados", preco_max: 500}
   ↓
2. DatabaseManager busca produtos com esses critérios
   ↓
Saída: Lista de 5 produtos mais relevantes
```

**EXEMPLO:**
```python
retriever = ProductRetriever()
produtos = retriever.retrieve("tênis para corrida", limit=5)
# Retorna: [produto1, produto2, produto3, ...]
```

---

### 3. AUGMENTED: ContextAugmenter

```
┌─────────────────────────────┐
│    ContextAugmenter         │
├─────────────────────────────┤
│ (classe com métodos static) │
├─────────────────────────────┤
│ + format_product()$         │
│ + augment()$                │
└─────────────────────────────┘
```

**O QUE FAZ:**
- **Segunda etapa do RAG**: Aumento de contexto
- Transforma produtos em texto formatado
- Prepara informações para o modelo de IA

**RESPONSABILIDADES:**
1. Formatar cada produto em texto legível
2. Destacar promoções e vantagens
3. Criar contexto completo para o LLM
4. Organizar informações de forma clara

**TRANSFORMAÇÃO:**
```python
# ENTRADA: Objeto produto (dict)
produto = {
    "nome": "Tênis Nike Air Max",
    "preco": 499.90,
    "preco_promocional": 449.90,
    "estoque": 45
}

# SAÍDA: Texto formatado
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Tênis Nike Air Max
🔥 PROMOÇÃO! De R$ 499.90 por
💰 R$ 449.90
📊 Estoque: 45 unidades
⭐ Avaliação: 4.8/5.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
```

**POR QUE EXISTE:**
- LLMs funcionam melhor com texto bem formatado
- Facilita a compreensão do modelo
- Destaca informações importantes visualmente

---

### 4. GENERATION: ResponseGenerator

```
┌─────────────────────────────┐
│    ResponseGenerator        │
├─────────────────────────────┤
│ - client: boto3.Client      │
│ - model: ChatBedrock        │
│ - historico: list           │
├─────────────────────────────┤
│ + generate(query, context)  │
│ - _get_historico()          │
└─────────────────────────────┘
```

**O QUE FAZ:**
- **Terceira etapa do RAG**: Geração de respostas
- Usa IA (Claude) para criar respostas naturais
- Mantém histórico da conversa

**RESPONSABILIDADES:**
1. Criar prompt para o Claude
2. Enviar contexto + pergunta para AWS Bedrock
3. Receber e processar resposta do Claude
4. Manter histórico das últimas interações
5. Gerar respostas personalizadas e naturais

**FLUXO:**
```
ENTRADA: 
  query = "Quero tênis para corrida"
  context = "Produtos encontrados: [tênis formatados]"
   ↓
PROCESSAMENTO:
1. Monta prompt do sistema:
   "Você é assistente de vendas..."
   "Catálogo disponível: [context]"
   "Histórico: [últimas conversas]"
   
2. Adiciona mensagem do usuário:
   "Quero tênis para corrida"
   
3. Envia para Claude via AWS Bedrock
   ↓
SAÍDA:
  "Encontrei ótimas opções de tênis para corrida!
   O Nike Air Max está em promoção por R$ 449,90..."
```

**INTEGRAÇÃO COM AWS:**
```python
# Usa boto3 para conectar ao AWS Bedrock
client = boto3.client('bedrock-runtime', region='us-east-1')

# Usa LangChain para facilitar comunicação
model = ChatBedrock(
    model_id='anthropic.claude-3-sonnet-20240229-v1:0',
    client=client
)

# Envia mensagem e recebe resposta
response = model.invoke(messages)
```

---

### 5. DADOS: DatabaseManager

```
┌─────────────────────────────┐
│     DatabaseManager         │
├─────────────────────────────┤
│ - db_path: str              │
├─────────────────────────────┤
│ + get_connection()          │
│ + buscar_produtos()         │
│ + get_estatisticas()        │
│ - _format_results()         │
└─────────────────────────────┘
```

**O QUE FAZ:**
- Gerencia acesso ao banco SQLite
- Executa queries SQL
- Formata resultados

**RESPONSABILIDADES:**
1. Conectar ao banco de dados
2. Buscar produtos com filtros
3. Aplicar condições de busca (LIKE, BETWEEN, etc)
4. Formatar resultados em dicionários Python
5. Gerar estatísticas do catálogo

**EXEMPLO DE USO:**
```python
db = DatabaseManager()

# Buscar produtos
produtos = db.buscar_produtos(
    filtros={
        'termos': ['tenis', 'nike'],
        'categoria': 'calcados',
        'preco_max': 500
    },
    limit=5
)

# Obter estatísticas
stats = db.get_estatisticas()
# Retorna: {
#   'total_produtos': 32,
#   'preco_min': 24.90,
#   'preco_max': 499.90
# }
```

**QUERIES EXECUTADAS:**
```sql
SELECT * FROM produtos 
WHERE (
    LOWER(nome) LIKE '%tenis%' OR 
    LOWER(descricao) LIKE '%tenis%'
)
AND LOWER(categoria) LIKE '%calcados%'
AND preco <= 500
LIMIT 5
```

---

### 6. PROCESSAMENTO: TextProcessor

```
┌─────────────────────────────┐
│      TextProcessor          │
├─────────────────────────────┤
│ + STOP_WORDS: set           │
│ + CATEGORIAS: list          │
├─────────────────────────────┤
│ + remover_acentos()$        │
│ + singular()$               │
│ + extrair_palavras_chave()$ │
│ + extrair_filtros()$        │
└─────────────────────────────┘
```

**O QUE FAZ:**
- Processa texto em português
- Extrai informações da consulta do usuário
- Identifica filtros automaticamente

**RESPONSABILIDADES:**
1. Remover acentos para normalização
2. Converter plural → singular
3. Remover stop words (palavras sem significado)
4. Extrair palavras-chave relevantes
5. Identificar filtros (categoria, preço)

**EXEMPLO PRÁTICO:**

```python
# ENTRADA
query = "Quero tênis Nike até R$ 200"

# PROCESSAMENTO

# 1. Extrair palavras-chave
palavras = TextProcessor.extrair_palavras_chave(query)
# Resultado: ['tenis', 'nike']
# Remove: 'quero', 'até', 'r$' (stop words)

# 2. Extrair filtros
filtros = TextProcessor.extrair_filtros(query)
# Resultado: {
#   'categoria': 'calcados',  # identifica "tênis" → calçados
#   'preco_max': 200.0        # identifica "até R$ 200"
# }
```

**LIMPEZA DE TEXTO:**
```python
"Tênis para corrida" 
   ↓ remover_acentos()
"Tenis para corrida"
   ↓ remover stop words
"Tenis corrida"
   ↓ converter singular
"Teni corrida"  # (exemplo simplificado)
```

---

## 🔗 RELACIONAMENTOS ENTRE CLASSES

### Tipo 1: Composição (diamante preenchido ♦)

**CatalogoRAG contém:**
- ProductRetriever
- ContextAugmenter  
- ResponseGenerator
- DatabaseManager

**SIGNIFICA:**
- CatalogoRAG **possui** essas classes
- Elas são criadas dentro do CatalogoRAG
- Não existem independentemente

```python
class CatalogoRAG:
    def __init__(self):
        self.retriever = ProductRetriever()    # Cria
        self.augmenter = ContextAugmenter()    # Cria
        self.generator = ResponseGenerator()   # Cria
        self.db = DatabaseManager()            # Cria
```

### Tipo 2: Associação (linha simples →)

**ProductRetriever usa:**
- DatabaseManager (para buscar dados)
- TextProcessor (para processar texto)

**SIGNIFICA:**
- ProductRetriever **depende** dessas classes
- Elas são passadas ou criadas para uso

```python
class ProductRetriever:
    def __init__(self):
        self.db = DatabaseManager()      # Usa
        self.processor = TextProcessor()  # Usa
    
    def retrieve(self, query):
        # Usa o processador
        palavras = self.processor.extrair_palavras_chave(query)
        # Usa o banco
        produtos = self.db.buscar_produtos(filtros)
```

### Tipo 3: Dependência (linha tracejada ··>)

**DatabaseManager depende de:**
- sqlite3 (biblioteca Python)

**TextProcessor depende de:**
- re (expressões regulares)
- unicodedata (normalização)

**SIGNIFICA:**
- São bibliotecas externas importadas
- Não fazem parte do sistema

---

## 🎬 FLUXO COMPLETO DO SISTEMA

### Exemplo: Usuário pergunta "Quero tênis Nike até R$ 500"

```
┌──────────────────────────────────────────────────────────────┐
│ 1. ENTRADA                                                   │
│    Usuário digita: "Quero tênis Nike até R$ 500"            │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. CATALOGORAG (Orquestrador)                                │
│    app.processar_consulta("Quero tênis Nike até R$ 500")    │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. RETRIEVAL (ProductRetriever)                              │
│                                                              │
│    3.1 TextProcessor processa a query:                       │
│        • Remove acentos: "tenis", "nike"                    │
│        • Identifica categoria: "calçados"                   │
│        • Identifica preço máximo: 500                       │
│                                                              │
│    3.2 DatabaseManager busca no banco:                       │
│        SELECT * FROM produtos                                │
│        WHERE nome LIKE '%tenis%'                             │
│          OR descricao LIKE '%nike%'                          │
│        AND categoria = 'Calçados'                            │
│        AND preco <= 500                                      │
│        LIMIT 5                                               │
│                                                              │
│    3.3 Retorna: [Produto1, Produto2, Produto3]              │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. AUGMENTED (ContextAugmenter)                              │
│                                                              │
│    Formata cada produto:                                     │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                        │
│    📦 Tênis Nike Air Max                                     │
│    🔥 PROMOÇÃO! De R$ 499.90 por                            │
│    💰 R$ 449.90                                              │
│    📊 Estoque: 45 unidades                                   │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                        │
│                                                              │
│    Monta contexto completo com todos os produtos             │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 5. GENERATION (ResponseGenerator)                            │
│                                                              │
│    5.1 Monta prompt:                                         │
│        System: "Você é assistente de vendas..."             │
│        Context: "[produtos formatados]"                      │
│        Histórico: "[conversas anteriores]"                   │
│        User: "Quero tênis Nike até R$ 500"                  │
│                                                              │
│    5.2 Envia para AWS Bedrock (Claude):                      │
│        API → Claude 3 Sonnet                                 │
│                                                              │
│    5.3 Claude processa e gera resposta natural:              │
│        "Encontrei ótimas opções de tênis Nike! O Air Max    │
│         está em promoção por R$ 449,90, economia de R$ 50!  │
│         Ele tem avaliação 4.8/5 e temos 45 unidades..."     │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 6. SAÍDA                                                     │
│    Resposta exibida para o usuário                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎓 CONCEITOS CHAVE

### RAG (Retrieval-Augmented Generation)

**R**etrieval = Recuperar informações do banco  
**A**ugmented = Aumentar com contexto formatado  
**G**eneration = Gerar resposta com IA  

**POR QUE RAG?**
- LLMs sozinhas não têm acesso a dados específicos
- RAG "aumenta" a capacidade do modelo com informações reais
- Combina busca tradicional + IA generativa

### Pipeline em 3 Etapas

1. **Buscar** (Retrieve) → ProductRetriever  
2. **Formatar** (Augment) → ContextAugmenter  
3. **Responder** (Generate) → ResponseGenerator  

---

## 💡 ANALOGIA DO MUNDO REAL

Imagine uma **loja física**:

1. **ProductRetriever** = Vendedor que procura produtos no estoque
2. **ContextAugmenter** = Organiza produtos na vitrine de forma atraente
3. **ResponseGenerator** = Vendedor experiente que apresenta os produtos
4. **DatabaseManager** = Sistema de inventário da loja
5. **TextProcessor** = Intérprete que entende o que o cliente quer
6. **CatalogoRAG** = Gerente que coordena todo o atendimento

---

## 🔍 SÍMBOLOS DO DIAGRAMA

| Símbolo | Significado |
|---------|-------------|
| `+` | Método público (pode ser chamado de fora) |
| `-` | Atributo privado (uso interno da classe) |
| `$` | Método estático (não precisa de instância) |
| `♦───>` | Composição (contém, possui) |
| `───>` | Associação (usa, depende) |
| `··>` | Dependência (importa biblioteca) |
| `<<external>>` | Classe externa (não faz parte do projeto) |

---

## ✅ CHECKLIST DE COMPREENSÃO

Você entendeu o diagrama se consegue responder:

- [ ] Qual classe coordena todo o sistema?
- [ ] Qual classe busca produtos no banco?
- [ ] Qual classe formata produtos em texto?
- [ ] Qual classe se comunica com a IA?
- [ ] Qual classe processa a linguagem do usuário?
- [ ] Quais são as 3 etapas do RAG?
- [ ] Por que o sistema usa RAG ao invés de só IA?

**Respostas:**
1. CatalogoRAG
2. ProductRetriever (usando DatabaseManager)
3. ContextAugmenter
4. ResponseGenerator
5. TextProcessor
6. Retrieval, Augmented, Generation
7. Para dar ao Claude acesso a dados específicos do catálogo

---

**Documento criado para facilitar o entendimento da arquitetura do sistema RAG**
