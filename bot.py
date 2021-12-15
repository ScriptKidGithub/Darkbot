from typing import Counter
import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from config import TOKEN
import jishaku
import datetime
import asyncio
import random

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

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@bot.command()
@commands.has_role("cheeeese")
async def gstart(ctx):
    await ctx.send("Let us start with the Giveaway! Answer the questions within 25 seconds!")

    questions = ["Which channel should the Giveaway be hosted in?",
                "What should be the duration of the Giveaway?",
                "What should be the prize for the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await bot.wait_for("message", timeout=25.0, check = check)
        except asyncio.TimeoutError:
            await ctx.send("You did not answer in time! Please be quicker next time!")
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You did the mention the channel properly! Check the help command")
        return

    channel = bot.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send("You did the mention the duration propely! Please check the help command")
        return
    elif time == -2:
        await ctx.send("You did the mention the duration propely! Please check the help command")
        return

    prize = answers[2]

    await ctx.send(f"The Giveaway is successfully hosted in {channel.mention} for {answers[1]}")

    embed = discord.Embed(title = f"{prize}", description = "Hosted by ...", color = ctx.author.color)

    embed.set_footer(text = f"Ends in {answers[1]}")

    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention}! You won {prize}!")

@bot.command()
@commands.has_role("cheeeese")
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_messsage(id_)
    except:
        await ctx.send("The provided id is incorrect! Please check the help command")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention}! ")

@bot.command() 
async def github(ctx):
    await ctx.send(f"https://github.com/ScriptKidGithub/Python-Bot")  

bot.load_extension("jishaku")

@bot.event
async def on_ready():
    print("Bot is online!")

bot.run(TOKEN)
