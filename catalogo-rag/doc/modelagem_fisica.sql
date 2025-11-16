-- ============================================================
-- MODELAGEM FÍSICA - SISTEMA RAG DE CATÁLOGO DE PRODUTOS
-- ============================================================
-- Database: SQLite 3
-- Autor: Sistema Catalogo RAG
-- Data: 2025-11-15
-- Descrição: Estrutura de banco de dados para catálogo de 
--            produtos com suporte a RAG (Retrieval-Augmented 
--            Generation)
-- ============================================================

-- ============================================================
-- TABELA: produtos
-- ============================================================
-- Armazena o catálogo completo de produtos disponíveis para
-- consulta e venda através do assistente virtual.
-- ============================================================

CREATE TABLE IF NOT EXISTS produtos (
    -- Identificação
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    
    -- Classificação
    categoria           TEXT NOT NULL,
    subcategoria        TEXT,
    
    -- Precificação
    preco               REAL NOT NULL,
    preco_promocional   REAL,  -- NULL = sem promoção
    
    -- Características
    marca               TEXT,
    cor                 TEXT,
    tamanho             TEXT,
    material            TEXT,
    
    -- Estoque
    estoque             INTEGER NOT NULL DEFAULT 0,
    
    -- Descrição
    descricao           TEXT,
    especificacoes      TEXT,
    
    -- Avaliações
    avaliacao           REAL CHECK(avaliacao >= 0.0 AND avaliacao <= 5.0),
    num_avaliacoes      INTEGER DEFAULT 0,
    
    -- Especificações físicas
    peso                REAL,  -- em quilogramas
    dimensoes           TEXT,  -- formato: "LxAxP cm"
    
    -- Auditoria
    data_cadastro       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ÍNDICES
-- ============================================================
-- Índices para otimização de consultas frequentes do sistema RAG
-- ============================================================

-- Índice para buscas por nome (usado em queries textuais)
CREATE INDEX IF NOT EXISTS idx_nome 
    ON produtos(nome);

-- Índice para filtros por categoria
CREATE INDEX IF NOT EXISTS idx_categoria 
    ON produtos(categoria);

-- Índice para filtros e ordenação por preço
CREATE INDEX IF NOT EXISTS idx_preco 
    ON produtos(preco);

-- ============================================================
-- COMENTÁRIOS E REGRAS DE NEGÓCIO
-- ============================================================

-- CATEGORIAS VÁLIDAS:
--   - Calçados: Sandálias, Tênis, Sapatos, Botas, Chinelos
--   - Roupas: Camisetas, Vestidos, Calças, Shorts, Jaquetas
--   - Acessórios: Óculos, Bolsas, Relógios, Cintos, Carteiras
--   - Fitness: Roupas de treino, Equipamentos

-- REGRAS DE PREÇO:
--   - preco: Preço normal do produto (obrigatório)
--   - preco_promocional: Preço em promoção (opcional)
--   - Se preco_promocional existe, deve ser menor que preco

-- REGRAS DE ESTOQUE:
--   - estoque >= 0 sempre
--   - estoque = 0 indica produto esgotado
--   - Recomendado manter estoque mínimo de 10 unidades

-- REGRAS DE AVALIAÇÃO:
--   - avaliacao: Média de 0.0 a 5.0
--   - num_avaliacoes: Quantidade de avaliações recebidas

-- FORMATO DE DADOS:
--   - peso: Valor em kg (ex: 0.85 para 850g)
--   - dimensoes: String "LxAxP cm" (ex: "30x20x12cm")
--   - tamanho: Varia por categoria
--       * Calçados: numeração (ex: "40", "37/38")
--       * Roupas: P/M/G/GG ou números
--       * Acessórios: Único ou medidas específicas

-- ============================================================
-- VIEWS AUXILIARES (Opcional - para relatórios)
-- ============================================================

-- View de produtos em promoção
CREATE VIEW IF NOT EXISTS v_produtos_promocao AS
SELECT 
    id,
    nome,
    categoria,
    preco,
    preco_promocional,
    ROUND((preco - preco_promocional) / preco * 100, 2) as desconto_percentual,
    marca,
    estoque
FROM produtos
WHERE preco_promocional IS NOT NULL
ORDER BY desconto_percentual DESC;

-- View de produtos mais bem avaliados
CREATE VIEW IF NOT EXISTS v_produtos_top_avaliados AS
SELECT 
    id,
    nome,
    categoria,
    preco,
    avaliacao,
    num_avaliacoes,
    marca
FROM produtos
WHERE avaliacao >= 4.5 
  AND num_avaliacoes >= 100
ORDER BY avaliacao DESC, num_avaliacoes DESC;

-- View de produtos com estoque baixo
CREATE VIEW IF NOT EXISTS v_estoque_baixo AS
SELECT 
    id,
    nome,
    categoria,
    estoque,
    preco,
    marca
FROM produtos
WHERE estoque > 0 AND estoque < 10
ORDER BY estoque ASC;

-- ============================================================
-- TRIGGERS (Opcional - para validações)
-- ============================================================

-- Trigger para garantir que preco_promocional < preco
CREATE TRIGGER IF NOT EXISTS trg_validar_preco_promocional
BEFORE INSERT ON produtos
WHEN NEW.preco_promocional IS NOT NULL
BEGIN
    SELECT CASE
        WHEN NEW.preco_promocional >= NEW.preco THEN
            RAISE(ABORT, 'Preço promocional deve ser menor que o preço normal')
    END;
END;

-- Trigger para validar estoque não negativo
CREATE TRIGGER IF NOT EXISTS trg_validar_estoque
BEFORE UPDATE ON produtos
WHEN NEW.estoque < 0
BEGIN
    SELECT RAISE(ABORT, 'Estoque não pode ser negativo');
END;

-- ============================================================
-- QUERIES ÚTEIS PARA O SISTEMA RAG
-- ============================================================

-- Busca por termo (usado pelo TextProcessor)
-- SELECT * FROM produtos 
-- WHERE LOWER(nome) LIKE LOWER('%termo%')
--    OR LOWER(descricao) LIKE LOWER('%termo%')
-- LIMIT 5;

-- Busca com filtros de categoria e preço
-- SELECT * FROM produtos
-- WHERE categoria = 'Calçados'
--   AND preco BETWEEN 50 AND 200
-- ORDER BY avaliacao DESC
-- LIMIT 10;

-- Estatísticas do catálogo
-- SELECT 
--     COUNT(*) as total_produtos,
--     COUNT(DISTINCT categoria) as total_categorias,
--     MIN(preco) as preco_minimo,
--     MAX(preco) as preco_maximo,
--     AVG(preco) as preco_medio,
--     SUM(estoque) as estoque_total
-- FROM produtos;

-- ============================================================
-- FIM DA MODELAGEM FÍSICA
-- ============================================================
