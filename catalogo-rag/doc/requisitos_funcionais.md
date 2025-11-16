# 📋 REQUISITOS FUNCIONAIS - SISTEMA RAG CATÁLOGO DE PRODUTOS

## 📊 Informações do Documento

**Sistema:** Assistente Virtual de Produtos (RAG)  
**Versão:** 1.0.0  
**Data:** 15/11/2025  
**Metodologia:** Análise baseada em código-fonte  

---

## 🎯 VISÃO GERAL DO SISTEMA

### Objetivo Principal
Fornecer um assistente virtual inteligente que ajuda usuários a encontrar e conhecer produtos de um catálogo de moda e acessórios através de conversação natural.

### Escopo
- Consulta de catálogo de produtos
- Busca inteligente por texto livre
- Recomendações personalizadas via IA
- Informações detalhadas sobre produtos
- Suporte a promoções e descontos

---

## 📑 LISTA DE REQUISITOS FUNCIONAIS

### RF001 - Consulta de Produtos por Linguagem Natural

**Descrição:** O sistema deve permitir que o usuário faça consultas em linguagem natural sobre produtos.

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Texto livre digitado pelo usuário
- Exemplos: 
  - "Quero um tênis para corrida"
  - "Mostre vestidos até R$ 100"
  - "Tem óculos de sol em promoção?"

**Processamento:**
1. Receber query do usuário
2. Extrair palavras-chave relevantes
3. Identificar filtros implícitos (categoria, preço)
4. Buscar produtos correspondentes
5. Gerar resposta natural com IA

**Saídas:**
- Resposta textual personalizada
- Lista de produtos relevantes
- Informações detalhadas de cada produto

**Regras de Negócio:**
- Máximo de 5 produtos por resposta
- Priorizar produtos em promoção
- Considerar histórico da conversa

**Critérios de Aceitação:**
- ✅ Sistema entende português brasileiro
- ✅ Identifica categoria corretamente
- ✅ Aplica filtros de preço automaticamente
- ✅ Resposta é natural e conversacional

**Rastreabilidade:**
- Classe: `CatalogoRAG.processar_consulta()`
- Arquivo: `app.py`

---

### RF002 - Extração Automática de Palavras-Chave

**Descrição:** O sistema deve extrair automaticamente palavras-chave relevantes da consulta do usuário.

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Texto da consulta do usuário

**Processamento:**
1. Normalizar texto (remover acentos)
2. Remover stop words (palavras sem significado)
3. Converter plural para singular
4. Identificar termos relevantes

**Saídas:**
- Lista de palavras-chave
- Exemplo: "tênis nike" → ["tenis", "nike"]

**Regras de Negócio:**
- Stop words: o, a, de, para, com, que, etc.
- Palavras com menos de 3 caracteres são ignoradas
- Se nenhuma palavra-chave for encontrada, usar palavras longas (>3 chars)

**Critérios de Aceitação:**
- ✅ Remove acentuação corretamente
- ✅ Filtra stop words em português
- ✅ Mantém palavras significativas
- ✅ Funciona com termos compostos

**Rastreabilidade:**
- Classe: `TextProcessor.extrair_palavras_chave()`
- Arquivo: `text_processor.py`

---

### RF003 - Identificação Automática de Filtros

**Descrição:** O sistema deve identificar automaticamente filtros na consulta (categoria, faixa de preço).

**Prioridade:** 🟡 Média (Importante)

**Entradas:**
- Texto da consulta

**Processamento:**
1. Detectar menção a categorias (calçados, roupas, acessórios, fitness)
2. Identificar expressões de preço ("até R$ 100", "acima de R$ 50")
3. Extrair valores numéricos

**Saídas:**
- Dicionário de filtros
```python
{
    'categoria': 'calcados',
    'preco_max': 100.0,
    'preco_min': 50.0
}
```

**Regras de Negócio:**
- Categorias reconhecidas: calçados, roupas, acessórios, fitness
- Expressões de preço máximo: "até", "menos", "abaixo"
- Expressões de preço mínimo: "acima", "mais", "a partir"

**Critérios de Aceitação:**
- ✅ Identifica categoria corretamente
- ✅ Extrai preço máximo de expressões
- ✅ Extrai preço mínimo de expressões
- ✅ Lida com valores sem cifra (R$)

**Rastreabilidade:**
- Classe: `TextProcessor.extrair_filtros()`
- Arquivo: `text_processor.py`

---

### RF004 - Busca de Produtos no Banco de Dados

**Descrição:** O sistema deve buscar produtos no banco de dados aplicando filtros.

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Filtros (termos, categoria, preço_min, preço_max)
- Limite de resultados (padrão: 5)

**Processamento:**
1. Construir query SQL dinâmica
2. Aplicar filtros de texto (LIKE)
3. Aplicar filtros de categoria
4. Aplicar filtros de faixa de preço
5. Limitar quantidade de resultados

**Saídas:**
- Lista de produtos encontrados
- Cada produto com todos os campos

**Regras de Negócio:**
- Busca em nome E descrição do produto
- Case-insensitive (ignora maiúsculas/minúsculas)
- Remove acentos para comparação
- Limite padrão: 10 produtos, configurável

**Critérios de Aceitação:**
- ✅ Busca funciona com acentos
- ✅ Múltiplos termos com OR
- ✅ Filtros combinados funcionam
- ✅ Retorna produtos ordenados por relevância

**Rastreabilidade:**
- Classe: `DatabaseManager.buscar_produtos()`
- Arquivo: `database.py`

---

### RF005 - Formatação de Produtos para Exibição

**Descrição:** O sistema deve formatar produtos em texto visualmente atraente.

**Prioridade:** 🟡 Média (Importante)

**Entradas:**
- Objeto produto (dicionário)

**Processamento:**
1. Formatar preço (normal e promocional)
2. Calcular desconto percentual se houver promoção
3. Adicionar emojis para categorização visual
4. Estruturar informações hierarquicamente

**Saídas:**
- Texto formatado com emojis e separadores
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Tênis Nike Air Max
🔥 PROMOÇÃO! De R$ 499.90 por
💰 R$ 449.90
🏷️ Calçados » Tênis
⭐ Avaliação: 4.8/5.0 (1523 avaliações)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Regras de Negócio:**
- Destacar promoções com emoji 🔥
- Mostrar percentual de desconto
- Incluir avaliação e número de reviews
- Apresentar estoque disponível

**Critérios de Aceitação:**
- ✅ Formato padronizado para todos produtos
- ✅ Destaque visual para promoções
- ✅ Informações completas e organizadas
- ✅ Legível para humanos e IA

**Rastreabilidade:**
- Classe: `ContextAugmenter.format_product()`
- Arquivo: `augmenter.py`

---

### RF006 - Geração de Respostas com IA

**Descrição:** O sistema deve gerar respostas naturais usando Claude (AWS Bedrock).

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Query do usuário
- Contexto formatado (produtos)
- Histórico de conversa

**Processamento:**
1. Montar prompt do sistema com instruções
2. Adicionar contexto do catálogo
3. Incluir histórico das últimas interações
4. Enviar para Claude via AWS Bedrock
5. Processar resposta da IA

**Saídas:**
- Resposta textual natural e personalizada
- Recomendações baseadas no contexto
- Destacando promoções e vantagens

**Regras de Negócio:**
- Modelo: Claude 3 Sonnet
- Max tokens: 500
- Temperature: 0.5 (equilíbrio criatividade/consistência)
- Top_p: 0.9
- Manter até 10 interações no histórico

**Critérios de Aceitação:**
- ✅ Resposta em português brasileiro
- ✅ Tom amigável e profissional
- ✅ Baseada apenas em produtos fornecidos
- ✅ Destaca promoções
- ✅ Mantém contexto da conversa

**Rastreabilidade:**
- Classe: `ResponseGenerator.generate()`
- Arquivo: `generator.py`

---

### RF007 - Manutenção de Histórico de Conversa

**Descrição:** O sistema deve manter histórico das últimas interações para contexto.

**Prioridade:** 🟡 Média (Importante)

**Entradas:**
- Query do usuário
- Resposta gerada

**Processamento:**
1. Adicionar pergunta ao histórico
2. Adicionar resposta ao histórico
3. Manter apenas últimas N interações (configurável)
4. Incluir histórico em próximas consultas

**Saídas:**
- Histórico formatado das últimas conversas

**Regras de Negócio:**
- Máximo de 10 interações mantidas (HISTORICO_MAX)
- Formato: "Cliente: ...", "Assistente: ..."
- Apenas últimas 6 interações enviadas ao Claude

**Critérios de Aceitação:**
- ✅ Histórico persiste durante sessão
- ✅ Limite respeitado automaticamente
- ✅ Claude considera contexto anterior
- ✅ Conversa fluida e coerente

**Rastreabilidade:**
- Classe: `ResponseGenerator.historico`
- Arquivo: `generator.py`

---

### RF008 - Exibição de Estatísticas do Catálogo

**Descrição:** O sistema deve exibir estatísticas gerais do catálogo.

**Prioridade:** 🟢 Baixa (Desejável)

**Entradas:**
- Comando: "stats"

**Processamento:**
1. Contar total de produtos
2. Agrupar por categoria
3. Calcular estatísticas de preço (min, max, média)

**Saídas:**
```
📊 ESTATÍSTICAS DO CATÁLOGO
📦 Total de produtos: 32
💰 Faixa de preços: R$ 24.90 - R$ 499.90
📊 Preço médio: R$ 156.23

🏷️ Produtos por categoria:
   • Calçados: 15 produtos
   • Roupas: 10 produtos
   • Acessórios: 5 produtos
   • Fitness: 2 produtos
```

**Regras de Negócio:**
- Comando especial: "stats"
- Cálculos em tempo real
- Formatação visual com emojis

**Critérios de Aceitação:**
- ✅ Dados precisos e atualizados
- ✅ Formatação clara e legível
- ✅ Resposta imediata

**Rastreabilidade:**
- Classe: `DatabaseManager.get_estatisticas()`
- Método: `CatalogoRAG.mostrar_estatisticas()`
- Arquivo: `database.py`, `app.py`

---

### RF009 - Interface de Linha de Comando (CLI)

**Descrição:** O sistema deve fornecer interface de chat via terminal.

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Texto digitado pelo usuário no terminal

**Processamento:**
1. Exibir boas-vindas e instruções
2. Loop infinito aguardando entrada
3. Processar comandos especiais (sair, stats)
4. Enviar consultas para pipeline RAG
5. Exibir respostas formatadas

**Saídas:**
- Interface conversacional no terminal
- Mensagens de boas-vindas
- Exemplos de uso
- Respostas do assistente

**Regras de Negócio:**
- Comandos especiais: 'sair', 'exit', 'quit', 'stats'
- Tratamento de erros com mensagens amigáveis
- Suporte a interrupção (Ctrl+C)

**Critérios de Aceitação:**
- ✅ Interface intuitiva
- ✅ Exemplos de uso claros
- ✅ Comandos especiais funcionam
- ✅ Tratamento de erros adequado
- ✅ Saída limpa do programa

**Rastreabilidade:**
- Função: `main()`
- Arquivo: `app.py`

---

### RF010 - Validação de Existência do Banco de Dados

**Descrição:** O sistema deve verificar se o banco de dados existe antes de iniciar.

**Prioridade:** 🔴 Alta (Essencial)

**Entradas:**
- Caminho do banco de dados (DB_PATH)

**Processamento:**
1. Verificar se arquivo existe no caminho especificado
2. Se não existir, lançar exceção com mensagem clara

**Saídas:**
- Sucesso: Conexão estabelecida
- Erro: Mensagem indicando ausência do banco

**Regras de Negócio:**
- Caminho configurável em settings.py
- Mensagem deve orientar execução de script de criação

**Critérios de Aceitação:**
- ✅ Detecta ausência do arquivo
- ✅ Mensagem de erro clara
- ✅ Não tenta conectar sem banco
- ✅ Orienta usuário sobre próximo passo

**Rastreabilidade:**
- Classe: `DatabaseManager.__init__()`
- Arquivo: `database.py`

---

### RF011 - Priorização de Produtos em Promoção

**Descrição:** O sistema deve destacar e priorizar produtos com preço promocional.

**Prioridade:** 🟡 Média (Importante)

**Entradas:**
- Produtos com campo `preco_promocional` preenchido

**Processamento:**
1. Detectar se produto tem preço promocional
2. Calcular percentual de desconto
3. Destacar na formatação

**Saídas:**
- Produtos promocionais com destaque visual
- Cálculo de economia

**Regras de Negócio:**
- Desconto % = ((preco - preco_promocional) / preco) * 100
- Destaque: emoji 🔥 e texto "PROMOÇÃO!"
- Mostrar preço original e promocional

**Critérios de Aceitação:**
- ✅ Identifica promoções corretamente
- ✅ Cálculo de desconto preciso
- ✅ Destaque visual efetivo
- ✅ IA menciona promoções nas respostas

**Rastreabilidade:**
- Classe: `ContextAugmenter.format_product()`
- Arquivo: `augmenter.py`

---

### RF012 - Busca Case-Insensitive com Normalização

**Descrição:** O sistema deve buscar produtos ignorando maiúsculas/minúsculas e acentos.

**Prioridade:** 🟡 Média (Importante)

**Entradas:**
- Termo de busca com possíveis acentos e variação de case

**Processamento:**
1. Converter para minúsculas (LOWER)
2. Normalizar acentos (REPLACE)
3. Comparar com dados normalizados

**Saídas:**
- Produtos encontrados independente de formatação

**Regras de Negócio:**
- "Tênis" = "tenis" = "TENIS" = "TêNiS"
- Busca em nome e descrição
- Múltiplos termos com OR

**Critérios de Aceitação:**
- ✅ Encontra produtos com acentos diferentes
- ✅ Não depende de case
- ✅ Busca eficiente com índices

**Rastreabilidade:**
- Método: `DatabaseManager.buscar_produtos()`
- Arquivo: `database.py`

---

### RF013 - Configuração Centralizada

**Descrição:** O sistema deve permitir configuração centralizada de parâmetros.

**Prioridade:** 🟢 Baixa (Desejável)

**Entradas:**
- Arquivo de configuração (settings.py)

**Processamento:**
- Carregar configurações na inicialização

**Saídas:**
- Parâmetros acessíveis em todo o sistema

**Configurações Disponíveis:**
```python
# AWS
AWS_REGION = 'us-east-1'

# Bedrock
BEDROCK_MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'
MAX_TOKENS = 500
TEMPERATURE = 0.5
TOP_P = 0.9

# Database
DB_PATH = 'data/catalogo.db'

# Aplicação
APP_NAME = "Assistente Virtual de Produtos"
APP_VERSION = "1.0.0"
HISTORICO_MAX = 10
```

**Critérios de Aceitação:**
- ✅ Configurações centralizadas
- ✅ Fácil manutenção
- ✅ Valores padrão sensatos
- ✅ Documentado

**Rastreabilidade:**
- Arquivo: `settings.py`

---

### RF014 - Debug e Logging

**Descrição:** O sistema deve fornecer informações de debug durante execução.

**Prioridade:** 🟢 Baixa (Desejável)

**Entradas:**
- Operações do sistema

**Processamento:**
- Imprimir informações de debug em pontos-chave

**Saídas:**
```
🔍 DEBUG - Palavras-chave: ['tenis', 'nike']
📦 DEBUG - Produtos encontrados: 3
```

**Regras de Negócio:**
- Apenas em modo de desenvolvimento
- Remover em produção

**Critérios de Aceitação:**
- ✅ Facilita debugging
- ✅ Informações úteis
- ✅ Não interfere na UX

**Rastreabilidade:**
- Classe: `ProductRetriever.retrieve()`
- Arquivo: `retriever.py`

---

## 📊 MATRIZ DE RASTREABILIDADE

| ID | Requisito | Prioridade | Classe/Método | Status |
|----|-----------|------------|---------------|--------|
| RF001 | Consulta por linguagem natural | 🔴 Alta | CatalogoRAG.processar_consulta() | ✅ Implementado |
| RF002 | Extração de palavras-chave | 🔴 Alta | TextProcessor.extrair_palavras_chave() | ✅ Implementado |
| RF003 | Identificação de filtros | 🟡 Média | TextProcessor.extrair_filtros() | ✅ Implementado |
| RF004 | Busca no banco de dados | 🔴 Alta | DatabaseManager.buscar_produtos() | ✅ Implementado |
| RF005 | Formatação de produtos | 🟡 Média | ContextAugmenter.format_product() | ✅ Implementado |
| RF006 | Geração com IA | 🔴 Alta | ResponseGenerator.generate() | ✅ Implementado |
| RF007 | Histórico de conversa | 🟡 Média | ResponseGenerator.historico | ✅ Implementado |
| RF008 | Estatísticas do catálogo | 🟢 Baixa | DatabaseManager.get_estatisticas() | ✅ Implementado |
| RF009 | Interface CLI | 🔴 Alta | main() | ✅ Implementado |
| RF010 | Validação do banco | 🔴 Alta | DatabaseManager.__init__() | ✅ Implementado |
| RF011 | Destaque de promoções | 🟡 Média | ContextAugmenter | ✅ Implementado |
| RF012 | Busca normalizada | 🟡 Média | DatabaseManager + TextProcessor | ✅ Implementado |
| RF013 | Configuração centralizada | 🟢 Baixa | settings.py | ✅ Implementado |
| RF014 | Debug e logging | 🟢 Baixa | ProductRetriever | ✅ Implementado |

---

## 🎯 REQUISITOS POR CATEGORIA

### Busca e Recuperação (Retrieval)
- RF001 - Consulta por linguagem natural
- RF002 - Extração de palavras-chave
- RF003 - Identificação de filtros
- RF004 - Busca no banco de dados
- RF012 - Busca case-insensitive

### Apresentação (Augmented)
- RF005 - Formatação de produtos
- RF011 - Destaque de promoções

### Geração de Respostas (Generation)
- RF006 - Geração com IA
- RF007 - Histórico de conversa

### Interface e UX
- RF009 - Interface CLI
- RF008 - Estatísticas

### Infraestrutura
- RF010 - Validação do banco
- RF013 - Configuração centralizada
- RF014 - Debug e logging

---

## 📈 COBERTURA DE REQUISITOS

**Total de Requisitos:** 14  
**Implementados:** 14 (100%)  
**Em Desenvolvimento:** 0  
**Pendentes:** 0  

### Prioridades
- 🔴 **Alta (Essencial):** 6 requisitos (43%)
- 🟡 **Média (Importante):** 5 requisitos (36%)
- 🟢 **Baixa (Desejável):** 3 requisitos (21%)

---

## 🔄 FLUXO DE REQUISITOS

```
Usuário digita consulta
        ↓
    [RF009] Interface CLI
        ↓
    [RF001] Processa consulta
        ↓
┌───────┴────────┐
│   RETRIEVAL    │
├────────────────┤
│ [RF002] Extrair palavras-chave
│ [RF003] Identificar filtros
│ [RF004] Buscar no banco
│ [RF012] Normalização
└───────┬────────┘
        ↓
┌───────┴────────┐
│   AUGMENTED    │
├────────────────┤
│ [RF005] Formatar produtos
│ [RF011] Destacar promoções
└───────┬────────┘
        ↓
┌───────┴────────┐
│  GENERATION    │
├────────────────┤
│ [RF006] Gerar resposta IA
│ [RF007] Usar histórico
└───────┬────────┘
        ↓
 Resposta ao usuário
```

---

## 🎓 REQUISITOS NÃO FUNCIONAIS IDENTIFICADOS

Embora não sejam requisitos funcionais, o código implementa:

### Performance
- Limite de 5 produtos por busca (evita sobrecarga)
- Índices no banco de dados
- Histórico limitado a 10 interações

### Usabilidade
- Interface em português brasileiro
- Mensagens de erro amigáveis
- Exemplos de uso na inicialização

### Confiabilidade
- Validação de existência do banco
- Tratamento de exceções
- Fallback quando não há palavras-chave

### Manutenibilidade
- Configuração centralizada
- Código modular (classes separadas)
- Debug mode disponível

---

## 📝 REQUISITOS FUTUROS SUGERIDOS

Com base na análise, sugerimos:

1. **RF015 - Filtro por Marca**
   - Permitir busca específica por marca
   - Ex: "mostre todos os produtos Nike"

2. **RF016 - Ordenação de Resultados**
   - Ordenar por preço, avaliação, popularidade
   - Ex: "mais baratos primeiro", "mais bem avaliados"

3. **RF017 - Comparação de Produtos**
   - Comparar características de múltiplos produtos
   - Ex: "compare o tênis Nike com o Adidas"

4. **RF018 - Notificação de Estoque Baixo**
   - Alertar quando estoque < 10 unidades
   - Sugerir produtos similares se esgotado

5. **RF019 - Persistência de Histórico**
   - Salvar histórico entre sessões
   - Recuperar conversas anteriores

6. **RF020 - Exportação de Resultados**
   - Exportar produtos encontrados (PDF, CSV)
   - Compartilhar resultados

---

## ✅ VALIDAÇÃO DOS REQUISITOS

Todos os requisitos identificados foram:
- ✅ Implementados no código
- ✅ Testados via execução
- ✅ Documentados neste documento
- ✅ Rastreáveis ao código-fonte

---

**Documento de Requisitos Funcionais v1.0**  
**Gerado a partir da análise do código-fonte**  
**Data: 15/11/2025**
