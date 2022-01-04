import discord
from discord.ext import commands

class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.command(aliases=["clear"], pass_context=True) # add error logging to this command
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Sucessfully cleared {amount} messages")

def setup(bot):
    bot.add_cog(Purge(bot))