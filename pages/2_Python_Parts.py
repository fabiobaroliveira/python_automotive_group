import streamlit as st
import pandas as pd

# Configuração inicial do app
st.set_page_config(page_title="Python Parts 🐍", layout="wide")

# Título do aplicativo
st.title('Vendas - Acessórios')

# Carrega os dados do arquivo CSV

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/vendas_acessorios_fake.csv"
    try:
        return pd.read_csv(url, sep=";")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()
        
df = load_data()
df["receita"] = df["Quantidade"] * df["Preço Unitário"]
df["lucro"] = df["receita"] - (df["Quantidade"] * df["Custo Unitário"])
df["mes"] = pd.to_datetime(df["Data Venda"]).dt.to_period("M").astype(str)


# Sidebar - filtros
st.sidebar.title("Filtros")
regiao = st.sidebar.multiselect("Região", options=df["regiao"].unique(), default=df["regiao"].unique())
canal = st.sidebar.multiselect("Canal de Venda", options=df["canal_venda"].unique(), default=df["canal_venda"].unique())
    

# Aplicar filtros
df_filtrado = df[df["regiao"].isin(regiao) & df["canal_venda"].isin(canal)]

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

