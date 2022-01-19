import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clear"]) # add error logging to this command
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        if amount is None:
            await ctx.send("No amount provided brruh!!")
        elif amount > 1000:
            await ctx.send("You cannot purge more than 1000 bruh!!")
        else:
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(f"Sucessfully cleared {amount} messages")
            
        @commands.command()
    @commands.has_permissions(kick_members=True) # add timout perms here
    async def timeout(self, ctx, member: discord.Member, minutes: int):
        duration = datetime.timedelta(minutes=minutes)
        await member.timeout_for(duration)
        await ctx.reply(f"{member} timed out for {minutes} minutes.")
        await ctx.send(member.timed_out)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason):
        await user.kick(reason=reason)
        await ctx.send(f"Kicked {user} with a reason `{reason}`")

    @commands.command(hidden=False) # add error logging to this command
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason):
        await user.ban(reason=reason)
        await ctx.send(f"Banned {user} with a reason `{reason}`")

def setup(bot):
    bot.add_cog(Moderation(bot))
