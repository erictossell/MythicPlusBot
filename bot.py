#---------------Take a Lap Discord Bot-----------------


#Imports
import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


#Load Environment variables
load_dotenv('configurations/main.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Set up Discord BOT with correct permissions
intents = discord.Intents(messages=True, guilds=True, members=True)
intents.message_content = True #v2
intents.presences = True #v2

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Activity(type=discord.ActivityType.watching, name="for !help"))

cogs_list = ['commands.general', 'commands.poll', 'events.errors', 'commands.raiderIO', 'events.memberEvents']

def load_extensions():
    for cog in cogs_list:
        bot.load_extension(cog)

async def main():
    load_extensions()
    await bot.start(TOKEN)

asyncio.run(main())