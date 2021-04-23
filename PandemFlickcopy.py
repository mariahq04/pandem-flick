import discord
import os
from BOT_TOKENcopy import TOKEN
from discord.ext import commands

# if the '@' is first, bot will register the message as a command
client = commands.Bot(command_prefix='@')
# deleting the default 'help' command lets us create our own
client.remove_command('help')


# using cogs allows us to seperate each command/sets of commands into
# their own .py files to keep everything seperate, these are in the /cogs
# folder. 


# only owner of server may call these commandm if @command.is_owner is uncommented
# in discord type "!load [cog file name]" to load those commands to the bot
@client.command(name='load', hidden=True)
# @commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogscopy.{extension}')
    await ctx.send("loaded.")


# removes an active cog from the bot
@client.command(name='unload', hidden=True)
# @commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogscopy.{extension}')
    await ctx.send("unloaded.")


# reloads a specific cog that has been loaded
@client.command(name='reload', hidden=True)
# @commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogscopy.{extension}')
    client.load_extension(f'cogscopy.{extension}')
    await ctx.send("reloaded.")


# "calling !refresh updates all loaded cogs incase code has been chaanged"
@client.command(name='refresh', hidden=True)
async def refresh(ctx):
    for filename in os.listdir('/Users/jasmine/PycharmProjects/SearchComponent/cogscopy'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogscopy.{filename[:-3]}')
            client.load_extension(f'cogscopy.{filename[:-3]}')
    await ctx.send("Refreshed all cogs.")


# loop that initializes cogs
for filename in os.listdir('/Users/jasmine/PycharmProjects/SearchComponent/cogscopy'):
    if filename.endswith('.py'):
        client.load_extension(f'cogscopy.{filename[:-3]}')

# starts the bot, using TOKEN stored in BOT_TOKEN.py
client.run(TOKEN)
