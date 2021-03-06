import discord
from discord.ext import commands
import random
import datetime
import praw
from bot import reddit_client_id, reddit_client_secret
from cogs.errors import CustomChecks

reddit = praw.Reddit(client_id=reddit_client_id, client_secret=reddit_client_secret, user_agent='windows:Kanemki Discord Bot:v1.2.0 (by /u/RobertCDR)')

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Images"

    #get someone's profile pic or yours
    @commands.command(aliases=['avatar', 'av'], help="shows your avatar or someone else's", usage="pfp @user`[optional]`###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pfp(self, ctx, member: discord.User=None):
        if not member:  #if no one is mentioned then the bot will show the avatar of the command author
            member = ctx.message.author
        pfp = discord.Embed(description="[Avatar URL](%s)" % member.avatar_url, color=0xff0000, timestamp=datetime.datetime.utcnow())   #create the embed
        pfp.set_image(url=member.avatar_url)   #set the embed's image to the avatar
        pfp.set_thumbnail(url=member.default_avatar_url)    #and the thumbnail to the default avatar of the user as a nice addition
        pfp.set_footer(text=f'Requested by {str(ctx.author)}', icon_url=ctx.message.author.avatar_url)
        pfp.set_author(name=f'{member}', icon_url=member.avatar_url)
        await ctx.send(embed=pfp)   #send the embed

    #I made this command just because sometimes I want to get the cover art of a spotify track
    #I read in the docs that there is actually a way to get it and said "why not?"
    @commands.command(help="if you've found yourself in the situation of wanting to get the cover art of a Spotify track, this command can help you out (it literally does nothing more)",
        usage="spotify @user`[optional]`###1s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def spotify(self, ctx, member: discord.Member=None):
        if not member:  #if you want to get cover art from a track that you are listening
            member = ctx.message.author
        embed = discord.Embed(timestamp=datetime.datetime.utcnow()) #create the embed
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        if not member.activity: #if no activity is detected, return
            embed.color = 0xde2f43
            embed.description = ':x: No activity detected.'
            return await ctx.send(embed=embed)
        else:   #if the user has an activity
            for activity in member.activities:  #iterate through all the activities of a user
                if isinstance(activity, discord.Spotify):   #check if the activity is discord.Spotify
                    #assign the embed assets
                    embed.color = 0x1DB954
                    embed.title = activity.title
                    embed.url = f"https://open.spotify.com/track/{activity.track_id}"
                    embed.set_author(name='Spotify', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/753667014827966464/spotify.png')
                    embed.description = ', '.join(activity.artists)
                    embed.description = f'**by**: {embed.description}\n**on**: {activity.album}'
                    embed.set_image(url=activity.album_cover_url)
                    embed.set_thumbnail(url=member.avatar_url)
            if not embed.description:   #if no discord.Spotify activity is detected
                embed.color = 0xde2f43
                embed.description = ':x: No Spotify activity detected.'
        return await ctx.send(embed=embed)  #send the embed

    @commands.command(help="award someone for whatever reason it goes through your head", usage="award @user <reason>###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def award(self, ctx, awarded: discord.User, *, awreas : str):
        embed = discord.Embed(color=0xffec00, title='Award', description=f"Congrats {awarded.mention}! You've been awarded by {ctx.message.author.mention}: ***{awreas}***", timestamp=datetime.datetime.utcnow())
        embed.set_image(url='https://cdn.discordapp.com/attachments/725102631185547427/726574014037753886/190614-Award-nominations-iStock-1002281408.png')
        embed.set_author(name=awarded, icon_url=awarded.avatar_url)
        embed.set_footer(text=f'*Certified and approved by {str(ctx.message.author)}', icon_url=ctx.message.author.avatar_url)
        await ctx.channel.purge(limit=1)
        await ctx.send(embed=embed)

    #visualize any hex code
    #todo tried to make it work with rgb codes too but I got tired of doing it and moved on
    #I plan to do it someday, but today is not that day
    @commands.command(aliases=['colour'], help="visualize a hex color", usage="color <hex>###1s/user###No")
    @CustomChecks.blacklist_check()
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

    @commands.command(aliases=['aww', 'cute'], help="melts your heart", usage="eyebleach###3s/user###No")
    @CustomChecks.blacklist_check()
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

    @commands.command(aliases=['doggo', 'doggie', 'woof'], help="see some cute doggos", usage="dog###3s/user###No")
    @CustomChecks.blacklist_check()
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

    @commands.command(aliases=['kitty', 'meow', 'kat'], help="see some cute kitties", usage="cat###3s/user###No")
    @CustomChecks.blacklist_check()
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

    @commands.command(aliases=['bunny', 'bunbun', 'longears', 'bun'], help="brighten up your day by seeing some cute bun-buns",
        usage="rabbit###3s/user###No"
    )
    @CustomChecks.blacklist_check()
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

    @commands.command(help="see some bears", usage="bear###3s/user###No")
    @CustomChecks.blacklist_check()
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

    @commands.command(aliases=['nicepc', 'wowsetup'], help="see other people's setups", usage="battlestation###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def battlestation(self, ctx):
        battlestations_submissions =  reddit.subreddit('battlestations').hot()
        post = random.randint(1, 100)
        for x in range (0, post):
            submission = next(x for x in battlestations_submissions if not x.stickied)
        image = discord.Embed(title=submission.title, url=submission.url, color=random.randint(0, 0xffffff))
        image.set_footer(text=f'r/{submission.subreddit} | {str(ctx.message.author)}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/732974326671998986/reddit.png')
        await ctx.send(embed=image)

    @commands.command(help="see some nice flowers", usage="flower###3s/user###No")
    @CustomChecks.blacklist_check()
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