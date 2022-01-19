import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import bot_has_permissions
from discord.ext.commands.errors import BotMissingPermissions, MissingPermissions, MissingRequiredArgument, MissingRole
from discord.member import Member
from config import DEFAULT_PREFIX, TOKEN, DEFAULT_PREFIX, OWNER_ID
import jishaku
import datetime
import asyncio
import random
import time
from discord.ext.commands import CommandNotFound
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),case_insensitive=True,owner_id=OWNER_ID,strip_after_prefix=True,intents=discord.Intents.all()) 

bot.load_extension("jishaku")

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"📥 `cogs.{extension}`")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"📤 `cogs.{extension}`")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Command Error", description=f"```py\n{error}\n```")
    embed.color = 0x00ff00
    # embed2 = discord.Embed(title="Command Error", description=f"```py\n{error}\n```")
    # embed2.color = discord.Color.red
# add commmand name here - (ctx.command)
    await ctx.send(embed=embed)
    raise error

bot.run(TOKEN)
