import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date , timedelta 
st.set_page_config(page_title="Python Rent a Car 🐍", layout="wide")

st.title("Python Rent a Car ")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes_locadora.csv", sep=";")
    veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos_locadora.csv", sep=";")
    locacoes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/locacoes.csv", sep=";")
    equipes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/equipes.csv", sep=";")
    lojas_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/lojas.csv", sep=";")
    
    return clientes_df, veiculos_df, locacoes_df, equipes_df, lojas_df

clientes_df, veiculos_df, locacoes_df,equipes_df, lojas_df = load_data()


# Merge dos dataframes
df = locacoes_df.merge(clientes_df, on="id_cliente") \
                .merge(veiculos_df, on="id_veiculo") \
                .merge(lojas_df, on="id_loja")\
                .merge(equipes_df, on="id_atendente")
                

# Alterar tipos numéricos
df["valor_total"] = df["valor_total"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["valor_diaria"] = df["valor_diaria"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

# Conversão de datas
df["data_locacao"] = pd.to_datetime(df["data_locacao"], dayfirst=True)
df["data_devolucao"] = pd.to_datetime(df["data_devolucao"], dayfirst=True)


# Opções de filtro
filtro_data = st.selectbox(
    "Filtrar por período:",
    ("Hoje", "Últimos 7 dias", "Último mês", "Período completo")
)

# Define o intervalo de datas
data_fim = df["data_locacao"].max().date()
data_inicio = df["data_locacao"].min().date()

if filtro_data == "Hoje":
        data_inicio_filtro = date.today()
        data_fim_filtro = date.today()
elif filtro_data == "Últimos 7 dias":
        data_inicio_filtro = date.today() - timedelta(days=6)
        data_fim_filtro = date.today()
elif filtro_data == "Último mês":
        data_inicio_filtro = date.today() - timedelta(days=30)
        data_fim_filtro = date.today()
else:  # Período completo
        data_inicio_filtro = data_inicio
        data_fim_filtro = data_fim


# Aplica o filtro
df_filtrado = df[
        (df["data_locacao"].dt.date >= data_inicio_filtro) &
        (df["data_locacao"].dt.date <= data_fim_filtro)
]

# KPIs
faturamento = df_filtrado["valor_total"].sum()
num_locacoes = df_filtrado["id_locacao"].nunique()
ticket_medio = faturamento / num_locacoes if num_locacoes > 0 else 0




def format_currency(value):
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:,.1f} mi"
    elif value >= 1_000:
        return f"R$ {value / 1_000:,.1f} mil"
    else:
        return f"R$ {value:,.2f}"

# Layout do dashboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento do período", format_currency(faturamento))
#col2.metric
col3.metric("Nº de locações", num_locacoes)
col4.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")



# Agrupamento por loja para gerar indicadores
df_lojas = df_filtrado.groupby("nome_loja").agg(
    Faturamento=("valor_total", "sum"),
    Locações=("id_locacao", "count")
).sort_values("Faturamento", ascending=False).reset_index()

# Formatar valores para moeda
df_lojas["Faturamento"] = df_lojas["Faturamento"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.dataframe(df_lojas)

# Rodapé
st.markdown("---")
st.markdown("Python Rent a Car 🐍 - Dados fictícios gerados para fins didáticos")
