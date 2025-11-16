# 🛍️ Assistente Virtual de Moda para E-commerce

Chatbot inteligente especializado em moda e vestuário, utilizando AWS Bedrock com Claude 3.5 Haiku e LangChain para oferecer respostas concisas e úteis sobre produtos de vestuário.

## 📋 Descrição

Este projeto implementa um assistente virtual conversacional focado em e-commerce de moda. O bot utiliza o modelo Claude 3.5 Haiku através do AWS Bedrock para fornecer respostas personalizadas, mantendo um histórico de conversação.

## ✨ Funcionalidades

- 💬 Interface de chat interativa via terminal
- 🤖 Respostas geradas por IA especializadas em moda
- 📝 Manutenção de histórico de conversação
- ⚡ Respostas concisas (máximo 300 caracteres)
- 🔄 Integração com AWS Bedrock
- 🎯 Prompt engineering otimizado para e-commerce

## 🔧 Pré-requisitos

- Python 3.8+
- Conta AWS com acesso ao Bedrock
- Credenciais AWS configuradas
- Acesso ao modelo Claude 3.5 Haiku na região `us-east-2`

## 📦 Instalação

```bash
# Instalar dependências
pip install boto3 langchain-core
```

## ⚙️ Configuração

### 1. Credenciais AWS

Configure suas credenciais AWS usando um dos métodos:

**Opção A: AWS CLI**
```bash
aws configure
```

**Opção B: Variáveis de ambiente**
```bash
export AWS_ACCESS_KEY_ID="sua_access_key"
export AWS_SECRET_ACCESS_KEY="sua_secret_key"
export AWS_DEFAULT_REGION="us-east-2"
```

**Opção C: Arquivo de credenciais**
```
~/.aws/credentials
```

### 2. Parâmetros do Modelo

O código utiliza as seguintes configurações (ajustáveis no código):

```python
MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
region_name = "us-east-2"
max_tokens = 300
temperature = 0.5
```

## 🚀 Como Usar

1. Execute o script:
```bash
python assistente_moda.py
```

2. Converse com o assistente:
```
Assistente: Olá! Sou seu Assistente Virtual. :)
Em que posso ajudar hoje?
User: Qual a diferença entre jeans slim e skinny?
Assistente:
Jeans slim tem corte ajustado mas confortável, acompanhando a silhueta sem apertar muito. 
Jeans skinny é mais justo, colado ao corpo da cintura ao tornozelo. 
Slim é ideal para look casual elegante, skinny para visual moderno e estilizado.
```

3. Para sair, digite:
```
User: sair
```

## 📁 Estrutura do Código

```
├── Configuração do Bedrock
│   └── Cliente boto3 + região
├── Função _invocar_bedrock()
│   └── Invocação direta do modelo
├── Modelo LangChain
│   └── RunnableLambda wrapper
├── Sistema de Histórico
│   └── Lista de mensagens
├── Template de Prompt
│   └── ChatPromptTemplate
├── Função inv_modelo()
│   └── Chain completo
└── Loop Principal
    └── Interface de chat
```

## 🔑 Componentes Principais

### `_invocar_bedrock(messages)`
Função interna que realiza a invocação direta da API do Bedrock, processando entrada e retornando a resposta do modelo.

### `get_chat_prompt(entrada)`
Cria o template de prompt com contexto de sistema e instruções específicas para e-commerce de moda.

### `inv_modelo(prompt)`
Orquestra o fluxo completo: template → modelo → resposta.

### `historico`
Lista que armazena todas as interações para contexto futuro.

## 💡 Exemplo de Uso

```python
# Perguntas sobre produtos
User: Como escolher o tamanho de camisa?

# Dúvidas sobre estilo
User: Qual tipo de sapato combina com calça social?

# Informações sobre cuidados
User: Como lavar roupa de seda?

# Recomendações
User: Sugestões de looks para entrevista de emprego
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Boto3** - SDK AWS para Python
- **LangChain Core** - Framework para aplicações com LLMs
- **AWS Bedrock** - Serviço de IA gerenciado
- **Claude 3.5 Haiku** - Modelo de linguagem da Anthropic

## ⚠️ Notas Importantes

1. **Custos**: O uso do AWS Bedrock é cobrado por tokens processados
2. **Região**: O modelo deve estar disponível na região configurada (us-east-2)
3. **Permissões**: A conta AWS precisa ter permissões para `bedrock:InvokeModel`
4. **Limites**: Respostas limitadas a 300 caracteres por design
5. **Histórico**: Armazenado apenas em memória (perdido ao fechar o programa)

## 🔒 Segurança

- Nunca commite credenciais AWS no código
- Use IAM roles quando possível (EC2, Lambda, etc)
- Implemente rate limiting para produção
- Monitore custos no AWS Cost Explorer

## 📈 Melhorias Futuras

- [ ] Persistência de histórico em banco de dados
- [ ] Interface web com Streamlit/Gradio
- [ ] Suporte a múltiplos idiomas
- [ ] Sistema de feedback do usuário
- [ ] Cache de respostas comuns
- [ ] Integração com catálogo de produtos
- [ ] Análise de sentimento

## 📄 Licença

Este projeto é um exemplo educacional. Adapte conforme necessário para seu caso de uso.

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas!

---

**Desenvolvido com ❤️ para e-commerce de moda**
