import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

# Buscar sandália (igual ao código faz)
cursor.execute("SELECT * FROM roupas WHERE nome LIKE ?", ('%sandália%',))
resultado = cursor.fetchall()

print("=" * 80)
print("🔍 BUSCA POR 'SANDÁLIA':")
print("=" * 80)

if resultado:
    print(f"✅ Encontrados {len(resultado)} produto(s):\n")
    for p in resultado:
        print(f"ID: {p[0]}")
        print(f"Nome: {p[1]}")
        print(f"Campo 2 (deveria ser preço): {p[2]}")
        print(f"Campo 3 (deveria ser qtd): {p[3]}")
        if len(p) > 4:
            print(f"Campo 4 (descrição): {p[4]}")
        print("-" * 80)
else:
    print("❌ NENHUM produto com 'sandália' encontrado!")

# Ver estrutura da tabela
print("\n📊 ESTRUTURA DA TABELA:")
cursor.execute("PRAGMA table_info(roupas)")
colunas = cursor.fetchall()
for col in colunas:
    print(f"  {col[1]} ({col[2]})")

conn.close()
exit()