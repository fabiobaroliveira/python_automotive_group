import streamlit as st
import pandas as pd

# Configuração inicial do app
st.set_page_config(page_title="Python Parts 🐍", layout="wide")

# Título do aplicativo
st.title('Resumo - Vendas de Acessórios')

# Carregar os dados

# URL bruta do arquivo CSV no GitHub
url = "https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/vendas_acessorios_fake.csv"
df = pd.read_csv(url, parse_dates=["data_venda"])
df["receita"] = df["quantidade"] * df["preco_unitario"]
df["lucro"] = df["receita"] - (df["quantidade"] * df["custo_unitario"])
df["mes"] = df["data_venda"].dt.to_period("M").astype(str)

# Sidebar - filtros
st.sidebar.title("Filtros")
periodo = st.sidebar.selectbox("Período", options=[ "Todo o período", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Último ano"])
mes = []
if periodo == "Todo o período":
    mes = df["mes"].unique() 
elif periodo == "Último mês":
    mes = [df["mes"].max()]
elif periodo == "Últimos 3 meses":
    mes = df["mes"].unique()[-3:]
elif periodo == "Últimos 6 meses":
    mes = df["mes"].unique()[-6:]
elif periodo == "Último ano":
    mes = df["mes"].unique()[-12:]
 

regiao = st.sidebar.multiselect("Região", options=df["regiao"].unique(), default=df["regiao"].unique())
canal = st.sidebar.multiselect("Canal de Venda", options=df["canal_venda"].unique(), default=df["canal_venda"].unique())
    

# Aplicar filtros
df_filtrado = df[df["regiao"].isin(regiao) & df["canal_venda"].isin(canal) & df["mes"].isin(mes)]
# Métricas principais
st.metric("Receita Total", f"R$ {df_filtrado['receita'].sum():,.2f}")
st.metric("Lucro Bruto", f"R$ {df_filtrado['lucro'].sum():,.2f}")
st.metric("Quantidade Vendida", int(df_filtrado["quantidade"].sum()))

# Gráfico de receita por mês
st.subheader("Receita por Mês")
receita_mes = df_filtrado.groupby("mes")["receita"].sum().reset_index()
st.line_chart(receita_mes.set_index("mes"))

# Tabela top produtos
st.subheader("Produtos por Receita")
top = df_filtrado.groupby("produto_nome")["receita"].sum().sort_values(ascending=False).head(5)
st.table(top.reset_index())

# Rodapé
st.markdown("---")
st.markdown("Python Parts 🐍 - Dados fictícios gerados para fins didáticos")
