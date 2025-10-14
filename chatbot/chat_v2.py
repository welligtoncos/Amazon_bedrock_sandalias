import boto3
import json

# ============================================
# CONFIGURAÇÕES
# ============================================
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'  # Custo 73% menor
MAX_HISTORICO = 10  # Limita histórico para controlar custos

# System Prompt (instruções gerais do assistente)
SYSTEM_PROMPT = """Você é um assistente virtual da Meteora, um e-commerce de moda e vestuário.

DIRETRIZES:
- Seja conciso: máximo 300 caracteres por resposta
- Foque em produtos de moda: roupas, calçados, acessórios
- Mantenha tom profissional e amigável
- Use o contexto das mensagens anteriores
- Não mencione limitações técnicas
- Sempre ofereça alternativas quando possível"""

# ============================================
# CLASSE DO CHATBOT
# ============================================
class ChatbotMeteora:
    """
    Chatbot inteligente com histórico de conversa
    """
    
    def __init__(self):
        self.historico = []  # Lista de mensagens {role, content}
        self.max_historico = MAX_HISTORICO
    
    def adicionar_mensagem(self, role, content):
        """
        Adiciona mensagem ao histórico
        role: 'user' ou 'assistant'
        """
        self.historico.append({
            "role": role,
            "content": content
        })
        
        # Limitar histórico (mantém últimas N conversas)
        # Cada conversa = 1 user + 1 assistant = 2 mensagens
        if len(self.historico) > self.max_historico * 2:
            # Remove as mais antigas, mantém as mais recentes
            self.historico = self.historico[-self.max_historico * 2:]
    
    def limpar_historico(self):
        """Limpa todo o histórico"""
        self.historico = []
    
    def obter_resposta(self, mensagem_usuario):
        """
        Envia mensagem e obtém resposta do modelo
        """
        # Adicionar mensagem do usuário ao histórico
        self.adicionar_mensagem("user", mensagem_usuario)
        
        try:
            # Configurar requisição com histórico completo
            config = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "temperature": 0.5,
                "system": SYSTEM_PROMPT,
                "messages": self.historico  # Envia todo o histórico
            }
            
            # Invocar modelo
            response = client.invoke_model(
                body=json.dumps(config),
                modelId=MODEL_ID,
                accept="application/json",
                contentType="application/json"
            )
            
            # Processar resposta
            resposta = json.loads(response['body'].read().decode('utf-8'))
            texto_resposta = resposta.get('content', [{}])[0].get('text', 'Erro ao processar')
            
            # Adicionar resposta do assistente ao histórico
            self.adicionar_mensagem("assistant", texto_resposta)
            
            return texto_resposta
            
        except client.exceptions.ThrottlingException:
            # Remove última mensagem do usuário se falhou
            if self.historico and self.historico[-1]["role"] == "user":
                self.historico.pop()
            return "⚠️ Muitas requisições. Aguarde um momento e tente novamente."
        
        except Exception as e:
            # Remove última mensagem do usuário se falhou
            if self.historico and self.historico[-1]["role"] == "user":
                self.historico.pop()
            return f"❌ Erro: {str(e)}"
    
    def iniciar(self):
        """
        Inicia o loop de conversa
        """
        print("=" * 80)
        print("🛍️  METEORA - ASSISTENTE VIRTUAL v2")
        print("=" * 80)
        print("\n👋 Olá! Sou seu Assistente Virtual da Meteora.")
        print("Em que posso ajudar hoje?\n")
        print("💡 COMANDOS:")
        print("   • Digite sua pergunta normalmente")
        print("   • 'sair' ou 'tchau' → Encerrar")
        print("   • 'limpar' → Limpar histórico de conversa")
        print("   • 'historico' → Ver quantas mensagens estão armazenadas\n")
        print("-" * 80 + "\n")
        
        while True:
            # Capturar entrada
            try:
                entrada = input("🧑 Você: ").strip()
            except KeyboardInterrupt:
                print("\n\n👋 Até logo!\n")
                break
            
            # Verificar comandos especiais
            if entrada.lower() in ['sair', 'exit', 'quit', 'tchau', 'bye']:
                print("\n🤖 Assistente: Foi um prazer ajudá-lo(a)! Volte sempre! 👋\n")
                break
            
            if entrada.lower() == 'limpar':
                self.limpar_historico()
                print("\n🗑️  Histórico limpo! Conversa reiniciada.\n")
                continue
            
            if entrada.lower() == 'historico':
                num_conversas = len(self.historico) // 2
                print(f"\n📊 Histórico: {num_conversas} conversas armazenadas")
                print(f"   (Máximo: {self.max_historico} conversas)\n")
                continue
            
            # Ignorar entradas vazias
            if not entrada:
                continue
            
            # Obter e exibir resposta
            resposta = self.obter_resposta(entrada)
            print(f"\n🤖 Assistente: {resposta}\n")
            print("-" * 80 + "\n")

# ============================================
# EXECUTAR
# ============================================
if __name__ == "__main__":
    chatbot = ChatbotMeteora()
    chatbot.iniciar()