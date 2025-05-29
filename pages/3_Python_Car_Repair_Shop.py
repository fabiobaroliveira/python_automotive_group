import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Python Car Repair Shop 🐍", layout="wide")

st.title("🧑‍🔧 Python Car Repair Shop")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_initial_data():
    try:
        clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes.csv")
        veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos.csv")
        agendamentos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/agendamentos.csv", sep=";")
    except Exception as e:
        st.error(f"Erro ao carregar dados dos arquivos CSV: {e}")
        clientes_df = pd.DataFrame(columns=["id_cliente", "nome", "cpf", "telefone"])
        veiculos_df = pd.DataFrame(columns=["id_veiculo", "id_cliente", "placa", "marca", "modelo"])
        agendamentos_df = pd.DataFrame(columns=["id_agendamento", "id_veiculo", "data_agendamento", "horario_agendamento", "tipo_servico", "valor", "observacoes", "status"])
        return clientes_df, veiculos_df, agendamentos_df

    if "data_agendamento" in agendamentos_df.columns:
        agendamentos_df["data_agendamento"] = pd.to_datetime(agendamentos_df["data_agendamento"], errors="coerce").dt.date

    def safe_astype(df, col, dtype):
        if col in df.columns:
            try:
                if pd.api.types.is_integer_dtype(dtype) and df[col].isnull().any():
                    # Use Int64 for integers if NaNs are present
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
                elif pd.api.types.is_float_dtype(dtype):
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)
                elif pd.api.types.is_string_dtype(dtype) or dtype == str:
                     df[col] = df[col].fillna("").astype(str)
                else:
                    df[col] = df[col].astype(dtype)
            except Exception as e:
                st.warning(f"Não foi possível converter a coluna ", {col}, " para {dtype}: {e}")
        return df

    clientes_df = safe_astype(clientes_df, "id_cliente", int)
    veiculos_df = safe_astype(veiculos_df, "id_veiculo", int)
    veiculos_df = safe_astype(veiculos_df, "id_cliente", int)
    agendamentos_df = safe_astype(agendamentos_df, "id_agendamento", int)
    agendamentos_df = safe_astype(agendamentos_df, "id_veiculo", "Int64")
    agendamentos_df = safe_astype(agendamentos_df, "valor", float)

    if "observacoes" not in agendamentos_df.columns:
        agendamentos_df["observacoes"] = ""
    agendamentos_df = safe_astype(agendamentos_df, "observacoes", str)

    return clientes_df, veiculos_df, agendamentos_df

initial_clientes, initial_veiculos, initial_agendamentos = load_initial_data()

if "clientes_df" not in st.session_state:
    st.session_state.clientes_df = initial_clientes.copy()
if "veiculos_df" not in st.session_state:
    st.session_state.veiculos_df = initial_veiculos.copy()
if "agendamentos_df" not in st.session_state:
    st.session_state.agendamentos_df = initial_agendamentos.copy()

def add_cliente(nome, cpf, telefone):
    df = st.session_state.clientes_df
    novo_id = (df["id_cliente"].max() + 1) if not df.empty else 1
    novo_cliente = pd.DataFrame([{"id_cliente": novo_id, "nome": nome, "cpf": cpf, "telefone": telefone}])
    st.session_state.clientes_df = pd.concat([df, novo_cliente], ignore_index=True)
    st.session_state.clientes_df["id_cliente"] = st.session_state.clientes_df["id_cliente"].astype(int)
    return novo_id

def add_veiculo(id_cliente, placa, marca, modelo):
    df = st.session_state.veiculos_df
    novo_id = (df["id_veiculo"].max() + 1) if not df.empty else 1
    novo_veiculo = pd.DataFrame([{
        "id_veiculo": novo_id,
        "id_cliente": int(id_cliente),
        "placa": placa.upper(),
        "marca": marca,
        "modelo": modelo
    }])
    st.session_state.veiculos_df = pd.concat([df, novo_veiculo], ignore_index=True)
    st.session_state.veiculos_df["id_veiculo"] = st.session_state.veiculos_df["id_veiculo"].astype(int)
    st.session_state.veiculos_df["id_cliente"] = st.session_state.veiculos_df["id_cliente"].astype(int)
    return novo_id

def add_agendamento(id_veiculo, data, horario, tipo_servico, valor, observacoes, status="Confirmado"):
    df = st.session_state.agendamentos_df
    novo_id = (df["id_agendamento"].max() + 1) if not df.empty else 1
    novo_agendamento = pd.DataFrame([{
        "id_agendamento": novo_id,
        "id_veiculo": int(id_veiculo) if pd.notna(id_veiculo) else pd.NA,
        "data_agendamento": data,
        "horario_agendamento": horario,
        "tipo_servico": tipo_servico,
        "valor": float(valor) if valor else 0.0,
        "observacoes": str(observacoes) if observacoes else "",
        "status": status
    }])
    st.session_state.agendamentos_df = pd.concat([df, novo_agendamento], ignore_index=True)
    st.session_state.agendamentos_df["id_agendamento"] = st.session_state.agendamentos_df["id_agendamento"].astype(int)
    st.session_state.agendamentos_df["id_veiculo"] = st.session_state.agendamentos_df["id_veiculo"].astype("Int64")
    st.session_state.agendamentos_df["valor"] = pd.to_numeric(st.session_state.agendamentos_df["valor"], errors="coerce").fillna(0)
    st.session_state.agendamentos_df["observacoes"] = st.session_state.agendamentos_df["observacoes"].fillna("").astype(str)

tab_agenda, tab_cadastros, tab_resumo = st.tabs(["📅 Agenda", "📖 Cadastros", "💰 Resumo Financeiro"])

with tab_agenda:
    st.title("📆 Agenda do dia")
    hoje = date.today()
    st.subheader(f"Hoje é {hoje.strftime("%d/%m/%Y")}")

    agendamentos_df_today = st.session_state.agendamentos_df
    veiculos_df_today = st.session_state.veiculos_df
    clientes_df_today = st.session_state.clientes_df

    if not agendamentos_df_today.empty and "data_agendamento" in agendamentos_df_today.columns:
        agendamentos_hoje = agendamentos_df_today[agendamentos_df_today["data_agendamento"] == hoje].copy()
    else:
        agendamentos_hoje = pd.DataFrame(columns=agendamentos_df_today.columns)

    agendamentos_hoje["id_veiculo"] = agendamentos_hoje["id_veiculo"].astype("Int64")
    veiculos_df_today["id_veiculo"] = veiculos_df_today["id_veiculo"].astype(int)
    clientes_df_today["id_cliente"] = clientes_df_today["id_cliente"].astype(int)

    agenda_completa = pd.DataFrame()
    if not agendamentos_hoje.empty and not veiculos_df_today.empty:
        try:
            # Ensure id_veiculo in veiculos_df_today is compatible for merge (e.g., Int64 if agendamentos_hoje uses Int64)
            veiculos_df_today_merged = veiculos_df_today.copy()
            veiculos_df_today_merged["id_veiculo"] = veiculos_df_today_merged["id_veiculo"].astype("Int64")

            agenda_veiculo = agendamentos_hoje.merge(veiculos_df_today_merged, on="id_veiculo", how="left")
            agenda_veiculo["id_cliente"] = agenda_veiculo["id_cliente"].astype("Int64")

            if not agenda_veiculo.empty and not clientes_df_today.empty:
                clientes_nomes = clientes_df_today[["id_cliente", "nome"]].copy()
                clientes_nomes["id_cliente"] = clientes_nomes["id_cliente"].astype("Int64")
                agenda_completa = agenda_veiculo.merge(clientes_nomes, on="id_cliente", how="left")
            else:
                agenda_completa = agenda_veiculo
        except Exception as e:
            st.error(f"Erro durante o merge dos dados da agenda: {e}")
            agenda_completa = agendamentos_hoje
    else:
        agenda_completa = agendamentos_hoje

    colunas_agenda_final = ["id_agendamento", "horario_agendamento", "nome", "marca", "modelo", "tipo_servico", "status"]
    for col in colunas_agenda_final:
        if col not in agenda_completa.columns:
            agenda_completa[col] = None
    agenda_final = agenda_completa[colunas_agenda_final]

    if "horario_agendamento" in agenda_final.columns:
        agenda_final = agenda_final.sort_values(by="horario_agendamento").reset_index(drop=True)

    confirmados = pd.DataFrame()
    if "status" in agenda_final.columns:
        confirmados = agenda_final[agenda_final["status"].astype(str).str.lower() == "confirmado"]

    num_agendamentos = len(agenda_final)
    num_confirmados = len(confirmados)
    horarios_livres = max(0, 10 - num_agendamentos)

    col1, col2, col3 = st.columns(3)
    col1.metric("📆 Agendamentos Hoje", num_agendamentos)
    col2.metric("✅ Confirmados Hoje", num_confirmados)
    col3.metric("⏳ Horários Livres Hoje", horarios_livres)

    st.dataframe(agenda_final, use_container_width=True, hide_index=True)

    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if st.button("➕ Novo Agendamento"):
        st.session_state.show_form = True

    if st.session_state.show_form:
        with st.form(key="form_agendamento"):
            st.subheader("📝 Novo Agendamento")
            col1, col2 = st.columns(2)
            id_veiculo_selecionado = None
            cliente_nome_selecionado = None
            id_cliente_para_filtro = None # Variavel para guardar o ID do cliente selecionado

            with col1:
                opcao_cliente = st.radio("Tipo de Cliente:", ["Existente", "Novo"], horizontal=True, key="radio_cliente_tipo")

                if opcao_cliente == "Existente":
                    clientes_list = st.session_state.clientes_df["nome"].sort_values().unique()
                    if len(clientes_list) > 0:
                        cliente_selecionado = st.selectbox("Selecione o cliente:", clientes_list, key="select_cliente_existente", index=None, placeholder="Selecione...")
                        if cliente_selecionado:
                            id_cliente_df = st.session_state.clientes_df[st.session_state.clientes_df["nome"] == cliente_selecionado]
                            if not id_cliente_df.empty:
                                # Guarda o ID do cliente para filtrar veículos
                                id_cliente_para_filtro = int(id_cliente_df["id_cliente"].values[0])
                                cliente_nome_selecionado = cliente_selecionado
                            else:
                                st.error("Cliente selecionado não encontrado (erro interno).")
                    else:
                        st.warning("Nenhum cliente cadastrado.")

                    # Filtrar veículos APÓS obter o id_cliente_para_filtro
                    if id_cliente_para_filtro is not None:
                        # Garante que a coluna id_cliente em veiculos_df é int para comparação
                        st.session_state.veiculos_df["id_cliente"] = st.session_state.veiculos_df["id_cliente"].astype(int)
                        veiculos_cliente = st.session_state.veiculos_df[st.session_state.veiculos_df["id_cliente"] == id_cliente_para_filtro]

                        if not veiculos_cliente.empty:
                            veiculo_display = veiculos_cliente.apply(lambda x: f"{x["marca"]} {x["modelo"]} - {x["placa"]}", axis=1).tolist()
                            veiculo_selecionado_display = st.selectbox("Selecione o veículo:", veiculo_display, key="select_veiculo_existente", index=None, placeholder="Selecione...")
                            if veiculo_selecionado_display:
                                idx = veiculo_display.index(veiculo_selecionado_display)
                                id_veiculo_selecionado = int(veiculos_cliente.iloc[idx]["id_veiculo"])
                        else:
                            st.warning("Cliente não possui veículos cadastrados.")
                    # Se cliente_selecionado mas id_cliente_para_filtro é None (erro anterior), não mostra veículos
                    elif cliente_selecionado:
                         st.warning("Selecione um cliente válido para ver os veículos.")

                else: # Novo Cliente
                    novo_nome = st.text_input("Nome completo*", key="input_novo_nome")
                    novo_cpf = st.text_input("CPF*", key="input_novo_cpf")
                    novo_telefone = st.text_input("Telefone*", key="input_novo_telefone")
                    nova_placa = st.text_input("Placa do veículo*", key="input_nova_placa").upper()
                    nova_marca = st.text_input("Marca*", key="input_nova_marca")
                    novo_modelo = st.text_input("Modelo*", key="input_novo_modelo")

            with col2:
                horarios_disponiveis = [f"{h:02d}:00" for h in range(8, 18)]
                horarios_ocupados = []
                if "horario_agendamento" in agendamentos_hoje.columns:
                    horarios_ocupados = agendamentos_hoje["horario_agendamento"].tolist()
                horarios_livres = [h for h in horarios_disponiveis if h not in horarios_ocupados]

                horario = st.selectbox("Horário*", horarios_livres, key="select_horario", index=None, placeholder="Selecione...")
                tipo_servico = st.selectbox("Tipo de serviço*", ["Troca de óleo", "Revisão periódica", "Alinhamento", "Balanceamento", "Freios", "Suspensão"], key="select_servico", index=None, placeholder="Selecione...")
                valor = st.number_input("Valor estimado (R$)*", min_value=0.0, value=50.0, format="%.2f", key="input_valor")
                observacoes = st.text_area("Observações", key="input_obs")

            col_submit, col_cancel, _ = st.columns([1, 1, 4])
            with col_submit:
                submitted = st.form_submit_button("✅ Confirmar")
            with col_cancel:
                cancelled = st.form_submit_button("❌ Cancelar")

            if submitted:
                valid = True
                current_id_veiculo = None
                current_cliente_nome = None

                if opcao_cliente == "Novo":
                    if not all([novo_nome, novo_cpf, novo_telefone, nova_placa, nova_marca, novo_modelo]):
                        st.error("Preencha todos os campos obrigatórios (*) para novo cliente e veículo.")
                        valid = False
                    else:
                        try:
                            novo_id_cliente = add_cliente(nome=novo_nome, cpf=novo_cpf, telefone=novo_telefone)
                            current_id_veiculo = add_veiculo(id_cliente=novo_id_cliente, placa=nova_placa, marca=nova_marca, modelo=novo_modelo)
                            current_cliente_nome = novo_nome
                        except Exception as e:
                            st.error(f"Erro ao cadastrar novo cliente/veículo: {e}")
                            valid = False
                else: # Cliente Existente
                    if not id_veiculo_selecionado:
                        st.error("Selecione um cliente e um veículo válidos.")
                        valid = False
                    else:
                        current_id_veiculo = id_veiculo_selecionado
                        current_cliente_nome = cliente_nome_selecionado

                if not horario:
                    st.error("Selecione um horário disponível.")
                    valid = False
                if not tipo_servico:
                     st.error("Selecione um tipo de serviço.")
                     valid = False

                if valid and current_id_veiculo is not None:
                    try:
                        add_agendamento(
                            id_veiculo=current_id_veiculo,
                            data=hoje,
                            horario=horario,
                            tipo_servico=tipo_servico,
                            valor=valor,
                            observacoes=observacoes,
                            status="Confirmado"
                        )
                        st.success(f"Agendamento para {current_cliente_nome} às {horario} confirmado!")
                        st.session_state.show_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao adicionar agendamento: {e}")
                elif valid and current_id_veiculo is None:
                     st.error("ID do veículo não foi definido corretamente. Verifique a seleção.")

            if cancelled:
                st.session_state.show_form = False
                st.rerun()

with tab_cadastros:
    st.title("📖 Cadastros")
    st.markdown("---")
    tab1, tab2, tab3 = st.tabs(["Clientes", "Veículos", "Serviços"])

    with tab1:
        st.subheader("📋 Lista de Clientes")
        filtro_cliente = st.text_input("🔎 Buscar por Nome ou CPF", key="filtro_cliente_tab1").strip().lower()
        df_clientes_show = st.session_state.clientes_df.copy()
        df_clientes_show["cpf"] = df_clientes_show["cpf"].astype(str)
        if filtro_cliente:
            clientes_filtrados = df_clientes_show[
                df_clientes_show["nome"].str.lower().str.contains(filtro_cliente, na=False) |
                df_clientes_show["cpf"].str.startswith(filtro_cliente)
            ]
            st.dataframe(clientes_filtrados, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_clientes_show, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("🚗 Veículos por Cliente")
        filtro_veiculo = st.text_input("🔎 Buscar por Nome, CPF ou Placa", key="filtro_veiculo_tab2").strip().lower()
        df_veiculos_show = st.session_state.veiculos_df.copy()
        df_clientes_show = st.session_state.clientes_df[["id_cliente", "nome", "cpf"]].copy()
        df_veiculos_show["id_cliente"] = df_veiculos_show["id_cliente"].astype(int)
        df_clientes_show["id_cliente"] = df_clientes_show["id_cliente"].astype(int)
        df_clientes_show["cpf"] = df_clientes_show["cpf"].astype(str)
        veiculos_completo = df_veiculos_show.merge(df_clientes_show, on="id_cliente", how="left")
        if filtro_veiculo:
            veiculos_filtrados = veiculos_completo[
                veiculos_completo["nome"].str.lower().str.contains(filtro_veiculo, na=False) |
                veiculos_completo["cpf"].str.startswith(filtro_veiculo) |
                veiculos_completo["placa"].str.lower().str.contains(filtro_veiculo, na=False)
            ]
            st.dataframe(veiculos_filtrados[["placa", "marca", "modelo", "nome", "cpf"]], use_container_width=True, hide_index=True)
        else:
            st.dataframe(veiculos_completo[["placa", "marca", "modelo", "nome", "cpf"]], use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("📅 Histórico de Serviços")
        df_agendamentos_hist = st.session_state.agendamentos_df.copy()
        df_veiculos_hist = st.session_state.veiculos_df.copy()
        df_clientes_hist = st.session_state.clientes_df[["id_cliente", "nome"]].copy()

        df_agendamentos_hist["id_veiculo"] = df_agendamentos_hist["id_veiculo"].astype("Int64")
        df_veiculos_hist["id_veiculo"] = df_veiculos_hist["id_veiculo"].astype("Int64") # Match type for merge
        df_veiculos_hist["id_cliente"] = df_veiculos_hist["id_cliente"].astype("Int64") # Match type for merge
        df_clientes_hist["id_cliente"] = df_clientes_hist["id_cliente"].astype("Int64") # Match type for merge

        servicos_com_veiculo = df_agendamentos_hist.merge(df_veiculos_hist, on="id_veiculo", how="left")
        servicos_completos = servicos_com_veiculo.merge(df_clientes_hist, on="id_cliente", how="left")

        if not servicos_completos.empty and "data_agendamento" in servicos_completos.columns and servicos_completos["data_agendamento"].notna().any():
            min_date = servicos_completos["data_agendamento"].min()
            max_date = servicos_completos["data_agendamento"].max()
            if pd.isna(min_date): min_date = date.today()
            if pd.isna(max_date): max_date = date.today()
            dates = st.date_input("Selecione o período:", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="date_filter_tab3")
            if len(dates) == 2:
                start_date, end_date = dates
                mask = (servicos_completos["data_agendamento"] >= start_date) & (servicos_completos["data_agendamento"] <= end_date)
                df_filtrado = servicos_completos[mask]
            else:
                df_filtrado = servicos_completos
        else:
            st.info("Não há dados de agendamento para filtrar.")
            df_filtrado = pd.DataFrame()

        colunas_desejadas_display = ["id_agendamento", "data_agendamento", "horario_agendamento", "nome", "marca", "modelo", "placa", "tipo_servico", "valor", "status", "observacoes"]
        colunas_existentes = [col for col in colunas_desejadas_display if col in df_filtrado.columns]
        df_display = df_filtrado[colunas_existentes].rename(columns={
            "nome": "Cliente", "marca": "Marca", "modelo": "Modelo", "placa": "Placa", "observacoes": "Observações", "tipo_servico": "Serviço", "valor": "Valor (R$)", "status": "Status", "data_agendamento": "Data", "horario_agendamento": "Hora"
        })

        col1, col2 = st.columns(2)
        col1.metric("Serviços no Período", len(df_display))
        st.dataframe(df_display, use_container_width=True, hide_index=True)

with tab_resumo:
    st.title("💰 Resumo Financeiro")
    st.markdown("---")
    df_agendamentos_resumo = st.session_state.agendamentos_df.copy()
    df_veiculos_resumo = st.session_state.veiculos_df.copy()

    df_agendamentos_resumo["valor"] = pd.to_numeric(df_agendamentos_resumo["valor"], errors="coerce").fillna(0)
    df_agendamentos_resumo["status"] = df_agendamentos_resumo["status"].astype(str)
    df_veiculos_resumo["marca"] = df_veiculos_resumo["marca"].astype(str)

    confirmados_df = df_agendamentos_resumo[df_agendamentos_resumo["status"].str.lower() == "confirmado"]
    valor_total_previsto = df_agendamentos_resumo["valor"].sum()
    valor_total_realizado = confirmados_df["valor"].sum()
    valor_medio = df_agendamentos_resumo["valor"].mean() if not df_agendamentos_resumo.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Receita Total [Prevista]", f"R$ {valor_total_previsto:,.2f}")
    col2.metric("Receita Total [Realizado]", f"R$ {valor_total_realizado:,.2f}")
    col3.metric("Receita Média por Serviço", f"R$ {valor_medio:,.2f}")

    st.markdown("---")
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        st.subheader("🔧 Serviços Mais Comuns")
        if not df_agendamentos_resumo.empty and "tipo_servico" in df_agendamentos_resumo.columns:
            servicos_count = df_agendamentos_resumo["tipo_servico"].value_counts()
            st.bar_chart(servicos_count)
        else:
            st.write("Nenhum serviço registrado.")
    with col_graf2:
        st.subheader("🚗 Marcas Mais Atendidas")
        if not df_veiculos_resumo.empty and "marca" in df_veiculos_resumo.columns:
            marcas_count = df_veiculos_resumo["marca"].value_counts()
            st.bar_chart(marcas_count)
        else:
            st.write("Nenhum veículo registrado.")

st.markdown("---")
st.markdown("Python Car Repair Shop 🐍 - Dados fictícios gerados para fins didáticos")
