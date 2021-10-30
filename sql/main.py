# Built in Python Libraries
import json, pathlib

import requests
from PIL import Image, ImageDraw
from io import BytesIO

def getPokemonInfo(pokemonValue):
    url = f"http://pokeapi.co/api/v2/pokemon/{pokemonValue}/"
    wild_pokemon = requests.post(url).json()
    with open(f"JSON Pokemon/Pokemon#{wild_pokemon['id']}", 'w') as file:
        json.dump(wild_pokemon, file, indent=4)