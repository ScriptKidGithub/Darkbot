import discord
from discord.ext import commands
from config import TOKEN
import jishaku

bot = commands.Bot(command_prefix=">>",case_insensitive=True, intents=discord.Intents.all())

@bot.command()
async def hi(ctx):
    await ctx.send(f"Hello {ctx.message.author}")

@bot.command() 
async def ping(ctx):
    await ctx.send(f"The bot latency is {round((bot.latency)*1000)} ms")  

bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print("Bot is online!")

bot.run(TOKEN)
