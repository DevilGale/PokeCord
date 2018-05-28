from MainVars import *
from PokeCord import *

Poke = PokeCord()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + "(ID: " + client.user.id + ")")
    print('~~~~~~~~~~~~')
    async for message in client.logs_from(client.get_channel(CHANNEL_IDs), limit=2):
        if (datetime.utcnow() - message.timestamp).total_seconds() <= 30:
            if message.content == "Restarting...":
                await client.edit_message(message, "Restarted!")
            if message.content == (BOT_PREFIX + "restart"):
                await client.add_reaction(message, '👌')

@client.event
async def on_message(message):
    if message.author == client.user or message.channel == CHANNEL_IDs:
            return
    if not message.content.startswith(BOT_PREFIX):
        if Poke.appeared:
            print("++++++")
            print("{}{} - {}{}".format(bcolors.BOLD, message.author, message.content, bcolors.ENDC))
            await Poke.check_capture(message)
            print("++++++")
        elif message.content == "restart" and message.author.id == MASTER_ID:
            await client.send_message(message.channel, 'Restarting...')
            client.close()
            os.execl(sys.executable, sys.executable, * sys.argv)
        else:
            return
    else:
        try:
            print("----")
            print("{}{} - {}{}".format(bcolors.HEADER, message.author, message.content, bcolors.ENDC))
            cmd_content = [message.content.split(" ")[0], " ".join(message.content.split(" ")[1:])]
            print('{}{}{}'.format(bcolors.WARNING, cmd_content, bcolors.ENDC))
            try:
                # print("{}await cmd_{}(\"{}\", message, {}){}".format(bcolors.OKBLUE, cmd_content[0].lstrip(BOT_PREFIX), cmd_content[0], cmd_content[1], bcolors.ENDC))
                # await eval("cmd_{}(\"{}\", message, {})".format(cmd_content[0].lstrip(BOT_PREFIX), cmd_content[0], cmd_content[1]))
                func = getattr(Poke, "cmd_" + cmd_content[0].lstrip(BOT_PREFIX))
                print("{}({}, {}, {})".format("cmd_" + cmd_content[0].lstrip(BOT_PREFIX), cmd_content[0], message, cmd_content[1]))
                await func(cmd_content[0], message, cmd_content[1])

            except Exception as Err:
                await client.send_message(message.channel, 'There is no command called: ' + message.content.split(" ")[0].lstrip(BOT_PREFIX))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("{}{} ({}) -> {}{}".format(bcolors.FAIL, fname, exc_tb.tb_lineno, Err, bcolors.ENDC))
            # except Exception as Err:
            #     await client.send_message(message.channel, 'There is no command called: ' + message.content.split(" ")[0].lstrip(BOT_PREFIX))
            #     exc_type, exc_obj, exc_tb = sys.exc_info()
            #     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #     print("{}{} ({}) -> {}{}".format(bcolors.FAIL, fname, exc_tb.tb_lineno, Err, bcolors.ENDC))
            #     return
        except Exception as Err:
            print(bcolors.FAIL + str(Err) + bcolors.ENDC)
        print()

# async def cmd_spawn(cmd, message):
#     await client.send_message(message.channel, 'A Wild Pokémon appears!')
#     url = "http://pokeapi.co/api/v2/pokemon/" + str(random.randint(1,200)) + "/"
    
#     pokestore = requests.get(url).json()
#     embed = discord.Embed()
#     # embed.set_image(url=pokestore['sprites']['front_default'])
#     embed.set_thumbnail(url=pokestore['sprites']['front_default'])
#     await client.send_message(message.channel, "Who's that Pokémon", embed=embed)
#     embed.set_thumbnail(url="https://play.pokemonshowdown.com/sprites/xyani/" + pokestore['name'] + ".gif")
#     await client.send_message(message.channel, "Who's that Pokémon", embed=embed)
#     print("Finished finding")

client.run(TOKEN)