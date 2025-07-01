"""
ORCA INTERIORES SAAS - VERSÃO COMPLETA
Sistema de Orçamento Inteligente para Marcenaria
Versão: 3.0 Final
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import io
import base64

# Configuração da página
st.set_page_config(
    page_title="Orca Interiores | Orçamento Inteligente",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Premium
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -2rem -1rem 3rem -1rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-content {
        text-align: center;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    .premium-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        text-align: center;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# Importar módulos
try:
    from auth_manager import AuthManager
    from file_analyzer import FileAnalyzer
    from orcamento_engine import OrcamentoEngine
    from ai_analyzer import AIAnalyzer
    AUTH_DISPONIVEL = True
    IA_DISPONIVEL = True
except ImportError as e:
    st.error(f"Erro ao importar módulos: {e}")
    AUTH_DISPONIVEL = False
    IA_DISPONIVEL = False

def main():
    """Função principal da aplicação"""
    
    # Header Premium
    st.markdown("""
    <div class="header-container">
        <div class="header-content">
            <div class="header-title">🏠 Orca Interiores</div>
            <div class="header-subtitle">Orçamento Inteligente para Marcenaria • Powered by AI</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializar componentes
    if AUTH_DISPONIVEL:
        auth_manager = AuthManager()
        file_analyzer = FileAnalyzer()
        orcamento_engine = OrcamentoEngine()
        
        if IA_DISPONIVEL:
            ai_analyzer = AIAnalyzer()
            st.markdown('<div class="ai-badge">🤖 IA Ativada</div>', unsafe_allow_html=True)
    else:
        st.error("Sistema não disponível. Verifique a instalação.")
        return
    
    # Sistema de autenticação
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    
    if not st.session_state.usuario_logado:
        mostrar_login(auth_manager)
    else:
        mostrar_aplicacao_principal(auth_manager, file_analyzer, orcamento_engine, ai_analyzer if IA_DISPONIVEL else None)

def mostrar_login(auth_manager):
    """Tela de login limpa"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h2 style="text-align: center; color: #667eea; margin-bottom: 2rem;">
                🔐 Acesso Profissional
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### 📧 Email")
            email = st.text_input("", placeholder="seu@email.com", label_visibility="collapsed")
            
            st.markdown("### 🔑 Senha")
            senha = st.text_input("", type="password", placeholder="Sua senha", label_visibility="collapsed")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_btn = st.form_submit_button("🚀 Entrar", use_container_width=True)
            
            with col_btn2:
                demo_btn = st.form_submit_button("🎯 Conta Demo", use_container_width=True)
        
        if login_btn and email and senha:
            usuario = auth_manager.fazer_login(email, senha)
            if usuario:
                st.session_state.usuario_logado = usuario
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("❌ Email ou senha incorretos")
        
        if demo_btn:
            usuario = auth_manager.fazer_login("demo@orcainteriores.com", "demo123")
            if usuario:
                st.session_state.usuario_logado = usuario
                st.success("✅ Acesso demo ativado!")
                st.rerun()

def mostrar_aplicacao_principal(auth_manager, file_analyzer, orcamento_engine, ai_analyzer):
    """Interface principal da aplicação"""
    
    usuario = st.session_state.usuario_logado
    
    # Header do usuário
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%); 
                    padding: 1rem; border-radius: 12px; margin-bottom: 2rem;">
            <h3 style="margin: 0; color: #667eea;">👋 Olá, {usuario['nome']}</h3>
            <p style="margin: 0; color: #6b7280;">Plano: {usuario['plano'].title()} • 
               Orçamentos: {usuario['orcamentos_usados']}/{usuario['limite_orcamentos']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.usuario_logado = None
            st.rerun()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Análise", "📊 Resultados", "⚙️ Configurações", "📖 Ajuda"])
    
    with tab1:
        mostrar_upload(file_analyzer, ai_analyzer)
    
    with tab2:
        if 'analise' in st.session_state and st.session_state.analise:
            mostrar_resultados(st.session_state.analise, orcamento_engine)
        else:
            st.markdown("""
            <div class="premium-card">
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; color: #667eea; margin-bottom: 1rem;">📊</div>
                    <h3 style="color: #667eea;">Nenhuma análise disponível</h3>
                    <p style="color: #6b7280;">Faça upload de um arquivo 3D na aba "Upload & Análise"</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        mostrar_configuracoes()
    
    with tab4:
        mostrar_ajuda()

def mostrar_upload(file_analyzer, ai_analyzer):
    """Interface de upload"""
    
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #667eea; margin-bottom: 1rem;">📤 Upload de Arquivo 3D</h2>
        <p style="color: #6b7280; margin-bottom: 2rem;">
            Faça upload do seu projeto de marcenaria em formato OBJ, DAE, STL ou PLY
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=['obj', 'dae', 'stl', 'ply'],
        help="Formatos suportados: OBJ, DAE, STL, PLY (máximo 500MB)",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f"""
        <div class="premium-card">
            <h4 style="color: #667eea;">📁 Arquivo Carregado</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="metric-container">
                    <div class="metric-value">{uploaded_file.name}</div>
                    <div class="metric-label">Nome do Arquivo</div>
                </div>
                <div class="metric-container">
                    <div class="metric-value">{uploaded_file.size / 1024 / 1024:.1f} MB</div>
                    <div class="metric-label">Tamanho</div>
                </div>
                <div class="metric-container">
                    <div class="metric-value">{uploaded_file.type}</div>
                    <div class="metric-label">Tipo</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Analisar com IA", use_container_width=True, type="primary"):
            with st.spinner("🤖 Analisando arquivo com IA..."):
                try:
                    arquivo_conteudo = uploaded_file.read()
                    
                    if ai_analyzer:
                        resultado = file_analyzer.analisar_arquivo_3d_com_ia(
                            arquivo_conteudo, 
                            uploaded_file.name,
                            ai_analyzer
                        )
                    else:
                        resultado = file_analyzer.analisar_arquivo_3d(arquivo_conteudo, uploaded_file.name)
                    
                    if resultado and not resultado.get('erro'):
                        st.session_state.analise = resultado
                        st.success("✅ Análise concluída com sucesso!")
                        
                        if resultado.get('ia_ativa'):
                            st.markdown('<div class="status-success">🤖 IA Ativada - Análise Inteligente</div>', unsafe_allow_html=True)
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div class="metric-value">{resultado.get('total_componentes', 0)}</div>
                                <div class="metric-label">Componentes</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div class="metric-value">{resultado.get('area_total_m2', 0):.1f}m²</div>
                                <div class="metric-label">Área Total</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            if resultado.get('ia_estatisticas'):
                                marcenaria = resultado['ia_estatisticas'].get('marcenaria', 0)
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{marcenaria}</div>
                                    <div class="metric-label">Móveis Detectados</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col4:
                            if resultado.get('ia_estatisticas'):
                                confianca = resultado['ia_estatisticas'].get('confianca_media', 0)
                                st.markdown(f"""
                                <div class="metric-container">
                                    <div class="metric-value">{confianca:.0%}</div>
                                    <div class="metric-label">Confiança IA</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.info("📊 Vá para a aba 'Resultados' para ver a análise completa e gerar o orçamento!")
                        
                    else:
                        st.error(f"❌ Erro na análise: {resultado.get('erro', 'Erro desconhecido')}")
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar arquivo: {str(e)}")

def mostrar_resultados(analise, orcamento_engine):
    """Exibe resultados da análise"""
    
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #667eea; margin-bottom: 1rem;">📊 Resultados da Análise</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if analise.get('ia_ativa'):
        st.markdown('<div class="status-success">🤖 Análise realizada com IA Avançada</div>', unsafe_allow_html=True)
        
        if analise.get('ia_insights'):
            st.markdown("""
            <div class="premium-card">
                <h4 style="color: #667eea;">💡 Insights da IA</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for insight in analise['ia_insights']:
                st.info(insight)
        
        if analise.get('ia_recomendacoes'):
            st.markdown("""
            <div class="premium-card">
                <h4 style="color: #667eea;">🔧 Recomendações</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for rec in analise['ia_recomendacoes']:
                st.warning(rec)
    
    # Configurações de orçamento
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #667eea;">⚙️ Configurações do Orçamento</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        material = st.selectbox(
            "Material",
            ["mdf_15mm", "mdf_18mm", "compensado_15mm", "compensado_18mm", "melamina_15mm", "melamina_18mm"],
            format_func=lambda x: x.replace('_', ' ').title()
        )
    
    with col2:
        complexidade = st.selectbox(
            "Complexidade",
            ["simples", "media", "complexa", "premium"]
        )
    
    with col3:
        qualidade = st.selectbox(
            "Qualidade Acessórios",
            ["comum", "premium"]
        )
    
    with col4:
        margem = st.slider("Margem de Lucro (%)", 10, 50, 25)
    
    if st.button("💰 Gerar Orçamento Calibrado", use_container_width=True, type="primary"):
        with st.spinner("💰 Calculando orçamento..."):
            configuracoes = {
                'material': material,
                'complexidade': complexidade,
                'qualidade_acessorios': qualidade,
                'margem_lucro': margem
            }
            
            orcamento = orcamento_engine.calcular_orcamento_completo(analise, configuracoes)
            
            if orcamento:
                st.session_state.orcamento = orcamento
                mostrar_orcamento(orcamento, orcamento_engine)
            else:
                st.error("❌ Erro ao gerar orçamento")

def mostrar_orcamento(orcamento, orcamento_engine):
    """Exibe orçamento detalhado"""
    
    resumo = orcamento.get('resumo', {})
    
    st.markdown(f"""
    <div class="premium-card">
        <div style="text-align: center;">
            <h2 style="color: #667eea; margin-bottom: 0.5rem;">💰 Orçamento Final</h2>
            <div style="font-size: 3rem; font-weight: 700; color: #10b981; margin: 1rem 0;">
                R$ {resumo.get('valor_final', 0):,.2f}
            </div>
            <p style="color: #6b7280; font-size: 1.1rem;">
                {resumo.get('area_total_m2', 0):.1f}m² • R$ {resumo.get('preco_por_m2', 0):,.2f}/m²
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">R$ {resumo.get('custo_material', 0):,.0f}</div>
            <div class="metric-label">Material</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">R$ {resumo.get('custo_paineis_extras', 0):,.0f}</div>
            <div class="metric-label">Painéis Extras</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">R$ {resumo.get('custo_montagem', 0):,.0f}</div>
            <div class="metric-label">Montagem</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">R$ {resumo.get('valor_lucro', 0):,.0f}</div>
            <div class="metric-label">Margem</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos
    if orcamento.get('componentes'):
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: #667eea;">📈 Análise Visual</h4>
        </div>
        """, unsafe_allow_html=True)
        
        graficos = orcamento_engine.gerar_graficos(orcamento)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if graficos.get('pizza'):
                st.plotly_chart(graficos['pizza'], use_container_width=True)
        
        with col2:
            if graficos.get('barras'):
                st.plotly_chart(graficos['barras'], use_container_width=True)
    
    # Componentes detalhados
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #667eea;">🔍 Componentes Detalhados</h4>
    </div>
    """, unsafe_allow_html=True)
    
    for i, comp in enumerate(orcamento.get('componentes', [])):
        with st.expander(f"📦 {comp.get('nome', f'Componente {i+1}')} - R$ {comp.get('custo_total', 0):,.2f}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Tipo:** {comp.get('tipo', 'N/A').title()}")
                st.write(f"**Área:** {comp.get('area_m2', 0):.2f} m²")
                st.write(f"**Preço/m²:** R$ {comp.get('preco_por_m2', 0):,.2f}")
            
            with col2:
                if comp.get('ia_tipo_detectado'):
                    st.write(f"**🤖 IA Detectou:** {comp['ia_tipo_detectado']}")
                    st.write(f"**🎯 Confiança:** {comp.get('ia_confianca', 0):.1%}")
    
    if st.button("📄 Gerar Relatório", use_container_width=True):
        relatorio = orcamento_engine.gerar_relatorio_detalhado(orcamento)
        
        st.download_button(
            label="📥 Download Relatório",
            data=relatorio,
            file_name=f"orcamento_orca_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

def mostrar_configuracoes():
    """Configurações da aplicação"""
    
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #667eea; margin-bottom: 1rem;">⚙️ Configurações</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #667eea;">💰 Preços Base (Calibrados)</h4>
        <p style="color: #6b7280;">Preços baseados em análise de orçamentos reais de fábricas</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**MDF 15mm:** R$ 200,00/m²")
        st.info("**MDF 18mm:** R$ 220,00/m²")
        st.info("**Compensado 15mm:** R$ 180,00/m²")
    
    with col2:
        st.info("**Compensado 18mm:** R$ 200,00/m²")
        st.info("**Melamina 15mm:** R$ 240,00/m²")
        st.info("**Melamina 18mm:** R$ 260,00/m²")

def mostrar_ajuda():
    """Ajuda e documentação"""
    
    st.markdown("""
    <div class="premium-card">
        <h2 style="color: #667eea; margin-bottom: 1rem;">📖 Como Usar</h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: #667eea;">🚀 Passo a Passo</h4>
        
        <div style="margin: 1rem 0;">
            <strong>1. Preparar Arquivo no SketchUp</strong>
            <ul>
                <li>Manter apenas móveis de marcenaria</li>
                <li>Remover paredes, pisos, eletrodomésticos</li>
                <li>Usar nomes descritivos (ex: "Armario_Superior_Cozinha")</li>
                <li>Exportar em formato OBJ ou DAE</li>
            </ul>
        </div>
        
        <div style="margin: 1rem 0;">
            <strong>2. Upload e Análise</strong>
            <ul>
                <li>Fazer upload do arquivo 3D</li>
                <li>Aguardar análise automática com IA</li>
                <li>Verificar componentes detectados</li>
            </ul>
        </div>
        
        <div style="margin: 1rem 0;">
            <strong>3. Configurar Orçamento</strong>
            <ul>
                <li>Escolher material (MDF, compensado, melamina)</li>
                <li>Definir complexidade do projeto</li>
                <li>Ajustar margem de lucro</li>
            </ul>
        </div>
        
        <div style="margin: 1rem 0;">
            <strong>4. Gerar Relatório</strong>
            <ul>
                <li>Revisar orçamento detalhado</li>
                <li>Exportar relatório</li>
                <li>Enviar para cliente</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

