import discord
from discord.ext import commands
import os
import discord.utils
import io
import asyncio
import random
import textwrap
import traceback
from contextlib import redirect_stdout
import json
import config
from cogs.errors import CustomChecks

intents = discord.Intents.all()
mentions = discord.AllowedMentions(everyone=False)

TOKEN = config.discord
giphy_api_key = config.giphy
reddit_client_id = config.client_id
reddit_client_secret = config.client_secret
rapid_api = config.rapid_api
wolfram_key = config.wolfram_key

#a function that loads the json file containing every guild's prefix and returns it
def get_prefix(bot, message):
    with open('./guild data/prefixes.json', 'r') as f:  #open the json file containing prefixes
        prefixes = json.load(f) #load it
    return commands.when_mentioned_or(prefixes[str(message.guild.id)])(bot, message)  #return the prefix associated with the guild id

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, allowed_mentions=mentions, intents=intents)

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
    except:
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

@bot.command(hidden=True, aliases=['1000-7', "Jason", "Yamori", "Kaneki", "Ghoul", "Rize"])
@CustomChecks.blacklist_check()
async def whats1000_7(ctx):
    gif_list=[
        "https://cdn.discordapp.com/attachments/725102631185547427/777798974862000168/8IzZ.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799001034194954/9477f98e6d5154911c05467c4acb24c5.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799013637423114/090267babdec0455aab0ae6188dddc5b.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799047175995392/1431501301_tumblr_nldqrc0dEW1r4jf9no1_r1_540.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799063818993714/a06f456bf3d252555da9622c857196b2aaf6716d_hq.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799072492552192/bf7cf8d6d8867fc263263ed42fdcf22e.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799101978509322/community_image_1416272108.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799120764928010/d13a02578a2ebe3c49f716173b3898f3.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799134559207434/f2ff2d9b85e7cc3b8da34b7b9bf40838.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799141459361812/f5f0311ae14f89a9f2db18e1d4033b2da0328186_hq.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799169741815818/kaneki1.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799217879580702/kaneki-awaken-psychotic.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799311844704276/kanekis-ghoul-eye.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799414811066388/kaneki-torture.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799419390591016/Rize.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799518707253258/tenor.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799554358837258/tumblr_njoggkgHvZ1u8p62eo1_500.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799573170421760/tumblr_nlhqaraUlV1r2gwz1o1_500.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799598575714364/tumblr_nupzk4akgr1rvxid3o1_400.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799618502721547/tumblr_o3y583ncOp1tqjhmao1_500.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799665646436392/tumblr_o3y583ncOp1tqjhmao3_r1_500.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799682453667870/tumblr_o3y583ncOp1tqjhmao4_r2_500.gif",
        "https://cdn.discordapp.com/attachments/725102631185547427/777799698673041408/tumblr_og6j4zpttY1tqjhmao1_500.gif",
        "https://tenor.com/view/sherrybirkin-kanekiken-kaneki-tokyo-ghoul-gif-9563195",
        "https://tenor.com/view/kanekiscream-gif-5669942",
        "https://tenor.com/view/kaneki-gif-5972481",
        "https://tenor.com/view/kanekiken-tokyoghoul-centipede-gif-7687999",
        "https://tenor.com/view/kaneki-ken-anime-horrible-gif-11872797",
        "https://tenor.com/view/kaneki-kaneki-ken-tokyo-ghoul-kaneki-tokyo-ghoul-kaneki-ken-tokyo-ghoul-gif-16567958",
        "https://tenor.com/view/kaneki-tokyo-ghoul-gif-10538639",
        "https://tenor.com/view/jason-kaneki-anime-tokyo-ghoul-gif-13016916",
        "https://tenor.com/view/sherrybirkin-kanekiken-kaneki-tokyoghoul-gif-9579276",
        "https://tenor.com/view/sherrybirkin-kanekiken-kaneki-tokyoghoul-gif-9579304",
        "https://tenor.com/view/kaneki-ken-tokyo-ghoul-transform-anime-gif-17947332",
        "https://tenor.com/view/kaneki-tokyo-ghoul-transformation-gif-9291708",
        "https://tenor.com/view/anime-tokyoghoul-kaneki-gif-5125910",
        "https://tenor.com/view/tokyo-ghoul-kaneki-touka-kaneki-x-touka-gif-9498908",
        "https://tenor.com/view/kaneki-vs-jason-tokyo-ghoul-anime-hit-it-fight-gif-16128860",
        "https://tenor.com/view/jason-vs-kaneki-tokyo-ghoul-dash-jump-gif-15922547",
        "https://tenor.com/view/tokyo-ghoul-jason-omar-es-gay-yakumo-oomori-gif-14355745",
        "https://tenor.com/view/tokyo-ghoul-jason-gif-5319896",
        "https://tenor.com/view/kaneki-haise-gone-tokyo-ghoul-kaneki-gone-gif-18847282",
        "https://tenor.com/view/sherry-birkin-rize-kashimiro-tokyo-ghoul-gif-9646157",
        "https://tenor.com/view/tokyoghoul-gif-7918613"
    ]
    x=993
    embed = discord.Embed(color=0xffffff, title="What's 1000-7?", description=f"{x}...")
    embed.set_image(url=random.choice(gif_list))
    embed.set_author(name='Tokyo Ghoul', icon_url=bot.user.avatar_url)
    message = await ctx.send(embed=embed)
    await asyncio.sleep(5)
    while x > 1:
        x -= 7
        embed.description = f"{x}..."
        embed.set_image(url=random.choice(gif_list))
        await message.edit(embed=embed)
        await asyncio.sleep(5)


#start the bot
bot.run(TOKEN)
