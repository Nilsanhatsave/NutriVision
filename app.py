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
    initial_sidebar_state="collapsed"
)

from dashboard.enfermeiro import render_enfermeiro
from dashboard.medico import render_medico
from dashboard.agronomo import render_agronomo

# ============ CSS SEM IMAGENS ============
st.markdown("""
<style>
    /* Reset e base */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f5e9 100%);
    }
    
    /* ============ LOGIN ============ */
    .login-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 650px;
        margin: 1rem auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(46, 125, 50, 0.15);
        position: relative;
        z-index: 10;
    }
    
    /* ============ HEADER ============ */
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
    
    .main-subheader strong { color: #1B5E20; font-weight: 600; }
    
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
    
    .login-icon { font-size: 2.5rem; display: block; margin-bottom: 0.5rem; }
    
    /* ============ BOTÕES DE LOGIN ============ */
    .login-btn {
        background: linear-gradient(145deg, #2E7D32, #1B5E20) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3) !important;
        width: 100%;
        cursor: pointer;
    }
    .login-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(46, 125, 50, 0.4) !important;
    }
    .login-btn-enf { background: linear-gradient(145deg, #1565C0, #0D47A1) !important; box-shadow: 0 4px 15px rgba(21, 101, 192, 0.3) !important; }
    .login-btn-med { background: linear-gradient(145deg, #C62828, #B71C1C) !important; box-shadow: 0 4px 15px rgba(198, 40, 40, 0.3) !important; }
    .login-btn-agro { background: linear-gradient(145deg, #E65100, #BF360C) !important; box-shadow: 0 4px 15px rgba(230, 81, 0, 0.3) !important; }
    
    /* ============ BOTÃO FLUTUANTE DE LOGOUT ============ */
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
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .floating-logout:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 6px 30px rgba(211, 47, 47, 0.5);
    }
    
    /* ============ SIDEBAR ============ */
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
    
    /* ============ FOOTER ============ */
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
    
    /* ============ ANIMAÇÕES ============ */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in { animation: fadeInUp 0.6s ease forwards; }
    
    /* ============ CARDS ============ */
    .section-card, .result-container, .card {
        background: white !important;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid rgba(0,0,0,0.04);
    }
    
    /* ============ SCROLLBAR ============ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #2E7D32, #1B5E20);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #1B5E20;
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    st.markdown('<p class="main-header">🌿 NutriVision</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="main-subheader">
        <strong>Plataforma Inteligente de Deteção Precoce da Anemia, Fome Oculta e Insegurança Alimentar</strong><br>
        para a Prevenção através de Intervenções Integradas nos Sistemas de Saúde e Agroalimentares
    </p>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-container fade-in">', unsafe_allow_html=True)
        st.markdown('<p class="login-title">🔐 Acesso à Plataforma</p>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Selecione o seu perfil para aceder ao sistema</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div style="text-align:center"><span class="login-icon">👩🏾‍⚕️</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.8rem;color:#666;">Enfermeiro</p>', unsafe_allow_html=True)
            if st.button("Acessar", key="btn_enfermeiro", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.perfil = "Enfermeiro"
                st.rerun()
        
        with col2:
            st.markdown('<div style="text-align:center"><span class="login-icon">👨🏾‍⚕️</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.8rem;color:#666;">Médico</p>', unsafe_allow_html=True)
            if st.button("Acessar", key="btn_medico", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.perfil = "Médico"
                st.rerun()
        
        with col3:
            st.markdown('<div style="text-align:center"><span class="login-icon">👨🏾‍🌾</span></div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:0.8rem;color:#666;">Agrónomo</p>', unsafe_allow_html=True)
            if st.button("Acessar", key="btn_agronomo", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.perfil = "Agrónomo"
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem;color:#999;font-size:0.9rem;background:rgba(255,255,255,0.7);border-radius:12px;padding:1rem;">
            <p>🌱 <strong>One Health / Nexus</strong> · Saúde · Nutrição · Agricultura · Clima</p>
            <p style="font-size:0.8rem;color:#bbb;">v2.0 · Sistema de Apoio à Decisão</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # Botão flutuante de logout
        st.markdown(f"""
        <div style="position:fixed;bottom:2rem;right:2rem;z-index:1000;">
            <button onclick="document.getElementById('logout_btn').click()" 
                    style="background:linear-gradient(145deg,#D32F2F,#B71C1C);color:white;border:none;border-radius:50px;
                           padding:0.8rem 1.8rem;font-weight:600;font-size:0.95rem;
                           box-shadow:0 4px 20px rgba(211,47,47,0.4);cursor:pointer;transition:all 0.3s ease;
                           display:flex;align-items:center;gap:0.5rem;">
                🚪 Sair
            </button>
        </div>
        """, unsafe_allow_html=True)
        
        col_logout, col_logout2 = st.columns([10, 1])
        with col_logout2:
            if st.button("Sair", key="logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.perfil = None
                st.rerun()
        
        with st.sidebar:
            st.markdown(f"""
            <div class="sidebar-profile">
                <span class="avatar">
                    {"👩🏾‍⚕️" if st.session_state.perfil == "Enfermeiro" else "👨🏾‍⚕️" if st.session_state.perfil == "Médico" else "👨🏾‍🌾"}
                </span>
                <div class="name">{st.session_state.perfil}</div>
                <span class="role">
                    {"Triagem e Recolha" if st.session_state.perfil == "Enfermeiro" else 
                     "Diagnóstico e Tratamento" if st.session_state.perfil == "Médico" else 
                     "Planeamento Agrícola e Lacunas"}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.caption("📋 **Informações**")
            st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            st.caption("🌿 NutriVision v2.0")
            st.caption("🏥 One Health / Nexus")
        
        # Renderizar dashboard conforme perfil
        if st.session_state.perfil == "Enfermeiro":
            render_enfermeiro()
        elif st.session_state.perfil == "Médico":
            render_medico()
        elif st.session_state.perfil == "Agrónomo":
            render_agronomo()
        
        st.markdown("""
        <div class="footer">
            <p>🌿 <strong>NutriVision</strong> · Plataforma Inteligente de Apoio à Decisão</p>
            <p>Saúde · Nutrição · Agricultura · Clima · <strong>One Health/Nexus</strong></p>
            <p style="font-size:0.75rem;color:#ccc;">v2.0 · Desenvolvido para fortalecer sistemas agroalimentares</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()