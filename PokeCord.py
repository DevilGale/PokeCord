import requests
import random
import time
from PIL import Image
from io import BytesIO

from MainVars import *


class PokeCord:
    def __init__(self):
        self.pokestore = None
        self.imgr_results = None

    @property    
    def appeared(self):
        print("A pokemon appeared: {}".format((self.pokestore != None)))
        return self.pokestore != None

    async def cmd_restart(self, cmd, message, content=None):
        await client.send_message(message.channel, 'Restarting...')
        client.close()
        os.execl(sys.executable, sys.executable, * sys.argv)

    async def cmd_shutdown(self, cmd, message, content=None):
        client.close()
        # exit()

    async def cmd_debug(self, cmd, message, content=None):
        if message.author.id == MASTER_ID:
            eval(message.content.lstrip(cmd).strip())
            try:
                print(eval(message.content.lstrip(cmd).strip()))
            except:
                print(str(eval(message.content.lstrip(cmd).strip())))
        embed = discord.Embed(type="rich", title="Debug", color=0xEEE8AA)
        embed.set_footer(text=message.content[:2048])
        try:
            embed.description = str(eval(message.content.lstrip(cmd).strip()))
        except:
            embed.description = eval(message.content.lstrip(cmd).strip())
        await client.send_message(message.channel, embed=embed)
        await client.delete_message(message)
        return

    async def cmd_edit_embed(self, cmd, message, content=None):
        msg_list = []
        message = await client.get_message(message.channel, content)
        msg_list.append(await client.send_message(message.channel, 'What in the embed do you want to change?'))
        msg_list.append(await client.wait_for_message(author=message.author))
        msg_list.append(await client.send_message(message.channel, 'What would you like it to change to?'))
        msg_list.append(await client.wait_for_message(author=message.author))
        for msg in msg_list:
            print("{}{}{}".format(bcolors.WARNING, msg.content, bcolors.ENDC))
        for embed in message.embeds:
            if msg_list[1].content.lower() == "title":
                embed.title = msg_list[3].content
            elif msg_list[1].content.lower() == "description":
                embed.description = msg_list[3].content
            elif msg_list[1].content.lower() == "color":
                embed.color = msg_list[3].content
            elif msg_list[1].content.lower() == "footer":
                embed.set_footer(text=msg_list[3].content)
            elif msg_list[1].content.lower() == "thumbnail":
                embed.set_thumbnail(url=msg_list[3].content)
            elif msg_list[1].content.lower() == "image":
                embed.set_image(url=msg_list[3].content)
            elif msg_list[1].content.lower() == "author":
                embed.set_author(name=msg_list[3].content)
            else:
                await client.send_message(message.channel, 'The requested field is not availiable.')
        client.delete_messages(msg_list)

    async def cmd_spawn(self, cmd, message, content=None):
        await client.send_message(message.channel, 'A Wild Pokémon appears!')
        if content.isdigit():
            url = "http://pokeapi.co/api/v2/pokemon/{}/".format(content)
        else:
            url = "http://pokeapi.co/api/v2/pokemon/" + str(random.randint(1,200)) + "/"
        t0 = time.clock()
        self.pokestore = requests.post(url).json()
        print("Obtained Pokemon - " + str(time.clock() - t0))
        embed = discord.Embed()
        embed.title = "Who's that Pokémon"
        embed.set_thumbnail(url=await self.convert_gif_bw(self.pokestore))
        await client.send_message(message.channel, embed=embed)

    async def check_capture(self, message):
        if self.pokestore is None:
            return
        if self.pokestore['name'] == message.content.lower():
            embed = discord.Embed(type="rich", title="Gotcha!", color=0xEEE8AA)
            embed.description = "{} was caught by {}".format(self.pokestore['name'].upper(), message.author.mention)
            embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/xyani/{}.gif".format(self.pokestore['name']))
            # await client.send_message(message.channel, "Gotcha!\n{} was caught by {}".format(self.pokestore['name'].upper(), message.author.mention))
            await client.send_message(message.channel, embed=embed)
            self.pokestore = None
            return

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

        shape_img.save('bw_image.png')

    async def convert_gif_bw(self, poke):
        txtfile_name = "test.gif"
        response = requests.get("https://play.pokemonshowdown.com/sprites/xyani/" + poke['name'] + ".gif")
        print("Obtained image")
        frames = Image.open(BytesIO(response.content))
        p = frames.getpalette()
        last_frame = frames.convert('RGBA')
        all_frames = []
        width, height = last_frame.size
        compilation = Image.new('RGBA', size=(width * 5, height * 5))

        try:
            while True:
                if not frames.getpalette():
                    frames.putpalette(p)

                current_frame = frames.convert('RGBA')   
                #It seems that each frame can have a base different color besides white
                if len(all_frames) <= 25:
                    compilation.paste(current_frame,box=(width * divmod(len(all_frames),6)[1], height * divmod(len(all_frames),6)[0]))
                    
                pixdata = current_frame.load()
                first_color_frame = pixdata[1,1]
                for x in range(0, width - 1):
                    for y in range(0, height - 1):
                        if pixdata[x,y] != first_color_frame:
                            pixdata[x,y] = black
                all_frames.append(current_frame)
                frames.seek(frames.tell() + 1)
        except EOFError:
            pass
        compilation.show(title="show_25")
        all_frames[0].save(txtfile_name, save_all=True, optimize=True, append_images=all_frames[1:], loop=1000)
        
        self.imgr_result = imgr_client.upload_from_path(txtfile_name, config=None, anon=True)['link']
        return self.imgr_result

    async def wait_msg_delete(self, msg, after):
        await asyncio.sleep(after)
        await client.delete_message(msg)

    async def cmd_info(self, cmd, message, content=None):
        print(cmd)
