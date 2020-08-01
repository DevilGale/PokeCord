from config import *

import random
from datetime import datetime

class PokeObj:
    def __init__(self, pokeObj, psn):
        #print(pokeObj.keys())
        self.name = pokeObj['name']
        self.nickname = None
        self.index = pokeObj['id']
        self.type = [type['type']['name'] for type in pokeObj['types']]
        if len(pokeObj['moves']) < 4:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], len(pokeObj['moves']))]
        else:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], 4)]

        self.lvl = 5
        self.exp = 0

        self.caughtInfo = (datetime.now().strftime("%a, %b %d, %Y - %I:%M %p"), psn.display_name, psn.id)

    def __repr__(self):
        return "{}#{}".format(self.name,self.index)

    def __eq__(self, other):
        if self.nickname == None or other.nickname == None:
            return self.name == other.name
        else:
            return self.nickname == other.nickname

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, PokeName):
        self._name = PokeName

    @property
    def nickname(self):
        return self._nickname
    
    @nickname.setter
    def nickname(self, new_name):
        self._nickname = new_name

    @property
    def index(self):
        return self._index
    
    @index.setter
    def index(self, index):
        self._index = index

    @property
    def moves(self):
        return self._moves

    @moves.setter
    def moves(self, moves):
        self._moves = moves
    

