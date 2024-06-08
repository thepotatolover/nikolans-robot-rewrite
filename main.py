import discord
from discord.ext import commands
import logging
import os

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot = discord.Bot(intents=discord.Intents.all())

bot.rulers = ["767780952436244491", "1118973285766533250"]
bot.logginghook = "https://discord.com/api/webhooks/f"
bot.suggestionshook = "https://discord.com/api/webhooks/f"
bot.logginghookname = "nikolan's robot logging"
bot.supportserver = "https://discord.gg/rgYmNt5BSg"
bot.ownername = "nikolan"

# code for the blacklist check
blacklisted = [] # make empty array

def reloadbl(): # function to refresh the blacklisted user list
    global blacklisted
    with open("data/blusers", 'r') as blfiles:
        blacklisted = blfiles.readlines()
bot.reloadbl = reloadbl # make the function available from all files
reloadbl() # run once before bot startup

@bot.check # will run before every command is executed
async def blacklist_check(ctx):
    global blacklisted
    if str(ctx.author.id) in str(blacklisted): # checks if user is blacklisted
        embed = discord.Embed(color=0xff0000, title="You have been blocked from using this bot!", description=f"If you think this was a mistake, join the [Discord Server]({bot.supportserver}) or DM @{bot.ownername}.")
        await ctx.respond(embed=embed, ephemeral=True) # tells user they is blacklisted
        return False # tells command not to execute
    return True # tells command to executey bc user isnt blacklisted

cogs = ['ping', 'ai', 'gimsa', 'dbg', 'apicmds', 'logging', "animals", 'steam', 'winkeys', 'help', 'suggestions']
for h in cogs:
    try:
        bot.load_extension(f"cogs.{h}")
        print(f"Loaded extension {h}")
    except Exception as e:
        print(f"Failed to load extension {h}: {e}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

bot.run("f")
