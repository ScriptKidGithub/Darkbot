import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import bot_has_permissions
from discord.ext.commands.errors import BotMissingPermissions, MissingPermissions, MissingRequiredArgument, MissingRole
from discord.member import Member
from config import DEFAULT_PREFIX, TOKEN, EMOTE_INFO, STATUS_LOG, DEFAULT_PREFIX, OWNER_ID, ERROR_LOG
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

bot.run(TOKEN)
