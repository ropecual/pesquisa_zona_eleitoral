import csv
from faker import Faker
import random
import pandas as pd

# Inicialize o Faker
fake = Faker('pt_BR')
estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PI', 'PR', 'RJ',
           'RN', 'RO', 'RS', 'SC', 'SE', 'SP', 'TO', 'ZZ']
# Abra o arquivo CSV com os números de sessões eleitorais
with open('totais_lat_lon.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Pule o cabeçalho, se houver

    # Obtenha todos os números de sessão eleitoral do CSV em uma lista
    dados = [{'numero_zona': row[2], 'Cidade': row[7], 'Estado': row[8]} for row in reader]

    registros_ficticios = []

    # Itere para criar registros fictícios com números de sessão eleitoral aleatórios
    for _ in range(50000):  # Número de registros fictícios que você deseja criar (altere conforme necessário)
        # Escolha um número de sessão eleitoral aleatório da lista
        dado_aleatorio = random.choice(dados)
        endereco_completo = fake.address()
        registro = {
            # Crie um registro fictício usando o Faker
            'nome': fake.name(),
            'endereco': endereco_completo.split(',')[0],
            'cidade': dado_aleatorio['Cidade'],
            'estado': dado_aleatorio['Estado'],
            'numero_zona': dado_aleatorio['numero_zona']
        }
        registros_ficticios.append(registro)

df = pd.DataFrame(registros_ficticios)
print(df)

# Salve o DataFrame em um arquivo CSV, se desejar
df.to_csv('registros_ficticios.csv', index=False)

resultado = df.groupby(['numero_zona', 'cidade']).size().reset_index(name='Contagem de Pessoas')
resultado.to_csv('resultado.csv', index=False)
print(resultado)


locais_sessoes = pd.read_csv('totais_lat_lon.csv')

resultado_df_full = locais_sessoes.merge(resultado, on='numero_zona',how='left')
