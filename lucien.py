# bot.py
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='?', description = description, intents=intents)


@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{client.user} has connected to Discord!\n')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})\n\n'
    )

    for guild in client.guilds:
        for member in guild.members:
            print(member)

@client.command()
async def add(ctx, left, right):
    """Adds two numbers together."""

    if left.isdigit() or right.isdigit():
        int_left = int(left)
        int_right = int(right)
        await ctx.send(int_left + int_right)
    elif isinstance(left, str) and isinstance(right, str):
        await ctx.send(left + right)
    else:
        # Handle unsupported types
        await ctx.send('Invalid arguments')


client.run(TOKEN)