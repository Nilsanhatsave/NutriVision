import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from models.anemia_model import AnemiaModel
from models.nutrition_model import NutritionModel
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
        background: linear-gradient(145deg, #1565C0, #0D47A1);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 4px 15px rgba(21, 101, 192, 0.3);
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .floating-btn:hover { transform: translateX(-5px); box-shadow: 0 6px 25px rgba(21, 101, 192, 0.4); }
    .floating-btn-secondary { background: linear-gradient(145deg, #2E7D32, #1B5E20); box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3); }
    .floating-btn-secondary:hover { box-shadow: 0 6px 25px rgba(46, 125, 50, 0.4); }
    .result-container {
        background: linear-gradient(145deg, #f8f9fa, #ffffff);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #e8f5e9;
        margin-top: 1rem;
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
        color: #1565C0;
        margin-bottom: 0.8rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E3F2FD;
    }
    .age-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .age-badge-0 { background: #E3F2FD; color: #1565C0; }
    .age-badge-1 { background: #E8F5E9; color: #2E7D32; }
    .age-badge-2 { background: #FFF3E0; color: #E65100; }
    .age-badge-3 { background: #FCE4EC; color: #C62828; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .fade-in { animation: fadeInUp 0.5s ease forwards; }
</style>
""", unsafe_allow_html=True)

def render_enfermeiro():
    st.markdown('<h1 style="font-size:2rem;font-weight:700;color:#1565C0;">👩🏾‍⚕️ Enfermeiro - Triagem Nutricional</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;color:#555;margin-bottom:1.5rem;">Registe dados antropométricos, dietéticos, socioeconómicos e alimentares da criança < 5 anos</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="floating-actions">
        <button class="floating-btn" onclick="document.getElementById('nova_triagem').click()">📋 Nova Triagem</button>
        <button class="floating-btn floating-btn-secondary" onclick="document.getElementById('ver_pacientes').click()">📊 Ver Pacientes</button>
    </div>
    """, unsafe_allow_html=True)
    
    anemia_model = AnemiaModel()
    nutrition_model = NutritionModel()
    food_security_model = FoodSecurityModel()
    
    if 'patients' not in st.session_state:
        st.session_state.patients = []
    
    tab1, tab2 = st.tabs(["📋 Nova Triagem", "📊 Pacientes Avaliados"])
    
    with tab1:
        with st.container():
            st.markdown('<div id="nova_triagem"></div>', unsafe_allow_html=True)
            
            # ============ AVISO IMPORTANTE ============
            st.info("""
            🎯 **Público-Alvo:** Crianças de **0 a 59 meses** (< 5 anos)
            
            A avaliação é adaptada conforme a faixa etária.
            """)
            
            st.subheader("📝 Dados da Criança e Família")
            
            with st.form("triagem_form"):
                # ============ DADOS PESSOAIS ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">👶 Identificação da Criança</div>', unsafe_allow_html=True)
                
                col_nome1, col_nome2, col_nome3 = st.columns(3)
                with col_nome1:
                    primeiro_nome = st.text_input("Primeiro Nome *", placeholder="Ex: Maria")
                with col_nome2:
                    nome_meio = st.text_input("Nome do Meio", placeholder="Ex: Joaquina")
                with col_nome3:
                    apelido = st.text_input("Apelido *", placeholder="Ex: Santos")
                
                nome_completo = f"{primeiro_nome} {nome_meio} {apelido}".strip()
                
                col_idade, col_sexo = st.columns(2)
                with col_idade:
                    idade_meses = st.number_input("Idade (meses)", min_value=0, max_value=59, value=24, step=1)
                with col_sexo:
                    sexo = st.selectbox("Sexo", ["Feminino", "Masculino"])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ CATEGORIZAÇÃO POR IDADE ============
                if idade_meses < 6:
                    grupo_etario = "Lactente (0-6 meses)"
                    cor_badge = "age-badge-0"
                    icon = "🍼"
                    mostrar_complementar = False
                    mostrar_ferro = False
                    msg_etario = "Aleitamento materno exclusivo recomendado"
                elif idade_meses <= 12:
                    grupo_etario = "Lactente (6-12 meses)"
                    cor_badge = "age-badge-1"
                    icon = "🍚"
                    mostrar_complementar = True
                    mostrar_ferro = True
                    msg_etario = "Fase de introdução alimentar - atenção à diversidade"
                elif idade_meses <= 24:
                    grupo_etario = "Criança (12-24 meses)"
                    cor_badge = "age-badge-2"
                    icon = "🍽️"
                    mostrar_complementar = True
                    mostrar_ferro = True
                    msg_etario = "Consolidação da alimentação familiar"
                elif idade_meses <= 36:
                    grupo_etario = "Criança (24-36 meses)"
                    cor_badge = "age-badge-3"
                    icon = "🥘"
                    mostrar_complementar = False
                    mostrar_ferro = True
                    msg_etario = "Dieta familiar - avaliar diversidade e ferro"
                else:
                    grupo_etario = "Pré-escolar (36-59 meses)"
                    cor_badge = "age-badge-3"
                    icon = "🥗"
                    mostrar_complementar = False
                    mostrar_ferro = True
                    msg_etario = "Dieta completa - avaliar diversidade e ferro"
                
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:0.5rem;margin:0.5rem 0;padding:0.5rem;background:#f5f5f5;border-radius:8px;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <span><strong>Grupo Etário:</strong> {grupo_etario}</span>
                    <span class="age-badge {cor_badge}" style="margin-left:auto;">{idade_meses} meses</span>
                </div>
                <p style="color:#555;font-size:0.9rem;">📌 {msg_etario}</p>
                """, unsafe_allow_html=True)
                
                # ============ DADOS ANTROPOMÉTRICOS ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📏 Dados Antropométricos</div>', unsafe_allow_html=True)
                
                col_ant1, col_ant2, col_ant3 = st.columns(3)
                with col_ant1:
                    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
                with col_ant2:
                    altura = st.number_input("Altura/Comprimento (cm)", min_value=0.0, max_value=150.0, value=85.0, step=0.1)
                with col_ant3:
                    muac = st.number_input("MUAC (mm)", min_value=0, max_value=200, value=130, step=1)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ ALEITAMENTO ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🍼 Aleitamento</div>', unsafe_allow_html=True)
                
                if idade_meses < 6:
                    aleitamento = st.selectbox("Tipo de aleitamento", [
                        "Aleitamento Materno Exclusivo ✅",
                        "Aleitamento Materno + Água/Chá ⚠️",
                        "Aleitamento Materno + Leite Artificial ⚠️",
                        "Leite Artificial Exclusivo ⚠️"
                    ])
                    if "Exclusivo" not in aleitamento:
                        st.warning("⚠️ Recomenda-se aleitamento materno exclusivo até os 6 meses")
                    else:
                        st.success("✅ Aleitamento materno exclusivo - recomendado pela OMS")
                else:
                    aleitamento = st.selectbox("Tipo de aleitamento", [
                        "Aleitamento Materno",
                        "Leite Artificial",
                        "Aleitamento Materno + Leite Artificial",
                        "Sem leite"
                    ])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ ALIMENTAÇÃO COMPLEMENTAR (6-24 MESES) ============
                if mostrar_complementar:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">🍚 Avaliação da Alimentação Complementar (6-24 meses)</div>', unsafe_allow_html=True)
                    st.caption("Critérios baseados nas recomendações da OMS para alimentação complementar")
                    
                    col_comp1, col_comp2 = st.columns(2)
                    with col_comp1:
                        idade_introducao = st.selectbox("Idade de introdução de alimentos complementares", [
                            "Antes dos 4 meses", "Entre 4-5 meses", "Aos 6 meses", "Aos 7-8 meses", "Após 8 meses"
                        ])
                        frequencia_refeicoes = st.selectbox("Frequência de refeições complementares por dia", [
                            "Menos de 1", "1 refeição", "2 refeições", "3 ou mais refeições"
                        ])
                    with col_comp2:
                        consistencia = st.selectbox("Consistência da alimentação complementar", [
                            "Líquida (apenas sopas)", "Papa fina", "Papa espessa", "Com pedaços", "Alimentos sólidos"
                        ])
                        grupos_alimentares = st.multiselect(
                            "Grupos alimentares incluídos (selecione os que são oferecidos)",
                            ["Cereais", "Leguminosas", "Verduras", "Frutas", "Carnes", "Ovos", "Laticínios", "Óleos"]
                        )
                    
                    # Avaliação automática
                    idade_score = {"Antes dos 4 meses": 0, "Entre 4-5 meses": 1, "Aos 6 meses": 3, "Aos 7-8 meses": 2, "Após 8 meses": 1}
                    freq_score = {"Menos de 1": 0, "1 refeição": 1, "2 refeições": 2, "3 ou mais refeições": 3}
                    consistencia_score = {"Líquida (apenas sopas)": 0, "Papa fina": 1, "Papa espessa": 2, "Com pedaços": 3, "Alimentos sólidos": 3}
                    
                    pontuacao_comp = (
                        idade_score.get(idade_introducao, 0) +
                        freq_score.get(frequencia_refeicoes, 0) +
                        consistencia_score.get(consistencia, 0) +
                        min(len(grupos_alimentares), 3)
                    )
                    
                    if idade_meses <= 12:
                        # Critérios mais rigorosos para < 12 meses
                        if pontuacao_comp >= 9:
                            classif_comp = "Adequada ✅"
                            cor_comp = "green"
                            msg_comp = "Excelente! Alimentação complementar adequada"
                        elif pontuacao_comp >= 6:
                            classif_comp = "Parcialmente Adequada ⚠️"
                            cor_comp = "orange"
                            msg_comp = "Necessita melhorar alguns aspetos"
                        else:
                            classif_comp = "Inadequada 🔴"
                            cor_comp = "red"
                            msg_comp = "⚠️ URGENTE: Alimentação complementar inadequada"
                    else:
                        # Critérios para 12-24 meses
                        if pontuacao_comp >= 8:
                            classif_comp = "Adequada ✅"
                            cor_comp = "green"
                            msg_comp = "Boa consolidação da alimentação"
                        elif pontuacao_comp >= 5:
                            classif_comp = "Parcialmente Adequada ⚠️"
                            cor_comp = "orange"
                            msg_comp = "Necessita melhorar diversidade"
                        else:
                            classif_comp = "Inadequada 🔴"
                            cor_comp = "red"
                            msg_comp = "⚠️ Alimentação pouco diversificada"
                    
                    st.markdown(f"""
                    <div style="background:#f5f5f5;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid {cor_comp};">
                        <strong>Classificação:</strong> 
                        <span style="color:{cor_comp};font-weight:bold;">{classif_comp}</span>
                        <br>
                        <small>Pontuação: {pontuacao_comp}/12 | {msg_comp}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if pontuacao_comp < 6:
                        st.error("""
                        📌 **Recomendações Urgentes:**
                        - Iniciar alimentos complementares aos 6 meses
                        - Aumentar variedade (mínimo 4 grupos/dia)
                        - Oferecer 3 refeições/dia a partir dos 9 meses
                        - Aumentar consistência progressivamente
                        """)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    classif_comp = "Não aplicável (idade fora do grupo)"
                    pontuacao_comp = None
                
                # ============ CONSUMO DE FERRO (TODOS > 6 MESES) ============
                if mostrar_ferro:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">🥩 Consumo de Alimentos Ricos em Ferro</div>', unsafe_allow_html=True)
                    
                    if idade_meses < 12:
                        st.caption("Avaliação da introdução de alimentos ricos em ferro")
                    elif idade_meses < 36:
                        st.caption("Avaliação do consumo regular de alimentos ricos em ferro")
                    else:
                        st.caption("Avaliação da dieta familiar - consumo de ferro")
                    
                    col_ferro1, col_ferro2 = st.columns(2)
                    with col_ferro1:
                        freq_feijao = st.selectbox("Frequência de feijão/leguminosas", [
                            "Não consome", "1-2 vezes/semana", "3-4 vezes/semana", "5 ou mais vezes/semana"
                        ])
                        freq_carne = st.selectbox("Frequência de carne/peixe/frango", [
                            "Não consome", "1-2 vezes/semana", "3-4 vezes/semana", "5 ou mais vezes/semana"
                        ])
                    with col_ferro2:
                        freq_ovos = st.selectbox("Frequência de ovos", [
                            "Não consome", "1-2 vezes/semana", "3-4 vezes/semana", "5 ou mais vezes/semana"
                        ])
                        freq_verduras = st.selectbox("Frequência de folhas verdes escuras", [
                            "Não consome", "1-2 vezes/semana", "3-4 vezes/semana", "5 ou mais vezes/semana"
                        ])
                    
                    freq_score_map = {"Não consome": 0, "1-2 vezes/semana": 1, "3-4 vezes/semana": 2, "5 ou mais vezes/semana": 3}
                    
                    pontuacao_ferro = (
                        freq_score_map.get(freq_feijao, 0) +
                        freq_score_map.get(freq_carne, 0) +
                        freq_score_map.get(freq_ovos, 0) +
                        freq_score_map.get(freq_verduras, 0)
                    )
                    
                    # Critérios ajustados por idade
                    if idade_meses < 12:
                        # Mais rigoroso para < 1 ano
                        if pontuacao_ferro >= 8:
                            classif_ferro = "Adequado ✅"
                            cor_ferro = "green"
                            msg_ferro = "Boa introdução de alimentos ricos em ferro"
                        elif pontuacao_ferro >= 5:
                            classif_ferro = "Moderado ⚠️"
                            cor_ferro = "orange"
                            msg_ferro = "Aumentar frequência de alimentos ricos em ferro"
                        else:
                            classif_ferro = "Inadequado 🔴"
                            cor_ferro = "red"
                            msg_ferro = "⚠️ Alto risco de anemia - intervenção urgente"
                    elif idade_meses < 36:
                        # Critérios para 1-3 anos
                        if pontuacao_ferro >= 9:
                            classif_ferro = "Adequado ✅"
                            cor_ferro = "green"
                            msg_ferro = "Bom consumo de alimentos ricos em ferro"
                        elif pontuacao_ferro >= 6:
                            classif_ferro = "Moderado ⚠️"
                            cor_ferro = "orange"
                            msg_ferro = "Melhorar consumo de ferro"
                        else:
                            classif_ferro = "Inadequado 🔴"
                            cor_ferro = "red"
                            msg_ferro = "⚠️ Consumo muito baixo de ferro"
                    else:
                        # Critérios para 3-5 anos
                        if pontuacao_ferro >= 9:
                            classif_ferro = "Adequado ✅"
                            cor_ferro = "green"
                            msg_ferro = "Dieta rica em ferro"
                        elif pontuacao_ferro >= 6:
                            classif_ferro = "Moderado ⚠️"
                            cor_ferro = "orange"
                            msg_ferro = "Necessita mais alimentos ricos em ferro"
                        else:
                            classif_ferro = "Inadequado 🔴"
                            cor_ferro = "red"
                            msg_ferro = "⚠️ Risco elevado de anemia"
                    
                    st.markdown(f"""
                    <div style="background:#f5f5f5;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid {cor_ferro};">
                        <strong>Classificação:</strong> 
                        <span style="color:{cor_ferro};font-weight:bold;">{classif_ferro}</span>
                        <br>
                        <small>Pontuação: {pontuacao_ferro}/12 | {msg_ferro}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if pontuacao_ferro < 6:
                        st.warning("""
                        📌 **Recomendações para aumentar consumo de ferro:**
                        - Aumentar feijão e leguminosas
                        - Incluir carne vermelha, frango ou peixe
                        - Oferecer ovos (gema)
                        - Adicionar folhas verdes escuras
                        - Combinar com vitamina C (frutas) para melhor absorção
                        """)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    classif_ferro = "Não aplicável (< 6 meses)"
                    pontuacao_ferro = None
                
                # ============ DIVERSIDADE ALIMENTAR (TODOS) ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🍽️ Diversidade Alimentar</div>', unsafe_allow_html=True)
                
                if idade_meses < 6:
                    st.info("🍼 Criança em aleitamento materno exclusivo - diversidade alimentar não aplicável")
                    diversidade = 0
                    alimentos_consumidos = []
                else:
                    st.caption("Marque os alimentos consumidos pela criança na última semana:")
                    
                    col_diet1, col_diet2, col_diet3 = st.columns(3)
                    
                    with col_diet1:
                        cereais = st.checkbox("Cereais (arroz, milho, massa)")
                        leguminosas = st.checkbox("Leguminosas (feijão, amendoim)")
                        laticinios = st.checkbox("Laticínios (leite, queijo)")
                    
                    with col_diet2:
                        carnes = st.checkbox("Carnes/Peixe/Frango")
                        ovos = st.checkbox("Ovos")
                        frutas = st.checkbox("Frutas")
                    
                    with col_diet3:
                        verduras = st.checkbox("Verduras e legumes")
                        oleos = st.checkbox("Óleos e gorduras")
                        acucares = st.checkbox("Açúcares e doces")
                    
                    alimentos_consumidos = [cereais, leguminosas, laticinios, carnes, ovos, frutas, verduras, oleos, acucares]
                    diversidade = sum(alimentos_consumidos)
                    
                    if idade_meses < 12:
                        # Critério para < 1 ano: mínimo 4 grupos
                        if diversidade >= 5:
                            st.success(f"✅ Diversidade: {diversidade}/9 - Adequada para a idade")
                        elif diversidade >= 4:
                            st.warning(f"⚠️ Diversidade: {diversidade}/9 - Mínima aceitável")
                        else:
                            st.error(f"🔴 Diversidade: {diversidade}/9 - Insuficiente para a idade")
                    else:
                        # Critério para > 1 ano: mínimo 4 grupos
                        if diversidade >= 6:
                            st.success(f"✅ Diversidade: {diversidade}/9 - Excelente")
                        elif diversidade >= 4:
                            st.info(f"📌 Diversidade: {diversidade}/9 - Adequada")
                        else:
                            st.error(f"🔴 Diversidade: {diversidade}/9 - Baixa - risco nutricional")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ SOCIOECONÓMICOS ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🏠 Características Socioeconómicas</div>', unsafe_allow_html=True)
                
                col_socio1, col_socio2 = st.columns(2)
                with col_socio1:
                    escolaridade_mae = st.selectbox("Nível de escolaridade da mãe/cuidador", [
                        "Sem escolaridade", "Ensino Primário", "Ensino Secundário", "Ensino Superior"
                    ])
                    tamanho_familia = st.number_input("Número de pessoas no agregado familiar", min_value=1, max_value=20, value=5, step=1)
                with col_socio2:
                    renda = st.selectbox("Nível de renda familiar (proxy)", [
                        "Baixa", "Média-baixa", "Média", "Média-alta", "Alta"
                    ])
                    condicao_casa = st.selectbox("Condição da habitação", [
                        "Tijolo/Bloco", "Taipa/Adobe", "Madeira/Zincagem", "Outra"
                    ])
                
                col_socio3, col_socio4 = st.columns(2)
                with col_socio3:
                    agua = st.selectbox("Fonte de água", [
                        "Água canalizada em casa", "Fonte pública", "Poço", "Rio/Chuva", "Outra"
                    ])
                with col_socio4:
                    sani = st.selectbox("Acesso a saneamento", [
                        "Rede de esgoto", "Fossa séptica", "Fossa melhorada", "Fossa tradicional", "Nenhum"
                    ])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ SAÚDE ============
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🩺 Saúde e Suplementação</div>', unsafe_allow_html=True)
                
                col_saude1, col_saude2 = st.columns(2)
                with col_saude1:
                    febre = st.selectbox("Febre (última semana)", ["Não", "Sim"])
                    diarreia = st.selectbox("Diarreia (última semana)", ["Não", "Sim"])
                with col_saude2:
                    supl_ferro = st.selectbox("Suplementação de Ferro", ["Não", "Sim"])
                    supl_vit_a = st.selectbox("Suplementação Vitamina A", ["Não", "Sim"])
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============ BOTÃO CALCULAR ============
                calcular = st.form_submit_button("🔬 Calcular Risco", use_container_width=True, type="primary")
                
                if calcular:
                    if not primeiro_nome or not apelido:
                        st.error("⚠️ Por favor, insira pelo menos o Primeiro Nome e Apelido")
                    else:
                        # Preparar dados para o modelo
                        patient_data = {
                            'nome': nome_completo,
                            'primeiro_nome': primeiro_nome,
                            'nome_meio': nome_meio,
                            'apelido': apelido,
                            'sexo': sexo,
                            'idade_meses': idade_meses,
                            'grupo_etario': grupo_etario,
                            'peso_kg': peso,
                            'altura_cm': altura,
                            'muac_mm': muac,
                            'hemoglobina': None,
                            'febre': 1 if febre == "Sim" else 0,
                            'diarreia': 1 if diarreia == "Sim" else 0,
                            'suplementacao_ferro': 1 if supl_ferro == "Sim" else 0,
                            'suplementacao_vit_a': 1 if supl_vit_a == "Sim" else 0,
                            'diversidade_alimentar': diversidade if idade_meses >= 6 else 0,
                            'consumo_ferro': 1 if (idade_meses >= 6 and (leguminosas or carnes or ovos)) else 0,
                            'consumo_vit_a': 1 if (idade_meses >= 6 and (verduras or frutas)) else 0,
                            'consumo_proteinas': 1 if (idade_meses >= 6 and (carnes or leguminosas or ovos)) else 0,
                            'aleitamento': aleitamento,
                            'escolaridade_mae': escolaridade_mae,
                            'tamanho_familia': tamanho_familia,
                            'renda': renda,
                            'condicao_casa': condicao_casa,
                            'agua': agua,
                            'sani': sani,
                            'classificacao_complementar': classif_comp if mostrar_complementar else "Não aplicável",
                            'pontuacao_complementar': pontuacao_comp,
                            'classificacao_ferro': classif_ferro if mostrar_ferro else "Não aplicável",
                            'pontuacao_ferro': pontuacao_ferro,
                            'inseguranca_alimentar': 0,
                            'recomendacao_agricola': None,
                            'status_agronomo': 'Pendente'
                        }
                        
                        with st.spinner("🔄 A IA está a analisar os dados..."):
                            anemia_result = anemia_model.predict(patient_data)
                            nutrition_result = nutrition_model.predict(patient_data)
                            
                            community_data = {
                                'producao_total': 1000,
                                'diversidade_agricola': 4,
                                'producao_leguminosas': 8,
                                'producao_hortalicas': 15,
                                'preco_alimentos': 50,
                                'precipitacao': 650,
                                'temperatura': 28,
                                'seca_frequencia': 1,
                                'duracao_epoca': 120
                            }
                            food_security_result = food_security_model.predict(community_data)
                        
                        st.session_state.patients.append({
                            **patient_data,
                            'data_avaliacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
                            'anemia_risco': anemia_result['nivel_risco'],
                            'anemia_prob': anemia_result['probabilidade'],
                            'nutrition_risco': nutrition_result['nivel_risco'],
                            'nutrition_prob': nutrition_result['probabilidade'],
                            'food_security_risco': food_security_result['nivel_risco'],
                            'food_security_prob': food_security_result['probabilidade'],
                            'deficits': nutrition_result.get('deficits', ['Nenhum']),
                            'recomendacao_anemia': anemia_result.get('recomendacao', ''),
                            'hemoglobina': None
                        })
                        
                        st.success(f"✅ Avaliação concluída para **{nome_completo}**!")
                        
                        # Mostrar resultados
                        st.markdown('<div class="result-container fade-in">', unsafe_allow_html=True)
                        st.subheader("📊 Resultados da Avaliação")
                        
                        # Mostrar grupo etário
                        st.markdown(f"""
                        <div style="background:#E3F2FD;border-radius:8px;padding:0.5rem 1rem;margin-bottom:1rem;">
                            <strong>👶 Grupo Etário:</strong> {grupo_etario} ({idade_meses} meses)
                            <span style="margin-left:1rem;background:#1565C0;color:white;padding:0.1rem 0.8rem;border-radius:12px;font-size:0.8rem;">
                                {msg_etario}
                            </span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_r1, col_r2, col_r3 = st.columns(3)
                        
                        with col_r1:
                            cor_anemia = "🟢" if anemia_result['nivel_risco'] == "BAIXO" else "🟡" if anemia_result['nivel_risco'] == "MÉDIO" else "🔴"
                            st.metric("Risco de Anemia", f"{cor_anemia} {anemia_result['nivel_risco']}", f"{anemia_result['probabilidade']:.1f}%")
                        
                        with col_r2:
                            cor_nutrition = "🟢" if nutrition_result['nivel_risco'] == "BAIXO" else "🟡" if nutrition_result['nivel_risco'] == "MÉDIO" else "🔴"
                            st.metric("Risco de Fome Oculta", f"{cor_nutrition} {nutrition_result['nivel_risco']}", f"{nutrition_result['probabilidade']:.1f}%")
                        
                        with col_r3:
                            cor_food = "🟢" if food_security_result['nivel_risco'] == "BAIXO" else "🟡" if food_security_result['nivel_risco'] == "MÉDIO" else "🔴"
                            st.metric("Insegurança Alimentar", f"{cor_food} {food_security_result['nivel_risco']}", f"{food_security_result['probabilidade']:.1f}%")
                        
                        st.markdown("---")
                        st.subheader("📋 Resumo da Avaliação Nutricional")
                        
                        col_res1, col_res2 = st.columns(2)
                        with col_res1:
                            st.markdown(f"""
                            **🍽️ Dieta:**\n
                            - DDS: {diversidade}/9 {'✅' if diversidade >= 4 else '⚠️'}
                            - Consumo ferro: {'✅ Sim' if patient_data['consumo_ferro'] else '❌ Não'}
                            - Aleitamento: {aleitamento}
                            """)
                            if mostrar_complementar:
                                st.markdown(f"""
                                **🍚 Alimentação Complementar:**\n
                                - Classificação: {classif_comp}
                                - Pontuação: {pontuacao_comp}/12
                                """)
                        with col_res2:
                            st.markdown(f"""
                            **🏠 Socioeconómico:**\n
                            - Escolaridade mãe: {escolaridade_mae}
                            - Tamanho família: {tamanho_familia}
                            - Renda: {renda}
                            - Água: {agua}
                            - Saneamento: {sani}
                            """)
                            if mostrar_ferro:
                                st.markdown(f"""
                                **🥩 Consumo de Ferro:**\n
                                - Classificação: {classif_ferro}
                                - Pontuação: {pontuacao_ferro}/12
                                """)
                        
                        if anemia_result['nivel_risco'] == "ALTO" or nutrition_result['nivel_risco'] == "ALTO":
                            st.error("🚨 **PRIORIDADE ALTA** - Encaminhar para médico com urgência")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div id="ver_pacientes"></div>', unsafe_allow_html=True)
            st.header("📋 Pacientes Avaliados (< 5 anos)")
            
            if st.session_state.patients:
                df = pd.DataFrame(st.session_state.patients)
                
                col_est1, col_est2, col_est3, col_est4, col_est5 = st.columns(5)
                with col_est1:
                    st.metric("Total", len(df))
                with col_est2:
                    alto_risco = len(df[df['anemia_risco'] == 'ALTO'])
                    st.metric("Risco ALTO", alto_risco)
                with col_est3:
                    lactentes = len(df[df['idade_meses'] < 6])
                    st.metric("< 6 meses", lactentes)
                with col_est4:
                    criancas = len(df[(df['idade_meses'] >= 6) & (df['idade_meses'] < 24)])
                    st.metric("6-24 meses", criancas)
                with col_est5:
                    pre_escolar = len(df[df['idade_meses'] >= 24])
                    st.metric("24-59 meses", pre_escolar)
                
                st.dataframe(
                    df[['nome', 'idade_meses', 'grupo_etario', 'anemia_risco', 'nutrition_risco', 'diversidade_alimentar', 'data_avaliacao']],
                    use_container_width=True
                )
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    fig1 = px.pie(df, names='anemia_risco', title='Risco de Anemia', color_discrete_sequence=['#4CAF50', '#FF9800', '#F44336'])
                    st.plotly_chart(fig1, use_container_width=True)
                with col_g2:
                    fig2 = px.histogram(df, x='diversidade_alimentar', title='Diversidade Alimentar', nbins=9, color='anemia_risco')
                    st.plotly_chart(fig2, use_container_width=True)
                
                csv = df.to_csv(index=False)
                st.download_button(label="📥 Baixar Dados (CSV)", data=csv, file_name=f"triagens_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
            else:
                st.info("📋 Nenhum paciente avaliado ainda. Realize a primeira triagem!")