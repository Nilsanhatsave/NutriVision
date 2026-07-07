import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def render_medico():
    st.title("👨🏾‍⚕️ Médico - Avaliação Clínica")
    st.markdown("Visualize os pacientes encaminhados, confirme diagnósticos e solicite exames")
    
    if 'patients' not in st.session_state or not st.session_state.patients:
        st.warning("⚠️ Nenhum paciente registado. Aguarde o encaminhamento do enfermeiro.")
        return
    
    # Filtrar pacientes com risco ALTO ou MÉDIO
    df_patients = pd.DataFrame(st.session_state.patients)
    pacientes_risco = df_patients[(df_patients['anemia_risco'].isin(['ALTO', 'MÉDIO'])) | 
                                  (df_patients['nutrition_risco'].isin(['ALTO', 'MÉDIO']))]
    
    if pacientes_risco.empty:
        st.success("✅ Nenhum paciente com risco elevado no momento")
        return
    
    # Selecionar paciente
    st.subheader("🔍 Selecionar Paciente")
    
    # Criar lista com informações
    pacientes_lista = []
    for _, row in pacientes_risco.iterrows():
        nome = row['nome']
        idade = row['idade_meses']
        risco = row['anemia_risco']
        pacientes_lista.append(f"{nome} ({idade} meses) - Risco: {risco}")
    
    selected = st.selectbox("Selecione um paciente para avaliação:", pacientes_lista)
    
    # Extrair nome do paciente selecionado
    nome_selecionado = selected.split(" (")[0]
    patient_data = df_patients[df_patients['nome'] == nome_selecionado].iloc[0].to_dict()
    
    st.divider()
    
    # Dashboard do paciente
    st.header(f"📋 Ficha do Paciente: {patient_data['nome']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Dados Antropométricos")
        st.write(f"**Idade:** {patient_data['idade_meses']} meses")
        st.write(f"**Peso:** {patient_data['peso_kg']} kg")
        st.write(f"**Altura:** {patient_data['altura_cm']} cm")
        st.write(f"**MUAC:** {patient_data['muac_mm']} mm")
        st.write(f"**Diversidade Alimentar:** {patient_data['diversidade_alimentar']}/9")
    
    with col2:
        st.subheader("🏥 Dados Clínicos")
        st.write(f"**Febre:** {'Sim' if patient_data.get('febre') else 'Não'}")
        st.write(f"**Diarreia:** {'Sim' if patient_data.get('diarreia') else 'Não'}")
        st.write(f"**Suplementação Ferro:** {'Sim' if patient_data.get('suplementacao_ferro') else 'Não'}")
        st.write(f"**Suplementação Vit A:** {'Sim' if patient_data.get('suplementacao_vit_a') else 'Não'}")
        
        # Campo para hemoglobina (apenas médico)
        hemoglobina = st.number_input("Hemoglobina (g/dL)", min_value=0.0, max_value=20.0, value=11.0, step=0.1)
        if st.button("💾 Atualizar Hemoglobina"):
            st.session_state.patients = [
                {**p, 'hemoglobina': hemoglobina} if p['nome'] == patient_data['nome'] else p 
                for p in st.session_state.patients
            ]
            st.success("✅ Hemoglobina atualizada!")
    
    st.divider()
    
    # Análise de Risco
    st.header("📊 Análise de Risco Completa")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        risco_anemia = patient_data.get('anemia_risco', 'N/A')
        cor_anemia = "🟢" if risco_anemia == "BAIXO" else "🟡" if risco_anemia == "MÉDIO" else "🔴"
        st.metric(
            "Risco de Anemia",
            f"{cor_anemia} {risco_anemia}",
            f"{patient_data.get('anemia_prob', 0):.1f}%"
        )
    
    with col4:
        risco_nutrition = patient_data.get('nutrition_risco', 'N/A')
        cor_nutrition = "🟢" if risco_nutrition == "BAIXO" else "🟡" if risco_nutrition == "MÉDIO" else "🔴"
        st.metric(
            "Risco de Fome Oculta",
            f"{cor_nutrition} {risco_nutrition}",
            f"{patient_data.get('nutrition_prob', 0):.1f}%"
        )
        if patient_data.get('deficits'):
            st.caption(f"Déficits: {', '.join(patient_data['deficits'])}")
    
    with col5:
        risco_food = patient_data.get('food_security_risco', 'N/A')
        cor_food = "🟢" if risco_food == "BAIXO" else "🟡" if risco_food == "MÉDIO" else "🔴"
        st.metric(
            "Insegurança Alimentar",
            f"{cor_food} {risco_food}",
            f"{patient_data.get('food_security_prob', 0):.1f}%"
        )
    
    # Fatores associados
    st.subheader("🔍 Fatores Associados ao Risco")
    
    fatores = []
    if patient_data.get('diversidade_alimentar', 0) < 4:
        fatores.append("Baixa diversidade alimentar")
    if patient_data.get('consumo_ferro', 0) == 0:
        fatores.append("Baixo consumo de ferro")
    if patient_data.get('consumo_vit_a', 0) == 0:
        fatores.append("Baixo consumo de Vitamina A")
    if patient_data.get('febre', 0) == 1:
        fatores.append("Febre recente")
    if patient_data.get('diarreia', 0) == 1:
        fatores.append("Diarreia recente")
    if patient_data.get('muac_mm', 0) < 125:
        fatores.append("MUAC baixo (< 125 mm)")
    
    if fatores:
        for f in fatores:
            st.write(f"• {f}")
    else:
        st.success("✅ Nenhum fator de risco adicional identificado")
    
    st.divider()
    
    # Decisão Clínica
    st.header("🏥 Decisão Clínica")
    
    col6, col7 = st.columns(2)
    
    with col6:
        diagnostico = st.text_area(
            "Diagnóstico e Observações Clínicas",
            height=100,
            placeholder="Descreva o diagnóstico, com base nos dados e exames..."
        )
        
        if st.button("💾 Registar Diagnóstico", use_container_width=True):
            if diagnostico:
                # Atualizar paciente com diagnóstico
                for p in st.session_state.patients:
                    if p['nome'] == patient_data['nome']:
                        p['diagnostico'] = diagnostico
                        p['data_diagnostico'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                        break
                st.success("✅ Diagnóstico registado com sucesso!")
            else:
                st.warning("⚠️ Por favor, insira o diagnóstico")
    
    with col7:
        prescricao = st.text_area(
            "Prescrição e Plano de Tratamento",
            height=100,
            placeholder="Medicamentos, suplementação, plano de seguimento..."
        )
        
        seguimento = st.date_input("Data do Próximo Controlo")
        
        if st.button("📅 Definir Plano de Seguimento", use_container_width=True):
            if prescricao:
                for p in st.session_state.patients:
                    if p['nome'] == patient_data['nome']:
                        p['prescricao'] = prescricao
                        p['proximo_controlo'] = seguimento.strftime('%d/%m/%Y')
                        break
                st.success(f"✅ Plano definido para {seguimento.strftime('%d/%m/%Y')}")
            else:
                st.warning("⚠️ Por favor, insira a prescrição")
    
    # Verificar se precisa de hemograma
    if patient_data.get('anemia_risco') == "ALTO" and patient_data.get('hemoglobina') is None:
        st.warning("⚠️ **Ação Recomendada:** Solicitar hemograma completo para confirmação de anemia")
    
    # Evolução (simulada)
    st.header("📈 Evolução do Paciente")
    
    # Dados simulados
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
    pesos = [10.0, 10.2, 10.5, 10.3, 10.8, patient_data['peso_kg']]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=meses,
        y=pesos,
        mode='lines+markers',
        name='Peso (kg)',
        line=dict(color='#2E7D32', width=3),
        marker=dict(size=10)
    ))
    fig.update_layout(
        title='Evolução do Peso',
        xaxis_title='Mês',
        yaxis_title='Peso (kg)',
        hovermode='x unified',
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)