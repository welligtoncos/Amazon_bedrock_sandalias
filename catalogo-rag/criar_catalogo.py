import sqlite3
import os

def criar_banco_catalogo():
    """Cria banco de dados com catálogo de produtos"""
    
    # Criar diretório se não existir
    os.makedirs('data', exist_ok=True)
    
    # Conectar ao banco
    conn = sqlite3.connect('data/catalogo.db')
    cursor = conn.cursor()
    
    # Criar tabela de produtos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        subcategoria TEXT,
        preco REAL NOT NULL,
        preco_promocional REAL,
        marca TEXT,
        cor TEXT,
        tamanho TEXT,
        material TEXT,
        estoque INTEGER NOT NULL,
        descricao TEXT,
        especificacoes TEXT,
        avaliacao REAL,
        num_avaliacoes INTEGER,
        peso REAL,
        dimensoes TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Criar índices para busca rápida
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_nome ON produtos(nome)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_categoria ON produtos(categoria)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_preco ON produtos(preco)')
    
    # Dados de exemplo - Catálogo de Moda
    produtos = [
        # Calçados
        ('Sandália Havaianas Slim', 'Calçados', 'Sandálias', 29.90, 24.90, 'Havaianas', 'Preta', '37/38', 
         'Borracha', 150, 'Sandália confortável e durável, perfeita para o dia a dia',
         'Sola antiderrapante, tiras finas, palmilha anatômica', 4.7, 2341, 0.15, '24x7x2cm'),
        
        ('Tênis Nike Air Max', 'Calçados', 'Tênis', 499.90, 449.90, 'Nike', 'Branco/Preto', '40', 
         'Tecido/Borracha', 45, 'Tênis esportivo com tecnologia Air Max para máximo conforto',
         'Amortecimento Air, cabedal respirável, sola de borracha', 4.8, 1523, 0.85, '30x20x12cm'),
        
        ('Sapato Social Masculino', 'Calçados', 'Sapatos', 159.90, None, 'Di Pollini', 'Marrom', '42', 
         'Couro', 30, 'Sapato social elegante em couro legítimo',
         'Couro bovino, forro têxtil, solado de borracha', 4.5, 876, 0.95, '29x10x8cm'),
        
        ('Bota Feminina Cano Alto', 'Calçados', 'Botas', 189.90, 169.90, 'Vizzano', 'Preta', '37', 
         'Sintético', 25, 'Bota estilosa com salto médio e cano alto',
         'Salto 7cm, zíper lateral, forro macio', 4.6, 654, 1.1, '28x35x10cm'),
        
        # Roupas
        ('Camiseta Básica Algodão', 'Roupas', 'Camisetas', 39.90, 29.90, 'Hering', 'Branca', 'M', 
         'Algodão', 200, 'Camiseta básica 100% algodão, confortável e versátil',
         '100% algodão penteado, gola redonda, manga curta', 4.4, 3210, 0.18, 'Dobrado: 20x25x3cm'),
        
        ('Calça Jeans Skinny', 'Roupas', 'Calças', 129.90, 99.90, 'Levi\'s', 'Azul', '40', 
         'Jeans/Elastano', 80, 'Calça jeans skinny com elastano para melhor ajuste',
         '98% algodão, 2% elastano, cintura média, 5 bolsos', 4.7, 1876, 0.55, 'Dobrado: 25x30x8cm'),
        
        ('Vestido Floral Verão', 'Roupas', 'Vestidos', 89.90, 79.90, 'Farm', 'Estampado', 'P', 
         'Viscose', 60, 'Vestido leve e fresco com estampa floral',
         'Viscose, alças reguláveis, forro interno', 4.8, 923, 0.25, 'Dobrado: 22x28x4cm'),
        
        ('Jaqueta Jeans Oversized', 'Roupas', 'Jaquetas', 169.90, 149.90, 'Zara', 'Azul Claro', 'M', 
         'Jeans', 40, 'Jaqueta jeans oversized, estilo moderno e descontraído',
         '100% algodão, bolsos frontais, botões metálicos', 4.6, 567, 0.75, 'Dobrado: 30x35x10cm'),
        
        # Acessórios
        ('Óculos de Sol Ray-Ban', 'Acessórios', 'Óculos', 399.90, 349.90, 'Ray-Ban', 'Preto', 'Único', 
         'Acetato/Metal', 35, 'Óculos de sol clássico com proteção UV400',
         'Proteção UV400, lentes polarizadas, estojo incluso', 4.9, 2134, 0.08, '15x5x15cm (com estojo)'),
        
        ('Bolsa Transversal Couro', 'Acessórios', 'Bolsas', 189.90, 169.90, 'Arezzo', 'Caramelo', 'Único', 
         'Couro', 45, 'Bolsa transversal em couro legítimo',
         'Couro bovino, alça regulável, bolsos internos', 4.7, 1234, 0.45, '25x18x8cm'),
        
        ('Relógio Digital Esportivo', 'Acessórios', 'Relógios', 149.90, 129.90, 'Casio', 'Preto', 'Único', 
         'Resina', 70, 'Relógio digital com múltiplas funções',
         'À prova d\'água 50m, cronômetro, alarme, luz LED', 4.6, 1543, 0.05, '5x5x1.5cm'),
        
        ('Cinto Couro Masculino', 'Acessórios', 'Cintos', 79.90, 69.90, 'Dumond', 'Marrom', '42', 
         'Couro', 90, 'Cinto clássico em couro com fivela metálica',
         'Couro bovino, fivela níquel, largura 3.5cm', 4.5, 876, 0.22, '120x4x0.3cm'),
        
        # Roupas Íntimas
        ('Kit 3 Cuecas Boxer', 'Roupas', 'Íntimas', 59.90, 49.90, 'Lupo', 'Sortidas', 'G', 
         'Algodão/Elastano', 120, 'Kit com 3 cuecas boxer confortáveis',
         '95% algodão, 5% elastano, elástico emborrachado', 4.6, 2341, 0.15, '20x15x5cm'),
        
        ('Sutiã Push-up Renda', 'Roupas', 'Íntimas', 69.90, 59.90, 'Hope', 'Preto', '42', 
         'Microfibra/Renda', 75, 'Sutiã com bojo e renda delicada',
         'Bojo removível, alças ajustáveis, renda importada', 4.7, 1654, 0.08, '15x20x10cm'),
        
        # Esportivos
        ('Legging Fitness Suplex', 'Roupas', 'Fitness', 79.90, 69.90, 'Live!', 'Preta', 'M', 
         'Suplex', 95, 'Legging de alta compressão para treinos',
         'Tecido suplex, cintura alta, secagem rápida', 4.8, 1987, 0.22, 'Dobrado: 20x25x4cm'),
        
        ('Shorts Running Masculino', 'Roupas', 'Fitness', 59.90, 49.90, 'Adidas', 'Azul', 'M', 
         'Poliéster', 110, 'Shorts leve para corrida com tecnologia Climalite',
         'Tecnologia Climalite, bolso com zíper, elástico na cintura', 4.5, 1234, 0.12, 'Dobrado: 18x22x3cm'),
    ]
    
    cursor.executemany('''
        INSERT INTO produtos (
            nome, categoria, subcategoria, preco, preco_promocional,
            marca, cor, tamanho, material, estoque, descricao,
            especificacoes, avaliacao, num_avaliacoes, peso, dimensoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', produtos)
    
    conn.commit()
    
    # Verificar
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]
    
    print("=" * 60)
    print("✅ BANCO DE DADOS CRIADO COM SUCESSO!")
    print("=" * 60)
    print(f"📦 Total de produtos: {total}")
    print(f"📁 Localização: {os.path.abspath('data/catalogo.db')}")
    print("=" * 60)
    
    # Mostrar algumas estatísticas
    cursor.execute("SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria")
    print("\n📊 Produtos por categoria:")
    for cat, count in cursor.fetchall():
        print(f"   • {cat}: {count} produtos")
    
    conn.close()

if __name__ == "__main__":
    criar_banco_catalogo()