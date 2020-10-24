import discord
from discord.ext import commands
import random
import os
import discord.utils
import ast
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import json
import config

intents = discord.Intents.all()

#a function that loads the json file containing every guild's prefix and returns it
def get_prefix(bot, message):
    with open('./guild data/prefixes.json', 'r') as f:  #open the json file containing prefixes
        prefixes = json.load(f) #load it
    return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)  #return the prefix associated with the guild id

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents)

TOKEN = config.discord
giphy_api_key = config.giphy
reddit_client_id = config.client_id
reddit_client_secret = config.client_secret
rapid_api = config.rapid_api

#the for loop below loads every cog when starting the bot
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
bot.load_extension('jishaku')

#those below are developer only commands
#changes the bot's status and prints some things in my console to show that he's fully online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} - {bot.user.id}\ndiscord.py: v{discord.__version__}\n')
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name='Tomkyo Ghoul | >help'))

#creates a default value for the prefix when the bot joins a guild
@bot.event
async def on_guild_join(guild):
    with open ('./guild data/prefixes.json', 'r') as f: #open the json file containing prefixes
        prefixes = json.load(f) #load it
    prefixes[str(guild.id)] = '>'   #set the prefix to that guild to the default bot prefix
    with open('./guild data/prefixes.json', 'w') as f:  #open the json file in write mode
        json.dump(prefixes, f, indent=4)    #dump the new prefix

#remote leave a guild by it's id
@bot.command(hidden=True)
@commands.is_owner()
async def leave(ctx, guild_id: int): 
    embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Left guild: **{bot.get_guild(guild_id).name}**')
    await bot.get_guild(guild_id).leave()   #get the guild by it's id and leave it
    await ctx.send(embed=embed)

#logs the bot out
@bot.command(hidden=True)
@commands.is_owner()
async def logout(ctx):
    await ctx.message.add_reaction('\u2705')
    await bot.logout()

#loads a cog
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\u2705')

#loads all cogs
@bot.command(hidden=True)
@commands.is_owner()
async def loadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.message.add_reaction('\u2705')

#unloads a cog
@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\u2705')

#unloads all cogs
@bot.command(hidden=True)
@commands.is_owner()
async def unloadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.unload_extension(f'cogs.{filename[:-3]}')
            await ctx.message.add_reaction('\u2705')

#reloads a cog
@bot.command(aliases=['reload'], hidden=True)
@commands.is_owner()
async def _reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\u2705')

#reload all cogs
@bot.command(hidden=True)
@commands.is_owner()
async def reloadall(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.reload_extension(f'cogs.{filename[:-3]}')
            await ctx.message.add_reaction('\u2705')



#helper function for the eval
def cleanup_code(content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

#R. Danny's eval function
@bot.command(aliases=['eval', 'ev'], hidden=True)
@commands.is_owner()
async def _eval(ctx, *, body):
    _last_result = None
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': _last_result
    }
    env.update(globals())
    body = cleanup_code(body)
    stdout = io.StringIO()
    to_compile = f'async def func():\n{textwrap.indent(body, " ")}'
    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass
    if ret is None:
        if value:
            await ctx.send(f'```py\n{value}\n```')
        else:
            _last_result = ret
            await ctx.send(f'```py\n{value}{ret}\n```')

#start the bot
bot.run(TOKEN)