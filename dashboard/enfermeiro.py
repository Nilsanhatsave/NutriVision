import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

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
    .locked-box {
        background: #f5f5f5;
        border-radius: 8px;
        padding: 1.5rem;
        text-align: center;
        border: 2px dashed #ccc;
    }
    .locked-box .icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
    .locked-box .title { font-weight: 700; color: #666; font-size: 1.1rem; }
    .locked-box .subtitle { color: #999; font-size: 0.9rem; margin-top: 0.3rem; }
    .info-box {
        background: #E3F2FD;
        border-left: 4px solid #2196F3;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .age-badge {
        display: inline-block;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .age-badge-0 { background: #E3F2FD; color: #1565C0; }
    .age-badge-1 { background: #E8F5E9; color: #2E7D32; }
    .age-badge-2 { background: #FFF3E0; color: #E65100; }
    .age-badge-3 { background: #FCE4EC; color: #C62828; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .fade-in { animation: fadeInUp 0.5s ease forwards; }
    .hidden { display: none; }
</style>
""", unsafe_allow_html=True)

def render_enfermeiro():
    st.markdown('<h1 style="font-size:2rem;font-weight:700;color:#1565C0;">👩🏾‍⚕️ Enfermeiro - Triagem Nutricional</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:1rem;color:#555;margin-bottom:1.5rem;">Registe os dados da criança. Os campos são ajustados automaticamente conforme a idade.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="floating-actions">
        <button class="floating-btn" onclick="document.getElementById('nova_triagem').click()">📋 Nova Triagem</button>
        <button class="floating-btn floating-btn-secondary" onclick="document.getElementById('ver_pacientes').click()">📊 Ver Pacientes</button>
    </div>
    """, unsafe_allow_html=True)
    
    if 'patients' not in st.session_state:
        st.session_state.patients = []
    
    tab1, tab2 = st.tabs(["📋 Nova Triagem", "📊 Pacientes Avaliados"])
    
    with tab1:
        with st.container():
            st.markdown('<div id="nova_triagem"></div>', unsafe_allow_html=True)
            
            with st.form("triagem_form"):
                # ============================================================
                # PASSO 1: DADOS PESSOAIS E IDADE (SEMPRE VISÍVEL)
                # ============================================================
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">👶 Passo 1: Identificação da Criança</div>', unsafe_allow_html=True)
                
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
                
                # Determinar grupo etário
                if idade_meses < 6:
                    grupo_etario = "Lactente (0-6 meses)"
                    badge_class = "age-badge-0"
                    icon = "🍼"
                    msg_etario = "Aleitamento materno exclusivo recomendado até 6 meses"
                    mostrar_complementar = False
                    mostrar_ferro = False
                    mostrar_diversidade = False
                    mostrar_aleitamento = True
                elif idade_meses <= 12:
                    grupo_etario = "Lactente (6-12 meses)"
                    badge_class = "age-badge-1"
                    icon = "🍚"
                    msg_etario = "Fase de introdução alimentar"
                    mostrar_complementar = True
                    mostrar_ferro = True
                    mostrar_diversidade = True
                    mostrar_aleitamento = True
                elif idade_meses <= 24:
                    grupo_etario = "Criança (12-24 meses)"
                    badge_class = "age-badge-2"
                    icon = "🍽️"
                    msg_etario = "Consolidação da alimentação familiar"
                    mostrar_complementar = True
                    mostrar_ferro = True
                    mostrar_diversidade = True
                    mostrar_aleitamento = True
                else:
                    grupo_etario = "Criança (> 24 meses)"
                    badge_class = "age-badge-3"
                    icon = "🥗"
                    msg_etario = "Dieta familiar - avaliar diversidade e ferro"
                    mostrar_complementar = False  # BLOQUEADO para > 24 meses
                    mostrar_ferro = True
                    mostrar_diversidade = True
                    mostrar_aleitamento = False  # BLOQUEADO para > 24 meses
                
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:0.5rem;margin:0.5rem 0;padding:0.5rem 1rem;background:#f5f5f5;border-radius:8px;">
                    <span style="font-size:1.5rem;">{icon}</span>
                    <span><strong>Grupo Etário:</strong> {grupo_etario}</span>
                    <span class="age-badge {badge_class}" style="margin-left:auto;">{idade_meses} meses</span>
                </div>
                <p style="color:#555;font-size:0.9rem;">📌 {msg_etario}</p>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============================================================
                # PASSO 2: DADOS ANTROPOMÉTRICOS (SEMPRE VISÍVEL)
                # ============================================================
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📏 Passo 2: Dados Antropométricos</div>', unsafe_allow_html=True)
                
                col_ant1, col_ant2, col_ant3 = st.columns(3)
                with col_ant1:
                    peso = st.number_input("Peso (kg)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
                with col_ant2:
                    altura = st.number_input("Altura/Comprimento (cm)", min_value=0.0, max_value=150.0, value=85.0, step=0.1)
                with col_ant3:
                    muac = st.number_input("MUAC (mm)", min_value=0, max_value=200, value=130, step=1)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # ============================================================
                # PASSO 3: ALEITAMENTO (BLOQUEADO PARA > 24 MESES)
                # ============================================================
                if mostrar_aleitamento:
                    st.markdown('<div class="section-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-title">🍼 Passo 3: Aleitamento</div>', unsafe_allow_html=True)
                    
                    if idade_meses < 6:
                        aleitamento = st.selectbox("Tipo de aleitamento", [
                            "Aleitamento Materno Exclusivo ✅ (Recomendado)",
                            "Aleitamento Materno + Água/Chá ⚠️",
                            "Aleitamento Materno + Leite Artificial ⚠️",
                            "Leite Artificial Exclusivo ⚠️"
                        ])
                        if "Exclusivo" not in aleitamento:
                            st.warning("⚠️ A OMS recomenda aleitamento materno exclusivo até os 6 meses")
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
                else:
                    # Bloqueado para > 24 meses
                    st.markdown("""
                    <div class="locked-box">
                        <span class="icon">🔒</span>
                        <div class="title">Campo Bloqueado</div>
                        <div class="subtitle">Criança com mais de 24 meses - o aleitamento já não é o principal fator nutricional</div>
                        <div style="margin-top:0.5rem;font-size:0.85rem;color:#aaa;">A avaliação de diversidade alimentar é aplicada no passo seguinte</div>
                    </div>
                    """, unsafe_allow_html=True)
                    aleitamento = "Não aplicável (> 24 meses)"
                
                # ============================================================
                # PASSO 4: ALIMENTAÇÃO COMPLEMENTAR (APENAS < 24 MESES)
                # ============================================================
                if mostrar_complementar:
                    with st.expander("🍚 Passo 4: Alimentação Complementar (6-24 meses)", expanded=True):
                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
                        
                        if idade_meses < 6:
                            st.markdown("""
                            <div class="info-box">
                                ℹ️ A OMS recomenda aleitamento materno exclusivo até os 6 meses.
                                Se a mãe já iniciou alimentação complementar, preencha os campos abaixo.
                            </div>
                            """, unsafe_allow_html=True)
                        
                        col_comp1, col_comp2 = st.columns(2)
                        with col_comp1:
                            idade_introducao = st.selectbox("Idade de introdução", [
                                "Antes dos 4 meses ⚠️" if idade_meses < 6 else "Antes dos 4 meses",
                                "Entre 4-5 meses", "Aos 6 meses ✅", "Aos 7-8 meses", "Após 8 meses"
                            ])
                            frequencia_refeicoes = st.selectbox("Frequência de refeições/dia", [
                                "Menos de 1", "1 refeição", "2 refeições", "3 ou mais refeições"
                            ])
                        with col_comp2:
                            consistencia = st.selectbox("Consistência", [
                                "Líquida", "Papa fina", "Papa espessa", "Com pedaços", "Alimentos sólidos"
                            ])
                            grupos_alimentares = st.multiselect(
                                "Grupos alimentares incluídos",
                                ["Cereais", "Leguminosas", "Verduras", "Frutas", "Carnes", "Ovos", "Laticínios", "Óleos"]
                            )
                        
                        if "Antes dos 4 meses" in idade_introducao and idade_meses < 6:
                            st.error("🚨 Atenção: A introdução alimentar antes dos 4 meses não é recomendada!")
                        
                        # Avaliação
                        idade_score = {"Antes dos 4 meses": 0, "Entre 4-5 meses": 1, "Aos 6 meses ✅": 3, "Aos 7-8 meses": 2, "Após 8 meses": 1}
                        freq_score = {"Menos de 1": 0, "1 refeição": 1, "2 refeições": 2, "3 ou mais refeições": 3}
                        consistencia_score = {"Líquida": 0, "Papa fina": 1, "Papa espessa": 2, "Com pedaços": 3, "Alimentos sólidos": 3}
                        
                        # Ajustar chave para idade_introducao
                        chave_idade = idade_introducao if idade_introducao in idade_score else "Aos 6 meses ✅"
                        pontuacao_comp = (
                            idade_score.get(chave_idade, 0) +
                            freq_score.get(frequencia_refeicoes, 0) +
                            consistencia_score.get(consistencia, 0) +
                            min(len(grupos_alimentares), 3)
                        )
                        
                        if idade_meses <= 12:
                            if pontuacao_comp >= 9:
                                classif_comp = "Adequada ✅"
                            elif pontuacao_comp >= 6:
                                classif_comp = "Parcialmente Adequada ⚠️"
                            else:
                                classif_comp = "Inadequada 🔴"
                        else:
                            if pontuacao_comp >= 8:
                                classif_comp = "Adequada ✅"
                            elif pontuacao_comp >= 5:
                                classif_comp = "Parcialmente Adequada ⚠️"
                            else:
                                classif_comp = "Inadequada 🔴"
                        
                        st.markdown(f"""
                        <div style="background:#f5f5f5;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid {'green' if 'Adequada' in classif_comp else 'orange' if 'Parcial' in classif_comp else 'red'};">
                            <strong>Classificação:</strong> {classif_comp}
                            <br><small>Pontuação: {pontuacao_comp}/12</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Bloqueado para > 24 meses
                    st.markdown("""
                    <div class="locked-box">
                        <span class="icon">🔒</span>
                        <div class="title">Campo Bloqueado</div>
                        <div class="subtitle">Criança com mais de 24 meses - alimentação complementar já consolidada</div>
                        <div style="margin-top:0.5rem;font-size:0.85rem;color:#aaa;">A avaliação de diversidade alimentar é aplicada no passo seguinte</div>
                    </div>
                    """, unsafe_allow_html=True)
                    classif_comp = "Não aplicável (> 24 meses)"
                    pontuacao_comp = None
                    idade_introducao = None
                    frequencia_refeicoes = None
                    consistencia = None
                    grupos_alimentares = []
                
                # ============================================================
                # PASSO 5: CONSUMO DE FERRO (APENAS > 6 MESES)
                # ============================================================
                if mostrar_ferro:
                    with st.expander("🥩 Passo 5: Consumo de Alimentos Ricos em Ferro", expanded=True):
                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
                        
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
                        
                        if idade_meses < 12:
                            if pontuacao_ferro >= 8:
                                classif_ferro = "Adequado ✅"
                            elif pontuacao_ferro >= 5:
                                classif_ferro = "Moderado ⚠️"
                            else:
                                classif_ferro = "Inadequado 🔴"
                        else:
                            if pontuacao_ferro >= 9:
                                classif_ferro = "Adequado ✅"
                            elif pontuacao_ferro >= 6:
                                classif_ferro = "Moderado ⚠️"
                            else:
                                classif_ferro = "Inadequado 🔴"
                        
                        st.markdown(f"""
                        <div style="background:#f5f5f5;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid {'green' if 'Adequado' in classif_ferro else 'orange' if 'Moderado' in classif_ferro else 'red'};">
                            <strong>Classificação:</strong> {classif_ferro}
                            <br><small>Pontuação: {pontuacao_ferro}/12</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    with st.expander("🥩 Passo 5: Consumo de Alimentos Ricos em Ferro", expanded=False):
                        st.markdown("""
                        <div class="locked-box">
                            <span class="icon">🔒</span>
                            <div class="title">Campo Bloqueado</div>
                            <div class="subtitle">Criança com menos de 6 meses - em aleitamento materno exclusivo</div>
                        </div>
                        """, unsafe_allow_html=True)
                        classif_ferro = "Não aplicável (< 6 meses)"
                        pontuacao_ferro = None
                        freq_feijao = freq_carne = freq_ovos = freq_verduras = None
                
                # ============================================================
                # PASSO 6: DIVERSIDADE ALIMENTAR (APENAS > 6 MESES)
                # ============================================================
                if mostrar_diversidade:
                    with st.expander("🍽️ Passo 6: Diversidade Alimentar", expanded=True):
                        st.markdown('<div class="section-card">', unsafe_allow_html=True)
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
                            if diversidade >= 5:
                                st.success(f"✅ Diversidade: {diversidade}/9 - Adequada para a idade")
                            elif diversidade >= 4:
                                st.warning(f"⚠️ Diversidade: {diversidade}/9 - Mínima aceitável")
                            else:
                                st.error(f"🔴 Diversidade: {diversidade}/9 - Insuficiente para a idade")
                        else:
                            if diversidade >= 6:
                                st.success(f"✅ Diversidade: {diversidade}/9 - Excelente")
                            elif diversidade >= 4:
                                st.info(f"📌 Diversidade: {diversidade}/9 - Adequada")
                            else:
                                st.error(f"🔴 Diversidade: {diversidade}/9 - Baixa - risco nutricional")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    with st.expander("🍽️ Passo 6: Diversidade Alimentar", expanded=False):
                        st.markdown("""
                        <div class="locked-box">
                            <span class="icon">🔒</span>
                            <div class="title">Campo Bloqueado</div>
                            <div class="subtitle">Criança com menos de 6 meses - em aleitamento materno exclusivo</div>
                        </div>
                        """, unsafe_allow_html=True)
                        diversidade = 0
                        alimentos_consumidos = [False] * 9
                
                # ============================================================
                # BOTÃO CALCULAR
                # ============================================================
                calcular = st.form_submit_button("🔬 Calcular Risco", use_container_width=True, type="primary")
                
                if calcular:
                    if not primeiro_nome or not apelido:
                        st.error("⚠️ Por favor, insira pelo menos o Primeiro Nome e Apelido")
                    else:
                        # Determinar riscos
                        if idade_meses < 6:
                            anemia_risco = "BAIXO"
                            anemia_prob = 10
                        elif diversidade < 4:
                            anemia_risco = "ALTO"
                            anemia_prob = 85
                        elif diversidade < 6:
                            anemia_risco = "MÉDIO"
                            anemia_prob = 55
                        else:
                            anemia_risco = "BAIXO"
                            anemia_prob = 20
                        
                        if idade_meses < 6:
                            nutrition_risco = "BAIXO"
                            nutrition_prob = 5
                        elif diversidade < 3:
                            nutrition_risco = "ALTO"
                            nutrition_prob = 80
                        elif diversidade < 5:
                            nutrition_risco = "MÉDIO"
                            nutrition_prob = 50
                        else:
                            nutrition_risco = "BAIXO"
                            nutrition_prob = 15
                        
                        food_security_risco = "MÉDIO"
                        food_security_prob = 40
                        
                        # Salvar paciente
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
                            'aleitamento': aleitamento,
                            'diversidade_alimentar': diversidade if idade_meses >= 6 else 0,
                            'classificacao_complementar': classif_comp if idade_meses < 24 else "Não aplicável (> 24 meses)",
                            'pontuacao_complementar': pontuacao_comp if idade_meses < 24 else None,
                            'classificacao_ferro': classif_ferro if idade_meses >= 6 else "Não aplicável (< 6 meses)",
                            'pontuacao_ferro': pontuacao_ferro if idade_meses >= 6 else None,
                            'data_avaliacao': datetime.now().strftime('%d/%m/%Y %H:%M'),
                            'anemia_risco': anemia_risco,
                            'anemia_prob': anemia_prob,
                            'nutrition_risco': nutrition_risco,
                            'nutrition_prob': nutrition_prob,
                            'food_security_risco': food_security_risco,
                            'food_security_prob': food_security_prob,
                            'deficits': ['Ferro'] if diversidade < 4 else ['Nenhum']
                        }
                        
                        st.session_state.patients.append(patient_data)
                        st.success(f"✅ Avaliação concluída para **{nome_completo}**!")
                        
                        # Mostrar resultados
                        st.markdown('<div class="result-container fade-in">', unsafe_allow_html=True)
                        st.subheader("📊 Resultados da Avaliação")
                        
                        col_r1, col_r2, col_r3 = st.columns(3)
                        
                        with col_r1:
                            cor_anemia = "🟢" if anemia_risco == "BAIXO" else "🟡" if anemia_risco == "MÉDIO" else "🔴"
                            st.metric("Risco de Anemia", f"{cor_anemia} {anemia_risco}", f"{anemia_prob:.1f}%")
                        
                        with col_r2:
                            cor_nutrition = "🟢" if nutrition_risco == "BAIXO" else "🟡" if nutrition_risco == "MÉDIO" else "🔴"
                            st.metric("Risco de Fome Oculta", f"{cor_nutrition} {nutrition_risco}", f"{nutrition_prob:.1f}%")
                        
                        with col_r3:
                            cor_food = "🟢" if food_security_risco == "BAIXO" else "🟡" if food_security_risco == "MÉDIO" else "🔴"
                            st.metric("Insegurança Alimentar", f"{cor_food} {food_security_risco}", f"{food_security_prob:.1f}%")
                        
                        st.markdown("---")
                        st.subheader("📋 Resumo da Avaliação")
                        
                        resumo = f"""
                        **👶 Grupo Etário:** {grupo_etario} ({idade_meses} meses)
                        - **Diversidade Alimentar:** {diversidade}/9
                        """
                        
                        if idade_meses < 24:
                            resumo += f"\n- **Aleitamento:** {aleitamento}"
                            resumo += f"\n- **Alimentação Complementar:** {classif_comp}"
                        else:
                            resumo += "\n- **Aleitamento:** Não aplicável (> 24 meses)"
                            resumo += "\n- **Alimentação Complementar:** Não aplicável (> 24 meses)"
                        
                        if idade_meses >= 6:
                            resumo += f"\n- **Consumo de Ferro:** {classif_ferro}"
                        else:
                            resumo += "\n- **Consumo de Ferro:** Não aplicável (< 6 meses)"
                        
                        st.markdown(resumo)
                        
                        if anemia_risco == "ALTO" or nutrition_risco == "ALTO":
                            st.error("🚨 **PRIORIDADE ALTA** - Encaminhar para médico com urgência")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        with st.container():
            st.markdown('<div id="ver_pacientes"></div>', unsafe_allow_html=True)
            st.header("📋 Pacientes Avaliados")
            
            if st.session_state.patients:
                df = pd.DataFrame(st.session_state.patients)
                
                col_est1, col_est2, col_est3, col_est4 = st.columns(4)
                with col_est1:
                    st.metric("Total", len(df))
                with col_est2:
                    alto_risco = len(df[df['anemia_risco'] == 'ALTO'])
                    st.metric("Risco ALTO", alto_risco)
                with col_est3:
                    media_diversidade = df['diversidade_alimentar'].mean()
                    st.metric("DDS Médio", f"{media_diversidade:.1f}/9")
                with col_est4:
                    baixa_diversidade = len(df[df['diversidade_alimentar'] < 4])
                    st.metric("Baixa Diversidade", baixa_diversidade)
                
                st.dataframe(
                    df[['nome', 'idade_meses', 'grupo_etario', 'anemia_risco', 'nutrition_risco', 'diversidade_alimentar', 'data_avaliacao']],
                    use_container_width=True
                )
                
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    if len(df['anemia_risco'].unique()) > 1:
                        fig1 = px.pie(df, names='anemia_risco', title='Risco de Anemia', color_discrete_sequence=['#4CAF50', '#FF9800', '#F44336'])
                        st.plotly_chart(fig1, use_container_width=True)
                with col_g2:
                    fig2 = px.histogram(df, x='diversidade_alimentar', title='Diversidade Alimentar', nbins=9)
                    st.plotly_chart(fig2, use_container_width=True)
                
                csv = df.to_csv(index=False)
                st.download_button(label="📥 Baixar Dados (CSV)", data=csv, file_name=f"triagens_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
            else:
                st.info("📋 Nenhum paciente avaliado ainda. Realize a primeira triagem!")