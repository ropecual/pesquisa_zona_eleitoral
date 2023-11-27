from time import sleep
import requests
import json
from geopy import Nominatim


def get_coordinates(cep, cidade, endereco=None):
    cep_url = cep
    cidade_url = cidade.replace(' ', '%20')
    endereco_url = endereco.replace('', '%20')
    print("Processando latitude e longitude de: " + str(cep_url) + " - " + str(cidade))

    data = get_coordinates_from_first_method(cep_url, cidade_url)

    if len(data) == 0:
        print("Dado não encontrado, tentando segundo método: Google")
        print("Processando latitude e longitude de: " + str(endereco) + " - " + str(cidade))
        lat, lon = get_coordinates_from_google_maps(endereco, cidade)

        if lat is None or lon is None:
            print("Dado não encontrado, tentando terceiro método")
            print("Processando latitude e longitude de: " + str(endereco) + " - " + str(cidade))
            data = get_coordinates_from_first_method(endereco_url, cidade_url)

            if len(data) == 0:
                print("Dado não encontrado, tentando quarto método: Direto Nomatim")
                sleep(2)
                position = get_coordinates_from_nomatim(cep, cidade)
                return str(position.latitude), str(position.longitude)
            else:
                return data[0]['lat'], data[0]['lon']
        else:
            return str(lat), str(lon)

    else:
        return data[0]['lat'], data[0]['lon']


def get_coordinates_from_first_method(endereco, cidade):
    url = f"https://nominatim.openstreetmap.org/search?q={endereco}+{cidade}&format=json&limit=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    if response.status_code != 200:
        data = []
    return data


def get_coordinates_from_nomatim(endereco, cidade):
    geolocator = Nominatim(user_agent='myGeocoder')
    endereco_completo = f"{endereco}, {cidade}"
    location = geolocator.geocode(endereco_completo, exactly_one=True)
    if location is None:
        print("Coordenadas não encontradas. Utilizando ponto central do município")
        sleep(2)
        location = geolocator.geocode(cidade, exactly_one=True)
    return location

"""
Cria uma classe simples e adicione sua chave api do google na mesma
class Settings:
    def __init__(self):
        self.GOOGLE_KEY = "<SUA CHAVE AQUI>"

"""
from config import settings
def get_coordinates_from_google_maps(endereco, cidade):
    api_key = settings.GOOGLE_KEY
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": endereco, "key": api_key}

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data["status"] == "OK":
        # Extraia a latitude e a longitude do primeiro resultado
        lat = data["results"][0]["geometry"]["location"]["lat"]
        lng = data["results"][0]["geometry"]["location"]["lng"]
        return lat, lng
    else:
        print("Não foi possível encontrar as coordenadas. ")
        return None, None