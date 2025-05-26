import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Python Rent a Car 🐍", layout="wide")

st.title("Python Rent a Car ")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes.csv")
    veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos.csv")
    agendamentos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/agendamentos.csv")