import streamlit as st
import pandas as pd
import random
from faker import Faker
import plotly.graph_objects as go
from datetime import date , timedelta , datetime
st.set_page_config(page_title="Python Rent a Car 🐍", layout="wide")

st.title("Python Rent a Car (em desenvolvimento)")
st.markdown("---")


# Criando Dados
fake = Faker('pt_BR')

# Parâmetros
num_clientes = 100
num_veiculos = 50
num_lojas = 5
num_locacoes = 555

# Gerar Clientes
clientes = []
for i in range(num_clientes):
    clientes.append({
        'id_cliente': i + 1,
        'nome': fake.name(),
        'cpf': fake.unique.cpf(),
        'email': fake.email(),
        'telefone': fake.phone_number(),
        'nps': random.choices([10, 9, 8, 7, 6, 5, 4], weights=[0.3, 0.3, 0.2, 0.05, 0.05, 0.05, 0.05])[0]
    })
clientes_df = pd.DataFrame(clientes)

# Gerar Veículos

# Categorias e faixas de preço por dia
categorias = {
    'Econômico': (98, 157),
    'Intermediário': (180, 247),
    'SUV': (299, 433)
}

# Marcas, modelos e categorias
marcas_modelos_categorias = [
    ('Fiat', 'Argo', 'Econômico'),
    ('Chevrolet', 'Onix', 'Econômico'),
    ('Volkswagen', 'Gol', 'Econômico'),
    ('Hyundai', 'HB20', 'Intermediário'),
    ('Ford', 'Ka', 'Econômico'),
    ('Toyota', 'Corolla', 'Intermediário'),
    ('Jeep', 'Renegade', 'SUV'),
    ('Honda', 'HR-V', 'SUV')
]

veiculos = []
for i in range(num_veiculos):
    marca, modelo, categoria = random.choice(marcas_modelos_categorias)
    ano = random.randint(2018, 2023)
    veiculos.append({
        'id_veiculo': i + 1,
        'marca': marca,
        'modelo': modelo,
        'categoria': categoria,
        'ano': ano,
        'placa': fake.unique.license_plate(),
        'status': 'disponível',
        'km_total': random.randint(20000, 150000),
        'tempo_manutencao_dias': random.randint(0, 20)
    })
veiculos_df = pd.DataFrame(veiculos)

# Gerar Lojas
cidades_estados = { "São Paulo": "SP",
                  "Rio de Janeiro": "RJ",
                  "Belo Horizonte": "MG",
                  "Porto Alegre": "RS",
                  "Curitiba": "PR"}

lojas = []
for i, (cidade, estado) in enumerate(cidades_estados.items(), start=1):
    lojas.append({
        "id_loja": i,
        "nome_loja": f"Locadora {cidade}",
        "cidade": cidade,
        "estado": estado
    })

lojas_df = pd.DataFrame(lojas)

# Gerar Locações 
locacoes = []
historico_veiculos = {v: [] for v in veiculos_df['id_veiculo'].tolist()}
tentativas = 0
while len(locacoes) < num_locacoes and tentativas < num_locacoes * 10:
    tentativas += 1
    id_cliente = random.choice(clientes_df['id_cliente'].tolist())
    id_veiculo = random.choice(veiculos_df['id_veiculo'].tolist())
    id_loja = random.choice(lojas_df['id_loja'].tolist())
    data_inicio = fake.date_between(start_date='-2y', end_date='today')
    duracao = random.randint(1, 15)
    data_fim = data_inicio + timedelta(days=duracao)
    if random.random() < 0.2:
        data_fim = None  # locação ativa

    conflito = False
    for loc in historico_veiculos[id_veiculo]:
        inicio = loc['data_inicio']
        fim = loc['data_fim'] if loc['data_fim'] else datetime.today().date()
        if data_fim:
            if not (data_fim <= inicio or data_inicio >= fim):
                conflito = True
                break
        else:
            if data_inicio <= fim:
                conflito = True
                break

    if not conflito:
        categoria = veiculos_df.loc[veiculos_df['id_veiculo'] == id_veiculo, 'categoria'].values[0]
        preco_min, preco_max = categorias[categoria]
        preco_dia = random.randint(preco_min, preco_max)
        receita = preco_dia * duracao if data_fim else 0
        custo = receita * random.uniform(0.4, 0.7)
        km_rodado = random.randint(100, 1000)
        reclamacao = random.choices([0, 1], weights=[0.9, 0.1])[0]
        sinistro = random.choices([0, 1], weights=[0.95, 0.05])[0]

        nova_loc = {
            'id_locacao': len(locacoes) + 1,
            'id_cliente': id_cliente,
            'id_veiculo': id_veiculo,
            'id_loja': id_loja,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'receita': receita,
            'custo': custo,
            'km_rodado': km_rodado,
            'reclamacao': reclamacao,
            'sinistro': sinistro,
            'preco_dia': preco_dia
        }
        locacoes.append(nova_loc)
        historico_veiculos[id_veiculo].append(nova_loc)

locacoes_df = pd.DataFrame(locacoes)

# Vendas e Marketing
marketing = []

for mes in pd.date_range(start='2023-01-01', end='2024-12-01', freq='MS'):
    cotacoes = random.randint(150, 400)
    alugueis_confirmados = random.randint(int(cotacoes * 0.3), cotacoes)
    investimento_marketing = random.randint(5000, 15000)
    novos_clientes = random.randint(20, 80)

    taxa_conversao = alugueis_confirmados / cotacoes
    cac = investimento_marketing / novos_clientes if novos_clientes else 0

    marketing.append({
        'mes': mes.strftime('%Y-%m'),
        'cotacoes': cotacoes,
        'alugueis_confirmados': alugueis_confirmados,
        'taxa_conversao': round(taxa_conversao, 2),
        'investimento_marketing': investimento_marketing,
        'novos_clientes': novos_clientes,
        'cac': round(cac, 2)
    })

marketing_df = pd.DataFrame(marketing)


'''

# Painel 

## KPIs Operacionais
'''
# Filtrar apenas veiculos disponiveis 
veiculos_disponiveis = veiculos_df[veiculos_df['status'] == 'disponível']

# Filtrar apenas veículos em locação ativa
veiculos_alugados = (
    locacoes_df[locacoes_df['data_fim'].isna()]
    ['id_veiculo'].unique()
)
# Números de veiculos em locação ativa
numero_alugados = len(veiculos_alugados)

taxa_ocupacao_frota = (numero_alugados /num_veiculos)*100

st.metric("Taxa de Ocupação da Frota",f"{taxa_ocupacao_frota:.2f}%")

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
