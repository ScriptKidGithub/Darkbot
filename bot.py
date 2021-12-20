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

bot = commands.Bot(command_prefix=commands.when_mentioned_or(DEFAULT_PREFIX),case_insensitive=True,owner_id=OWNER_ID,strip_after_prefix=True,intents=discord.Intents.all())

@bot.command(aliases=["hello"])
async def hi(ctx):
    await ctx.send(f"Hello {ctx.message.author}")

@bot.command(name="ping", aliases=["latency"], description="Replies with the websocket latency") 
async def ping(ctx):
    await ctx.send(f"The bot latency is {round((bot.latency)*1000)} ms")  

@bot.command(aliases=["support", "inv"])
async def invite(ctx):
    await ctx.send(f"Click [here](https://discord.com/api/oauth2/authorize?client_id=918501406443454484&permissions=8&scope=bot%20applications.commands) to invite the bot")

kicklog = bot.get_channel(920673040377978930)
@bot.command(aliases=["clear"], pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"Sucessfully cleared {amount} messages")
    await kicklog.send('hello')

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please specify an amount to delete") 

@bot.command(aliases=["make_role", "role_create"])
@commands.has_permissions(manage_roles=True) 
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f"Successfully created a role with name `{name}`")

@create_role.error
async def create_role_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please provide a role name!") 

@create_role.error
async def create_role_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"You donot have the proper roles to create roles! Required permission is `MANAGE_ROLES`") 

@bot.command()
@bot_has_permissions(kick_members=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason):
  await user.kick(reason=reason)
  await ctx.send(f"Kicked {user} with a reason `{reason}`")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send("Please mention someone to kick!") 

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"You donot have the proper permission to kick members! Required permission is `KICK_MEMBERS`")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, BotMissingPermissions):
        await ctx.send(f"{EMOTE_INFO} Please check my permissions! Required permission is `KICK_MEMBERS`")

############################################

@bot.command(hidden=False)
@bot_has_permissions(ban_members=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason):
  await user.ban(reason=reason)
  await ctx.send(f"Banned {user} with a reason `{reason}`")

########################33
@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(ERROR_LOG)
    await channel.send(error)
    raise error

  
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f"Please mention someone to ban!") 

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"You donot have the proper permission to ban members! Required permission is `BAN_MEMBERS`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, BotMissingPermissions):
        await ctx.send(f"I donot have the proper permissions to ban members! Required permission is `BAN_MEMBERS`")  

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

@bot.command(aliases=["gcreate", "gaw", "giveawaycreate"])
@commands.has_permissions(manage_guild=True)
async def giveaway(ctx):
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
@commands.has_permissions(manage_guild=True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_messsage(id_)
    except:
        await ctx.send("The provided id is incorrect! Please check the help command")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(bot.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention}! You are the new winner!")

@bot.command() 
async def github(ctx):
    await ctx.send(f"https://github.com/ScriptKidGithub/Python-Bot")  

start_time = time.time() 
@bot.command(aliases=["up"])
async def uptime(ctx):
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    await ctx.send(text)

bot.load_extension("jishaku")

@bot.event
async def check_bot_additions():
   _guilds = bot.guilds
   for g in _guilds:
    entries = g.audit_logs(action=discord.AuditLogAction.add_bot, limit=1)
    print("bot is adddeddd")

@bot.event
async def on_ready():

    status_channel = bot.get_channel(STATUS_LOG)
    print("Bot is online!")
    await status_channel.send(f"`{datetime.datetime.utcnow()}` | 🟢 Online `({round((bot.latency)*1000)} ms`)")
    
#@bot.event
#async def discord.on_connect():
 #   status_channel = bot.get_channel(STATUS_LOG)
  #  await status_channel.send(f"a joined a new server!")

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f"You donot have the proper permissions to host Giveaways! Required permission is `MANAGE_SERVER`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

bot.run(TOKEN)
