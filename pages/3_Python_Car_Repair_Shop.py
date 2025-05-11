
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Python Car Repair Shop 🐍", layout="wide")

st.title("🧑‍🔧 Python Car Repair Shop")
st.markdown("---")

# Carregar os dados
clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes.csv")
veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos.csv")
agendamentos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/agendamentos.csv")

# Converter data_agendamento para tipo datetime.date
agendamentos_df["data_agendamento"] = pd.to_datetime(agendamentos_df["data_agendamento"]).dt.date

agendamentos_df['cliente_id'] = agendamentos_df['cliente_id'].astype(str)
clientes_df['id_cliente'] = clientes_df['id_cliente'].astype(str)

#Agendado do Dia

# Filtra agendamentos apenas para a data de hoje
hoje = date.today()
agendamentos_hoje = agendamentos_df[agendamentos_df["data_agendamento"] == hoje]
# Junta com veículos
agenda_veiculo = agendamentos_hoje.merge(veiculos_df, on="id_veiculo", how="left")
# Junta com clientes
agenda_completa = agenda_veiculo.merge(clientes_df[["id_cliente", "nome"]],
                                       left_on="cliente_id", right_on="id_cliente", how="left")

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

# Filtra os confirmardos (status "Confirmardo")
confirmardos = agenda_final[agenda_final["status"] == "Confirmardo"]

st.title("📆 Agenda do dia")
#subititulo
st.subheader(f"Hoje é {hoje.strftime('%d/%m/%Y')}")
# Estatísticas simples
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("📆 Agendamentos", len(agenda_final))
col2.metric("✅ Confirmardos", len(confirmardos))
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
    st.dataframe(agendamentos_df, use_container_width=True, hide_index=True)


# Metricas principais
st.markdown("---")
st.title("💰 Resumo Financeiro")
st.markdown("---")

confirmardos_df = agendamentos_df[agendamentos_df['status'] == 'Confirmardo']

valor_total_previsto = agendamentos_df['valor'].sum()
valor_total_realizado = confirmardos_df['valor'].sum()
valor_medio = agendamentos_df['valor'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Receita Total [Prevista]", f"R$ {valor_total_previsto:,.2f}")
col2.metric("Receita Total [Realizado]", f"R$ {valor_total_realizado:,.2f}")
col3.metric("Receita Média", f"R$ {valor_medio:,.2f}")

# Rodapé
st.markdown("---")
st.markdown("Python Car Repair 🐍 - Dados fictícios gerados para fins didáticos")
