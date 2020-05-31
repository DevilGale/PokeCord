from discord.ext import commands
from Config import *
from Objects.user import *

# sys is needed for the restart function. See line 142.
import sys

from datetime import time, datetime, timedelta

import requests
from PIL import Image
from io import BytesIO

#Trainer -> [Items, box, ]

class PokeCord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.time_to_spawn = None
        self.pokestore = None
        self.imgr_results = None
        self.spawn_msg = None
        self.users_list = {}

    def __getstate__(self):
        return ({
            'time'  : self.time_to_spawn,
            'store' : self.pokestore,
            'imgr'  : self.imgr_results,
            'msg'   : self.spawn_msg,
            'users' : self.users_list
            })
        pass

    def __setstate__(self, dictState):
        self.time_to_spawn = dictState['time']
        self.pokestore     = dictState['store']
        self.imgr_results  = dictState['imgr']
        self.spawn_msg     = dictState['msg']
        self.users_list    = dictState['users']
        pass

    @property
    def time_to_spawn(self):
        return self._time_to_spawn
    
    @time_to_spawn.setter
    def time_to_spawn(self, value):
        self._time_to_spawn = value

    def getSeconds(self):
        return (self.time_to_spawn - datetime.now()).total_seconds()

    def setToSpawn(self):
        if self.time_to_spawn == None:
            return False
        else:
            return True

    @property    
    def appeared(self):
        #print("A pokemon appeared: {}".format((self.pokestore != None)))
        return self.pokestore != None

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
    
    @commands.command(name='info')
    async def cmd_info(self, context):
        print("Info")

    @commands.Cog.listener()
    async def on_command_completion(self, context):
        self.update_pickle()
        #print(dir(context)) #For checking is a command that changes the bot state

    def update_pickle(self):
        with open("IO Files/PokeCord.pickle", 'wb') as file:
            try:
                pickle.dump(self, file)
                pass
            except Exception as Err:
                print(Err) 

    @commands.Cog.listener()
    async def on_ready(self):
        print("Listening")
        #Check if a pokemon is queued to be spawned
        if self.setToSpawn():
            #If time to spawn in the future set in motion
            if self.time_to_spawn > datetime.now():
                await asyncio.sleep(self.getSeconds())
            await self.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))

    @commands.Cog.listener()
    async def on_message(self, message):
        #Bot or wrong channel do nothing
        if message.author == self.bot.user or message.content[1:].startswith("spawn"): #or message.channel == CHANNEL_IDs:
            return

        #Pokemon is going to be found
        if self.setToSpawn():
            pass
        else:
            #Pokemon is ready for capture
            if self.appeared:
                await self.check_capture(message)
            else:
                self.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
                await message.channel.send('Pokemon set to spawn!')
                await asyncio.sleep(self.getSeconds())
                await self._spawn(message)
            self.update_pickle()

    #     # [CHANGE] When a command is sent and a pokemon hasn't been set up it eats the command
    #     #If a pokemon isn't set to spawn and isn't up, set a random time
    #     if not self.setToSpawn() and not self.appeared:
    #         self.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
    #         await message.channel.send('Pokemon set to spawn!')
    #         await asyncio.sleep(self.getSeconds())
    #         await self.cmd_spawn('spawn', message)

    #     #Not a command
    #     if not message.content.startswith(BOT_PREFIX):
    #         if self.appeared:
    #             if await self.check_capture(message):
    #                 update_pickle()

    @commands.command(name='restart')
    async def cmd_restart(self, ctx, message=None):
        await ctx.channel.send('Restarting...')
        await self.bot.close()
        os.execl(sys.executable, sys.executable, * sys.argv)

    @commands.command(name='shutdown')
    @commands.is_owner()
    async def cmd_shutdown(self, context):
        await self.bot.close()
        # exit()

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
        await self._spawn(context, message)

    async def _spawn(self, context, message=None):
        self.time_to_spawn = None
        await context.channel.send('A Wild Pokémon appears!')
        if message != None:
            if message.isdigit():
                pokeNum = message
                url = f"http://pokeapi.co/api/v2/pokemon/{message}/"
            else:
                #print error
                msg = "When using spawn must be number if input given"
                await context.channel.send(msg)
                return
        else:
            pokeNum = str(random.randint(1,200))
            url = "http://pokeapi.co/api/v2/pokemon/" + pokeNum + "/"
        #Checks if Pokemon number exists. If it does pulls file
        if os.path.isfile("IO Files/Pokemon/Pokemon#{}".format(pokeNum)):
            with open('IO Files/Pokemon/Pokemon#{}'.format(pokeNum), 'r') as file:
                self.pokestore = json.load(file)
        else:
            t0 = datetime.now()
            self.pokestore = requests.post(url).json()
            print(f"Obtained Pokemon - {datetime.now() - t0}")
            with open(f"IO Files/Pokemon/Pokemon#{self.pokestore['id']}", 'w') as file:
                json.dump(self.pokestore, file)
        embed = discord.Embed()
        embed.title = "Who's that Pokémon"
        embed.set_thumbnail(url=await self.convert_gif_bw(self.pokestore))
        sent_msg = await context.channel.send(embed=embed)
        self.spawn_msg = sent_msg.id

        game = discord.Game("Who's That Pokemon?")
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    @commands.command(name='missing')
    async def cmd_missing(self, context, message=None):
        if self.spawn_msg != None:
            new_embed = discord.Embed()
            for embed in self.spawn_msg.embeds:
                new_embed = embed
                new_embed.set_thumbnail(url=imgr_result)
            await client.edit_message(self.spawn_msg, embed=new_embed)

    @commands.command(name='inventory')
    async def cmd_inventory(self, context):
        # prnt_txt = self.users_list[message.author]
        if context.author.id in self.users_list.keys():
            #print(self.users_list[context.author.id])
            await context.channel.send(embed=self.users_list[context.author.id].embed_list(context.author))
        else:
            msg = "{} you have caught no Pokemon".format(context.author.name)
            await context.channel.send(msg)

    @commands.command(name='bad_gif')
    @commands.is_owner()
    async def cmd_bad_gif(self, context, message=None):
        if message == None:
            if self.pokestore == None:
                msg = "No pokemon is spawned"
                await context.channel.send(msg)
                return
            file = open("IO Files/badGIF.txt", 'a+')
            file.write("{}#{}\n".format(self.pokestore['name'], self.pokestore['id']))
            file.close()
            msg = "Pokemon has been added to file"
            await context.channel.send(msg)
        else:
            self.sort_gif_file()

    def sort_gif_file(self):
        with open("IO Files/badGIF.txt", 'r') as file:
            docText = file.read().strip()
        #print(docText.split("\n"))
        docText = docText.split("\n")
        with open("IO Files/sorted_badGIF.txt", 'w') as file:
            file.write("\n".join(sorted(set(docText), key=lambda item: int(item.split('#')[-1]))))

    async def check_capture(self, message):
        if self.pokestore is None:
            return False
        if self.pokestore['name'] == message.content.lower():
            await self.bot.change_presence(status=discord.Status.invisible)

            embed = discord.Embed(type="rich", title="Gotcha!", color=0xEEE8AA)
            embed.description = "{} was caught by {}".format(self.pokestore['name'].upper(), message.author.mention)
            embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/xyani/{}.gif".format(self.pokestore['name']))
            # await client.send_message(message.channel, "Gotcha!\n{} was caught by {}".format(self.pokestore['name'].upper(), message.author.mention))
            await message.channel.send(embed=embed)
            if message.author.id in self.users_list.keys():
                self.users_list[message.author.id].addPokeList(self.pokestore, message.author)
            else:
                self.users_list[message.author.id] = User(message.author, self.pokestore)
            self.pokestore = None
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
        p = frames.getpalette()
        last_frame = frames.convert('RGBA')
        all_frames = []
        width, height = last_frame.size
        #Creates a viewing picture
        compilation = Image.new('RGBA', size=(width * 5, height * 10))

        for i in range(frames.n_frames):
            frames.seek(i)
            if len(all_frames) <= 50:
                    compilation.paste(frames.convert('RGBA'),box=(width * divmod(len(all_frames),6)[1], height * divmod(len(all_frames),9)[0]))
                    
            if i != 0:
                curr_frame = frames.convert('RGBA')
                disp_frame = Image.alpha_composite(prev_frame, curr_frame)
            else:
                disp_frame = frames.convert('RGBA')
            pixdata = disp_frame.load()
            for x in range(width - 1):
                for y in range(height - 1):
                    if pixdata[x,y][3] == 255:
                        pixdata[x,y] = black
                    else:
                        pixdata[x,y] = white
            all_frames.append(disp_frame)

            prev_frame = frames.convert('RGBA')

        # try:
        #     while True:
        #         if not frames.getpalette():
        #             frames.putpalette(p)

        #         current_frame = frames.convert('RGBA')   
        #         #It seems that each frame can have a base different color besides white
        #         if len(all_frames) <= 50:
        #             compilation.paste(current_frame,box=(width * divmod(len(all_frames),6)[1], height * divmod(len(all_frames),9)[0]))
                    
        #         pixdata = current_frame.load()
        #         first_color_frame = pixdata[1,1]
        #         for x in range(0, width - 1):
        #             for y in range(0, height - 1):
        #                 if pixdata[x,y][3] == 255:
        #                     pixdata[x,y] = black + (255,)
        #                 else
        #                     pixdata[x,y] = white + (255,)
        #                 # if pixdata[x,y] != first_color_frame:
        #                 #     pixdata[x,y] = black
        #         all_frames.append(current_frame)
        #         frames.seek(frames.tell() + 1)
        # except EOFError:
        #     pass
        # compilation.show(title="show_25")
        compilation.save("Images/GIFcollage.png")
        #Save the gif
        all_frames[0].save(txtfile_name, save_all=True, optimize=True, append_images=all_frames[1:], loop=1000)
        #Upload to Imgr
        try:
            self.imgr_result = imgr_client.upload_from_path(txtfile_name, config=None, anon=True)['link']
        except Exception as Err:
            print(Err)
            raise Err
        return self.imgr_result

    async def wait_msg_delete(self, msg, after):
        await asyncio.sleep(after)
        await client.delete_message(msg)

    @commands.command(name='clean')
    @commands.is_owner()
    async def cmd_clean(self, context, numMessages: int = 0):
        if numMessages == 0:
            for msg in self.bot.cached_messages:
                await msg.delete()
        else:
            deleted = await context.channel.purge(limit=numMessages + 1)

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
        await context.message.delete()
        return
