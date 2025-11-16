import sqlite3
import os

# Caminho completo do banco
DB_PATH = r'C:\rsm_projects-inteligencia-artificial\Amazon_bedrock_sandalias\chatbot_rag_aula\produtos.db'

# Apagar banco antigo se existir
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print("🗑️  Banco antigo removido")

# Criar novo banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
CREATE TABLE roupas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL,
    descricao TEXT
)
''')

# Produtos corretos
produtos = [
    ('Sandália de Praia', 45.90, 25, 'Sandália confortável com tiras reguláveis, sola de borracha antiderrapante.'),
    ('Óculos de Sol', 89.90, 15, 'Óculos com proteção UV400, armação leve e resistente.'),
    ('Moletom de Lã Cinza', 129.90, 10, 'Moletom quentinho de lã, capuz e bolso frontal.'),
    ('Cachecol de Tricô', 49.90, 20, 'Cachecol macio de tricô, várias cores disponíveis.'),
    ('Vestido de Verão', 119.90, 12, 'Vestido leve e fresco com estampa floral.'),
    ('Bermuda Cargo', 79.90, 18, 'Bermuda cargo com vários bolsos, tecido resistente.'),
    ('Camiseta Branca', 39.90, 50, 'Camiseta 100% algodão, gola redonda.'),
    ('Jaqueta Jeans', 159.90, 8, 'Jaqueta jeans clássica, lavagem escura.'),
    ('Sandália Rasteira Feminina', 59.90, 30, 'Sandália rasteira elegante, ideal para o verão.'),
    ('Sandália Esportiva', 89.90, 20, 'Sandália esportiva com velcro, confortável para caminhadas.'),
]

cursor.executemany('''
INSERT INTO roupas (nome, preco, quantidade, descricao) 
VALUES (?, ?, ?, ?)
''', produtos)

conn.commit()

# VERIFICAR
print("\n" + "=" * 80)
print(f"✅ BANCO RECRIADO EM: {DB_PATH}")
print("=" * 80)

cursor.execute("SELECT * FROM roupas")
for p in cursor.fetchall():
    print(f"✅ ID {p[0]:2} | {p[1]:30} | R$ {p[2]:6.2f} | {p[3]:3} un.")

# TESTAR BUSCA POR SANDÁLIA
print("\n" + "=" * 80)
print("🧪 TESTE DE BUSCA POR 'SANDÁLIA'")
print("=" * 80)

cursor.execute("SELECT * FROM roupas WHERE nome LIKE '%sandália%' OR nome LIKE '%sandalia%'")
resultado = cursor.fetchall()

if resultado:
    print(f"✅ ENCONTRADO {len(resultado)} produto(s):")
    for p in resultado:
        print(f"   → {p[1]} - R${p[2]}")
else:
    print("❌ NÃO ENCONTRADO!")

# TESTAR BUSCA POR ÓCULOS
print("\n" + "=" * 80)
print("🧪 TESTE DE BUSCA POR 'ÓCULOS'")
print("=" * 80)

cursor.execute("SELECT * FROM roupas WHERE nome LIKE '%óculos%' OR nome LIKE '%oculos%'")
resultado2 = cursor.fetchall()

if resultado2:
    print(f"✅ ENCONTRADO {len(resultado2)} produto(s):")
    for p in resultado2:
        print(f"   → {p[1]} - R${p[2]}")
else:
    print("❌ NÃO ENCONTRADO!")

# TESTAR BUSCA CASE-INSENSITIVE
print("\n" + "=" * 80)
print("🧪 TESTE CASE-INSENSITIVE (moletom)")
print("=" * 80)

cursor.execute("SELECT * FROM roupas WHERE LOWER(nome) LIKE LOWER(?)", ('%moletom%',))
resultado3 = cursor.fetchall()

if resultado3:
    print(f"✅ ENCONTRADO {len(resultado3)} produto(s):")
    for p in resultado3:
        print(f"   → {p[1]} - R${p[2]}")
else:
    print("❌ NÃO ENCONTRADO!")

conn.close()

print("\n" + "=" * 80)
print("✅ BANCO PRONTO PARA USO!")
print(f"📁 Local: {DB_PATH}")
print("=" * 80)