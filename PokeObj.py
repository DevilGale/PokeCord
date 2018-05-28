from MainVars import *

class PokeObj:
    def __init__(self, pokeObj):
        print(pokeObj.keys())
        self.name = pokeObj['name']
        self.index = pokeObj['id']
        if len(pokeObj['moves']) < 4:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], len(pokeObj['moves']))]
        else:
            self.moves = [item['move'] for item in random.sample(pokeObj['moves'], 4)]

    def __repr__(self):
        return "{}#{}".format(self.Pname,self.index)

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
    

