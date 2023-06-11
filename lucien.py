# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents = discord.Intents.default())

@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break
    
    print(f'{client.user} has connected to Discord!\n')

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    for guild in client.guilds:
        for member in guild.members:
            print(member)


client.run(TOKEN)