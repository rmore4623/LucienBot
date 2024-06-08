# lucien.py
import os
import discord
import logging

from dotenv import load_dotenv
from discord.ext import commands
from config import member_roles

logging.basicConfig(filename="logs/lucen.log", level=logging.INFO)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
ADMIN_ID = os.getenv("LUCIEN_ADMIN")

description = "Lucien is a discord bot developed by srawalke."

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="/", description=description, intents=intents)

member_cache = {}


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    logging.info(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name} (id: {guild.id})\n\n"
    )


@bot.event
async def mute():
    global member_cache
    for member in member_cache.values():
        await member.edit(mute=True)


@bot.command()
async def get_cache(ctx):
    global member_cache
    if member_cache:
        member_strings = [str(member) for member in member_cache.values()]
        await ctx.send("\n".join(member_strings))
    else:
        await ctx.send("Cache is empty.")


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


@bot.command()
async def get_members(ctx):
    members = ctx.guild.members

    members = "\n".join(
        [str(member) for member in members if member.top_role.name in member_roles]
    )
    await ctx.send(members)


@bot.command()
async def add(ctx, left, right):
    """Adds two numbers together."""
    if left.isdigit() and right.isdigit():
        int_left, int_right = int(left), int(right)
        await ctx.send(int_left + int_right)
    elif isinstance(left, str) and isinstance(right, str):
        await ctx.send(left + right)
    else:
        await ctx.send("Invalid arguments")


bot.run(TOKEN)
