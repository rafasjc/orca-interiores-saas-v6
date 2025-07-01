"""
Sistema de IA para Análise de Móveis
Classificação automática e inteligente de componentes de marcenaria
Versão: 3.0 Final
"""

import re
import math
from typing import Dict, List, Tuple, Optional

class AIAnalyzer:
    """Sistema de IA para análise de móveis"""
    
    def __init__(self):
        """Inicializa o sistema de IA"""
        
        # Base de conhecimento de móveis
        self.knowledge_base = {
            'armario': {
                'palavras_chave': ['armario', 'cabinet', 'wardrobe', 'closet', 'guarda', 'superior', 'inferior'],
                'dimensoes_tipicas': {
                    'largura': (0.3, 1.2),  # 30cm a 120cm
                    'altura': (0.6, 2.4),   # 60cm a 240cm
                    'profundidade': (0.3, 0.6)  # 30cm a 60cm
                },
                'area_tipica': (0.18, 2.88),  # m²
                'proporcoes': {
                    'altura_largura': (0.5, 8.0),
                    'profundidade_largura': (0.25, 2.0)
                }
            },
            'despenseiro': {
                'palavras_chave': ['despenseiro', 'pantry', 'coluna', 'torre', 'alto', 'vertical'],
                'dimensoes_tipicas': {
                    'largura': (0.4, 0.8),
                    'altura': (1.8, 2.4),
                    'profundidade': (0.4, 0.6)
                },
                'area_tipica': (0.16, 1.92),
                'proporcoes': {
                    'altura_largura': (2.25, 6.0),
                    'profundidade_largura': (0.5, 1.5)
                }
            },
            'balcao': {
                'palavras_chave': ['balcao', 'counter', 'base', 'inferior', 'bancada', 'pia'],
                'dimensoes_tipicas': {
                    'largura': (0.4, 3.0),
                    'altura': (0.8, 0.95),
                    'profundidade': (0.5, 0.65)
                },
                'area_tipica': (0.2, 1.95),
                'proporcoes': {
                    'altura_largura': (0.27, 2.38),
                    'profundidade_largura': (0.17, 1.63)
                }
            },
            'gaveteiro': {
                'palavras_chave': ['gaveteiro', 'drawer', 'gaveta', 'chest', 'caixa'],
                'dimensoes_tipicas': {
                    'largura': (0.3, 0.8),
                    'altura': (0.6, 1.2),
                    'profundidade': (0.4, 0.6)
                },
                'area_tipica': (0.12, 0.96),
                'proporcoes': {
                    'altura_largura': (0.75, 4.0),
                    'profundidade_largura': (0.5, 2.0)
                }
            },
            'prateleira': {
                'palavras_chave': ['prateleira', 'shelf', 'estante', 'divider', 'divisoria'],
                'dimensoes_tipicas': {
                    'largura': (0.3, 1.5),
                    'altura': (0.02, 0.05),  # Muito fina
                    'profundidade': (0.25, 0.5)
                },
                'area_tipica': (0.075, 0.75),
                'proporcoes': {
                    'altura_largura': (0.013, 0.167),
                    'profundidade_largura': (0.17, 1.67)
                }
            },
            'porta': {
                'palavras_chave': ['porta', 'door', 'folha', 'leaf', 'frente'],
                'dimensoes_tipicas': {
                    'largura': (0.3, 0.8),
                    'altura': (0.6, 2.2),
                    'profundidade': (0.015, 0.025)  # Muito fina
                },
                'area_tipica': (0.18, 1.76),
                'proporcoes': {
                    'altura_largura': (0.75, 7.33),
                    'profundidade_largura': (0.019, 0.083)
                }
            }
        }
        
        # Elementos que devem ser filtrados
        self.elementos_nao_marcenaria = {
            'parede': ['wall', 'parede', 'muro', 'divisoria_alvenaria'],
            'piso': ['floor', 'piso', 'chao', 'pavimento'],
            'teto': ['ceiling', 'teto', 'forro', 'laje'],
            'eletrodomestico': ['geladeira', 'fogao', 'microondas', 'lava', 'seca', 'refrigerator', 'stove'],
            'estrutura': ['viga', 'pilar', 'coluna_estrutural', 'beam', 'column'],
            'decoracao': ['quadro', 'vaso', 'luminaria', 'lamp', 'decoration']
        }
    
    def analyze_component(self, componente: Dict) -> Dict:
        """Analisa um componente individual"""
        
        try:
            nome = componente.get('nome', '').lower()
            dimensoes = componente.get('dimensoes', {})
            area_m2 = componente.get('area_m2', 0)
            
            # Análise semântica (nome)
            resultado_semantico = self._analisar_semantica(nome)
            
            # Análise geométrica (dimensões)
            resultado_geometrico = self._analisar_geometria(dimensoes, area_m2)
            
            # Análise dimensional (base de conhecimento)
            resultado_dimensional = self._analisar_dimensoes(dimensoes, area_m2)
            
            # Combinar resultados
            resultado_final = self._combinar_analises(
                resultado_semantico,
                resultado_geometrico,
                resultado_dimensional,
                componente
            )
            
            return resultado_final
            
        except Exception as e:
            return {
                'tipo_detectado': 'erro',
                'confianca': 0.0,
                'motivo': f'Erro na análise: {str(e)}',
                'sugestoes': ['Verificar dados do componente'],
                'alternativas': []
            }
    
    def _analisar_semantica(self, nome: str) -> Dict:
        """Análise baseada no nome do componente"""
        
        # Verificar elementos não-marcenaria primeiro
        for categoria, palavras in self.elementos_nao_marcenaria.items():
            for palavra in palavras:
                if palavra in nome:
                    return {
                        'tipo': 'nao_marcenaria',
                        'confianca': 0.95,
                        'motivo': f'Nome contém "{palavra}" (categoria: {categoria})'
                    }
        
        # Verificar móveis de marcenaria
        melhor_match = None
        melhor_score = 0
        
        for tipo_movel, dados in self.knowledge_base.items():
            score = 0
            palavras_encontradas = []
            
            for palavra in dados['palavras_chave']:
                if palavra in nome:
                    score += 1
                    palavras_encontradas.append(palavra)
            
            if score > melhor_score:
                melhor_score = score
                melhor_match = {
                    'tipo': tipo_movel,
                    'confianca': min(0.9, score * 0.3),
                    'motivo': f'Nome contém palavras-chave: {palavras_encontradas}',
                    'palavras_encontradas': palavras_encontradas
                }
        
        if melhor_match:
            return melhor_match
        
        return {
            'tipo': 'indefinido',
            'confianca': 0.1,
            'motivo': 'Nome não contém palavras-chave reconhecidas'
        }
    
    def _analisar_geometria(self, dimensoes: Dict, area_m2: float) -> Dict:
        """Análise baseada em padrões geométricos"""
        
        if not dimensoes or area_m2 <= 0:
            return {
                'tipo': 'invalido',
                'confianca': 0.0,
                'motivo': 'Dimensões inválidas ou área zero'
            }
        
        largura = dimensoes.get('largura', 0)
        altura = dimensoes.get('altura', 0)
        profundidade = dimensoes.get('profundidade', 0)
        
        if largura <= 0 or altura <= 0 or profundidade <= 0:
            return {
                'tipo': 'invalido',
                'confianca': 0.0,
                'motivo': 'Uma ou mais dimensões são zero ou negativas'
            }
        
        # Calcular proporções
        proporcoes = {
            'altura_largura': altura / largura,
            'profundidade_largura': profundidade / largura,
            'area_volume': area_m2 / (largura * altura * profundidade)
        }
        
        # Detectar padrões específicos
        
        # Prateleira: muito fina em altura
        if altura < 0.06:  # Menos de 6cm
            return {
                'tipo': 'prateleira',
                'confianca': 0.85,
                'motivo': f'Muito fina (altura: {altura*100:.1f}cm)',
                'proporcoes': proporcoes
            }
        
        # Porta: muito fina em profundidade
        if profundidade < 0.03:  # Menos de 3cm
            return {
                'tipo': 'porta',
                'confianca': 0.8,
                'motivo': f'Muito fina (profundidade: {profundidade*100:.1f}cm)',
                'proporcoes': proporcoes
            }
        
        # Despenseiro: muito alto em relação à largura
        if proporcoes['altura_largura'] > 2.5:
            return {
                'tipo': 'despenseiro',
                'confianca': 0.75,
                'motivo': f'Proporção alta (altura/largura: {proporcoes["altura_largura"]:.1f})',
                'proporcoes': proporcoes
            }
        
        # Balcão: baixo e comprido
        if altura < 1.0 and largura > 1.0:
            return {
                'tipo': 'balcao',
                'confianca': 0.7,
                'motivo': f'Baixo e comprido (altura: {altura*100:.0f}cm, largura: {largura*100:.0f}cm)',
                'proporcoes': proporcoes
            }
        
        # Elemento muito grande (provavelmente parede/piso)
        if area_m2 > 10:
            return {
                'tipo': 'nao_marcenaria',
                'confianca': 0.9,
                'motivo': f'Área muito grande ({area_m2:.1f}m²) - provavelmente estrutura',
                'proporcoes': proporcoes
            }
        
        return {
            'tipo': 'armario',  # Padrão
            'confianca': 0.4,
            'motivo': 'Padrão geométrico de armário',
            'proporcoes': proporcoes
        }
    
    def _analisar_dimensoes(self, dimensoes: Dict, area_m2: float) -> Dict:
        """Análise baseada na base de conhecimento dimensional"""
        
        if not dimensoes:
            return {
                'tipo': 'indefinido',
                'confianca': 0.0,
                'motivo': 'Dimensões não disponíveis'
            }
        
        largura = dimensoes.get('largura', 0)
        altura = dimensoes.get('altura', 0)
        profundidade = dimensoes.get('profundidade', 0)
        
        melhor_match = None
        melhor_score = 0
        
        for tipo_movel, dados in self.knowledge_base.items():
            score = 0
            motivos = []
            
            # Verificar dimensões típicas
            dim_tipicas = dados['dimensoes_tipicas']
            
            if dim_tipicas['largura'][0] <= largura <= dim_tipicas['largura'][1]:
                score += 1
                motivos.append(f'largura compatível ({largura*100:.0f}cm)')
            
            if dim_tipicas['altura'][0] <= altura <= dim_tipicas['altura'][1]:
                score += 1
                motivos.append(f'altura compatível ({altura*100:.0f}cm)')
            
            if dim_tipicas['profundidade'][0] <= profundidade <= dim_tipicas['profundidade'][1]:
                score += 1
                motivos.append(f'profundidade compatível ({profundidade*100:.0f}cm)')
            
            # Verificar área típica
            area_tipica = dados['area_tipica']
            if area_tipica[0] <= area_m2 <= area_tipica[1]:
                score += 1
                motivos.append(f'área compatível ({area_m2:.2f}m²)')
            
            # Verificar proporções
            if altura > 0 and largura > 0:
                prop_altura_largura = altura / largura
                prop_range = dados['proporcoes']['altura_largura']
                if prop_range[0] <= prop_altura_largura <= prop_range[1]:
                    score += 1
                    motivos.append(f'proporção altura/largura compatível ({prop_altura_largura:.1f})')
            
            if profundidade > 0 and largura > 0:
                prop_prof_largura = profundidade / largura
                prop_range = dados['proporcoes']['profundidade_largura']
                if prop_range[0] <= prop_prof_largura <= prop_range[1]:
                    score += 1
                    motivos.append(f'proporção profundidade/largura compatível ({prop_prof_largura:.1f})')
            
            if score > melhor_score:
                melhor_score = score
                melhor_match = {
                    'tipo': tipo_movel,
                    'confianca': min(0.95, score * 0.15),
                    'motivo': f'Dimensões compatíveis: {", ".join(motivos)}',
                    'score_dimensional': score,
                    'motivos_detalhados': motivos
                }
        
        if melhor_match:
            return melhor_match
        
        return {
            'tipo': 'indefinido',
            'confianca': 0.2,
            'motivo': 'Dimensões não correspondem a nenhum tipo conhecido'
        }
    
    def _combinar_analises(self, semantico: Dict, geometrico: Dict, dimensional: Dict, componente: Dict) -> Dict:
        """Combina resultados das diferentes análises"""
        
        # Pesos para cada tipo de análise
        peso_semantico = 0.4
        peso_geometrico = 0.3
        peso_dimensional = 0.3
        
        # Se análise semântica detectou não-marcenaria com alta confiança
        if semantico['tipo'] == 'nao_marcenaria' and semantico['confianca'] > 0.8:
            return {
                'tipo_detectado': 'nao_marcenaria',
                'confianca': semantico['confianca'],
                'motivo': f'Análise semântica: {semantico["motivo"]}',
                'sugestoes': ['Remover este elemento do arquivo SketchUp'],
                'alternativas': [],
                'detalhes': {
                    'semantico': semantico,
                    'geometrico': geometrico,
                    'dimensional': dimensional
                }
            }
        
        # Se análise geométrica detectou elemento inválido
        if geometrico['tipo'] == 'invalido':
            return {
                'tipo_detectado': 'invalido',
                'confianca': 0.0,
                'motivo': f'Análise geométrica: {geometrico["motivo"]}',
                'sugestoes': ['Verificar geometria do componente'],
                'alternativas': [],
                'detalhes': {
                    'semantico': semantico,
                    'geometrico': geometrico,
                    'dimensional': dimensional
                }
            }
        
        # Combinar análises válidas
        candidatos = []
        
        if semantico['tipo'] not in ['nao_marcenaria', 'invalido', 'indefinido']:
            candidatos.append({
                'tipo': semantico['tipo'],
                'score': semantico['confianca'] * peso_semantico,
                'origem': 'semantica'
            })
        
        if geometrico['tipo'] not in ['nao_marcenaria', 'invalido', 'indefinido']:
            candidatos.append({
                'tipo': geometrico['tipo'],
                'score': geometrico['confianca'] * peso_geometrico,
                'origem': 'geometrica'
            })
        
        if dimensional['tipo'] not in ['nao_marcenaria', 'invalido', 'indefinido']:
            candidatos.append({
                'tipo': dimensional['tipo'],
                'score': dimensional['confianca'] * peso_dimensional,
                'origem': 'dimensional'
            })
        
        if not candidatos:
            return {
                'tipo_detectado': 'indefinido',
                'confianca': 0.1,
                'motivo': 'Nenhuma análise produziu resultado válido',
                'sugestoes': ['Verificar nome e dimensões do componente'],
                'alternativas': [],
                'detalhes': {
                    'semantico': semantico,
                    'geometrico': geometrico,
                    'dimensional': dimensional
                }
            }
        
        # Encontrar melhor candidato
        melhor_candidato = max(candidatos, key=lambda x: x['score'])
        
        # Calcular confiança final
        confianca_final = melhor_candidato['score']
        
        # Bonus se múltiplas análises concordam
        tipos_detectados = [c['tipo'] for c in candidatos]
        if len(set(tipos_detectados)) == 1:  # Todas concordam
            confianca_final = min(0.95, confianca_final * 1.3)
        
        # Gerar motivo combinado
        motivos = []
        if semantico['tipo'] == melhor_candidato['tipo']:
            motivos.append(f"Semântica: {semantico['motivo']}")
        if geometrico['tipo'] == melhor_candidato['tipo']:
            motivos.append(f"Geometria: {geometrico['motivo']}")
        if dimensional['tipo'] == melhor_candidato['tipo']:
            motivos.append(f"Dimensões: {dimensional['motivo']}")
        
        motivo_final = " | ".join(motivos) if motivos else f"Melhor match: {melhor_candidato['origem']}"
        
        # Gerar alternativas
        alternativas = [c['tipo'] for c in candidatos if c['tipo'] != melhor_candidato['tipo']]
        
        # Gerar sugestões
        sugestoes = []
        if confianca_final < 0.5:
            sugestoes.append('Baixa confiança - revisar manualmente')
        if semantico['tipo'] == 'indefinido':
            sugestoes.append('Usar nome mais descritivo no SketchUp')
        if dimensional['tipo'] == 'indefinido':
            sugestoes.append('Verificar se dimensões estão realistas')
        
        return {
            'tipo_detectado': melhor_candidato['tipo'],
            'confianca': confianca_final,
            'motivo': motivo_final,
            'sugestoes': sugestoes,
            'alternativas': alternativas,
            'detalhes': {
                'semantico': semantico,
                'geometrico': geometrico,
                'dimensional': dimensional,
                'candidatos': candidatos
            }
        }
    
    def analyze_batch(self, componentes: List[Dict]) -> Dict:
        """Análise em lote para insights gerais"""
        
        if not componentes:
            return {
                'estatisticas': {},
                'insights': ['Nenhum componente para analisar'],
                'recomendacoes': []
            }
        
        # Estatísticas gerais
        total_componentes = len(componentes)
        tipos_detectados = {}
        confiancas = []
        areas = []
        
        for comp in componentes:
            tipo = comp.get('ia_tipo_detectado', comp.get('tipo', 'indefinido'))
            tipos_detectados[tipo] = tipos_detectados.get(tipo, 0) + 1
            
            if comp.get('ia_confianca'):
                confiancas.append(comp['ia_confianca'])
            
            if comp.get('area_m2'):
                areas.append(comp['area_m2'])
        
        # Calcular métricas
        confianca_media = sum(confiancas) / len(confiancas) if confiancas else 0
        area_total = sum(areas)
        tipo_mais_comum = max(tipos_detectados.items(), key=lambda x: x[1])[0] if tipos_detectados else None
        
        # Estatísticas detalhadas
        estatisticas = {
            'total_componentes': total_componentes,
            'tipos_detectados': tipos_detectados,
            'confianca_media': confianca_media,
            'confianca_minima': min(confiancas) if confiancas else 0,
            'confianca_maxima': max(confiancas) if confiancas else 0,
            'area_total_m2': area_total,
            'area_media_m2': area_total / total_componentes if total_componentes > 0 else 0,
            'tipo_mais_comum': tipo_mais_comum,
            'diversidade_tipos': len(tipos_detectados),
            'marcenaria': sum(1 for comp in componentes if comp.get('ia_tipo_detectado', comp.get('tipo')) not in ['nao_marcenaria', 'invalido']),
            'nao_marcenaria': tipos_detectados.get('nao_marcenaria', 0),
            'invalidos': tipos_detectados.get('invalido', 0)
        }
        
        # Gerar insights
        insights = []
        
        if confianca_media > 0.8:
            insights.append(f"✅ Excelente qualidade: {confianca_media:.0%} de confiança média")
        elif confianca_media > 0.6:
            insights.append(f"👍 Boa qualidade: {confianca_media:.0%} de confiança média")
        else:
            insights.append(f"⚠️ Qualidade baixa: apenas {confianca_media:.0%} de confiança média")
        
        marcenaria_pct = estatisticas['marcenaria'] / total_componentes if total_componentes > 0 else 0
        if marcenaria_pct > 0.9:
            insights.append(f"🎯 Arquivo bem preparado: {marcenaria_pct:.0%} é marcenaria")
        elif marcenaria_pct > 0.7:
            insights.append(f"📊 Arquivo misto: {marcenaria_pct:.0%} é marcenaria")
        else:
            insights.append(f"⚠️ Muitos elementos não-marcenaria: apenas {marcenaria_pct:.0%} é marcenaria")
        
        if tipo_mais_comum:
            count = tipos_detectados[tipo_mais_comum]
            insights.append(f"📈 Tipo mais comum: {tipo_mais_comum.title()} ({count} ocorrências)")
        
        # Gerar recomendações
        recomendacoes = []
        
        if confianca_media < 0.6:
            recomendacoes.append("🔧 Melhorar preparação do arquivo 3D")
            recomendacoes.append("📝 Usar nomes mais descritivos nos objetos")
        
        if marcenaria_pct < 0.8:
            recomendacoes.append("🗑️ Remover elementos não-marcenaria do SketchUp")
            recomendacoes.append("🎯 Manter apenas móveis de marcenaria")
        
        if estatisticas['invalidos'] > 0:
            recomendacoes.append("📏 Verificar geometrias inválidas")
            recomendacoes.append("🔍 Revisar objetos indefinidos manualmente")
        
        if len(tipos_detectados) < 2:
            recomendacoes.append("📐 Verificar se todos os móveis foram modelados")
        
        return {
            'estatisticas': estatisticas,
            'insights': insights,
            'recomendacoes': recomendacoes
        }

# Exemplo de uso
if __name__ == "__main__":
    ai = AIAnalyzer()
    
    # Teste com componente exemplo
    componente_teste = {
        'nome': 'Armario_Superior_Cozinha',
        'dimensoes': {
            'largura': 0.8,
            'altura': 0.7,
            'profundidade': 0.35
        },
        'area_m2': 0.56
    }
    
    resultado = ai.analyze_component(componente_teste)
    print(f"🤖 IA detectou: {resultado['tipo_detectado']}")
    print(f"🎯 Confiança: {resultado['confianca']:.1%}")
    print(f"💡 Motivo: {resultado['motivo']}")
    print("✅ Sistema de IA funcionando!")

