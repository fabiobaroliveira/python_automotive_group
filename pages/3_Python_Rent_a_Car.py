import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date

st.set_page_config(page_title="Python Rent a Car 🐍", layout="wide")

st.title("Python Rent a Car ")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes_locadora.csv", sep=";")
    veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos_locadora.csv", sep=";")
    locacoes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/locacoes.csv", sep=";")
    lojas_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/lojas.csv", sep=";")
    return clientes_df, veiculos_df, locacoes_df, lojas_df

clientes_df, veiculos_df, locacoes_df,lojas_df = load_data()


# Merge dos dataframes
df = locacoes_df.merge(clientes_df, on="id_cliente") \
                .merge(veiculos_df, on="id_veiculo") \
                .merge(lojas_df, on="id_loja")

# Alterar tipos numéricos
df["valor_total"] = df["valor_total"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["valor_diaria"] = df["valor_diaria"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

# Conversão de datas
df["data_locacao"] = pd.to_datetime(df["data_locacao"], dayfirst=True)
df["data_devolucao"] = pd.to_datetime(df["data_devolucao"], dayfirst=True)


# Filtro por data
data_hoje = date.today()
df_hoje = df[df["data_locacao"].dt.date == data_hoje]

# KPIs
faturamento = df_hoje["valor_total"].sum()
num_locacoes = df_hoje["id_locacao"].nunique()
ticket_medio = faturamento / num_locacoes if num_locacoes > 0 else 0
ocupacao_frota = 100 * df[df["status"] == "Ativa"]["id_veiculo"].nunique() / veiculos_df["id_veiculo"].nunique()

# Layout do dashboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento do dia", f"R$ {faturamento:,.2f}")
col2.metric("Nº de locações", num_locacoes)
col3.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")
col4.metric("Ocupação da frota", f"{ocupacao_frota:.1f}%")


# Agrupamento por loja para gerar indicadores
df_lojas = df_hoje.groupby("nome_loja").agg(
    Faturamento=("valor_total", "sum"),
    Locações=("id_locacao", "count")
).sort_values("Faturamento", ascending=False).reset_index()

# Formatar valores para moeda
df_lojas["Faturamento"] = df_lojas["Faturamento"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Criar tabela com Plotly
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(df_lojas.columns),
        fill_color='darkolivegreen',
        font=dict(color='white', size=14),
        align='left'
    ),
    cells=dict(
        values=[df_lojas[col] for col in df_lojas.columns],
        fill_color='lightgray',
        align='left'
    )
)])

st.subheader("Desempenho por Loja (Hoje)")
st.plotly_chart(fig, use_container_width=True)
