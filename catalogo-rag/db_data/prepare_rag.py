import os, sys
import sqlite3
import pickle
import numpy as np
import json
from unidecode import unidecode

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from config.settings import DB_PATH, BEDROCK_EMBEDDING_MODEL, AWS_REGION
from rag.embeddings import Embeddings

CATALOGO_PKL = os.path.join("db_data", "catalogo.pkl")
VECTORS_PKL  = os.path.join("db_data", "vectors.pkl")

os.makedirs("db_data", exist_ok=True)


# ---------------------------------------------------------
# 1. CRIAR BANCO + TABELA MINIMAL
# ---------------------------------------------------------
def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DROP TABLE IF EXISTS produtos;
    """)

    cursor.execute("""
    CREATE TABLE produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        descricao TEXT,
        preco REAL NOT NULL
    );
    """)

    produtos = [
        ("Sandália Feminina Conforto", "Calçados", "Sandália preta confortável", 79.90),
        ("Sandália Rasteira Dourada", "Calçados", "Rasteira leve e macia", 59.90),
        ("Sandália Festa Salto Alto", "Calçados", "Ideal para festas e eventos", 129.90),
        ("Tênis Corrida Pro Run", "Calçados", "Tênis leve para corrida", 199.90),
        ("Camiseta Básica Algodão", "Roupas", "Camiseta 100% algodão branca", 39.90),
    ]

    cursor.executemany("""
        INSERT INTO produtos (nome, categoria, descricao, preco)
        VALUES (?, ?, ?, ?)
    """, produtos)

    conn.commit()
    conn.close()
    print("✅ Banco criado com tabela simples e produtos inseridos.")


# ---------------------------------------------------------
# 2. EXPORTAR PARA catalogo.pkl
# ---------------------------------------------------------
def exportar_catalogo():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()

    catalogo = {row["id"]: dict(row) for row in rows}

    conn.close()

    with open(CATALOGO_PKL, "wb") as f:
        pickle.dump(catalogo, f)

    print(f"📦 Catálogo exportado → {CATALOGO_PKL}")


# ---------------------------------------------------------
# 3. GERAR EMBEDDINGS Titan → vectors.pkl
# ---------------------------------------------------------
def gerar_embeddings():
    with open(CATALOGO_PKL, "rb") as f:
        catalogo = pickle.load(f)

    emb = Embeddings()

    ids = []
    vectors = []

    print("\n🧠 Gerando embeddings Titan...\n")

    for pid, produto in catalogo.items():
        texto = f"{produto['nome']}. {produto['descricao']}. Categoria: {produto['categoria']}"
        vetor = emb.embed(unidecode(texto.lower()))

        ids.append(pid)
        vectors.append(vetor)

        print(f"✔ Vetor gerado para ID={pid}")

    with open(VECTORS_PKL, "wb") as f:
        pickle.dump({"ids": ids, "vectors": np.array(vectors)}, f)

    print(f"\n🧠 Embeddings salvos em {VECTORS_PKL}")


if __name__ == "__main__":
    print("\n=== PREPARANDO AMBIENTE RAG COMPLETO ===\n")

    criar_banco()
    exportar_catalogo()
    gerar_embeddings()

    print("\n🎉 AMBIENTE RAG PRONTO! Execute: python app.py\n")
