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
    .lacuna-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 5px solid #E65100;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .lacuna-card-alta { border-left-color: #D32F2F; }
    .lacuna-card-media { border-left-color: #FF9800; }
    .lacuna-card-baixa { border-left-color: #4CAF50; }
    .recomendacao-box {
        background: linear-gradient(145deg, #E8F5E9, #ffffff);
        border-radius: 12px;
        padding: 1.2rem;
        border: 2px solid #2E7D32;
    }
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
    .agri-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .agri-badge-alta { background: #F44336; color: white; }
    .agri-badge-media { background: #FF9800; color: white; }
    .agri-badge-baixa { background: #4CAF50; color: white; }
</style>
""", unsafe_allow_html=True)

def render_agronomo():
    st.markdown('<h1 style="font-size:2rem;font-weight:700;color:#E65100;">👨🏾‍🌾 Agrónomo - Planeamento Agrícola</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;color:#555;margin-bottom:1.5rem;">Analise lacunas nutricionais, registe dados agroalimentares e climáticos, e planeie intervenções</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="floating-actions">
        <button class="floating-btn" onclick="document.getElementById('ver_lacunas').click()">🥗 Ver Lacunas</button>
        <button class="floating-btn floating-btn-secondary" onclick="document.getElementById('recomendacoes').click()">🌱 Recomendações</button>
    </div>
    """, unsafe_allow_html=True)
    
    rec_engine = RecommendationEngine()
    food_security_model = FoodSecurityModel()
    
    # Inicializar dados agrícolas
    if 'agri_data' not in st.session_state:
        st.session_state.agri_data = {
            'producao_agricola': '',
            'diversidade_agricola': 0,
            'producao_leguminosas': 0,
            'producao_hortalicas': 0,
            'producao_graos': 0,
            'producao_tubers': 0,
            'producao_frutas': 0,
            'criacao_animal': '',
            'ovos_semana': 0,
            'leite_dia': 0,
            'disponibilidade_alimentos': '',
            'preco_feijao': 0,
            'preco_milho': 0,
            'preco_arroz': 0,
            'preco_oleo': 0,
            'sazonalidade': '',
            'meses_escassez': '',
            'precipitacao': 0,
            'temperatura': 0,
            'seca_frequencia': 0,
            'cheias_frequencia': 0,
            'epoca_agricola': 0,
            'data_registo': datetime.now().strftime('%d/%m/%Y %H:%M')
        }
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🌾 Dados Agroalimentares", "🥗 Verificação de Lacunas", "🌱 Recomendações"])
    
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
    
    with tab2:
        st.markdown('<div id="dados_agro"></div>', unsafe_allow_html=True)
        st.header("🌾 Registo de Dados Agroalimentares e Climáticos")
        st.markdown("Registe informações sobre produção, mercado e clima da comunidade")
        
        with st.form("agri_form"):
            # ============ PRODUÇÃO AGRÍCOLA ============
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🌱 Produção Agrícola</div>', unsafe_allow_html=True)
            
            col_prod1, col_prod2 = st.columns(2)
            with col_prod1:
                producao_agricola = st.text_area("Culturas produzidas (descreva)", placeholder="Ex: Milho, Feijão, Mandioca, Amendoim")
                diversidade_agricola = st.number_input("Número de culturas diferentes", min_value=0, max_value=20, value=4, step=1)
                producao_leguminosas = st.number_input("Produção de leguminosas (kg/mês)", min_value=0, value=50, step=10)
            with col_prod2:
                producao_hortalicas = st.number_input("Produção de hortícolas (kg/mês)", min_value=0, value=30, step=10)
                producao_graos = st.number_input("Produção de grãos (kg/mês)", min_value=0, value=100, step=10)
                producao_tubers = st.number_input("Produção de tubérculos (kg/mês)", min_value=0, value=80, step=10)
                producao_frutas = st.number_input("Produção de frutas (kg/mês)", min_value=0, value=20, step=10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ============ CRIAÇÃO ANIMAL ============
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🐔 Criação Animal</div>', unsafe_allow_html=True)
            
            col_anim1, col_anim2 = st.columns(2)
            with col_anim1:
                criacao_animal = st.text_area("Animais criados", placeholder="Ex: Galinhas, Cabras, Porcos")
                ovos_semana = st.number_input("Ovos produzidos por semana", min_value=0, value=20, step=5)
            with col_anim2:
                leite_dia = st.number_input("Litros de leite por dia", min_value=0.0, value=0.0, step=0.5)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ============ MERCADO E DISPONIBILIDADE ============
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💰 Mercado e Disponibilidade</div>', unsafe_allow_html=True)
            
            col_merc1, col_merc2 = st.columns(2)
            with col_merc1:
                disponibilidade_alimentos = st.selectbox("Disponibilidade geral de alimentos", ["Alta", "Média", "Baixa", "Muito baixa"])
                sazonalidade = st.selectbox("Sazonalidade de produção", ["Estável todo ano", "Duas estações", "Uma estação", "Muito variável"])
            with col_merc2:
                meses_escassez = st.text_input("Meses de maior escassez", placeholder="Ex: Jan-Mar, Out-Dez")
                preco_feijao = st.number_input("Preço do feijão (MZN/kg)", min_value=0, value=80, step=5)
                preco_milho = st.number_input("Preço do milho (MZN/kg)", min_value=0, value=50, step=5)
                preco_arroz = st.number_input("Preço do arroz (MZN/kg)", min_value=0, value=70, step=5)
                preco_oleo = st.number_input("Preço do óleo (MZN/litro)", min_value=0, value=120, step=5)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ============ DADOS CLIMÁTICOS ============
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🌦 Dados Climáticos</div>', unsafe_allow_html=True)
            
            col_clim1, col_clim2 = st.columns(2)
            with col_clim1:
                precipitacao = st.number_input("Precipitação anual (mm)", min_value=0, value=700, step=50)
                temperatura = st.number_input("Temperatura média (°C)", min_value=0, value=28, step=1)
            with col_clim2:
                seca_frequencia = st.number_input("Frequência de secas (eventos/ano)", min_value=0, value=1, step=1)
                cheias_frequencia = st.number_input("Frequência de cheias (eventos/ano)", min_value=0, value=0, step=1)
                epoca_agricola = st.number_input("Duração da época agrícola (dias)", min_value=0, value=120, step=10)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # ============ BOTÃO SALVAR ============
            salvar_agri = st.form_submit_button("💾 Salvar Dados Agroalimentares", use_container_width=True, type="primary")
            
            if salvar_agri:
                st.session_state.agri_data = {
                    'producao_agricola': producao_agricola,
                    'diversidade_agricola': diversidade_agricola,
                    'producao_leguminosas': producao_leguminosas,
                    'producao_hortalicas': producao_hortalicas,
                    'producao_graos': producao_graos,
                    'producao_tubers': producao_tubers,
                    'producao_frutas': producao_frutas,
                    'criacao_animal': criacao_animal,
                    'ovos_semana': ovos_semana,
                    'leite_dia': leite_dia,
                    'disponibilidade_alimentos': disponibilidade_alimentos,
                    'sazonalidade': sazonalidade,
                    'meses_escassez': meses_escassez,
                    'preco_feijao': preco_feijao,
                    'preco_milho': preco_milho,
                    'preco_arroz': preco_arroz,
                    'preco_oleo': preco_oleo,
                    'precipitacao': precipitacao,
                    'temperatura': temperatura,
                    'seca_frequencia': seca_frequencia,
                    'cheias_frequencia': cheias_frequencia,
                    'epoca_agricola': epoca_agricola,
                    'data_registo': datetime.now().strftime('%d/%m/%Y %H:%M')
                }
                st.success("✅ Dados agroalimentares registados com sucesso!")
    
    with tab3:
        st.markdown('<div id="ver_lacunas"></div>', unsafe_allow_html=True)
        st.header("🥗 Verificação de Lacunas Nutricionais")
        st.markdown("Analise os casos encaminhados e identifique lacunas na produção alimentar")
        
        if 'patients' in st.session_state and st.session_state.patients:
            df = pd.DataFrame(st.session_state.patients)
            
            casos_risco = df[(df['anemia_risco'].isin(['ALTO', 'MÉDIO'])) | 
                            (df['nutrition_risco'].isin(['ALTO', 'MÉDIO']))]
            
            if casos_risco.empty:
                st.success("✅ Nenhum caso com risco elevado no momento")
            else:
                st.warning(f"⚠️ {len(casos_risco)} casos necessitam de verificação agrícola")
                
                for idx, row in casos_risco.iterrows():
                    with st.expander(f"👶 {row['nome']} - {row['idade_meses']} meses - Risco: {row['anemia_risco']}"):
                        col_l1, col_l2 = st.columns(2)
                        
                        with col_l1:
                            st.markdown(f"""
                            **Dados da Criança:**
                            - **Idade:** {row['idade_meses']} meses
                            - **DDS:** {row['diversidade_alimentar']}/9
                            - **Consumo ferro:** {"Sim" if row['consumo_ferro'] else "Não"}
                            - **Refeições/dia:** {row.get('refeicoes_dia', 'N/A')}
                            - **Aleitamento:** {row.get('aleitamento', 'N/A')}
                            - **Risco Anemia:** {row['anemia_risco']}
                            - **Risco Fome Oculta:** {row['nutrition_risco']}
                            - **Déficits:** {', '.join(row.get('deficits', ['Nenhum']))}
                            """)
                        
                        with col_l2:
                            st.markdown(f"""
                            **Dados Socioeconómicos:**
                            - **Escolaridade mãe:** {row.get('escolaridade_mae', 'N/A')}
                            - **Tamanho família:** {row.get('tamanho_familia', 'N/A')}
                            - **Renda:** {row.get('renda', 'N/A')}
                            - **Água:** {row.get('agua', 'N/A')}
                            - **Saneamento:** {row.get('sani', 'N/A')}
                            """)
                        
                        # Análise de lacuna
                        st.markdown("---")
                        st.markdown("**🥗 Análise de Lacuna Nutricional:**")
                        
                        lacunas = []
                        if row['diversidade_alimentar'] < 4:
                            lacunas.append("⚠️ Baixa diversidade alimentar")
                        if row['consumo_ferro'] == 0:
                            lacunas.append("⚠️ Défice de ferro")
                        if row.get('refeicoes_dia', 0) < 3:
                            lacunas.append("⚠️ Baixa frequência de refeições")
                        
                        if lacunas:
                            for l in lacunas:
                                st.write(l)
                            
                            # Recomendações agrícolas específicas
                            st.markdown("**🌱 Recomendações Agrícolas Sugeridas:**")
                            
                            recomendacoes = []
                            if row['diversidade_alimentar'] < 4:
                                recomendacoes.append("• Diversificar produção agrícola (mínimo 5 culturas)")
                                recomendacoes.append("• Promover hortas familiares com variedade de vegetais")
                            if row['consumo_ferro'] == 0:
                                recomendacoes.append("• Aumentar produção de leguminosas (feijão, amendoim)")
                                recomendacoes.append("• Promover cultivo de folhas verdes escuras (couve, espinafre)")
                                recomendacoes.append("• Melhorar criação de galinhas para ovos")
                            
                            for r in recomendacoes:
                                st.write(r)
                            
                            # Campo para recomendações do agrónomo
                            recomendacao_agronomo = st.text_area(
                                "Registe a sua recomendação agrícola para este caso:",
                                placeholder="Ex: Distribuir sementes de feijão biofortificado para esta família...",
                                key=f"rec_{idx}"
                            )
                            
                            if st.button(f"✅ Registar Recomendação para {row['nome']}", key=f"btn_{idx}"):
                                if recomendacao_agronomo:
                                    # Atualizar paciente com recomendação
                                    for p in st.session_state.patients:
                                        if p['nome'] == row['nome']:
                                            p['recomendacao_agricola'] = recomendacao_agronomo
                                            p['status_agronomo'] = 'Analisado'
                                            break
                                    st.success(f"✅ Recomendação registada para {row['nome']}!")
                                    st.rerun()
                                else:
                                    st.warning("⚠️ Por favor, insira uma recomendação")
                        else:
                            st.success("✅ Nenhuma lacuna nutricional crítica identificada")
        else:
            st.info("📋 Aguardando dados de triagem do enfermeiro")
    
    with tab4:
        st.markdown('<div id="recomendacoes"></div>', unsafe_allow_html=True)
        st.header("🌱 Recomendações Agrícolas Integradas")
        st.markdown("Recomendações baseadas na análise integrada de dados de saúde, produção e clima")
        
        if st.button("🔄 Gerar Recomendações Integradas", use_container_width=True, type="primary"):
            with st.spinner("A IA está a analisar os dados integrados..."):
                # Análise de dados dos pacientes
                if 'patients' in st.session_state and st.session_state.patients:
                    df = pd.DataFrame(st.session_state.patients)
                    
                    # Estatísticas
                    total = len(df)
                    risco_alto = len(df[df['anemia_risco'] == 'ALTO'])
                    risco_medio = len(df[df['anemia_risco'] == 'MÉDIO'])
                    baixa_diversidade = len(df[df['diversidade_alimentar'] < 4])
                    consumo_ferro = len(df[df['consumo_ferro'] == 1])
                    media_dds = df['diversidade_alimentar'].mean()
                    
                    # Dados agrícolas
                    agri = st.session_state.agri_data
                    
                    # Gerar recomendações
                    recomendacoes = []
                    
                    # 1. Recomendações baseadas em risco de anemia
                    if risco_alto > total * 0.3:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '🍖 Combate à Anemia',
                            'acao': 'Distribuir sementes de feijão e amendoim biofortificados para todas as famílias com crianças em risco',
                            'prazo': 'Imediato'
                        })
                    
                    # 2. Recomendações baseadas em diversidade alimentar
                    if baixa_diversidade > total * 0.4:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '🥬 Diversificação Alimentar',
                            'acao': 'Implementar hortas familiares com 5+ culturas (verduras, leguminosas, tubérculos)',
                            'prazo': 'Curto prazo (1-2 meses)'
                        })
                    
                    # 3. Recomendações baseadas em produção agrícola
                    if agri['producao_leguminosas'] < 50:
                        recomendacoes.append({
                            'prioridade': 'MÉDIA',
                            'categoria': '🌱 Produção de Leguminosas',
                            'acao': 'Aumentar produção de leguminosas (feijão, amendoim) em 50%',
                            'prazo': 'Médio prazo (3-6 meses)'
                        })
                    
                    if agri['producao_hortalicas'] < 30:
                        recomendacoes.append({
                            'prioridade': 'MÉDIA',
                            'categoria': '🥗 Produção de Hortícolas',
                            'acao': 'Expandir produção de hortícolas (couve, espinafre, cenoura)',
                            'prazo': 'Médio prazo (3-6 meses)'
                        })
                    
                    # 4. Recomendações baseadas em clima
                    if agri['seca_frequencia'] > 1:
                        recomendacoes.append({
                            'prioridade': 'MÉDIA',
                            'categoria': '🌦 Resiliência Climática',
                            'acao': 'Introduzir culturas tolerantes à seca (mandioca, sorgo, batata-doce)',
                            'prazo': 'Médio prazo (3-6 meses)'
                        })
                    
                    # 5. Recomendações baseadas em criação animal
                    if agri['ovos_semana'] < 20:
                        recomendacoes.append({
                            'prioridade': 'BAIXA',
                            'categoria': '🐔 Produção Animal',
                            'acao': 'Melhorar criação de galinhas para produção de ovos (mínimo 30 ovos/semana)',
                            'prazo': 'Longo prazo (6-12 meses)'
                        })
                    
                    # 6. Recomendação geral
                    if media_dds < 4:
                        recomendacoes.append({
                            'prioridade': 'ALTA',
                            'categoria': '📋 Educação Alimentar',
                            'acao': 'Promover campanhas de educação nutricional sobre diversidade alimentar',
                            'prazo': 'Imediato'
                        })
                    
                    # Mostrar recomendações
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
                    
                    # Sumário executivo
                    st.markdown("---")
                    st.subheader("📊 Sumário Executivo")
                    
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("Prioridade ALTA", len([r for r in recomendacoes if r['prioridade'] == 'ALTA']))
                    with col_s2:
                        st.metric("Prioridade MÉDIA", len([r for r in recomendacoes if r['prioridade'] == 'MÉDIA']))
                    with col_s3:
                        st.metric("Prioridade BAIXA", len([r for r in recomendacoes if r['prioridade'] == 'BAIXA']))
                    
                else:
                    st.warning("⚠️ Sem dados de pacientes para análise. Aguarde as triagens do enfermeiro.")