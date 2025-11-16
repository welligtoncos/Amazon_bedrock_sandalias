from data.database import DatabaseManager
from utils.text_processor import TextProcessor

class ProductRetriever:
    """Recuperador de produtos (RETRIEVAL)"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.processor = TextProcessor()
    
    def retrieve(self, query, limit=5):
        """
        Recupera produtos relevantes
        
        Args:
            query: Pergunta do usuário
            limit: Número máximo de produtos
        
        Returns:
            Lista de produtos encontrados
        """
        # Extrair palavras-chave e filtros
        palavras_chave = self.processor.extrair_palavras_chave(query)
        filtros_auto = self.processor.extrair_filtros(query)
        
        # Adicionar palavras-chave aos filtros
        if palavras_chave:
            filtros_auto['termos'] = palavras_chave
        
        # Buscar produtos
        produtos = self.db.buscar_produtos(filtros=filtros_auto, limit=limit)
        
        # DEBUG (remover em produção)
        print(f"🔍 DEBUG - Palavras-chave: {palavras_chave}")
        print(f"📦 DEBUG - Produtos encontrados: {len(produtos)}")
        
        return produtos