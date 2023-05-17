#---------------Take a Lap Discord Bot-----------------
# Description: This file contains the main function for the bot.
# Author: Eriim

#Imports
import os
import discord
from dotenv import load_dotenv

#Load Environment variables
load_dotenv('configurations/main.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
SUPPORT_CHANNEL_ID = os.getenv('SUPPORT_CHANNEL_ID')
SUPPORT_SERVER_ID = os.getenv('SUPPORT_SERVER_ID')

#Set up Discord BOT with correct permissions
intents = discord.Intents( guilds=True, members=True)
intents.guilds = True

bot = discord.Bot(intents=intents,
                   activity=discord.Activity(type=discord.ActivityType.watching,
                                             name="for slash commands!"))

cogs_list = ['app.commands.general_cog',
             'app.commands.admin_cog',
             'app.commands.member_events_cog',
             'app.commands.guild_cog',
             'app.commands.character_cog',
             'app.commands.announcement_cog']

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
