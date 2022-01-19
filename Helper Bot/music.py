import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        voicechannel = ctx.author.voice.channel
        await voicechannel.connect()
        await ctx.send(f"Connected to {voicechannel}")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(Music(bot))
