import streamlit as st
import pandas as pd

# Configuração inicial do app
st.set_page_config(page_title="Python Cars 🐍", layout="wide")

# Título do aplicativo
st.title('🚗 Dashboard de Vendas - Veículos Seminovos')

# Carrega os dados do arquivo CSV
@st.cache_data
def load_data():
        url = "https://raw.github.com/fabiobaroliveira/python_automotive_group/blob/main/pages/vendas_loja_seminovos.csv"
    try:
        return pd.read_csv(url, sep=";")
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()  # Retorna DataFrame vazio para evitar crash    

df = load_data()

# Sidebar para filtros

with st.sidebar:
    st.header("Filtros")

    # Filtro de datas
    df['Data_venda'] = pd.to_datetime(df['Data_venda'])
    data_inicial = df['Data_venda'].min()
    data_final = df['Data_venda'].max()

    intervalo_data = st.sidebar.date_input(
        "Selecione o período",
        value=(data_inicial, data_final),
        min_value=data_inicial,
        max_value=data_final
)
    # Filtro por marca (multiselect)
    marcas_disponiveis = sorted(df['Marca'].unique().tolist())
    marca_selecionada = st.multiselect(
        "Selecione uma ou mais marcas:",
        options=marcas_disponiveis,
        default=None
    )
     # Filtro por Modelo (multiselect)
    modelos_disponiveis = sorted(df['Modelo'].unique().tolist())
    modelo_selecionado = st.multiselect(
        "Selecione um ou mais modelos:",
        options=modelos_disponiveis,
        default=None
    )

    # Filtro por estado (multiselect)
    estados_disponiveis = sorted(df['Estado'].unique().tolist())
    estado_selecionado = st.multiselect(
        "Selecione um ou mais estados:",
        options=estados_disponiveis,
        default=None
    )

    # Filtro por lead (multiselect)
    lead_disponiveis = sorted(df['Origem_lead'].unique().tolist())
    lead_selecionado = st.multiselect(
        "Selecione um ou mais canais de lead:",
        options=lead_disponiveis,
        default=None
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
    mask = (df['Data_venda'] >= pd.to_datetime(intervalo_data[0])) & \
           (df['Data_venda'] <= pd.to_datetime(intervalo_data[1]))
    df_filtrado = df_filtrado.loc[mask]     

# Mostra resumo dos filtros aplicados
filtro_marca = ", ".join(marca_selecionada) if marca_selecionada else "Todas as marcas"
filtro_modelo = ", ".join(modelo_selecionado) if modelo_selecionado else "Todos os modelos"
filtro_estado = ", ".join(estado_selecionado) if estado_selecionado else "Todos os estados"
filtro_lead = ", ".join(lead_selecionado) if lead_selecionado else "Todos os leads"



st.write(f"**Filtros aplicados:** ")
st.write(f"**Marcas**: {filtro_marca} | **Modelos**: {filtro_modelo} ")
st.write(f"**Estados**: {filtro_estado} | **Canais de Leads**: {filtro_lead} ")
st.write(f"**Total de veículos vendidos:** {len(df_filtrado)}")

# Seção de análise por marca (sempre visível)
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
st.write("""
---
Python Cars 🐍 - Dados fictícios gerados para fins didáticos """
        )
