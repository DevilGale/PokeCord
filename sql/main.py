# Project Includes
from sqlalchemy.orm import session
#from sql.tables import Pokemon
import tables # database for bot
from pil import PilPokemon # Request and parser for pokemon

# Built in Python Libraries
import json
from pathlib import Path

# import requests
# from PIL import Image, ImageDraw
# from io import BytesIO

def getPokemonInfo(pokemonValue):
    url = f"http://pokeapi.co/api/v2/pokemon/{pokemonValue}/"
    wild_pokemon = requests.post(url).json()
    with open(f"JSON Pokemon/Pokemon#{wild_pokemon['id']}", 'w') as file:
        json.dump(wild_pokemon, file, indent=4)

def setupFolders():
    imgFolder = Path('Images')
    if not imgFolder.exists():
        imgFolder.mkdir()
    pass

if __name__ == '__main__':
    setupFolders()
    pokemon = PilPokemon()
    pokemon.getGIF(1)
    pokemon.getNormalizedImage()
    filename = f'Images/#{pokemon.details["id"]:03d}{pokemon.details["name"]}.gif'
    if not Path(filename).exists():
        pokemon.saveGIF(pokemon.normal_image, filename)

    qry = tables.session.query(tables.Pokemon).filter(tables.Pokemon.id==pokemon.details["id"])
    if not qry.first():
        print("Add")
        sqlPokemon = tables.Pokemon.fromJson(pokemon.details)
        sqlPokemon.image_path = filename

        tables.session.add(sqlPokemon)
        tables.session.commit()
    
