import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()

print("=" * 80)
print("🔍 DIAGNÓSTICO COMPLETO DO BANCO")
print("=" * 80)

# 1. Ver TODOS os produtos RAW
cursor.execute("SELECT * FROM roupas")
todos = cursor.fetchall()

print(f"\n📦 Total de produtos: {len(todos)}\n")

for i, p in enumerate(todos, 1):
    print(f"Produto {i}:")
    print(f"  ID: {p[0]}")
    print(f"  Campo 1 (nome): '{p[1]}' (tipo: {type(p[1])})")
    print(f"  Campo 2 (preço): '{p[2]}' (tipo: {type(p[2])})")
    print(f"  Campo 3 (qtd): '{p[3]}' (tipo: {type(p[3])})")
    if len(p) > 4:
        print(f"  Campo 4 (desc): '{p[4][:50]}...' (tipo: {type(p[4])})")
    print()

# 2. Testar qual campo TEM "Óculos"
print("=" * 80)
print("🔍 PROCURANDO 'Óculos' EM CADA CAMPO")
print("=" * 80)

cursor.execute("SELECT * FROM roupas")
for p in cursor.fetchall():
    for idx, campo in enumerate(p):
        if 'óculos' in str(campo).lower() or 'oculos' in str(campo).lower():
            print(f"✅ ENCONTRADO no campo {idx}: '{campo}'")
            print(f"   Produto completo: {p}")

conn.close()
exit()