from rag.retriever import ProductRetriever
from rag.augmenter import ContextAugmenter
from rag.generator import ResponseGenerator 
from config.settings import APP_NAME, APP_VERSION

class CatalogoRAG:

    def __init__(self):
        self.retriever = ProductRetriever()
        self.augmenter = ContextAugmenter()
        self.generator = ResponseGenerator() 

    def processar_consulta(self, query):
        produtos = self.retriever.retrieve(query)
        contexto = self.augmenter.augment(produtos, query)
        return self.generator.generate(query, contexto)

def main():
    print(f"{APP_NAME} - v{APP_VERSION}")
    app = CatalogoRAG()

    while True:
        q = input("\nVocê: ").strip()
        if q in ("sair", "exit"):
            break
        print("\nAssistente:", app.processar_consulta(q))

if __name__ == "__main__":
    main()
