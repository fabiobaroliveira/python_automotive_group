import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Python AG",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e introdução
st.title("🐍 Bem-vindo a Python Automotive Group!")
st.markdown("""
    Selecione abaixo qual dashboard você deseja visualizar:
""")

# Colunas para os cards de seleção
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 🚗 Python Cars
    Dashboard de vendas de veículos seminovos
    """)
    if st.button("Acessar Python Cars", key="cars"):
        st.switch_page("pages/1_Python_Cars.py")

with col2:
    st.markdown("""
    ### 🚛 Python Parts
    Dashboard de vendas de acessórios automotivos
    """)
    if st.button("Acessar Python Parts", key="parts"):
        st.switch_page("pages/2_Python_Parts.py")

with col3:
    st.markdown("""
    ### 🧑‍🔧 Python Car Repair Shop
    Dashboard para uma oficina mecânica
    """)
    if st.button("Acessar Python Car Repair Shop", key="repair"):
        st.switch_page("pages/3_Python_Car_Repair_Shop.py")

# Rodapé
st.markdown("---", unsafe_allow_html=True)

st.markdown("""
<div style="font-family: Arial; background-color: #fafafa; padding: 10px; border-radius: 8px;">
    <p><strong>Python Automotive Group 🐍</strong> – Dados fictícios gerados para fins didáticos</p>
    <p>Criado por <strong>Fabio B. Oliveira</strong></p>
    <p>
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="18" style="vertical-align:middle; margin-right:5px;" />
        <a href="https://www.linkedin.com/in/fbarbosaoliveira/" target="_blank">LinkedIn: fbarbosaoliveira</a>
    </p>
</div>
""", unsafe_allow_html=True)