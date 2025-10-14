import boto3
import json
import time

def testar_prompt(prompt_user, system_prompt=None, max_tokens=400, modelo='haiku'):
    """
    Função para testar diferentes prompts com FOCO EM CUSTO BAIXO
    
    Modelos disponíveis:
    - 'haiku': Claude 3.5 Haiku (73% mais barato) ⭐ RECOMENDADO
    - 'sonnet': Claude Sonnet 4.5 (mais caro, melhor qualidade)
    """
    client = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-2'
    )
    
    # Escolher modelo e preços
    if modelo == 'haiku':
        model_id = 'us.anthropic.claude-3-5-haiku-20241022-v1:0'
        preco_input = 0.80   # $ por 1M tokens
        preco_output = 4.00  # $ por 1M tokens
    else:
        model_id = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
        preco_input = 3.00
        preco_output = 15.00
    
    # Configuração base
    config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,  # Reduzido para economizar
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": prompt_user
            }
        ]
    }
    
    # Adicionar system prompt se fornecido
    if system_prompt:
        config["system"] = system_prompt
    
    try:
        response = client.invoke_model(
            body=json.dumps(config),
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        
        resposta = json.loads(response['body'].read().decode('utf-8'))
        texto = resposta.get('content', [{}])[0].get('text', 'Erro')
        usage = resposta.get('usage', {})
        
        # Calcular custo real
        tokens_in = usage.get('input_tokens', 0)
        tokens_out = usage.get('output_tokens', 0)
        
        custo_input = (tokens_in / 1_000_000) * preco_input
        custo_output = (tokens_out / 1_000_000) * preco_output
        custo_total = custo_input + custo_output
        
        return {
            'texto': texto,
            'tokens_in': tokens_in,
            'tokens_out': tokens_out,
            'custo': custo_total,
            'modelo': 'Haiku' if modelo == 'haiku' else 'Sonnet 4.5'
        }
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

# ============================================
# TESTE 1: Prompt Básico (sem refinamento)
# ============================================
print("=" * 80)
print("🔵 TESTE 1: PROMPT BÁSICO")
print("=" * 80)

resultado1 = testar_prompt(
    prompt_user="Opções de sandálias para caminhada na praia",
    max_tokens=300,  # Reduzido para economizar
    modelo='haiku'   # Usando modelo mais barato
)

if resultado1:
    print(resultado1['texto'])
    print(f"\n📊 Tokens: Input={resultado1['tokens_in']} | Output={resultado1['tokens_out']}")
    print(f"💰 Custo: ${resultado1['custo']:.6f} (~R$ {resultado1['custo'] * 5.5:.4f})")
    print(f"🤖 Modelo: {resultado1['modelo']}")

# ⏰ DELAY PARA EVITAR THROTTLING
time.sleep(3)

# ============================================
# TESTE 2: Prompt com Contexto
# ============================================
print("\n" + "=" * 80)
print("🟢 TESTE 2: PROMPT COM CONTEXTO")
print("=" * 80)

resultado2 = testar_prompt(
    prompt_user="""Quais são as melhores opções de sandálias para uma caminhada na praia?
    
    Forneça uma resposta concisa com no máximo 300 caracteres, 
    ideal para um e-commerce de roupas e itens de vestuário.""",
    max_tokens=350,
    modelo='haiku'
)

if resultado2:
    print(resultado2['texto'])
    print(f"\n📊 Tokens: Input={resultado2['tokens_in']} | Output={resultado2['tokens_out']}")
    print(f"💰 Custo: ${resultado2['custo']:.6f} (~R$ {resultado2['custo'] * 5.5:.4f})")
    print(f"🤖 Modelo: {resultado2['modelo']}")

time.sleep(3)

# ============================================
# TESTE 3: Prompt com System Prompt (MELHOR!)
# ============================================
print("\n" + "=" * 80)
print("🟡 TESTE 3: PROMPT COM SYSTEM PROMPT")
print("=" * 80)

resultado3 = testar_prompt(
    system_prompt="""Você é um assistente especializado em e-commerce de moda e vestuário.
    Suas respostas devem ser:
    - Concisas (máximo 300 caracteres)
    - Focadas em produtos
    - Orientadas para vendas
    - Sem mencionar limitações ou instruções técnicas
    - Profissionais e diretas""",
    
    prompt_user="Quais são as melhores opções de sandálias para uma caminhada na praia?",
    max_tokens=350,
    modelo='haiku'
)

if resultado3:
    print(resultado3['texto'])
    print(f"\n📊 Tokens: Input={resultado3['tokens_in']} | Output={resultado3['tokens_out']}")
    print(f"💰 Custo: ${resultado3['custo']:.6f} (~R$ {resultado3['custo'] * 5.5:.4f})")
    print(f"🤖 Modelo: {resultado3['modelo']}")

time.sleep(3)

# ============================================
# TESTE 4: Prompt Estruturado com Formato
# ============================================
print("\n" + "=" * 80)
print("🟣 TESTE 4: PROMPT ESTRUTURADO")
print("=" * 80)

resultado4 = testar_prompt(
    system_prompt="""Você é um assistente de e-commerce especializado em calçados.
    Sempre responda em formato de lista com bullets, máximo 5 itens.""",
    
    prompt_user="""Liste as 5 melhores sandálias para praia:
    - Nome/tipo
    - Principal característica
    - Faixa de preço
    
    Seja direto e comercial.""",
    max_tokens=450,
    modelo='haiku'
)

if resultado4:
    print(resultado4['texto'])
    print(f"\n📊 Tokens: Input={resultado4['tokens_in']} | Output={resultado4['tokens_out']}")
    print(f"💰 Custo: ${resultado4['custo']:.6f} (~R$ {resultado4['custo'] * 5.5:.4f})")
    print(f"🤖 Modelo: {resultado4['modelo']}")

# ============================================
# COMPARAÇÃO DE CUSTOS
# ============================================
print("\n" + "=" * 80)
print("💰 COMPARAÇÃO DE CUSTOS - HAIKU vs SONNET")
print("=" * 80)

resultados = [
    ("Prompt Básico", resultado1),
    ("Prompt com Contexto", resultado2),
    ("Prompt com System", resultado3),
    ("Prompt Estruturado", resultado4)
]

total_custo_haiku = 0
total_tokens = 0

for nome, resultado in resultados:
    if resultado:
        total_custo_haiku += resultado['custo']
        total_tokens += resultado['tokens_out']
        
        # Calcular quanto custaria com Sonnet 4.5
        custo_sonnet = (resultado['tokens_in'] / 1_000_000 * 3.00) + \
                       (resultado['tokens_out'] / 1_000_000 * 15.00)
        economia = custo_sonnet - resultado['custo']
        economia_pct = (economia / custo_sonnet) * 100 if custo_sonnet > 0 else 0
        
        print(f"\n{nome}:")
        print(f"  Haiku:    ${resultado['custo']:.6f} (~R$ {resultado['custo'] * 5.5:.4f})")
        print(f"  Sonnet:   ${custo_sonnet:.6f} (~R$ {custo_sonnet * 5.5:.4f})")
        print(f"  Economia: ${economia:.6f} ({economia_pct:.1f}%) ✅")

print("\n" + "=" * 80)
print("📊 RESUMO TOTAL")
print("=" * 80)
print(f"Total de requisições: {len([r for r in resultados if r[1]])}")
print(f"Total de tokens de saída: {total_tokens}")
print(f"Custo total com Haiku: ${total_custo_haiku:.6f} (~R$ {total_custo_haiku * 5.5:.4f})")

# Calcular economia vs Sonnet
total_custo_sonnet = sum([(r[1]['tokens_in'] / 1_000_000 * 3.00) + 
                           (r[1]['tokens_out'] / 1_000_000 * 15.00) 
                           for r in resultados if r[1]])
economia_total = total_custo_sonnet - total_custo_haiku
economia_pct_total = (economia_total / total_custo_sonnet) * 100 if total_custo_sonnet > 0 else 0

print(f"Custo total com Sonnet: ${total_custo_sonnet:.6f} (~R$ {total_custo_sonnet * 5.5:.4f})")
print(f"💰 ECONOMIA TOTAL: ${economia_total:.6f} ({economia_pct_total:.1f}%) 🎉")

# ============================================
# DICAS DE ECONOMIA
# ============================================
print("\n" + "=" * 80)
print("💡 DICAS PARA ECONOMIZAR AINDA MAIS")
print("=" * 80)
print("""
1. ✅ Use Claude 3.5 Haiku → 73% mais barato que Sonnet
2. ✅ Reduza max_tokens → Menos tokens = Menos custo
3. ✅ Prompts concisos → Evite textos longos desnecessários
4. ✅ Cache respostas → Perguntas repetidas = Custo zero
5. ✅ System prompts claros → Respostas diretas, menos tokens
6. ✅ Amazon Nova Micro → 99% mais barato (para casos simples)

🎯 Para este caso (e-commerce), Haiku é IDEAL:
   - Respostas rápidas e concisas
   - Custo 73% menor que Sonnet 4.5
   - Qualidade suficiente para descrições de produtos
""")