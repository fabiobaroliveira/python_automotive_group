import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Python AG",
    page_icon="🐍",
    layout="wide"
)

# Título e introdução
st.title("🐍 Bem-vindo a Python Automotive Group!")
st.markdown("""
    Selecione abaixo qual dashboard você deseja visualizar:
""")

# Colunas para os cards de seleção
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🚗 Python Cars
    Dashboard de vendas de veículos seminovos
    """)
    if st.button("Acessar Python Cars", key="cars"):
        st.switch_page("pages/1_🚗_Python_Cars.py")

with col2:
    st.markdown("""
    ### 🔧 Python Parts
    Dashboard de vendas de acessórios automotivos
    """)
    if st.button("Acessar Python Parts", key="parts"):
        st.switch_page("pages/2_🔧_Python_Parts.py")

# Rodapé
st.markdown("---")
st.markdown("Python Automotive Group 🐍 - Dados fictícios gerados para fins didáticos")
st.write("Criado por Fabio B. Oliveira")
st.write("Linkedin: https://www.linkedin.com/in/fbarbosaoliveira/")