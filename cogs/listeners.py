import discord
import json
from discord.ext import commands

class Listeners(commands.Cog):
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

def setup(bot):
    bot.add_cog(Listeners(bot))