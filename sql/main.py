# Probject Libs
from PokeCord import PokeCord
import env, log
# Pip Libs
from discord.ext import commands
from pathlib import Path

def setupFolders():
    imgFolder = Path('Images')
    if not imgFolder.exists():
        imgFolder.mkdir()
    pass


bot = commands.Bot(command_prefix=env.get("BOT_PREFIX"))

@bot.event
async def on_connect():
    log.separator()
    log.info(f"Logged in as {bot.user.name}(ID: {bot.user.id})")
    Poke = PokeCord(bot)
    bot.add_cog(Poke)

@bot.event
async def on_command(context):
    log.info(f"'{context.command}' by {context.author}")
    pass

@bot.event
async def on_command_error(ctx, error):
    log.info(error)
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command(name='restart')
async def cmd_restart(ctx):
    pass
    # print(sys.executable)
    # print(sys.argv)
    # await ctx.send('Restarting...')
    # try:
    #     await bot.close()
    # except:
    #     pass
    # finally:
    #     os.execl(Path(sys.executable), '"' + sys.executable + '"', * sys.argv)

@bot.command(name='shutdown')
@commands.is_owner()
async def cmd_shutdown(context):
    await bot.close()

if __name__ == '__main__':
    setupFolders()
    log.info("Start Bot")
    bot.run(env.get("TOKEN"))
