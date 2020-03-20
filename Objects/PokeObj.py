from Config import *

from datetime import datetime

class PokeObj:
    def __init__(self, pokeObj, psn):
        #print(pokeObj.keys())
        self.name = pokeObj['name']
        self.index = pokeObj['id']
        self.type = [type['type']['name'] for type in pokeObj['types']]
        if len(pokeObj['moves']) < 4:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], len(pokeObj['moves']))]
        else:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], 4)]

        self.lvl = 5
        self.exp = 0

        self.caughtBy = (datetime.now().strftime("%a, %b %d, %Y - %I:%M %p"), psn.id)

    def __repr__(self):
        return "{}#{}".format(self.name,self.index)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, PokeName):
        self._name = PokeName

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
    

