from typing import Counter
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from config import TOKEN
import jishaku

bot = commands.Bot(command_prefix=">>",case_insensitive=True, intents=discord.Intents.all())

@bot.command(aliases=["hello"])
async def hi(ctx):
    await ctx.send(f"Hello {ctx.message.author}")

@bot.command(aliases=["latency"]) 
async def ping(ctx):
    await ctx.send(f"The bot latency is {round((bot.latency)*1000)} ms")  

@bot.command(aliases=["support", "inv"])
async def invite(ctx):
    await ctx.send(f"Click [here](https://discord.com/api/oauth2/authorize?client_id=918501406443454484&permissions=8&scope=bot%20applications.commands) to invite the bot")

@bot.command(aliases=["clear"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Sucessfully cleared messages")

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please specify an amount to delete")   

@bot.command() 
async def github(ctx):
    await ctx.send(f"https://github.com/ScriptKidGithub/Python-Bot")  

bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print("Bot is online!")

bot.run(TOKEN)
