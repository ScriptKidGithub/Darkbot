import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user} with a reason `{reason}`")

def setup(bot):
    bot.add_cog(Kick(bot))