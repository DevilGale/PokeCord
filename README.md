# PokeCord (Incomplete)

Is a bot where every so often a pokemon spawns and has to be guessed to be caught.

**Who's that Pokemon?**  
![](Images/who.gif)
![](Images/charizard.gif)

## Getting Started

### Installing

1. Create virtual environment `py -m venv venv && venv/Scripts/activate`

2. Install dependencies: `pip install -r requirements.txt`

3. Create a copy of `.env` and name it `.env.local`

4. Create your API secrets and put them in `.env.local`

- [imgur](https://api.imgur.com/oauth2/addclient)
  - Application name: `PokeCord` (can be whatever you want)
  - Authorization type: `OAuth 2 authorization with a callback URL`
  - Authorization callback URL: `https://imgur.com`
  - On submit, edit `imgr_client_id` and `imgr_client_secret`
- [discord](https://discordpy.readthedocs.io/en/latest/discord.html)

Example `.env.local`:

> MASTER_ID = "abcd#1234"
>
> CLIENT_ID = abcd1234
> ...

- **Note: the bot will still have to be added to the discord channel**

### Running

Run '[runbot.bat](runbot.bat)' after installing to start the bot.

- If you're using virtualenv: `py main.py`

## Built with

- Windows 10 (Untested on Linux)
- [discord.ext](https://discordpy.readthedocs.io/en/latest/ext/commands/index.html) - Interactions with Discord
- [Pillow](https://pillow.readthedocs.io/en/stable/reference/Image.html) - Image Editing
- [imgurpython](https://github.com/Imgur/imgurpython) - Image Uploading

## To-do

- [x] Catch-able Pokemon
- [ ] Admin Change spawn time
- [ ] Limit which region is spawned
- [ ] Fix checking and catching channel
- [ ] Fix Re-coloring
- [ ] Add items
- [ ] Add leveling and battling
- [ ] Add variabled spawn rate based off rarity (maybe)
