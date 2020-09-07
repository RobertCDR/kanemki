import discord
from discord.ext import commands
import numpy

#this is an experimental cog
#don't know how to make string based operations or how to parse the user input so I'll stick to this until I become a better programmer
class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['sum', 'add'])
    async def suma(self, ctx, *numbers : float):
        if not numbers:
            await ctx.send('Input numbers')
            return
        await ctx.send(numpy.sum(numbers))

    @commands.command(aliases=['reduce', 'diff'])
    async def subtract(self, ctx, nr1 : float, nr2 : float):
        await ctx.send(numpy.subtract(nr1, nr2))
    
    @commands.command(aliases=['times', 'multiply'])
    async def multy(self, ctx, *numbers : float):
        if not numbers:
            await ctx.send('Input numbers')
            return
        await ctx.send(numpy.prod(numbers))

    @commands.command(aliases=['div'])
    async def divide(self, ctx, nr1 : float, nr2 : float):
        await ctx.send(numpy.divide(nr1, nr2))

    @commands.command(aliases=['pow'])
    async def power(self, ctx, nr1 : float, nr2 : int):
        await ctx.send(numpy.power(nr1, nr2))

    @commands.command(aliases=['sqrt'])
    async def squareroot(self, ctx, nr1 : float):
        await ctx.send(numpy.sqrt(nr1))

    @commands.command(aliases=['log2'])
    async def logarithm2(self, ctx, nr1 : float):
        await ctx.send(numpy.log2(nr1))

    @commands.command(aliases=['lg', 'log10'])
    async def logarithm10(self, ctx, nr1 : float):
        await ctx.send(numpy.log10(nr1))

def setup(bot):
    bot.add_cog(Math(bot))