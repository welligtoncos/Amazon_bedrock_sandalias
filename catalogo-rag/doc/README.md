# 📊 MODELAGEM FÍSICA - SISTEMA RAG CATÁLOGO DE PRODUTOS

## 📁 Documentação Completa Gerada

Este pacote contém a documentação completa da modelagem física do banco de dados do Sistema RAG de Catálogo de Produtos.

---

## 📚 Arquivos Inclusos

### 1️⃣ **diagrama_erd.mermaid**
📊 Diagrama Entidade-Relacionamento em formato Mermaid
- Visualização gráfica da estrutura do banco
- Pode ser renderizado no GitHub, VS Code, ou mermaid.live
- Mostra campos, tipos, constraints e relacionamentos

### 2️⃣ **modelagem_fisica.sql**
💾 Script SQL Completo (DDL)
- Comandos CREATE TABLE com todas as especificações
- Definição de índices otimizados
- Constraints e validações
- Triggers de integridade
- Views auxiliares para relatórios
- Queries de exemplo comentadas

### 3️⃣ **documentacao_modelagem_fisica.md**
📖 Documentação Detalhada em Markdown
- Descrição completa de cada campo
- Regras de negócio explicadas
- Integração com sistema RAG
- Exemplos de uso
- Estatísticas do catálogo
- Guias de performance e manutenção

### 4️⃣ **dicionario_dados.md**
📋 Dicionário de Dados Completo
- Tabela detalhada de todos os campos
- Domínios e valores válidos
- Mapeamento com classes Python
- Histórico de alterações
- Queries de exemplo por categoria

### 5️⃣ **estrutura_visual.txt**
🎨 Visualização ASCII da Estrutura
- Diagrama visual em texto puro
- Exemplo de registro completo
- Árvore de categorias
- Estatísticas atuais
- Fácil visualização em qualquer editor

---

## 🎯 Resumo da Estrutura

### Banco de Dados
- **SGBD:** SQLite 3
- **Codificação:** UTF-8
- **Total de Tabelas:** 1 (produtos)
- **Total de Registros:** 32 produtos
- **Total de Índices:** 3 (nome, categoria, preço)

### Tabela Principal: `produtos`
```
📦 produtos
├─ 18 campos
├─ 3 índices otimizados
├─ 2 triggers de validação
├─ 3 views auxiliares
└─ Integrada com sistema RAG
```

---

## 🔑 Campos Principais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **id** | INTEGER | Chave primária (auto-incremento) |
| **nome** | TEXT | Nome do produto |
| **categoria** | TEXT | Categoria principal |
| **preco** | REAL | Preço de venda (R$) |
| **preco_promocional** | REAL | Preço em promoção |
| **estoque** | INTEGER | Quantidade disponível |
| **avaliacao** | REAL | Nota de 0.0 a 5.0 |

---

## 🔍 Índices Criados

1. **idx_nome** - Otimiza buscas textuais
2. **idx_categoria** - Acelera filtros por categoria
3. **idx_preco** - Melhora ordenação por preço

---

## 📊 Estatísticas do Catálogo

| Métrica | Valor |
|---------|-------|
| Total de Produtos | 32 |
| Categorias | 4 (Calçados, Roupas, Acessórios, Fitness) |
| Faixa de Preços | R$ 24,90 - R$ 499,90 |
| Preço Médio | R$ 156,23 |
| Produtos em Promoção | ~70% |

---

## 🔄 Integração RAG

A modelagem física foi otimizada para o pipeline RAG:

```
1. RETRIEVAL
   └─ ProductRetriever busca produtos usando índices

2. AUGMENTED  
   └─ ContextAugmenter formata produtos em contexto

3. GENERATION
   └─ ResponseGenerator cria resposta com Claude (AWS Bedrock)
```

---

## 📝 Categorias Suportadas

### 👟 Calçados
- Sandálias, Tênis, Sapatos, Botas, Chinelos

### 👕 Roupas
- Camisetas, Vestidos, Calças, Shorts, Jaquetas

### 👜 Acessórios
- Óculos, Bolsas, Relógios, Cintos, Carteiras

### 🏃 Fitness
- Roupas de treino, Equipamentos

---

## 💡 Como Usar Esta Documentação

### Para Desenvolvedores
1. Leia **documentacao_modelagem_fisica.md** para entender a estrutura
2. Use **modelagem_fisica.sql** para criar o banco
3. Consulte **dicionario_dados.md** para referência de campos

### Para Analistas de Dados
1. Veja **estrutura_visual.txt** para visão geral rápida
2. Use queries de exemplo em **modelagem_fisica.sql**
3. Consulte estatísticas em **documentacao_modelagem_fisica.md**

### Para Designers/UX
1. Visualize **diagrama_erd.mermaid** no mermaid.live
2. Entenda categorias em **estrutura_visual.txt**
3. Veja exemplos de produtos em **dicionario_dados.md**

---

## 🛠️ Criação do Banco

Para criar o banco de dados:

```bash
# Opção 1: Executar o script SQL
sqlite3 catalogo.db < modelagem_fisica.sql

# Opção 2: Via Python
python criar_catalogo.py
```

---

## 🔐 Validações Implementadas

✅ Preço promocional menor que preço normal  
✅ Estoque sempre >= 0  
✅ Avaliação entre 0.0 e 5.0  
✅ Campos obrigatórios validados  
✅ Data de cadastro automática  

---

## 📈 Performance

- **Índices:** Otimizados para queries do RAG
- **Triggers:** Validam dados em tempo de inserção
- **Views:** Facilitam consultas complexas
- **Adequado para:** Catálogos até ~100k produtos

---

## 🔄 Manutenção

```sql
-- Backup
.backup catalogo_backup.db

-- Otimização
VACUUM;

-- Análise
ANALYZE;

-- Verificar integridade
PRAGMA integrity_check;
```

---

## 📞 Suporte

Para dúvidas sobre a modelagem:
1. Consulte os arquivos de documentação
2. Revise os comentários no script SQL
3. Veja exemplos de queries inclusos

---

## 📌 Versão

**Versão da Modelagem:** 1.0  
**Data de Criação:** 15/11/2025  
**Última Atualização:** 15/11/2025  
**Sistema:** RAG Catálogo de Produtos  

---

## 🎯 Próximos Passos Sugeridos

1. ✅ Documentação completa - **CONCLUÍDO**
2. 🔄 Implementar sistema de cache
3. 🔄 Adicionar full-text search (FTS5)
4. 🔄 Criar tabela de logs de consultas
5. 🔄 Implementar versionamento de produtos

---

**Documentação gerada automaticamente pelo Sistema RAG**  
**Todos os direitos reservados © 2025**
