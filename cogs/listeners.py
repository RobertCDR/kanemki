import discord
import json
from discord.ext import commands
import datetime

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #a listener for when the bot is removed from a guild
    #it removes the data stored in the guild data such as custom prefixes, roles
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
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
            with open('./guild data/botroles.json', 'r') as f:
                botrole = json.load(f)
            botrole.pop(str(guild.id))
            with open('./guild data/botroles.json', 'w') as f:
                json.dump(botrole, f, indent=4)
            with open('./guild data/welcome.json', 'r') as f:
                welcome = json.load(f)
            welcome.pop(str(guild.id))
            with open ('./guild data/welcome.json', 'w') as f:
                json.dump(welcome, f, indent=4)
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logsch.pop(str(guild.id))
            with open('./guild data/logsch.json', 'w') as f:
                json.dump(logsch, f, indent=4)
            with open ('./guild data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            prefixes.pop(str(guild.id))
            with open('./guild data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    #a listener which adds roles to bots/members when they join
    #the roles must be manually set using the config command
    #and this is exactly the problem, not fatal, but needs to be fixed because it raises an error if the guild does not have the roles set
    @commands.Cog.listener()
    async def on_member_join(self, member):
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
            else:
                raise
        #it wasn't a fatal error, but why see it raised in your terminal tho
        try:
            with open('./guild data/welcome.json', 'r') as f:
                welcome = json.load(f)
            channel = self.bot.get_channel(welcome[str(member.guild.id)][0])
            message = welcome[str(member.guild.id)][1]
            if message is not None:
                await channel.send(f"{member.mention} {message}")
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(member.guild.id)])
            embed = discord.Embed(
                color=0x2cff00, title='Member Joined', timestamp=datetime.datetime.utcnow(),
                description=f"{member.mention}\n**Account Created:** {member.created_at.__format__('%a, %d %b %Y %H:%M')}\n**ID:** {member.id}"
            )
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(member.guild.id)])
            roles = list(map(lambda x: x.mention, member.roles[::-1]))
            roles = roles[:-1]
            embed = discord.Embed(
                color=0xff0000, title='Member Left', timestamp=datetime.datetime.utcnow(),
                description=f"{member.mention}\n**Joined:** {member.joined_at.__format__('%a, %d %b %Y %H:%M')}\n**Roles:** {' '.join(roles)}\n**ID:** {member.id}"
            )
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise


    #todo continue this and fix problems
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(before.guild.id)])
            if before.nick != after.nick:
                embed = discord.Embed(
                    color=0x0019ff, title='Nickname Changed', timestamp=datetime.datetime.utcnow(),
                    description=f"{after.mention}\n**Before:** {before.nick}\n**After:** {after.nick}\n**ID:** {after.id}"
                )
                embed.set_author(name=after, icon_url=after.avatar_url)
                await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(guild.id)])
            if user in guild.members:
                roles = list(map(lambda x: x.mention, user.roles[::-1]))
                roles = roles[:-1]
                embed = discord.Embed(
                    color=0xff0000, title='Member Banned', timestamp=datetime.datetime.utcnow(),
                    description=f"{user.mention}\n**Joined at:** {user.joined_at.__format__('%a, %d %b %Y %H:%M')}\n**Roles:** {' '.join(roles)}\n**ID:** {user.id}"
                )
                embed.set_author(name=user, icon_url=user.avatar_url)
                embed.set_thumbnail(url=guild.icon_url)
            else:
                embed = discord.Embed(
                    color=0xff0000, title='User Banned', timestamp=datetime.datetime.utcnow(),
                    description=f"{user.mention}\n**ID:** {user.id}"
                )
                embed.set_author(name=user, icon_url=user.avatar_url)
                embed.set_thumbnail(url=user.avatar_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(guild.id)])
            embed = discord.Embed(
                    color=0x2cff00, title='User Unbanned', timestamp=datetime.datetime.utcnow(),
                    description=f"{user.mention}\n**ID:** {user.id}"
                )
            embed.set_author(name=user, icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(message.guild.id)])
            embed = discord.Embed(
                color=0xff0000, title='Message Deleted', timestamp=datetime.datetime.utcnow(),
                description=f"{message.author.mention}\n{message.content}\n**Channel: {message.channel.name}**\n**Author ID:** {message.author.id}\n**Message ID:** {message.id}\n**Channel ID:** {message.channel.id}"
            )
            embed.set_author(icon_url=message.author.avatar_url, name=message.author)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(messages[0].guild.id)])
            embed = discord.Embed(
                color=0xff0000, title='Bulk Message Delete', timestamp=datetime.datetime.utcnow(),
                description=f"**{len(messages)} messages**\n**Channel:** {messages[0].channel.mention}"
            )
            embed.set_thumbnail(url=messages[0].guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise


    #! links are took as edited messages which is pretty weird
    #! probable cause: links turn into embeds after being sent
    #todo fix needed
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(before.guild.id)])
            embed = discord.Embed(
                color=0x0019ff, title=f'Message Edited', timestamp=datetime.datetime.utcnow(),
                description=f"{before.author.mention}\n[Jump to message]({after.jump_url})\n**Author ID:** {before.author.id}"
            )
            embed.set_author(icon_url=before.author.avatar_url, name=before.author)
            embed.add_field(name='Before', value=f'{before.content}')
            embed.add_field(name='After', value=f'{after.content}')
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            elif isinstance(error, discord.HTTPException):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(channel.guild.id)])
            embed = discord.Embed(
                color=0x2cff00, title=f'Channel Created', timestamp=datetime.datetime.utcnow(),
                description=f"**{channel.name}**\n**Category:** {channel.category}\n**Position:** {channel.position}\n**Channel ID:** {channel.id}"
            )
            embed.set_thumbnail(url=channel.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(channel.guild.id)])
            embed = discord.Embed(
                color=0xff0000, title=f'Channel Deleted', timestamp=datetime.datetime.utcnow(),
                description=f"**{channel.name}**\n**Category:** {channel.category}\n**Position:** {channel.position}\n**Channel ID:** {channel.id}"
            )
            embed.set_thumbnail(url=channel.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(before.guild.id)])
            if (before.name is after.name) and (before.category is after.category) and (before.position is after.position):
                changes = 'No'
            else:
                changes = 'Yes'
            embed = discord.Embed(
                color=0x0019ff, title=f'Channel Edited', timestamp=datetime.datetime.utcnow(),
                description=f"**Before: {before.name}**\n**Category:** {before.category}\n**Position:** {before.position}\n \n"
            )
            embed.description += f"**After: {after.name}**\n**Category:** {after.category}\n**Position:** {after.position}\n**Permissions Changed:** {changes}\n\n**Channel ID:** {after.id}"
            embed.set_thumbnail(url=after.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(role.guild.id)])
            embed = discord.Embed(
                color=0x2cff00, title='Role Created', timestamp=datetime.datetime.utcnow(),
                description=f"**{role.name}**\n**Color:** {role.color}\n**Position:** {role.position}\n**Hoisted:** {role.hoist}\n**Mentionable:** {role.mentionable}\n**Role ID:** {role.id}"
            )
            embed.set_thumbnail(url=role.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(role.guild.id)])
            embed = discord.Embed(
                color=0xff0000, title='Role Deleted', timestamp=datetime.datetime.utcnow(),
                description=f"**{role.name}**\n**Color:** {role.color}\n**Position:** {role.position}\n**Hoisted:** {role.hoist}\n**Mentionable:** {role.mentionable}\n**Role ID:** {role.id}"
            )
            embed.set_thumbnail(url=role.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(after.guild.id)])
            if before.permissions.value != after.permissions.value:
                changes = 'Yes'
            else:
                changes = 'No'
            embed = discord.Embed(
                color=0x0019ff, title='Role Edited', timestamp=datetime.datetime.utcnow(),
                description=f"**Before: {before.name}**\n**Color:** {before.color}\n**Position:** {before.position}\n**Hoisted:** {before.hoist}\n**Mentionable:** {before.mentionable}\n\n"
            )
            embed.description += f"**After: {after.name}**\n**Color:** {after.color}\n**Position:** {after.position}\n**Hoisted:** {after.hoist}\n**Mentionable:** {after.mentionable}\n**Permissions Changed:** {changes}\n\n**Role ID:** {after.id}"
            embed.set_thumbnail(url=after.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.command()
    async def j(self, ctx):
        channel = self.bot.get_channel(592064545057538051)
        await channel.connect()

    @commands.command()
    async def l(self, ctx):
        voice_state = ctx.message.guild.voice_client
        await voice_state.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            with open('./guild data/logsch.json', 'r') as f:
                logsch = json.load(f)
            logs = self.bot.get_channel(logsch[str(member.guild.id)])
            if before.channel is None and after.channel is not None:
                embed = discord.Embed(
                    color=0x4f00ff, title='Joined Voice Channel', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Member ID:** {member.id}\n**Channel ID:** {after.channel.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.channel is not None and after.channel is None:
                embed = discord.Embed(
                    color=0x4f00ff, title='Left Voice Channel', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {before.channel.name}**\n**Category:** {before.channel.category}\n**Member ID:** {member.id}\n**Channel ID:** {before.channel.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.channel is not after.channel:
                embed = discord.Embed(
                    color=0x4f00ff, title='Switched Voice Channels', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Before:**\n**Channel: {before.channel.name}**\n**Category:** {before.channel.category}\n**Channel ID:** {before.channel.id}\n\n"
                )
                embed.description += f"**After:**\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n\n**Member ID:** {member.id}"
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.deaf is False and after.deaf is True:
                embed = discord.Embed(
                    color=0x4f00ff, title='Server Deafen', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n**Member ID:** {member.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.deaf is True and after.deaf is False:
                embed = discord.Embed(
                    color=0x4f00ff, title='Server Undeafen', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n**Member ID:** {member.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.mute is False and after.mute is True:
                embed = discord.Embed(
                    color=0x4f00ff, title='Server Mute', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n**Member ID:** {member.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.mute is True and after.mute is False:
                embed = discord.Embed(
                    color=0x4f00ff, title='Server Unmute', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n**Member ID:** {member.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            else:
                pass
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

def setup(bot):
    bot.add_cog(Listeners(bot))