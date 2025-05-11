import pandas as pd
from faker import Faker
import random

fake = Faker('pt_BR')

def gerar_clientes(num_clientes=300):
    clientes = []
    for i in range(1, num_clientes + 1):
        sexo = random.choice(["Masculino", "Feminino"])
        nome = fake.first_name_male() if sexo == "Masculino" else fake.first_name_female()
        clientes.append({
            "id_cliente": i,
            "nome": f"{nome} {fake.last_name()}",
            "cpf": fake.cpf(),
            "telefone": fake.phone_number(),
            "email": fake.safe_email(),
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=70),
            "sexo": sexo,
            "endereco": fake.street_address(),
            "numero": fake.building_number(),
            "bairro": fake.neighborhood(),
            "cep": fake.postcode(),
            "cidade": "São Paulo",
            "estado": "São Paulo",
        })
    return pd.DataFrame(clientes)

def gerar_veiculos(num_veiculos=100, clientes_df=None):
    marcas_modelos = {
        "Fiat": ["Argo", "Cronos", "Pulse"],
        "Volkswagen": ["Polo", "Virtus", "Nivus"],
        "Hyundai": ["HB20", "HB20S", "Creta"],
        "GM": ["Onix", "Onix Sedan", "Tracker"]
    }
    cores = ["Preto", "Branco", "Prata", "Vermelho", "Azul", "Cinza"]
    veiculos = []
    for i in range(1, num_veiculos + 1):
        marca = random.choice(list(marcas_modelos.keys()))
        modelo = random.choice(marcas_modelos[marca])
        veiculos.append({
            "id_veiculo": i,
            "id_cliente": random.choice(clientes_df["id_cliente"]),
            "marca": marca,
            "modelo": modelo,
            "ano": random.randint(2010, 2024),
            "cor": random.choice(cores),
            "placa": fake.license_plate()
        })
    return pd.DataFrame(veiculos)

def gerar_agendamentos(num_agendamentos=200, veiculos_df=None):
    agendamentos = []
    for i in range(1, num_agendamentos + 1):
        valor = round(random.uniform(100, 2000), 2)
        data = fake.date_between(start_date='-7d', end_date='+7d')
        # Gerar um horário entre 8h e 17h, com passo de 1 hora
        hora = random.choice(range(8, 17)) 
        minuto = 0  # Para garantir horários redondos (ex: 09:00, 10:00)
        horario_agendamento = f"{hora:02d}:{minuto:02d}"  # Formata como "09:00"
        agendamentos.append({
            "id_agendamento": i,
            "id_veiculo": random.choice(veiculos_df["id_veiculo"]),
            "data_agendamento": data,
            "horario_agendamento": horario_agendamento,
            "tipo_servico": random.choice(["Revisão", "Troca de óleo", "Freios", "Suspensão", "Diagnóstico"]),
            "valor": valor,
            "status": random.choice(["Confirmardo", "Pendente", "Cancelado"])
        })
    return pd.DataFrame(agendamentos)

