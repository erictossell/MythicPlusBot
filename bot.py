#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the main function for the bot.
# Author: Eriim

#Imports
import os
import logging
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
intents.guilds = True
intents.guild_messages = True


bot = commands.Bot(intents=intents,
                   activity=discord.Activity(type=discord.ActivityType.watching,
                                             name="for !help"))

cogs_list = ['commands.general_cog',
             'commands.poll_cog',
             'commands.errors_cog',
             'commands.raider_io_cog',
             'commands.member_events_cog',
             'commands.leaderboard_cog',
             'commands.character_cog']

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def load_extensions():
    """Load the cogs from the cogs_list.
    """
    for cog in cogs_list:
        bot.load_extension(cog)

def main():
    """The main function for the bot."""
    load_extensions()
    bot.run(os.getenv('DISCORD_TOKEN'))

main()
