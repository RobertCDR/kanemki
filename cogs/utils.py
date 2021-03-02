import discord
from discord.ext import commands
import random
import discord.utils
import datetime
import aiohttp
import json
from dpymenus import PaginatedMenu
from bot import rapid_api
from cogs.errors import CustomChecks

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Utilities"

    @commands.command(help="get an invite link for the bot", usage="invite###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def invite(self, ctx):
        #create the embed containing the link with the bot scope and administrator (integer 8) permissions
        embed = discord.Embed(color=random.randint(0, 0xffffff), title='Bot invite link', url=f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot', timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=self.bot.user.avatar_url, name='Thanks for thinking about inviting me <3')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
        await ctx.send(embed=embed) #send the embed

    @commands.command(help="Displays the bot latency.", aliases=["latency"], usage="ping###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def ping(self, ctx):
        ping = round(self.bot.latency*1000)
        embed = discord.Embed(color=0xde2f43, description=f'pong! {ping}ms')
        if ping <= 250:
            embed.color = 0x75b254
        elif ping > 250 and ping <= 500:
            embed.color = 0xfccc51
        else:
            embed.color = 0xde2f43
        await ctx.send(embed=embed)

    #get info about yourself or someone else on a discord server
    @commands.command(aliases=['uinfo', 'about', 'whois'], help="get info about yourself or someone else",
        usage="userinfo @user`[optional]`###2s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def userinfo(self, ctx, member : discord.Member=None):
        if not member:  #if nobody is mentioned
            member = ctx.message.author #the member is set to the command author
        embed = discord.Embed(color=0xff0000, timestamp=datetime.datetime.utcnow(), description=member.mention) #create the embed
        #check the user's hypesquad house
        if member.public_flags.hypesquad_balance:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659063759667280/balance.png')
        elif member.public_flags.hypesquad_bravery:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659066246365184/bravery.png')
        elif member.public_flags.hypesquad_brilliance:
            embed.set_author(name=f'{member}', icon_url='https://cdn.discordapp.com/attachments/725102631185547427/769659069224189962/brilliance.png')
        else:
            embed.set_author(name=f'{member}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        #check what status does the user have
        if member.status is discord.Status.online:
            embed.add_field(name='**Status**', value=f'```css\n+{member.status}\n```', inline=True)
        elif member.status is discord.Status.dnd:
            embed.add_field(name='**Status**', value=f'```diff\n-{member.status}\n```', inline=True)
        elif member.status is discord.Status.idle:
            embed.add_field(name='**Status**', value=f'```fix\n{member.status}\n```', inline=True)
        elif member.status is discord.Status.offline:
            embed.add_field(name='**Status**', value=f'```css\n.{member.status}\n```', inline=True)
        if member.activity == None: #if the member does not have an activity
            activity = 'None'   #the default value is set to none
        else:   #otherwise, if the member has an activity
            activity = member.activity.name #the value is set to that activity's name
        reg = member.created_at.__format__('%a, %d %b %Y %H:%M')    #when the account was created
        join = member.joined_at.__format__('%a, %d %b %Y %H:%M')    #when the user joined the server
        embed.add_field(name='**Activity**', value=f'```bash\n"{activity}"\n```', inline=True)
        embed.add_field(name='**Nickname**', value=f'```css\n[{member.nick}]\n```', inline=True)
        embed.add_field(name='**ID**', value=f'```diff\n-{member.id}\n```', inline=True)
        #calculate the age of the account in days
        then = member.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        days = str(age).split(',', 1)
        embed.add_field(name='**Registered**', value=f'```ini\n[{reg} ({days[0]})]\n```', inline=True)
        then = member.joined_at
        age = now - then
        days = str(age).split(',', 1)
        embed.add_field(name='**Joined**', value=f'```ini\n[{join} ({days[0]})]\n```', inline=False)
        #get a list of all the guild roles the user has from top to bottom
        allroles = list(map(lambda x: x.mention, member.roles[::-1]))
        allroles = allroles[:-1]    #except the default role @everyone
        allroles = ' '.join(allroles)
        if allroles:
            embed.add_field(name=f'**Roles** ({len(member.roles)-1})', value=allroles, inline=False)
        else:
            embed.add_field(name='**Roles** (0)', value='```css\n[None]\n```', inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'aboutsrv'], help="get info about the server", usage="serverinfo###2s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=ctx.guild.icon_url, name=f'{ctx.guild} Server Info')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        embed.add_field(name='**Owner**', value=f'```fix\n{ctx.guild.owner}\n```')
        embed.add_field(name='**Region**', value=f'```ini\n[{ctx.guild.region}]\n```', inline=True)
        created = ctx.guild.created_at.__format__('%A, %d %B %Y %H:%M') #when the guild was created
        #the guild's age in days
        then = ctx.guild.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        age = str(age)
        days = list(age.split(',', 1))
        embed.add_field(name='**Created**', value=f'```ini\n[{created} ({days[0]})]\n```', inline=True)
        embed.add_field(name='**ID**', value=f'```diff\n-{ctx.guild.id} (guild)  -{ctx.guild.owner.id} (owner)\n```', inline=False)
        embed.add_field(name='**Text Channels**', value=f'```fix\n{len(ctx.guild.text_channels)}\n```', inline=True)
        embed.add_field(name='**Voice Channels**', value=f'```fix\n{len(ctx.guild.voice_channels)}\n```', inline=True)
        embed.add_field(name='**Emotes**', value=f'```fix\n{len(ctx.guild.emojis)}\n```')
        bots = sum(member.bot for member in ctx.guild.members) #count the bots in the guild
        #count how many users are on/dnd/idle/off in the guild
        online = sum(member.status == discord.Status.online and not member.bot for member in ctx.guild.members)
        dnd = sum(member.status == discord.Status.dnd and not member.bot for member in ctx.guild.members)
        idle = sum(member.status == discord.Status.idle and not member.bot for member in ctx.guild.members)
        off = sum(member.status == discord.Status.offline and not member.bot for member in ctx.guild.members)
        embed.add_field(name='**Members**', value=f'```diff\n-{ctx.guild.member_count} ({bots} bots)\n-on: {online} | dnd: {dnd} | idle: {idle} | off: {off}\n```')
        #get a list of all the guild roles from top to bottom
        allroles = list(map(lambda x: x.mention, ctx.guild.roles[::-1]))
        allroles = allroles[:-1]
        allroles = ' '.join(allroles)
        embed.add_field(name=f'**Roles** ({len(ctx.guild.roles)-1})', value=allroles, inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['rinfo'], help="get info about a role", usage="roleinfo @role###2s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def roleinfo(self, ctx, role : discord.Role):
        embed = discord.Embed(description=role.mention, color=0xff0000, timestamp=datetime.datetime.utcnow())   #create the embed
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f'Role Info {role}', icon_url=self.bot.user.avatar_url)
        embed.add_field(name='**ID**', value=f'```diff\n-{role.id}\n```')
        created = role.created_at.__format__('%A, %d %B %Y %H:%M')  #when the role was created
        embed.add_field(name='**Color**', value=f'```fix\n{role.color}\n```')
        embed.add_field(name='**Mentionable**', value=f'```diff\n-{role.mentionable}\n```')
        #calculate the age of the role in days
        then = role.created_at
        now = datetime.datetime.utcnow()
        age = now - then
        age = str(age)
        days = list(age.split(',', 1))
        embed.add_field(name='**Created**', value=f'```ini\n[{created} ({days[0]})]\n```')
        embed.add_field(name='**Members**', value=f'```fix\n{len(role.members)}\n```')
        if role.hoist is False:
            embed.add_field(name='**Hoisted**', value=f'```css\n[{role.hoist}]\n```')
        else:
            embed.add_field(name='**Hoisted**', value=f'```ini\n[{role.hoist}]\n```')
        await ctx.send(embed=embed)

    @commands.command(aliases=['perms', 'userperms'], help="see a user's guild permissions",
        usage="permissions @user`[optional]`###2s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def permissions(self, ctx, member : discord.Member=None):
        if not member:  #if nobody is mentioned
            member = ctx.message.author #the member becomes the command author
        #create a string of permissions of the user and capitalize them
        perms = ', '.join(perm.capitalize() for perm, value in member.guild_permissions if value)
        #replace the underscores with spaces in the string
        perms = perms.replace('_', ' ')
        #create the embed
        embed = discord.Embed(description=f'{member.mention}\n```ini\n[{perms}]\n```', color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=member.avatar_url, name=f'Guild Permissions {member}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        await ctx.send(embed=embed) #send the embed

    @commands.command(aliases=['rperms', 'roleperms'])
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def rpermissions(self, ctx, *, role : discord.Role):
        #create a string of permissions of the role and capitalize them
        perms = ', '.join(perm.capitalize() for perm, value in role.permissions if value)
        perms = perms.replace('_', ' ') #replace the underscores with spaces
        #create the embed
        embed = discord.Embed(description=f'{role.mention}\n```css\n[{perms}]\n```', color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(icon_url=ctx.guild.icon_url, name=f"Role Permissions {role}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
        await ctx.send(embed=embed) #send the embed

    #search a word on urban dictionary and return an embed menu containing 5 definitions
    #todo rework needed
    @commands.command(aliases=['urbandict', 'urbandic', 'urbdic', 'urbdict'], help="get word definitions from urban dictionary",
        usage="urban <word>###5s/user###Depends on what you search"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user) #cooldown 10s/user
    async def urban(self, ctx, *, search):
        search.replace(' ', '+')    #replace the spaces with plus signs so the link won't be broken
        querystring = {"term":f"{search}"}  #the term searched will be used in the link
        #the headers for the data request
        headers = {
            'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
            'x-rapidapi-key': rapid_api
        }
        #create a session using aiohttp, request the data using the querystring and the header
        async with aiohttp.ClientSession() as session:
            async with session.get(url='https://mashape-community-urban-dictionary.p.rapidapi.com/define', params=querystring, headers=headers) as r:
                data = await r.json()   #json parse the data
        #if no results are found for the term return
        if not data['list']:
            embed = discord.Embed(color=0xde2f43, description=f':x: No results found.')
            return await ctx.send(embed=embed)
        #assign values for every page (word, link, definition, thumbs up/down)
        word1, word2, word3, word4, word5 = data['list'][0]['word'], data['list'][1]['word'], data['list'][2]['word'], data['list'][3]['word'], data['list'][4]['word']
        link1, link2, link3, link4, link5 = data['list'][0]['permalink'], data['list'][1]['permalink'], data['list'][2]['permalink'], data['list'][3]['permalink'], data['list'][4]['permalink']
        def1, def2, def3, def4, def5 = data['list'][0]['definition'], data['list'][1]['definition'], data['list'][2]['definition'], data['list'][3]['definition'], data['list'][4]['definition']
        ex1, ex2, ex3, ex4, ex5 = data['list'][0]['example'], data['list'][1]['example'], data['list'][2]['example'], data['list'][3]['example'], data['list'][4]['example']
        tup1, tup2, tup3, tup4, tup5 = data['list'][0]['thumbs_up'], data['list'][1]['thumbs_up'], data['list'][2]['thumbs_up'], data['list'][3]['thumbs_up'], data['list'][4]['thumbs_up']
        tdown1, tdown2, tdown3, tdown4, tdown5 = data['list'][0]['thumbs_down'], data['list'][1]['thumbs_down'], data['list'][2]['thumbs_down'], data['list'][3]['thumbs_down'], data['list'][4]['thumbs_down']
        thumbnail = 'https://cdn.discordapp.com/attachments/725102631185547427/738844966528483448/urban-dict.png'
        color = random.randint(0, 0xffffff)
        #create the pages
        p1 = discord.Embed(title=word1, url=link1, description=f'1st definition for `{word1}`', color=color)
        p2 = discord.Embed(title=word2, url=link2, description=f'2nd definition for `{word1}`', color=color)
        p3 = discord.Embed(title=word3, url=link3, description=f'3rd definition for `{word1}`', color=color)
        p4 = discord.Embed(title=word4, url=link4, description=f'4th definition for `{word1}`', color=color)
        p5 = discord.Embed(title=word5, url=link5, description=f'5th definition for `{word1}`', color=color)
        p1.set_thumbnail(url=thumbnail), p2.set_thumbnail(url=thumbnail),p3.set_thumbnail(url=thumbnail), p4.set_thumbnail(url=thumbnail), p5.set_thumbnail(url=thumbnail)
        p1.add_field(name='**Definition**', value=def1), p2.add_field(name='**Definition**', value=def2), p3.add_field(name='**Definition**', value=def3), p4.add_field(name='**Definition**', value=def4), p5.add_field(name='**Definition**', value=def5)
        p1.add_field(name='**Example**', value=ex1, inline=False), p2.add_field(name='**Example**', value=ex2, inline=False), p3.add_field(name='**Example**', value=ex3, inline=False), p4.add_field(name='**Example**', value=ex4, inline=False), p5.add_field(name='**Example**', value=ex5, inline=False)
        p1.add_field(name=':thumbsup:', value=tup1), p2.add_field(name=':thumbsup:', value=tup2), p3.add_field(name=':thumbsup:', value=tup3), p4.add_field(name=':thumbsup:', value=tup4), p5.add_field(name=':thumbsup:', value=tup5)
        p1.add_field(name=':thumbsdown:', value=tdown1), p2.add_field(name=':thumbsdown:', value=tdown2), p3.add_field(name=':thumbsdown:', value=tdown3), p4.add_field(name=':thumbsdown:', value=tdown4), p5.add_field(name=':thumbsdown:', value=tdown5)
        p1.set_author(icon_url=self.bot.user.avatar_url, name='Urban Dictionary'), p2.set_author(icon_url=self.bot.user.avatar_url, name='Urban Dictionary'), p3.set_author(icon_url=self.bot.user.avatar_url, name='Urban Dictionary'), p4.set_author(icon_url=self.bot.user.avatar_url, name='Urban Dictionary'), p5.set_author(icon_url=self.bot.user.avatar_url, name='Urban Dictionary')
        p1.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}'), p2.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}'), p3.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}'), p4.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}'), p5.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
        menu = PaginatedMenu(ctx) #create the menu
        menu.add_pages([p1, p2, p3, p4, p5])  #add the pages to the menu
        menu.set_timeout(60)
        menu.set_cancel_page(p1)
        menu.set_timeout_page(p1)   
        menu.allow_multisession()   #this will let the user invoke another menu while the another one is still active
        await menu.open()   #open the menu

    @commands.command(aliases=['covid19', 'sarscov2', 'covid'], help="get daily statistics for covid19 in a country",
        usage="coronavirus <country>###5s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 5, commands.BucketType.user) #cooldown 10s/user
    async def coronavirus(self, ctx, *, country):
        country.replace(' ', '+')   #replace spaces with plus signs for countries with multiple words in their name
        session = aiohttp.ClientSession()   #create the aiohttp session
        querystring = {"country":f"{country}"}  #the country we search for is put in the querystring
        #headers for the data request
        headers = {
        'x-rapidapi-host': "covid-193.p.rapidapi.com",
        'x-rapidapi-key': rapid_api
        }
        #requesting a response using the querystring and the headers
        response = await session.get(url="https://covid-193.p.rapidapi.com/statistics", params=querystring, headers=headers)
        #json parse the data
        data = json.loads(await response.text())
        if int(data['results']) == 0:   #if there is no results in the requested data return
            embed = discord.Embed(color=0xde2f43, description=f':x: No results for **{country}**.')
            return await ctx.send(embed=embed)
        #assigning values for variables from the data
        population = data['response'][0]['population']
        country = data['response'][0]['country']
        new, active, critical, recovered, total = data['response'][0]['cases']['new'], data['response'][0]['cases']['active'], data['response'][0]['cases']['critical'], data['response'][0]['cases']['recovered'], data['response'][0]['cases']['total']
        deathsn, deathst = data['response'][0]['deaths']['new'], data['response'][0]['deaths']['total']
        testst = data['response'][0]['tests']['total']
        await session.close()   #close the session
        #create the embed
        embed = discord.Embed(title=f'Statistics for {country}', color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/725102631185547427/739190220448202912/covid19.png')
        embed.set_author(icon_url=self.bot.user.avatar_url, name='COVID-19 Statistics')
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
        embed.add_field(name='Population', value=f'```ini\n[{population}]\n```')
        embed.add_field(name='Total cases', value=f'```diff\n->[{total}]\n```')
        embed.add_field(name='Total tests', value=f'```fix\n{testst}\n```')
        embed.add_field(name='New cases', value=f'```css\n[{new}]\n```')
        embed.add_field(name='Active cases', value=f'```css\n[{active}]\n```')
        embed.add_field(name='Critical cases', value=f'```css\n[{critical}]\n```')
        embed.add_field(name='Recovered', value=f'```diff\n+{recovered}\n```')
        embed.add_field(name='New deaths', value=f'```{deathsn}```')
        embed.add_field(name='Total deaths', value=f'```{deathst}```')
        await ctx.send(embed=embed) #send the embed

    #a command group in which you can create a shopping list, add different tasks, you know the deal
    @commands.group(help="create task/shopping/etc. lists", usage="todo###1s/user###No", case_insensitive=True)
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=':pencil2: To do list commands', color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
            description = f'{ctx.prefix}todo add `item`: Add a new task to your to do list.\n'
            description += f'{ctx.prefix}todo list: See your to do list.\n'
            description += f'{ctx.prefix}todo remove `item_number`: Remove an item from your list.\n'
            description += f'{ctx.prefix}todo edit `item_number` `edit`: Edit an item from the list.\n'
            description += f'{ctx.prefix}todo clear: Clears your list.'
            embed.description = description
            await ctx.send(embed=embed)

    #add an item to the list
    @todo.command()
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add(self, ctx, *, task: str):
        with open('./user data/todo.json', 'r') as f:   #open the json file and load it
            user_list = json.load(f)
        try:    #try to add the item to the list
            user_list[str(ctx.message.author.id)].append(task)
        except Exception as error:  #if the user did not create a list before, initialize one in the json file
            if isinstance(error, KeyError):
                user_list[str(ctx.message.author.id)] = []
                user_list[str(ctx.message.author.id)].append(task)
        with open('./user data/todo.json', 'w') as f:   #open the json file and dump the list
            json.dump(user_list, f, indent=4)
        embed = embed = discord.Embed(description=':memo: Successfully added in the list.', color=random.randint(0, 0xffffff))
        await ctx.send(embed=embed)

    #see your todo list
    @todo.command(aliases=['list'])
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def _list(self, ctx):
        with open('./user data/todo.json', 'r') as f:   #open the json file and load it
            user_list = json.load(f)
        #create the embed
        embed = discord.Embed(title=f":clipboard: {str(ctx.message.author)[:-5]}'s to do list", color=random.randint(0, 0xffffff))
        description = ''
        try:    #try to get the string containing the tasks
            tasks = user_list[str(ctx.message.author.id)]
        except Exception as error:  #if the user didn't create a list
            if isinstance(error, KeyError):
                description += '**No items added.**'
                embed.description = description
                return await ctx.send(embed=embed)
        if tasks == []: #if the list is empty
            description += 'No items added.'
            embed.description = description
            return await ctx.send(embed=embed)
        for i in range(0, len(tasks)):
            description += f'**{i+1}.** __{tasks[i]}__\n'
        embed.description = description
        await ctx.send(embed=embed) #send the embed

    #remove an item from the list
    @todo.command()
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def remove(self, ctx, item: int):
        with open('./user data/todo.json', 'r') as f:   #open the json file and load it
            user_list = json.load(f)
        embed = discord.Embed(color=0xde2f43)
        if item < 1:    #we start counting from 1 in the todo list
            embed.description = ':x: List index out of range.'
            return await ctx.send(embed=embed)
        try:    #try to get the users' list
            tasks = user_list[str(ctx.message.author.id)]
        except Exception as error:  #if the user did not create a list
            if isinstance(error, KeyError):
                embed.description = ':x: Your list is empty.'
                return await ctx.send(embed=embed)
        if tasks == []: #if the users' list is empty
            embed.description = ':x: Your list is empty.'
            return await ctx.send(embed=embed)
        try:
            tasks.remove(tasks[item-1]) #remove the item
        except Exception as error:  #if the number of the item is not on the list
            if isinstance(error, IndexError):
                embed.description = ':x: List index out of range.'
                return await ctx.send(embed=embed)
        user_list[str(ctx.message.author.id)] = tasks   #assign the new list to the user
        with open('./user data/todo.json', 'w') as f:   #open the file and dump the new list
            json.dump(user_list, f, indent=4)
        embed = discord.Embed(description=':outbox_tray: Successfully removed from the list.', color=random.randint(0, 0xffffff))
        await ctx.send(embed=embed)

    #edit an item from the list
    #same as above, but instead of removing the item, we replace it
    @todo.command()
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def edit(self, ctx, item: int, *, task):
        with open('./user data/todo.json', 'r') as f:
            user_list = json.load(f)
        embed = discord.Embed(color=0xde2f43)
        if item < 1:
            embed.description = ':x: List index out of range.'
            return await ctx.send(embed=embed)
        try:
            tasks = user_list[str(ctx.message.author.id)]
        except Exception as error:
            if isinstance(error, KeyError):
                embed.description = ':x: Your list is empty.'
                return await ctx.send(embed=embed)
        if tasks == []:
            embed.description = ':x: Your list is empty.'
            return await ctx.send(embed=embed)
        try:
            tasks[item-1] = task
        except Exception as error:
            if isinstance(error, IndexError):
                embed.description = ':x: List index out of range.'
                return await ctx.send(embed=embed)
        user_list[str(ctx.message.author.id)] = tasks
        with open('./user data/todo.json', 'w') as f:
            json.dump(user_list, f, indent=4)
        embed = discord.Embed(description=':memo: Successfully edited the list.', color=random.randint(0, 0xffffff))
        await ctx.send(embed=embed)

    #clear the list
    @todo.command()
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def clear(self, ctx):
        with open('./user data/todo.json', 'r') as f:   #open the json file and load it
            user_list = json.load(f)
        user_list[str(ctx.message.author.id)] = []  #empty the list
        with open('./user data/todo.json', 'w') as f:   #open the json file and dump the empty list
            json.dump(user_list, f, indent=4)
        embed = discord.Embed(description=':notepad_spiral: Successfully cleared list.', color=random.randint(0, 0xffffff))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Utils(bot))