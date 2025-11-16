import re
import unicodedata


class TextProcessor:
    """Processador de texto avançado para consultas naturais."""

    STOP_WORDS = {
        'o', 'a', 'os', 'as', 'um', 'uma',
        'de', 'da', 'do', 'das', 'dos',
        'em', 'para', 'com', 'por',
        'que', 'eh', 'é', 'na', 'no',
        'tem', 'têm', 'ha', 'há',
        'quero', 'procuro', 'gostaria',
        'comprar', 'busco', 'preciso',
        'quanto', 'preco', 'preço', 'valor'
    }

    # categorias ampliadas
    CATEGORIAS = {
        "calçados", "calcado", "sandalias", "sandalia",
        "tenis", "tênis", "botas", "sapatos",
        "roupas", "camiseta", "camisa", "calca", "jeans",
        "acessorios", "bolsa", "mochila"
    }

    @staticmethod
    def remover_acentos(texto):
        """Remove acentos"""
        return ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if not unicodedata.combining(c)
        )

    @staticmethod
    def singular(palavra):
        """Melhor singularização"""
        if palavra.endswith("ões"):
            return palavra[:-3] + "ao"
        if palavra.endswith("s") and len(palavra) > 3:
            return palavra[:-1]
        return palavra

    @classmethod
    def extrair_palavras_chave(cls, texto):
        """Extrai keywords para busca texto-livre."""
        texto_limpo = cls.remover_acentos(texto.lower())
        texto_limpo = re.sub(r'[^a-z0-9\s]', ' ', texto_limpo)

        palavras = texto_limpo.split()
        keywords = []

        for palavra in palavras:
            if palavra in cls.STOP_WORDS:
                continue

            if len(palavra) < 3:
                continue

            palavra = cls.singular(palavra)
            keywords.append(palavra)

        # Fallback
        if not keywords:
            keywords = [p for p in palavras if len(p) > 3]

        return keywords

    @classmethod
    def extrair_filtros(cls, texto):
        """Extrai filtros estruturados (categoria, preços, etc.)"""
        filtros = {}

        texto_limpo = cls.remover_acentos(texto.lower())

        # Categoria
        for cat in cls.CATEGORIAS:
            if cat in texto_limpo:
                filtros["categoria"] = cat
                break

        # Preço máximo
        max_match = re.search(
            r"(?:ate|menos que|abaixo de|maximo|ate por)\s*r?\$?\s*(\d+(?:,\d{2})?)",
            texto_limpo
        )
        if max_match:
            filtros["preco_max"] = float(max_match.group(1).replace(",", "."))

        # Preço mínimo
        min_match = re.search(
            r"(?:acima de|mais de|apartir de|a partir de|minimo)\s*r?\$?\s*(\d+(?:,\d{2})?)",
            texto_limpo
        )
        if min_match:
            filtros["preco_min"] = float(min_match.group(1).replace(",", "."))

        # Termos de busca
        termos = cls.extrair_palavras_chave(texto)
        if termos:
            filtros["termos"] = termos

        return filtros
