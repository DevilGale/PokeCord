from Config import *
from PokeCord import *

if os.path.isfile("IO Files/PokeCord.pickle"):
    with open("IO Files/PokeCord.pickle", 'rb') as file:
        Poke = pickle.load(file)
else:
    Poke = PokeCord()

@client.event
async def on_ready():
    print('\nLogged in as ' + client.user.name + "(ID: " + client.user.id + ")")
    print('~~~~~~~~~~~~')
    async for message in client.logs_from(client.get_channel(CHANNEL_IDs), limit=2):
        if (datetime.utcnow() - message.timestamp).total_seconds() <= 30:
            if message.content == "Restarting...":
                await client.edit_message(message, "Restarted!")
            if message.content == (BOT_PREFIX + "restart"):
                await client.add_reaction(message, '👌')

@client.event
async def on_message(message):
    #Bot or wrong channel do nothing
    if message.author == client.user or message.channel == CHANNEL_IDs:
        return
    #Not a command
    if not message.content.startswith(BOT_PREFIX):
        if Poke.appeared:
            print("++++++")
            print("{}{} - {}{}".format(bcolors.BOLD, message.author, message.content, bcolors.ENDC))
            if await Poke.check_capture(message):
                update_pickle()
            print("++++++")
        elif message.content == "restart" and message.author.id == MASTER_ID:
            await client.send_message(message.channel, 'Restarting...')
            client.close()
            os.execl(sys.executable, sys.executable, * sys.argv)
        else:
            return
    else:
        print("----")
        print("{}{} - {}{}".format(bcolors.HEADER, message.author, message.content, bcolors.ENDC))
        cmd_content = [message.content.split(" ")[0], " ".join(message.content.split(" ")[1:])]
        if cmd_content[1] == '':
            cmd_content[1] = None
        print('{}{}{}'.format(bcolors.WARNING, cmd_content, bcolors.ENDC))
        try:
            func = getattr(Poke, "cmd_" + cmd_content[0].lstrip(BOT_PREFIX))
            print("{}({}, {}, {})".format("cmd_" + cmd_content[0].lstrip(BOT_PREFIX), cmd_content[0], message, cmd_content[1]))
            await func(cmd_content[0], message, cmd_content[1])
            update_pickle()
        #If no function is named what was called
        except AttributeError:
            await client.send_message(message.channel, 'There is no command called: ' + message.content.split(" ")[0].lstrip(BOT_PREFIX))
        #If an error occurs
        except Exception as Err:
            await client.send_message(message.channel, 'Something went wrong')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print("{}{} ({}) -> {}{}".format(bcolors.FAIL, fname, exc_tb.tb_lineno, Err, bcolors.ENDC))

        print()

def update_pickle():
    with open("IO Files/PokeCord.pickle", 'wb') as file:
        pickle.dump(Poke, file)

client.run(TOKEN)