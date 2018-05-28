
class user:
	def __init__(self, user):
        self.user = user
        self.pokeList = {}
        self.items = []

    @items.setter
    def items(self, value):
        self._items.append(value)

    @pokeList.setter
    def pokeList(self, value):
        if value['name'] in self._pokeList:
            self._pokeList[value['name']].append(value)
        else:
            self._pokeList[value['name']] = [value]

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