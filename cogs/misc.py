import discord
from discord.ext import commands
import random
import datetime
import wolframalpha
import typing
import string
from bot import wolfram_key
from cogs.errors import CustomChecks

wolfram = wolframalpha.Client(wolfram_key)

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Misc"

    #embed sandbox
    #maybe I will further develop it someday
    @commands.command(aliases=['emb'], help="create a custom embed",
        usage="embed <title>(t) <description>(descr, d) <author> <footer> <thumbnail>(thumb, tn) <image>(img, i) <time>\n\n*thumbnail and image parameters require links, the others are only text*###1s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def embed(self, ctx, *, args: str=None):
        if not args:    #if there are no parameters given, return
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify at least one parameter for the embed.')
            return await ctx.send(embed=embed)
        embed = discord.Embed(color=random.randint(0, 0xffffff))    #create the embed with only the color field
        args = list(args.split(', '))   #create a list containing the parameters and the content of each one
        for i in range(0, len(args)):   #create a for loop to iterate over the elements
            x = list(args[i].split('=', 1)) #create another another list from each element
            if x[0] == 'title' or x[0] == 't':
                embed.title = x[1]
            if x[0] == 'description' or x[0] == 'descr' or x[0] == 'd':
                embed.description = x[1]
            if x[0] == 'author':
                embed.set_author(name=x[1])
            if x[0] == 'footer':
                embed.set_footer(text=x[1])
            if x[0] == 'thumbnail' or x[0] == 'tn' or x[0] == 'thumb':
                embed.set_thumbnail(url=x[1])
            if x[0] == 'image' or x[0] == 'img' or x[0] == 'i':
                embed.set_image(url=x[1])
            if x[0] == 'time':
                embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed) #send the embed

    #this will transform text into Morse code according to the International Morse Code
    @commands.command(aliases=['tomorse'], help="translate text into Morse code", usage="textomorse <text>###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def texttomorse(self, ctx, *, text):
        #this is the dictionary with letters and their Morse code equivalent
        text_to_morse = {
            "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
            "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
            "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
            "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.", "0": "-----"
        }
        #this is the reversed dictionary
        text = text.upper() #uppercase the string
        message = ''    #and then create another string that will contain the translated message
        for x in text:  #iterate through the string and add the converted value to the new message
            if x.isdigit():
                message += f'{text_to_morse[x]} '
            elif x.isalpha():
                message += f'{text_to_morse[x]} '
            elif x == ' ':
                message += ' / '
            else:   #except symbols and other things that cannot be converted
                message += f'{x} '
        await ctx.send(message)

    #this is the viceversa of the previous command
    @commands.command(aliases=['totext'], help="translate Morse code into text", usage="morsetotext <morse_code>###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def morsetotext(self, ctx, *, text):
        morse_to_text = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
            '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
            '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z',
            '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0'
        }
        text = text.split(' ')
        message = ''
        for x in text:
            if x in morse_to_text.keys():
                message += morse_to_text[x]
            elif x == '/':
                message += ' '
            else:
                message += x
        await ctx.send(message)

    @commands.command(aliases=['age', 'howmanydays'], help="calculate your age in days", usage="agedays `dd`/`mm`/`yyyy`###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def agedays(self, ctx, *, birthday):
        date = birthday.split('/')  #the date should come in format dd/mm/yyyy so it can be split and formatted
        if int(date[0]) > 31:   #there's no month with 50 days
            return await ctx.send('Invalid date')
        elif int(date[1]) > 12: #and here on Earth the year has 12 months
            return await ctx.send('Invalid date')
        #if february has more than 28 days and the year is not divisible by 4 then it's not a bisect year and it's not a valid date
        #damn primary school was useful
        elif int(date[1]) == 2 and int(date[0]) > 28 and int(date[2])%4 != 0:
            return await ctx.send('Invalid date')
        #these are the conditions for every month with 30 days
        #damn kindergarten was useful with it's knuckle rule for months
        elif (int(date[1]) == 4 or int(date[1]) == 6 or int(date[1]) == 9 or int(date[1]) == 11) and int(date[0]) > 30:
            return await ctx.send('Invalid date')
        date = datetime.datetime.strptime(birthday, '%d/%m/%Y') #format the date
        #calculate the days
        now = datetime.datetime.utcnow()
        age = now - date
        age = str(age)
        days = list(age.split(',', 1))
        embed = discord.Embed(title=str(ctx.message.author), description=days[0], color=random.randint(0, 0xffffff))   #create the embed
        await ctx.send(embed=embed) #send the embed

    @commands.command(aliases=['lmgtfy'], help="for every person that's tired of someone's stupid questions or too lazy to switch tabs",
        usage="search <query>###1s/user###Depends on what you search"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def search(self, ctx, *, search):
        copy_search = search.replace(' ', '+')
        embed = discord.Embed(title=f"Here's your Google search for: {search}.", url=f'http://lmgtfy.com/?q={copy_search}', color=random.randint(0, 0xffffff), timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=self.bot.user.avatar_url, name='LMGTFY', url='https://lmgtfy.com/')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/751834441667706990/lmgtfy.png')
        embed.description = "[LMGTFY](https://lmgtfy.com/)\nFor all those people who find it more convenient to bother you with their question rather than search it for themselves."
        await ctx.send(embed=embed)

    #generate random passwords
    @commands.command(aliases=['passgen', 'password'], help="generate a random password for whatever use you want",
        usage="passwordgen <length>`[optional]` <purpose>`[optional]`"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def passwordgen(self, ctx, length: typing.Optional[int]=10, *, use: typing.Optional[str]=None):
        gen = random.SystemRandom() #random generator that uses sources provided by the OS
        characters = string.ascii_letters + string.digits + string.punctuation
        password = str().join(gen.choice(characters) for char in range(length)) #generate the password
        dm = await ctx.message.author.create_dm()
        embed = discord.Embed(color=0xff0000, title=use, description=password, timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=self.bot.user.avatar_url, name='Random Password Request')
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/763464041112272896/password.jpg')
        await dm.send(embed=embed)

    #pick a random thing
    @commands.command(help="let the bot pick between different things", usage="pick <items>###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def pick(self, ctx, *args):
        if args:
            await ctx.send(random.choice(args))
        else:
            await ctx.send('gimme some choices')

    #the wolframalpha api is very interesting
    #I will make some nice additions using it
    #the command below is far from ready
    @commands.command(aliases=["calculate"], hidden=True)
    @CustomChecks.blacklist_check()
    @commands.is_owner()
    async def wf(self, ctx, *, query: str):
        data = wolfram.query(query)
        for pod in data.pods:
            await ctx.send(f"{pod}\n\n")

def setup(bot):
    bot.add_cog(Misc(bot))
