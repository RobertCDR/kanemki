import discord
from discord.ext import commands
import random
import asyncio
import typing

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['frick'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def fuck(self, ctx, partner : discord.Member):
        if partner is ctx.message.author:
            return await ctx.send(r'have fun fucking yourself I guess ¯\_(ツ)_/¯')
        responses = ["{} and {} are making some wild sex", "{} are 2 night lovers {}", "{} and {} have a rough round"]
        choice = random.choice(responses)
        choice = choice.format(ctx.message.author.mention, partner.mention)
        await ctx.send(choice)

    #opens a file and selects a random thing from it
    #same principle applies for the following commands
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pun(self, ctx):
        pun = random.choice(list(open('./text files/puns.txt', encoding='utf8')))   #opens the text file, converts the content into a list and picks a random line from it
        await ctx.send(pun) #send the pun (yes, I manually selected them and actually laughed, help)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def sex(self, ctx):
        response = random.choice(list(open('./text files/sex.txt', encoding='utf8')))
        await ctx.send(f'{ctx.message.author.mention} {response}')

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roast(self, ctx):
        roast = random.choice(list(open('./text files/roast.txt', encoding='utf8')))
        await ctx.send(roast)

    @commands.command(aliases=['fortunecookie', 'fortune'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def fookie(self, ctx):
        fortune = random.choice(list(open('./text files/fookies.txt', encoding='utf8')))
        embed = discord.Embed(color=random.randint(0, 0xffffff), description=f':fortune_cookie: {fortune}', title=str(ctx.message.author))
        await ctx.send(embed=embed)

    #had some fun doing this command
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def hack(self, ctx, victim : discord.Member):
        if victim is ctx.message.author:    #if you mention yourself
            return await ctx.send('why would you hack yourself?')   #return this
        search = random.choice(list(open('./text files/searches.txt'))) #select a random thing from a file with funny and weird google searches
        percent = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100% - Hacking complete']
        #some random bullshit that passed through my head or seen it on Dank Memer
        action = [
            f'Injecting trojan into ID: {victim.id}',
            f'Getting access key from discriminator: {str(victim)[-5:]}',
            f'Tracing IP address: {random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}',
            'Exploiting vulnerabilities...',
            f"Latest incognito search: {search}",
            'Passwords acquired. Accessing accounts...',
            'Bypassing security: 2FA, security questions, reCAPTCHA...',
            'Extracting data...',
            'Selling data on Deep Web...',
            'Hack traces erased :)',
        ]
        counters = ['stop', 'counter', 'counterhack', 'report']
        #it was such a bummer to try different characters so I sticked to this
        animation = ["███ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯","███ ███ ▯ ▯ ▯ ▯ ▯ ▯ ▯ ▯", "███ ███ ███ ▯ ▯ ▯ ▯ ▯ ▯ ▯", "███ ███ ███ ███ ▯ ▯ ▯ ▯ ▯ ▯", "███ ███ ███ ███ ███ ▯ ▯ ▯ ▯ ▯", "███ ███ ███ ███ ███ ███ ▯ ▯ ▯ ▯", "███ ███ ███ ███ ███ ███ ███ ▯ ▯ ▯", "███ ███ ███ ███ ███ ███ ███ ███ ▯ ▯", "███ ███ ███ ███ ███ ███ ███ ███ ███ ▯", "███ ███ ███ ███ ███ ███ ███ ███ ███ ███"]
        message = await ctx.send('**Loading...**') #send the first the message
        def check(x):
            return x.author is victim and x.channel is ctx.message.channel
        for i in range(len(animation)): #create a for loop to go through the lists and edit the message
            try:
                counter = await self.bot.wait_for('message', check=check, timeout=3)
                if counter.content.lower() in counters:
                    await ctx.send(f"**Counter Hack Successfull. Bounty placed on** {ctx.message.author.mention}**'s head on Deep Web.**")
                    return
            except asyncio.TimeoutError:
                await asyncio.sleep(random.randint(1.0, 3.0))   #wait after every edit starting with the first message
                await message.edit(content=f'```diff\n-{action[i]}\n``` ```fix\nStatus: {percent[i]}\n{animation[i]}\n```') #edit the message
        await ctx.send(f'**Successfully hacked** {victim.mention}**.**')  #confirmation that the hacking was done as if the big "100% - hacking complete" was not enough

    @commands.command(aliases=['pula', 'penis', 'ppsize'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pp(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.message.author
        nr = random.randint(0,30)
        if nr == 0:
            embed = discord.Embed(color=random.randint(0,0xffffff), description=f"{member.mention}'s pula is {nr} centimeters long")
            embed.set_author(name='pspspspsps come here little pussy', icon_url='{}'.format(member.avatar_url))
            await ctx.send(embed=embed)
        elif nr >= 20:
            if nr == 30:
                embed = discord.Embed(color=random.randint(0,0xffffff), description=f"{member.mention}'s pula is {nr} centimeters long")
                embed.set_author(name='Hail Johnny Sins v2.0', icon_url='{}'.format(member.avatar_url))
                await ctx.send(embed=embed)
                return
            embed = discord.Embed(color=random.randint(0,0xffffff), description=f"{member.mention}'s pula is {nr} centimeters long")
            embed.set_author(name='congrats for having a big pp, sir', icon_url='{}'.format(member.avatar_url))
            await ctx.send(embed=embed)
        elif nr < 20:
            if nr < 15:
                embed = discord.Embed(color=random.randint(0,0xffffff), description=f"{member.mention}'s pula is {nr} centimeters long")
                embed.set_author(name='at least you can use it as a spare finger', icon_url='{}'.format(member.avatar_url))
                await ctx.send(embed=embed)
                return
            embed = discord.Embed(color=random.randint(0,0xffffff), description=f"{member.mention}'s pula is {nr} centimeters long")
            embed.set_author(name='not the best, not the worst', icon_url='{}'.format(member.avatar_url))
            await ctx.send(embed=embed)
                    
    @commands.command(aliases=['8ball'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ask(self, ctx, *, question : str):
        response = random.choice(list(open('./text files/8ball.txt')))
        await ctx.send(f'{ctx.message.author.mention} {response}')

    @commands.command(aliases=['howgay', 'gay', 'gayr8'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def gayrate(self, ctx, member : discord.Member=None):
        if not member:
            member = ctx.message.author
        nr = random.randint(0, 100)
        if nr >= 50:
            embed = discord.Embed(color=random.randint(0,0xffffff), title=str(member), description='homo alert bois\n protect your buttholes')
            embed.add_field(name=':rainbow_flag:', value=f'you are {nr}% gay')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=random.randint(0,0xffffff), title=str(member), description='you passed the nongay check :point_right::ok_hand:')
            embed.add_field(name=':rainbow_flag:', value=f'you are {nr}% gay')
            await ctx.send(embed=embed)

    @commands.command(aliases=['howhot', 'hotr8'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def hotrate(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.message.author
        nr = random.randint(-100, 100)
        embed = discord.Embed(color=random.randint(0, 0xffffff), title=str(member))
        if nr >= 50:
            embed.description = "someone's looking good"
            embed.add_field(name=':smirk:', value=f"you're {nr}% hot")
        elif nr > 0 and nr < 50:
            embed.description = "a kinda good amount of hot"
            embed.add_field(name=':wink:', value=f"you're {nr}% hot")
        else:
            embed.description = "well, at least you can qualify as a human being"
            embed.add_field(name=':grimacing:', value=f"you're {nr}% hot")
        await ctx.send(embed=embed)

    @commands.command(aliases=['love', 'compatibility', 'lovemeter'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ship(self, ctx, pair: discord.Member, pair2: typing.Optional[discord.Member]=None):
        if (pair is ctx.message.author and pair2 is None) or (pair is ctx.message.author and pair2 is ctx.message.author):
            result = '❣ Love and be yourself with all your goods and bads ❣'
            i = 100
            string = '```'
            while i > 2:
                string += '​█'
                i -= 2
            string += '```'
            embed = discord.Embed(color=random.randint(0,0xffffff), title=f'**{str(ctx.message.author)}** :heart_exclamation: **{str(pair)}**', description=f'You are perfect.\n{string}')
            embed.set_author(icon_url=self.bot.user.avatar_url, name='Love Machine')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/738787852472549446/hearts.png')
            embed.add_field(name='Result', value=f'{result}')
            return await ctx.send(embed=embed)
        if pair2 is None:
            pair2 = ctx.message.author
        nr = random.randint(0, 100)
        string = '```'
        i = nr
        x = 100 - nr
        while i > 2:
            string += '​█'
            i -= 2
        while x > -2:
            string += ' '
            x -= 1
        string += '```'
        if nr == 0:
            result = 'Welp, this is so sad... :pensive:'
        elif nr <= 44 and nr >= 1:
            result = "Guess it's not meant to be... :cry:"
        elif nr <= 64 and nr >=45:
            shrug = r'¯\_(ツ)_/¯'
            result = f"It's worth a shot I guess {shrug}"
        elif nr <= 79 and nr >= 65:
            result = 'These are some pretty good chances :smirk:'
        elif nr <= 89 and nr >= 80:
            result = "You'd make a pretty good pair :hushed:"
        elif nr <= 99 and nr >= 90:
            result = "It's like you were almost meant for each other :smiling_face_with_3_hearts:"
        else:
            result = ':heartpulse: You 2 are the perfect couple! :heartpulse:'
        embed = discord.Embed(color=random.randint(0,0xffffff), title=f'**{str(pair)}** :heart_exclamation: **{str(pair2)}**', description=f'You are {nr}% compatible.\n{string}')
        embed.set_author(icon_url=self.bot.user.avatar_url, name='Love Machine')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/738787852472549446/hearts.png')
        embed.add_field(name='Result', value=f'{result}')
        await ctx.send(embed=embed)

    #the classic say command
    #utils.escape_mentions is broken
    @commands.command(aliases=['parrot', 'mimic', 'repeat'])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def say(self, ctx, *, mimic):
        await ctx.message.delete()  #first, delete the message sent by the command author
        mimic = discord.utils.escape_mentions(mimic)    #prevents mentions (noboby wants to be pinged by a stupid everyone)
        await ctx.send(mimic)   #send the message

    #a variation of the say command
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clapify(self, ctx, *, text):
        message = ''    #initiate a variable as an empty string
        for x in text[-len(text):-1]:   #loop through the characters between the first and the last one
            message += f'**{x}**'   #bold every character
            message += " :clap: "   #add the clap emote between characters
        message += f'**{text[-1]}**'    #add the last character to the string
        await ctx.send(message) #send the message

    #another variation of the say command, but this one adds spoiler tags for each character
    #yes, I'm evil, but the decision to use this command is yours
    #like the forbidden apple
    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def spoilify(self, ctx, *, text):
        await ctx.message.delete()
        message = f'**{ctx.message.author}** - '
        for x in text:
            message += f'||{x}||'
        await ctx.send(message)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def emojify(self, ctx, *, text):
        message = ''
        numbers = {
            '0': ':zero:', '1': ':one:', '2': ':two:', '3': ':three:', '4': ':four:', '5': ':five:', '6': ':six:', '7': ':seven:', '8': ':eight:', '9': ':nine:'
        }
        for x in text:
            if x.isalpha():
                message += f':regional_indicator_{x.lower()}:'
            elif x.isdigit():
                message += numbers[x]
            elif x == ' ':
                message += '     '
            else:
                message += x
        await ctx.send(message)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def lewdify(self, ctx, *, text):
        text = text.split(' ')
        message = ''
        emojis = [':weary:', ':pleading_face:', ':flushed:', ':hot_face:', ':drooling_face:', ':point_right: :ok_hand:', ':sweat_drops:', ':eggplant:', ':peach:']
        for x in range (0, len(text)):
            message += text[x]
            message += f" {random.choice(emojis)} "
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Fun(bot))