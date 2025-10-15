import boto3
import json
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from datetime import datetime

# ============================================
# CONFIGURAÇÃO BEDROCK
# ============================================
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name="us-east-2"
)

MODEL_ID = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'

# ============================================
# FUNÇÃO PARA CONFIGURAR MODELO
# ============================================
def configurar_modelo(client, max_tokens=500, temperature=0.3, top_p=0.9):
    """Configura parâmetros do modelo para análises financeiras precisas"""
    def _invocar_com_parametros(messages):
        if isinstance(messages, dict):
            entrada = messages.get('query', messages.get('input', ''))
        elif isinstance(messages, list):
            entrada = str(messages[-1].content if hasattr(messages[-1], 'content') else messages[-1])
        else:
            entrada = str(messages)
        
        config = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "system": """Você é um assistente financeiro e contábil especializado da RSM/Pollvo.

SUAS RESPONSABILIDADES:
- Analisar dados financeiros, contábeis, fiscais e de folha de pagamento
- Fornecer insights baseados em dados reais do banco
- Responder perguntas sobre receitas, despesas, impostos, funcionários
- Calcular métricas e KPIs quando solicitado
- Identificar tendências e anomalias

REGRAS IMPORTANTES:
- Use APENAS dados fornecidos do banco de dados
- Sempre formate valores monetários em R$ (ex: R$ 123.456,78)
- Mencione períodos (mês/ano) quando relevante
- Se não houver dados: informe claramente e não invente
- Seja preciso com números e cálculos
- Destaque insights relevantes
- Use linguagem profissional mas acessível

FORMATO DE RESPOSTA:
- Clara e objetiva
- Com valores formatados corretamente
- Destacando informações-chave
- Com contexto temporal quando aplicável""",
            "messages": [{"role": "user", "content": entrada}]
        }
        
        response = client.invoke_model(
            body=json.dumps(config),
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json"
        )
        
        resposta = json.loads(response['body'].read().decode('utf-8'))
        return resposta.get('content', [{}])[0].get('text', 'Erro ao processar')
    
    return RunnableLambda(_invocar_com_parametros)

modelo = configurar_modelo(bedrock_client)

# ============================================
# HISTÓRICO
# ============================================
historico = []

def get_hist():
    return "\n".join(historico)

# ============================================
# FUNÇÕES DE CONSULTA INTELIGENTE (CORRIGIDAS)
# ============================================
def consultar_dados_financeiros(pergunta):
    """
    Identifica tipo de consulta e executa SQL apropriado
    Retorna: (tipo_consulta, dados, colunas)
    """
    conn = sqlite3.connect('dados_financeiros.db')
    cursor = conn.cursor()
    
    pergunta_lower = pergunta.lower()
    
    try:
        # ============================================
        # 1. RECEITAS / FATURAMENTO
        # ============================================
        if any(palavra in pergunta_lower for palavra in ['receita', 'faturamento', 'vendas', 'lucro']):
            # Verificar se é por empresa específica
            empresas = ['rsm brasil', 'rsm tech', 'rsm consultoria', 'rsm auditoria', 
                       'pollvo digital', 'pollvo labs', 'pollvo']
            empresa_filtro = None
            for emp in empresas:
                if emp in pergunta_lower:
                    empresa_filtro = emp
                    break
            
            if empresa_filtro:
                # 🔧 CORREÇÃO: Ajustar SELECT para corresponder às colunas
                cursor.execute('''
                SELECT empresa, centro_custo, SUM(receita) as total, ano, mes
                FROM rsm_contabil_consolidado
                WHERE LOWER(empresa) LIKE ?
                GROUP BY empresa, centro_custo, ano, mes
                ORDER BY ano DESC, mes DESC, total DESC
                LIMIT 15
                ''', ('%' + empresa_filtro + '%',))
                colunas = ['Empresa', 'Centro de Custo', 'Receita Total', 'Ano', 'Mês']
            else:
                cursor.execute('''
                SELECT empresa, SUM(receita) as total, ano, mes
                FROM rsm_contabil_consolidado
                GROUP BY empresa, ano, mes
                ORDER BY ano DESC, mes DESC, total DESC
                LIMIT 20
                ''')
                colunas = ['Empresa', 'Receita Total', 'Ano', 'Mês']
            
            tipo = "RECEITAS E FATURAMENTO"
        
        # ============================================
        # 2. IMPOSTOS / TRIBUTOS (CORRIGIDO)
        # ============================================
        elif any(palavra in pergunta_lower for palavra in ['imposto', 'tributo', 'fiscal', 'irpj', 'csll', 'pis', 'cofins', 'iss', 'inss']):
            tipo_imposto = None
            for tipo_imp in ['irpj', 'csll', 'pis', 'cofins', 'iss', 'inss', 'icms', 'ipi']:
                if tipo_imp in pergunta_lower:
                    tipo_imposto = tipo_imp.upper()
                    break
            
            if tipo_imposto:
                # 🔧 CORREÇÃO: Usar valor_a_recolher ao invés de imposto
                cursor.execute('''
                SELECT empresa, tipo_imposto, SUM(valor_a_recolher) as total, 
                       AVG(aliquota_efetiva) as aliquota_media, ano, mes
                FROM fiscal_consolidado
                WHERE UPPER(tipo_imposto) = ?
                GROUP BY empresa, tipo_imposto, ano, mes
                ORDER BY ano DESC, mes DESC, total DESC
                LIMIT 15
                ''', (tipo_imposto,))
                colunas = ['Empresa', 'Tipo', 'Total', 'Alíquota Média (%)', 'Ano', 'Mês']
            else:
                # 🔧 CORREÇÃO: Usar valor_a_recolher
                cursor.execute('''
                SELECT tipo_imposto, SUM(valor_a_recolher) as total, 
                       AVG(aliquota_efetiva) as aliquota_media, ano, mes
                FROM fiscal_consolidado
                GROUP BY tipo_imposto, ano, mes
                ORDER BY ano DESC, mes DESC, total DESC
                LIMIT 20
                ''')
                colunas = ['Tipo Imposto', 'Total', 'Alíquota Média (%)', 'Ano', 'Mês']
            
            tipo = "IMPOSTOS E TRIBUTOS"
        
        # ============================================
        # 3. FOLHA DE PAGAMENTO
        # ============================================
        elif any(palavra in pergunta_lower for palavra in ['folha', 'funcionário', 'funcionario', 'salário', 'salario', 'departamento', 'rh', 'ti']):
            # Verificar se busca departamento específico
            if 'ti' in pergunta_lower or 'tecnologia' in pergunta_lower:
                cursor.execute('''
                SELECT departamento, empresa, SUM(funcionarios) as total_func, 
                       SUM(folha) as total_folha, AVG(salario_medio) as salario_medio_geral,
                       ano, mes
                FROM folha_consolidada
                WHERE LOWER(departamento) LIKE '%ti%' 
                   OR LOWER(departamento) LIKE '%tecnologia%'
                   OR LOWER(departamento) LIKE '%desenvolvimento%'
                   OR LOWER(departamento) LIKE '%suporte%'
                GROUP BY departamento, empresa, ano, mes
                ORDER BY ano DESC, mes DESC, total_folha DESC
                LIMIT 20
                ''')
            else:
                cursor.execute('''
                SELECT departamento, empresa, SUM(funcionarios) as total_func, 
                       SUM(folha) as total_folha, AVG(salario_medio) as salario_medio_geral,
                       ano, mes
                FROM folha_consolidada
                GROUP BY departamento, empresa, ano, mes
                ORDER BY ano DESC, mes DESC, total_folha DESC
                LIMIT 20
                ''')
            
            colunas = ['Departamento', 'Empresa', 'Funcionários', 'Folha Total', 'Salário Médio', 'Ano', 'Mês']
            tipo = "FOLHA DE PAGAMENTO"
        
        # ============================================
        # 4. SITUAÇÃO FINANCEIRA
        # ============================================
        elif any(palavra in pergunta_lower for palavra in ['financeiro', 'pago', 'pendente', 'vencido', 'contas', 'pagamento', 'pagar']):
            cursor.execute('''
            SELECT status, empresa, SUM(quantidade) as qtd, SUM(valor) as total, ano, mes
            FROM financeiro_consolidado
            GROUP BY status, empresa, ano, mes
            ORDER BY ano DESC, mes DESC, total DESC
            LIMIT 20
            ''')
            colunas = ['Status', 'Empresa', 'Quantidade', 'Valor Total', 'Ano', 'Mês']
            tipo = "SITUAÇÃO FINANCEIRA"
        
        # ============================================
        # 5. PROJETOS / CLIENTES
        # ============================================
        elif any(palavra in pergunta_lower for palavra in ['projeto', 'cliente', 'timesheet', 'pollvo', 'lucrat']):
            cursor.execute('''
            SELECT projeto, cliente, SUM(receita_projeto) as total, ano, mes
            FROM pollvo_timesheet
            GROUP BY projeto, cliente, ano, mes
            ORDER BY ano DESC, mes DESC, total DESC
            LIMIT 20
            ''')
            colunas = ['Projeto', 'Cliente', 'Receita', 'Ano', 'Mês']
            tipo = "PROJETOS E CLIENTES"
        
        # ============================================
        # 6. COMPARAÇÃO / TENDÊNCIAS (CORRIGIDO)
        # ============================================
        elif any(palavra in pergunta_lower for palavra in ['comparar', 'comparação', 'comparacao', 'tendência', 'tendencia', 'evolução', 'evolucao', 'crescimento', 'últimos', 'ultimos', 'últimas', 'ultimas']):
            # 🔧 CORREÇÃO: Usar nomes corretos da view
            cursor.execute('''
            SELECT ano, mes, 
                   receita_total_rsm, receita_total_pollvo,
                   impostos_total, folha_total, funcionarios_total
            FROM resumo_executivo
            ORDER BY ano DESC, mes DESC
            LIMIT 12
            ''')
            colunas = ['Ano', 'Mês', 'Receita RSM', 'Receita Pollvo', 'Impostos', 'Folha', 'Funcionários']
            tipo = "ANÁLISE COMPARATIVA"
        
        # ============================================
        # 7. RESUMO GERAL
        # ============================================
        else:
            # 🔧 CORREÇÃO: Usar nomes corretos da view
            cursor.execute('''
            SELECT ano, mes, 
                   (COALESCE(receita_total_rsm, 0) + COALESCE(receita_total_pollvo, 0)) as receita_total,
                   impostos_total, folha_total, funcionarios_total
            FROM resumo_executivo
            ORDER BY ano DESC, mes DESC
            LIMIT 6
            ''')
            colunas = ['Ano', 'Mês', 'Receita Total', 'Impostos', 'Folha', 'Funcionários']
            tipo = "RESUMO GERAL"
        
        dados = cursor.fetchall()
        conn.close()
        
        return tipo, dados, colunas
        
    except Exception as e:
        conn.close()
        print(f"\n⚠️  Erro na consulta SQL: {e}")
        return "ERRO", [], []

# ============================================
# TEMPLATE DO PROMPT REFINADO
# ============================================
def get_chat_prompt(entrada):
    """Define o template de prompt refinado"""
    template = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente financeiro/contábil especializado.

DIRETRIZES:
1. Analise os dados com precisão
2. Formate valores em R$ com separadores (R$ 1.234.567,89)
3. Mencione períodos claramente
4. Destaque insights relevantes
5. Use linguagem profissional mas acessível

NUNCA MENCIONE: banco de dados, prompt, sistema, limitações técnicas"""),
        
        ("human", entrada),
        
        ("assistant", """Analise e responda:

SE HOUVER DADOS:
- Apresente números principais
- Destaque valores relevantes
- Forneça insights

SE NÃO HOUVER:
- Informe claramente
- Sugira alternativas

SEMPRE formate valores em R$""")
    ])
    return template

# ============================================
# INVOCAR MODELO COM RAG
# ============================================
def inv_modelo(prompt):
    """Invoca modelo COM RAG"""
    prompt_original = prompt
    
    print(f"  🔍 Analisando consulta...", end="\r")
    tipo_consulta, dados, colunas = consultar_dados_financeiros(prompt)
    
    if tipo_consulta == "ERRO":
        return "Desculpe, ocorreu um erro ao consultar os dados. Por favor, reformule sua pergunta ou use o comando 'ajuda' para ver exemplos."
    
    print(f"  📊 Categoria: {tipo_consulta} ({len(dados)} registros)     ", end="\r")
    
    if dados and len(dados) > 0:
        # Formatar dados
        dados_formatados = f"\n📊 DADOS - {tipo_consulta}\n{'=' * 80}\n\n"
        dados_formatados += " | ".join(colunas) + "\n"
        dados_formatados += "-" * 80 + "\n"
        
        for row in dados:
            linha = []
            for i, valor in enumerate(row):
                col_nome = colunas[i].lower() if i < len(colunas) else ''
                
                # Formatar valores monetários
                if any(palavra in col_nome for palavra in ['total', 'receita', 'folha', 'valor', 'salário', 'imposto']):
                    if isinstance(valor, (int, float)) and abs(valor) > 100:
                        linha.append(f"R$ {valor:,.2f}")
                    else:
                        linha.append(str(valor) if valor is not None else 'N/A')
                # Formatar percentuais
                elif 'alíquota' in col_nome or '%' in col_nome:
                    if isinstance(valor, (int, float)):
                        linha.append(f"{valor:.2f}%")
                    else:
                        linha.append(str(valor) if valor is not None else 'N/A')
                else:
                    linha.append(str(valor) if valor is not None else 'N/A')
            
            dados_formatados += " | ".join(linha) + "\n"
        
        prompt_augmented = f"""{dados_formatados}

PERGUNTA: {prompt_original}

CONTEXTO:
- Data: {datetime.now().strftime('%d/%m/%Y')}
- Registros: {len(dados)}
- Categoria: {tipo_consulta}

INSTRUÇÕES:
1. Analise os dados
2. Formate valores em R$
3. Mencione períodos
4. Destaque insights
5. Seja objetivo"""
        
    else:
        prompt_augmented = f"""SITUAÇÃO: Nenhum dado encontrado.

CONSULTA: "{prompt_original}"
CATEGORIA: {tipo_consulta}

INSTRUÇÕES:
1. Informe que não há dados
2. Sugira consultas alternativas:
   • Receitas por empresa
   • Impostos por tipo
   • Folha por departamento
   • Situação financeira
   • Projetos Pollvo
3. Seja prestativo"""
    
    chain = get_chat_prompt(prompt_augmented).pipe(modelo)
    response = chain.invoke({"query": prompt_augmented})
    return response

# ============================================
# COMANDOS ESPECIAIS (mantidos iguais)
# ============================================
def mostrar_resumo():
    """Mostra resumo executivo"""
    conn = sqlite3.connect('dados_financeiros.db')
    cursor = conn.cursor()
    data_atual = datetime.now()
    
    print("\n" + "=" * 80)
    print(f"📊 RESUMO EXECUTIVO - {data_atual.strftime('%B/%Y').upper()}")
    print("=" * 80)
    
    # Receitas
    cursor.execute('SELECT SUM(receita) FROM rsm_contabil_consolidado WHERE ano = ? AND mes = ?', 
                  (data_atual.year, data_atual.month))
    receita_rsm = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(receita) FROM pollvo_contabil_consolidado WHERE ano = ? AND mes = ?',
                  (data_atual.year, data_atual.month))
    receita_pollvo = cursor.fetchone()[0] or 0
    
    print(f"\n💰 RECEITAS:")
    print(f"   • RSM:    R$ {receita_rsm:>15,.2f}")
    print(f"   • Pollvo: R$ {receita_pollvo:>15,.2f}")
    print(f"   • TOTAL:  R$ {(receita_rsm + receita_pollvo):>15,.2f}")
    
    # Impostos (CORRIGIDO)
    cursor.execute('''
    SELECT tipo_imposto, SUM(imposto) as total
    FROM rsm_fiscal_consolidado
    WHERE ano = ? AND mes = ?
    GROUP BY tipo_imposto
    ORDER BY total DESC
    LIMIT 5
    ''', (data_atual.year, data_atual.month))
    
    print(f"\n📊 IMPOSTOS (Top 5):")
    impostos_total = 0
    for row in cursor.fetchall():
        print(f"   • {row[0]:10} → R$ {row[1]:>12,.2f}")
        impostos_total += row[1]
    print(f"   {'─' * 35}")
    print(f"   • TOTAL:      R$ {impostos_total:>12,.2f}")
    
    # Folha
    cursor.execute('''
    SELECT SUM(folha), SUM(funcionarios) FROM rsm_folha_consolidada
    WHERE ano = ? AND mes = ?
    ''', (data_atual.year, data_atual.month))
    folha_dados = cursor.fetchone()
    folha = folha_dados[0] or 0
    func = folha_dados[1] or 0
    
    print(f"\n👥 FOLHA DE PAGAMENTO:")
    print(f"   • Funcionários:    {func:>6}")
    print(f"   • Folha Total:     R$ {folha:>12,.2f}")
    if func > 0:
        print(f"   • Salário Médio:   R$ {(folha/func):>12,.2f}")
    
    # Financeiro
    cursor.execute('''
    SELECT status, SUM(qtd), SUM(total)
    FROM rsm_financeiro_consolidado
    WHERE ano = ? AND mes = ?
    GROUP BY status
    ORDER BY SUM(total) DESC
    ''', (data_atual.year, data_atual.month))
    
    print(f"\n💳 SITUAÇÃO FINANCEIRA:")
    for row in cursor.fetchall():
        print(f"   • {row[0]:15} → {row[1]:4} itens | R$ {row[2]:>12,.2f}")
    
    print("=" * 80 + "\n")
    conn.close()

def listar_empresas():
    """Lista empresas"""
    conn = sqlite3.connect('dados_financeiros.db')
    cursor = conn.cursor()
    
    print("\n" + "=" * 80)
    print("🏢 EMPRESAS CADASTRADAS")
    print("=" * 80)
    
    print("\n📌 RSM:")
    cursor.execute('SELECT DISTINCT empresa FROM rsm_contabil_consolidado ORDER BY empresa')
    for row in cursor.fetchall():
        print(f"   • {row[0]}")
    
    print("\n📌 POLLVO:")
    cursor.execute('SELECT DISTINCT empresa FROM pollvo_contabil_consolidado ORDER BY empresa')
    for row in cursor.fetchall():
        print(f"   • {row[0]}")
    
    print("=" * 80 + "\n")
    conn.close()

def mostrar_ajuda():
    """Mostra exemplos"""
    print("\n" + "=" * 80)
    print("💡 EXEMPLOS DE CONSULTAS")
    print("=" * 80)
    
    exemplos = {
        "Receitas": [
            "Qual a receita da RSM Brasil?",
            "Mostre o faturamento total",
            "Receitas por centro de custo"
        ],
        "Impostos": [
            "Quanto pagamos de IRPJ?",
            "Top 5 impostos mais caros",
            "Carga tributária total"
        ],
        "Folha": [
            "Quantos funcionários no TI?",
            "Custo da folha de pagamento",
            "Salário médio por departamento"
        ],
        "Financeiro": [
            "Contas pendentes",
            "Situação das contas a pagar",
            "Valor de contas vencidas"
        ],
        "Projetos": [
            "Projetos mais lucrativos da Pollvo",
            "Receita do Projeto Alpha",
            "Top clientes"
        ],
        "Análises": [
            "Compare receitas dos últimos 3 meses",
            "Evolução da folha de pagamento",
            "Tendência de crescimento"
        ]
    }
    
    for categoria, perguntas in exemplos.items():
        print(f"\n📍 {categoria}:")
        for p in perguntas:
            print(f"   • {p}")
    
    print("\n" + "=" * 80 + "\n")

# ============================================
# MENSAGEM INICIAL
# ============================================
print("=" * 80)
print("💼 RSM/POLLVO - ASSISTENTE FINANCEIRO REFINADO v2")
print("=" * 80)
print("✨ RAG + LangChain + Claude 3.5 Haiku + Correções de Bugs")
print("=" * 80)
print(f"\n🤖 Assistente financeiro e contábil pronto!")
print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
print("\n📝 Comandos: resumo | empresas | ajuda | sair")
print("\n💡 Pergunte sobre:")
print("   • Receitas • Impostos • Folha • Financeiro • Projetos\n")
print("-" * 80 + "\n")

# ============================================
# LOOP PRINCIPAL
# ============================================
while True:
    try:
        entrada = input("💬 Você: ").strip()
        
        if entrada.lower() == "sair":
            print("\n👋 Até logo!\n")
            break
        
        if entrada.lower() == "resumo":
            mostrar_resumo()
            continue
        
        if entrada.lower() == "empresas":
            listar_empresas()
            continue
        
        if entrada.lower() == "ajuda":
            mostrar_ajuda()
            continue
        
        if not entrada:
            continue
        
        historico.append(f"User: {entrada}")
        
        response = inv_modelo(entrada)
        
        print(" " * 80, end="\r")
        print(f"\n🤖 Assistente:\n{response}\n")
        print("-" * 80 + "\n")
        
        historico.append(f"Assistant: {response}")
        
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!\n")
        break
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        print("💡 Tente reformular a pergunta ou use 'ajuda'\n")
        if historico and historico[-1].startswith("User:"):
            historico.pop()