import streamlit as st
import pandas as pd
import altair as alt

# Configuração
st.set_page_config(page_title="Python Parts 🐍", layout="wide")
st.title('📦 Resumo - Vendas de Acessórios')

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/vendas_acessorios_fake.csv"
    df = pd.read_csv(url, parse_dates=["data_venda"])
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["lucro"] = df["receita"] - (df["quantidade"] * df["custo_unitario"])
    df["mes"] = df["data_venda"].dt.to_period("M").astype(str)
    return df.sort_values("data_venda")

df = load_data()

# Sidebar
st.sidebar.title("Filtros")
periodo = st.sidebar.selectbox(
    "Período", 
    options=["Todo o período", "Último mês", "Últimos 3 meses", "Últimos 6 meses", "Último ano"]
)

mes_options = {
    "Todo o período": df["mes"].unique(),
    "Último mês": [df["mes"].max()],
    "Últimos 3 meses": df["mes"].unique()[-3:],
    "Últimos 6 meses": df["mes"].unique()[-6:],
    "Último ano": df["mes"].unique()[-12:]
}
mes = mes_options[periodo]

regiao = st.sidebar.multiselect(
    "Região", 
    options=df["regiao"].unique(), 
    default=df["regiao"].unique()
)
canal = st.sidebar.multiselect(
    "Canal de Venda", 
    options=df["canal_venda"].unique(), 
    default=df["canal_venda"].unique()
)

# Filtros
df_filtrado = df[df["regiao"].isin(regiao) & df["canal_venda"].isin(canal) & df["mes"].isin(mes)]

# Métricas
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Receita Total", f"R$ {df_filtrado['receita'].sum():,.2f}")
with col2:
    st.metric("Lucro Bruto", f"R$ {df_filtrado['lucro'].sum():,.2f}")
with col3:
    st.metric("Quantidade Vendida", int(df_filtrado["quantidade"].sum()))

# Gráficos
st.subheader("📈 Receita por Mês")
receita_mes = df_filtrado.groupby("mes")["receita"].sum().reset_index()
st.altair_chart(
    alt.Chart(receita_mes).mark_line().encode(
        x="mes:T",
        y="receita:Q"
    ), use_container_width=True
)

st.subheader("🏆 Top Produtos")
top_produtos = df_filtrado.groupby("produto_nome")["receita"].sum().nlargest(5)
st.dataframe(
    top_produtos.reset_index().style.format({"receita": "R$ {:.2f}"}),
    hide_index=True
)

# Rodapé
st.markdown("---")
st.markdown("Python Parts 🐍 - Dados fictícios para fins didáticos")