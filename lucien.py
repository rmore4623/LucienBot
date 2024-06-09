# lucien.py
import os
import discord
import logging

from dotenv import load_dotenv
from discord.ext import commands
from config import member_roles

logging.basicConfig(filename="logs/lucien.log", level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
ADMIN_ID = os.getenv("LUCIEN_ADMIN")

description = "Lucien is a Discord bot developed by srawalke."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", description=description, intents=intents)

member_cache = {}


"""
An event handler that is called when the bot has successfully connected to the server.
Will log the server name and id that the bot is connected to.
"""
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    logging.info(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name} (id: {guild.id})\n\n"
    )


"""
An event handler that is called when a message is sent in the server.
Author of the message will be checked against the member_cache.
If the author is in the member_cache, the message will be deleted.
"""
@bot.event
async def on_message(message):
    global member_cache
    if message.author.id in member_cache:
        await message.delete()
        await bot.process_commands(message)
    else:
        await bot.process_commands(message)


"""
A command that will return the list of members that are currently cached.
"""
@bot.command()
async def get_cache(ctx):
    global member_cache
    if member_cache:
        member_strings = [str(member) for member in member_cache.values()]
        await ctx.send("\n".join(member_strings))
    else:
        await ctx.send("Cache is empty.")


"""
A command that will add members specified in the arguments to the member_cache.
If the member is not found in the member_cache, a message will be sent.
"""
@bot.command()
async def set_mute_member(ctx, *args):
    global member_cache
    if ctx.author.name != ADMIN_ID:
        await ctx.send("You are not authorized to use this command.")
        return

    member = None

    if not args:
        await ctx.send("No arguments provided.")
        return

    for arg in args:
        for mbr in ctx.guild.members:
            if arg == mbr.name:
                member = mbr

        if not member:
            await ctx.send(
                f"MEMBER `{arg}` NOT FOUND.\n\nTry getting a list of members using `/get_members`"
            )
            return

        member_cache[member.id] = member
        await ctx.send(f"Member `{member}` has been cached.")


"""
A command that will display the list of members in the server.
Only members with roles specified in the member_roles list will be displayed.
"""
@bot.command()
async def get_members(ctx):
    members = ctx.guild.members

    members = "\n".join(
        [str(member) for member in members if member.top_role.name in member_roles]
    )
    await ctx.send(members)


"""
A command that will determine if the arguments are integers or strings.
If the arguments are integers, they will be added together.
If the arguments are strings, they will be concatenated.
If the arguments are not integers or strings, an error message will be sent.
"""
@bot.command()
async def add(ctx, left, right):
    """Adds two numbers together."""
    if left.isdigit() and right.isdigit():
        await ctx.send(int(left) + int(right))
    elif isinstance(left, str) and isinstance(right, str):
        await ctx.send(left + right)
    else:
        await ctx.send("Invalid arguments")


bot.run(TOKEN)
