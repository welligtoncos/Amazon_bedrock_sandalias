import boto3
import json
import numpy as np
from unidecode import unidecode
from config.settings import AWS_REGION, BEDROCK_EMBEDDING_MODEL


class Embeddings:
    """Gera embeddings usando Amazon Bedrock (Titan / Claude / Llama)."""

    def __init__(self):
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
        )

    # -----------------------------
    # NORMALIZAÇÃO ROBUSTA
    # -----------------------------
    def _normalize(self, text: str) -> str:
        return unidecode(text.lower().strip())

    # -----------------------------
    # PUXAR EMBEDDING DO BEDROCK
    # -----------------------------
    def embed(self, text: str):
        """
        Gera embedding robusto para o pipeline RAG.
        Retorna SEMPRE vetor float32.
        """

        if not isinstance(text, str):
            raise ValueError("Texto para embedding deve ser uma string.")

        text = self._normalize(text)

        if len(text) == 0:
            return np.zeros(1024, dtype=np.float32)

        payload = {"inputText": text}

        try:
            response = self.client.invoke_model(
                modelId=BEDROCK_EMBEDDING_MODEL,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload).encode("utf-8")
            )

            data = json.loads(response["body"].read())

            # --------------------------------------------
            # 1️⃣ Titan Embeddings v2 — formato atual
            # --------------------------------------------
            if "embedding" in data:
                return np.array(data["embedding"], dtype=np.float32)

            # --------------------------------------------
            # 2️⃣ Titan Embeddings v1 — formato antigo
            # { "output": { "embedding": [...] } }
            # --------------------------------------------
            if "output" in data and isinstance(data["output"], dict):
                if "embedding" in data["output"]:
                    return np.array(data["output"]["embedding"], dtype=np.float32)

            # --------------------------------------------
            # 3️⃣ Formatos alternativos (Claude, Llama)
            # --------------------------------------------
            if "embeddings" in data:
                return np.array(data["embeddings"], dtype=np.float32)

            if "vectors" in data:
                return np.array(data["vectors"], dtype=np.float32)

            # --------------------------------------------
            # FALLOUT: nenhum formato reconhecido
            # --------------------------------------------
            raise RuntimeError(
                f"❌ Formato inesperado para o modelo {BEDROCK_EMBEDDING_MODEL} → {data}"
            )

        # -----------------------------
        # ERROS CONTROLADOS
        # -----------------------------
        except self.client.exceptions.ValidationException as e:
            raise RuntimeError(f"❌ Erro de validação no Bedrock: {e}")

        except self.client.exceptions.ThrottlingException:
            raise RuntimeError(
                "❌ Serviço de Embeddings está sofrendo throttling. "
                "Reduza a taxa de requisições ou aguarde alguns segundos."
            )

        # -----------------------------
        # ERRO DESCONHECIDO
        # -----------------------------
        except Exception as e:
            raise RuntimeError(f"❌ Erro inesperado ao gerar embedding: {e}")
