from Config import *
from PokeCord import *

from datetime import timedelta, datetime

#from discord import utils

# Checking folders exist
if not os.path.isdir("IO Files/"):
    print("Creating IO Files folder...")
    os.makedirs("IO Files")

if not os.path.isdir("IO Files/Pokemon/"):
    print("Creating Pokemon folder...")
    os.makedirs("IO Files/Pokemon/")

if not os.path.isdir("Images"):
    print("Creating Images folder...")
    os.makedirs("Images")

# Checking pickle exists

# if os.path.isfile("IO Files/PokeCord.pickle"):
#     with open("IO Files/PokeCord.pickle", 'rb') as file:
#         Poke = pickle.load(file)
#     if not Poke:
#         Poke = PokeCord()
# else:
#     Poke = PokeCord()

#Load permissions
#.read()

# @client.event
# async def on_ready():
#     print("Started")
#     print('\nLogged in as ' + client.user.name + "(ID: " + str(client.user.id) + ")")
#     print('~~~~~~~~~~~~')
#     type_in = input(">>> ")
#     while(type_in != "exit"):
#         try:
#             print(str(eval(type_in)))
#         except AttributeError as e:
#             pass
#             #print("ERROR: {1}".format(e(1)))
#         except TypeError as e:
#             pass
#             #print("({0}): {1}".format(e))
#         except NameError as e:
#             pass
#             #print("({0}): {1}".format(e[1]))
#         type_in = input(">>> ")
#     #If last command was restart
#     #i = 0
#     ##async for message in client.logs_from(client.get_channel(CHANNEL_IDs), limit=2):
#     ##    if (datetime.utcnow() - message.timestamp).total_seconds() <= 30:
#     ##        if message.content == "Restarting..." and i == 0:
#     ##            await client.edit_message(message, "Restarted!")
#     ##        if message.content == (BOT_PREFIX + "restart") and i == 1:
#     ##            await client.add_reaction(message, '👌')
#     ##    i = i + 1
#     #Check if a pokemon is queued to be spawned
#     if Poke.setToSpawn():
#         #If time to spawn in the future set in motion
#         if Poke.time_to_spawn > datetime.now():
#             await asyncio.sleep(Poke.getSeconds())
#             await Poke.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))
#         #Otherwise spawn immedietely
#         else:
#             await Poke.cmd_spawn('spawn', client.get_channel(CHANNEL_IDs))

# @client.event
# async def on_message(message):
#     #Bot or wrong channel do nothing
#     if message.author == client.user or message.channel == CHANNEL_IDs:
#         return
#     print("----")
#     print("[{}]{} {} - {}{}".format(datetime.now().strftime("%I:%M %p"), bcolors.HEADER, message.author, message.content, bcolors.ENDC))
    
#     '''
#     #Pokemon is going to be found
#     if Poke.setToSpawn():
#         pass
#     else:
#         #Pokemon is ready for capture
#         if Poke.appeared:
#             await Poke.check_capture(message)
#         else:
#             Poke.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
#             await client.send_message(message.channel, 'Pokemon set to spawn!')
#             await asyncio.sleep(Poke.getSeconds())
#             await Poke.cmd_spawn('spawn', message)
#         update_pickle()
#     '''

#     # [CHANGE] When a command is sent and a pokemon hasn't been set up it eats the command
#     #If a pokemon isn't set to spawn and isn't up, set a random time
#     if not Poke.setToSpawn() and not Poke.appeared:
#         Poke.time_to_spawn = datetime.now() + timedelta(minutes=random.randint(1,10))
#         await message.channel.send('Pokemon set to spawn!')
#         await asyncio.sleep(Poke.getSeconds())
#         await Poke.cmd_spawn('spawn', message)

#     #Not a command
#     if not message.content.startswith(BOT_PREFIX):
#         if Poke.appeared:
#             if await Poke.check_capture(message):
#                 update_pickle()
#         elif message.content == "restart" and message.author.id == MASTER_ID:
#             await message.channel.send('Restarting...')
#             await client.close()
#             os.execl(sys.executable, sys.executable, * sys.argv)
#         else:
#             return
#     else:
#         print(message)
#         cmd_content = [message.content.split(" ")[0], " ".join(message.content.split(" ")[1:])]
#         if cmd_content[1] == '':
#             cmd_content[1] = None
#         print('{}{}{}'.format(bcolors.WARNING, cmd_content, bcolors.ENDC))
#         try:
#             func = getattr(Poke, "cmd_" + cmd_content[0].lstrip(BOT_PREFIX))
#             print("{}({}, {}, {})".format("cmd_" + cmd_content[0].lstrip(BOT_PREFIX), cmd_content[0], message, cmd_content[1]))
#             await func(cmd_content[0], message, cmd_content[1])
#             update_pickle()
#         #If no function is named what was called
#         except AttributeError:
#             await message.channel.send('There is no command called: ' + message.content.split(" ")[0].lstrip(BOT_PREFIX))
#         #If an error occurs
#         except Exception as Err:
#             await message.channel.send('Something went wrong')
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print("{}{} ({}) -> {}{}".format(bcolors.FAIL, fname, exc_tb.tb_lineno, Err, bcolors.ENDC))

#         print()

def update_pickle():
    print("Update Pickle!")
    with open("IO Files/PokeCord.pickle", 'wb') as file:
        try:
           pickle.dump(Poke.users_list, file)
        except Exception as Err:
            print(Err)    

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print('\nLogged in as ' + bot.user.name + "(ID: " + str(bot.user.id) + ")")
    print('~~~~~~~~~~~~')
    if os.path.isfile("IO Files/PokeCord.pickle"):
        with open("IO Files/PokeCord.pickle", 'rb') as file:
            try:
                Poke = pickle.load(file)
                if isinstance(Poke, PokeCord):
                    print("Found obj")
                    Poke.bot = bot
                else:
                    print("Couldn't Find")
                    Poke = PokeCord(bot)
            except EOFError:
                Poke = PokeCord(bot)
            except Exception as Err:
                print(Err)
                pass
    else:
        Poke = PokeCord(bot)
    bot.add_cog(Poke)

@bot.event
async def on_command(context):
    print("[{}]: '{}' by {}".format(datetime.now().strftime("%b-%d %H:%M"), context.command, context.author))
    pass

@bot.event
async def on_command_error(ctx, error):
    print(error)
    #print(dir(error))
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)