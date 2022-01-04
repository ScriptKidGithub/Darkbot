import discord
from discord.ext import commands

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["make_role", "role_create"]) # add error logging to this command
    @commands.has_permissions(manage_roles=True) 
    async def create_role(self, ctx, *, name):
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f"Successfully created a role with name `{name}`")

def setup(bot):
    bot.add_cog(Role(bot))