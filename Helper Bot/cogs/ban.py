import discord
from discord.ext import commands

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=False) # add error logging to this command
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason):
        await user.ban(reason=reason)
        await ctx.send(f"Banned {user} with a reason `{reason}`")

def setup(bot):
    bot.add_cog(Ban(bot))