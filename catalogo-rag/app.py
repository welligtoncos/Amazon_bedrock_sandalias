from rag.retriever import ProductRetriever
from rag.augmenter import ContextAugmenter
from rag.generator import ResponseGenerator
from data.database import DatabaseManager
from config.settings import APP_NAME, APP_VERSION

class CatalogoRAG:
    """Aplicação principal RAG"""
    
    def __init__(self):
        self.retriever = ProductRetriever()
        self.augmenter = ContextAugmenter()
        self.generator = ResponseGenerator()
        self.db = DatabaseManager()
    
    def processar_consulta(self, query):
        """
        Processa consulta do usuário (Pipeline RAG completo)
        
        Args:
            query: Pergunta do usuário
        
        Returns:
            Resposta gerada
        """
        # STEP 1: RETRIEVAL - Buscar produtos relevantes
        produtos = self.retriever.retrieve(query, limit=5)
        
        # STEP 2: AUGMENTED - Montar contexto
        context = self.augmenter.augment(produtos, query)
        
        # STEP 3: GENERATION - Gerar resposta
        response = self.generator.generate(query, context)
        
        return response
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas do catálogo"""
        stats = self.db.get_estatisticas()
        
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DO CATÁLOGO")
        print("="*60)
        print(f"📦 Total de produtos: {stats['total_produtos']}")
        print(f"💰 Faixa de preços: R$ {stats['preco_min']:.2f} - R$ {stats['preco_max']:.2f}")
        print(f"📊 Preço médio: R$ {stats['preco_medio']:.2f}")
        print("\n🏷️ Produtos por categoria:")
        for cat, count in stats['por_categoria'].items():
            print(f"   • {cat}: {count} produtos")
        print("="*60 + "\n")

def main():
    """Função principal"""
    print("="*60)
    print(f"🛍️  {APP_NAME}")
    print(f"📌 Versão {APP_VERSION}")
    print("="*60)
    print("\n👋 Olá! Sou seu assistente de compras virtual!")
    print("Posso ajudá-lo a encontrar produtos do nosso catálogo.\n")
    print("💡 Exemplos de perguntas:")
    print("   • 'Quero um tênis para corrida'")
    print("   • 'Mostre vestidos até R$ 100'")
    print("   • 'Tem óculos de sol em promoção?'")
    print("   • 'Calçados femininos confortáveis'")
    print("\n💬 Digite 'sair' para encerrar")
    print("📊 Digite 'stats' para ver estatísticas do catálogo")
    print("-"*60)
    
    try:
        app = CatalogoRAG()
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        return
    
    while True:
        try:
            # Receber entrada
            query = input("\n👤 Você: ").strip()
            
            # Comandos especiais
            if query.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Obrigado por usar nosso assistente! Até logo!")
                break
            
            if query.lower() == 'stats':
                app.mostrar_estatisticas()
                continue
            
            if not query:
                continue
            
            # Processar consulta
            response = app.processar_consulta(query)
            print(f"\n🤖 Assistente: {response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            print("Por favor, tente novamente.")

if __name__ == "__main__":
    main()