from MainVars import *
from PokeObj import *


class user:
    def __init__(self, user, poke):
        self.user = user
        self.pokeList = {poke['name'] : [PokeObj(poke)]}
        self.items = []

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, value):
        print(value)
        if value == []:
            self._items = []
        else:
            self._items.append(value)

    def getPokeList(self):
        return self.pokeList.keys()
    
    def addPokeList(self, value):
        if value['name'] in self.pokeList.keys():
            self.pokeList[value['name']].append(value)
        else:
            self.pokeList[value['name']] = [value]

    def removePokemon(self, name):
        if name in self.pokeList.keys():
            poke = self.pokeList[name].pop()
            if len(self.pokeList[name]) == 0:
                del self.pokeList[name]
            return poke
        else:
            return None

    def hasPokemon(self, name):
        if name in self.pokeList.keys():
            return True
        else:
            return False