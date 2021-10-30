from discord.ext import commands
import config as config
from Objects.user import *
#from pil import method_sum_check

import random
from datetime import time, datetime, timedelta

import log
import pickle
import requests
from PIL import Image, ImageDraw
from io import BytesIO

#Trainer -> [Items, box, ]

def check_is_pm(ctx):
    return ctx.message.channel.type == discord.ChannelType.private

    #return ctx.message.channel.type == discord.ChannelType.text

class PokeCord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_bind = {}
        self.time_to_spawn = None
        self.wild_pokemon = None #Spawned Pokemon
        self.imgur_results = None
        self.spawn_msg = None
        self.trainer_list = {}

    def __getstate__(self):
        return ({
            'channel_bind' : self.channel_bind,
            'time'         : self.time_to_spawn,
            'store'        : self.wild_pokemon,
            'imgur'        : self.imgur_results,
            'msg'          : self.spawn_msg,
            'users'        : self.trainer_list
            })
        pass

    def __setstate__(self, dictState):
        self.channel_bind  = dictState['channel_bind']
        self.time_to_spawn = dictState['time']
        self.wild_pokemon  = dictState['store']
        if 'imgr' in dictState:
            self.imgur_results = dictState['imgr']
        else:
            self.imgur_results = dictState['imgur']
        self.spawn_msg     = dictState['msg']
        self.trainer_list  = dictState['users']
        # if self.time_to_spawn != None: 
        #     asyncio.create_task(self.timed_spawn())

    @property
    def time_to_spawn(self):
        return self._time_to_spawn
    
    @time_to_spawn.setter
    def time_to_spawn(self, value):
        self._time_to_spawn = value

    def getSeconds(self):
        time_diff = (self.time_to_spawn - datetime.now()).total_seconds()
        if time_diff < 0:
            return 0
        else:
            return (self.time_to_spawn - datetime.now()).total_seconds()

    def setToSpawn(self):
        if self.time_to_spawn == None:
            return False
        else:
            return True

    @property    
    def appeared(self):
        #print("A pokemon appeared: {}".format((self.wild_pokemon != None)))
        return self.wild_pokemon != None

##############################################################################
##############################################################################
##############################################################################

        #If last command was restart
        #i = 0
        ##async for message in client.logs_from(client.get_channel(CHANNEL_IDs), limit=2):
        ##    if (datetime.utcnow() - message.timestamp).total_seconds() <= 30:
        ##        if message.content == "Restarting..." and i == 0:
        ##            await client.edit_message(message, "Restarted!")
        ##        if message.content == (BOT_PREFIX + "restart") and i == 1:
        ##            await client.add_reaction(message, '👌')
        ##    i = i + 1
    
    def update_pickle(self):
        with open("IO Files/PokeCord.pickle", 'wb') as file:
            try:
                pickle.dump(self, file)
                pass
            except Exception as Err:
                print(Err) 

    @commands.Cog.listener()
    async def on_command_completion(self, context):
        self.update_pickle()
        #print(dir(context)) #For checking is a command that changes the bot state

    #!! Someone get the last message or something
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            log.info(f"Access to - {guild.name}")
            if guild.id not in self.channel_bind:
                for channel in guild.text_channels:
                    log.info(f"{channel.name} - {guild.me.permissions_in(channel)}") # send_messages
                    if guild.me.permissions_in(channel).send_messages:
                        self.channel_bind[guild.id] = channel.id
                        break
                    log.info(f"{(guild.me.permissions_in(channel).send_messages)}")
                    #self.channel_bind[guild.id] = channels[0]
        #Check if a pokemon is queued to be spawned
        if self.appeared:
            game = discord.Game("Who's That Pokemon?")
            await self.bot.change_presence(status=discord.Status.online, activity=game)
        else:
            if self.setToSpawn():
                await asyncio.sleep(self.getSeconds())
                await self._spawn()
            else:
                self.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
                await asyncio.sleep(self.getSeconds())
                await self._spawn()
    #         #If time to spawn in the future set in motion
    #         if self.time_to_spawn > datetime.now():
    #             await asyncio.sleep(self.getSeconds())
    #         await self.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))

    @commands.Cog.listener()
    async def on_message(self, message):
        #Bot or wrong channel do nothing
        if (
            message.author == self.bot.user or 
            message.content[1:].startswith("spawn") or
            message.channel.type != discord.ChannelType.text
            ): #or message.channel == CHANNEL_IDs:
            return

        #print(f"[{datetime.now().strftime('%b-%d %H:%M')}] On Message ({message.channel.type}) {message.content}")
        #Pokemon is going to be found
        if self.setToSpawn():
            pass
        else:
            #Pokemon is ready for capture
            if self.appeared:
                if not await self.check_capture(message):
                    return
                if not self.setToSpawn():
                    self.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))    
                    await message.channel.send('Pokemon set to spawn!')
                    await asyncio.sleep(self.getSeconds())
                    await self._spawn()
            self.update_pickle()

    #     # [CHANGE] When a command is sent and a pokemon hasn't been set up it eats the command
    #     #If a pokemon isn't set to spawn and isn't up, set a random time
    #     if not self.setToSpawn() and not self.appeared:
    #         self.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
    #         await message.channel.send('Pokemon set to spawn!')
    #         await asyncio.sleep(self.getSeconds())
    #         await self.cmd_spawn('spawn', message)

    #-------------------------------------------------
    #                   Commands
    #-------------------------------------------------

    @commands.is_owner()
    @commands.command(name='bind',
        usage='[channel_id]',
        help="""Changes the channel the bot listens to. If no argument is given binds to current channel.
        optional [channel_id] - will link the channel given, if permissible.
        """
        )
    async def cmd_bind(self, ctx, channel:discord.TextChannel = None):
        if channel == None and ctx.message.channel.type == discord.ChannelType.private:
            await ctx.channel.send("Unable to bind to *direct messages*. Give *channel id* or give command in channel.")
            return
        elif channel == None:
            self.channel_bind[ctx.guild.id] = ctx.channel.id
        else:
            if not channel.guild.me.permissions_in(channel).send_messages:
                await ctx.channel.send(f"Unable to send messages in channel ({channel.name}) given")
            self.channel_bind[channel.guild.id] = channel.id

    @commands.command(name='info')
    async def cmd_info(self, context, emoji = None):
        await context.send("\u2716")
        foundEmoji = discord.utils.find(lambda m: m.name == 'heavy_multiplication_x', self.bot.emojis)
        if emoji == None:
            print("Info")
        else:
            print(emoji)

    @commands.is_owner()
    @commands.command(name='edit_embed')
    async def cmd_edit_embed(self, cmd, message, content=None):
        msg_list = []
        find_message = await message.channel.send(content)
        msg_list.append(await message.channel.send('What in the embed do you want to change?'))
        msg_list.append(await client.wait_for_message(author=message.author))
        msg_list.append(await message.channel.send('What would you like it to change to?'))
        msg_list.append(await client.wait_for_message(author=message.author))
        for msg in msg_list:
            print("{}{}{}".format(bcolors.WARNING, msg.content, bcolors.ENDC))
        for embed in find_message.embeds:
            new_embed = embed
            if msg_list[1].content.strip(" ")[1].lower() == "title":
                new_embed.title = msg_list[3].content
            elif msg_list[1].content.strip(" ")[1].lower() == "description":
                new_embed.description = msg_list[3].content
            elif msg_list[1].content.strip(" ")[1].lower() == "color":
                new_embed.color = msg_list[3].content
            elif msg_list[1].content.strip(" ")[1].lower() == "footer":
                new_embed.set_footer(text=msg_list[3].content)
            elif msg_list[1].content.strip(" ")[1].lower() == "thumbnail":
                new_embed.set_thumbnail(url=msg_list[3].content)
            elif msg_list[1].content.strip(" ")[1].lower() == "image":
                new_embed.set_image(url=msg_list[3].content)
            elif msg_list[1].content.strip(" ")[1].lower() == "author":
                new_embed.set_author(name=msg_list[3].content)
            else:
                await message.channel.send('The requested field is not availiable.')
            await client.edit_message(find_message, embed=new_embed)
        client.delete_messages(msg_list)

    @commands.command(name='spawn')
    @commands.is_owner()
    async def cmd_spawn(self, context, message=None):
        await self._spawn(context.channel, message)

    @commands.command(name='missing')
    async def cmd_missing(self, context, message=None):
        if self.spawn_msg != None:
            new_embed = discord.Embed()
            for embed in self.spawn_msg.embeds:
                new_embed = embed
                new_embed.set_thumbnail(url=imgur_result)
            await client.edit_message(self.spawn_msg, embed=new_embed)

    @commands.command(
        name='inventory', 
        aliases=['backpack'],
        help="Displays pokemon and items"
        )
    async def cmd_inventory(self, context, member:discord.Member = None):
        if member is None:
            if context.author.id in self.trainer_list.keys():
                #print(self.trainer_list[context.author.id])
                await context.channel.send(embed=self.trainer_list[context.author.id].embed_list(context.author))
            else:
                msg = "{} you have caught no Pokemon".format(context.author.name)
                await context.channel.send(msg)
        else:
            print(dir(member))
            if member.id in self.trainer_list:
                await context.author.send(embed=self.trainer_list[member.id].embed_list(member))
            else:
                await context.send(f"{member.name} has caught no Pokemon")

    @commands.command(name='bad_gif')
    @commands.is_owner()
    async def cmd_bad_gif(self, context, message=None):
        if message == None:
            if self.wild_pokemon == None:
                msg = "No pokemon is spawned"
                await context.channel.send(msg)
                return
            file = open("IO Files/badGIF.txt", 'a+')
            file.write("{}#{}\n".format(self.wild_pokemon['name'], self.wild_pokemon['id']))
            file.close()
            msg = "Pokemon has been added to file"
            await context.channel.send(msg)
        else:
            self.sort_gif_file()

    @commands.command(
        name='release', 
        usage='<pokemon> [pokemon index=0]',
        help="""Removes a pokemon from your inventory.
        <pokemon> - name of the pokemon you want to release
        optional [pokemon index] - caught multiple of the same pokemon and want to release a particular one
        """
        )
    async def cmd_release(self, ctx, pokemonName : str, pokemon_index:int = 0):
        if ctx.author.id in self.trainer_list:
            trainer = self.trainer_list[ctx.author.id]
            if trainer.hasPokemon(pokemonName):
                trainer.removePokemon(pokemonName)
                await ctx.channel.send(f"*{ctx.author.mention}*, {pokemonName} has been released.")    
            else:
                await ctx.channel.send(f"*{ctx.author.display_name}*, haven't caught any {pokemonName}.")    
        else:
            await ctx.channel.send(f"*{ctx.author.display_name}*, haven't caught any pokemon!")

    @commands.command(
        name='trade',
        help="Trade a pokemon between two users"
        )
    async def cmd_trade(self, ctx, member:discord.Member, give_pokemon:str, get_pokemon:str):
        if member.id in self.trainer_list and ctx.author.id in self.trainer_list:
            trainer_give = self.trainer_list[ctx.author.id]
            trainer_get = self.trainer_list[member.id]
            if not trainer_give.hasPokemon(give_pokemon):
                await ctx.send(f"*{ctx.author.display_name}* doesn't have that pokemon")
                return
            elif not trainer_get.hasPokemon(get_pokemon):
                await ctx.send(f"*{member.display_name}* doesn't have that pokemon")
                return
            else:
                sent_message = await ctx.send(f"*{member.display_name}*, *{ctx.author.display_name}* wants to trade {give_pokemon} for {get_pokemon}")
                await sent_message.add_reaction('\u2716') # X
                await sent_message.add_reaction('\u2714') # ✔

                def check(reaction, user):
                    #print(f"Reaction = {dir(reaction.emoji)} - {reaction.emoji}")
                    return (
                        user == member and 
                        reaction.message.id == sent_message.id and
                        (reaction.emoji == '\u2716' or reaction.emoji == '\u2714')
                    )

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("No Reponse. Canceling trade.")
                    await sent_message.delete()
                    pass
                else:
                    if reaction.emoji == '\u2714':
                        await ctx.send("Trade Accepted!")
                    else:
                        await ctx.send("Trade Rejected")
        else:
            await ctx.send("One of you haven't captured pokemon.")

    #-------------------------------------------------
    #               Other Functions
    #-------------------------------------------------

    async def timed_spawn(self, ctx):
        await asyncio.sleep(self.getSeconds())
        await self._spawn(ctx.channel)

    async def _spawn(self, channel=None, message=None):
        if channel == None:
            for channel in self.channel_bind.values():
                await self._spawn(self.bot.get_channel(channel))
            return

        self.time_to_spawn = None
        await channel.send('A Wild Pokémon appears!')
        if message != None:
            if message.isdigit():
                pokeNum = message
                url = f"http://pokeapi.co/api/v2/pokemon/{message}/"
            else:
                #print error
                msg = "When using spawn must be number if input given"
                await channel.send(msg)
                return
        else:
            pokeNum = str(random.randint(1,200))
            url = "http://pokeapi.co/api/v2/pokemon/" + pokeNum + "/"

        #Checks if Pokemon has already been found, if so pulls file
        if os.path.isfile("IO Files/Pokemon/Pokemon#{}".format(pokeNum)):
            with open('IO Files/Pokemon/Pokemon#{}'.format(pokeNum), 'r') as file:
                self.wild_pokemon = json.load(file)
        else:
            t0 = datetime.now()
            self.wild_pokemon = requests.post(url).json()
            log.info(f"Obtained Pokemon in {datetime.now() - t0}")
            with open(f"IO Files/Pokemon/Pokemon#{self.wild_pokemon['id']}", 'w') as file:
                json.dump(self.wild_pokemon, file)

        embed = discord.Embed()
        embed.title = "Who's that Pokémon"
        embed.set_thumbnail(url=await self.convert_gif_bw(self.wild_pokemon))
        sent_msg = await channel.send(embed=embed)
        self.spawn_msg = sent_msg.id

        game = discord.Game("Who's That Pokemon?")
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    def sort_gif_file(self):
        with open("IO Files/badGIF.txt", 'r') as file:
            docText = file.read().strip()
        #print(docText.split("\n"))
        docText = docText.split("\n")
        with open("IO Files/sorted_badGIF.txt", 'w') as file:
            file.write("\n".join(sorted(set(docText), key=lambda item: int(item.split('#')[-1]))))

    async def check_capture(self, message):
        if self.wild_pokemon is None:
            return False
        if self.wild_pokemon['name'] == message.content.lower():
            await self.bot.change_presence(status=discord.Status.invisible)

            print("[{}]: '{}' caught by {}".format(datetime.now().strftime("%b-%d %H:%M"), self.wild_pokemon['name'], message.author))
            embed = discord.Embed(type="rich", title="Gotcha!", color=0xEEE8AA)
            embed.description = "{} was caught by {}".format(self.wild_pokemon['name'].upper(), message.author.mention)
            embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/xyani/{}.gif".format(self.wild_pokemon['name']))
            # await client.send_message(message.channel, "Gotcha!\n{} was caught by {}".format(self.wild_pokemon['name'].upper(), message.author.mention))
            await message.channel.send(embed=embed)
            if message.author.id in self.trainer_list.keys():
                self.trainer_list[message.author.id].addPokeList(self.wild_pokemon, message.author)
            else:
                self.trainer_list[message.author.id] = User(message.author, self.wild_pokemon)
            self.wild_pokemon = None
            return True
        return False

    async def convert_bw(self, poke):
        response = requests.get(poke['sprites']['front_default'])
        print("Obtained Image")
        img = Image.open(BytesIO(response.content))
        shape_img = img.convert('RGBA')
        pixdata = shape_img.load()
        width, height = shape_img.size
        for x in range(0, width - 1):
            for y in range(0, height - 1):
                if pixdata[x,y] != (0, 0, 0, 0):
                    pixdata[x,y] = black
        shape_img.save('Images/bw_image.png')

    async def convert_gif_bw(self, poke):
        txtfile_name = "Images/PokeGIF.gif"
        #Get the gif file
        response = requests.get("https://play.pokemonshowdown.com/sprites/xyani/" + poke['name'] + ".gif")
        print("Obtained image: {}".format(response))
        #'Download' the file
        frames = Image.open(BytesIO(response.content))
        all_frames = []
        width, height = frames.size
        #Creates a viewing picture
        compilation = Image.new('RGBA', size=(width * 5, height * 10))

        prev_frame = Image.new('RGBA', size=frames.size, color=(255,255,255,0))
        for i in range(frames.n_frames):
            frames.seek(i)
            if len(all_frames) <= 50:
                    compilation.paste(frames, box=(width * int(i % 5), height * int(i / 5)))
                    
            disp_frame, prev_frame = method_dispose(frames, prev_frame)
            frames.seek(0)

            disp_frame = disp_frame.convert('RGB')
            pixdata = disp_frame.load()
            #Change Colors
            for x in range(width):
                for y in range(height):
                    if pixdata[x,y] != white:
                        pixdata[x,y] = black
            all_frames.append(disp_frame)

        compilation.save("Images/GIFcollage.png")
        #Save the gif
        all_frames[0].save(
            txtfile_name, 
            save_all=True, 
            append_images=all_frames[1:], 
            optimize=False,
            duration=frames.info['duration'],
            loop=0,
            disposal=1,
            transparency=255,
            background=0
            )
        #Upload to Imgur
        try:
            self.imgur_result = config.imgur_client.upload_from_path(txtfile_name, config=None, anon=True)['link']
        except Exception as Err:
            print(Err)
            raise Err
        return self.imgur_result

    async def wait_msg_delete(self, msg, after):
        await asyncio.sleep(after)
        await client.delete_message(msg)

    @commands.command(name='clean', aliases=['clear'], help='Deletes # of messages')
    @commands.is_owner()
    async def cmd_clean(self, context, numMessages: int = 0):
        if numMessages == 0:
            for msg in self.bot.cached_messages:
                await msg.delete()
        else:
            eleted = await context.channel.purge(limit=numMessages + 1)

    @commands.command(name='debug', help='Admin testing bot')# , hidden=True)
    @commands.is_owner()
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

def method_dispose(frames, previous_frame):
    # 0 PIL = Overlay and pass
    # 1 PIL = Overlay and return previous
    # 2 PIL = Erase Overlay
    new_frame = previous_frame.copy()
    current_frame = frames.convert()
    new_frame.alpha_composite(current_frame, dest=frames.dispose_extent[0:2], source=frames.dispose_extent)
    if frames.disposal_method == 0:
        return new_frame, Image.new('RGBA', box=frames.size)
    elif frames.disposal_method == 1:
        return new_frame, new_frame.copy()
    elif frames.disposal_method == 2 or frames.disposal_method == 3:
        draw = ImageDraw.Draw(previous_frame)
        draw.rectangle(frames.dispose_extent, fill=(white + (0,)))
        return new_frame, previous_frame.copy()
    else:
        print("UNKNOWN disposal_method")
        return current_frame, current_frame.copy()