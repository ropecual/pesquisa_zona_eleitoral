from time import sleep

import requests, json
from geopy import Nominatim


def get_coordinates(cep, cidade, endereco=None):
    cep_url = cep
    cidade_url = cidade.replace(' ', '%20')
    endereco_url = endereco.replace('', '%20')

    print("Processando latitude e longitude de: " + str(cep_url) + " - " + str(cidade))
    url = f"https://nominatim.openstreetmap.org/search?q={cep_url}+{cidade_url}&format=json&limit=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)

    if len(data) == 0 or response.status_code != 200:
        print("Dado não encontrado, tentando segundo método")
        print(response.status_code)
        sleep(2)
        print("Processando latitude e longitude de: " + str(endereco) + " - " + str(cidade))
        url = f"https://nominatim.openstreetmap.org/search?q={endereco_url}+{cidade_url}&format=json&limit=1"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.content)

        if len(data) == 0 or response.status_code != 200:
            print("Dado não encontrado, tentando terceiro método")
            print(response.status_code)
            sleep(2)
            position = get_coordinates_from_second_method(cep, cidade)
            return str(position.latitude), str(position.longitude)
        else:
            return data[0]['lat'], data[0]['lon']

    else:
        return data[0]['lat'], data[0]['lon']


def get_coordinates_from_second_method(endereco, cidade):
    geolocator = Nominatim(user_agent='myGeocoder')
    endereco_completo = f"{endereco}, {cidade}"
    location = geolocator.geocode(endereco_completo, exactly_one=True)
    if location is None:
        print("Coordenadas não encontradas. Utilizando ponto central do município")
        sleep(2)
        location = geolocator.geocode(cidade, exactly_one=True)
    return location
