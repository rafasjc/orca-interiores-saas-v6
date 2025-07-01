"""
Engine de Orçamento - Orca Interiores
Sistema calibrado com preços reais de fábrica
Versão: 3.0 Final Calibrada
"""

import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Optional

class OrcamentoEngine:
    """Engine de cálculo de orçamentos calibrado"""
    
    def __init__(self):
        """Inicializa o engine com preços calibrados"""
        
        # Preços base calibrados (baseados em orçamento real de R$ 9.327)
        self.precos_materiais = {
            'mdf_15mm': 320.00,      # +60% vs original
            'mdf_18mm': 350.00,      # +59% vs original  
            'compensado_15mm': 280.00, # +56% vs original
            'compensado_18mm': 310.00, # +55% vs original
            'melamina_15mm': 380.00,   # +58% vs original
            'melamina_18mm': 410.00    # +58% vs original
        }
        
        # Multiplicadores por tipo de móvel (calibrados)
        self.multiplicadores_tipo = {
            'armario': 1.0,        # Base
            'despenseiro': 1.9,    # Reduzido de 2.2x
            'balcao': 1.4,         # Reduzido de 1.6x
            'gaveteiro': 1.7,      # Reduzido de 2.0x
            'prateleira': 0.8,     # Mantido
            'porta': 1.2,          # Reduzido de 1.4x
            'gaveta': 1.5          # Reduzido de 1.8x
        }
        
        # Multiplicadores por complexidade (calibrados)
        self.multiplicadores_complexidade = {
            'simples': 1.0,
            'media': 1.2,          # Reduzido de 1.3x
            'complexa': 1.4,       # Reduzido de 1.6x
            'premium': 1.7         # Reduzido de 2.0x
        }
        
        # Configurações calibradas
        self.config = {
            'fator_desperdicio': 0.08,      # Reduzido de 10% para 8%
            'percentual_paineis_extras': 0.20,  # Reduzido de 25% para 20%
            'percentual_montagem': 0.10,    # Reduzido de 12% para 10%
            'fator_calibracao_geral': 1.1,  # Reduzido de 1.3x para 1.1x
            'custo_acessorios_por_m2': {
                'comum': 25.00,             # Reduzido de 30
                'premium': 40.00            # Reduzido de 45
            }
        }
    
    def calcular_orcamento_completo(self, analise: Dict, configuracoes: Dict) -> Optional[Dict]:
        """Calcula orçamento completo calibrado"""
        
        try:
            componentes = analise.get('componentes', [])
            if not componentes:
                return None
            
            # Extrair configurações
            material = configuracoes.get('material', 'mdf_18mm')
            complexidade = configuracoes.get('complexidade', 'media')
            qualidade_acessorios = configuracoes.get('qualidade_acessorios', 'comum')
            margem_lucro = configuracoes.get('margem_lucro', 25) / 100
            
            # Calcular cada componente
            componentes_calculados = []
            custo_total_material = 0
            area_total = 0
            
            for comp in componentes:
                resultado_comp = self._calcular_componente(
                    comp, material, complexidade, qualidade_acessorios
                )
                
                if resultado_comp:
                    componentes_calculados.append(resultado_comp)
                    custo_total_material += resultado_comp['custo_total']
                    area_total += resultado_comp['area_m2']
            
            if not componentes_calculados:
                return None
            
            # Aplicar fator de calibração geral
            custo_total_material *= self.config['fator_calibracao_geral']
            
            # Calcular custos adicionais
            custo_paineis_extras = custo_total_material * self.config['percentual_paineis_extras']
            custo_montagem = custo_total_material * self.config['percentual_montagem']
            
            # Custo base total
            custo_base = custo_total_material + custo_paineis_extras + custo_montagem
            
            # Aplicar margem de lucro
            valor_lucro = custo_base * margem_lucro
            valor_final = custo_base + valor_lucro
            
            # Resumo
            resumo = {
                'valor_final': valor_final,
                'area_total_m2': area_total,
                'preco_por_m2': valor_final / area_total if area_total > 0 else 0,
                'custo_material': custo_total_material,
                'custo_paineis_extras': custo_paineis_extras,
                'custo_montagem': custo_montagem,
                'custo_base': custo_base,
                'valor_lucro': valor_lucro,
                'margem_lucro_pct': margem_lucro * 100
            }
            
            return {
                'resumo': resumo,
                'componentes': componentes_calculados,
                'configuracoes': configuracoes,
                'timestamp': datetime.now().isoformat(),
                'versao_engine': '3.0_calibrada'
            }
            
        except Exception as e:
            print(f"Erro no cálculo do orçamento: {e}")
            return None
    
    def _calcular_componente(self, componente: Dict, material: str, 
                           complexidade: str, qualidade_acessorios: str) -> Optional[Dict]:
        """Calcula custo de um componente individual"""
        
        try:
            area_m2 = componente.get('area_m2', 0)
            tipo = componente.get('tipo', 'armario')
            nome = componente.get('nome', 'Componente')
            
            if area_m2 <= 0:
                return None
            
            # Preço base do material
            preco_base_m2 = self.precos_materiais.get(material, self.precos_materiais['mdf_18mm'])
            
            # Aplicar multiplicador por tipo
            multiplicador_tipo = self.multiplicadores_tipo.get(tipo, 1.0)
            
            # Aplicar multiplicador por complexidade
            multiplicador_complexidade = self.multiplicadores_complexidade.get(complexidade, 1.0)
            
            # Calcular preço por m² final
            preco_por_m2 = preco_base_m2 * multiplicador_tipo * multiplicador_complexidade
            
            # Aplicar fator de desperdício
            area_com_desperdicio = area_m2 * (1 + self.config['fator_desperdicio'])
            
            # Custo do material
            custo_material = area_com_desperdicio * preco_por_m2
            
            # Custo dos acessórios
            custo_acessorios_m2 = self.config['custo_acessorios_por_m2'].get(qualidade_acessorios, 25.00)
            custo_acessorios = area_m2 * custo_acessorios_m2
            
            # Custo total do componente
            custo_total = custo_material + custo_acessorios
            
            return {
                'nome': nome,
                'tipo': tipo,
                'area_m2': area_m2,
                'preco_por_m2': preco_por_m2,
                'custo_material': custo_material,
                'custo_acessorios': custo_acessorios,
                'custo_total': custo_total,
                'multiplicador_tipo': multiplicador_tipo,
                'multiplicador_complexidade': multiplicador_complexidade,
                'material_usado': material,
                'qualidade_acessorios': qualidade_acessorios,
                # Dados da IA se disponíveis
                'ia_tipo_detectado': componente.get('ia_tipo_detectado'),
                'ia_confianca': componente.get('ia_confianca'),
                'ia_motivo': componente.get('ia_motivo')
            }
            
        except Exception as e:
            print(f"Erro no cálculo do componente: {e}")
            return None
    
    def gerar_graficos(self, orcamento: Dict) -> Dict:
        """Gera gráficos do orçamento"""
        
        try:
            resumo = orcamento.get('resumo', {})
            componentes = orcamento.get('componentes', [])
            
            graficos = {}
            
            # Gráfico de pizza - Distribuição de custos
            if resumo:
                labels = ['Material', 'Painéis Extras', 'Montagem', 'Margem']
                values = [
                    resumo.get('custo_material', 0),
                    resumo.get('custo_paineis_extras', 0),
                    resumo.get('custo_montagem', 0),
                    resumo.get('valor_lucro', 0)
                ]
                
                fig_pizza = px.pie(
                    values=values,
                    names=labels,
                    title="Distribuição de Custos",
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#f5576c']
                )
                
                fig_pizza.update_layout(
                    font=dict(size=12),
                    showlegend=True,
                    height=400
                )
                
                graficos['pizza'] = fig_pizza
            
            # Gráfico de barras - Custo por componente
            if componentes:
                nomes = [comp.get('nome', f"Item {i+1}")[:20] for i, comp in enumerate(componentes)]
                custos = [comp.get('custo_total', 0) for comp in componentes]
                
                fig_barras = go.Figure(data=[
                    go.Bar(
                        x=nomes,
                        y=custos,
                        marker_color='#667eea',
                        text=[f'R$ {custo:,.0f}' for custo in custos],
                        textposition='auto'
                    )
                ])
                
                fig_barras.update_layout(
                    title="Custo por Componente",
                    xaxis_title="Componentes",
                    yaxis_title="Custo (R$)",
                    font=dict(size=12),
                    height=400,
                    xaxis={'tickangle': 45}
                )
                
                graficos['barras'] = fig_barras
            
            return graficos
            
        except Exception as e:
            print(f"Erro ao gerar gráficos: {e}")
            return {}
    
    def gerar_relatorio_detalhado(self, orcamento: Dict) -> str:
        """Gera relatório detalhado em texto"""
        
        try:
            resumo = orcamento.get('resumo', {})
            componentes = orcamento.get('componentes', [])
            configuracoes = orcamento.get('configuracoes', {})
            timestamp = orcamento.get('timestamp', datetime.now().isoformat())
            
            relatorio = []
            relatorio.append("=" * 60)
            relatorio.append("ORÇAMENTO DETALHADO - ORCA INTERIORES")
            relatorio.append("Sistema Calibrado com Preços Reais de Fábrica")
            relatorio.append("=" * 60)
            relatorio.append("")
            
            # Cabeçalho
            relatorio.append(f"Data/Hora: {timestamp}")
            relatorio.append(f"Versão: {orcamento.get('versao_engine', '3.0')}")
            relatorio.append("")
            
            # Resumo Executivo
            relatorio.append("RESUMO EXECUTIVO")
            relatorio.append("-" * 20)
            relatorio.append(f"Valor Final: R$ {resumo.get('valor_final', 0):,.2f}")
            relatorio.append(f"Área Total: {resumo.get('area_total_m2', 0):.2f} m²")
            relatorio.append(f"Preço por m²: R$ {resumo.get('preco_por_m2', 0):,.2f}")
            relatorio.append(f"Total de Componentes: {len(componentes)}")
            relatorio.append("")
            
            # Configurações
            relatorio.append("CONFIGURAÇÕES APLICADAS")
            relatorio.append("-" * 25)
            relatorio.append(f"Material: {configuracoes.get('material', 'N/A').replace('_', ' ').title()}")
            relatorio.append(f"Complexidade: {configuracoes.get('complexidade', 'N/A').title()}")
            relatorio.append(f"Qualidade Acessórios: {configuracoes.get('qualidade_acessorios', 'N/A').title()}")
            relatorio.append(f"Margem de Lucro: {configuracoes.get('margem_lucro', 0)}%")
            relatorio.append("")
            
            # Breakdown de Custos
            relatorio.append("BREAKDOWN DE CUSTOS")
            relatorio.append("-" * 20)
            relatorio.append(f"Custo Material: R$ {resumo.get('custo_material', 0):,.2f}")
            relatorio.append(f"Painéis Extras: R$ {resumo.get('custo_paineis_extras', 0):,.2f}")
            relatorio.append(f"Montagem: R$ {resumo.get('custo_montagem', 0):,.2f}")
            relatorio.append(f"Subtotal: R$ {resumo.get('custo_base', 0):,.2f}")
            relatorio.append(f"Margem de Lucro: R$ {resumo.get('valor_lucro', 0):,.2f}")
            relatorio.append(f"TOTAL FINAL: R$ {resumo.get('valor_final', 0):,.2f}")
            relatorio.append("")
            
            # Componentes Detalhados
            relatorio.append("COMPONENTES DETALHADOS")
            relatorio.append("-" * 25)
            
            for i, comp in enumerate(componentes, 1):
                relatorio.append(f"{i}. {comp.get('nome', f'Componente {i}')}")
                relatorio.append(f"   Tipo: {comp.get('tipo', 'N/A').title()}")
                relatorio.append(f"   Área: {comp.get('area_m2', 0):.2f} m²")
                relatorio.append(f"   Preço/m²: R$ {comp.get('preco_por_m2', 0):,.2f}")
                relatorio.append(f"   Custo Material: R$ {comp.get('custo_material', 0):,.2f}")
                relatorio.append(f"   Custo Acessórios: R$ {comp.get('custo_acessorios', 0):,.2f}")
                relatorio.append(f"   Custo Total: R$ {comp.get('custo_total', 0):,.2f}")
                
                # Dados da IA se disponíveis
                if comp.get('ia_tipo_detectado'):
                    relatorio.append(f"   🤖 IA Detectou: {comp['ia_tipo_detectado']}")
                    relatorio.append(f"   🎯 Confiança: {comp.get('ia_confianca', 0):.1%}")
                
                relatorio.append("")
            
            # Observações
            relatorio.append("OBSERVAÇÕES")
            relatorio.append("-" * 12)
            relatorio.append("• Preços calibrados com base em orçamentos reais de fábrica")
            relatorio.append("• Inclui fator de desperdício de 8%")
            relatorio.append("• Painéis extras: 20% do valor base")
            relatorio.append("• Montagem: 10% do valor base")
            relatorio.append("• Valores sujeitos a variação conforme fornecedor")
            relatorio.append("")
            
            relatorio.append("=" * 60)
            relatorio.append("Gerado por Orca Interiores - Sistema de Orçamento Inteligente")
            relatorio.append("=" * 60)
            
            return "\n".join(relatorio)
            
        except Exception as e:
            return f"Erro ao gerar relatório: {str(e)}"

# Exemplo de uso
if __name__ == "__main__":
    engine = OrcamentoEngine()
    
    # Teste com dados simulados
    analise_teste = {
        'componentes': [
            {
                'nome': 'Armario_Superior_Teste',
                'tipo': 'armario',
                'area_m2': 1.5
            },
            {
                'nome': 'Balcao_Base_Teste',
                'tipo': 'balcao',
                'area_m2': 2.0
            }
        ]
    }
    
    configuracoes_teste = {
        'material': 'mdf_18mm',
        'complexidade': 'media',
        'qualidade_acessorios': 'comum',
        'margem_lucro': 25
    }
    
    orcamento = engine.calcular_orcamento_completo(analise_teste, configuracoes_teste)
    
    if orcamento:
        print(f"✅ Orçamento gerado: R$ {orcamento['resumo']['valor_final']:,.2f}")
        print(f"📊 Área total: {orcamento['resumo']['area_total_m2']:.1f}m²")
        print(f"💰 Preço/m²: R$ {orcamento['resumo']['preco_por_m2']:,.2f}")
        print("🎯 Engine calibrado funcionando!")
    else:
        print("❌ Erro ao gerar orçamento")

