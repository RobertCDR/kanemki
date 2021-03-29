import discord
from discord.ext import commands
from discord.ext.commands import CheckFailure, CommandOnCooldown
from config import guild_collection, user_collection

#a custom checks class meant to create some decorators for the bot's commands
class CustomChecks():

    #check if the user is or not in the bot blacklist of the guild
    def blacklist_check():
        def predicate(ctx):
            try:
                results = guild_collection.find_one({"_id": ctx.author.id})
                if results is not None:
                    return False
                else:
                    return True
            except Exception as error:
                raise error
        return commands.check(predicate)

    #check if the user is the server owner or me (for blacklisting users)
    def blacklist_perm_check():
        def predicate(ctx):
            return ctx.author is ctx.guild.owner or ctx.author.id == 465138950223167499
        return commands.check(predicate)

    def guild_owner_check():
        def predicate(ctx):
            return ctx.author is ctx.guild.owner
        return commands.check(predicate)

    def rep_points_check():
        def predicate(ctx):
            try:
                result = user_collection.find_one({"_id": ctx.author.id})
                points = result["rep_points"]
            except Exception as error:
                if isinstance(error, KeyError):
                    return True
                else:
                    raise error
            if points > 0:
                return True
            else:
                return False
        return commands.check(predicate)

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #the global error handler
    #it's a lil bit tricky having both global and local handlers so be careful
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):    #if the command already has a local handler ignore every error raised by it (keep that in mind)
            return
        error = getattr(error, "original", error)   #unwrap the error
        if isinstance(error, commands.CommandNotFound):   #if the command does not exist
            embed = discord.Embed(color=0xbf1932, description=':exclamation: Invalid Command')
            await ctx.send(embed=embed)
        elif isinstance(error, CheckFailure):   #if the person does not meet the permissions necessary for the command
            if ctx.command.qualified_name == 'reputation':
                embed = discord.Embed(color=0xff0000, description='**You already gave a reputation point to someone today!**')
                embed.set_author(icon_url=ctx.author.avatar_url, name=ctx.author)
                embed.set_footer(icon_url=self.bot.user.avatar_url, text='Reputation points reset every 24 hours.')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xfccc51, description=':warning: You are either blacklisted from using the bot on this server or you do not meet the permissions required for this command.')
                await ctx.send(embed=embed)
        elif isinstance(error, CommandOnCooldown):  #self explanatory
            embed = discord.Embed(color=0xff0000, description=f"You can use this command again in {round(error.retry_after, 2)} seconds.")
            embed.set_author(name="Easy on there, Kaneki", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadInviteArgument): #if it's bad invite url
            embed = discord.Embed(color=0xde2f43, description=':x: Invalid invite.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.RoleNotFound):  #self explanatory
            embed = discord.Embed(color=0xde2f43, description=':x: Role not found.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):   #self explanatory
            embed = discord.Embed(color=0xde2f43, description=':x: Channel not found.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.UserNotFound):  #self explanatory
            embed = discord.Embed(color=0xde2f43, description=':x: User not found.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):  #self explanatory
            embed = discord.Embed(color=0xde2f43, description=':x: Member not found.')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandInvokeError):    #if an error occurs while invoking the command
            if ctx.command.qualified_name == 'agedays':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify your birthday in format `dd`/`mm`/`yyyy`.')
                await ctx.send(embed=embed)
            elif ctx.command.qualified_name == 'xkcd':
                embed = discord.Embed(color=0xfccc51, description=':warning: Enter a valid comic number.')
                await ctx.send(embed=embed)
            elif ctx.command.qualified_name == 'unban':
                embed = discord.Embed(color=0xde2f43, description=':x: Could not find that member.')
                await ctx.send(embed=embed)
            else:
                raise error
        elif isinstance(error, discord.Forbidden):   #when discord.Forbidden 403 occurs due to role hierarchy etc.
            embed = discord.Embed(color=0xde2f43, description=':x: Could not complete action due to missing permissions/role hierarchy/etc.')
            await ctx.send(embed=embed)
        elif isinstance(error, discord.NotFound):
            if ctx.command.qualified_name == 'unban':
                embed = discord.Embed(color=0xde2f43, description=':x: Unknown ban.')
                await ctx.send(embed=embed)
            else:
                raise error
        elif isinstance(error, commands.BadArgument): #if the argument passed in the command is not good (yes, shut up, I'm not good at explaining things)
            member_errors = ['userinfo', 'permissions', 'mute', 'unmute', 'kick', 'ban', 'softban', 'unban', 'pfp', 'award', '' 'fuck', 'hack', 'pula', 'gayrate', 'ship', 'hug', 'kiss', 'slap', 'wink', 'stare', 'lick', 'bite', 'cuddle', 'pat', 'smile', 'poke', 'tickle', 'point', 'punch']
            role_errors = ['roleinfo', 'rpermissions', 'config muted_set', 'config joinrole_set', 'config botrole_set']
            if ctx.command.qualified_name in member_errors:
                embed = discord.Embed(color=0xde2f43, description=':x: Could not find that member.')
                await ctx.send(embed=embed)
            elif ctx.command.qualified_name in role_errors:
                embed = discord.Embed(color=0xde2f43, description=':x: Role not found.')
                await ctx.send(embed=embed)
            elif ctx.command.qualified_name == 'clear':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify the amount of messages to clear.')
                await ctx.send(embed=embed)
            elif ctx.command.qualified_name == 'guess' or ctx.command.qualified_name == 'base2' or ctx.command.qualified_name == 'base10':
                await ctx.send('Not a valid number.')
            elif ctx.command.qualified_name == 'todo remove':
                await ctx.send('Not a valid item.')
            else:
                raise error
        elif isinstance(error, commands.MissingRequiredArgument):   #if the command is missing a parameter
            if error.param.name == 'victim':
                embed = discord.Embed(color=0xfccc51, description=':warning: Select your victim.')
                await ctx.send(embed=embed)
            elif error.param.name == 'invite':
                embed = discord.Embed(color=0xde2f43, description=':x: No invite given.')
                await ctx.send(embed=embed)
            elif error.param.name == 'role':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify a role.')
                await ctx.send(embed=embed)
            elif error.param.name == 'color':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify a Hex or RGB code.')
                await ctx.send(embed=embed)
            elif error.param.name == 'country':
                embed = discord.Embed(color=0xfccc51, description=':warning: Select a country.')
                await ctx.send(embed=embed)
            elif error.param.name == 'pair':
                embed = discord.Embed(color=0xde2f43, description=':heart: Select someone to ship.')
                await ctx.send(embed=embed)
            elif error.param.name == 'banned_user':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify the ID of the user.')
                await ctx.send(embed=embed)
            elif error.param.name == 'search':
                embed = discord.Embed(color=0x3c8bc7, description=':globe_with_meridians: Tell me what to look for.')
                await ctx.send(embed=embed)
            elif error.param.name == 'rolename':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify the name of the role.')
                await ctx.send(embed=embed)
            elif error.param.name == 'query':
                embed = discord.Embed(color=0xfccc51, description=':warning: Tell me what to look for.')
                await ctx.send(embed=embed)
            elif error.param.name == 'birthday':
                embed = discord.Embed(color=0xfccc51, description=':warning: Specify your birthday in format `dd`/`mm`/`yyyy`.')
                await ctx.send(embed=embed)
            elif error.param.name == 'member':
                embed = discord.Embed(color=0xfccc51, description=':warning: Mention someone.')
                await ctx.send(embed=embed)
            elif error.param.name == 'text':
                await ctx.send('gimme some text')
            elif error.param.name == 'awarded':
                await ctx.send('select someone to be awarded')
            elif error.param.name == 'awreas':
                await ctx.send('give a reason for the award')
            elif error.param.name == 'partner':
                await ctx.send('choose your freaky freaky partner')
            elif error.param.name == 'mimic':
                await ctx.send('what do you want me to say?')
            elif error.param.name == 'question':
                await ctx.send('ask me something first')
            elif error.param.name == 'birthday':
                await ctx.send('specify your birthday in format `dd`/`mm`/`yyyy`')
            elif error.param.name == 'nr2' or error.param.name == 'nr1':
                await ctx.send('input numbers')
            else:
                raise error
        else:   #if the error is none of the above, raise it in the terminal for further debugging (pain.)
            raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
