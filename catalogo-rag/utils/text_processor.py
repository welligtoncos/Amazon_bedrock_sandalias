import re
import unicodedata

class TextProcessor:
    """Processador de texto para extração de informações"""
    
    STOP_WORDS = {
        'o', 'a', 'de', 'da', 'do', 'em', 'para', 'com', 'os', 'as',
        'um', 'uma', 'e', 'é', 'eh', 'que', 'na', 'no', 'tem', 'têm', 'ter',
        'qual', 'quais', 'você', 'voce', 'vocês', 'voces', 'possui', 'ha', 'há',
        'quero', 'comprar', 'procuro', 'busco', 'gostaria', 'preciso',
        'quanto', 'custa', 'custam', 'preço', 'preco', 'preços', 'precos', 
        'valor', 'valores', 'cor', 'cores'
    }
    
    CATEGORIAS = ['calçados', 'calcados', 'calcado', 'roupas', 'roupa', 'acessórios', 'acessorios', 'fitness']
    
    @staticmethod
    def remover_acentos(texto):
        """Remove acentos do texto"""
        nfkd = unicodedata.normalize('NFKD', texto)
        return "".join([c for c in nfkd if not unicodedata.combining(c)])
    
    @staticmethod
    def singular(palavra):
        """Converte palavra para singular"""
        if palavra.endswith('s') and len(palavra) > 3:
            return palavra[:-1]
        return palavra
    
    @classmethod
    def extrair_palavras_chave(cls, texto):
        """Extrai palavras-chave relevantes"""
        texto_limpo = cls.remover_acentos(texto.lower())
        texto_limpo = re.sub(r'[^\w\s]', ' ', texto_limpo)
        
        palavras = texto_limpo.split()
        palavras_filtradas = []
        
        for palavra in palavras:
            if palavra not in cls.STOP_WORDS and len(palavra) > 2:
                palavra_singular = cls.singular(palavra)
                palavras_filtradas.append(palavra_singular)
        
        # Fallback
        if not palavras_filtradas:
            palavras_filtradas = [p for p in palavras if len(p) > 3]
        
        return palavras_filtradas
    
    @classmethod
    def extrair_filtros(cls, texto):
        """Extrai filtros da consulta do usuário"""
        filtros = {}
        
        # Extrair categoria
        texto_lower = cls.remover_acentos(texto.lower())
        for cat in cls.CATEGORIAS:
            if cat in texto_lower:
                filtros['categoria'] = cat
                break
        
        # Extrair faixa de preço
        preco_match = re.search(r'(?:até|menos|abaixo)\s*(?:de\s*)?r?\$?\s*(\d+(?:,\d{2})?)', texto_lower)
        if preco_match:
            filtros['preco_max'] = float(preco_match.group(1).replace(',', '.'))
        
        preco_match = re.search(r'(?:acima|mais|a partir)\s*(?:de\s*)?r?\$?\s*(\d+(?:,\d{2})?)', texto_lower)
        if preco_match:
            filtros['preco_min'] = float(preco_match.group(1).replace(',', '.'))
        
        return filtros