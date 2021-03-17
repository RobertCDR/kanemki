import discord
from discord.ext import commands
import datetime
import config
from pymongo import MongoClient

cluster = MongoClient(config.db_client)
database = cluster["KanemkiDB"]
guild_collection = database["guilddata"]

#! this is still kind of f-ed up because of previous bugs which I thought I had fixed
#* I mean it does it's job, but some things are off
#todo guess I'll need to investigate further...

class Listeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #creates a default value for the prefix when the bot joins a guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        prefix = {"_id": guild.id, "prefix": ">"}
        guild_collection.insert_one(prefix)

    #when the bot is removed from the guild, remove the data stored about it
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guild_collection.find_one_and_delete({"_id": guild.id})

    @commands.Cog.listener()
    async def on_member_join(self, member):
        result = guild_collection.find_one({"_id": member.guild.id})
        try:
            if member.bot:
                role = result["botrole"]
                role = discord.utils.get(member.guild.roles, id=role)   #get the role
            else:
                role = result["joinrole"]
                role = discord.utils.get(member.guild.roles, id=role)   #get the role
            await member.add_roles(role)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise error
        try:
            channel = result["welcomech"]
            channel = self.bot.get_channel(channel)
            message = result["welcomemsg"]
            await channel.send(f"{message} {member.mention}")
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise error
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
                raise error

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        result = guild_collection.find_one({"_id": member.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
                raise error

    #todo continue this and fix problems
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        result = guild_collection.find_one({"_id": before.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            if str(before.nick) != str(after.nick):
                embed = discord.Embed(
                    color=0x0019ff, title='Nickname Changed', timestamp=datetime.datetime.utcnow(),
                    description=f"{after.mention}\n**Before:** {before.nick}\n**After:** {after.nick}\n**ID:** {after.id}"
                )
                embed.set_author(name=after, icon_url=after.avatar_url)
                embed.set_thumbnail(url=after.guild.icon_url)
                await logs.send(embed=embed)
            elif len(before.roles) < len(after.roles):
                role = [x for x in after.roles if x not in before.roles]
                embed = discord.Embed(
                    color=0x0019ff, title='Role Given', timestamp=datetime.datetime.utcnow(),
                    description=f"{after.mention} {role[0].mention}\n**Role ID:** {role[0].id}\n**User ID:** {after.id}"
                )
                embed.set_author(name=f"{after} -> {role[0]}", icon_url=after.avatar_url)
                embed.set_thumbnail(url=after.guild.icon_url)
                await logs.send(embed=embed)
            elif len(before.roles) > len(after.roles):
                role = [x for x in before.roles if x not in after.roles]
                embed = discord.Embed(
                    color=0x0019ff, title='Role Removed', timestamp=datetime.datetime.utcnow(),
                    description=f"{after.mention} {role[0].mention}\n**Role ID:** {role[0].id}\n**User ID:** {after.id}"
                )
                embed.set_author(name=f"{after} -> {role[0]}", icon_url=after.avatar_url)
                embed.set_thumbnail(url=after.guild.icon_url)
                await logs.send(embed=embed)
            else:
                pass
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise error

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        result = guild_collection.find_one({"_id": guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
                raise error

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        result = guild_collection.find_one({"_id": guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
                raise error

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message is discord.Embed:
                pass
            else:
                result = guild_collection.find_one({"_id": message.guild.id})
                logs = result["logsch"]
                logs = self.bot.get_channel(logs)
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
                raise error

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, payload):
        result = guild_collection.find_one({"_id": payload.guild_id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            guild = self.bot.get_guild(payload.guild_id)
            channel = self.bot.get_channel(payload.channel_id)
            embed = discord.Embed(
                color=0xff0000, title='Bulk Message Delete', timestamp=datetime.datetime.utcnow(),
                description=f"**{len(payload.message_ids)} messages**\n**Channel:** {channel.name}"
            )
            embed.set_thumbnail(url=guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise error

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        result = guild_collection.find_one({"_id": before.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            embed = discord.Embed(
                color=0x0019ff, title='Message Edited', timestamp=datetime.datetime.utcnow(),
                description=f"{before.author.mention}\n[Jump to message]({after.jump_url})\n**Author ID:** {before.author.id}\n**Message ID:** {after.id}\n**Channel ID:** {after.channel.id}"
            )
            embed.set_author(icon_url=before.author.avatar_url, name=before.author)
            embed.add_field(name='Before', value=before.content)
            embed.add_field(name='After', value=after.content, inline=False)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            elif isinstance(error, discord.HTTPException):
                pass
            else:
                raise error

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        result = guild_collection.find_one({"_id": channel.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            embed = discord.Embed(
                color=0x2cff00, title='Channel Created', timestamp=datetime.datetime.utcnow(),
                description=f"**{channel.name}**\n**Category:** {channel.category}\n**Position:** {channel.position}\n**Channel ID:** {channel.id}"
            )
            embed.set_thumbnail(url=channel.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise error

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        result = guild_collection.find_one({"_id": channel.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            embed = discord.Embed(
                color=0xff0000, title='Channel Deleted', timestamp=datetime.datetime.utcnow(),
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
        result = guild_collection.find_one({"_id": before.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            if (before.name is after.name) and (before.category is after.category) and (before.position is after.position):
                changes = 'No'
            else:
                changes = 'Yes'
            embed = discord.Embed(
                color=0x0019ff, title='Channel Edited', timestamp=datetime.datetime.utcnow(),
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
        result = guild_collection.find_one({"_id": role.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
        result = guild_collection.find_one({"_id": role.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
        result = guild_collection.find_one({"_id": before.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        result = guild_collection.find_one({"_id": invite.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            if invite.max_age == 0:
                max_age = "♾️"
            else:
                max_age = str(datetime.timedelta(seconds=invite.max_age)).split(".", 1)[0]
            if invite.max_uses == 0:
                max_uses = "♾️"
            else:
                max_uses = invite.max_uses
            embed = discord.Embed(
                color=0x5d6fb0, title="Invite Created", timestamp=datetime.datetime.utcnow(),
                description=f"**Max Age:** {max_age}\n**Temporary:** {invite.temporary}\n**Max Uses:** {max_uses}\n**Inviter:** {invite.inviter.mention}\n**Inviter ID** {invite.inviter.id}\n"
            )
            embed.description += f"**URL:** {invite.url}"
            embed.set_thumbnail(url=invite.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        result = guild_collection.find_one({"_id": invite.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
            embed = discord.Embed(
                color=0xff0000, title="Invite Deleted", timestamp=datetime.datetime.utcnow(),
                description=f"**URL:** {invite.url}"
            )
            embed.set_thumbnail(url=invite.guild.icon_url)
            await logs.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        result = guild_collection.find_one({"_id": member.guild.id})
        try:
            logs = result["logsch"]
            logs = self.bot.get_channel(logs)
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
            elif before.self_stream is False and after.self_stream is True:
                embed = discord.Embed(
                    color=0x4f00ff, title='Started Streaming', timestamp=datetime.datetime.utcnow(),
                    description=f"{member.mention}\n**Channel: {after.channel.name}**\n**Category:** {after.channel.category}\n**Channel ID:** {after.channel.id}\n**Member ID:** {member.id}"
                )
                embed.set_author(name=member, icon_url=member.avatar_url)
                embed.set_thumbnail(url=member.guild.icon_url)
                await logs.send(embed=embed)
            elif before.self_stream is True and after.self_stream is False:
                embed = discord.Embed(
                    color=0x4f00ff, title='Stopped Streaming', timestamp=datetime.datetime.utcnow(),
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
    """
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            with open('./guild data/starboards.json', 'r') as f:
                starboards = json.load(f)
            starboard = self.bot.get_channel(starboards[str(payload.guild_id)])
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji='⭐')
            #todo store the message id somewhere
            if reaction.count >= 1:
                embed = discord.Embed(color=0xffac33, description=f"{message.content}\n\n[Jump to message]({message.jump_url})", timestamp=datetime.datetime.utcnow())
                embed.set_author(icon_url=message.author.avatar_url, name=message.author)
                embed.set_footer(icon_url=message.guild.icon_url, text=f'★ {message.guild} Starboard')
                await starboard.send(embed=embed)
        except Exception as error:
            if isinstance(error, KeyError):
                pass
            else:
                raise
    """

def setup(bot):
    bot.add_cog(Listeners(bot))
