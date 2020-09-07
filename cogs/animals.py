import discord
from discord.ext import commands
import random
import praw

reddit = praw.Reddit(client_id='YAD0cRFQ2mnFpQ', client_secret='3yotbah1AEJ6gfbwPDQoSkkkyDY', user_agent='windows:Kanemki Discord Bot:v1.0 (by /u/RobertCDR)')

class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['aww', 'cute'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def eyebleach(self, ctx):
        eyebleach_submissions = reddit.subreddit('eyebleach').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in eyebleach_submissions if not x.stickied)
        if submission.is_video:
            await ctx.send(submission.url)
        else:
            image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
            image.set_image(url=submission.url)
            image.set_footer(text=f'from r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
            await ctx.send(embed=image)

    @commands.command(aliases=['doggo', 'doggie', 'woof'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def dog(self, ctx):
        dogpictures_submissions =  reddit.subreddit('dogpictures').hot()
        dogswithjobs_submissions = reddit.subreddit('dogswithjobs').hot()
        lookatmydog_submissions = reddit.subreddit('lookatmydog').hot()
        corgi_submissions = reddit.subreddit('corgi').hot()
        goldenretrievers_submissions = reddit.subreddit('goldenretrievers').hot()
        list = [dogpictures_submissions, dogswithjobs_submissions, lookatmydog_submissions, corgi_submissions, goldenretrievers_submissions]
        submissions = random.choice(list)
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in submissions if not x.stickied)
        if submission.is_video:
            await ctx.send(submission.url)
        else:
            image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
            image.set_image(url=submission.url)
            image.set_footer(text=f'from r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
            await ctx.send(embed=image)

    @commands.command(aliases=['kitty', 'meow', 'kat'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def cat(self, ctx):
        cats_submissions = reddit.subreddit('cats').hot()
        catbellies_submissions =  reddit.subreddit('catbellies').hot()
        supermodelcats_submissions = reddit.subreddit('supermodelcats').hot()
        catloaf_submissions = reddit.subreddit('catloaf').hot()
        stuffoncats_submissions = reddit.subreddit('stuffoncats').hot()
        catpictures_submissions = reddit.subreddit('catpictures').hot()
        catsinsinks_submissions = reddit.subreddit('catsinsinks').hot()
        cat_submissions = reddit.subreddit('cat').hot()
        list = [cat_submissions, cats_submissions, catbellies_submissions, supermodelcats_submissions, catloaf_submissions, stuffoncats_submissions, catpictures_submissions, catsinsinks_submissions]
        submissions = random.choice(list)
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in submissions if not x.stickied)
        if submission.is_video:
            await ctx.send(submission.url)
        else:
            image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
            image.set_image(url=submission.url)
            image.set_footer(text=f'from r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
            await ctx.send(embed=image)

    @commands.command(aliases=['bunny', 'bunbun', 'longears', 'bun'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rabbit(self, ctx):
        rabbits_submissions =  reddit.subreddit('rabbits').hot()
        bunnieswithhats_submissions = reddit.subreddit('bunnieswithhats').hot()
        buncomfortable_submissions = reddit.subreddit('buncomfortable').hot()
        hairybuns_submissions = reddit.subreddit('hairybuns').hot()
        list = [rabbits_submissions, bunnieswithhats_submissions, buncomfortable_submissions, hairybuns_submissions]
        submissions = random.choice(list)
        post = random.randint(1, 100)
        for x in range (0, post):
            submission =  next(x for x in submissions if not x.stickied)
        if submission.is_video:
            await ctx.send(submission.url)
        else:
            image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
            image.set_image(url=submission.url)
            image.set_footer(text=f'from r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
            await ctx.send(embed=image)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bear(self, ctx):
        bears_submissions =  reddit.subreddit('bears').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in bears_submissions if not x.stickied)
        if submission.is_video:
            await ctx.send(submission.url)
        else:
            image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
            image.set_image(url=submission.url)
            image.set_footer(text=f'from r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
            await ctx.send(embed=image)

def setup(bot):
    bot.add_cog(Animals(bot))