from Config import *
from PokeCord import *

from datetime import timedelta

if os.path.isfile("IO Files/PokeCord.pickle"):
    with open("IO Files/PokeCord.pickle", 'rb') as file:
        Poke = pickle.load(file)
else:
    Poke = PokeCord()

@client.event
async def on_ready():
    print('\nLogged in as ' + client.user.name + "(ID: " + client.user.id + ")")
    print('~~~~~~~~~~~~')
    #If last command was restart
    i = 0
    async for message in client.logs_from(client.get_channel(CHANNEL_IDs), limit=2):
        if (datetime.utcnow() - message.timestamp).total_seconds() <= 30:
            if message.content == "Restarting..." and i == 0:
                await client.edit_message(message, "Restarted!")
            if message.content == (BOT_PREFIX + "restart") and i == 1:
                await client.add_reaction(message, '👌')
        i = i + 1
    #Check if a pokemon is queued to be spawned
    if Poke.setToSpawn():
        #If time to spawn in the future set in motion
        if Poke.time_to_spawn > datetime.now():
            await asyncio.sleep(Poke.getSeconds())
            await Poke.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))
        #Otherwise spawn immedietely
        else:
            await Poke.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))

@client.event
async def on_message(message):
    #Bot or wrong channel do nothing
    if message.author == client.user or message.channel == CHANNEL_IDs:
        return
    print("----")
    print("[{}]{} {} - {}{}".format(datetime.now().strftime("%I:%M %p"), bcolors.HEADER, message.author, message.content, bcolors.ENDC))
    
    '''
    #Pokemon is going to be found
    if Poke.setToSpawn():
        pass
    else:
        #Pokemon is ready for capture
        if Poke.appeared:
            await Poke.check_capture(message)
        else:
            Poke.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
            await client.send_message(message.channel, 'Pokemon set to spawn!')
            await asyncio.sleep(Poke.getSeconds())
            await Poke.cmd_spawn('spawn', message)
        update_pickle()
    '''

    #If a pokemon isn't set to spawn and isn't up, set a random time
    if not Poke.setToSpawn() and not Poke.appeared:
        Poke.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
        await client.send_message(message.channel, 'Pokemon set to spawn!')
        await asyncio.sleep(Poke.getSeconds())
        await Poke.cmd_spawn('spawn', message)
    #Not a command
    if not message.content.startswith(BOT_PREFIX):
        if Poke.appeared:
            if await Poke.check_capture(message):
                update_pickle()
        elif message.content == "restart" and message.author.id == MASTER_ID:
            await client.send_message(message.channel, 'Restarting...')
            client.close()
            os.execl(sys.executable, sys.executable, * sys.argv)
        else:
            return
    else:

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