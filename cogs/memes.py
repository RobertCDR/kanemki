import discord
from discord.ext import commands
import random
import praw
import aiohttp
from bot import reddit_client_id, reddit_client_secret
from cogs.errors import CustomChecks

#variable containing data for requests
#yes, I use praw and I hate it but don't know what else to do
#tried with aiohttp but it has the same delay of 2-3 seconds
reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent='windows:Kanemki Discord Bot:v1.1.0 (by /u/RobertCDR)')

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Memes & Stuff"

    #aiohttp tryout to get things from Reddit
    @commands.command(help="get memes from reddit", usage="meme###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meme(self, ctx):
        nr = random.randint(0, 99)  #position of a meme
        #the subreddits from where th bot cand get memes
        links = [
            'https://www.reddit.com/r/dankmemes/hot.json?sort=hot&t=week&limit=100',
            'https://www.reddit.com/r/memes/hot.json?sort=hot&t=week&limit=100',
            'https://www.reddit.com/r/funny/hot.json?sort=hot&t=week&limit=100'
        ]
        #private info
        headers = {
            'User-Agent': 'windows:Kanemki Discord Bot:v1.1.0 (by /u/RobertCDR)',
            'Client-Id': reddit_client_id,
            'Client-Secret': reddit_client_secret
        }
        #use an aiohttp session and request data using my private info and then json parse it
        async with aiohttp.ClientSession() as session:
            async with session.get(url=random.choice(links), headers=headers) as r:
                data = await r.json()
        #data from the random post
        post = data['data']['children'][nr]['data']
        subreddit = post['subreddit']
        title = post['title']
        image = post['url_overridden_by_dest']
        meme = discord.Embed(title=title, url=f"https://www.reddit.com{post['permalink']}", color=random.randint(0, 0xffffff)) #create the embed
        meme.set_image(url=image)   #the image is set to the meme
        meme.set_footer(text=f'r/{subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=meme)  #send the embed

    #yes, it may seem easier to use praw, but slow
    @commands.command(aliases=['wmeme', 'whlsm', 'wholesomeme'], help="get wholesome memes", usage="wholesome###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)  #the cooldown of the command
    async def wholesome(self, ctx):
        wholesomememes_submissions = reddit.subreddit('wholesomememes').hot()   #the iterator of the subreddit's hot section
        post = random.randint(1, 100)
        for x in range (0, post):   #goes through the submissions
            submission = next(x for x in wholesomememes_submissions if not x.stickied)
        meme = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff)) #create the embed
        meme.set_image(url=submission.url)  #set the image to the meme
        meme.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=meme)  #send the embed

    @commands.command(aliases=['14deep', 'deep', 'im14andthisisdeep'], help="I'm 14 and this is deep", usage="im14###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def im14(self, ctx):
        im14_submissions = reddit.subreddit('im14andthisisdeep').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in im14_submissions if not x.stickied)
        meme = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        meme.set_image(url=submission.url)
        meme.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=meme)

    @commands.command(help="see relatable memes", usage="meirl###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def meirl(self, ctx):
        meirl_submissions = reddit.subreddit('meirl').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in meirl_submissions if not x.stickied)
        meme = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        meme.set_image(url=submission.url)
        meme.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=meme)

    @commands.command(aliases=['insult', 'rareins', 'insultcom'], help="epic insults from internet people", usage="rareinsult###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rareinsult(self, ctx):
        rareinsults_submissions = reddit.subreddit('rareinsults').hot()
        kamikazebywords_submissions = reddit.subreddit('kamikazebywords').hot()
        list = [rareinsults_submissions, kamikazebywords_submissions]
        submissions = random.choice(list)
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in submissions if not x.stickied)
        comment = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        comment.set_image(url=submission.url)
        comment.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=comment)

    @commands.command(aliases=['ccom', 'cursedcom'], help="wonder what is gonna be left of humanity", usage="cursedcomment###3s/user###Only if you imagine it I guess (friendly advice, don't)")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cursedcomment(self, ctx):
        cursedcomments_submissions = reddit.subreddit('cursedcomments').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in cursedcomments_submissions if not x.stickied)
        comment = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        comment.set_image(url=submission.url)
        comment.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=comment)

    @commands.command(aliases=['holdup'], help="hold up memes", usage="holup###3s/user###Not really")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def holup(self, ctx):
        holup_submissions = reddit.subreddit('holup').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in holup_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_image(url=submission.url)
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

    @commands.command(help="see some blursed images (some cursed but not so cursed images)", usage="blursed###3s/user###Not so bad")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def blursed(self, ctx):
        blursed_submissions = reddit.subreddit('blursedimages').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in blursed_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_image(url=submission.url)
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

    @commands.command(help="see some cursed images", usage="cursed###3s/user###Not necessarily but with some exceptions")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cursed(self, ctx):
        cursed_submissions = reddit.subreddit('cursedimages').hot()
        post = random.randint(0, 100)
        for x in range (0, post):
            submission = next(x for x in cursed_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_image(url=submission.url)
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

    @commands.command(aliases=['50/50', 'fifty'], help="r/FiftyFifty - may God take care of you and erase the horrible things that you see from your memory",
        usage="fifty###3s/user###YES"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def fiftyfifty(self, ctx):
        fiftyfifty_submissions = reddit.subreddit('fiftyfifty').new()
        post = random.randint(0, 100)
        for x in range (0,post):
            submission = next(x for x in fiftyfifty_submissions if not x.stickied)
        link = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        link.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=link)

    @commands.command(aliases=['fax', 'fact'], help="get a random fact", usage="fact###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def facts(self, ctx):
        facts_submissions = reddit.subreddit('facts').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in facts_submissions if not x.stickied)
        fact = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        fact.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=fact)

    #get comics from xkcd.com
    #I don't understand most of them, but they seem funny to me anyway
    @commands.command(help="get comics from xkcd.com", usage="xkcd <comic_number>`[optional]`###3s/user###No")
    @CustomChecks.blacklist_check()
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
        async with aiohttp.ClientSession() as session:   #create a session using aiohttp
            async with session.get(url='https://xkcd.com/' + comic + '/info.0.json') as r:  #make a request to the json interface of that comic
                data = await r.json()    #json parse the requested data
        embed = discord.Embed(color=random.randint(0, 0xffffff), title=data['title'], url=data['img'])  #create the embed
        embed.set_image(url=data['img'])    #set the image to the comic
        embed.set_footer(text=f'xkcd.com  |  Comic #{comic}  |  {data["day"]}•{data["month"]}•{data["year"]}', icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed) #send the embed

def setup(bot):
    bot.add_cog(Memes(bot))
