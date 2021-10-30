# Pip Libs
import discord
from discord import channel
from discord.ext import commands
from pathlib import Path
from discord.client import Client
from discord.enums import ChannelType
# Project Libs
import tables
from pil import PilPokemon
import log

# def getPokemonInfo(pokemonValue):
#     url = f"http://pokeapi.co/api/v2/pokemon/{pokemonValue}/"
#     wild_pokemon = requests.post(url).json()
#     with open(f"JSON Pokemon/Pokemon#{wild_pokemon['id']}", 'w') as file:
#         json.dump(wild_pokemon, file, indent=4)

class PokeCord(commands.Cog):
    def __init__(self, bot:discord.Client):
        self.bot : discord.Client = bot
        self.spawn_time = tables.session.query(tables.PokeCord).filter(tables.PokeCord.discord_server==bot.guilds)
        self.session = tables.session

    @commands.Cog.listener()
    async def on_ready(self):
        # Get servers has access to
        for guild in self.bot.guilds:
            log.info(f"Access to - {guild.name}")
            # if guild.id not in self.channel_bind:
            #     for channel in guild.text_channels:
            #         log.info(f"{channel.name} - {guild.me.permissions_in(channel)}") # send_messages
            #         if guild.me.permissions_in(channel).send_messages:
            #             self.channel_bind[guild.id] = channel.id
            #             break
            #         log.info(f"{(guild.me.permissions_in(channel).send_messages)}")
        # Setup Wild Pokemon
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if (message.author == self.bot.user or 
            message.content[1:].startswith("spawn") or
            message.channel.type != discord.ChannelType.text
        ):
            return

        # Setup Spawning

    #-------------------------------------------------
    #                   Commands
    #-------------------------------------------------

    @commands.command(name='inventory', 
        aliases=['backpack'],
        help="Displays pokemon and items")
    async def cmd_inventory(self, context, member:discord.Member=None):
        if member == None:
            member = context.author

    @commands.command(name='release', 
        usage='<pokemon> [pokemon index=0]',
        help="""Removes a pokemon from your inventory.
        <pokemon> - name of the pokemon you want to release
        optional [pokemon index] - caught multiple of the same pokemon and want to release a particular one
        """)
    async def cmd_release(self, ctx, pokemonName : str, pokemon_index:int = 0):
        pass

    @commands.command(name='trade',
        help="Trade a pokemon between two users")
    async def cmd_trade(self, ctx, member:discord.Member, give_pokemon:str, get_pokemon:str):
        pass

    @commands.command(name='region',
        aliases=['pokedex'],
        help="Sets the region from which pokemon are able to spawn.")
    async def cmd_region(self, ctx, desired_region:str=None):
        pass

    @commands.is_owner()
    @commands.command(name="spawn")
    async def cmd_spawn(self, context, message=None):
        pass

    @commands.is_owner()
    @commands.command(name="bind",
        usage="[channel_id]",
        help="""Changes the channel the bot listens to. If no argument is given binds to current channel.
        optional [channel_id] - will link the channel given, if permissible.
        """)
    async def cmd_bind(self, ctx, channel:discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel

        if channel.type == discord.ChannelType.private:
            await ctx.channel.send("Unable to bind to *direct messages*. Give *channel id* or give command in channel.")
            return
        else:
            if channel.guild.me.permissions_in(channel).send_message:
                pass # bind
            else:
                await ctx.channel.send(f"Unable to send messages in channel ({channel.name}) given")

    @commands.is_owner()
    @commands.command(name="clean", 
        aliases=["clear"], 
        help="Deletes # of messages")
    async def cmd_clean(self, context, numMessage:int=0):
        if numMessage == 0:
            for msg in self.bot.cached_message:
                await msg.delete()
        else:
            await context.channel.purge(limit=numMessage + 1)
    
    @commands.is_owner()
    @commands.command(name="debug",
        help="Admin testing bot")
    async def cmd_debug(self, context, *, message):
        embed = discord.Embed(type="rich", title="__Debug__", color=0x7F0000)
        embed.set_footer(text=message[:2048])
        try:
            embed.description = str(eval(message))
        except Exception as Err:
            print(f"Hit debug except: {Err}")
            embed.add_field(name="Error", value=Err)
            # embed.description = eval(message.content.lstrip(cmd).strip())
        await context.send(embed=embed)
        if context.message.channel.type == discord.ChannelType.text:
            await context.message.delete()
        return

if __name__ == '__main__':
    pokemon = PilPokemon()
    pokemon.obtain(1, gif=True, bwGif=False)
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
    else:
        sqlPokemon = qry.first()

    discord_id = 136665080820400128
    qry = tables.session.query(tables.Trainer).filter(tables.Trainer.id==discord_id)
    if not qry.first():
        print("User Add")
        sqlTrainer = tables.Trainer(id=discord_id)
        tables.session.add(sqlTrainer)
        tables.session.commit()
    else:
        sqlTrainer = qry.first()

    qry = (tables.session.query(tables.PokemonMapping)
        .join(tables.Trainer, tables.Trainer.id == tables.PokemonMapping.trainer_id)
        .join(tables.Pokemon, tables.Pokemon.id == tables.PokemonMapping.pokemon)
        .filter(tables.Pokemon.id==pokemon.details["id"],
                tables.Trainer.id==discord_id
        )
    )
    if not qry.first():
        print("Pokemon Mapping Add")
        sqlPokemonMap = tables.PokemonMapping(
            trainer_id=sqlTrainer.id,
            pokemon=sqlPokemon.id,
            move1=None,
            move2=None,
            move3=None,
            move4=None
        )
        tables.session.add(sqlPokemonMap)
        tables.session.commit()
    else:
        sqlPokemonMap = qry.first()