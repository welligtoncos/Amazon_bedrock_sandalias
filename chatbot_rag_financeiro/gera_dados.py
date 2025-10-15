#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar banco de dados SQLite mockado
Simula estrutura de Data Lake (Athena/S3) local
Baseado em: RSM + Pollvo - Dados Contábeis, Financeiros, Fiscais, Folha, Timesheet

Autor: RSM Projects
Data: 2025
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random
from decimal import Decimal

class DatabaseFinanceiroBuilder:
    """Construtor de database financeiro mockado"""
    
    def __init__(self, db_name='dados_financeiros.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
        # Configurações de dados
        self.empresas_rsm = [
            'RSM Brasil Ltda',
            'RSM Tech Solutions',
            'RSM Consultoria Empresarial',
            'RSM Auditoria'
        ]
        
        self.empresas_pollvo = [
            'Pollvo Digital Ltda',
            'Pollvo Labs',
            'Pollvo Innovation'
        ]
        
        self.centros_custo = [
            'Administrativo',
            'Comercial',
            'TI e Tecnologia',
            'Financeiro',
            'Recursos Humanos',
            'Operações',
            'Marketing',
            'Jurídico'
        ]
        
        self.departamentos = [
            'Contabilidade',
            'Auditoria',
            'Vendas',
            'Desenvolvimento',
            'Suporte Técnico',
            'Gestão de Projetos',
            'Compliance',
            'Relacionamento com Cliente'
        ]
        
        self.status_financeiro = [
            'Pago',
            'Pendente',
            'Vencido',
            'Em Análise',
            'Cancelado',
            'Renegociado'
        ]
        
        self.tipos_imposto = [
            'IRPJ',      # Imposto de Renda Pessoa Jurídica
            'CSLL',      # Contribuição Social sobre Lucro Líquido
            'PIS',       # Programa de Integração Social
            'COFINS',    # Contribuição para Financiamento da Seguridade Social
            'ISS',       # Imposto Sobre Serviços
            'INSS',      # Instituto Nacional do Seguro Social
            'ICMS',      # Imposto sobre Circulação de Mercadorias
            'IPI'        # Imposto sobre Produtos Industrializados
        ]
        
        self.clientes = [
            'Banco do Brasil S/A',
            'Petrobras S/A',
            'Vale S/A',
            'Itaú Unibanco',
            'Bradesco S/A',
            'Ambev S/A',
            'JBS S/A',
            'Natura & Co',
            'Magazine Luiza',
            'B3 S/A'
        ]
        
        self.projetos = [
            'Projeto Alpha - ERP',
            'Projeto Beta - CRM',
            'Projeto Gamma - BI',
            'Projeto Delta - Mobile',
            'Projeto Epsilon - Cloud',
            'Projeto Zeta - Security',
            'Projeto Eta - Integration',
            'Projeto Theta - Analytics'
        ]
    
    def conectar(self):
        """Cria conexão com banco"""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
            print(f"🗑️  Banco antigo '{self.db_name}' removido")
        
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"✅ Conexão estabelecida: {self.db_name}")
    
    def criar_tabelas(self):
        """Cria estrutura de tabelas"""
        print("\n" + "=" * 80)
        print("📊 CRIANDO ESTRUTURA DE TABELAS")
        print("=" * 80)
        
        # ============================================
        # RSM - CONTÁBIL
        # ============================================
        print("\n1️⃣  Criando: rsm_contabil_consolidado")
        self.cursor.execute('''
        CREATE TABLE rsm_contabil_consolidado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            centro_custo TEXT NOT NULL,
            receita REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            data DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Índices para performance
        self.cursor.execute('''
        CREATE INDEX idx_rsm_contabil_empresa ON rsm_contabil_consolidado(empresa)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_rsm_contabil_data ON rsm_contabil_consolidado(ano, mes)
        ''')
        
        # ============================================
        # POLLVO - CONTÁBIL
        # ============================================
        print("2️⃣  Criando: pollvo_contabil_consolidado")
        self.cursor.execute('''
        CREATE TABLE pollvo_contabil_consolidado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            centro_custo TEXT NOT NULL,
            receita REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            data DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE INDEX idx_pollvo_contabil_empresa ON pollvo_contabil_consolidado(empresa)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_pollvo_contabil_data ON pollvo_contabil_consolidado(ano, mes)
        ''')
        
        # ============================================
        # RSM - FINANCEIRO
        # ============================================
        print("3️⃣  Criando: rsm_financeiro_consolidado")
        self.cursor.execute('''
        CREATE TABLE rsm_financeiro_consolidado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            status TEXT NOT NULL,
            qtd INTEGER NOT NULL,
            total REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            data_vencimento DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE INDEX idx_rsm_financeiro_status ON rsm_financeiro_consolidado(status)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_rsm_financeiro_data ON rsm_financeiro_consolidado(ano, mes)
        ''')
        
        # ============================================
        # RSM - FISCAL
        # ============================================
        print("4️⃣  Criando: rsm_fiscal_consolidado")
        self.cursor.execute('''
        CREATE TABLE rsm_fiscal_consolidado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            tipo_imposto TEXT NOT NULL,
            imposto REAL NOT NULL,
            base_calculo REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            competencia DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE INDEX idx_rsm_fiscal_tipo ON rsm_fiscal_consolidado(tipo_imposto)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_rsm_fiscal_data ON rsm_fiscal_consolidado(ano, mes)
        ''')
        
        # ============================================
        # RSM - FOLHA
        # ============================================
        print("5️⃣  Criando: rsm_folha_consolidada")
        self.cursor.execute('''
        CREATE TABLE rsm_folha_consolidada (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa TEXT NOT NULL,
            departamento TEXT NOT NULL,
            funcionarios INTEGER NOT NULL,
            folha REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            competencia DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE INDEX idx_rsm_folha_depto ON rsm_folha_consolidada(departamento)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_rsm_folha_data ON rsm_folha_consolidada(ano, mes)
        ''')
        
        # ============================================
        # POLLVO - TIMESHEET
        # ============================================
        print("6️⃣  Criando: pollvo_timesheet")
        self.cursor.execute('''
        CREATE TABLE pollvo_timesheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projeto TEXT NOT NULL,
            cliente TEXT NOT NULL,
            receita_projeto REAL NOT NULL,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            competencia DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        self.cursor.execute('''
        CREATE INDEX idx_pollvo_timesheet_cliente ON pollvo_timesheet(cliente)
        ''')
        self.cursor.execute('''
        CREATE INDEX idx_pollvo_timesheet_data ON pollvo_timesheet(ano, mes)
        ''')
        
        print("\n✅ Estrutura de tabelas criada com sucesso!")
    
    def popular_dados(self):
        """Popula tabelas com dados mockados"""
        print("\n" + "=" * 80)
        print("📝 POPULANDO DADOS (últimos 18 meses)")
        print("=" * 80)
        
        data_base = datetime.now()
        registros_inseridos = {
            'rsm_contabil': 0,
            'pollvo_contabil': 0,
            'rsm_financeiro': 0,
            'rsm_fiscal': 0,
            'rsm_folha': 0,
            'pollvo_timesheet': 0
        }
        
        for i in range(18):  # 18 meses de dados
            mes_data = data_base - timedelta(days=30 * i)
            ano = mes_data.year
            mes = mes_data.month
            data_str = f"{ano}-{mes:02d}-01"
            
            # RSM CONTÁBIL
            for empresa in self.empresas_rsm:
                for cc in random.sample(self.centros_custo, random.randint(4, 6)):
                    receita = round(random.uniform(50000, 800000), 2)
                    self.cursor.execute('''
                    INSERT INTO rsm_contabil_consolidado 
                    (empresa, centro_custo, receita, ano, mes, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (empresa, cc, receita, ano, mes, data_str))
                    registros_inseridos['rsm_contabil'] += 1
            
            # POLLVO CONTÁBIL
            for empresa in self.empresas_pollvo:
                for cc in random.sample(self.centros_custo, random.randint(3, 5)):
                    receita = round(random.uniform(30000, 500000), 2)
                    self.cursor.execute('''
                    INSERT INTO pollvo_contabil_consolidado 
                    (empresa, centro_custo, receita, ano, mes, data)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (empresa, cc, receita, ano, mes, data_str))
                    registros_inseridos['pollvo_contabil'] += 1
            
            # RSM FINANCEIRO
            for empresa in self.empresas_rsm:
                for status in self.status_financeiro:
                    qtd = random.randint(5, 80)
                    total = round(random.uniform(10000, 350000), 2)
                    self.cursor.execute('''
                    INSERT INTO rsm_financeiro_consolidado 
                    (empresa, status, qtd, total, ano, mes, data_vencimento)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (empresa, status, qtd, total, ano, mes, data_str))
                    registros_inseridos['rsm_financeiro'] += 1
            
            # RSM FISCAL
            for empresa in self.empresas_rsm:
                for tipo in self.tipos_imposto:
                    imposto = round(random.uniform(8000, 150000), 2)
                    # Base de cálculo entre 1.8x e 2.5x o imposto
                    base = round(imposto * random.uniform(1.8, 2.5), 2)
                    self.cursor.execute('''
                    INSERT INTO rsm_fiscal_consolidado 
                    (empresa, tipo_imposto, imposto, base_calculo, ano, mes, competencia)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (empresa, tipo, imposto, base, ano, mes, data_str))
                    registros_inseridos['rsm_fiscal'] += 1
            
            # RSM FOLHA
            for empresa in self.empresas_rsm:
                for depto in self.departamentos:
                    funcionarios = random.randint(5, 85)
                    # Salário médio entre R$ 5.000 e R$ 18.000
                    folha = round(funcionarios * random.uniform(5000, 18000), 2)
                    self.cursor.execute('''
                    INSERT INTO rsm_folha_consolidada 
                    (empresa, departamento, funcionarios, folha, ano, mes, competencia)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (empresa, depto, funcionarios, folha, ano, mes, data_str))
                    registros_inseridos['rsm_folha'] += 1
            
            # POLLVO TIMESHEET
            for projeto in self.projetos:
                cliente = random.choice(self.clientes)
                receita = round(random.uniform(25000, 280000), 2)
                self.cursor.execute('''
                INSERT INTO pollvo_timesheet 
                (projeto, cliente, receita_projeto, ano, mes, competencia)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (projeto, cliente, receita, ano, mes, data_str))
                registros_inseridos['pollvo_timesheet'] += 1
        
        self.conn.commit()
        
        print("\n📊 Registros inseridos:")
        for tabela, count in registros_inseridos.items():
            print(f"   • {tabela:25} → {count:5} registros")
    
    def criar_views(self):
        """Cria views analíticas"""
        print("\n" + "=" * 80)
        print("👁️  CRIANDO VIEWS ANALÍTICAS")
        print("=" * 80)
        
        # ============================================
        # VIEW: CONTÁBIL CONSOLIDADO
        # ============================================
        print("\n1️⃣  Criando: contabil_consolidado")
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS contabil_consolidado AS
        SELECT
            empresa,
            centro_custo,
            receita AS credito,
            0.0 AS debito,
            ano,
            mes,
            data
        FROM rsm_contabil_consolidado
        UNION ALL
        SELECT
            empresa,
            centro_custo,
            receita AS credito,
            0.0 AS debito,
            ano,
            mes,
            data
        FROM pollvo_contabil_consolidado
        ''')
        
        # ============================================
        # VIEW: FINANCEIRO CONSOLIDADO
        # ============================================
        print("2️⃣  Criando: financeiro_consolidado")
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS financeiro_consolidado AS
        SELECT
            empresa,
            status,
            qtd AS quantidade,
            total AS valor,
            ano,
            mes,
            data_vencimento
        FROM rsm_financeiro_consolidado
        ''')
        
        # ============================================
        # VIEW: FISCAL CONSOLIDADO
        # ============================================
        print("3️⃣  Criando: fiscal_consolidado")
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS fiscal_consolidado AS
        SELECT
            empresa,
            tipo_imposto,
            imposto AS valor_a_recolher,
            base_calculo,
            ROUND((imposto / NULLIF(base_calculo, 0)) * 100, 2) AS aliquota_efetiva,
            ano,
            mes,
            competencia
        FROM rsm_fiscal_consolidado
        ''')
        
        # ============================================
        # VIEW: FOLHA CONSOLIDADA
        # ============================================
        print("4️⃣  Criando: folha_consolidada")
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS folha_consolidada AS
        SELECT
            empresa,
            departamento,
            funcionarios,
            folha,
            ROUND(folha / NULLIF(funcionarios, 0), 2) AS salario_medio,
            ano,
            mes,
            competencia
        FROM rsm_folha_consolidada
        ''')
        
        # ============================================
        # VIEW: RESUMO EXECUTIVO (nova!)
        # ============================================
        print("5️⃣  Criando: resumo_executivo")
        self.cursor.execute('''
        CREATE VIEW IF NOT EXISTS resumo_executivo AS
        SELECT
            ano,
            mes,
            (SELECT SUM(receita) FROM rsm_contabil_consolidado r 
             WHERE r.ano = c.ano AND r.mes = c.mes) AS receita_total_rsm,
            (SELECT SUM(receita) FROM pollvo_contabil_consolidado p 
             WHERE p.ano = c.ano AND p.mes = c.mes) AS receita_total_pollvo,
            (SELECT SUM(imposto) FROM rsm_fiscal_consolidado f 
             WHERE f.ano = c.ano AND f.mes = c.mes) AS impostos_total,
            (SELECT SUM(folha) FROM rsm_folha_consolidada fo 
             WHERE fo.ano = c.ano AND fo.mes = c.mes) AS folha_total,
            (SELECT SUM(funcionarios) FROM rsm_folha_consolidada fo2 
             WHERE fo2.ano = c.ano AND fo2.mes = c.mes) AS funcionarios_total
        FROM (
            SELECT DISTINCT ano, mes FROM rsm_contabil_consolidado
        ) c
        ORDER BY ano DESC, mes DESC
        ''')
        
        print("\n✅ Views criadas com sucesso!")
    
    def gerar_relatorios(self):
        """Gera relatórios de validação"""
        print("\n" + "=" * 80)
        print("📈 RELATÓRIOS DE VALIDAÇÃO")
        print("=" * 80)
        
        data_atual = datetime.now()
        
        # Receita por empresa
        print("\n💰 RECEITA POR EMPRESA (3 meses mais recentes):")
        self.cursor.execute('''
        SELECT empresa, 
               SUM(receita) as total,
               COUNT(*) as registros
        FROM rsm_contabil_consolidado
        WHERE ano >= ? AND mes >= ?
        GROUP BY empresa
        ORDER BY total DESC
        ''', (data_atual.year, max(1, data_atual.month - 2)))
        
        for row in self.cursor.fetchall():
            print(f"   {row[0]:30} → R$ {row[1]:>15,.2f} ({row[2]:3} registros)")
        
        # Impostos por tipo
        print("\n📊 IMPOSTOS POR TIPO (mês mais recente):")
        self.cursor.execute('''
        SELECT tipo_imposto, 
               SUM(imposto) as total
        FROM rsm_fiscal_consolidado
        WHERE ano = ? AND mes = ?
        GROUP BY tipo_imposto
        ORDER BY total DESC
        ''', (data_atual.year, data_atual.month))
        
        for row in self.cursor.fetchall():
            print(f"   {row[0]:15} → R$ {row[1]:>15,.2f}")
        
        # Status financeiro
        print("\n💳 STATUS FINANCEIRO (mês mais recente):")
        self.cursor.execute('''
        SELECT status, 
               SUM(qtd) as quantidade,
               SUM(total) as valor
        FROM rsm_financeiro_consolidado
        WHERE ano = ? AND mes = ?
        GROUP BY status
        ORDER BY valor DESC
        ''', (data_atual.year, data_atual.month))
        
        for row in self.cursor.fetchall():
            print(f"   {row[0]:20} → {row[1]:4} itens | R$ {row[2]:>12,.2f}")
        
        # Departamentos com mais funcionários
        print("\n👥 DEPARTAMENTOS (funcionários totais):")
        self.cursor.execute('''
        SELECT departamento, 
               SUM(funcionarios) as total_func,
               SUM(folha) as total_folha
        FROM rsm_folha_consolidada
        WHERE ano = ? AND mes = ?
        GROUP BY departamento
        ORDER BY total_func DESC
        LIMIT 5
        ''', (data_atual.year, data_atual.month))
        
        for row in self.cursor.fetchall():
            print(f"   {row[0]:30} → {row[1]:3} func | R$ {row[2]:>12,.2f}")
        
        # Top projetos Pollvo
        print("\n🚀 TOP PROJETOS POLLVO (últimos 3 meses):")
        self.cursor.execute('''
        SELECT projeto, 
               SUM(receita_projeto) as total
        FROM pollvo_timesheet
        WHERE ano >= ? AND mes >= ?
        GROUP BY projeto
        ORDER BY total DESC
        LIMIT 5
        ''', (data_atual.year, max(1, data_atual.month - 2)))
        
        for row in self.cursor.fetchall():
            print(f"   {row[0]:35} → R$ {row[1]:>12,.2f}")
    
    def estatisticas_finais(self):
        """Mostra estatísticas finais do banco"""
        print("\n" + "=" * 80)
        print("📊 ESTATÍSTICAS FINAIS DO BANCO")
        print("=" * 80)
        
        tabelas = [
            'rsm_contabil_consolidado',
            'pollvo_contabil_consolidado',
            'rsm_financeiro_consolidado',
            'rsm_fiscal_consolidado',
            'rsm_folha_consolidada',
            'pollvo_timesheet'
        ]
        
        total_registros = 0
        
        print("\n📋 Tabelas:")
        for tabela in tabelas:
            self.cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = self.cursor.fetchone()[0]
            total_registros += count
            print(f"   • {tabela:40} → {count:6} registros")
        
        print(f"\n   TOTAL: {total_registros:,} registros")
        
        # Tamanho do banco
        tamanho = os.path.getsize(self.db_name) / (1024 * 1024)
        print(f"\n💾 Tamanho do arquivo: {tamanho:.2f} MB")
        
        # Views
        self.cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='view' 
        ORDER BY name
        """)
        views = self.cursor.fetchall()
        
        print(f"\n👁️  Views criadas: {len(views)}")
        for view in views:
            print(f"   • {view[0]}")
        
        # Índices
        self.cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='index' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """)
        indices = self.cursor.fetchall()
        
        print(f"\n🔍 Índices criados: {len(indices)}")
        for idx in indices:
            print(f"   • {idx[0]}")
    
    def fechar(self):
        """Fecha conexão"""
        if self.conn:
            self.conn.close()
            print(f"\n✅ Conexão fechada")
    
    def executar(self):
        """Executa todo o processo de criação"""
        print("\n" + "=" * 80)
        print("🏗️  INICIANDO CRIAÇÃO DO BANCO DE DADOS FINANCEIRO")
        print("=" * 80)
        print(f"\n📁 Arquivo: {self.db_name}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        try:
            self.conectar()
            self.criar_tabelas()
            self.popular_dados()
            self.criar_views()
            self.gerar_relatorios()
            self.estatisticas_finais()
            
            print("\n" + "=" * 80)
            print("✅ BANCO DE DADOS CRIADO COM SUCESSO!")
            print("=" * 80)
            print(f"\n💾 Arquivo gerado: {self.db_name}")
            print(f"🎯 Pronto para uso com RAG!")
            print("\n🚀 Próximo passo: python chat_rag_financeiro.py")
            print("=" * 80 + "\n")
            
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            raise
        finally:
            self.fechar()

# ============================================
# EXECUÇÃO PRINCIPAL
# ============================================
if __name__ == "__main__":
    builder = DatabaseFinanceiroBuilder('dados_financeiros.db')
    builder.executar()