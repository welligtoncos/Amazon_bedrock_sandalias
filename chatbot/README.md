# 🛍️ Meteora - Assistente Virtual com AWS Bedrock

Três implementações progressivas de um chatbot inteligente para e-commerce de moda, utilizando Claude 3.5 Haiku via AWS Bedrock.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Versão 1: Chatbot Básico](#versão-1-chatbot-básico)
- [Versão 2: Com Histórico de Conversas](#versão-2-com-histórico-de-conversas)
- [Versão 3: Avançado com Estatísticas](#versão-3-avançado-com-estatísticas)
- [Comparação entre Versões](#comparação-entre-versões)
- [Configuração](#configuração)
- [Estrutura do Projeto](#estrutura-do-projeto)

---

## 🎯 Visão Geral

Este projeto demonstra três níveis de complexidade na construção de um assistente virtual usando AWS Bedrock e o modelo Claude 3.5 Haiku da Anthropic. Cada versão adiciona funcionalidades progressivamente mais sofisticadas.

**Caso de Uso:** Assistente virtual para a Meteora, um e-commerce de moda e vestuário, capaz de responder perguntas sobre produtos, recomendar itens e auxiliar clientes.

---

## 🔧 Pré-requisitos

### Requisitos Técnicas
- Python 3.8+
- Conta AWS ativa
- Acesso ao AWS Bedrock com modelo Claude habilitado
- Credenciais AWS configuradas

### Dependências
```bash
pip install boto3
```

### Configuração AWS
```bash
# Configurar credenciais AWS
aws configure

# Ou via variáveis de ambiente
export AWS_ACCESS_KEY_ID="sua-chave"
export AWS_SECRET_ACCESS_KEY="sua-chave-secreta"
export AWS_DEFAULT_REGION="us-east-2"
```

---

## 📦 Versão 1: Chatbot Básico

### Arquivo: `chatbot_basico.py`

### 🎯 O que faz
Implementação mais simples do chatbot. Cada pergunta é tratada de forma independente, sem memória de conversas anteriores.

### ✨ Funcionalidades
- ✅ Comunicação direta com AWS Bedrock
- ✅ Respostas limitadas a 300 caracteres (economia de tokens)
- ✅ System prompt configurado para assistente de moda
- ✅ Interface de linha de comando simples
- ✅ Comando para sair (`sair`, `exit`, `quit`, `tchau`)

### 🚀 Como usar
```bash
python chatbot_basico.py
```

### 💡 Exemplo de Uso
```
🛍️  METEORA - ASSISTENTE VIRTUAL
================================================================================

Assistente: Olá! Sou seu Assistente Virtual da Meteora. 😊
Em que posso ajudar hoje?

💡 Dica: Digite 'sair' para encerrar

Você: Que tipo de roupas vocês vendem?

Assistente: Oferecemos roupas casuais e formais, incluindo camisetas, calças, 
vestidos, jaquetas e acessórios para todas as ocasiões. O que você procura?

Você: sair

Assistente: Foi um prazer ajudá-lo(a)! Até logo! 👋
```

### ⚠️ Limitações
- **Sem memória**: Não lembra de perguntas anteriores
- **Sem contexto**: Cada pergunta é tratada isoladamente
- **Sem estatísticas**: Não rastreia custos ou uso

### 🎓 Ideal para
- Aprender os fundamentos de AWS Bedrock
- Testes rápidos e prototipagem
- Casos onde contexto não é necessário

---

## 💬 Versão 2: Com Histórico de Conversas

### Arquivo: `chatbot_com_historico.py`

### 🎯 O que faz
Adiciona memória ao chatbot, permitindo conversas contextualizadas. O assistente "lembra" das mensagens anteriores e pode referenciá-las.

### ✨ Funcionalidades
- ✅ **Histórico de conversa**: Mantém até 10 pares de mensagens (usuário + assistente)
- ✅ **Contexto preservado**: Responde considerando mensagens anteriores
- ✅ **Gerenciamento de memória**: Remove mensagens antigas automaticamente
- ✅ **Comandos adicionais**:
  - `limpar` - Reseta o histórico
  - `historico` - Mostra quantas conversas estão armazenadas
- ✅ **Tratamento de erros robusto**

### 🧠 Como funciona o histórico

```python
# Estrutura do histórico
[
    {"role": "user", "content": "Vocês vendem camisetas?"},
    {"role": "assistant", "content": "Sim! Temos diversos modelos..."},
    {"role": "user", "content": "E qual o preço médio?"},  # ← Contexto preservado
    {"role": "assistant", "content": "Das camisetas que mencionei..."}
]
```

**Controle de limite**: Quando o histórico atinge 20 mensagens (10 conversas), as mais antigas são removidas automaticamente.

### 🚀 Como usar
```bash
python chatbot_com_historico.py
```

### 💡 Exemplo de Uso Contextual
```
Você: Vocês vendem jaquetas de couro?

Assistente: Sim! Temos jaquetas de couro genuíno e sintético, em diversos 
estilos: bomber, biker e clássicas. Qual estilo te interessa?

Você: Quanto custa a bomber?

Assistente: A jaqueta bomber em couro sintético custa R$ 299, e a de couro 
genuíno R$ 599. Ambas disponíveis em várias cores!

Você: limpar
🗑️  Histórico limpo! Conversa reiniciada.

Você: Quanto custa?

Assistente: Olá! Para informar o preço, preciso saber qual produto você 
procura. Temos roupas, calçados e acessórios. O que te interessa?
```

### 📊 Comandos Especiais
```
limpar     → Limpa todo o histórico
historico  → Mostra: "3/10 conversas armazenadas"
sair       → Encerra o chatbot
```

### ⚙️ Configurações Ajustáveis
```python
MAX_HISTORICO = 10  # Número máximo de pares de mensagens
# Aumentar = mais contexto, mais custo
# Diminuir = menos contexto, menos custo
```

### 🎓 Ideal para
- Conversas complexas que exigem contexto
- Atendimento ao cliente com múltiplas perguntas
- Quando o usuário refere-se a mensagens anteriores

---

## 📊 Versão 3: Avançado com Estatísticas

### Arquivo: `chatbot_avancado.py`

### 🎯 O que faz
Versão profissional com todas as funcionalidades anteriores + rastreamento detalhado de uso, custos e performance.

### ✨ Funcionalidades

#### Tudo da Versão 2 +
- ✅ **Rastreamento de custos em tempo real**
- ✅ **Contador de tokens (entrada e saída)**
- ✅ **Estatísticas por requisição**
- ✅ **Relatório completo da sessão**
- ✅ **Cálculo de custo médio por pergunta**
- ✅ **Duração da sessão**
- ✅ **Conversão USD → BRL**

### 💰 Cálculo de Custos

O chatbot calcula automaticamente os custos baseado na tabela de preços do Claude 3.5 Haiku:

```python
# Preços por 1 milhão de tokens
Input:  $0.80
Output: $4.00

# Exemplo de cálculo
1000 tokens input  = $0.0008
50 tokens output   = $0.0002
Total              = $0.0010 (≈ R$ 0.0055)
```

### 🚀 Como usar
```bash
python chatbot_avancado.py
```

### 💡 Exemplo de Uso com Estatísticas
```
Você: Vocês têm vestidos para festa?

🤖 Assistente: Sim! Temos vestidos para festas, formais e casuais. 
Temos modelos longos, curtos, com brilho, lisos, em diversas cores e 
tamanhos. Qual estilo você procura?
   💰 $0.000234 | 📊 45 tokens

---------------------------------------------------------------------

Você: stats

================================================================================
📊 ESTATÍSTICAS DA SESSÃO
================================================================================
⏱️  Duração: 2min 15s
💬 Total de perguntas: 5
📥 Tokens de entrada: 1,234
📤 Tokens de saída: 567
💰 Custo total: $0.002850 (≈ R$ 0.0157)
📊 Custo médio/pergunta: $0.000570
================================================================================
```

### 📈 Relatório Final (ao sair)
```
🤖 Assistente: Foi um prazer ajudá-lo(a)! Até logo! 👋

================================================================================
📊 ESTATÍSTICAS DA SESSÃO
================================================================================
⏱️  Duração: 15min 32s
💬 Total de perguntas: 23
📥 Tokens de entrada: 5,678
📤 Tokens de saída: 2,345
💰 Custo total: $0.014102 (≈ R$ 0.0776)
📊 Custo médio/pergunta: $0.000613
================================================================================

👋 Até logo!
```

### 📊 Comandos Especiais
```
stats      → Mostra estatísticas parciais sem encerrar
limpar     → Limpa histórico (mantém estatísticas)
historico  → Mostra conversas armazenadas
sair       → Encerra e exibe relatório completo
```

### 🎓 Ideal para
- **Ambientes de produção**: Monitoramento de custos
- **Análise de performance**: Otimização de prompts
- **Gestão de orçamento**: Controle de gastos com IA
- **Auditoria**: Rastreamento detalhado de uso

---

## 📊 Comparação entre Versões

| Característica | v1 Básico | v2 Histórico | v3 Avançado |
|----------------|-----------|--------------|-------------|
| **Complexidade** | ⭐ Simples | ⭐⭐ Média | ⭐⭐⭐ Alta |
| **Linhas de código** | ~80 | ~120 | ~180 |
| **Histórico** | ❌ Não | ✅ Sim (10 conversas) | ✅ Sim (10 conversas) |
| **Contexto** | ❌ Não | ✅ Sim | ✅ Sim |
| **Estatísticas** | ❌ Não | ❌ Não | ✅ Completas |
| **Rastreamento de custos** | ❌ Não | ❌ Não | ✅ Sim |
| **Contagem de tokens** | ❌ Não | ❌ Não | ✅ Sim |
| **Relatórios** | ❌ Não | ❌ Não | ✅ Sim |
| **Ideal para** | Protótipos | Atendimento | Produção |
| **Uso recomendado** | Aprendizado | Cliente final | Empresarial |

---

## ⚙️ Configuração

### 1. Parâmetros Comuns (Todas as versões)

```python
# Região AWS (ajuste conforme sua região)
region_name = 'us-east-2'

# Modelo Claude
MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Limite de resposta (economia de tokens)
max_tokens = 300

# Criatividade (0.0 = determinístico, 1.0 = criativo)
temperature = 0.5
```

### 2. System Prompt

O comportamento do assistente é definido no `SYSTEM_PROMPT`:

```python
SYSTEM_PROMPT = """Você é um assistente virtual da Meteora, 
um e-commerce de moda e vestuário.

DIRETRIZES:
- Seja conciso: máximo 300 caracteres por resposta
- Foque em produtos de moda: roupas, calçados, acessórios
- Mantenha tom profissional e amigável
- Use o contexto das mensagens anteriores
- Sempre ofereça alternativas quando possível"""
```

**Dica**: Customize este prompt para seu caso de uso!

### 3. Ajuste de Histórico (v2 e v3)

```python
MAX_HISTORICO = 10  # Pares de mensagens (user + assistant)

# Cálculo de impacto:
# - 10 conversas = ~2000-3000 tokens por requisição
# - 5 conversas = ~1000-1500 tokens por requisição
# - 20 conversas = ~4000-6000 tokens por requisição
```

---

## 📁 Estrutura do Projeto

```
meteora-chatbot/
├── README.md                      # Este arquivo
├── chatbot_basico.py              # Versão 1
├── chatbot_com_historico.py       # Versão 2
├── chatbot_avancado.py            # Versão 3
└── requirements.txt               # Dependências
```

### `requirements.txt`
```txt
boto3>=1.28.0
```

---

## 🚀 Instalação e Execução

### 1. Clone ou baixe os arquivos
```bash
# Baixar os três scripts Python
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure AWS
```bash
aws configure
# Insira: Access Key, Secret Key, Região (us-east-2)
```

### 4. Execute a versão desejada
```bash
# Versão 1 - Básico
python chatbot_basico.py

# Versão 2 - Com Histórico
python chatbot_com_historico.py

# Versão 3 - Avançado
python chatbot_avancado.py
```

---

## 💡 Dicas de Uso

### Otimização de Custos
1. **Use Versão 1** para testes rápidos (sem contexto = menos tokens)
2. **Ajuste `MAX_HISTORICO`** na v2/v3 baseado na necessidade real
3. **Limite `max_tokens`** para respostas concisas
4. **Use temperatura baixa** (0.3-0.5) para respostas consistentes

### Melhores Práticas
- **System Prompt**: Seja específico sobre o comportamento desejado
- **Contexto**: Use histórico apenas quando necessário
- **Erros**: Sempre trate exceções (ThrottlingException, etc.)
- **Monitoramento**: Use v3 em produção para rastrear custos

### Solução de Problemas

**Erro: "ThrottlingException"**
```
Causa: Muitas requisições em curto período
Solução: Aguarde alguns segundos entre requisições
```

**Erro: "ValidationException"**
```
Causa: Modelo não habilitado no Bedrock
Solução: Ative o Claude 3.5 Haiku no console AWS Bedrock
```

**Erro: "CredentialsError"**
```
Causa: Credenciais AWS não configuradas
Solução: Execute 'aws configure'
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

### Custos Claude 3.5 Haiku
- Input: $0.80 / 1M tokens
- Output: $4.00 / 1M tokens
- [Pricing oficial](https://www.anthropic.com/pricing)

---

## 🎯 Próximos Passos

### Possíveis Melhorias
1. **Interface Web**: Criar UI com Flask/Streamlit
2. **Streaming**: Respostas em tempo real (palavra por palavra)
3. **Múltiplos usuários**: Sistema de sessões
4. **Integração**: Conectar com catálogo de produtos real
5. **Analytics**: Dashboard com métricas de uso
6. **RAG**: Adicionar busca em base de conhecimento

### Evolução Recomendada
```
Básico → Histórico → Avançado → Web Interface → Produção
  ↓         ↓            ↓            ↓            ↓
Aprender  Testar    Monitorar    Escalar    Otimizar
```

---

## 📄 Licença

Este projeto é fornecido como exemplo educacional. Adapte conforme necessário.

---

## 🤝 Contribuições

Sugestões de melhorias são bem-vindas! 

---

**Desenvolvido com ❤️ para demonstrar o poder da AWS Bedrock + Claude**

🛍️ **Meteora** - Seu Assistente Virtual Inteligente
