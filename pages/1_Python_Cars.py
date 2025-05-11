import streamlit as st
import pandas as pd

# Configuração inicial do app
st.set_page_config(page_title="Python Cars 🐍", layout="wide")

# Título do aplicativo
st.title('🚗 Dashboard de Vendas - Veículos Seminovos')

# Carrega os dados do arquivo CSV
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/vendas_loja_seminovos.csv"
    try:
        return pd.read_csv(url, sep=";")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

df = load_data()

# Sidebar para filtros
with st.sidebar:
    
    st.header("Filtros")
    
    df['Data_venda'] = pd.to_datetime(df['Data_venda'])
    data_inicial = df['Data_venda'].min()
    data_final = df['Data_venda'].max()
    
    marca_selecionada = st.multiselect(
        "Selecione uma ou mais marcas:",
        options=sorted(df['Marca'].unique())
    )

    modelo_selecionado = st.multiselect(
        "Selecione um ou mais modelos:",
        options=sorted(df['Modelo'].unique())
    )

    estado_selecionado = st.multiselect(
        "Selecione um ou mais estados:",
        options=sorted(df['Estado'].unique())
    )

    lead_selecionado = st.multiselect(
        "Selecione um ou mais canais de lead:",
        options=sorted(df['Origem_lead'].unique())
    )

# Aplica os filtros
df_filtrado = df.copy()

if marca_selecionada:
    df_filtrado = df_filtrado[df_filtrado['Marca'].isin(marca_selecionada)]
if modelo_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Modelo'].isin(modelo_selecionado)]
if estado_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Estado'].isin(estado_selecionado)]
if lead_selecionado:
    df_filtrado = df_filtrado[df_filtrado['Origem_lead'].isin(lead_selecionado)]

if len(intervalo_data) == 2:
    inicio, fim = pd.to_datetime(intervalo_data[0]), pd.to_datetime(intervalo_data[1])
    df_filtrado = df_filtrado[(df_filtrado['Data_venda'] >= inicio) & (df_filtrado['Data_venda'] <= fim)]

# Resumo dos filtros aplicados
st.write("**Filtros aplicados:**")
st.write(f"**Marcas**: {', '.join(marca_selecionada) if marca_selecionada else 'Todas'} | "
         f"**Modelos**: {', '.join(modelo_selecionado) if modelo_selecionado else 'Todos'}")
st.write(f"**Estados**: {', '.join(estado_selecionado) if estado_selecionado else 'Todos'} | "
         f"**Leads**: {', '.join(lead_selecionado) if lead_selecionado else 'Todos'}")
st.write(f"**Total de veículos vendidos:** {len(df_filtrado)}")

# Visualizações Seção de análise por marca (sempre visível)
st.subheader("Vendas por Marca")
if marca_selecionada:
    # Se há marcas selecionadas, mostra apenas as selecionadas
    vendas_por_marca = df_filtrado.groupby("Marca").size()
else:
    # Se nenhuma marca selecionada, mostra todas
    vendas_por_marca = df_filtrado.groupby("Marca").size()

st.bar_chart(vendas_por_marca, 
            x_label="Unidades Vendidas", 
            color="#494C3A", 
            horizontal=True)

# Seção de análise por modelo
st.subheader("Vendas por Modelo")
vendas_por_modelo = df_filtrado.groupby("Modelo").size()

if modelo_selecionado:
    # Se há estados selecionados, mostra apenas os selecionados
    vendas_por_modelo = df_filtrado.groupby("Modelo").size()
else:
    # Se nenhum estado selecionado, mostra todos
    vendas_por_modelo = df_filtrado.groupby("Modelo").size()

st.bar_chart(vendas_por_modelo,
                color="#494C3A",
                horizontal=True,
                use_container_width=True)    

# Seção de análise por estado
st.subheader("Vendas por Estado")
if estado_selecionado:
    # Se há estados selecionados, mostra apenas os selecionados
    vendas_por_estado = df_filtrado.groupby("Estado").size()
else:
    # Se nenhum estado selecionado, mostra todos
    vendas_por_estado = df_filtrado.groupby("Estado").size()

st.bar_chart(vendas_por_estado, 
            x_label="Unidades Vendidas", 
            color="#494C3A", 
            horizontal=True)

# Seção de análise por Canal
st.subheader("Vendas por Lead")
if lead_selecionado:
    # Se há estados selecionados, mostra apenas os selecionados
    vendas_por_lead = df_filtrado.groupby("Origem_lead").size()
else:
    # Se nenhum estado selecionado, mostra todos
    vendas_por_lead = df_filtrado.groupby("Origem_lead").size()

st.bar_chart(vendas_por_lead, 
            x_label="Unidades Vendidas", 
            color="#494C3A", 
            horizontal=True)


# Rodapé
st.markdown("---")
st.markdown("Python Cars 🐍 - Dados fictícios gerados para fins didáticos")
