import sys
from time import sleep
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pandas as pd

from create_df import create_df

if __name__ == '__main__':
    # Padroniza o encoding da aplicação e arquivos
    sys.stdout.reconfigure(encoding='utf-8')
    # Define o local da aplicação como local de download
    download_dir = os.getcwd()
    # Seta os atributos para o webdriver chrome
    prefs = {'download.default_directory': download_dir}
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', prefs)

    # Lista de estados para percorrer
    values = ['AC',]

    # Inicia o navegador e vai até a pagina designada
    navegador = webdriver.Chrome(options=options)
    navegador.minimize_window()
    navegador.implicitly_wait(5)
    navegador.get('https://cad-app-estruturaje.tse.jus.br/estruturaje-servico-ws/paginas/zonaEleitoral/consultar.faces')

    botao_consultar = navegador.find_element(By.ID, 'consultaForm:btnConsultar')

    dropdown_uf = Select(navegador.find_element(By.ID, 'consultaForm:listaUF_input'))
    # Para cada local na lista de valores criada acima, ele realiza o download. Após, fecha o navegador
    for local in values:
        print("Baixando dados de: " + local)
        dropdown_uf.select_by_value(local)
        botao_consultar.click()
        sleep(3)
        botao_csv = navegador.find_element(By.ID, 'consultaForm:j_idt54')
        botao_csv.click()
        sleep(2)
    navegador.quit()

    # Criamos um dicionário que percorrerá todos os downloads, adicionando, via pandas, o conteudo de cada csv em uma
    # entrada chave->valor
    nome_arquivo = 'lista_zonas_eleitorais.csv'
    dic_dataframe = {}
    for i in range(len(values)):
        if i != 0:
            nome_arquivo = 'lista_zonas_eleitorais (' + str(i) + ').csv'

        csv_path = os.path.join(download_dir, nome_arquivo)

        while not os.path.exists(csv_path):
            pass
        print("Adicionando ao dicionário dados de: " + nome_arquivo)
        dic_dataframe[i] = pd.read_csv(csv_path, sep=",", encoding='Windows-1254')

    # transformamos o conteudo do dicionario em um dataframe.
    dataframes_totais = pd.concat(dic_dataframe.values(), ignore_index=True)

    # Limpa a pasta após a extração para o dataframe total
    nome_arquivo = 'lista_zonas_eleitorais.csv'
    for i in range(len(values)):
        if i != 0:
            nome_arquivo = 'lista_zonas_eleitorais (' + str(i) + ').csv'

        csv_path = os.path.join(download_dir, nome_arquivo)
        # Verifica se há o arquivo, se houver, ele será deletado.
        if os.path.isfile(csv_path):
            os.remove(csv_path)

    # Converte o dataframe total em um csv
    csv_path = os.path.join(download_dir, 'totais.csv')
    if os.path.isfile(csv_path):
        os.remove(csv_path)

    dataframes_totais.to_csv('totais.csv', index=True)

    print("Lista de Zonas criadas, deseja calcular a latitude e longitude? (isso costuma demorar)")
    print("[0] Não")
    print("Qualquer outra Tecla para sim")
    print("")
    opcao = input()
    if opcao != "0":
       create_df('totais.csv')
