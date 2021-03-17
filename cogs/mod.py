import discord
from discord.ext import commands
import asyncio
import datetime
import typing
from dpymenus import PaginatedMenu
from cogs.errors import CustomChecks
import config
from pymongo import MongoClient

cluster = MongoClient(config.db_client)
database = cluster["KanemkiDB"]
guild_collection = database["guilddata"]

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    alias = "Moderation"

    @commands.group(help="blacklist users from using the bot in the server", usage="blacklist###1s/user###No", case_insensitive=True)
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def blacklist(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title='Blacklist', description='Blacklist or whitelist users from using the bot on this guild. *Note that only the server owner or the creator of the bot himself can use these commands.*\n\n')
            embed.description += f"{ctx.prefix}blacklist add `user` or `user_id`\n"
            embed.description += f"{ctx.prefix}blacklist remove `user` or `user_id`"
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

    @blacklist.command()
    @CustomChecks.blacklist_check()
    @CustomChecks.blacklist_perm_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def add(self, ctx, user: discord.User):
        if user.id == 465138950223167499:
            embed = discord.Embed(color=0xde2f43, description=':x: You cannot blacklist the creator of the bot from his own bot.')
            return await ctx.send(embed=embed)
        elif user.id == 723864146965168168:
            embed = discord.Embed(color=0xde2f43, description=':x: You cannot blacklist the bot himself.')
            return await ctx.send(embed=embed)
        else:
            try:
                results = guild_collection.find_one({"_id": ctx.guild.id})
                blacklist = results["blacklist"]
                if user.id in blacklist:
                    embed = discord.Embed(color=0xde2f43, description=':x: User already blacklisted on this server.')
                    return await ctx.send(embed=embed)
                else:
                    blacklist.append(user.id)
                    guild_collection.update_one({"_id": ctx.guild.id}, {"$addToSet": {"blacklist": user.id}})
            except Exception as error:
                if isinstance(error, KeyError):
                    guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"blacklist": [user.id]}})
                else:
                    raise error
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully blacklisted {user.mention} from using the bot on this server.')
        await ctx.send(embed=embed)

    @blacklist.command()
    @CustomChecks.blacklist_check()
    @CustomChecks.blacklist_perm_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def remove(self, ctx, user: discord.User):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            blacklist = result["blacklist"]
            if blacklist == []:
                embed = discord.Embed(color=0xde2f43, description=':x: Blacklist empty.')
                return await ctx.send(embed=embed)
            if user.id in blacklist:
                blacklist.remove(user.id)
                guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"blacklist": blacklist}})
            else:
                embed = discord.Embed(color=0xde2f43, description=':x: User not on blacklist.')
                return await ctx.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: Blacklist empty.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully removed {user.mention} from bot blacklist.')
        await ctx.send(embed=embed)

    #a command group for server configuration commands
    @commands.group(case_insensitive=True, help="configuration commands for the server", usage="config###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None: #if a subcommand is not invoked, display a list with server configuration commands
            embed = discord.Embed(title=':tools: Server Configuration Commands', color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
            description = '**Customize your server using these configuration commands (acknowledge that you need administrator permissions).**\n'
            description += f'{ctx.prefix}config prefix `prefix`: Change the server prefix. (type `default` or `clear` for the default prefix)\n'
            description += f'{ctx.prefix}config muted-set `@role`: Assign the role given to muted members.\n'
            description += f'{ctx.prefix}config muted-remove: Remove the custom muted role of the guild.\n'
            description += f'{ctx.prefix}config joinrole-set `@role`: Assign the role given to new guild members.\n'
            description += f'{ctx.prefix}config joinrole-remove: Remove the role given to new guild members.\n'
            description += f'{ctx.prefix}config botrole-set `@role`: Assign the role given to bots that join the guild.\n'
            description += f'{ctx.prefix}config botrole-remove: Remove the role given to bots when they join the guild.\n'
            description += f'{ctx.prefix}config welcomech-set `#channel`: Set a welcome channel to greet new members.\n'
            description += f'{ctx.prefix}config welcomech-remove: Remove the welcome channel for new members.\n'
            description += f'{ctx.prefix}config welcomemsg-set `message`: Set a welcome message for new members.\n'
            description += f'{ctx.prefix}config welcomemesg-remove: Remove the welcome message.\n'
            description += f'{ctx.prefix}config logsch-set `#channel`: Set a logs channel\n'
            description += f'{ctx.prefix}config logsch-remove: Remove the logs channel.\n'
            """
            description += f'{ctx.prefix}config starboard-set `#channel`: Set a starboard channel where messages with the :star: reaction will be highlighted.\n'
            description += f'{ctx.prefix}config starboard-remove: Remove the starboard channel.'
            """
            embed.description = description
            await ctx.send(embed=embed)

    #a command which sets a custom prefix for the guild
    @config.command()
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)   #check if the command author is a server admin
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def prefix(self, ctx, prefix : str=None):
        if not prefix:  #if a prefix is not specified return and notify the user
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify a prefix.')
            return await ctx.send(embed=embed)
        set_default = ['default', 'clear', 'standard']
        if len(prefix) > 5 and prefix.lower() not in set_default: #if the length of the prefix is too big
            embed = discord.Embed(color=0xfccc51, description=':warning: Prefix length can be max 5 characters.')
            return await ctx.send(embed=embed)
        if prefix.lower() == 'default' or prefix.lower() == 'clear':    #'default' and 'clear' will set the guild prefix to the default bot prefix
            prefix = ">"
            guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
        else:   #if an actual custom prefix is given
            guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"prefix": prefix}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully changed guild prefix to **{prefix}**.')
        await ctx.send(embed=embed)

    @config.command(aliases=['muted-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def muted_set(self, ctx, muted: discord.Role):
        guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mutedrole": muted.id}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully changed muted role to {muted.mention}.')
        #overwrite the channel permissions for the muted role
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(muted)
            perms.send_messages = False
            await channel.set_permissions(muted, overwrite=perms)
        for channel in ctx.guild.voice_channels:
            perms = channel.overwrites_for(muted)
            perms.connect = False
            await channel.set_permissions(muted, overwrite=perms)
        await ctx.send(embed=embed)

    #this subcommand removes the custom muted role of a guild
    @config.command(aliases=['muted-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def muted_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            role_id = result["mutedrole"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"mutedrole": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No muted role was set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: Successfully removed muted role.')
        await ctx.send(embed=embed)

    @config.command(aliases=['joinrole-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joinrole_set(self, ctx, role: discord.Role):
        guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"joinrole": role.id}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully changed member role to {role.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['joinrole-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def joinrole_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            role_id = result["joinrole"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"joinrole": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No join role was set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: Successfully removed member join role.')
        await ctx.send(embed=embed)

    @config.command(aliases=['botrole-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botrole_set(self, ctx, role: discord.Role):
        guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"botrole": role.id}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully changed bot join role to {role.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['botrole-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botrole_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            role_id = result["botrole"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"botrole": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No bot role was set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: Successfully removed bot join role.')
        await ctx.send(embed=embed)

    @config.command(aliases=['logsch-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def logsch_set(self, ctx, channel: discord.channel.TextChannel):
        guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"logsch": channel.id}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully set logs channel to {channel.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['logsch-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def logsch_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            channel_id = result["logsch"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"logsch": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No logs was channel set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: Successfully removed logs channel.')
        await ctx.send(embed=embed)

    @config.command(aliases=['welcomech-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcomech_set(self, ctx, channel: discord.channel.TextChannel):
        guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"welcomech": channel.id}})
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully set welcome channel to {channel.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['welcomech-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcomech_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            channel_id = result["welcomech"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"welcomech": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No welcome channel was set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully removed welcome channel.')
        await ctx.send(embed=embed)

    @config.command(aliases=['welcomemsg-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcomemsg_set(self, ctx, *, message):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            channel_id = result["welcomech"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"welcomemsg": message}})
        except Exception as error:
            if isinstance(error, KeyError):
                guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"welcomech": ctx.channel.id}})
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully set welcome message.')
        await ctx.send(embed=embed)

    @config.command(aliases=['welcomemsg-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def welcomemsg_remove(self, ctx):
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            message = result["welcomemsg"]
            guild_collection.update_one({"_id": ctx.guild.id}, {"$unset": {"welcomemsg": ""}})
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No welcome message was set.')
                return await ctx.send(embed=embed)
            else:
                raise error
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully removed welcome message.')
        await ctx.send(embed=embed)
    
    """
    @config.command(aliases=['starboard-set'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def starboard_set(self, ctx, channel: discord.channel.TextChannel):
        with open('./guild data/starboards.json', 'r') as f:
            starboards = json.load(f)
        starboards[str(ctx.guild.id)] = channel.id
        with open('./guild data/starboards.json', 'w') as f:
            json.dump(starboards, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully set starboard to {channel.mention}.')
        await ctx.send(embed=embed)

    @config.command(aliases=['starboard-remove'])
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def starboard_remove(self, ctx):
        with open('./guild data/starboards.json', 'r') as f:
            starboards = json.load(f)
        try:
            starboards.pop(str(ctx.guild.id))
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No logs was channel set.')
                return await ctx.send(embed=embed)
            else:
                raise
        with open('./guild data/starboards.json', 'w') as f:
            json.dump(starboards, f, indent=4)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully removed starboard channel.')
        await ctx.send(embed=embed)
    """

    @commands.command(help="get a list of all the roles in the guild", usage="roles###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roles(self, ctx):
        #create a string with mentioned roles in top to bottom order
        roles = '\n'.join(role.mention for role in ctx.guild.roles[::-1])
        #create the embed
        embed = discord.Embed(color=0xff0000, title='Guild roles', description=roles, timestamp=datetime.datetime.utcnow())
        embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {str(ctx.message.author)}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed) #send the embed

    #create a new role with optional color, hoist and mention parameters
    @commands.command(help="create a newrole",
        usage="newrole <name> <color>`[optional->hex]` <hoist>`[optional->True/False]` <mentioable>`[optional->True/False]`###2s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def newrole(self, ctx, name: str=None, color: typing.Optional[discord.Color]=None, hoist: typing.Optional[bool]=False, mentionable: typing.Optional[bool]=False):
        if name is None:    #the role needs at least a name
            return await ctx.send("name the role first")
        #create the role using the given parameters
        #todo optional permissions shall be added when I remember
        if color:
            role = await ctx.guild.create_role(name=name, color=color, hoist=hoist, mentionable=mentionable)
        else:
            role = await ctx.guild.create_role(name=name, hoist=hoist, mentionable=mentionable)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully created role {role.mention}.')
        await ctx.send(embed=embed)

    @commands.command(help="delete a role", usage="delrole @role(s)###2s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delrole(self, ctx, role: commands.Greedy[discord.Role]):
        for x in role:
            await x.delete()
        embed = discord.Embed(color=0x75b254, description=f":white_check_mark: Roles deleted: {', '.join(list(map(lambda x: x.name, role)))}.")
        await ctx.send(embed=embed)

    @commands.command(help="add a role to a member", usage="addrole @role @user(s)###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def addrole(self, ctx, role: discord.Role, member: commands.Greedy[discord.Member]):
        for x in member:
            if role in x.roles:
                pass
            else:
                await x.add_roles(role)
        embed = discord.Embed(color=0x75b254, description=f":white_check_mark: Successfully added role {role.mention} to {' '.join(list(map(lambda x: x.mention, member)))}.")
        await ctx.send(embed=embed)

    @commands.command(help="remove a role from a member", usage="remrole @role @user(s)###1s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def remrole(self, ctx, role: discord.Role, member: commands.Greedy[discord.Member]):
        for x in member:
            if role not in x.roles:
                pass
            else:
                await x.remove_roles(role)
        embed = discord.Embed(color=0x75b254, description=f":white_check_mark: Successfully removed role {role.mention} from {' '.join(list(map(lambda x: x.mention, member)))}.")
        await ctx.send(embed=embed)

    @commands.command(help="lock a text channel", usage="lock #channel###2s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        #get the channel overwrites for @everyone
        perms = channel.overwrites_for(ctx.guild.default_role)
        #deny the permissions to send messages
        perms.send_messages = False
        #overwrite the new permissions for @everyone
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        embed = discord.Embed(color=0xfccc51, description=':warning: Channel has been locked.')
        await channel.send(embed=embed)

    #unlock a text channel
    @commands.command(help="unlock a text channel", usage="unlock #channel###2s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def unlock(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel =  ctx.channel
        perms = channel.overwrites_for(ctx.guild.default_role)
        perms.send_messages = None
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Channel has been unlocked.')
        await channel.send(embed=embed)

    #same thing as above, but in a for loop and with overwrites for voice channels
    @commands.command(help="lock all text and voice channels except the ones that are invisible", usage="lockdown###15s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lockdown(self, ctx):
        embed = discord.Embed(color=0xde2f43, description=':octagonal_sign: Server lockdown.')
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            if perms.send_messages is (None or True):
                perms.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
                await channel.send(embed=embed)
                await asyncio.sleep(1.5)
            else:
                pass
        for channel in ctx.guild.voice_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            if perms.connect is (None or True):
                perms.connect = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            else:
                pass

    @commands.command(aliases=['lockdown-end'], help="unlock the text/voice channels locked after the lockdown", usage="lockdownend###15s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def lockdownend(self, ctx):
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Lockdown ended.')
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)
            await channel.send(embed=embed)
            await asyncio.sleep(1.5)
        for channel in ctx.guild.voice_channels:
            perms = channel.overwrites_for(ctx.guild.default_role)
            perms.connect = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

    @commands.command(aliases=['revokeinv', 'deleteinvite', 'delinvite', 'revokeinvite'],
        help="revoke a server invite", usage="delinv <invite_link>###2s/user###No"
    )
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def delinv(self, ctx, invite: discord.Invite):
        if invite.guild is not ctx.guild:
            embed = discord.Embed(color=0xde2f43, description=':x: Invite must be from this guild.')
            return await ctx.send(embed=embed)
        await self.bot.delete_invite(invite)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: Successfully revoked invite.')
        await ctx.send(embed=embed)

    #todo this will need further development too
    @commands.command(aliases=['purge', 'clean'], help="purge an amount of messages from a channel", usage="clear <amount>###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
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

    @commands.command(help="mute/mass mute users", usage="mute @user(s) <time>(ex: 1s/m/h/d) <reason>`[optional]`###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def mute(self, ctx, victims : commands.Greedy[discord.Member]=None, time=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        if not time:    #if the mute time is not specified
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of time (ex: 10s, 10m, 10h, 10d, 10w).')
            return await ctx.send(embed=embed)
        def convert_time_to_seconds(time):  #a function that converts the mute time according to how the command author specified
            time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "S": 1, "M": 60, "H": 3600, "D": 86400, "W": 604800}
            try:
                x = time_convert[time[-1]]
            except Exception as error:
                if isinstance(error, KeyError):
                    x = 0;
            if x:
                try:
                    return int(time[:-1]) * time_convert[time[-1]]
                except:
                    return time
            else:
                return False
        if not convert_time_to_seconds(time):
            embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of time (ex: 10s, 10m, 10h, 10d, 10w).')
            return await ctx.send(embed=embed)
        result = guild_collection.find_one({"_id": ctx.guild.id})
        try:
            muted = result["mutedrole"]
            muted = discord.utils.get(ctx.guild.roles, id=muted)
            if muted is None:
                raise KeyError
        #if there is no muted role set for the guild create a default one and overwrite it's channel permissions
        except Exception as error:
            if isinstance(error, KeyError):
                perms = discord.Permissions(read_messages=True, add_reactions=True, external_emojis=True, change_nickname=True)
                muted = await ctx.guild.create_role(name='Muted', permissions=perms)
                guild_collection.update_one({"_id": ctx.guild.id}, {"$set": {"mutedrole": muted.id}})
            else:
                raise error
            for channel in ctx.guild.text_channels:
                perms = channel.overwrites_for(muted)
                perms.send_messages = False
                await channel.set_permissions(muted, overwrite=perms)
            for channel in ctx.guild.voice_channels:
                perms = channel.overwrites_for(muted)
                perms.connect = False
                await channel.set_permissions(muted, overwrite=perms)
        muted_members = []
        for victim in victims:  #iterate through the mentioned users
            #if the member mentioned has mod permissions or is an admin
            if (victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator) and not victim.bot:
                embed = discord.Embed(color=0xde2f43, description=':x: That user is a mod/admin.')
                await ctx.send(embed=embed)
            elif muted in victim.roles: #if the user is already muted
                embed = discord.Embed(color=0xde2f43, description=':x: That user is already muted.')
                await ctx.send(embed=embed)
            else:   #if the user passed the above checks
                if not victim.bot:
                    await victim.add_roles(muted)
                    muted_members.append(victim)
                    try:
                        dm = await victim.create_dm()
                        message = discord.Embed(color=0xff0000, title=f"You've been muted in **{ctx.guild.name}**.", description=f"**Reason**: {reason}", timestamp=datetime.datetime.utcnow())
                        message.set_thumbnail(url=ctx.guild.icon_url)
                        await dm.send(embed=message)
                    except:
                        pass
                else:
                    await victim.add_roles(muted)   #add the role to the user
                    muted_members.append(victim)    #add the user to a list of muted users
        if len(muted_members) > 0:  #if at least one member was muted
            _list = ', '.join(victim.mention for victim in muted_members)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Successfully muted** {_list}**.**')
            await ctx.send(embed=embed)
            await asyncio.sleep(convert_time_to_seconds(time))  #wait for the time to pass
            for victim in muted_members:
                await victim.remove_roles(muted)    #remove the role from the members

    @commands.command(help="unmute/mass unmute users", usage="unmute @user(s)###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unmute(self, ctx, victims : commands.Greedy[discord.Member]=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        try:
            result = guild_collection.find_one({"_id": ctx.guild.id})
            muted = result["mutedrole"]
            if muted is None:
                raise KeyError
        except Exception as error:
            if isinstance(error, KeyError):
                embed = discord.Embed(color=0xde2f43, description=':x: No muted role found.')
                return await ctx.send(embed=embed)
            else:
                raise
        unmuted_list = []
        for victim in victims:  #iterate through the mentioned users
            #if the member mentioned has mod permissions or is an admin
            if victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator:
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
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Successfully unmuted** {_list}**.**')
            await ctx.send(embed=embed)

    @commands.command(help="kick/mass kick users", usage="kick @user(s) <reason>`[optional]`###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def kick(self, ctx, victims : commands.Greedy[discord.Member]=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        kicked_list = []
        for victim in victims:
            if (victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator) and not victim.bot:
                embed = discord.Embed(color=0xde2f43, description=':x: This user is a mod/admin.')
                return await ctx.send(embed=embed)
            else:
                if not victim.bot:
                    await victim.kick(reason=reason)
                    kicked_list.append(victim)
                    try:
                        dm = await victim.create_dm()
                        message = discord.Embed(color=0xff0000, title=f"You've been kicked from **{ctx.guild.name}**.", description=f"**Reason**: {reason}")
                        message.set_thumbnail(url=ctx.guild.icon_url)
                        await dm.send(embed=message)
                    except:
                        pass
                else:
                    await victim.kick(reason=reason)
                    kicked_list.append(victim)
        if len(kicked_list) > 0:
            _list = ', '.join(victim.mention for victim in kicked_list)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Successfully kicked** {_list}**.**')
            await ctx.send(embed=embed)
        
    @commands.command(help="ban/mass ban users", usage="ban @user(s) <reason>`[optional]`###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    #Greedy and Union will allow you to ban guild members and users outside of the guild
    async def ban(self, ctx, victims : commands.Greedy[typing.Union[discord.Member, discord.User]]=None, *, reason=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim(s).')
            return await ctx.send(embed=embed)
        banned_list = []
        for victim in victims:
            if victim in ctx.guild.members: #check if the user is a guild member and the look if he got mod perms
                if (victim.guild_permissions.manage_messages or victim.guild_permissions.kick_members or victim.guild_permissions.ban_members or victim.guild_permissions.administrator) and not victim.bot:
                    embed = discord.Embed(color=0xde2f43, description=':x: This user is a mod/admin.')
                    return await ctx.send(embed=embed)
                else:   #ban the member if doesn't have permissions
                    await ctx.guild.ban(victim, reason=reason, delete_message_days=1)
                banned_list.append(victim)
            else:   #if the user is not in the guild, ban him from the guild
                if not victim.bot:
                    await ctx.guild.ban(victim, reason=reason, delete_message_days=1)
                    banned_list.append(victim)
                    try:
                        dm = await victim.create_dm()
                        message = discord.Embed(color=0xff0000, title=f"You've been banned in **{ctx.guild.name}**.", description=f"**Reason**: {reason}")
                        message.set_thumbnail(url=ctx.guild.icon_url)
                        await dm.send(embed=message)
                    except:
                        pass
                else:
                    await ctx.guild.ban(victim, reason=reason, delete_message_days=1)
                    banned_list.append(victim)
        if len(banned_list) > 0:
            _list = ', '.join(victim.mention for victim in banned_list)
            embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Successfully banned** {_list}**.**')
            await ctx.send(embed=embed)

    @commands.command(help="unban/mass unban users", usage="unban <user>(id, username#discriminator)###3s/user###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def unban(self, ctx, victims: commands.Greedy[discord.User]=None):
        if victims is None:
            embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
            return await ctx.send(embed=embed)
        users = []
        for victim in victims:
            await ctx.guild.unban(victim)
            banned_user = str(victim).split("=", 1)
            users.append(victim.mention)
        _list = ', '.join(users)
        embed = discord.Embed(color=0x75b254, description=f':white_check_mark: **Successfully unbanned** {_list}**.**')
        await ctx.send(embed=embed)
    
    #not so sure about this command
    #it will need some reworking in the future
    """@commands.command(aliases=['tempban'], help="needs reworking", usage="-###-###No")
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def softban(self, ctx, victim : discord.Member, time=None, *, reason=None):
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
            await ctx.guild.unban(user)"""

    #unban all the users that have been banned in the guild
    @commands.command(help="unban all banned users from this server (acces restricted for everyone besides the server owner)",
        usage="unbanall###10s/user###No"
    )
    @CustomChecks.blacklist_check()
    @CustomChecks.guild_owner_check()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unbanall(self, ctx):
        banned_users = await ctx.guild.bans()   #get all the banned users
        for ban_entry in banned_users:  #unban them one by one
            user = ban_entry.user
            await ctx.guild.unban(user)
        embed = discord.Embed(color=0x75b254, description=':white_check_mark: **Successfully unbanned all guild bans.**')
        await ctx.send(embed=embed)

    #below is some work in progress
    #I will try to make some audit log commands to ease the acces to it

    """
    @commands.group(case_insensitive=True, aliases=['audit'])
    @CustomChecks.blacklist_check()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def auditlog(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title=":books: Audit Log Commands", color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f"Requested by {ctx.message.author}")
            embed.description = '**Access the Audit Log of the server with ease using these commands (acknowledge that you need administrator permissions)**\n'
            embed.description += f"{ctx.prefix}audit recent: Get the most recent events."
            await ctx.send(embed=embed)

    @auditlog.command()
    @CustomChecks.blacklist_check()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def recent(self, ctx):
        menu = PaginatedMenu(ctx)
        menu.set_timeout(60)
        menu.allow_multisession()
        embed_list = list()
        for x in range(0, 9):
            async for event in ctx.guild.audit_logs():
                embed = discord.Embed(title=':watch: Most Recent Events', color=0xff0000, timestamp=datetime.datetime.utcnow())
                embed.set_footer(icon_url=ctx.message.author.avatar_url, text=f'Requested by {ctx.message.author}')
                embed.description = ''
                user = event.user.mention
                action = event.action
                time = event.created_at.utcnow()
                if event.target is None or event.target is discord.Emoji:
                    embed.description += f"{user}: {action} at {time}\n"
                else:
                    target = event.target.mention
                    embed.description += f"{user}: {action} - {target} at {time}\n"
            embed_list.append(embed)
        menu.add_pages(embed_list)    
        await menu.open()
    """

def setup(bot):
    bot.add_cog(Mod(bot))
