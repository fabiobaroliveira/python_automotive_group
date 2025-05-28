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
    agendamentos_df["data_agendamento"] = pd.to_datetime(agendamentos_df["data_agendamento"]).dt.date

    return clientes_df, veiculos_df, agendamentos_df

clientes_df, veiculos_df, agendamentos_df = load_data()

tab_agenda, tab_cadastros, tab_resumo = st.tabs(["📅 Agenda", "📖 Cadastros", "💰 Resumo Financeiro"])

with tab_agenda:
    #region AGENDA DO DIA

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

        # Adicione isso na seção da AGENDA DO DIA (substitua o código atual)
    st.title("📆 Agenda do dia")
    st.subheader(f"Hoje é {hoje.strftime('%d/%m/%Y')}")

    # Estatísticas simples
    col1, col2, col3 = st.columns(3)
    col1.metric("📆 Agendamentos", len(agenda_final))
    col2.metric("✅ Confirmados", len(confirmados))
    col3.metric("⏳ Horários Livres", 16 - len(agenda_final))  # Supondo 16 horários disponíveis (8h-17h)

    # Visualização da agenda
    st.dataframe(agenda_final, use_container_width=True, hide_index=True)

    # Seção para novo agendamento
    with st.expander("➕ NOVO AGENDAMENTO", expanded=False):
        with st.form(key='form_agendamento'):
            col1, col2 = st.columns(2)
            
            with col1:
                # Selecionar cliente existente ou novo
                opcao_cliente = st.radio("Cliente:", ["Existente", "Novo"])
                
                if opcao_cliente == "Existente":
                    cliente_selecionado = st.selectbox(
                        "Selecione o cliente:",
                        clientes_df['nome'].sort_values().unique()
                    )
                    id_cliente = clientes_df[clientes_df['nome'] == cliente_selecionado]['id_cliente'].values[0]
                    
                    # Mostrar veículos do cliente
                    veiculos_cliente = veiculos_df[veiculos_df['id_cliente'] == id_cliente]
                    if not veiculos_cliente.empty:
                        veiculo_selecionado = st.selectbox(
                            "Selecione o veículo:",
                            veiculos_cliente.apply(lambda x: f"{x['marca']} {x['modelo']} - {x['placa']}", axis=1)
                        )
                        id_veiculo = veiculos_cliente.iloc[veiculos_cliente.apply(lambda x: f"{x['marca']} {x['modelo']} - {x['placa']}", axis=1).tolist().index(veiculo_selecionado)]['id_veiculo']
                    else:
                        st.warning("Cliente não possui veículos cadastrados.")
                        id_veiculo = None
                else:
                    st.text_input("Nome completo*", key='novo_nome')
                    st.text_input("CPF*", key='novo_cpf')
                    st.text_input("Telefone*", key='novo_telefone')
                    st.text_input("Placa do veículo*", key='nova_placa')
                    st.text_input("Marca*", key='nova_marca')
                    st.text_input("Modelo*", key='novo_modelo')
                    id_cliente = None
                    id_veiculo = None
            
            with col2:
                # Horários disponíveis (exemplo: das 8h às 17h, de hora em hora)
                horarios_disponiveis = [f"{h:02d}:00" for h in range(8, 18)]
                horarios_ocupados = agenda_final['horario_agendamento'].tolist()
                horarios_livres = [h for h in horarios_disponiveis if h not in horarios_ocupados]
                
                horario = st.selectbox("Horário*", horarios_livres)
                tipo_servico = st.selectbox("Tipo de serviço*", 
                                        ["Troca de óleo", "Revisão periódica", "Alinhamento", 
                                        "Balanceamento", "Freios", "Suspensão"])
                valor = st.number_input("Valor estimado (R$)*", min_value=0.0, format="%.2f")
                observacoes = st.text_area("Observações")
            
            if st.form_submit_button("Agendar"):
                if opcao_cliente == "Novo":
                    # Adicionar novo cliente e veículo (simulação)
                    novo_id_cliente = clientes_df['id_cliente'].max() + 1
                    novo_id_veiculo = veiculos_df['id_veiculo'].max() + 1
                    
                    # Aqui você adicionaria aos DataFrames (na prática, salvaria no banco de dados)
                    st.success(f"Novo agendamento criado para {st.session_state.novo_nome} às {horario}")
                else:
                    st.success(f"Agendamento para {cliente_selecionado} às {horario} confirmado")
                
                # Simulação - adiciona à agenda (em uma aplicação real, você persistiria os dados)
                novo_agendamento = {
                    'id_agendamento': agendamentos_df['id_agendamento'].max() + 1,
                    'data_agendamento': hoje,
                    'horario_agendamento': horario,
                    'id_veiculo': id_veiculo if opcao_cliente == "Existente" else novo_id_veiculo,
                    'tipo_servico': tipo_servico,
                    'valor': valor,
                    'observacoes': observacoes,
                    'status': 'Confirmado'
                }
                
                # Atualiza o DataFrame (simulação)
                agendamentos_df = pd.concat([agendamentos_df, pd.DataFrame([novo_agendamento])], ignore_index=True)
                st.rerun()



    # Botões de ação para cada agendamento
    for _, row in agenda_final.iterrows():
        with st.expander(f"⚙️ Ações para {row['nome']} - {row['horario_agendamento']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"✅ Confirmar", key=f"confirm_{row['id_agendamento']}"):
                    # Atualizar status no DataFrame
                    agendamentos_df.loc[agendamentos_df['id_agendamento'] == row['id_agendamento'], 'status'] = 'Confirmado'
                    st.rerun()
            with col2:
                if st.button(f"✏️ Editar", key=f"edit_{row['id_agendamento']}"):
                    # Lógica para edição (poderíamos abrir um form com os dados atuais)
                    st.session_state.editando = row['id_agendamento']
            with col3:
                if st.button(f"❌ Cancelar", key=f"cancel_{row['id_agendamento']}"):
                    # Atualizar status no DataFrame
                    agendamentos_df.loc[agendamentos_df['id_agendamento'] == row['id_agendamento'], 'status'] = 'Cancelado'
                    st.rerun()

with tab_cadastros:
    #region CADASTROS
    # Consultas
    st.markdown("---")
    st.title("📖 Cadastros")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Clientes", "Veículos", "Serviços"])

    with tab1:
        st.subheader("📋 Lista de Clientes")

        filtro_cliente = st.text_input("🔎 Buscar por Nome ou CPF (início exato)", key="filtro_cliente_tab1").strip()

        if filtro_cliente:
            clientes_filtrados = clientes_df[
                clientes_df['nome'].str.lower().str.startswith(filtro_cliente.lower(), na=False) |
                clientes_df['cpf'].astype(str).str.startswith(filtro_cliente)
            ]

            if not clientes_filtrados.empty:
                st.dataframe(clientes_filtrados, use_container_width=True, hide_index=True)
            else:
                st.error("🔍 Nenhum cliente encontrado com os dados informados.")
        else:
            st.dataframe(clientes_df, use_container_width=True, hide_index=True)


    with tab2:
        st.subheader("🚗 Veículos por Cliente")

        # Campo de busca
        filtro = st.text_input("🔎 Buscar por Nome, CPF ou Placa").strip()

        if filtro:
            # Tenta localizar cliente primeiro
            clientes_encontrados = clientes_df[
                clientes_df['nome'].str.contains(filtro, case=False, na=False) |
                clientes_df['cpf'].astype(str).str.contains(filtro, na=False)
            ]

            # Se encontrar cliente, busca os veículos dele
            if not clientes_encontrados.empty:
                ids_clientes = clientes_encontrados['id_cliente'].tolist()

                # Filtra veículos pelos clientes encontrados
                veiculos_encontrados = veiculos_df[veiculos_df['id_cliente'].isin(ids_clientes)]
                veiculos_completo = veiculos_encontrados.merge(clientes_df, on="id_cliente", how="left")

                if not veiculos_completo.empty:
                    st.dataframe(veiculos_completo, use_container_width=True, hide_index=True)
                else:
                    st.warning("🙁 Cliente encontrado, mas não possui veículo cadastrado.")
            else:
                # Se não encontrou cliente, tenta pela placa diretamente
                veiculos_encontrados = veiculos_df[veiculos_df['placa'].str.upper().str.contains(filtro.upper(), na=False)]
                veiculos_completo = veiculos_encontrados.merge(clientes_df, on="id_cliente", how="left")

                if not veiculos_completo.empty:
                    st.dataframe(veiculos_completo, use_container_width=True, hide_index=True)
                else:
                    st.error("🔍 Nenhum resultado encontrado.")
        else:
            # Se nada for digitado, mostra todos
            veiculos_completo = veiculos_df.merge(clientes_df, on="id_cliente", how="left")
            st.dataframe(veiculos_completo, use_container_width=True, hide_index=True)

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

with tab_resumo:

    #region RESUMO FINANCEIRO
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
