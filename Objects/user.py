from config import *
from Objects.PokeObj import *

class User:
    def __init__(self, user, poke):
        self.user = user.id
        self.pokeList = {poke['name'] : [PokeObj(poke, user)]}
        self.items = []

    def __repr__(self):
        prnt_str = "__{}'s Pokemon__: include **{}/802** Pokemon:\n".format(self.user.name, len(self.pokeList.keys()))
        for PokeName in self.pokeList.keys():
            prnt_str += "{} *x{}*\n".format(PokeName.capitalize(),len(self.pokeList[PokeName]))
        return prnt_str

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
        return self._pokeList.keys()
    
    def addPokeList(self, value, user):
        #print(value)
        if value['name'] in self.pokeList.keys():
            self.pokeList[value['name']].append(PokeObj(value, user))
        else:
            self.pokeList[value['name']] = [PokeObj(value, user)]

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

    def listInventory(self):
        pass

    def embed_list(self, user):
        str_title = "__{}'s Pokemon__".format(user.name)
        str_footer = "Obtained {} of 802 Pokemon".format(len(self.pokeList.keys()))
        embed = discord.Embed(type="rich", title=str_title, color=0xEEE8AA)
        str_desc = ""
        for PokeName in self.pokeList.keys():
            str_desc += "{} *x{}*\n".format(PokeName.capitalize(),len(self.pokeList[PokeName]))
        embed.description = str_desc[:2048 - len(str_title + str_footer)]
        embed.set_footer(text=str_footer)
        return embed
