import sqlite3

conn = sqlite3.connect('produtos.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS roupas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    preco REAL,
    estoque INTEGER
)
''')

produtos = [
    ("Camiseta Básica", "Camiseta 100% algodão, várias cores disponíveis", 29.99, 150),
    ("Calça Jeans", "Calça jeans azul, modelagem reta", 89.90, 75),
    ("Vestido Floral", "Vestido com estampa floral, tecido leve", 149.90, 30),
    ("Blusa de Moletom", "Blusa de moletom com capuz, unissex", 119.99, 50),
    ("Jaqueta de Couro", "Jaqueta de couro sintético, preta", 299.99, 20),
    ("Camiseta de Algodão", "Camiseta confortável de algodão, várias cores", 25.00, 100),
    ("Calça Legging", "Calça legging preta, ideal para exercícios", 69.90, 40),
    ("Saia Plissada", "Saia plissada com estampa floral", 89.90, 60),
    ("Camisa Social", "Camisa social branca, tecido leve e confortável", 79.99, 45),
    ("Blazer Masculino", "Blazer azul escuro, ideal para eventos formais", 199.99, 25),
    ("Shorts de Verão", "Shorts de verão em algodão, várias cores", 49.90, 80),
    ("Sapatênis Casual", "Sapatênis casual em couro, disponível em várias cores", 129.90, 35),
    ("Tênis Esportivo", "Tênis esportivo com tecnologia de absorção de impacto", 149.90, 60),
    ("Bolsa de Couro", "Bolsa de couro legítimo, preta", 299.90, 15),
    ("Relógio de Pulso", "Relógio de pulso com mostrador analógico", 199.90, 10),
    ("Óculos de Sol", "Óculos de sol com proteção UV, estilo moderno", 89.90, 25),
    ("Casaco de Lã", "Casaco de lã, ideal para clima frio", 239.90, 20),
    ("Cachecol de Tricô", "Cachecol de tricô em várias cores", 39.90, 50),
    ("Luvas de Couro", "Luvas de couro, várias tamanhos disponíveis", 69.90, 30),
    ("Bermuda Cargo", "Bermuda cargo com múltiplos bolsos", 89.90, 70),
    ("Mochila Escolar", "Mochila escolar com vários compartimentos", 119.90, 40)
]

cursor.executemany('''
INSERT INTO roupas (nome, descricao, preco, estoque) 
VALUES (?, ?, ?, ?)
''', produtos)

conn.commit()
conn.close()

print("Banco de dados criado e populado com sucesso!")