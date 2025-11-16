# 🛍️ Meteora - Assistente Virtual de E-commerce com RAG

Um chatbot inteligente especializado em moda que utiliza **RAG (Retrieval-Augmented Generation)** para fornecer informações precisas sobre produtos de vestuário, consultando um banco de dados SQLite em tempo real.

## 📋 Descrição

O **Meteora** é um assistente virtual desenvolvido para e-commerce de moda que combina:
- **LLM Claude (Anthropic)** via AWS Bedrock
- **RAG** para consultas em tempo real ao banco de dados
- **Prompt Engineering** otimizado para respostas concisas
- **LangChain** para orquestração de prompts

O sistema garante que todas as respostas sejam baseadas em dados reais do inventário, evitando alucinações do modelo.

## ✨ Características Principais

- ✅ **Consulta em tempo real** ao banco de dados de produtos
- ✅ **Respostas baseadas em dados reais** (sem invenções)
- ✅ **Busca inteligente** por nome de produto
- ✅ **Informações completas**: nome, preço e estoque
- ✅ **Escopo controlado**: apenas perguntas sobre moda
- ✅ **Sugestões alternativas** quando produto não encontrado
- ✅ **Interface conversacional** amigável
- ✅ **Histórico de conversação**

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **AWS Bedrock** (Claude 3.5 Haiku)
- **LangChain** - Orquestração de LLM
- **SQLite** - Banco de dados local
- **Boto3** - SDK AWS para Python

## 📁 Estrutura do Projeto

```
meteora-chatbot/
│
├── chatbot_v1.py              # Versão inicial do chatbot
├── chatbot_v2_refinado.py     # Versão refinada com melhorias
├── criar_banco.py             # Script de criação do banco
├── diagnostico_banco.py       # Script de diagnóstico
├── produtos.db                # Banco SQLite (gerado)
└── README.md                  # Este arquivo
```

## 📦 Pré-requisitos

### 1. Conta AWS com acesso ao Bedrock
```bash
# Configure suas credenciais AWS
aws configure
```

### 2. Dependências Python
```bash
pip install boto3 langchain-core
```

### 3. Permissões AWS Bedrock
Certifique-se de ter acesso ao modelo:
- `us.anthropic.claude-3-5-haiku-20241022-v1:0`
- Região: `us-east-2`

## 🚀 Instalação

### Passo 1: Clone o repositório
```bash
git clone <seu-repositorio>
cd meteora-chatbot
```

### Passo 2: Instale as dependências
```bash
pip install boto3 langchain-core
```

### Passo 3: Configure AWS
```bash
aws configure
# Insira:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-2
```

### Passo 4: Crie o banco de dados
```bash
python criar_banco.py
```

Isso criará `produtos.db` com 21 produtos de exemplo.

## 💻 Uso

### Executar o chatbot (versão refinada)
```bash
python chatbot_v2_refinado.py
```

### Comandos disponíveis
| Comando | Descrição |
|---------|-----------|
| `produtos` | Lista todo o catálogo |
| `sair` | Encerra o chatbot |

### Exemplos de perguntas

```
User: Tem camiseta?
Assistente:
Sim! Temos a Camiseta Básica por R$ 29,99 com 150 unidades em estoque, 
e a Camiseta de Algodão por R$ 25,00 com 100 unidades disponíveis.

User: Quanto custa jaqueta?
Assistente:
A Jaqueta de Couro (couro sintético, preta) custa R$ 299,99 
e temos 20 unidades disponíveis.

User: Tem notebook?
Assistente:
Desculpe, não trabalhamos com eletrônicos. Posso ajudá-lo 
com roupas, calçados ou acessórios de moda?
```

## 🗄️ Estrutura do Banco de Dados

### Tabela: `roupas`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | Chave primária (auto-incremento) |
| `nome` | TEXT | Nome do produto |
| `descricao` | TEXT | Descrição detalhada |
| `preco` | REAL | Preço em R$ |
| `estoque` | INTEGER | Quantidade disponível |

### Produtos inclusos (21 itens)
- Roupas: Camisetas, Calças, Vestidos, Blusas, Jaquetas, etc.
- Calçados: Tênis, Sapatênis
- Acessórios: Bolsas, Relógios, Óculos, Cachecóis, etc.

## 🔧 Diagnóstico

Para verificar a estrutura do banco:
```bash
python diagnostico_banco.py
```

## 📊 Diferenças entre Versões

### V1 (chatbot_v1.py)
- ✅ RAG básico
- ✅ Busca apenas por nome
- ✅ Remoção de duplicatas
- ✅ Debug visual

### V2 Refinada (chatbot_v2_refinado.py)
- ✅ Busca em **nome E descrição**
- ✅ Prompt engineering aprimorado
- ✅ Formatação de produtos melhorada
- ✅ Instruções mais detalhadas ao modelo
- ✅ Melhor tratamento de casos sem resultados
- ✅ Interface aprimorada

## ⚙️ Configuração do Modelo

Parâmetros otimizados do Claude:

```python
max_tokens = 300      # ~225 palavras
temperature = 0.5     # Balanceado
top_p = 0.9          # Diversidade controlada
```

## 🎯 Prompt Engineering

### System Prompt
Define o comportamento:
- Escopo: apenas moda
- Fonte: apenas banco de dados
- Limite: 300 caracteres
- Tom: profissional e amigável

### RAG Augmentation
Injeta contexto relevante:
```
PRODUTOS DISPONÍVEIS:
[dados do banco]

PERGUNTA: [pergunta do usuário]

INSTRUÇÕES: [diretrizes específicas]
```

## 🔒 Segurança

- ✅ Sem exposição de credenciais no código
- ✅ Usa AWS IAM para autenticação
- ✅ Consultas SQL parametrizadas (proteção contra injection)
- ✅ Validação de entrada do usuário

## 🚀 Melhorias Futuras

- [ ] Adicionar filtros (preço, categoria)
- [ ] Implementar busca semântica com embeddings
- [ ] Interface web com Flask/Streamlit
- [ ] Sistema de recomendações
- [ ] Integração com APIs de pagamento
- [ ] Histórico persistente de conversas
- [ ] Métricas e analytics

## 🤝 Arquitetura do Sistema

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────┐
│  Interface (CLI)            │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  RAG Pipeline               │
│  ┌──────────────────────┐   │
│  │ 1. Consulta Banco    │   │
│  │ 2. Formata Contexto  │   │
│  │ 3. Augmenta Prompt   │   │
│  └──────────────────────┘   │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  AWS Bedrock                │
│  (Claude 3.5 Haiku)         │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  SQLite (produtos.db)       │
└─────────────────────────────┘
```

## 📈 Fluxo de Funcionamento

1. **Usuário faz pergunta** → "Tem camiseta?"
2. **Sistema extrai palavras-chave** → "camiseta"
3. **Consulta banco de dados** → `SELECT * FROM roupas WHERE nome LIKE '%camiseta%'`
4. **Formata dados encontrados** → Estrutura com preço, estoque, descrição
5. **Augmenta o prompt** → Adiciona contexto ao prompt original
6. **Envia para Claude** → Via AWS Bedrock
7. **Recebe resposta** → Resposta baseada em dados reais
8. **Exibe ao usuário** → Formatada e amigável

## 🐛 Troubleshooting

### Erro: "NoCredentialsError"
```bash
# Configure suas credenciais AWS
aws configure
```

### Erro: "AccessDeniedException"
Verifique se sua conta AWS tem permissão para acessar o Bedrock e o modelo Claude.

### Erro: "produtos.db não encontrado"
```bash
# Execute o script de criação do banco
python criar_banco.py
```

### Chatbot não encontra produtos
Execute o diagnóstico:
```bash
python diagnostico_banco.py
```

## 📚 Recursos Adicionais

- [Documentação AWS Bedrock](https://docs.aws.amazon.com/bedrock/)
- [LangChain Documentation](https://python.langchain.com/)
- [Claude API Reference](https://docs.anthropic.com/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## 📝 Licença

Este projeto é open source e está disponível sob a licença MIT.

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📧 Contato

Dúvidas ou sugestões? Abra uma issue no repositório!

---

⭐ **Desenvolvido com Claude e AWS Bedrock**
