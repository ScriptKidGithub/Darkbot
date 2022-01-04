import discord
from discord.ext import commands
import datetime
import time

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["latency"], description="Replies with the websocket latency") 
    async def ping(self, ctx):
        await ctx.send(f"The bot latency is {round((self.bot.latency)*1000)} ms") 

    @commands.command(aliases=["support", "inv"])
    async def invite(ctx):
        await ctx.send(f"Click [here](https://discord.com/api/oauth2/authorize?client_id=918501406443454484&permissions=8&scope=bot%20applications.commands) to invite the bot")   
    
    @commands.command() 
    async def github(self, ctx):
        await ctx.send(f"https://github.com/ScriptKidGithub/Python-Bot")

'''
    start_time = time.time() 
    @commands.command(aliases=["up"])
    async def uptime(ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        await ctx.send(text)     FIX UPTIME ISSUE
''' 

def setup(bot):
    bot.add_cog(General(bot))