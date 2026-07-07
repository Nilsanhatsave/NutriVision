import streamlit as st

st.set_page_config(
    page_title="NutriVision",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 NutriVision")
st.write("Plataforma Inteligente de Deteção de Anemia")

st.info("""
👩🏾‍⚕️ **Enfermeiro** - Triagem nutricional
👨🏾‍⚕️ **Médico** - Diagnóstico e tratamento
👨🏾‍🌾 **Agrónomo** - Planeamento agrícola
""")

if st.button("Acessar Enfermeiro"):
    st.success("Bem-vindo Enfermeiro!")

if st.button("Acessar Médico"):
    st.success("Bem-vindo Médico!")

if st.button("Acessar Agrónomo"):
    st.success("Bem-vindo Agrónomo!")