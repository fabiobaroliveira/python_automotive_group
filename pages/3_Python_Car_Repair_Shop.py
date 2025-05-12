import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Python Car Repair Shop 🐍", layout="wide")

st.title("🧑‍🔧 Python Car Repair Shop")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes.csv")
    veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos.csv")
    agendamentos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/agendamentos.csv")
# Converter a coluna de data para datetime
    agendamentos_df['status'] = agendamentos_df['status'].replace('Confirmardo', 'Confirmado')
    agendamentos_df["data_agendamento"] = pd.to_datetime(agendamentos_df["data_agendamento"]).dt.date

    return clientes_df, veiculos_df, agendamentos_df

clientes_df, veiculos_df, agendamentos_df = load_data()

# Agendado do Dia

# Filtra agendamentos apenas para a data de hoje
hoje = date.today()
agendamentos_hoje = agendamentos_df[agendamentos_df["data_agendamento"] == hoje]
# Junta com veículos
agenda_veiculo = agendamentos_hoje.merge(veiculos_df, on="id_veiculo", how="left")
# Junta com clientes
agenda_completa = agenda_veiculo.merge(clientes_df[["id_cliente", "nome"]], on="id_cliente", how="left")

# Seleciona e reorganiza as colunas
agenda_final = agenda_completa[[
    "id_agendamento",
    "horario_agendamento",
    "nome",
    "marca",
    "modelo",
    "tipo_servico",
    "status"
]]

# Ordena por horário
agenda_final = agenda_final.sort_values(by="horario_agendamento").reset_index(drop=True)

# Filtra os confirmardos (status "Confirmado")
confirmados = agenda_final[agenda_final["status"] == "Confirmado"]

st.title("📆 Agenda do dia")
#subititulo
st.subheader(f"Hoje é {hoje.strftime('%d/%m/%Y')}")
# Estatísticas simples
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("📆 Agendamentos", len(agenda_final))
col2.metric("✅ Confirmados", len(confirmados))
st.dataframe(agenda_final,use_container_width=True, hide_index=True)

# Consultas
st.markdown("---")
st.title("📖 Cadastros")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Clientes", "Veículos", "Serviços"])

with tab1:
    st.subheader("📋 Lista de Clientes")
    st.dataframe(clientes_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("🚗 Veículos por Cliente")
    st.dataframe(veiculos_df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📅 Serviços")
    

    # Converter para datetime se ainda não for
    agendamentos_df['data_agendamento'] = pd.to_datetime(agendamentos_df['data_agendamento'])
    
    # Seletor de data range
    min_date = agendamentos_df['data_agendamento'].min().date()
    max_date = agendamentos_df['data_agendamento'].max().date()
    
    dates = st.date_input(
        "Selecione o período:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_filter_tab3"
    )
    
    # Aplica filtro de data
    if len(dates) == 2:
        start_date, end_date = dates
        mask = (agendamentos_df['data_agendamento'].dt.date >= start_date) & \
               (agendamentos_df['data_agendamento'].dt.date <= end_date)
        df_filtrado = agendamentos_df[mask]
    else:
        df_filtrado = agendamentos_df

    col1, col2 = st.columns(2)
    col1.metric("📆 Agendamentos", len(df_filtrado))
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)


# Metricas principais
st.markdown("---")
st.title("💰 Resumo Financeiro")
st.markdown("---")

confirmardos_df = agendamentos_df[agendamentos_df['status'] == 'Confirmado']

valor_total_previsto = agendamentos_df['valor'].sum()
valor_total_realizado = confirmardos_df['valor'].sum()
valor_medio = agendamentos_df['valor'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Receita Total [Prevista]", f"R$ {valor_total_previsto:,.2f}")
col2.metric("Receita Total [Realizado]", f"R$ {valor_total_realizado:,.2f}")
col3.metric("Receita Média", f"R$ {valor_medio:,.2f}")

# --- Gráficos ---

col1, col2 = st.columns(2)
with col1:
    st.subheader("🔧 Serviços Mais Comuns")
    servicos_count = agendamentos_df['tipo_servico'].value_counts()
    st.bar_chart(servicos_count.head(2),horizontal=True)

with col2:
    st.subheader("🚗 Marcas Mais Atendidas")
    marcas_count = veiculos_df['marca'].value_counts()
    st.bar_chart(marcas_count.head(2),horizontal=True)


# Rodapé
st.markdown("---")
st.markdown("Python Car Repair Shop 🐍 - Dados fictícios gerados para fins didáticos")
