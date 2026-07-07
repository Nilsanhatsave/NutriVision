import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="NutriVision - Plataforma Integrada",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.enfermeiro import render_enfermeiro
from dashboard.medico import render_medico
from dashboard.agronomo import render_agronomo

# ============ CREDENCIAIS DE ACESSO ============
USERS = {
    'enfermeiro': {
        'password': 'enfermeiro123',
        'perfil': 'Enfermeiro',
        'role': 'Triagem e Recolha'
    },
    'medico': {
        'password': 'medico123',
        'perfil': 'Médico',
        'role': 'Diagnóstico e Tratamento'
    },
    'agronomo': {
        'password': 'agronomo123',
        'perfil': 'Agrónomo',
        'role': 'Planeamento Agrícola e Lacunas'
    }
}

# ============ CSS ============
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    .login-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 450px;
        margin: 2rem auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(46, 125, 50, 0.15);
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 40%, #43A047 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
        letter-spacing: -1px;
    }
    
    .main-subheader {
        font-size: 1rem;
        font-weight: 400;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 0 2rem;
        line-height: 1.6;
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 1rem 2rem;
        border: 1px solid rgba(46, 125, 50, 0.1);
    }
    
    .login-title {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        color: #1B5E20;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        text-align: center;
        color: #666;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }
    
    .login-error {
        background: #FFEBEE;
        border-left: 4px solid #D32F2F;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        color: #C62828;
        margin-bottom: 1rem;
    }
    
    .sidebar-profile {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 2px solid #E8F5E9;
        margin-bottom: 1rem;
        background: rgba(255,255,255,0.85);
        border-radius: 12px;
        padding: 1.2rem;
    }
    .sidebar-profile .avatar { font-size: 4rem; display: block; margin-bottom: 0.5rem; }
    .sidebar-profile .name { font-weight: 700; font-size: 1.2rem; color: #1B5E20; }
    .sidebar-profile .role { color: #666; font-size: 0.85rem; background: #E8F5E9; padding: 0.2rem 1rem; border-radius: 20px; display: inline-block; }
    
    .footer {
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        color: #999;
        font-size: 0.85rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 2rem;
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 1rem;
    }
    .footer strong { color: #2E7D32; }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #2E7D32;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-nav {
        padding: 0.5rem 0;
    }
    .sidebar-nav .nav-item {
        padding: 0.6rem 1rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #333;
        text-decoration: none;
    }
    .sidebar-nav .nav-item:hover {
        background: #E8F5E9;
        color: #1B5E20;
    }
    .sidebar-nav .nav-item.active {
        background: #2E7D32;
        color: white;
    }
    
    .floating-logout {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        z-index: 1000;
        background: linear-gradient(145deg, #D32F2F, #B71C1C);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.8rem 1.8rem;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 20px rgba(211, 47, 47, 0.4);
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .floating-logout:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 30px rgba(211, 47, 47, 0.5);
    }
    
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
    }
    
    .download-btn {
        background: #2E7D32;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        cursor: pointer;
        font-weight: 600;
    }
    .download-btn:hover {
        background: #1B5E20;
    }
</style>
""", unsafe_allow_html=True)

# ============ FUNÇÕES DE NAVEGAÇÃO ============
def show_map():
    st.title("🗺️ Mapa de Prevalência")
    st.markdown("Distribuição geográfica dos casos de anemia, fome oculta e insegurança alimentar")
    
    # Dados simulados
    comunidades = ['Distrito A', 'Distrito B', 'Distrito C', 'Distrito D', 'Distrito E']
    anemia = np.random.randint(10, 60, 5)
    fome_oculta = np.random.randint(5, 50, 5)
    inseguranca = np.random.randint(10, 70, 5)
    
    df = pd.DataFrame({
        'Comunidade': comunidades,
        'Anemia (%)': anemia,
        'Fome Oculta (%)': fome_oculta,
        'Insegurança Alimentar (%)': inseguranca
    })
    
    st.dataframe(df, use_container_width=True)
    
    # Gráfico
    import plotly.express as px
    fig = px.bar(df, x='Comunidade', y=['Anemia (%)', 'Fome Oculta (%)', 'Insegurança Alimentar (%)'],
                 title='Prevalência por Comunidade', barmode='group')
    st.plotly_chart(fig, use_container_width=True)

def show_prescricoes():
    st.title("📋 Prescrições")
    st.markdown("Registo de prescrições médicas e suplementações")
    
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        prescricoes = df[['nome', 'idade_meses', 'anemia_risco', 'data_avaliacao']].copy()
        prescricoes['Prescrição'] = prescricoes['anemia_risco'].apply(
            lambda x: 'Suplementação de Ferro + Ácido Fólico' if x == 'ALTO' 
            else 'Suplementação de Ferro' if x == 'MÉDIO' 
            else 'Acompanhamento Regular'
        )
        st.dataframe(prescricoes, use_container_width=True)
    else:
        st.info("📋 Nenhuma prescrição registada")

def show_relatorio():
    st.title("📄 Relatório Mensal")
    st.markdown("Baixe o relatório mensal em PDF")
    
    # Dados do relatório
    total = len(st.session_state.patients) if 'patients' in st.session_state else 0
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        alto_risco = len(df[df['anemia_risco'] == 'ALTO'])
        medio_risco = len(df[df['anemia_risco'] == 'MÉDIO'])
        baixo_risco = len(df[df['anemia_risco'] == 'BAIXO'])
    else:
        alto_risco = medio_risco = baixo_risco = 0
    
    st.markdown(f"""
    <div class="section-card">
        <h4>📊 Resumo do Mês</h4>
        <p><strong>Total de Crianças Avaliadas:</strong> {total}</p>
        <p><strong>Risco ALTO:</strong> {alto_risco}</p>
        <p><strong>Risco MÉDIO:</strong> {medio_risco}</p>
        <p><strong>Risco BAIXO:</strong> {baixo_risco}</p>
        <p><strong>Data:</strong> {datetime.now().strftime('%B %Y')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📥 Baixar Relatório PDF", use_container_width=True):
        st.success("✅ Relatório gerado com sucesso! (Funcionalidade em desenvolvimento)")

def show_historico():
    st.title("📜 Histórico das Crianças")
    
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        st.dataframe(df[['nome', 'idade_meses', 'anemia_risco', 'nutrition_risco', 
                        'food_security_risco', 'diversidade_alimentar', 'data_avaliacao']], 
                    use_container_width=True)
    else:
        st.info("📋 Nenhum histórico disponível")

def show_dicas():
    st.title("💡 Dicas Nutricionais")
    
    dicas = [
        "🍽️ **Diversifique a alimentação:** Ofereça alimentos de todos os grupos alimentares diariamente",
        "🥩 **Aumente o consumo de ferro:** Inclua carnes, feijão, ovos e folhas verdes escuras",
        "🍊 **Vitamina C ajuda na absorção de ferro:** Combine alimentos ricos em ferro com frutas cítricas",
        "🥬 **Folhas verdes escuras são ricas em ferro:** Couve, espinafre, brócolos",
        "🥚 **Ovos são excelentes fontes de proteína e ferro:** Ofereça a gema e a clara",
        "🌽 **Cereais fortificados:** Dê preferência a cereais enriquecidos com ferro e vitaminas",
        "💧 **Água potável:** Garanta acesso a água limpa para prevenir doenças",
        "🍎 **Frutas e vegetais:** Ofereça 5 porções de frutas e vegetais por dia"
    ]
    
    for i, dica in enumerate(dicas):
        with st.expander(f"💡 Dica {i+1}"):
            st.markdown(dica)

def show_prevencao():
    st.title("🛡️ Recomendações de Prevenção de Anemia")
    
    st.markdown("""
    <div class="section-card">
        <h4>📋 Medidas de Prevenção</h4>
        <ul>
            <li><strong>Aleitamento Materno Exclusivo:</strong> Até os 6 meses de idade</li>
            <li><strong>Alimentação Complementar:</strong> A partir dos 6 meses com alimentos ricos em ferro</li>
            <li><strong>Suplementação:</strong> Administrar ferro e ácido fólico conforme orientação médica</li>
            <li><strong>Diversidade Alimentar:</strong> Oferecer pelo menos 4 grupos alimentares por dia</li>
            <li><strong>Higiene e Saneamento:</strong> Prevenir infecções que causam perda de ferro</li>
            <li><strong>Monitorização Regular:</strong> Acompanhar o crescimento e desenvolvimento</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_evolucao():
    st.title("📈 Evolução de Cada Paciente")
    
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        selected = st.selectbox("Selecionar Paciente", df['nome'].unique())
        
        patient_data = df[df['nome'] == selected].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Idade", f"{patient_data['idade_meses']} meses")
            st.metric("Peso", f"{patient_data['peso_kg']} kg")
        with col2:
            st.metric("MUAC", f"{patient_data['muac_mm']} mm")
            st.metric("Diversidade Alimentar", f"{patient_data['diversidade_alimentar']}/9")
        
        # Gráfico de evolução simulado
        import plotly.graph_objects as go
        meses = ['Mês 1', 'Mês 2', 'Mês 3', 'Mês 4', 'Mês 5', 'Atual']
        pesos = [patient_data['peso_kg'] - 0.8, patient_data['peso_kg'] - 0.5, 
                 patient_data['peso_kg'] - 0.3, patient_data['peso_kg'] - 0.1, 
                 patient_data['peso_kg'] + 0.1, patient_data['peso_kg']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=meses, y=pesos, mode='lines+markers', 
                                name='Peso (kg)', line=dict(color='#2E7D32', width=3)))
        fig.update_layout(title=f'Evolução do Peso - {selected}', height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📋 Nenhum paciente registado")

def show_desempenho():
    st.title("📊 Avaliar Desempenho do Modelo")
    
    # Métricas simuladas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 AUC-ROC", "0.85", "Bom")
        st.metric("📈 Sensibilidade", "82%", "Boa")
    with col2:
        st.metric("🎯 Especificidade", "79%", "Boa")
        st.metric("📊 Precisão", "78%", "Boa")
    with col3:
        st.metric("🎯 F1-Score", "0.80", "Bom")
        st.metric("📈 Acurácia", "80%", "Boa")
    
    st.markdown("""
    <div class="section-card">
        <h4>📋 Interpretação</h4>
        <ul>
            <li><strong>AUC-ROC 0.85:</strong> Bom poder de discriminação do modelo</li>
            <li><strong>Sensibilidade 82%:</strong> O modelo identifica corretamente 82% dos casos positivos</li>
            <li><strong>Especificidade 79%:</strong> O modelo identifica corretamente 79% dos casos negativos</li>
            <li><strong>F1-Score 0.80:</strong> Bom equilíbrio entre precisão e sensibilidade</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_ia_apoio():
    st.title("🤖 IA de Apoio à Classificação")
    st.markdown("A IA analisa os dados e classifica o risco automaticamente")
    
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        
        st.subheader("📊 Classificações da IA")
        
        # Mostrar classificações
        col1, col2, col3 = st.columns(3)
        with col1:
            alto = len(df[df['anemia_risco'] == 'ALTO'])
            st.metric("Risco ALTO", alto, "🔴")
        with col2:
            medio = len(df[df['anemia_risco'] == 'MÉDIO'])
            st.metric("Risco MÉDIO", medio, "🟡")
        with col3:
            baixo = len(df[df['anemia_risco'] == 'BAIXO'])
            st.metric("Risco BAIXO", baixo, "🟢")
        
        st.markdown("""
        <div class="section-card">
            <h4>🤖 Como a IA classifica</h4>
            <p>A IA analisa múltiplos fatores:</p>
            <ul>
                <li>📏 Dados antropométricos (peso, altura, MUAC)</li>
                <li>🍽️ Diversidade alimentar</li>
                <li>🥩 Consumo de alimentos ricos em ferro</li>
                <li>🏠 Fatores socioeconómicos</li>
                <li>🩺 Histórico de saúde</li>
            </ul>
            <p><strong>Modelo:</strong> XGBoost com 85% de acurácia</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("📋 Registe pacientes para a IA classificar")

def show_encaminhamento():
    st.title("🚨 Encaminhamento de Casos de Risco")
    
    if 'patients' in st.session_state and st.session_state.patients:
        df = pd.DataFrame(st.session_state.patients)
        casos_risco = df[df['anemia_risco'] == 'ALTO']
        
        if not casos_risco.empty:
            st.warning(f"⚠️ {len(casos_risco)} casos de risco ALTO necessitam de encaminhamento")
            
            for idx, row in casos_risco.iterrows():
                with st.expander(f"👶 {row['nome']} - {row['idade_meses']} meses"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Peso:** {row['peso_kg']} kg")
                        st.write(f"**MUAC:** {row['muac_mm']} mm")
                        st.write(f"**Diversidade:** {row['diversidade_alimentar']}/9")
                    with col2:
                        st.write(f"**Risco Anemia:** {row['anemia_risco']}")
                        st.write(f"**Risco Fome Oculta:** {row['nutrition_risco']}")
                        st.write(f"**Data:** {row['data_avaliacao']}")
                    
                    if st.button(f"📤 Encaminhar {row['nome']}", key=f"enc_{idx}"):
                        st.success(f"✅ {row['nome']} encaminhado para o médico!")
        else:
            st.success("✅ Nenhum caso de risco ALTO no momento")
    else:
        st.info("📋 Nenhum paciente registado")

# ============ FUNÇÃO DE LOGIN ============
def login_page():
    st.markdown('<p class="main-header">🌿 NutriVision</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="main-subheader">
        <strong>Plataforma Inteligente de Deteção Precoce da Anemia, Fome Oculta e Insegurança Alimentar</strong><br>
        para a Prevenção através de Intervenções Integradas nos Sistemas de Saúde e Agroalimentares
    </p>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container fade-in">', unsafe_allow_html=True)
        st.markdown('<p class="login-title">🔐 Login</p>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Insira as suas credenciais para aceder ao sistema</p>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("👤 Nome de Utilizador", placeholder="ex: enfermeiro")
            password = st.text_input("🔑 Senha", type="password", placeholder="Insira a sua senha")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                login_button = st.form_submit_button("🔓 Entrar", use_container_width=True, type="primary")
        
        if login_button:
            if username and password:
                if username in USERS:
                    if USERS[username]['password'] == password:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.perfil = USERS[username]['perfil']
                        st.session_state.role = USERS[username]['role']
                        st.rerun()
                    else:
                        st.markdown('<div class="login-error">❌ Senha incorreta! Tente novamente.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="login-error">❌ Utilizador não encontrado! Verifique o nome.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="login-error">⚠️ Por favor, preencha todos os campos.</div>', unsafe_allow_html=True)
        
        with st.expander("ℹ️ Credenciais de Acesso"):
            st.markdown("""
            | Perfil | Utilizador | Senha |
            |--------|------------|-------|
            | 👩🏾‍⚕️ Enfermeiro | `enfermeiro` | `enfermeiro123` |
            | 👨🏾‍⚕️ Médico | `medico` | `medico123` |
            | 👨🏾‍🌾 Agrónomo | `agronomo` | `agronomo123` |
            """)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem;color:#999;font-size:0.9rem;background:rgba(255,255,255,0.7);border-radius:12px;padding:1rem;">
            <p>🌱 <strong>One Health / Nexus</strong> · Saúde · Nutrição · Agricultura · Clima</p>
            <p style="font-size:0.8rem;color:#bbb;">v2.0 · Sistema de Apoio à Decisão</p>
        </div>
        """, unsafe_allow_html=True)

# ============ FUNÇÃO DE LOGOUT ============
def logout():
    for key in ['logged_in', 'username', 'perfil', 'role', 'page']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ============ FUNÇÃO PRINCIPAL ============
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        # Inicializar página
        if 'page' not in st.session_state:
            st.session_state.page = 'Dashboard'
        
        # Sidebar com navegação
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-profile">
                <span class="avatar">
                    {"👩🏾‍⚕️" if st.session_state.perfil == "Enfermeiro" else "👨🏾‍⚕️" if st.session_state.perfil == "Médico" else "👨🏾‍🌾"}
                </span>
                <div class="name">{st.session_state.perfil}</div>
                <span class="role">{st.session_state.role}</span>
                <div style="margin-top:0.5rem;font-size:0.8rem;color:#999;">
                    👤 @{st.session_state.username}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📌 Navegação")
            
            # Menu de navegação
            menu_items = {
                "🏠 Dashboard": "Dashboard",
                "🗺️ Mapa de Prevalência": "Mapa",
                "📋 Prescrições": "Prescrições",
                "📄 Relatório Mensal": "Relatório",
                "📜 Histórico": "Histórico",
                "💡 Dicas Nutricionais": "Dicas",
                "🛡️ Prevenção de Anemia": "Prevenção",
                "📈 Evolução": "Evolução",
                "📊 Desempenho": "Desempenho",
                "🤖 IA de Apoio": "IA",
                "🚨 Encaminhamentos": "Encaminhamentos"
            }
            
            for label, page in menu_items.items():
                if st.button(label, key=f"nav_{page}", use_container_width=True):
                    st.session_state.page = page
                    st.rerun()
            
            st.markdown("---")
            st.caption("📋 **Informações**")
            st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            st.caption("🌿 NutriVision v2.0")
            st.caption("🏥 One Health / Nexus")
            
            if st.button("🚪 Sair", use_container_width=True):
                logout()
        
        # ============ CONTEÚDO PRINCIPAL ============
        page = st.session_state.page
        
        if page == "Dashboard":
            if st.session_state.perfil == "Enfermeiro":
                render_enfermeiro()
            elif st.session_state.perfil == "Médico":
                render_medico()
            elif st.session_state.perfil == "Agrónomo":
                render_agronomo()
        elif page == "Mapa":
            show_map()
        elif page == "Prescrições":
            show_prescricoes()
        elif page == "Relatório":
            show_relatorio()
        elif page == "Histórico":
            show_historico()
        elif page == "Dicas":
            show_dicas()
        elif page == "Prevenção":
            show_prevencao()
        elif page == "Evolução":
            show_evolucao()
        elif page == "Desempenho":
            show_desempenho()
        elif page == "IA":
            show_ia_apoio()
        elif page == "Encaminhamentos":
            show_encaminhamento()
        
        # Footer
        st.markdown("""
        <div class="footer">
            <p>🌿 <strong>NutriVision</strong> · Plataforma Inteligente de Apoio à Decisão</p>
            <p>Saúde · Nutrição · Agricultura · Clima · <strong>One Health/Nexus</strong></p>
            <p style="font-size:0.75rem;color:#ccc;">v2.0 · Desenvolvido para fortalecer sistemas agroalimentares</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()