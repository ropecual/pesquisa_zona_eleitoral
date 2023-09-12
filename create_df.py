import os
from time import sleep
import pandas as pd
from lat_lon import get_coordinates


def create_df(nome_arquivo):
    download_dir = os.getcwd()
    csv_path = os.path.join(download_dir, nome_arquivo)
    if os.path.isfile(csv_path):
        df = pd.read_csv(csv_path)

        df[['lat', 'lon']] = df.apply(
            lambda row: pd.Series(get_coordinates(row['cep'], row['nome_municipio'], row['endereco'])), axis=1)

        # Converte o dataframe total em um csv
        csv_path = os.path.join(download_dir, 'totais_lat_lon.csv')
        if os.path.isfile(csv_path):
            os.remove(csv_path)

        df.to_csv('totais_lat_lon.csv', index=True)
    else:
        print("Não há arquivo para processar")
