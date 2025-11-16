import os
import re
import pickle
import numpy as np
from unidecode import unidecode
from rag.embeddings import Embeddings


class ProductRetriever:
    """RAG PURA — comparação vetorial com TODO o catálogo (SEM SQL)"""

    def __init__(self,
                 vectors_path="db_data/vectors.pkl",
                 catalog_path="db_data/catalogo.pkl"):

        self.embedding = Embeddings()

        # -----------------------------
        # 1. Validar existência dos arquivos
        # -----------------------------
        if not os.path.exists(vectors_path):
            raise FileNotFoundError(
                f"❌ Arquivo {vectors_path} não encontrado. "
                f"Execute primeiro: python popular_embeddings.py"
            )

        if not os.path.exists(catalog_path):
            raise FileNotFoundError(
                f"❌ Arquivo {catalog_path} não encontrado. "
                f"Crie ou exporte o catálogo antes de usar o RAG."
            )

        # -----------------------------
        # 2. Carregar vetores
        # -----------------------------
        with open(vectors_path, "rb") as f:
            data = pickle.load(f)

        self.product_ids = data["ids"]
        self.product_vectors = np.array(data["vectors"], dtype=np.float32)

        # -----------------------------
        # 3. Carregar catálogo original
        # -----------------------------
        with open(catalog_path, "rb") as f:
            self.catalogo = pickle.load(f)

        if len(self.catalogo) == 0:
            print("⚠️ Aviso: catálogo carregado, mas está vazio!")

    # --------------------------
    # NORMALIZAÇÃO DA CONSULTA
    # --------------------------
    def _normalize(self, text: str):
        text = text.lower().strip()
        text = unidecode(text)
        text = re.sub(r"[^a-z0-9 ]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # --------------------------
    # SIMILARIDADE
    # --------------------------
    def _cosine_similarity(self, q, M):
        """similaridade protegida"""
        q_norm = np.linalg.norm(q)
        if q_norm == 0:
            return np.zeros(M.shape[0])

        q = q / q_norm
        M_norm = np.linalg.norm(M, axis=1, keepdims=True)
        M_norm[M_norm == 0] = 1e-8  # evita divisão por zero

        M = M / M_norm
        return np.dot(M, q)

    # --------------------------
    # BUSCA PRINCIPAL
    # --------------------------
    def retrieve(self, query, limit=5):
        """
        RAG PURA — busca vetorial completa SEM SQL.
        """

        # 1️⃣ normalizar consulta
        query_norm = self._normalize(query)

        # 2️⃣ gerar embedding
        query_vector = np.array(self.embedding.embed(query_norm), dtype=np.float32)

        # 3️⃣ calcular similaridade
        scores = self._cosine_similarity(query_vector, self.product_vectors)

        # 4️⃣ selecionar top-N
        top_idx = np.argsort(scores)[::-1][:limit]

        resultados = []
        for idx in top_idx:
            prod_id = self.product_ids[idx]

            if prod_id not in self.catalogo:
                continue  # failsafe

            produto = dict(self.catalogo.get(prod_id))
            produto["score"] = float(scores[idx])

            resultados.append(produto)

        return resultados
