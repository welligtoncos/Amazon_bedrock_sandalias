import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage
from config.settings import *


class ResponseGenerator:
    """Gerador de respostas 100% alinhado ao contexto RAG."""

    def __init__(self):
        self.client = boto3.client(
            service_name="bedrock-runtime",
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

        # histórico curto
        self.historico = []

    # -------------------------------------------
    # VALIDAÇÃO DE CONTEXTO
    # -------------------------------------------
    def _contexto_invalido(self, contexto: str):
        if not contexto:
            return True

        ctx = contexto.strip().lower()

        # casos claros de vazio
        if ctx == "" or ctx.startswith("nenhum produto") or len(ctx) < 10:
            return True

        # se não contém pelo menos 1 produto formatado
        if "id:" not in ctx and "nome:" not in ctx:
            return True

        return False

    # -------------------------------------------
    # GERAÇÃO PRINCIPAL
    # -------------------------------------------
    def generate(self, query, context):

        # se contexto não tem produto → retorno automático
        if self._contexto_invalido(context):
            return "Nenhum produto encontrado. Me diga outra característica ou categoria para buscar novamente."

        # prompt estruturado
        system_prompt = f"""
Você é um assistente de compras que responde *exclusivamente* com base nos produtos fornecidos.

REGRAS:
1. Não invente produtos, marcas, tamanhos, cores ou preços.
2. Não use conhecimento externo.
3. Só responda usando o catálogo abaixo.
4. Se a pergunta pedir algo que não está no catálogo, responda:
   → "Não encontrei esse item no catálogo."
5. Responda sempre de forma curta, objetiva e clara.
6. Nunca liste itens fora do catálogo.

CATÁLOGO DISPONÍVEL:

{context}
"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]

        resposta = self.model.invoke(messages).content.strip()

        # salvar histórico curto
        self.historico = [
            {"role": "user", "content": query},
            {"role": "assistant", "content": resposta}
        ]

        return resposta
