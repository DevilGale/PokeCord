# PokeCord (Incomplete)

Is a bot where every so often a pokemon spawns and has to be guessed to be caught.

**Who's that Pokemon?**  
![](Images/who.gif)
![](Images/charizard.gif)

## Getting Started

### Installing

Create your API secrets and input them into the '[var_secrets.py](var_secrets.py)' file, with the values enclosed in quotes.
- [imgur](https://api.imgur.com/oauth2/addclient)
- [discord](https://discordpy.readthedocs.io/en/latest/discord.html)

To install the dependencies for the project run `pip install -r requirements.txt`.

* **Note: the bot will still have to be added to the discord channel**

### Running

Run '[runbot.bat](runbot.bat)' after installing to start the bot.

## Built with

* Windows 10 (Untested on Linux)
* [discord.ext](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html) - Interactions with Discord
* [Pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html) - Image Editing 
* [imgurpython](https://github.com/Imgur/imgurpython) - Image Uploading

## To-do
- [x] Catch-able Pokemon
- [ ] Admin Change spawn time
- [ ] Limit which region is spawned
- [ ] Fix checking and catching channel
- [ ] Fix Re-coloring
- [ ] Add items
- [ ] Add leveling and battling
- [ ] Add variabled spawn rate based off rarity (maybe)