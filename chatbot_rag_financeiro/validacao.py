"""
Script para executar todas as queries SQL e gerar relatório
"""
import sqlite3
from datetime import datetime

def executar_validacao():
    conn = sqlite3.connect('dados_financeiros.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("VALIDACAO AUTOMATICA - 20 QUERIES SQL")
    print("=" * 80)
    print(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    testes = [
        ("01 - Receita Total", 
         "SELECT SUM(receita) FROM rsm_contabil_consolidado WHERE ano=2025 AND mes=10"),
        
        ("02 - Total Funcionarios",
         "SELECT SUM(funcionarios) FROM rsm_folha_consolidada WHERE ano=2025 AND mes=10"),
        
        ("03 - Tipos de Impostos",
         "SELECT COUNT(DISTINCT tipo_imposto) FROM rsm_fiscal_consolidado"),
        
        ("04 - IRPJ",
         "SELECT SUM(imposto) FROM rsm_fiscal_consolidado WHERE tipo_imposto='IRPJ' AND ano=2025 AND mes=10"),
        
        ("05 - Projeto Alpha",
         "SELECT SUM(receita_projeto) FROM pollvo_timesheet WHERE projeto LIKE '%Alpha%' AND ano=2025 AND mes=10"),
        
        ("06 - Receita RSM Brasil",
         "SELECT SUM(receita) FROM rsm_contabil_consolidado WHERE empresa LIKE '%RSM Brasil%' AND ano=2025 AND mes=10"),
        
        ("07 - Top 5 Impostos",
         "SELECT COUNT(*) FROM (SELECT tipo_imposto, SUM(imposto) as t FROM rsm_fiscal_consolidado WHERE ano=2025 AND mes=10 GROUP BY tipo_imposto ORDER BY t DESC LIMIT 5)"),
        
        ("08 - Funcionarios TI",
         "SELECT SUM(funcionarios) FROM rsm_folha_consolidada WHERE (LOWER(departamento) LIKE '%desenvolvimento%' OR LOWER(departamento) LIKE '%suporte%') AND ano=2025 AND mes=10"),
        
        ("09 - Contas Pendentes",
         "SELECT SUM(qtd), SUM(total) FROM rsm_financeiro_consolidado WHERE status='Pendente' AND ano=2025 AND mes=10"),
        
        ("10 - Projetos Petrobras",
         "SELECT COUNT(*), SUM(receita_projeto) FROM pollvo_timesheet WHERE cliente LIKE '%Petrobras%' AND ano=2025 AND mes=10"),
    ]
    
    resultados = []
    
    for nome, query in testes:
        try:
            cursor.execute(query)
            resultado = cursor.fetchone()
            resultados.append((nome, "OK", resultado))
            print(f"✅ {nome:30} → {resultado}")
        except Exception as e:
            resultados.append((nome, "ERRO", str(e)))
            print(f"❌ {nome:30} → ERRO: {e}")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"TOTAL: {len([r for r in resultados if r[1] == 'OK'])}/{len(testes)} queries executadas com sucesso")
    print("=" * 80)

if __name__ == "__main__":
    executar_validacao()