import boto3
import json
from datetime import datetime

# ============================================
# CONFIGURAÇÕES
# ============================================
client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-2'
)

MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
MAX_HISTORICO = 10

# Preços (por 1M tokens)
PRECO_INPUT = 0.80
PRECO_OUTPUT = 4.00

SYSTEM_PROMPT = """Você é um assistente virtual da Meteora, um e-commerce de moda e vestuário.

DIRETRIZES:
- Seja conciso: máximo 300 caracteres por resposta
- Foque em produtos de moda: roupas, calçados, acessórios
- Mantenha tom profissional e amigável
- Use o contexto das mensagens anteriores
- Sempre ofereça alternativas quando possível"""

# ============================================
# CLASSE DO CHATBOT AVANÇADO
# ============================================
class ChatbotMeteora:
    """
    Chatbot com histórico, estatísticas e controle de custos
    """
    
    def __init__(self):
        self.historico = []
        self.max_historico = MAX_HISTORICO
        
        # Estatísticas
        self.total_requisicoes = 0
        self.total_tokens_input = 0
        self.total_tokens_output = 0
        self.total_custo = 0.0
        self.inicio_sessao = datetime.now()
    
    def adicionar_mensagem(self, role, content):
        """Adiciona mensagem ao histórico"""
        self.historico.append({"role": role, "content": content})
        
        if len(self.historico) > self.max_historico * 2:
            self.historico = self.historico[-self.max_historico * 2:]
    
    def limpar_historico(self):
        """Limpa histórico"""
        self.historico = []
    
    def calcular_custo(self, tokens_in, tokens_out):
        """Calcula custo da requisição"""
        custo_in = (tokens_in / 1_000_000) * PRECO_INPUT
        custo_out = (tokens_out / 1_000_000) * PRECO_OUTPUT
        return custo_in + custo_out
    
    def mostrar_estatisticas(self):
        """Exibe estatísticas da sessão"""
        duracao = (datetime.now() - self.inicio_sessao).total_seconds()
        minutos = int(duracao // 60)
        segundos = int(duracao % 60)
        
        print("\n" + "=" * 80)
        print("📊 ESTATÍSTICAS DA SESSÃO")
        print("=" * 80)
        print(f"⏱️  Duração: {minutos}min {segundos}s")
        print(f"💬 Total de perguntas: {self.total_requisicoes}")
        print(f"📥 Tokens de entrada: {self.total_tokens_input:,}")
        print(f"📤 Tokens de saída: {self.total_tokens_output:,}")
        print(f"💰 Custo total: ${self.total_custo:.6f} (≈ R$ {self.total_custo * 5.5:.4f})")
        
        if self.total_requisicoes > 0:
            custo_medio = self.total_custo / self.total_requisicoes
            print(f"📊 Custo médio/pergunta: ${custo_medio:.6f}")
        
        print("=" * 80 + "\n")
    
    def obter_resposta(self, mensagem_usuario):
        """Envia mensagem e obtém resposta"""
        self.adicionar_mensagem("user", mensagem_usuario)
        
        try:
            config = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "temperature": 0.5,
                "system": SYSTEM_PROMPT,
                "messages": self.historico
            }
            
            response = client.invoke_model(
                body=json.dumps(config),
                modelId=MODEL_ID,
                accept="application/json",
                contentType="application/json"
            )
            
            resposta = json.loads(response['body'].read().decode('utf-8'))
            texto = resposta.get('content', [{}])[0].get('text', 'Erro')
            usage = resposta.get('usage', {})
            
            # Atualizar estatísticas
            tokens_in = usage.get('input_tokens', 0)
            tokens_out = usage.get('output_tokens', 0)
            custo = self.calcular_custo(tokens_in, tokens_out)
            
            self.total_requisicoes += 1
            self.total_tokens_input += tokens_in
            self.total_tokens_output += tokens_out
            self.total_custo += custo
            
            self.adicionar_mensagem("assistant", texto)
            
            return {
                'texto': texto,
                'tokens_in': tokens_in,
                'tokens_out': tokens_out,
                'custo': custo
            }
            
        except client.exceptions.ThrottlingException:
            if self.historico and self.historico[-1]["role"] == "user":
                self.historico.pop()
            return {'texto': "⚠️ Muitas requisições. Aguarde um momento.", 'erro': True}
        
        except Exception as e:
            if self.historico and self.historico[-1]["role"] == "user":
                self.historico.pop()
            return {'texto': f"❌ Erro: {str(e)}", 'erro': True}
    
    def iniciar(self):
        """Inicia o chatbot"""
        print("=" * 80)
        print("🛍️  METEORA - ASSISTENTE VIRTUAL v3 (Avançado)")
        print("=" * 80)
        print("\n👋 Olá! Sou seu Assistente Virtual da Meteora.")
        print("Em que posso ajudar hoje?\n")
        print("💡 COMANDOS:")
        print("   • Digite sua pergunta normalmente")
        print("   • 'sair' → Encerrar e ver estatísticas")
        print("   • 'limpar' → Limpar histórico")
        print("   • 'stats' → Ver estatísticas parciais")
        print("   • 'historico' → Ver mensagens armazenadas\n")
        print("-" * 80 + "\n")
        
        while True:
            try:
                entrada = input("🧑 Você: ").strip()
            except KeyboardInterrupt:
                print("\n")
                self.mostrar_estatisticas()
                print("👋 Até logo!\n")
                break
            
            if entrada.lower() in ['sair', 'exit', 'quit', 'tchau']:
                print("\n🤖 Assistente: Foi um prazer ajudá-lo(a)! Até logo! 👋")
                self.mostrar_estatisticas()
                break
            
            if entrada.lower() == 'limpar':
                self.limpar_historico()
                print("\n🗑️  Histórico limpo!\n")
                continue
            
            if entrada.lower() == 'stats':
                self.mostrar_estatisticas()
                continue
            
            if entrada.lower() == 'historico':
                num_conversas = len(self.historico) // 2
                print(f"\n📊 {num_conversas}/{self.max_historico} conversas no histórico\n")
                continue
            
            if not entrada:
                continue
            
            # Obter resposta
            resultado = self.obter_resposta(entrada)
            
            if 'erro' in resultado:
                print(f"\n{resultado['texto']}\n")
            else:
                print(f"\n🤖 Assistente: {resultado['texto']}")
                print(f"   💰 ${resultado['custo']:.6f} | 📊 {resultado['tokens_out']} tokens\n")
            
            print("-" * 80 + "\n")

# ============================================
# EXECUTAR
# ============================================
if __name__ == "__main__":
    chatbot = ChatbotMeteora()
    chatbot.iniciar()