import sqlite3
from config.settings import DB_PATH
import os

class DatabaseManager:
    """Gerenciador do banco de dados"""
    
    def __init__(self):
        self.db_path = DB_PATH
        
        # Verificar se banco existe
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"Banco de dados não encontrado em: {self.db_path}\n"
                f"Execute primeiro: python criar_catalogo.py"
            )
    
    def get_connection(self):
        """Retorna conexão com o banco"""
        return sqlite3.connect(self.db_path)
    
    def buscar_produtos(self, filtros=None, limit=10):
        """
        Busca produtos com filtros
        
        Args:
            filtros: Dict com filtros
            limit: Número máximo de resultados
        
        Returns:
            Lista de produtos
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []
        
        if filtros:
            # Busca por termo (palavras-chave)
            if 'termos' in filtros and filtros['termos']:
                condicoes = []
                for termo in filtros['termos']:
                    condicoes.append("""(
                        LOWER(REPLACE(REPLACE(REPLACE(REPLACE(nome, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) 
                        LIKE LOWER(?)
                        OR 
                        LOWER(REPLACE(REPLACE(REPLACE(REPLACE(descricao, 'á', 'a'), 'é', 'e'), 'í', 'i'), 'ó', 'o')) 
                        LIKE LOWER(?)
                    )""")
                    params.extend(['%' + termo + '%', '%' + termo + '%'])
                
                query += " AND (" + " OR ".join(condicoes) + ")"
            
            # Filtro de categoria
            if 'categoria' in filtros:
                query += " AND LOWER(categoria) LIKE LOWER(?)"
                params.append('%' + filtros['categoria'] + '%')
            
            # Filtro de preço
            if 'preco_min' in filtros:
                query += " AND preco >= ?"
                params.append(filtros['preco_min'])
            
            if 'preco_max' in filtros:
                query += " AND preco <= ?"
                params.append(filtros['preco_max'])
        
        query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        
        return self._format_results(results)
    
    def _format_results(self, results):
        """Formata resultados do banco"""
        colunas = [
            'id', 'nome', 'categoria', 'subcategoria', 'preco', 'preco_promocional',
            'marca', 'cor', 'tamanho', 'material', 'estoque', 'descricao',
            'especificacoes', 'avaliacao', 'num_avaliacoes', 'peso', 'dimensoes', 'data_cadastro'
        ]
        
        produtos = []
        for row in results:
            produto = dict(zip(colunas, row))
            produtos.append(produto)
        
        return produtos
    
    def get_estatisticas(self):
        """Retorna estatísticas do catálogo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total de produtos
        cursor.execute("SELECT COUNT(*) FROM produtos")
        stats['total_produtos'] = cursor.fetchone()[0]
        
        # Produtos por categoria
        cursor.execute("SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria")
        stats['por_categoria'] = dict(cursor.fetchall())
        
        # Faixa de preços
        cursor.execute("SELECT MIN(preco), MAX(preco), AVG(preco) FROM produtos")
        min_p, max_p, avg_p = cursor.fetchone()
        stats['preco_min'] = min_p
        stats['preco_max'] = max_p
        stats['preco_medio'] = round(avg_p, 2)
        
        conn.close()
        return stats