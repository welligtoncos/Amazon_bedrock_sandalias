import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import *

class ResponseGenerator:
    """Gerador de respostas (GENERATION)"""
    
    def __init__(self):
        self.client = boto3.client(
            service_name='bedrock-runtime',
            region_name=AWS_REGION
        )
        
        self.model = ChatBedrock(
            model_id=BEDROCK_MODEL_ID,
            client=self.client,
            model_kwargs={
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
                "top_p": TOP_P
            }
        )
        
        self.historico = []
    
    def generate(self, query, context):
        """
        Gera resposta usando Claude
        
        Args:
            query: Pergunta do usuário
            context: Contexto com produtos
        
        Returns:
            Resposta gerada
        """
        system_prompt = f"""Você é um assistente virtual especializado em vendas de produtos de moda e acessórios.

INSTRUÇÕES:
- Seja amigável, prestativo e profissional
- Use APENAS as informações dos produtos fornecidos abaixo
- Destaque promoções e vantagens dos produtos
- Seja objetivo mas completo
- Se não houver produtos, sugira alternativas ou refinamento da busca
- Responda APENAS sobre produtos de moda (roupas, calçados, acessórios)
- Faça recomendações baseadas nas necessidades do cliente

CATÁLOGO DISPONÍVEL:
{context}

HISTÓRICO DA CONVERSA:
{self._get_historico()}
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = self.model.invoke(messages)
        response_text = response.content
        
        # Salvar no histórico
        self.historico.append(f"Cliente: {query}")
        self.historico.append(f"Assistente: {response_text}")
        
        # Manter apenas últimas interações
        if len(self.historico) > HISTORICO_MAX:
            self.historico = self.historico[-HISTORICO_MAX:]
        
        return response_text
    
    def _get_historico(self):
        """Retorna histórico formatado"""
        return "\n".join(self.historico[-6:]) if self.historico else "Primeira interação"