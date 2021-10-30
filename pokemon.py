import datetime
import json
import os
import random
import log
import requests


class Pokemon:
    def __init__(self, id):
        self.id = id
        self.json = None

        self._fetch()

    def _fetch(self):
        url = f"http://pokeapi.co/api/v2/pokemon/{id}/"
        # Checks if Pokemon has already been found, if so pulls file
        if os.path.isfile("IO Files/Pokemon/Pokemon#{}".format(self.id)):
            with open("IO Files/Pokemon/Pokemon#{}".format(self.id), "r") as file:
                self.wild_pokemon = json.load(file)
        else:
            t0 = datetime.now()
            self.wild_pokemon = requests.post(url).json()
            log.info(f"Obtained Pokemon in {datetime.now() - t0}")
            with open(f"IO Files/Pokemon/Pokemon#{self.wild_pokemon['id']}", "w") as file:
                json.dump(self.wild_pokemon, file)


def from_message(msg: str):
    if msg != None:
        if msg.isdigit():
            return Pokemon(msg)
        else:
            return Pokemon(msg.lower())
    else:
        poke_num = str(random.randint(1, 200))
        return Pokemon(poke_num)
