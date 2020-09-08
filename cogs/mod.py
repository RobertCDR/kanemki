import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import json
import datetime
import typing

#the moderation commands need some reworking because I can't catch the errors properly and they still need some fixes
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #a listener for when the bot is removed from a guild
    #it removes the data stored in the guild data such as custom prefixes, roles
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open ('./guild data/mutedroles.json', 'r') as f:
            mutedrole = json.load(f)
        mutedrole.pop(str(guild.id))
        with open('./guild data/mutedroles.json', 'w') as f:
            json.dump(mutedrole, f, indent=4)
        with open ('./guild data/joinroles.json', 'r') as f:
            joinrole = json.load(f)
        joinrole.pop(str(guild.id))
        with open('./guild data/joinroles.json', 'w') as f:
            json.dump(joinrole, f, indent=4)
        with open ('./guild data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('./guild data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    #a listener which adds roles to bots/members when they join
    #the roles must be manually set using the config command
    #and this is exactly the problem, not fatal, but needs to be fixed because it raises an error if the guild does not have the roles set
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            if member.bot:  #if a bot joins the guild
                with open('./guild data/botroles.json', 'r') as f:  #open the json file containing bot roles
                    botrole = json.load(f)  #load it
                role = botrole[str(member.guild.id)]    #get the id of the bot role set in the guild
                role = discord.utils.get(member.guild.roles, id=role)   #get the role
                await member.add_roles(role)    #add it to the bot
            else:   #if a non-bot account joins the guild
                with open('./guild data/joinroles.json', 'r') as f: #open the json file containing member roles
                    joinrole = json.load(f) #load it
                role = joinrole[str(member.guild.id)]   #get the id of the role set in the guild
                role = discord.utils.get(member.guild.roles, id=role)   #get the role
                await member.add_roles(role)    #add it to the user
        #if the guild did not set any role to be assigned to new members, a KeyError will be raised trying to load the role id for that guild
        except Exception as error:  #soo the bot will ignore it
            if isinstance(error, KeyError):
                pass
        #it wasn't a fatal error, but why see it raised in your terminal tho

    #a command group for server configuration commands
    @commands.group(case_insensitive=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None: #if a subcommand is not invoked, display a list with server configuration commands
            embed = discord.Embed(title=':tools: Server Configuration Commands', color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
            description = '**Customize your experience with Kanemki using these server configuration commands (acknowledge that these are server admin only commands).**\n'
            description += f'{ctx.prefix}config prefix `prefix`: Change the server prefix. (type `default` or `clear` for the default prefix)\n'
            description += f'{ctx.prefix}config muted-set `@role`: Assign the role given to muted members.\n'
            description += f'{ctx.prefix}config muted-remove: Remove the custom muted role of the guild.\n'
            description += f'{ctx.prefix}config joinrole-set `@role`: Assign the role given to new guild members.\n'
            description += f'{ctx.prefix}config joinrole-remove: Remove the role given to new guild members.\n'
            description += f'{ctx.prefix}config botrole-set `@role`: Assign the role given to bots that join the guild.\n'
            description += f'{ctx.prefix}config botrole-remove: Remove the role given to bots when they join the guild.'
            embed.description = description
            await ctx.send(embed=embed)

    #a command which sets a custom prefix for the guild
    @config.command()
    @commands.has_permissions(administrator=True)   #check if the command author is a server admin
    async def prefix(self, ctx, prefix : str=None):
        if not prefix:  #if a prefix is not specified return and notify the user
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify a prefix.')
            return await ctx.send(embed=embed)
        set_default = ['default', 'clear']
        if len(prefix) > 5 and prefix.lower() not in set_default: #if the length of the prefix is too big
            embed = discord.Embed(color=0xfccc51, description=':warning: Prefix length can be max 5 characters.')
            return await ctx.send(embed=embed)
        with open ('./guild data/prefixes.json', 'r') as f: #open the json file containig prefixes
            prefixes = json.load(f) #load it
        if prefix.lower() == 'default' or prefix.lower() == 'clear':    #'default' and 'clear' will set the guild prefix to the default bot prefix
            prefixes[str(ctx.guild.id)] = '>'
        else:   #if an actual custom prefix is given
            prefixes[str(ctx.guild.id)] = prefix    #put into the json file as the value associated with the guild's id
        with open('./guild data/prefixes.json', 'w') as f:  #open the json file in write mode
            json.dump(prefixes, f, indent=4)    #dump the new prefix
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully changed guild prefix to **{prefixes[str(ctx.guild.id)]}**.')
        await ctx.send(embed=embed)

    #I'm only leaving comments on the next three things
    #the same principle is followed by the next subcommands
    #a subcommand which sets a custom mute role for the mute command
    @config.command(aliases=['muted-set'])
    @commands.has_permissions(administrator=True)
    async def muted_set(self, ctx, role: discord.Role):
        with open('./guild data/mutedroles.json', 'r') as f:    #open the json file contaning mute roles
            mutedrole = json.load(f)    #load it
        mutedrole[str(ctx.guild.id)] = role.id  #put the id into the json file as the value associated with the guild's id
        with open('./guild data/mutedroles.json', 'w') as f:    #open the json file in write mode
            json.dump(mutedrole, f, indent=4)   #dump the guild's id along with it's value, the role id
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully changed muted role to {role.mention}.')
        await ctx.send(embed=embed)

    #this subcommand removes the custom muted role of a guild
    @config.command(aliases=['muted-remove'])
    @commands.has_permissions(administrator=True)
    async def muted_remove(self, ctx):
        with open ('./guild data/mutedroles.json', 'r') as f:   #open the json file containing mute role ids for guilds
            joinrole = json.load(f) #load it
        joinrole.pop(str(ctx.guild.id)) #pop the guild id and it's value, the role id
        with open('./guild data/mutedroles.json', 'w') as f:    #open the json file in write mode
            json.dump(joinrole, f, indent=4)    #dump the modifications
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully removed muted role.')
        await ctx.send(embed=embed)

    @config.command(aliases=['joinrole-set'])
    @commands.has_permissions(administrator=True)
    async def joinrole_set(self, ctx, role: discord.Role):
        with open('./guild data/joinroles.json', 'r') as f:
            joinrole = json.load(f)
        joinrole[str(ctx.guild.id)] = role.id
        with open('./guild data/joinroles.json', 'w') as f:
            json.dump(joinrole, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully changed member role to {role.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['joinrole-remove'])
    @commands.has_permissions(administrator=True)
    async def joinrole_remove(self, ctx):
        with open ('./guild data/joinroles.json', 'r') as f:
            joinrole = json.load(f)
        joinrole.pop(str(ctx.guild.id))
        with open('./guild data/joinroles.json', 'w') as f:
            json.dump(joinrole, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully removed member join role.')
        await ctx.send(embed=embed)

    @config.command(aliases=['botrole-set'])
    @commands.has_permissions(administrator=True)
    async def botrole_set(self, ctx, role: discord.Role):
        with open('./guild data/botroles.json', 'r') as f:
            joinrole = json.load(f)
        joinrole[str(ctx.guild.id)] = role.id
        with open('./guild data/botroles.json', 'w') as f:
            json.dump(joinrole, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully changed bot join role to {role.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['botrole-remove'])
    @commands.has_permissions(administrator=True)
    async def botrole_remove(self, ctx):
        with open ('./guild data/botroles.json', 'r') as f:
            joinrole = json.load(f)
        joinrole.pop(str(ctx.guild.id))
        with open('./guild data/botroles.json', 'w') as f:
            json.dump(joinrole, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Succesfully removed bot join role.')
        await ctx.send(embed=embed)

    #this command displays a list of the guild roles
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def roles(self, ctx):
        #create a string with mentioned roles in top to bottom order
        roles = '\n'.join(role.mention for role in ctx.guild.roles[::-1])
        #create the embed
        embed = discord.Embed(color=0xff0000, title='Guild roles', description=roles, timestamp=datetime.datetime.utcnow())
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed) #send the embed

    #a purge command
    #this will need further development too
    @commands.command(aliases=['purge', 'clean'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int=0):
        if not amount:  #if no amount is specified
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of messages to clear.')
            await ctx.send(embed=embed)
        else:
            if amount <= 1000:  #if the amount is under 1k messages
                await ctx.channel.purge(limit=amount+1)
            else:
                embed = discord.Embed(color=0xfccc51, description=':warning: The amount is too big.')
                return await ctx.send(embed=embed)

    #mute a user / mass mute users
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, victims : commands.Greedy[discord.Member]=None, time=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        if not time:    #if the mute time is not specified
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of time (ex: 10s, 10m, 10h, 10d, 10w).')
            return await ctx.send(embed=embed)
        def convert_time_to_seconds(time):  #a function that converts the mute time according to how the command author specified
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
            try:
                return int(time[:-1]) * time_convert[time[-1]]
            except:
                return time
        with open('./guild data/mutedroles.json', 'r') as f:    #open the json file containing muted roles ids
            mutedrole = json.load(f)    #load the file
        if str(ctx.guild.id) in str(mutedrole): #if the guild has already a muted role set
            muted = mutedrole[str(ctx.guild.id)]    #get the id of the role
            muted = discord.utils.get(ctx.guild.roles, id=muted)  #get the role
        else:   #if there is no muted role set for the guild create a default one
            perms = discord.Permissions(read_messages=True, add_reactions=True, external_emojis=True, change_nickname=True)
            muted = await ctx.guild.create_role(name='Muted', permissions=perms)
            mutedrole[str(ctx.guild.id)] = muted.id
            #after creating the default mute role dump it into the json file
            with open('./guild data/mutedroles.json', 'w') as f:
                json.dump(mutedrole, f, indent=4)
        muted_members = []
        for victim in victims:  #iterate through the mentioned users
            if victim.bot:  #if the member mentioned is a bot
                embed = discord.Embed(color=0xde2f43, description=':octagonal_sign: Cannot mute bots (due to solidarity for my people).')
                await ctx.send(embed=embed)
            #if the member mentioned has mod permissions or is an admin
            elif victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
                embed = discord.Embed(color=0xde2f43, description=':x: That user is a mod/admin.')
                await ctx.send(embed=embed)
            elif muted in victim.roles: #if the user is already muted
                embed = discord.Embed(color=0xde2f43, description=':x: That user is already muted.')
                await ctx.send(embed=embed)
            else:   #if the user passed the above checks
                await victim.add_roles(muted)   #add the role to the user
                muted_members.append(victim)    #add the user to a list of muted users
        if len(muted_members) > 0:  #if at least one member was muted
            _list = ', '.join(victim.mention for victim in muted_members)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Succesfully muted** {_list}**.**')
            await ctx.send(embed=embed)
            for victim in muted_members:    #iterate through the muted users list
                dm = await victim.create_dm()   #create a conversation with the members
                message = discord.Embed(color=0xff0000, title=f"You've been muted in **{ctx.guild.name}**.", description=f"**Reason**: {reason}")
                message.set_thumbnail(url=ctx.guild.icon_url)
                await dm.send(embed=message)   #message that he/she was muted in that guild
            await asyncio.sleep(convert_time_to_seconds(time))  #wait for the time to pass
            for victim in muted_members:
                await victim.remove_roles(muted)    #remove the role from the members

    #unmute a user / mass unmute users
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, victims : commands.Greedy[discord.Member]=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        with open('./guild data/mutedroles.json', 'r') as f:    #open and load the json file
            mutedrole = json.load(f)
        muted = mutedrole[str(ctx.guild.id)]    #get the id of the role
        muted = discord.utils.get(ctx.guild.roles, id=muted)  #get the role
        unmuted_list = []
        for victim in victims:  #iterate through the mentioned users
            if victim.bot:  #if the member mentioned is a bot
                embed = discord.Embed(color=0xde2f43, description=':octagonal_sign: That user is a bot.')
                await ctx.send(embed=embed)
            #if the member mentioned has mod permissions or is an admin
            elif victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
                embed = discord.Embed(color=0xde2f43, description=':x: That user is a mod/admin.')
                await ctx.send(embed=embed)
            elif muted in victim.roles: #if the user is indeed muted
                await victim.remove_roles(muted)    #remove the role
                unmuted_list.append(victim) #add the member to a list of unmuted members
            else:   #if the user passed all the checks but it's not muted
                embed = discord.Embed(color=0xde2f43, description=':x: That user is not muted.')
                await ctx.send(embed=embed)
        if len(unmuted_list) > 0:   #if at least one user was unmuted
            _list = ', '.join(victim.mention for victim in unmuted_list)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Succesfully unmuted** {_list}**.**')
            await ctx.send(embed=embed)

    #kick a user / mass kick users
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, victims : commands.Greedy[discord.Member]=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        kicked_list = []
        for victim in victims:
            if victim.bot:
                embed = discord.Embed(color=0xde2f43, description=':stop_sign: Cannot kick bots (due to solidarity for my people).')
                return await ctx.send(embed=embed)
            elif victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
                embed = discord.Embed(color=0xde2f43, description=':x: This user is a mod/admin.')
                return await ctx.send(embed=embed)
            else:
                await victim.kick(reason=reason)    #kick the member
                kicked_list.append(victim)
        if len(kicked_list) > 0:
            _list = ', '.join(victim.mention for victim in kicked_list)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Succesfully kicked** {_list}**.**')
            await ctx.send(embed=embed)
            for victim in kicked_list:
                dm = await victim.create_dm()
                message = discord.Embed(color=0xff0000, title=f"You've been kicked from **{ctx.guild.name}**.", description=f"**Reason**: {reason}")
                message.set_thumbnail(url=ctx.guild.icon_url)
                await dm.send(embed=message)
        
    #ban a user / mass ban users
    #same thing as above
    #it will need some further inspection because it does not work with the user id if the user is not in the guild
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, victims : commands.Greedy[discord.Member]=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        banned_list = []
        for victim in victims:
            if victim.bot:
                embed = discord.Embed(color=0xde2f43, description=':stop_sign: Cannot ban bots (due to solidarity for my people).')
                return await ctx.send(embed=embed)
            elif victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
                embed = discord.Embed(color=0xde2f43, description=':x: This user is a mod/admin.')
                return await ctx.send(embed=embed)
            else:
                await victim.ban(reason=reason)    #ban the member
                banned_list.append(victim)
        if len(banned_list) > 0:
            _list = ', '.join(victim.mention for victim in banned_list)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Succesfully banned** {_list}**.**')
            await ctx.send(embed=embed)
            for victim in banned_list:
                dm = await victim.create_dm()
                message = discord.Embed(color=0xff0000, title=f"You've been banned in **{ctx.guild.name}**.", description=f"**Reason**: {reason}")
                message.set_thumbnail(url=ctx.guild.icon_url)
                await dm.send(embed=message)

    #unban a user / mass unban users
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, victims : commands.Greedy[discord.Object]=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        users = []
        for victim in victims:
            await ctx.guild.unban(victim)  #unban the user by it's id
            banned_user = str(victim).split("=", 1)
            users.append(f'<@{banned_user[1][:-1]}>')
        _list = ', '.join(users)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Succesfully unbanned** {_list}**.**')
        await ctx.send(embed=embed)
    
    #not so sure about this command
    #it will need some reworking in the future
    @commands.command(aliases=['tempban'])
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, victim : discord.Member, time=None, *, reason=None):
        if victim.bot:
            embed = discord.Embed(color=0xde2f43, description=':stop_sign: Cannot ban bots (due to solidarity for my people).')
            return await ctx.send(embed=embed)
        if victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
            embed = discord.Embed(color=0xde2f43, description=':x: This user is a mod/admin.')
            return await ctx.send(embed=embed)
        if not time:
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of time (ex: 1h, 1d, 1wm 1m, 1y).')
            return await ctx.send(embed=embed)
        await victim.ban(reason=reason)
        dm = await victim.create_dm()
        message = discord.Embed(color=0xff0000, title=f"You've been softbanned in **{ctx.guild.name}**.", description=f"**Reason**: {reason}\n**Time**: {time}")
        message.set_thumbnail(url=ctx.guild.icon_url)
        await dm.send(embed=message)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: {victim.mention} **has been softbanned.**')
        await ctx.send(embed=embed)
        def convert_time_to_seconds(time):
            time_convert = {"h": 3600, "d": 86400, "w": 604800, "m": 2592000, "y": 31536000}
            try:
                return int(time[:-1]) * time_convert[time[-1]]
            except:
                return time
        await asyncio.sleep(convert_time_to_seconds(time))
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
        if user.id == victim.id:
            await ctx.guild.unban(user)

    #unban all the users that have been banned in the guild
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unbanall(self, ctx):
        banned_users = await ctx.guild.bans()   #get all the banned users
        for ban_entry in banned_users:  #unban them one by one
            user = ban_entry.user
            await ctx.guild.unban(user)
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: **Succesfully unbanned all guild bans.**')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))