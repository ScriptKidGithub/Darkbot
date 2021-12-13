from typing import Counter
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from config import TOKEN
import jishaku

bot = commands.Bot(command_prefix=">>",case_insensitive=True, intents=discord.Intents.all())

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.message.author}")

@bot.command() 
async def ping(ctx):
    await ctx.send(f"The bot latency is {round((bot.latency)*1000)} ms")  

@bot.command()
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
