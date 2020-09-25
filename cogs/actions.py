import discord
from discord.ext import commands
import json
import aiohttp
import random
import datetime
from bot import giphy_api_key

class Actions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #search a gif from giphy
    #the other commands are almost the same, except the search variable already has a value
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def gif(self, ctx, *, search):
        search = search.replace(' ', '+')   #replace the spaces with plus signs otherwise the request link will be broken
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=10'
        session = aiohttp.ClientSession()   #create a session using aiohttp
        embed = discord.Embed(color=random.randint(0, 0xffffff))  #create the embed
        response = await session.get(url=url)  #request the data
        data = json.loads(await response.text()) #json parse the data and make it available for use
        gif = random.randint(0, 9)
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()   #close the session
        await ctx.send(embed=embed) #send the embed

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def facepalm(self, ctx):
        search = 'facepalm'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shrug(self, ctx):
        search = 'shrug'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cry(self, ctx):
        search = 'cry'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pout(self, ctx):
        search = 'pout'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def run(self, ctx):
        search = 'run'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tongue(self, ctx):
        search = 'tongue out'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hug(self, ctx, member : discord.Member):
        search = 'hug'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} hugged you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kiss(self, ctx, member : discord.Member):
        search = 'kiss'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} kissed you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def slap(self, ctx, member : discord.Member):
        search = 'slap'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} slapped you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def wink(self, ctx, member : discord.Member):
        search = 'wink'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} winked at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stare(self, ctx, member : discord.Member):
        search = 'stare'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} is staring at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def lick(self, ctx, member : discord.Member):
        search = 'lick'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} licked you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bite(self, ctx, member : discord.Member):
        search = 'bite'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} bit you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cuddle(self, ctx, member : discord.Member):
        search = 'cuddle'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} is cuddling with you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pat(self, ctx, member : discord.Member):
        search = 'pat'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} patted you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def smile(self, ctx, member : discord.Member):
        search = 'smile'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} is smiling at you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def poke(self, ctx, member : discord.Member):
        search = 'finger poke'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} poked you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def tickle(self, ctx, member : discord.Member):
        search = 'tickle'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} is tickling you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def point(self, ctx, member : discord.Member):
        search = 'finger point'
        search.replace(' ', '+')
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} is pointing (at) you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def punch(self, ctx, member : discord.Member):
        search = 'punch'
        url = f'http://api.giphy.com/v1/gifs/search?q={search}&api_key={giphy_api_key}&limit=50'
        session = aiohttp.ClientSession()
        embed = discord.Embed(description=f'{member.mention}, {ctx.message.author.mention} punched you', color=random.randint(0, 0xffffff))
        response = await session.get(url=url)
        data = json.loads(await response.text())
        gif = random.randint(0, 49)
        embed.set_image(url=data['data'][gif]['images']['original']['url'])
        if data['data'][gif]['username']:
            text = f"Powered by GIPHY • {data['data'][gif]['username']}"
        else:
            text = "Powered by GIPHY"
        embed.set_image(url=data['data'][gif]['images']['original']['url']) #the embed's image will bet set to a random gif
        embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/725102631185547427/735969171984351292/giphy.png', text=text)
        await session.close()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Actions(bot))