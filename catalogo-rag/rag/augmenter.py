class ContextAugmenter:
    """Gera contexto estruturado e limpo para uso no RAG."""

    # -----------------------------------------
    # Função safe para evitar valores vazios
    # -----------------------------------------
    @staticmethod
    def _safe(value, default="N/A"):
        if value is None or str(value).strip() in ("", "null", "None"):
            return default
        return value

    # -----------------------------------------
    # Formatador de produto (ideal para LLM)
    # -----------------------------------------
    @staticmethod
    def format_product(produto):
        preco = float(produto.get("preco") or 0)
        preco_prom = produto.get("preco_promocional")
        preco_prom = float(preco_prom) if preco_prom else None

        if preco_prom:
            preco_exibir = preco_prom
            promocao_txt = f"Preço original: R$ {preco:.2f} → Agora: R$ {preco_prom:.2f}"
        else:
            preco_exibir = preco
            promocao_txt = "Sem promoção disponível"

        return f"""
=== PRODUTO ===
ID: {produto.get('id')}
Nome: {produto.get('nome')}
Categoria: {ContextAugmenter._safe(produto.get('categoria'))}
Subcategoria: {ContextAugmenter._safe(produto.get('subcategoria'))}
Preço: R$ {preco_exibir:.2f}
Promoção: {promocao_txt}
Marca: {ContextAugmenter._safe(produto.get('marca'))}
Cor: {ContextAugmenter._safe(produto.get('cor'))}
Tamanho: {ContextAugmenter._safe(produto.get('tamanho'))}
Estoque: {ContextAugmenter._safe(produto.get('estoque'))}
Avaliação: {ContextAugmenter._safe(produto.get('avaliacao'))} / 5.0
Nº Avaliações: {ContextAugmenter._safe(produto.get('num_avaliacoes'))}
Descrição: {ContextAugmenter._safe(produto.get('descricao'))}
Especificações: {ContextAugmenter._safe(produto.get('especificacoes'))}
Score_Vectorial: {float(produto.get('score') or 0):.4f}
""".strip()

    # -----------------------------------------
    # Monta o contexto final (para o LLM)
    # -----------------------------------------
    @classmethod
    def augment(cls, produtos, query):
        if not produtos:
            return (
                f"Nenhum produto encontrado para a consulta: '{query}'. "
                "Peça ao usuário mais detalhes ou outra característica."
            )

        blocos = [cls.format_product(prod) for prod in produtos]

        contexto_produtos = "\n\n".join(blocos)

        return f"""
CONSULTA DO USUÁRIO:
"{query}"

PRODUTOS ENCONTRADOS (ORDENADOS POR SIMILARIDADE):
{contexto_produtos}

REGRAS PARA O MODELO:
- Só use os produtos acima.
- Não invente informações, marcas ou preços.
- Se o usuário pedir algo fora dessa lista, responda: "Não está no catálogo".
""".strip()
