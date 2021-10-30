import env, log, sys, config, pickle
from pathlib import Path
from PokeCord import *

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

bot = commands.Bot(command_prefix=config.BOT_PREFIX)

@bot.event
async def on_connect():
    log.separator()
    log.info(f"Logged in as {bot.user.name}(ID: {bot.user.id})")
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
    log.info(f"'{context.command}' by {context.author}")
    pass

@bot.event
async def on_command_error(ctx, error):
    print(error)
    #print(dir(error))
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command(name='restart')
async def cmd_restart(ctx):
    print(sys.executable)
    print(sys.argv)
    await ctx.send('Restarting...')
    try:
        await bot.close()
    except:
        pass
    finally:
        os.execl(Path(sys.executable), '"' + sys.executable + '"', * sys.argv)

@bot.command(name='shutdown')
@commands.is_owner()
async def cmd_shutdown(context):
    await bot.close()

log.info("Start Bot")
bot.run(env.get("TOKEN"))