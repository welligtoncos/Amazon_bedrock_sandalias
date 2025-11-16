class ContextAugmenter:
    """Aumentador de contexto (AUGMENTED)"""
    
    @staticmethod
    def format_product(produto):
        """Formata um produto para exibição"""
        preco_exibir = produto['preco_promocional'] if produto['preco_promocional'] else produto['preco']
        desconto = ""
        
        if produto['preco_promocional']:
            economia = produto['preco'] - produto['preco_promocional']
            perc = (economia / produto['preco']) * 100
            desconto = f" 🔥 PROMOÇÃO! De R$ {produto['preco']:.2f} por"
        
        text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 {produto['nome']}
{desconto}
💰 R$ {preco_exibir:.2f}
🏷️ {produto['categoria']} » {produto['subcategoria'] or 'Geral'}
🏭 Marca: {produto['marca'] or 'N/A'}
🎨 Cor: {produto['cor'] or 'N/A'}
📏 Tamanho: {produto['tamanho'] or 'Único'}
📊 Estoque: {produto['estoque']} unidades
⭐ Avaliação: {produto['avaliacao']}/5.0 ({produto['num_avaliacoes']} avaliações)

📝 {produto['descricao']}
🔧 Especificações: {produto['especificacoes']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return text
    
    @classmethod
    def augment(cls, produtos, query):
        """
        Cria contexto aumentado com produtos
        
        Args:
            produtos: Lista de produtos encontrados
            query: Pergunta original do usuário
        
        Returns:
            String com contexto formatado
        """
        if not produtos:
            return "Nenhum produto encontrado no catálogo."
        
        context = f"Produtos encontrados ({len(produtos)} resultados):\n\n"
        
        for produto in produtos:
            context += cls.format_product(produto)
            context += "\n"
        
        return context