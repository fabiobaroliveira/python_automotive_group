import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date , timedelta , datetime
st.set_page_config(page_title="Python Rent a Car 🐍", layout="wide")

st.title("Python Rent a Car (em desenvolvimento)")
st.markdown("---")

# Carregar os dados
@st.cache_data
def load_data():
    clientes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/clientes_locadora.csv", sep=";")
    veiculos_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/veiculos_locadora.csv", sep=";")
    locacoes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/locacoes.csv", sep=";")
    equipes_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/equipes.csv", sep=";")
    lojas_df = pd.read_csv("https://raw.githubusercontent.com/fabiobaroliveira/python_automotive_group/main/pages/lojas.csv", sep=";")
    
    return clientes_df, veiculos_df, locacoes_df, equipes_df, lojas_df

clientes_df, veiculos_df, locacoes_df,equipes_df, lojas_df = load_data()


# Merge dos dataframes
df = locacoes_df.merge(clientes_df, on="id_cliente") \
                .merge(veiculos_df, on="id_veiculo") \
                .merge(lojas_df, on="id_loja")\
                .merge(equipes_df, on="id_atendente")
                

# Alterar tipos numéricos
df["valor_total"] = df["valor_total"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["valor_diaria"] = df["valor_diaria"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)

# Conversão de datas
df["data_locacao"] = pd.to_datetime(df["data_locacao"], dayfirst=True)
df["data_devolucao"] = pd.to_datetime(df["data_devolucao"], dayfirst=True)


# Opções de filtro
filtro_data = st.selectbox(
    "Filtrar por período:",
    ("Hoje", "Últimos 7 dias", "Último mês", "Período completo")
)

# Define o intervalo de datas
data_fim = df["data_locacao"].max().date()
data_inicio = df["data_locacao"].min().date()

if filtro_data == "Hoje":
        data_inicio_filtro = date.today()
        data_fim_filtro = date.today()
elif filtro_data == "Últimos 7 dias":
        data_inicio_filtro = date.today() - timedelta(days=6)
        data_fim_filtro = date.today()
elif filtro_data == "Último mês":
        data_inicio_filtro = date.today() - timedelta(days=30)
        data_fim_filtro = date.today()
else:  # Período completo
        data_inicio_filtro = data_inicio
        data_fim_filtro = data_fim


# Aplica o filtro
df_filtrado = df[
        (df["data_locacao"].dt.date >= data_inicio_filtro) &
        (df["data_locacao"].dt.date <= data_fim_filtro)
]

# KPIs
faturamento = df_filtrado["valor_total"].sum()
num_locacoes = df_filtrado["id_locacao"].nunique()
ticket_medio = faturamento / num_locacoes if num_locacoes > 0 else 0

def format_currency(value):
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:,.1f} mi"
    elif value >= 1_000:
        return f"R$ {value / 1_000:,.1f} mil"
    else:
        return f"R$ {value:,.2f}"

# Layout do dashboard
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento do período", format_currency(faturamento))
#col2.metric
col3.metric("Nº de locações", num_locacoes)
col4.metric("Ticket médio", f"R$ {ticket_medio:,.2f}")



# Agrupamento por loja para gerar indicadores
df_lojas = df_filtrado.groupby("nome_loja").agg(
    Faturamento=("valor_total", "sum"),
    Locações=("id_locacao", "count")
).sort_values("Faturamento", ascending=False).reset_index()

# Formatar valores para moeda
df_lojas["Faturamento"] = df_lojas["Faturamento"].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.dataframe(df_lojas)

'''

# Painel 

KPIs Operacionais

### Taxa de Ocupação da Frota

(Nº de veículos alugados / Total de veículos disponíveis) × 100

Mostra a eficiência no uso dos veículos.

'''

# Função para adicionar nova coluna com Status Correto

data_hoje = date.today()  # YYYY-MM-DD  Data de hoje no formato date

def status_real(data_devolucao_str):
    # Se for None ou NaN 
    if pd.isna(data_devolucao_str):
        return "Sem data"    
    # Converte a string "dd-mm-yyyy" para um objeto date
    try:
        data_devolucao = datetime.strptime(data_devolucao_str, "%d-%m-%Y").date()
    except ValueError:
        return "Formato inválido"
    
    # Compara as datas
    if data_devolucao >= data_hoje:
        return "Ativa"
    else:
        return "Finalizada"

# Aplica a função na coluna 'data_devolucao'
locacoes_df['status_real'] = locacoes_df['data_devolucao'].apply(status_real)

# Filtrar apenas locações "Ativa"
locacoes_ativas = locacoes_df[locacoes_df['status_real'] == 'Ativa']

# Calcular o número de veículos alugados 
veiculos_alugados = len(locacoes_ativas)

# Total de veículos na frota
total_veiculos = len(veiculos_df)

# Calculo Taxa de Ocupação
taxa_ocupacacao_frota = (veiculos_alugados/total_veiculos)*100

# Layout do dashboard Painel Operacional
col100, col110, col120 = st.columns(3)
col100.metric("Taxa de Ocupação da Frota", f"{taxa_ocupacacao_frota:.2f}%")


'''

### Dias Médios de Aluguel por Veículo

(Total de dias alugados / Nº total de veículos na frota)

Indica o tempo médio que um veículo passa alugado.

'''

'''
### Tempo de Indisponibilidade 

(Tempo em manutenção ou parado / Tempo total disponível)

Ajuda a identificar gargalos na manutenção.

'''

'''
KPIs Financeiros

### Receita Média Diária (RAD)

(Receita total de aluguéis / Nº total de dias alugados)

Mede a rentabilidade por dia de aluguel.

'''

'''

KPIs de Gestão de Frota

### Idade Média da Frota

(Soma da idade dos veículos / Nº total de veículos)

Frota muito antiga pode aumentar custos de manutenção.

### Quilometragem Média por Veículo

(Quilometragem total / Nº de veículos)

Ajuda a planejar a renovação da frota.

'''


# Rodapé
st.markdown("---")
st.markdown("Python Rent a Car 🐍 - Dados fictícios gerados para fins didáticos")
