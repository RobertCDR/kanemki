import discord
from discord.ext import commands, tasks
from cogs.errors import CustomChecks
import json
import datetime
import random
import PIL

class SocialnEconomy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.rep_points_reset.start()

    @commands.command(aliases=["rep"])
    @CustomChecks.blacklist_check()
    @CustomChecks.rep_points_check()
    async def reputation(self, ctx, user: discord.User=None):
        with open('./user data/reputation.json', 'r') as f:
            reputation = json.load(f)
        try:
            author_points = reputation[str(ctx.author.id)]['points']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(ctx.author.id)] = {}
                reputation[str(ctx.author.id)]['points'] = 1
                author_points = reputation[str(ctx.author.id)]['points']
            else:
                raise
        try:
            author_rep = reputation[str(ctx.author.id)]['reputation']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(ctx.author.id)]['reputation'] = 0
                author_rep = reputation[str(ctx.author.id)]['reputation']
            else:
                raise
        try:
            user_points = reputation[str(user.id)]['points']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(user.id)] = {}
                reputation[str(user.id)]['points'] = 1
                user_points = reputation[str(user.id)]['points']
            else:
                raise
        try:
            user_rep = reputation[str(user.id)]['reputation']
        except Exception as error:
            if isinstance(error, KeyError):
                reputation[str(user.id)]['reputation'] = 0
                user_rep = reputation[str(user.id)]['reputation']
            else:
                raise
        if author_points > 0:
            author_points -= 1
            user_rep += 1
            reputation[str(ctx.author.id)]['points'] = author_points
            reputation[str(user.id)]['reputation'] = user_rep
        reputation[str(ctx.author.id)]['reputation'] = author_rep
        reputation[str(user.id)]['points'] = user_points
        with open('./user data/reputation.json', 'w') as f:
            json.dump(reputation, f, indent=4)
        embed = discord.Embed(description=f":military_medal: {ctx.author.mention} **gave** {user.mention} **a reputation point!**", color=0xff0000)
        await ctx.send(embed=embed)

    

    """@tasks.loop(seconds=10, reconnect=True)
    async def rep_points_reset(self):
        with open('./user data/reputation.json', 'r') as f:
            reputation = json.load(f)
        for user in reputation:
            user['points'] = 1"""

def setup(bot):
    bot.add_cog(SocialnEconomy(bot))
