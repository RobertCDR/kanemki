import discord
from discord.ext import commands
import random
import datetime
import praw
import json
import aiohttp
from bot import reddit_client_id, reddit_client_secret

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent='windows:Kanemki Discord Bot:v2.0 (by /u/RobertCDR)')

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #get someone's profile pic or yours
    @commands.command(aliases=['avatar', 'av'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pfp(self, ctx, member: discord.Member=None):  
        if not member:  #if no one is mentioned then the bot will show the avatar of the command author
            member = ctx.message.author
        pfp = discord.Embed(description="[Avatar URL](%s)" % member.avatar_url, color=0xff0000, timestamp=datetime.datetime.utcnow())   #create the embed
        pfp.set_image(url="{}".format(member.avatar_url))   #set the embed's image to the avatar
        pfp.set_footer(text=f'Requested by {str(ctx.author)}', icon_url=ctx.message.author.avatar_url)
        pfp.set_author(name=f'{member}', icon_url=member.avatar_url)
        await ctx.send(embed=pfp)   #send the embed
    
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def award(self, ctx, awarded : discord.User, *, awreas : str):
        embed = discord.Embed(color=0xffec00, title='Award', description=f'Congrats {awarded.mention}! You`ve been awarded by {ctx.message.author.mention}: ***{awreas}***', timestamp=datetime.datetime.utcnow())
        embed.set_image(url='https://cdn.discordapp.com/attachments/725102631185547427/726574014037753886/190614-Award-nominations-iStock-1002281408.png')
        embed.set_author(name=awarded, icon_url=awarded.avatar_url)
        embed.set_footer(text=f'*Certified and approved by {str(ctx.message.author)}', icon_url=ctx.message.author.avatar_url)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

    #get comics from xkcd.com
    #I don't understand most of them, but they seem funny to me anyway 
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)  #cooldown: 1 use once every 3 seconds / user
    async def xkcd(self, ctx, comic: str=None):
        #the first request below is for keeping the comics up to date
        #I don't want to check the site daily to see the latest comic number
        session = aiohttp.ClientSession()
        response = await session.get(url='https://xkcd.com/info.0.json')
        data = await response.json()
        await session.close()
        if not comic:   #if no comic number is specified
            comic = str(random.randint(1, int(data['num'])))    #then it will be a random one between the first and the latest
        session = aiohttp.ClientSession()   #create a session using aiohttp
        response = await session.get(url='https://xkcd.com/' + comic + '/info.0.json')  #make a request to the json interface of that comic
        data = await response.json()    #json parse the requested data
        await session.close()   #close the session
        embed = discord.Embed(color=random.randint(0, 0xffffff), title=data['title'], url=data['img'])  #create the embed
        embed.set_image(url=data['img'])    #set the image to the comic
        embed.set_footer(text=f'xkcd.com  |  Comic #{comic}  |  {data["day"]}•{data["month"]}•{data["year"]}', icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed) #send the embed

    #visualize any hex code
    #tried to make it work with rgb codes too but I got tired of doing it and moved on
    #I plan to do it someday, but today is not that day
    @commands.command(aliases=['colour'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def color(self, ctx, *, color):
        color = str(color).replace('#', '') #remove the # if it's given along with the code
        #a character list to check if the code is valid
        charlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F']
        if len(color) == 6: #hex codes are made of 6 characters
            for x in color: #loop through the hex characters
                if x not in charlist:   #if one character is not in the list above it means that the hex is not valid
                    embed = discord.Embed(color=0xde2f43, description=':x: Not a valid Hex.')
                    return await ctx.send(embed=embed)
        else:   #if the hex is not made of 6 characters it's not valid
            embed = discord.Embed(color=0xde2f43, description=':x: Not a valid Hex.')
            return await ctx.send(embed=embed)
        #the site gives you the option to put some text on the requested color so I did this
        author = str(ctx.message.author).replace(' ', '+')  #there will be some problems with like 4 or so characters, but it's not that bad
        url = 'https://dummyimage.com/500x500/' + color + f'&text={author}.png' #create the url of the color image
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0x36393f) #create the embed
        embed.set_author(name='Color Visualizer', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='**Hex**', value=f'#{color}')
        #get the first 2, middle 2 and last 2 characters of the hex code and convert them to rgb
        r, g, b = color[:2], color[2:4], color[4:]
        r, g, b = int(r, 16), int(g, 16), int(b, 16)
        embed.add_field(name='**RGB**', value=f'{r}, {g}, {b}')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=str(ctx.message.author))
        embed.set_thumbnail(url=url)    #this is the image set to be the thumbnail
        await ctx.send(embed=embed) #send the embed

    @commands.command(aliases=['nasapc', 'rocketpc', 'wowsetup'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def battlestation(self, ctx):
        battlestations_submissions =  reddit.subreddit('battlestations').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in battlestations_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def flower(self, ctx):
        flowers_submissions = reddit.subreddit('flowers').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in flowers_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_image(url=submission.url)
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

def setup(bot):
    bot.add_cog(Images(bot))