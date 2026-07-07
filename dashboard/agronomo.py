import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.recommendation_engine import RecommendationEngine
from models.food_security_model import FoodSecurityModel

st.markdown("""
<style>
    .floating-actions {
        position: fixed;
        bottom: 6rem;
        right: 2rem;
        z-index: 999;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    .floating-btn {
        background: linear-gradient(145deg, #E65100, #BF360C);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(230, 81, 0, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .floating-btn:hover { transform: translateX(-5px); box-shadow: 0 6px 25px rgba(230, 81, 0, 0.4); }
    .floating-btn-secondary { background: linear-gradient(145deg, #2E7D32, #1B5E20); box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3); }
    .floating-btn-secondary:hover { box-shadow: 0 6px 25px rgba(46, 125, 50, 0.4); }
    
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #E65100;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #FFF3E0;
    }
    .request-box {
        background: #FFF3E0;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #E65100;
        margin: 0.5rem 0;
    }
    .request-box-responded {
        background: #E8F5E9;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }
    .badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-pendente { background: #FF9800; color: white; }
    .badge-respondido { background: #4CAF50; color: white; }
</style>
""", unsafe_allow_html=True)

def render_agronomo():
    st.markdown('<h1 style="font-size:2rem;font-weight:700;color:#E65100;">👨🏾‍🌾 Agrónomo - Planeamento Agrícola</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;color:#555;margin-bottom:1.5rem;">Analise lacunas nutricionais, receba pedidos do médico e planeie intervenções agrícolas</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="floating-actions">
        <button class="floating-btn" onclick="document.getElementById('pedidos').click()">📩 Pedidos Médicos</button>
        <button class="floating-btn floating-btn-secondary" onclick="document.getElementById('lacunas').click()">🥗 Ver Lacunas</button>
    </div>
    """, unsafe_allow_html=True)
    
    rec_engine = RecommendationEngine()
    food_security_model = FoodSecurityModel()
    
    # Inicializar pedidos agrícolas se não existir
    if 'agriculture_requests' not in st.session_state:
        st.session_state.agriculture_requests = []
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📩 Pedidos do Médico", "🥗 Lacunas Nutricionais", "🌱 Recomendações"])
    
    with tab1:
        st.header("📊 Perfil da Comunidade")
        
        if 'patients' in st.session_state and st.session_state.patients:
            df = pd.DataFrame(st.session_state.patients)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Crianças", len(df))
            with col2:
                risco_alto = len(df[df['anemia_risco'] == 'ALTO'])
                st.metric("Risco ALTO Anemia", risco_alto)
            with col3:
                baixa_diversidade = len(df[df['diversidade_alimentar'] < 4])
                st.metric("Baixa Diversidade", baixa_diversidade)
            with col4:
                media_div = df['diversidade_alimentar'].mean()
                st.metric("DDS Médio", f"{media_div:.1f}/9")
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                fig1 = px.pie(df, names='anemia_risco', title='Risco de Anemia', color_discrete_sequence=['#4CAF50', '#FF9800', '#F44336'])
                st.plotly_chart(fig1, use_container_width=True)
            with col_g2:
                fig2 = px.histogram(df, x='diversidade_alimentar', title='Diversidade Alimentar', nbins=9, color='anemia_risco')
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("📋 Aguardando dados de triagem do enfermeiro")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Prevalência Anemia", "40%", "⚠️ Elevada")
            with col2:
                st.metric("Insegurança Alimentar", "35%", "⚠️ Crítica")
            with col3:
                st.metric("Diversidade Agrícola", "4 culturas", "Ideal: 5+")
    
    with tab2:
        st.markdown('<div id="pedidos"></div>', unsafe_allow_html=True)
        st.header("📩 Pedidos do Médico")
        st.markdown("Responda aos pedidos de informação sobre produção agrícola familiar")
        
        if st.session_state.agriculture_requests:
            df_pedidos = pd.DataFrame(st.session_state.agriculture_requests)
            
            # Estatísticas
            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1:
                st.metric("Total de Pedidos", len(df_pedidos))
            with col_p2:
                pendentes = len(df_pedidos[df_pedidos['status'] == 'Pendente'])
                st.metric("Pendentes", pendentes, delta="⚠️" if pendentes > 0 else "✅")
            with col_p3:
                respondidos = len(df_pedidos[df_pedidos['status'] == 'Respondido'])
                st.metric("Respondidos", respondidos)
            
            st.divider()
            
            # Mostrar pedidos pendentes primeiro
            pendentes_df = df_pedidos[df_pedidos['status'] == 'Pendente']
            
            if not pendentes_df.empty:
                st.warning(f"⚠️ {len(pendentes_df)} pedidos aguardam resposta")
                
                for idx, row in pendentes_df.iterrows():
                    with st.expander(f"👶 {row['paciente']} - {row['idade']} meses - {row['data_pedido']}", expanded=True):
                        st.markdown(f"""
                        <div class="request-box">
                            <strong>📋 Informações do Pedido:</strong>
                            <ul>
                                <li><strong>Paciente:</strong> {row['paciente']}</li>
                                <li><strong>Idade:</strong> {row['idade']} meses</li>
                                <li><strong>Risco de Anemia:</strong> {row['risco_anemia']}</li>
                                <li><strong>Data do Pedido:</strong> {row['data_pedido']}</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a1, col_a2 = st.columns(2)
                        
                        with col_a1:
                            st.markdown(f"""
                            **🌱 Produção Atual:**
                            {row['culturas'] if row['culturas'] else 'Não informado'}
                            
                            **🐔 Animais:**
                            {row['animais'] if row['animais'] else 'Não informado'}
                            """)
                        
                        with col_a2:
                            st.markdown(f"""
                            **⚠️ Dificuldades:**
                            {row['dificuldades'] if row['dificuldades'] else 'Nenhuma'}
                            
                            **📝 Observações:**
                            {row['observacoes'] if row['observacoes'] else 'Nenhuma'}
                            """)
                        
                        # Recomendações do agrónomo
                        st.markdown("---")
                        st.markdown("**🌱 Recomendação Agrícola:**")
                        
                        recomendacao_agri = st.text_area(
                            f"Recomendação para {row['paciente']}:",
                            placeholder="Ex: Aumentar produção de feijão, introduzir hortícolas, melhorar criação de galinhas...",
                            key=f"agri_rec_{idx}",
                            height=80
                        )
                        
                        col_b1, col_b2 = st.columns(2)
                        with col_b1:
                            if st.button(f"✅ Enviar Recomendação", key=f"responder_{idx}", use_container_width=True):
                                if recomendacao_agri:
                                    st.session_state.agriculture_requests[idx]['status'] = 'Respondido'
                                    st.session_state.agriculture_requests[idx]['recomendacao'] = recomendacao_agri
                                    st.session_state.agriculture_requests[idx]['data_resposta'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                                    st.success(f"✅ Recomendação enviada para {row['paciente']}!")
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Por favor, insira uma recomendação")
                        
                        with col_b2:
                            if st.button(f"📋 Ver Dados do Paciente", key=f"ver_paciente_{idx}", use_container_width=True):
                                st.info(f"👶 {row['paciente']} - Consulte o histórico na aba Dashboard")
            else:
                st.success("✅ Nenhum pedido pendente")
            
            # Mostrar pedidos respondidos
            respondidos_df = df_pedidos[df_pedidos['status'] == 'Respondido']
            
            if not respondidos_df.empty:
                with st.expander("📋 Pedidos Respondidos"):
                    for idx, row in respondidos_df.iterrows():
                        st.markdown(f"""
                        <div class="request-box-responded">
                            <strong>✅ {row['paciente']}</strong> - {row['data_resposta']}
                            <br>
                            <span class="badge badge-respondido">Respondido</span>
                            <br><br>
                            <strong>🌱 Recomendação:</strong> {row['recomendacao']}
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("📋 Nenhum pedido do médico recebido ainda")
            st.markdown("""
            <div style="background:#f5f5f5;border-radius:8px;padding:1.5rem;text-align:center;border:1px dashed #ccc;">
                <span style="font-size:3rem;">📩</span>
                <p style="margin:0.5rem 0;color:#666;">
                    <strong>Aguardando pedidos</strong><br>
                    Os pedidos do médico aparecerão aqui automaticamente
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div id="lacunas"></div>', unsafe_allow_html=True)
        st.header("🥗 Análise de Lacunas Nutricionais")
        st.markdown("Identifique quais alimentos estão em falta na comunidade")
        
        if st.button("🔍 Analisar Lacunas Nutricionais", use_container_width=True):
            with st.spinner("A IA está a analisar os dados da comunidade..."):
                if 'patients' in st.session_state and st.session_state.patients:
                    df = pd.DataFrame(st.session_state.patients)
                    diversidade_media = df['diversidade_alimentar'].mean()
                    consumo_ferro = df['consumo_ferro'].mean() if 'consumo_ferro' in df.columns else 0.5
                    
                    patient_data = {
                        'diversidade_alimentar': diversidade_media,
                        'consumo_ferro': 1 if consumo_ferro > 0.5 else 0,
                        'consumo_vit_a': 0.5
                    }
                else:
                    patient_data = {'diversidade_alimentar': 3, 'consumo_ferro': 0, 'consumo_vit_a': 0}
                
                community_data = {
                    'producao_leguminosas': 8,
                    'producao_hortalicas': 15,
                    'diversidade_agricola': 4,
                    'producao_total': 1000,
                    'preco_alimentos': 50,
                    'precipitacao': 650,
                    'temperatura': 28,
                    'seca_frequencia': 1,
                    'duracao_epoca': 120
                }
                
                resultado = rec_engine.generate_lacuna_analysis(patient_data, community_data)
                
                st.subheader("📊 Resultado da Análise")
                
                col_l1, col_l2 = st.columns(2)
                
                with col_l1:
                    st.warning("⚠️ Lacunas Identificadas:")
                    if resultado['lacunas_identificadas']:
                        for lacuna in resultado['lacunas_identificadas']:
                            st.write(f"• {lacuna}")
                    else:
                        st.write("✅ Nenhuma lacuna crítica identificada")
                
                with col_l2:
                    st.success("🌱 Recomendações Agrícolas:")
                    if resultado['recomendacoes_agricolas']:
                        for rec in resultado['recomendacoes_agricolas']:
                            st.write(f"• {rec}")
                    else:
                        st.write("✅ Manter produção atual")
                
                st.metric(
                    "Nível de Prioridade",
                    resultado['nivel_prioridade'],
                    "Ação imediata necessária" if resultado['nivel_prioridade'] == 'ALTO' else "Planeamento a médio prazo"
                )
    
    with tab4:
        st.markdown('<div id="recomendacoes"></div>', unsafe_allow_html=True)
        st.header("🌱 Recomendações Agrícolas Integradas")
        st.markdown("Recomendações baseadas na análise integrada de dados de saúde, produção e clima")
        
        if st.button("🔄 Gerar Recomendações Integradas", use_container_width=True, type="primary"):
            with st.spinner("A IA está a analisar os dados integrados..."):
                if 'patients' in st.session_state and st.session_state.patients:
                    df = pd.DataFrame(st.session_state.patients)
                    
                    total = len(df)
                    risco_alto = len(df[df['anemia_risco'] == 'ALTO'])
                    baixa_diversidade = len(df[df['diversidade_alimentar'] < 4])
                    media_dds = df['diversidade_alimentar'].mean()
                    
                    recomendacoes = []
                    
                    if risco_alto > total * 0.3:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '🍖 Combate à Anemia',
                            'acao': 'Distribuir sementes de feijão e amendoim biofortificados para famílias com crianças em risco',
                            'prazo': 'Imediato'
                        })
                    
                    if baixa_diversidade > total * 0.4:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '🥬 Diversificação Alimentar',
                            'acao': 'Implementar hortas familiares com 5+ culturas (verduras, leguminosas, tubérculos)',
                            'prazo': 'Curto prazo (1-2 meses)'
                        })
                    
                    if media_dds < 4:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '📋 Educação Alimentar',
                            'acao': 'Promover campanhas de educação nutricional sobre diversidade alimentar',
                            'prazo': 'Imediato'
                        })
                    
                    if not recomendacoes:
                        recomendacoes.append({
                            'prioridade': 'BAIXA',
                            'categoria': '✅ Manutenção',
                            'acao': 'Manter as práticas agrícolas atuais, continuar monitorizando',
                            'prazo': 'Contínuo'
                        })
                    
                    st.subheader("📋 Recomendações Geradas")
                    
                    for rec in recomendacoes:
                        cor = "#D32F2F" if rec['prioridade'] == 'ALTA' else "#FF9800" if rec['prioridade'] == 'MÉDIA' else "#4CAF50"
                        st.markdown(f"""
                        <div style="background:white;border-radius:12px;padding:1rem;margin-bottom:0.8rem;
                                    border-left:5px solid {cor};box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <strong>{rec['categoria']}</strong>
                                <span style="background:{cor};color:white;padding:0.2rem 0.8rem;border-radius:20px;font-size:0.75rem;font-weight:600;">
                                    {rec['prioridade']}
                                </span>
                            </div>
                            <p style="margin:0.5rem 0;">{rec['acao']}</p>
                            <div style="display:flex;justify-content:space-between;font-size:0.85rem;color:#666;">
                                <span>⏱️ {rec['prazo']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Sem dados de pacientes para análise. Aguarde as triagens do enfermeiro.")