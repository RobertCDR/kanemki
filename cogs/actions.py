import discord
from discord.ext import commands
import json
import aiohttp
import random
from bot import giphy_api_key
from cogs.errors import CustomChecks

class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Actions"

    #search a gif from giphy
    #the other commands are almost the same, except the search variable already has a value
    @commands.command(help="get a gif from GIPHY", usage="gif <query>###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gif(self, ctx, *, query):
        query = query.replace(' ', '+')   #replace the spaces with plus signs otherwise the request link will be broken
        url = f'http://api.giphy.com/v1/gifs/search?q={query}&api_key={giphy_api_key}&limit=10'
        session = aiohttp.ClientSession()   #create a session using aiohttp
        embed = discord.Embed(color=random.randint(0, 0xffffff))  #create the embed
        try:    #when no results are found catch the errorwith try and except
            response = await session.get(url=url)  #request the data
            data = json.loads(await response.text()) #json parse the data and make it available for use
            gif = random.randint(0, 9)
            if data['data'][gif]['username']:
                text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
            else:
                text = "Powered by GIPHY"
            embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
            embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
            await ctx.send(embed=embed) #send the embed
        except Exception as error:
            if isinstance(error, IndexError):
                embed = discord.Embed(color=0xde2f43, description=f':x: No results found for **{query}**.')
                await ctx.send(embed=embed)
        await session.close()   #close the session

    @commands.command(help="get a facepalm gif", usage="facepalm###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def facepalm(self, ctx):
        search = 'facepalm'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="get a shrug gif", usage="facepalm###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shrug(self, ctx):
        search = 'shrug'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="get a cry gif", usage="cry###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cry(self, ctx):
        search = 'cry'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="get a pout gif", usage="pout###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pout(self, ctx):
        search = 'pout'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="run", usage="run###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def run(self, ctx):
        search = 'run'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="get a tongue out gif", usage="tongue###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tongue(self, ctx):
        search = 'tongue out'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="hug someone", usage="hug @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        search = 'hug'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} hugged you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="kiss someone", usage="kiss @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kiss(self, ctx, user: discord.User):
        search = 'kiss'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} kissed you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="slap someone", usage="slap @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slap(self, ctx, user: discord.User):
        search = 'slap'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} slapped you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="wink at somebody", usage="wink @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wink(self, ctx, user: discord.User):
        search = 'wink'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} winked at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="stare at someone", usage="stare @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stare(self, ctx, user: discord.User):
        search = 'stare'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} is staring at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="lick someone", usage="lick @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def lick(self, ctx, user: discord.User):
        search = 'lick'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} licked you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="bite someone", usage="bite @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bite(self, ctx, user: discord.User):
        search = 'bite'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} bit you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="cuddle with someone", usage="cuddle @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.User):
        search = 'cuddle'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} is cuddling with you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="pat someone", usage="pat @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pat(self, ctx, user: discord.User):
        search = 'pat'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} patted you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="smile at someone", usage="smile @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def smile(self, ctx, user: discord.User):
        search = 'smile'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} is smiling at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="poke someone", usage="poke @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def poke(self, ctx, user: discord.User):
        search = 'finger poke'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} poked you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="tickle someone", usage="tickle @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tickle(self, ctx, user: discord.User):
        search = 'tickle'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} is tickling you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="point at someone", usage="point @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def point(self, ctx, user: discord.User):
        search = 'finger point'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} is pointing (at) you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command(help="punch someone", usage="punch @user###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def punch(self, ctx, user: discord.User):
        search = 'punch'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=20'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{user.mention}, {ctx.message.author.mention} punched you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 19)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • GIF by {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Actions(bot))